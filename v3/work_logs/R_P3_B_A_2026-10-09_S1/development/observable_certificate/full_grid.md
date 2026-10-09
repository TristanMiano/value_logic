# Complete baseline and centered public-certificate grid

All23 previously specified episodes are retained. Displayed upper bounds are rounded upward to six decimal places. Exact Fraction values and input hashes are in the baseline and centered public result JSON. This table reads no private scores. No policy, service, RNG or truth computation is performed.

| Kind | T / B | State | Seed | Baseline terminal upper | Centered terminal upper | Baseline Brier upper | Centered Brier upper |
|---|---|---|---:|---:|---:|---:|---:|
| uniform | 992 / 2 | exact | 307201 | 331.099885 | 325.071426 | 481.539183 | 476.276307 |
| uniform | 992 / 2 | 16 | 307201 | 331.368760 | 325.233678 | 480.491473 | 475.145413 |
| uniform | 992 / 4 | exact | 307201 | 523.998673 | 504.488747 | 478.348719 | 462.258387 |
| uniform | 992 / 4 | 16 | 307201 | 523.903733 | 504.338018 | 477.945104 | 461.781359 |
| uniform | 992 / 8 | exact | 307201 | 581.539994 | 558.138417 | 442.062920 | 405.775526 |
| uniform | 992 / 8 | 16 | 307201 | 581.562104 | 558.134308 | 442.017811 | 405.712214 |
| uniform | 992 / 16 | exact | 307201 | 691.335923 | 629.178790 | 467.380657 | 407.113531 |
| uniform | 992 / 16 | 16 | 307201 | 691.337067 | 629.165019 | 467.365339 | 407.081348 |
| uniform | 3968 / 2 | exact | 307201 | 1,112.105408 | 1,109.533960 | 1,919.503548 | 1,917.696874 |
| uniform | 3968 / 2 | 16 | 307201 | 1,117.197693 | 1,113.683494 | 1,900.231452 | 1,898.115029 |
| uniform | 3968 / 4 | exact | 307201 | 1,739.992905 | 1,725.510692 | 1,785.572130 | 1,782.829918 |
| uniform | 3968 / 4 | 16 | 307201 | 1,732.815995 | 1,717.747965 | 1,813.595002 | 1,808.588796 |
| uniform | 3968 / 8 | exact | 307201 | 2,041.282517 | 2,012.418851 | 1,701.219478 | 1,672.282554 |
| uniform | 3968 / 8 | 16 | 307201 | 2,041.466126 | 2,012.253451 | 1,699.711845 | 1,670.306538 |
| uniform | 3968 / 16 | exact | 307201 | 2,290.110474 | 2,176.804414 | 1,499.081590 | 1,385.259977 |
| uniform | 3968 / 16 | 16 | 307201 | 2,290.180970 | 2,176.757359 | 1,498.854138 | 1,384.917878 |
| uniform | 992 / 8 | exact | 307203 | 576.115891 | 543.384998 | 402.905118 | 373.027064 |
| uniform | 992 / 8 | 16 | 307203 | 576.113114 | 543.367688 | 402.854956 | 372.961022 |
| uniform | 992 / 8 | exact | 307207 | 560.111573 | 531.600892 | 402.052589 | 371.612489 |
| uniform | 992 / 8 | 16 | 307207 | 560.143937 | 531.609404 | 402.017129 | 371.553412 |
| adaptive | 992 / 4 | 16 | 307201 | 620.687897 | 541.751162 | 485.349656 | 410.805818 |
| adaptive | 992 / 8 | 16 | 307201 | 759.784986 | 660.390408 | 556.673143 | 444.624649 |
| adaptive | 3968 / 8 | 16 | 307201 | 2,482.545414 | 2,208.940439 | 1,762.685237 | 1,531.656728 |

The baseline coverage statements are separate per metric. The centered design uses a shared sampling event; its joint terminal/Brier statement is fixed-end and per episode under fresh fair bits. Fixed seeds do not establish coverage; no simultaneous23-arm guarantee is made.
