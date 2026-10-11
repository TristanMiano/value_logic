"""Close only the missing concurrent administrative artifact-link finding.

Reads the preserved first audit and compares its immutable input hashes.
Does not repeat clock/ledger reconstruction or invoke any project script.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import sys
import traceback

HERE=Path(__file__).resolve().parent
SESSION=HERE.parents[2]
ROOT=SESSION.parents[2]
W=SESSION.relative_to(ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    out=HERE/"link_closure_01"
    out.mkdir(exist_ok=False)
    checks=[]
    def check(label,ok):
        checks.append({"check":label,"pass":bool(ok)})
    result={"schema":"P3-10-admin-artifact-link-closure-v1","reviewer":"/root/certificate_reconstruction",
            "started_utc":datetime.now(timezone.utc).isoformat(),"source_sha256":sha(Path(__file__).read_bytes()),
            "principal_research_credit_ns":0,"scientific_executions":0,"clock_or_ledger_reconstruction_repeated":False}
    try:
        old_data=(HERE/"run_01/results.json").read_bytes()
        old=json.loads(old_data)
        manifest_data=(HERE/"run_01/source_hashes.json").read_bytes()
        manifest=json.loads(manifest_data)
        result["original_audit_results_sha256"]=sha(old_data)
        check("original audit result has expected sole link failure",old["status"]=="FAIL" and old["exception"] is None and old["failed_checks"]==1 and
              old["failures"][0]["check"]=="local artifact link: v3/work_logs/P3_10_2026-10-11_S1.md -> P3_10_2026-10-11_S1/closing_verification.json")
        check("original audit source manifest binding unchanged",sha(manifest_data)==old["source_hashes_sha256"])
        for item in manifest:
            if not item["concurrent_root_document"]:
                check("core audit source unchanged: "+item["path"],sha((ROOT/item["path"]).read_bytes())==item["sha256"])
        closing_path=SESSION/"closing_verification.json"
        closing=closing_path.read_bytes()
        parsed=json.loads(closing)
        check("linked closing verification is readable JSON object",isinstance(parsed,dict))
        result["closing_verification"]={"path":str(closing_path.relative_to(ROOT)),"bytes":len(closing),"sha256":sha(closing),"declared_status":parsed.get("status")}
        (out/"closing_verification.reviewed.json").write_bytes(closing)
        session=ROOT/"v3/work_logs/P3_10_2026-10-11_S1.md"
        session_data=session.read_bytes()
        (out/"session.reviewed.md").write_bytes(session_data)
        result["session_sha256"]=sha(session_data)
        local_links=[]
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)",session_data.decode()):
            target=target.split("#",1)[0]
            if not target or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:",target):
                continue
            resolved=session.parent/target
            check("current session artifact exists: "+target,resolved.exists())
            local_links.append({"target":target,"resolved":str(resolved.resolve()),"exists":resolved.exists()})
        result["current_session_local_links"]=local_links
        result["interpretation"]="The preserved first run remains FAIL with one missing-link observation. All its accounting checks passed; its immutable inputs remain unchanged and the sole link defect is now closed. No historical attention/CPU verification or publication claim is added."
    except Exception as exc:
        result["exception"]={"type":type(exc).__name__,"message":str(exc)}
        (out/"failure_traceback.txt").write_text(traceback.format_exc())
    result["finished_utc"]=datetime.now(timezone.utc).isoformat()
    result["checks"]=checks
    result["failed_checks"]=sum(not c["pass"] for c in checks)
    result["status"]="PASS" if result["failed_checks"]==0 and "exception" not in result else "FAIL"
    data=(json.dumps(result,indent=2,sort_keys=True)+"\n").encode()
    (out/"results.json").write_bytes(data)
    print(json.dumps({"status":result["status"],"checks":len(checks),"failed_checks":result["failed_checks"],"results_sha256":sha(data)}))
    return 0 if result["status"]=="PASS" else 1


if __name__=="__main__":
    sys.exit(main())
