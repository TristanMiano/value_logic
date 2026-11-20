"""Compare published first-hypothesis support across two review arrangements."""
import csv
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import sys

DIGEST="d2cefdc657c8956bc67c945076b048c66b2be6c816adf5d7f9cf8a088321fab3"


def summarize(rows,label):
    for full_only in (False,True):
        counts=[]
        for arrangement in ("0","1"):
            group=[r for r in rows if r["is_RR"]==arrangement]
            yes=sum((r["support"]=="support") if full_only else (r["support_binary"]=="1") for r in group)
            counts.append((yes,len(group)-yes))
        (a,b),(c,d)=counts
        odds=F(a*d,b*c) if b*c else None
        print(label,"full only" if full_only else "full or partial",counts,
              "support odds ratio",odds,"fourfold sensitivity",odds/4 if odds is not None else None)
        if label=="all":
            assert a+b==152 and c+d==71
        if label=="other work" and not full_only:
            assert odds==F(71,3)


def main(path):
    assert sha256(path.read_bytes()).hexdigest()==DIGEST,"unexpected source table"
    with path.open(encoding="utf8",newline="") as f:
        all_rows=list(csv.DictReader(f,delimiter="\t"))
    rows=[r for r in all_rows if r["include_in_analysis"]=="1"]
    assert all((r["support_binary"]=="1")==(r["support"] in ("support","partial support")) for r in rows)
    print("Included/archived",len(rows),len(all_rows))
    summarize(rows,"all")
    for val,label in (("0","other work"),("1","close replication")):
        summarize([r for r in rows if r["is_replication"]==val],label)


if __name__=="__main__":
    main(Path(sys.argv[1]))
