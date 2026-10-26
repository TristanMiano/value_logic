# Prospective matroid extension screen

Codex (GPT-6), s18 DEVELOPMENT. Check the one-sided ordered exchange
matching on every priority order and every basis of the six-edge K4
graphic matroid, and on bounded additional uniform and binary-linear
matroids. This deliberately includes cases beyond merely partition
matroids. Find a matching by complete permutation search, independently
of the Hall proof. For sampled tied utility vectors, check that every
suboptimal greedy basis has a strict true inverted local comparison at
every optimal reported basis.

Then run200 fixed-seed streams of100 rounds over changing matroid base
families on at most7 elements, with zero through three corrupted rounds.
Use ordinary greedy and path ranking; count true-suboptimal choices and
check the stated finite bound. This is not exhaustive online verification,
and finite stream outcomes cannot sharpen the general bound. Preserve
source/result hashes and count cases; do not claim a full-cost improvement.

The frozen [checker](matroid_check.py) passed once on Python3.12.14 in
1,467,808,500ns; SHA256
880e54130fd9ab82d026f180ba238ec5a040fcfe99741b2fc08f7884712cb812.
The [result](matroid_result.json) records17,760 exchange matchings,
7,832 strict inverted witnesses and20,000 stream rounds. Every matching,
false-pair count and stated mistake bound held. The oracle counts include
138,224 greedy and255,618 exchange feasibility queries. These counts
describe this construction screen; they do not compare complete workloads.
