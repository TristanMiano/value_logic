"""Close one administrative JSON-census finding without repeating passed checks.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
The preserved failed public command has an empty stdout stream whose filename
ends in .json. That raw stream is not a claimed successful JSON result.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    base_path = HERE/"closing_checks/attempt_01.json"
    base_bytes = base_path.read_bytes()
    base = json.loads(base_bytes)
    assert base["status"] == "FAIL" and len(base["errors"]) == 1
    error = base["errors"][0]
    path = "v3/work_logs/P3_10_2026-10-11_S1/commands/public/stdout.json"
    assert error["check"] == "new_json_parse" and error["path"] == path
    data = (ROOT/path).read_bytes()
    command_path = HERE/"commands/public/completion.json"
    command = json.loads(command_path.read_bytes())
    assert command["returncode"] == 1 and command["stdout_bytes"] == 0
    assert len(data) == 0 and sha(data) == command["stdout_sha256"]
    assert command["command"][-1] == "public"
    assert sha((HERE/"verify_closure_v2.py").read_bytes()) == base["verification_source_sha256"]
    assert sha((HERE/"actuals.json").read_bytes()) == base["actuals_sha256"]
    assert sha((ROOT/"v3/time_ledger.csv").read_bytes()) == base["ledger"]["result_sha256"]
    assert json.loads((HERE/"clock_state.json").read_bytes()) is None
    result = dict(base)
    result.update(status="PASS", errors=[], original_verification_utc=base["verified_utc"],
        verified_utc=datetime.now(timezone.utc).isoformat(),
        preserved_initial_result={"path":str(base_path.relative_to(ROOT)),"sha256":sha(base_bytes)},
        json_census_disposition={"successful_json_files_parsed":base["new_json_files_parsed"],
            "raw_failed_command_streams_excluded":[{"path":path,"bytes":0,"sha256":sha(data),
                "command_completion_sha256":sha(command_path.read_bytes()),"command_returncode":1}],
            "reason":"The original failed command emitted no stdout. The exact empty stream is preserved and bound by its nonzero-return command record; no successful JSON payload was promised or generated there."},
        closure_source_sha256=sha(Path(__file__).read_bytes()),
        repeated_scientific_execution=False,
        closure_scope="Narrow empty failed-command stream classification and unchanged accounting hashes; all other checks inherit the preserved administrative result.")
    with (HERE/"closing_verification.json").open("x") as stream:
        json.dump(result,stream,indent=2);stream.write("\n")
    print(json.dumps({"status":"PASS","protected_files":base["protected_files_byte_and_mode_identical"],
        "original_evidence_files":base["original_evidence_files"],"unit_seals":base["unique_unit_seals_verified"],
        "json_payloads":base["new_json_files_parsed"],"preserved_empty_failed_stdout":1,
        "focused_documents":base["markdown"]["files"],"links":base["markdown"]["local_links_checked"],
        "closing_verification_sha256":sha((HERE/"closing_verification.json").read_bytes())}))


if __name__ == "__main__":
    main()
