# Reproducing W7's first recurrence

From the repository root, run the small examples, proofs with executable checks, and seeded simulations with Python. The tested environment used Python 3.13.14, NumPy 2.2.5, SciPy 1.15.3, pandas 2.3.3, rdata 1.0.0 and xarray 2025.1.2. The last two packages read the archived R data. Run these commands in an environment of your choice.

```console
python -m pip install numpy==2.2.5 scipy==1.15.3 pandas==2.3.3 rdata==1.0.0 xarray==2025.1.2
python v4/notebook/P4-R7-C001/replay.py
python v4/notebook/P4-R7-C001/replay.py --data PATH_TO_DATA
python v4/notebook/clock.py v4/notebook/P4-R7-C001/timing.jsonl --sum
```

The first replay needs no data downloads and runs 21 programs. The second also runs eleven archive analyses. Each program prints its numerical results and checks its recorded inputs or internal identities. One can run any program individually with the arguments in [replay.py](replay.py). Numerical optimization uses SciPy's HiGHS solver where indicated; the Warsaw results additionally verify rational certificates. Several ancillary literature comparisons use published aggregate counts, identified alongside their sources in the six [result notes](record.md).

Place the following files in a single data directory, keeping the basenames listed. The analysis scripts pin the bytes they read by SHA-256. The scientific data remain with their respective depositors.

| Public source | Files in the data directory |
| --- | --- |
| [Valentini et al., pigeon transmission archive](https://doi.org/10.6084/m9.figshare.14043362) | From `figshare.zip` take `globalITMeasures.RData`, `globalITMeasuresControlRandomPairs.RData` and `birdsExperimentalId.txt`. These contain the authors' flight measures and identities. |
| [Chimento, Alarcón-Nieto and Aplin, great-tit turnover archive](https://doi.org/10.5281/zenodo.4644347) | `df_solves.Rda` and `df_surv.Rda` from the publication's v2.0 data directory. |
| [Scheel, Schijen and Lakens, hypothesis-support table](https://github.com/amscheel/positive_result_rates/blob/442ef4c78c921ffa8f5b3ec1d0f2c55a852467be/raw_data/positive_results_in_registered_reports_data.tsv) | `positive_results_in_registered_reports_data.tsv` |
| [Toyokawa, Whalen and Laland, group choice data](https://github.com/WataruToyokawa/ToyokawaWhalenLaland2018/blob/9415e1b04d615a3d2f0a6cd2066a253c2f8c3e40/data/allBehaviouralData2.csv) | `allBehaviouralData2.csv` |
| [Pabulib, Wesoła](https://github.com/pabulib/pabulib_files/blob/beda04462f2fbee240202510b860106ee9754dd4/pb_files/Poland_Warszawa_2020_Wesola.pb) and [Żoliborz](https://github.com/pabulib/pabulib_files/blob/beda04462f2fbee240202510b860106ee9754dd4/pb_files/Poland_Warszawa_2020_Zoliborz.pb) | `Poland_Warszawa_2020_Wesola.pb` and `Poland_Warszawa_2020_Zoliborz.pb` |
| [Cook, Kay and Regier, World Color Survey](https://linguistics.berkeley.edu/wcs/data.html) | The intact archive `WCS-Data-20110316.zip`; the decoder reads the chip coordinates, local dictionary and naming responses. |
| [Devine et al., experiment-two data prepared for modeling](https://github.com/seandamiandevine/choiceval/blob/29f1cb817de925c6ff82244d6d6205dccf1eee1a/exp2/models/choice_exp2_clean.csv) | `choice_exp2_clean.csv`; the replay reads only a subject key, trial ordering, contingency and choice. |
