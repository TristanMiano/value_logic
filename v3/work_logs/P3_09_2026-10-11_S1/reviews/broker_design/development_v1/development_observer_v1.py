"""Frozen P3-09 development selfcheck observer; never generates final inputs."""
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def save(path, value):
    with path.open("x", encoding="ascii") as stream:
        stream.write(canonical(value) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder = Path(sys.argv[1]).resolve()
    frozen = folder / "source"
    manifest = json.loads((folder / "manifest.json").read_text())
    for row in manifest["sources"]:
        path = frozen / row["path"]
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError("Frozen development source mismatch: " + row["path"])
    if digest(Path(__file__)) != manifest["observer_sha256"]:
        raise ValueError("Development observer changed after its manifest.")
    output = folder / "run"
    output.mkdir(exist_ok=False)
    save(output / "started.json", {
        "stage": "DEVELOPMENT", "principal_clock_credit": 0,
        "manifest_sha256": digest(folder / "manifest.json"),
        "command": [sys.executable, str(Path(__file__).resolve()), str(folder)],
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "final_generation_calls": 0})
    sys.path.insert(0, str(frozen / "v3/experiments"))
    import p309_broker as adapter
    if Path(adapter.__file__).resolve() != frozen / "v3/experiments/p309_broker.py":
        raise ValueError("Development adapter imported from a different source.")
    error = None
    try:
        result = adapter.selfcheck()
    except adapter.SelfcheckFailure as failure:
        result = failure.record
        error = {"type": type(failure).__name__, "message": str(failure),
            "cause_type": None if failure.__cause__ is None else type(failure.__cause__).__name__,
            "cause": None if failure.__cause__ is None else str(failure.__cause__)}
    save(output / "results.json", result)
    after = [{"path": row["path"], "unchanged": digest(frozen / row["path"]) == row["sha256"]}
             for row in manifest["sources"]]
    summary = {"stage": "DEVELOPMENT", "principal_clock_credit": 0,
        "status": result.get("status"), "error": error,
        "public_records": len(result.get("public_records", [])),
        "scores": len(result.get("scores", [])),
        "negative_control_copies": len(result.get("observer_negative_controls", [])),
        "assertions": len(result.get("checks", [])),
        "failed_assertions": [row for row in result.get("checks", []) if not row["passed"]],
        "final_generation_calls": result.get("final_generation_calls"),
        "final_seed_streams_generated": result.get("final_seed_streams_generated"),
        "result_sha256": digest(output / "results.json"),
        "source_after": after, "finished_utc": datetime.now(timezone.utc).isoformat()}
    save(output / "summary.json", summary)
    print(canonical(summary))
    if error is not None or result.get("status") != "PASS" or not all(row["unchanged"] for row in after):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
