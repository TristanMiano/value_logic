# P3-10-A1 lineage reader: narrow closure

Signed by **ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction**, 2026-10-11. Principal clock credit: **0**.

I inspected the narrow diff from reviewed reader SHA-256 `d3e5d1ff4a5fc4c03fea4d07d1f205c763d1cf52476c63a3c6c6c27cb55c6f8e` to revised reader SHA-256 `54a11007e1530baa25a6f495294b1bdb57f70cefe08568df7f5aa8b815b376ce`. Both findings in the signed v1 source review are closed:

- **A1-L1:** the revised manifest/binding equality additionally requires the externally announced A1 manifest hash `36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359`.
- **A1-L2:** the revised reader requires the complete remaining-unit metadata to equal the exact frozen conformance slice and the reused IDs to equal the complementary frozen roster.

The diff changes only those three assertions. It does not change result parsing order, the public-bounds-before-private-validation barrier, any scientific method, or any original/final evidence. The public-only boundary verdict in v1 remains applicable. This closure is a source review; it does not execute the principal reader. The principal's completed-stage release separately binds the same revised reader hash.
