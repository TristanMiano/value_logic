"""Array-only Python and C++ implementations of the repaired semantic kernel."""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from experiments.build_cpp_kernel import build_cpp_kernel, library_path


REFUTED = np.int8(0)
OPEN = np.int8(1)
SUPPORTED = np.int8(2)


@dataclass(frozen=True)
class KernelInputs:
    """One block of primitive arrays; no row owns a Python record."""

    structured_raw: np.ndarray
    ce_logits: np.ndarray
    schema: np.ndarray
    threshold: np.ndarray
    evidence_present: np.ndarray
    evidence_valid: np.ndarray
    can_support: np.ndarray
    can_refute: np.ndarray
    eta: np.ndarray
    center_eta: np.ndarray
    binding_ok: np.ndarray
    center_binding_ok: np.ndarray

    def normalized(self) -> "KernelInputs":
        structured = np.ascontiguousarray(self.structured_raw, dtype=np.float32)
        logits = np.ascontiguousarray(self.ce_logits, dtype=np.float32)
        if structured.ndim != 2 or structured.shape[1] != 4:
            raise ValueError("structured_raw must have shape (row, 4)")
        if logits.shape != (len(structured), 3):
            raise ValueError("ce_logits must have shape (row, 3)")
        count = len(structured)

        def vector(value: np.ndarray, dtype: np.dtype) -> np.ndarray:
            array = np.ascontiguousarray(value, dtype=dtype)
            if array.shape != (count,):
                raise ValueError("every kernel metadata array must have shape (row,)")
            return array

        result = KernelInputs(
            structured,
            logits,
            vector(self.schema, np.int8),
            vector(self.threshold, np.float64),
            vector(self.evidence_present, np.uint8),
            vector(self.evidence_valid, np.uint8),
            vector(self.can_support, np.uint8),
            vector(self.can_refute, np.uint8),
            vector(self.eta, np.float64),
            vector(self.center_eta, np.float64),
            vector(self.binding_ok, np.uint8),
            vector(self.center_binding_ok, np.uint8),
        )
        if not np.isin(result.schema, (0, 1)).all():
            raise ValueError("schema must contain only 0 (loss) or 1 (latency)")
        if not (np.isfinite(result.structured_raw).all() and np.isfinite(result.ce_logits).all()):
            raise ValueError("model outputs must be finite")
        if not np.isfinite(result.threshold).all():
            raise ValueError("thresholds must be finite")
        for radii in (result.eta, result.center_eta):
            if np.any(np.isfinite(radii) & (radii < 0.0)):
                raise ValueError("finite calibration radii must be nonnegative")
        return result


@dataclass(frozen=True)
class KernelOutputs:
    structured_state: np.ndarray
    center_state: np.ndarray
    shadow_state: np.ndarray
    ce_state: np.ndarray
    self_confidence_state: np.ndarray
    support_margin: np.ndarray
    refutation_margin: np.ndarray
    support_relu: np.ndarray
    refutation_relu: np.ndarray


def _decode_region(
    lower: np.ndarray,
    upper: np.ndarray,
    threshold: np.ndarray,
    usable: np.ndarray,
    can_support: np.ndarray,
    can_refute: np.ndarray,
) -> np.ndarray:
    values = np.full(len(lower), OPEN, dtype=np.int8)
    support = usable & can_support & (upper <= threshold)
    refute = usable & can_refute & (lower > threshold)
    values[support] = SUPPORTED
    values[refute] = REFUTED
    return values


def numpy_decode_block(inputs: KernelInputs) -> KernelOutputs:
    """Readable reference implementation used for differential testing."""

    data = inputs.normalized()
    rows = np.arange(len(data.schema))
    scales = np.where(data.schema == 0, 0.1, 10.0).astype(np.float64)
    centers = data.structured_raw[rows, np.where(data.schema == 0, 0, 2)].astype(np.float64)
    radii = data.structured_raw[rows, np.where(data.schema == 0, 1, 3)].astype(np.float64)
    centers *= scales
    radii = np.maximum(radii, 0.0) * scales
    present = data.evidence_present.astype(bool)
    valid = data.evidence_valid.astype(bool)
    supports = data.can_support.astype(bool)
    refutes = data.can_refute.astype(bool)

    full_radius = radii + data.eta
    lower = centers - full_radius
    upper = centers + full_radius
    structured = _decode_region(
        lower,
        upper,
        data.threshold,
        data.binding_ok.astype(bool) & present & valid,
        supports,
        refutes,
    )
    center = _decode_region(
        centers - data.center_eta,
        centers + data.center_eta,
        data.threshold,
        data.center_binding_ok.astype(bool) & present & valid,
        supports,
        refutes,
    )
    shadow = _decode_region(
        centers - radii,
        centers + radii,
        data.threshold,
        present & valid,
        supports,
        refutes,
    )

    ce = np.argmax(data.ce_logits, axis=1).astype(np.int8)
    ce[(~present) | (~valid) | ((ce == SUPPORTED) & ~supports) | ((ce == REFUTED) & ~refutes)] = OPEN
    logits = data.ce_logits.astype(np.float64)
    exponentials = np.exp(logits - logits.max(axis=1, keepdims=True))
    confidence = exponentials.max(axis=1) / exponentials.sum(axis=1)
    self_confidence = np.where(confidence >= 0.5, SUPPORTED, OPEN).astype(np.int8)

    support_margin = (data.threshold - upper).astype(np.float32)
    refutation_margin = (lower - data.threshold).astype(np.float32)
    support_relu = np.maximum(0.0, (data.threshold - upper) / scales).astype(np.float32)
    refutation_relu = np.maximum(0.0, (lower - data.threshold) / scales).astype(np.float32)
    return KernelOutputs(
        structured,
        center,
        shadow,
        ce,
        self_confidence,
        support_margin,
        refutation_margin,
        support_relu,
        refutation_relu,
    )


class CppKernel:
    """Thin block-level wrapper around the C ABI; it owns no experiment data."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = library_path() if path is None else Path(path)
        self.library = ctypes.CDLL(str(self.path))
        self.function = self.library.vl_decode_block_v1
        p_float = ctypes.POINTER(ctypes.c_float)
        p_double = ctypes.POINTER(ctypes.c_double)
        p_i8 = ctypes.POINTER(ctypes.c_int8)
        p_u8 = ctypes.POINTER(ctypes.c_uint8)
        self.function.argtypes = [
            ctypes.c_int64,
            p_float,
            p_float,
            p_i8,
            p_double,
            p_u8,
            p_u8,
            p_u8,
            p_u8,
            p_double,
            p_double,
            p_u8,
            p_u8,
            p_i8,
            p_i8,
            p_i8,
            p_i8,
            p_i8,
            p_float,
            p_float,
            p_float,
            p_float,
        ]
        self.function.restype = ctypes.c_int

    @staticmethod
    def _pointer(array: np.ndarray, scalar: type[ctypes._SimpleCData]) -> ctypes._Pointer:
        return array.ctypes.data_as(ctypes.POINTER(scalar))

    def decode(self, inputs: KernelInputs) -> KernelOutputs:
        data = inputs.normalized()
        count = len(data.schema)
        states = [np.empty(count, dtype=np.int8) for _ in range(5)]
        floats = [np.empty(count, dtype=np.float32) for _ in range(4)]
        status = self.function(
            count,
            self._pointer(data.structured_raw, ctypes.c_float),
            self._pointer(data.ce_logits, ctypes.c_float),
            self._pointer(data.schema, ctypes.c_int8),
            self._pointer(data.threshold, ctypes.c_double),
            self._pointer(data.evidence_present, ctypes.c_uint8),
            self._pointer(data.evidence_valid, ctypes.c_uint8),
            self._pointer(data.can_support, ctypes.c_uint8),
            self._pointer(data.can_refute, ctypes.c_uint8),
            self._pointer(data.eta, ctypes.c_double),
            self._pointer(data.center_eta, ctypes.c_double),
            self._pointer(data.binding_ok, ctypes.c_uint8),
            self._pointer(data.center_binding_ok, ctypes.c_uint8),
            *(self._pointer(array, ctypes.c_int8) for array in states),
            *(self._pointer(array, ctypes.c_float) for array in floats),
        )
        if status != 0:
            meanings = {
                1: "null pointer",
                2: "negative row count",
                3: "invalid schema",
                4: "nonfinite model output or threshold",
                5: "negative finite calibration radius",
            }
            raise RuntimeError(f"C++ semantic kernel failed: {meanings.get(status, status)}")
        return KernelOutputs(*states, *floats)


def built_cpp_kernel(*, force: bool = False) -> CppKernel:
    build_cpp_kernel(force=force)
    return CppKernel()


def assert_kernel_equivalence(reference: KernelOutputs, candidate: KernelOutputs) -> None:
    for name in (
        "structured_state",
        "center_state",
        "shadow_state",
        "ce_state",
        "self_confidence_state",
    ):
        if not np.array_equal(getattr(reference, name), getattr(candidate, name)):
            raise AssertionError(f"C++ and NumPy differ in {name}")
    for name in (
        "support_margin",
        "refutation_margin",
        "support_relu",
        "refutation_relu",
    ):
        if not np.array_equal(getattr(reference, name), getattr(candidate, name)):
            maximum = float(np.max(np.abs(getattr(reference, name) - getattr(candidate, name))))
            raise AssertionError(f"C++ and NumPy differ in {name}; max_abs={maximum}")
