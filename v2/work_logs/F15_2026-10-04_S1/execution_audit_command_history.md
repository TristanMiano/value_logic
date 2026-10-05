# Delegated execution audit: aggregate-related command history

Contributor: **delegated ChatGPT (GPT-6 Astra Pro), execution audit**.
Scope: this agent's access to the F15 aggregate, in execution order. Individual
command UTC starts were not separately metered. The tool transcript retains
the original invocations and outputs; this document records their relevant
code without inventing timestamps.

Before the principal reported completion, this agent only read frozen source,
checked frozen hashes, and created `execution_audit.md` outside the run
directory. After completion, initial reads listed run filenames, read stage
manifests, the pre-evaluation validation, individual sample cases/models,
assessments and external logs. They did not open the combined aggregate for
writing. No invocation by this agent ran a preparation/evaluation command or
an experimental population generator.

## 1. Run inventory

```bash
rg --files v2/work_logs/F15_2026-10-04_S1 v2/work_logs/F15_v1_run1
```

This listed `retention_results.json` among the saved files. The filename-only
listing did not inspect its contents.

## 2. First complete hash sweep: discrepancy detected

The following read-only Python command was the first content access to the
combined aggregate by this agent. It returned 362 run files, 181 JSON files,
181 sidecars, and exactly one mismatch:
`evaluation_attempt_1/retention_results.json`.

```python
from pathlib import Path
import hashlib,json
root=Path.cwd(); run=root/'v2/work_logs/F15_v1_run1'
files=sorted(p for p in run.rglob('*') if p.is_file()); errors=[]
for p in files:
 if p.suffix=='.sha256':
  target=Path(str(p)[:-7])
  if not target.is_file(): errors.append('orphan '+str(p.relative_to(run)))
 elif not Path(str(p)+'.sha256').is_file(): errors.append('missing sidecar '+str(p.relative_to(run)))
 else:
  if hashlib.sha256(p.read_bytes()).hexdigest()!=Path(str(p)+'.sha256').read_text().strip(): errors.append('hash '+str(p.relative_to(run)))
f=root/'v2/experiments/freeze.v1.json'; manifest=json.loads(f.read_text()); mism=[]
for rel,m in manifest['files'].items():
 b=(root/rel).read_bytes()
 if len(b)!=m['bytes'] or hashlib.sha256(b).hexdigest()!=m['sha256']: mism.append(rel)
print(json.dumps({'run_files':len(files),'json_files':sum(p.suffix=='.json' for p in files),'sidecars':sum(p.suffix=='.sha256' for p in files),'total_bytes':sum(p.stat().st_size for p in files),'sidecar_errors':errors,'manifest_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'frozen_byte_mismatches':mism},indent=2))
```

The same shell invocation subsequently ran only `git check-ignore` for two
external `.log` filenames, discovering that command logs needed force-adding
for preservation. It performed no write.

## 3. Attempted aggregate/per-case comparison: JSON parse failure

The next command began as follows. It failed on the final statement shown,
with `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.

```python
from pathlib import Path
import hashlib,json,datetime
r=Path('v2/work_logs/F15_v1_run1/evaluation_attempt_1'); a=r/'retention_results.json'; s=Path(str(a)+'.sha256'); data=a.read_bytes(); cases=json.loads(data)
```

The remaining, unexecuted command text would have printed aggregate stat/hash
details, loaded the 160 individual cases, constructed their canonical bytes
in memory, compared aggregate contents, and printed at most 20 differences.
It contained no file-opening write mode, `write_text`, `write_bytes`, unlink,
rename, truncation, or generator call. Because parsing failed first, none of
that later comparison code executed.

## 4. Independent zero-byte observation

```python
from pathlib import Path
import hashlib,datetime,json
for name in ('retention_results.json','retention_results.json.sha256'):
 p=Path('v2/work_logs/F15_v1_run1/evaluation_attempt_1')/name
 data=p.read_bytes(); st=p.stat()
 print(json.dumps({'file':str(p),'bytes_read':len(data),'stat_bytes':st.st_size,'sha256':hashlib.sha256(data).hexdigest(),'mtime_ns':st.st_mtime_ns,'mtime_utc':datetime.datetime.fromtimestamp(st.st_mtime,datetime.timezone.utc).isoformat(),'prefix':repr(data[:100])}))
```

This independently read zero aggregate bytes and zero stat bytes, with empty
SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The recorded aggregate mtime was `2026-10-05T03:50:17.107053+00:00`.
Its sidecar was 65 bytes, retained mtime
`2026-10-05T03:50:17.460057+00:00`, and contained the original checksum
`0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`.

## 5. In-memory reconstruction: exact original checksum recovered

```python
from pathlib import Path
import hashlib,json
root=Path.cwd(); config=json.loads((root/'v2/experiments/config.v1.json').read_text()); r=root/'v2/work_logs/F15_v1_run1/evaluation_attempt_1'
cases=[]
for seed in config['retention']['evaluation_seeds']:
 for variant in config['retention']['variants']:
  cases.append(json.loads((r/f'retention_{seed}_{variant}.json').read_text()))
data=(json.dumps(cases,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8'); expected=(r/'retention_results.json.sha256').read_text().strip()
print(json.dumps({'reconstructed_from_case_units':len(cases),'reconstructed_bytes':len(data),'reconstructed_sha256':hashlib.sha256(data).hexdigest(),'original_sidecar_sha256':expected,'exact_digest_match':hashlib.sha256(data).hexdigest()==expected,'method_rows':sum(len(c['methods']) for c in cases),'numeric_queries':sum(len(m['numeric']) for c in cases for m in c['methods'])},indent=2))
```

This produced no file. It found 15,833,616 canonical bytes with the exact
original checksum, from 160 cases / 1,920 rows / 11,520 queries.

## 6. Explicitly authorized recovery writes

Only after reporting those observations and receiving the principal's
specific recovery instruction did this agent write the recovered aggregate.
The recovery writer used exclusive `xb`/`x` modes, flush/fsync, directory
fsync, and an immediate reread. Its only output paths were:

- `retention_results_recovered.json` and its SHA256 sidecar;
- `retention_aggregate_recovery.json` and its SHA256 sidecar.

All four are under `v2/work_logs/F15_2026-10-04_S1/`, outside the original run
directory. The original aggregate and sidecar were opened only for reading;
their before/after snapshots were asserted equal. The recovery record contains
all 160 source file digests and the original/target stat and hash evidence.

A separate subsequent Python process reread the recovered file, parsed all
160 cases, checked both its own and the original sidecar, and reconfirmed that
the original aggregate remained zero bytes. It wrote only
`retention_recovery_second_read.json` and its sidecar in the audit directory.
Its observation was `2026-10-05T03:57:44.764051+00:00`.

These commands establish what this delegated agent executed. They do not
identify the cause of the original missing aggregate bytes or establish the
absence of activity by every external process. The principal separately
reported no known writer to the original aggregate after the runner.

## 7. Subsequent complete artifact audit

After recovery, this agent created and ran `audit_saved_artifacts.py` in this
directory. Its complete source is preserved and its SHA256 is recorded inside
`artifact_integrity_audit.json`. The script reads the original aggregate only
for inventory/hash/zero-byte-state checks, reads the separate recovered file
for case comparisons, and calls only frozen configuration/manifest/prepared
artifact validators. It contains no experimental generator or stage call.
Its only writes are its explicitly named audit-output JSON and sidecar.

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python v2/work_logs/F15_2026-10-04_S1/audit_saved_artifacts.py
```

This command completed with exit code 0, 3,644 checks and no unexpected errors,
while explicitly retaining the original zero-byte aggregate as a disclosed
hash exception. The script verified the recovered file against the original
sidecar and all 160 case files again.
