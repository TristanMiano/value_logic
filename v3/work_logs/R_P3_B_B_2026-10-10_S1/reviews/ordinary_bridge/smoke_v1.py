"""Focused first producer/receiver bridge check; DEVELOPMENT, zero clock credit."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(source_root, out):
    source_root, out = Path(source_root).resolve(), Path(out).resolve()
    assert not out.exists()
    out.mkdir(parents=True)
    source_manifest = json.loads((source_root.parent / "source_manifest.json").read_text())
    for row in source_manifest["files"]:
        assert sha(source_root / row["path"]) == row["sha256"]
    path = source_root / "v3/checks/05_add_evidence.py"
    spec = importlib.util.spec_from_file_location("_rp3bb_add_evidence", path)
    E = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = E
    spec.loader.exec_module(E)
    R, M, K, P = E.receiver_module(), E.M, E.K, E.P
    events = []
    def event(name, **values):
        item = {"name": name, **values}
        events.append(item)
        with (out / "events.jsonl").open("a") as handle:
            handle.write(json.dumps(item, default=str)+"\n")
    def save_packet(name, proof, work):
        payload = E.to_wire(proof, work)
        (out / (name+".json")).write_bytes(payload)
        assert E.from_wire(payload) == proof
        return payload
    def reject(name, callback, work, expected):
        try:
            callback()
        except expected as error:
            event(name, status="EXPECTED_REJECTION", exception=type(error).__name__,
                  reason=str(error), work=work)
            return error
        else:
            raise AssertionError("Expected rejection: "+name)
    try:
        setup = {}
        source_record = E.make_source_record(repo_root=source_root, work=setup)
        f0 = M.Frame(K.Request(1, (), (), (("difference", K.lit(-1)),),
                              "ordinary-bridge-cold", '{"fixture":"constant-v1"}'),
                     "difference", "task_loss")
        f1 = M.Frame(K.Request(1, (K.neg(K.bit(0)),), (),
                              (("difference", K.sub(K.bit(0), K.lit(1))),),
                              "ordinary-bridge-edit", '{"fixture":"constrained-edit-v1"}'),
                     "difference", "task_loss")
        witness, bound = (0,), F(-1)
        manager = E.RecordingManager(1, source_record=source_record, epoch="smoke-v1", work=setup)
        receiver = R.Receiver(source_record, "smoke-v1", 1, (0,), work=setup)
        work = {}
        p0 = E.export_dag(manager, f0, witness, bound, f0.record(), work=work)
        b0 = save_packet("cold", p0, work)
        report0 = receiver.receive(b0, f0, f0.record(), witness, bound,
                                   work=work, request_id="cold")
        assert receiver.current_receipt("cold") == report0
        event("cold", status="PASS", setup=setup, work=work, report=report0,
              packet_bytes=len(b0), receiver_counts=receiver.state_counts())
        work = {}
        p1 = E.export_dag(manager, f1, witness, bound, f1.record(), base=p0.next_cursor(), work=work)
        b1 = save_packet("delta", p1, work)
        report1 = receiver.receive(b1, f1, f1.record(), witness, bound,
                                   work=work, request_id="delta")
        event("delta", status="PASS", work=work, report=report1, packet_bytes=len(b1),
              receiver_counts=receiver.state_counts())
        work = {}
        full = E.export_dag(manager, f1, witness, bound, f1.record(), work=work)
        full_wire = save_packet("full_after_delta", full, work)
        fresh = R.Receiver(source_record, "smoke-v1", 1, (0,))
        full_report = fresh.receive(full_wire, f1, f1.record(), witness, bound,
                                    work=work, request_id="fresh-after-delta")
        assert full_report["bound"] == report1["bound"]
        event("full_after_delta", status="PASS", work=work, report=full_report,
              packet_bytes=len(full_wire))
        for symbolic in (False, True):
            work = {}
            tree = E.export_tree(manager, f1, witness, bound, f1.record(),
                                 symbolic=symbolic, work=work)
            checked = P.PortfolioCache().verify(tree, f1, f1.record(), work)
            event("legacy_tree_symbolic_"+str(symbolic), status="PASS", work=work,
                  proof=tree.record(), report=checked)
        work = {}
        empty_receiver = R.Receiver(source_record, "smoke-v1", 1, (0,))
        empty_cache = P.PortfolioCache()
        bridged_receiver, bridged, bootstrap_report = E.admit_checked_add(
            empty_receiver, empty_cache, "old", b0, f0, f0.record(), witness, bound,
            expected_source_record=source_record, request_id="bootstrap", work=work)
        assert empty_receiver.state_counts() == {"nodes": 0, "applies": 0, "expressions": 0}
        assert not empty_cache._domains and set(bridged._domains) == {"old"}
        native = P.PortfolioCache()
        band = M.build_band(f0, 0, bound, work)
        native.admit_band("old", band, f0.record(), work)
        choices = (P.Choice("old", f0.record(), (K.bit(0),)),)
        hybrid_proof = bridged.build(f1, choices, witness, bound, allow_direct=False, work=work)
        native_proof = native.build(f1, choices, witness, bound, allow_direct=False, work=work)
        hybrid_report = bridged.verify(hybrid_proof, f1, f1.record(), work)
        native_report = native.verify(native_proof, f1, f1.record(), work)
        assert M.canonical(hybrid_proof.record()) == M.canonical(native_proof.record())
        assert hybrid_report == native_report
        event("verified_add_to_identical_portfolio_kernel", status="PASS", work=work,
              bootstrap_report=bootstrap_report, shared_proof=hybrid_proof.record(),
              shared_report=hybrid_report)
        bad = json.loads(full_wire)
        bad["roots"]["bad"] = next(i for i, row in enumerate(bad["nodes"]) if row == ["T", 1, 1])
        guard_receiver = R.Receiver(source_record, "smoke-v1", 1, (0,))
        work = {}
        reject("wrong_bad_root", lambda: guard_receiver.receive(
            json.dumps(bad), f1, f1.record(), witness, bound, work=work, request_id="bad-root"), work, R.Rejected)
        assert guard_receiver.state_counts() == {"nodes": 0, "applies": 0, "expressions": 0}
        guard_receiver.reset(source_record, "new-epoch", 1, (0,))
        work = {}
        reject("stale_epoch", lambda: guard_receiver.receive(
            full_wire, f1, f1.record(), witness, bound, work=work, request_id="stale"), work, R.Rejected)
        work = {}
        reject("adapter_substituted_bound", lambda: E.admit_checked_add(
            empty_receiver, empty_cache, "bad", b0, f0, f0.record(), witness, F(-2),
            expected_source_record=source_record, request_id="bad-bound", work=work), work, R.Rejected)
        work = {}
        reject("adapter_fake_receiver", lambda: E.admit_checked_add(
            object(), empty_cache, "bad", b0, f0, f0.record(), witness, bound,
            expected_source_record=source_record, request_id="fake", work=work), work, E.EvidenceRejected)
        assert not empty_cache._domains
        false_frame = M.Frame(K.Request(1, (), (), (("difference", K.bit(0)),),
                                      "false-bound-v1"), "difference", "task_loss")
        work = {}
        false = reject("actually_false_bound", lambda: E.export_dag(
            manager, false_frame, witness, F(0), false_frame.record(), work=work), work, E.NoBoundProof)
        assert false.counterexample == (1,)
        work = {}
        before_nodes = len(manager.nodes)
        reject("computed_4097_bit_wire_limit", lambda: manager.terminal(F(1 << 4096), work), work, E.EvidenceLimit)
        assert len(manager.nodes) == before_nodes
        assert work["max_requested_terminal_component_bits"] == 4097
        producer_state = manager.state_bytes()
        receiver_state = M.canonical(receiver.state_record()).encode("utf-8")
        (out / "producer_state.json").write_bytes(producer_state)
        (out / "receiver_state.json").write_bytes(receiver_state)
        for row in source_manifest["files"]:
            assert sha(source_root / row["path"]) == row["sha256"]
        summary = {"stage": "DEVELOPMENT", "status": "PASS", "principal_research_credit_seconds": 0,
                   "same_model_nonblind": True, "events": len(events),
                   "source_manifest_sha256": sha(source_root.parent / "source_manifest.json"),
                   "source_record": source_record, "producer_state_bytes": len(producer_state),
                   "receiver_state_bytes": len(receiver_state),
                   "scope": "First focused compatibility check; no tariff or comparative superiority claim."}
        (out / "results.json").write_text(json.dumps(summary, indent=2)+"\n")
        (out / "manifest.json").write_text(json.dumps({"stage": "DEVELOPMENT", "files": [
            {"path": path.name, "bytes": path.stat().st_size, "sha256": sha(path)}
            for path in sorted(out.iterdir()) if path.is_file()]}, indent=2)+"\n")
        print(json.dumps(summary, indent=2))
    except Exception:
        (out / "failure.json").write_text(json.dumps({"stage": "DEVELOPMENT", "status": "FAIL",
            "utc": datetime.now(timezone.utc).isoformat(), "traceback": traceback.format_exc(),
            "completed_events": len(events)}, indent=2)+"\n")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    run(args.source_root, args.out)
