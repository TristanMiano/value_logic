"""Executable witnesses for the Task 14B typed read/write interface.

These helpers do not add a semantic carrier.  They make the finite keys queried
by the frozen atom clauses explicit enough to regression-test negative reads and
event/write intersections.  The proof is in ``formalism/08b_audit_repairs.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True, order=True)
class RecordKey:
    """A typed request/store location or collection index."""

    namespace: str
    parts: tuple[str, ...] = ()


def key(namespace: str, *parts: str) -> RecordKey:
    return RecordKey(namespace, tuple(parts))


def _evidence_footprint(
    atom: str,
    mode: str,
    record_ids: Iterable[str],
    *,
    include_region: bool,
) -> frozenset[RecordKey]:
    keys = {
        key("cert-index", atom, mode),
        key("verifier", mode),
        key("mode-rules", mode),
        key("priority-index", atom, mode),
    }
    if include_region:
        keys.add(key("region-index", atom))
    for record_id in record_ids:
        keys.update(
            {
                key("certificate", record_id),
                key("current", record_id),
                key("correction-index", record_id),
            }
        )
        if include_region:
            keys.add(key("region", record_id, atom))
    return frozenset(keys)


def region_footprint(
    atom: str,
    mode: str,
    record_ids: Iterable[str] = (),
) -> frozenset[RecordKey]:
    """Read keys for adequacy or a region-valued constraint."""

    return _evidence_footprint(atom, mode, record_ids, include_region=True)


def improvement_footprint(
    atom: str,
    candidate_atom: str,
    fallback_atom: str,
    context: str,
    mode: str,
    candidate_record_ids: Iterable[str] = (),
    fallback_record_ids: Iterable[str] = (),
) -> frozenset[RecordKey]:
    """Read keys for a fallback-relative improvement atom."""

    return frozenset(
        {
            key("slot-address", atom),
            key("context", context),
            key("fallback", context),
        }
        | set(region_footprint(candidate_atom, mode, candidate_record_ids))
        | set(region_footprint(fallback_atom, mode, fallback_record_ids))
    )


def trace_footprint(
    atom: str,
    mode: str,
    trace_ids: Iterable[str] = (),
) -> frozenset[RecordKey]:
    """Read keys for the trace clause, including an empty trace index."""

    keys = {
        key("trace-index", atom, mode),
        key("verifier", mode),
        key("mode-rules", mode),
        key("priority-index", atom, mode),
    }
    for trace_id in trace_ids:
        keys.update(
            {
                key("trace", trace_id),
                key("current", trace_id),
                key("correction-index", trace_id),
            }
        )
    return frozenset(keys)


def comparison_footprint(
    kind: str,
    candidate: str,
    context: str,
    evaluated_set: Iterable[str],
    criterion: str,
    mode: str,
    *,
    search_ids: Iterable[str] = (),
    pair_record_ids: Mapping[str, Iterable[str]] | None = None,
) -> frozenset[RecordKey]:
    """Read keys for relative or certified undominated comparison.

    ``kind`` is ``relative`` or ``certified``.  Both forms retain pair-index
    negative reads because a newly inserted dominator can change either value.
    The certified form additionally reads each pair's current resolution; those
    member keys are represented here by the supplied record ids.
    """

    if kind not in {"relative", "certified"}:
        raise ValueError(f"unknown comparison footprint kind {kind!r}")
    evaluated = tuple(sorted(evaluated_set))
    set_id = ",".join(evaluated)
    keys = {
        key("slot-address", kind, candidate, context, set_id, criterion, mode),
        key("eval-index", context),
        key("search-index", candidate, context, set_id, criterion),
        key("verifier", mode),
        key("mode-rules", mode),
        key("priority-index", kind, candidate, context, set_id, criterion, mode),
    }
    for plan in evaluated:
        keys.update(
            {
                key("eval-entry", context, plan),
                key("pair-index", candidate, plan, context, criterion),
                key("eligibility", plan, context, criterion),
            }
        )
    for search_id in search_ids:
        keys.update(
            {
                key("search", search_id),
                key("search-current", search_id),
                key("correction-index", search_id),
            }
        )
    for plan, record_ids in (pair_record_ids or {}).items():
        if plan not in evaluated:
            raise ValueError(f"pair record for {plan!r} is outside the exact evaluated set")
        for record_id in record_ids:
            keys.update(
                {
                    key("pair", candidate, plan, context, criterion, record_id),
                    key("certificate", record_id),
                    key("current", record_id),
                    key("correction-index", record_id),
                }
            )
    return frozenset(keys)


def certificate_writes(atom: str, mode: str, record_id: str) -> frozenset[RecordKey]:
    return frozenset(
        {
            key("cert-index", atom, mode),
            key("region-index", atom),
            key("certificate", record_id),
            key("region", record_id, atom),
            key("current", record_id),
            key("correction-index", record_id),
        }
    )


def trace_writes(atom: str, mode: str, trace_id: str) -> frozenset[RecordKey]:
    return frozenset(
        {
            key("trace-index", atom, mode),
            key("trace", trace_id),
            key("current", trace_id),
            key("correction-index", trace_id),
        }
    )


def evaluated_set_writes(context: str, plan: str) -> frozenset[RecordKey]:
    return frozenset({key("eval-index", context), key("eval-entry", context, plan)})


def search_writes(
    candidate: str,
    context: str,
    evaluated_set: Iterable[str],
    criterion: str,
    search_id: str,
) -> frozenset[RecordKey]:
    set_id = ",".join(sorted(evaluated_set))
    return frozenset(
        {
            key("search-index", candidate, context, set_id, criterion),
            key("search", search_id),
            key("search-current", search_id),
            key("correction-index", search_id),
        }
    )


def pair_writes(
    candidate: str,
    other: str,
    context: str,
    criterion: str,
    record_id: str,
) -> frozenset[RecordKey]:
    return frozenset(
        {
            key("pair-index", candidate, other, context, criterion),
            key("pair", candidate, other, context, criterion, record_id),
            key("certificate", record_id),
            key("current", record_id),
            key("correction-index", record_id),
        }
    )


def projection(
    records: Mapping[RecordKey, object],
    footprint: Iterable[RecordKey],
) -> tuple[tuple[RecordKey, object], ...]:
    """Canonical projection; absent keys receive an explicit marker."""

    missing = ("<absent>",)
    return tuple((item, records.get(item, missing)) for item in sorted(footprint))


def write_disjoint(
    reads: Iterable[RecordKey],
    writes: Iterable[RecordKey],
) -> bool:
    return frozenset(reads).isdisjoint(writes)
