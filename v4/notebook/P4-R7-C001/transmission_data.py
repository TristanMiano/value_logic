"""Summarize the publisher-archived trajectory statistics for W7.1.

Pass the authors' figshare.zip or a directory containing the three listed
members (either under the original paths or with their basenames).
Requires rdata==1.0.0 and its dependencies. No raw tracks are redistributed.
"""

import argparse
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import rdata


MEMBERS = {
    "figshare/data/it-measures/globalITMeasures.RData":
        "a948f72144202b39b3318b93f696988ee17b5b9dc3bf6d9829d81def0dd7149f",
    "figshare/data/it-measures/globalITMeasuresControlRandomPairs.RData":
        "3303a1bc2359b4e7a7715a99df249ad04f118e1e77f6e2a694938b29dc50aa71",
    "figshare/data/birdsExperimentalId.txt":
        "91ef170069ac1f9e41db82e173abc55e5e90a489400f325333e30cc998b3cf81",
}


def read_members(source):
    result = []
    for name, digest in MEMBERS.items():
        if source.is_dir():
            local = source/name
            if not local.exists():
                local = source/Path(name).name
            raw = local.read_bytes()
        else:
            with ZipFile(source) as archive:
                raw = archive.read(name)
        if sha256(raw).hexdigest() != digest:
            raise ValueError(f"Unexpected content in {name}")
        if name.endswith(".RData"):
            result.append(rdata.read_rda(BytesIO(raw))["df"])
        else:
            result.append(pd.read_csv(BytesIO(raw), sep=r"\s+"))
    return result


def role_changes(frame, roles):
    columns=["TEenr","TEner"]
    pair=frame.groupby("Pair")[columns].mean().join(roles.set_index("Pair"))
    pair["net"]=pair.TEner-pair.TEenr
    pivot=pair.pivot(index="chain",columns="Generation",values="net")
    paired=pivot[[2,5]].dropna()
    change=paired[5]-paired[2]
    print("Novice-minus-experienced by generation",pair.groupby("Generation").net.mean().round(6).to_dict())
    print("Last minus first, complete chains",len(change),round(change.mean(),6),
          "declined",int((change<0).sum()))
    # One bird first in the newcomer role later flies with a different novice.
    former=pair.set_index("Naive")
    later=pair[pair.Experienced.isin(former.index)].set_index("Experienced")
    old=former.loc[later.index]
    diff=later.TEenr-old.TEner
    print("Same bird's outgoing transfer after becoming experienced:",len(diff),
          round(diff.mean(),6),"increased",int((diff>0).sum()))


def matched_surrogates(actual, controls, roles):
    # The source R loop writes the position of the focal pair within its
    # generation, but the ControlPair column contains the global pair ID.
    lookup={(g,i):pair for g,z in roles.groupby("Generation")
            for i,pair in enumerate(sorted(z.Pair),1)}
    c=controls.copy()
    c["focal"]=[lookup[g,i] for g,i in zip(c.Gen,c.Pair)]
    same=c.focal==c.ControlPair
    duplicate=c[same & (c.Release==c.ControlRelease)]
    duplicate=duplicate.merge(actual,left_on=["focal","Release"],right_on=["Pair","Release"],
                              validate="one_to_one")
    for field in ("TEenr","TEner","ERer","ERnr"):
        assert (duplicate[field+"_x"]==duplicate[field+"_y"]).all()
    # Every within-generation/global mapping after generation 2 is certified
    # by at least one exact four-statistic match on the same release.
    assert set(duplicate.focal)==set(roles.loc[roles.Generation>2,"Pair"])
    clean=c[~same]
    focal=clean.groupby(["focal","Release"])[["TEenr","TEner"]].mean()
    focal.index=focal.index.set_names(["Pair","Release"])
    physical=actual.set_index(["Pair","Release"])[["TEenr","TEner"]]
    assert len(focal)==len(physical) and focal.index.difference(physical.index).empty
    excess=physical-focal
    print("Surrogate rows, same pair, same flight",len(c),int(same.sum()),len(duplicate))
    print("Filtered comparators (row weighted)",clean[["TEenr","TEner"]].mean().round(6).to_dict())
    print("Distinct-pair controls per focal flight",focal.mean().round(6).to_dict())
    print("Actual minus matched controls by direction",excess.mean().round(6).to_dict(),
          "positive flights",(excess>0).sum().to_dict())
    pair=excess.groupby(level="Pair").mean().join(roles.set_index("Pair")["Generation"])
    corrected=(pair.TEner-pair.TEenr).groupby(pair.Generation).mean()
    print("Adjusted novice-minus-experienced by generation",corrected.round(6).to_dict())
    assert focal.index.get_level_values(0).nunique()==len(roles)


def summarize(observed, controls, pair_roles):
    # Follow the initially naive member as it becomes the experienced member
    # of a new pair. This handles the renumbering after chains dropped out.
    origin, chain = {}, {}
    for row in pair_roles.sort_values("Generation").itertuples():
        root = row.Pair if row.Generation == 2 else origin[row.Experienced]
        origin[row.Naive] = root
        chain[row.Pair] = root
    for history, step in [(10, 1), (7, 5)]:
        frame = observed[(observed.K == history) & (observed.SS == step)].copy()
        frame["chain"] = frame.Pair.map(chain)
        frame["novice_higher"] = frame.TEner > frame.TEenr
        assert not frame.isna().any().any()
        assert not frame.duplicated(["Pair", "Release"]).any()
        by_chain = frame.groupby("chain")[["TEenr", "TEner", "novice_higher"]].mean()
        print(f"History {history}, step {step}: {len(frame)} flights, "
              f"{frame.Pair.nunique()} pairs, {len(by_chain)} chains")
        print("Novice-to-experienced larger, flights and chain means:",
              int(frame.novice_higher.sum()), int((by_chain.TEner > by_chain.TEenr).sum()))
        print("Mean of chain means:", by_chain.mean().round(6).to_dict())
        print("Unweighted flight means:", frame[["TEenr", "TEner"]].mean().round(6).to_dict())
        role_changes(frame,pair_roles.assign(chain=pair_roles.Pair.map(chain)))
        if (history,step)==(10,1):
            matched_surrogates(frame,controls,pair_roles)
    assert set(controls.K) == {10} and set(controls.SS) == {1}
    print("Surrogate pairings:", len(controls), controls[["TEenr", "TEner"]].mean().round(6).to_dict())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    summarize(*read_members(parser.parse_args().source))
