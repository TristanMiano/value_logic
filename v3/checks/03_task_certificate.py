"""Named-action terminal certificate, DEVELOPMENT P3-03.

Contributor: ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction agent.
The complete supplied catalogue is the comparison scope. Compilation, guarding,
hashing and threshold comparisons are boundary work outside core allowances.
Local resid(f, g) means max(0, f-g); native phase-two res uses reversed arguments.
No action-search, acquisition policy, forecast learner or counterfactual API.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
from pathlib import Path


CORE_PATH = Path(__file__).with_name("03_bounded_logic.py")
_spec = importlib.util.spec_from_file_location("p303_task_core", CORE_PATH)
CORE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CORE)

WRAPPER_VERSION = "named-action-regret-v2"
RESERVED_LOSS = "__task_regret__"


class BindingError(CORE.InputError):
    """The retained request/catalogue and current compiled core no longer agree."""


class TaskCertificate:
    """A fixed objective request around one core Kernel.

    Source updates may use run/add_assumption/withdraw. A changed action
    catalogue, selected action, tolerance, program or unit needs a new request.
    Returned certificates are historical copies. Current-warrant checks are
    identity checks for such genuine outputs, not arbitrary-JSON authentication.
    Direct internal mutation is unsupported; catalogue/compiled-loss guards
    nevertheless reject the specific meaning substitutions tested in development.
    """

    def __init__(self, request):
        self.work = Counter()
        if not isinstance(request, dict) or set(request) != {
                "scope", "queries", "constraints", "cell_cap", "actions", "selected", "tolerance"}:
            raise CORE.InputError("task request fields")
        raw = self._admit(request, "request")
        self.request_sha256 = self._hash(raw)
        actions = request["actions"]
        if not isinstance(actions, dict) or not 1 <= len(actions) <= 15:
            raise CORE.InputError("one to fifteen supplied actions required")
        if RESERVED_LOSS in actions:
            raise CORE.InputError("reserved compiled-loss name")
        CORE.label(request["selected"])
        if request["selected"] not in actions:
            raise CORE.InputError("selected action is absent from catalogue")
        tolerance = CORE.rational(request["tolerance"])
        if tolerance < 0:
            raise CORE.InputError("nonnegative task tolerance required")
        if not isinstance(request["queries"], list) or not 1 <= len(request["queries"]) <= CORE.LIMITS["atoms"]:
            raise CORE.InputError("active query count")
        atom_count = len(request["queries"])
        unit = None
        counts = {}
        for name, row in actions.items():
            CORE.label(name)
            if not isinstance(row, dict) or set(row) != {"unit", "version", "expr"}:
                raise CORE.InputError("action loss fields")
            CORE.label(row["unit"]); CORE.label(row["version"])
            if unit is not None and row["unit"] != unit:
                raise CORE.InputError("all compared actions need the same declared loss unit")
            unit = row["unit"]
            counts[name] = CORE.validate_expr(row["expr"], atom_count, "loss")
            self.work["compilation_source_nodes_validated"] += counts[name]
            self.work["compilation_action_records"] += 1

        self.catalogue = deepcopy(actions)
        self.selected = request["selected"]
        self.tolerance = request["tolerance"]
        self.unit = unit
        self._tolerance_value = tolerance
        self._selection = (self.selected, self.tolerance, self.unit)
        self._catalogue_raw = self._admit(self.catalogue, "catalogue")
        self.catalogue_sha256 = self._hash(self._catalogue_raw)
        self._task_binding_raw = self._admit(self._task_record(), "task_binding")

        # Each residual is already nonnegative. Excluding a avoids a redundant
        # expression; the empty competitor family is explicitly the zero term.
        pieces = []
        for other in sorted(actions):
            if other == self.selected:
                continue
            pieces.append(["resid", deepcopy(actions[self.selected]["expr"]),
                           deepcopy(actions[other]["expr"])])
            self.work["compilation_expression_nodes_copied"] += counts[self.selected] + counts[other]
            self.work["compilation_positive_differences"] += 1
        expression = ["rat", "0"] if not pieces else pieces[0]
        for piece in pieces[1:]:
            expression = ["max", expression, piece]
            self.work["compilation_max_nodes"] += 1
        self.work["compiled_nodes_validated"] += CORE.validate_expr(expression, atom_count, "loss")
        descriptor = dict(selected=self.selected, catalogue_sha256=self.catalogue_sha256,
                          positive_difference="max(0, selected-other)")
        compiled_version = "regret:" + self._hash(CORE.canonical(descriptor))
        compiled = dict(unit=self.unit, version=compiled_version, expr=expression)
        self.compiled_loss_sha256 = self._hash(CORE.canonical(compiled))
        losses = deepcopy(actions)
        losses[RESERVED_LOSS] = compiled
        self._losses_raw = self._admit(losses, "compiled_catalogue")
        config = dict(scope=request["scope"], queries=deepcopy(request["queries"]),
                      constraints=deepcopy(request["constraints"]), cell_cap=request["cell_cap"], losses=losses)
        self.core = CORE.Kernel(config)
        self._core_input_sha256 = self.core.input_sha256
        self._scope = self.core.scope
        self._queries_raw = self._admit(self.core.queries, "query_binding")
        self.work["compilation_requests"] += 1

    def _admit(self, value, category):
        raw, nodes = CORE.admitted_data(value)
        self.work[category + "_bytes_encoded"] += len(raw)
        self.work[category + "_nodes_traversed"] += nodes
        return raw

    def _hash(self, raw):
        self.work["hash_calls"] += 1
        self.work["bytes_hashed"] += len(raw)
        return hashlib.sha256(raw).hexdigest()

    def _same(self, actual, expected):
        self.work["byte_comparisons"] += 1
        self.work["comparison_byte_envelope"] += max(len(actual), len(expected))
        return actual == expected

    def _task_record(self):
        """Full comparison task; output copies are distinct from live catalogue data."""
        return dict(wrapper_version=WRAPPER_VERSION, catalogue=self.catalogue,
                    selected=self.selected, tolerance=self.tolerance, common_unit=self.unit)

    def _guard(self):
        self.work["binding_checks"] += 1
        if (self.selected, self.tolerance, self.unit) != self._selection:
            raise BindingError("selected action, tolerance or unit changed; validate a new request")
        if not self._same(self._admit(self.catalogue, "guard_catalogue"), self._catalogue_raw):
            raise BindingError("original supplied catalogue changed")
        if not self._same(self._admit(self.core.losses, "guard_losses"), self._losses_raw):
            raise BindingError("action objective or compiled regret changed; validate a new request")
        if (self.core.input_sha256 != self._core_input_sha256 or self.core.scope != self._scope or
                not self._same(self._admit(self.core.queries, "guard_queries"), self._queries_raw)):
            raise BindingError("original query/scope changed; validate a new request")

    def run(self, allowance, mode="all"):
        self._guard()
        return self.core.run(allowance, mode)

    def add_assumption(self, assumption, allowance=1):
        self._guard()
        return self.core.add_assumption(assumption, allowance)

    def withdraw(self, evidence_id, allowance=1):
        self._guard()
        return self.core.withdraw(evidence_id, allowance)

    def certificate(self, allowance=1):
        self._guard()
        report = self.core.report(RESERVED_LOSS, allowance)
        certified = False
        status = report["status"]
        if status == "CONDITIONAL_OUTER_BOUND" and report["bounds"] is not None:
            # The endpoint is generated by the trusted bounded core, not an
            # arbitrary caller-supplied exact-real or fraction string.
            upper = Fraction(report["bounds"][1])
            self.work["threshold_comparisons"] += 1
            self.work["threshold_operand_bits"] += max(
                abs(upper.numerator).bit_length(), upper.denominator.bit_length(),
                abs(self._tolerance_value.numerator).bit_length(), self._tolerance_value.denominator.bit_length(), 1)
            certified = upper <= self._tolerance_value
            status = "CERTIFIED_CONDITIONAL" if certified else "NOT_CERTIFIED_BY_THIS_BOUND"
        result = dict(schema="value_logic.P3-03.task_certificate.v2", stage="DEVELOPMENT",
                      wrapper_version=WRAPPER_VERSION, request_sha256=self.request_sha256,
                      task_binding=self._task_record(),
                      selected=self.selected, action_names=sorted(self.catalogue),
                      catalogue_sha256=self.catalogue_sha256, common_unit=self.unit,
                      tolerance=self.tolerance, compiled_loss_name=RESERVED_LOSS,
                      compiled_loss_sha256=self.compiled_loss_sha256,
                      certified=certified, status=status,
                      guarantee="Pointwise tolerance against every supplied action, conditional on the active finite source.",
                      no_certificate_meaning="An excessive outer endpoint alone is not a counterexample or impossibility proof.",
                      core_report=report, boundary_work=dict(self.work),
                      boundary_snapshot="Before this outer certificate's serialization; outside the core transaction allowance.")
        self.work["certificate_serialization_bytes"] += len(CORE.canonical(result))
        return deepcopy(result)

    def certificate_is_current(self, certificate):
        """Current identity for genuine historical outputs; not JSON authentication.

        Source refinement may preserve an older, looser certificate. Source
        withdrawal/addition changes the binding. Objective changes require a
        fresh wrapper. Invalid private-state mutations return false here and
        are rejected by certificate() before any new certificate is produced.
        Full task/source/loss records are compared exactly; fingerprints are
        audit references. No numeric-bound or execution-lineage proof is made.
        """
        try:
            self._guard()
        except (CORE.InputError, CORE.ResourceLimit, TypeError, ValueError):
            return False
        if not isinstance(certificate, dict):
            return False
        expected = dict(wrapper_version=WRAPPER_VERSION, selected=self.selected,
                        common_unit=self.unit, tolerance=self.tolerance,
                        compiled_loss_name=RESERVED_LOSS)
        if any(certificate.get(key) != value for key, value in expected.items()):
            return False
        try:
            old_task = self._admit(certificate.get("task_binding"), "guard_report_task")
        except (CORE.InputError, CORE.ResourceLimit, TypeError, ValueError):
            return False
        if not self._same(old_task, self._task_binding_raw):
            return False
        report = certificate.get("core_report")
        return (isinstance(report, dict) and report.get("loss") == RESERVED_LOSS and
                self.core.report_is_current(report))

    def accounting(self):
        """Current work records before serializing this administrative copy."""
        return dict(wrapper_boundary_work=dict(self.work), core_work=dict(self.core.work),
                    convention="Boundary diagnostics are separate from coarse core transaction allowance; no CPU-unit equivalence.")
