# P3-03 development evidence

All attempts here are **DEVELOPMENT**. Each has inputs and a manifest saved
before scientific execution, followed by its summary and complete traces.
Earlier manifests bind their historical code/text snapshots; subsequent
development does not rewrite their records.

The largest repetitive trace is stored as deterministic, lossless gzip to keep
repository transfers small. Its logical artifact remains the exact original
JSON bytes hashed by the execution summary. The
[storage record](artifact_storage.json) binds both representations. From the
repository root, materialize and verify it with:

```sh
python v3/checks/03_materialize_evidence.py
```

The utility checks an existing output rather than overwriting it. It does not
rerun an experiment or generate new scientific evidence. Smaller traces remain
plain JSON. Reproduction of an experiment requires a new attempt number and
directory; never overwrite a completed attempt to make current code appear to
have been the originally exercised revision.
