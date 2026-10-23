"""Create a versioned flow-LP variant; preserve the exposed predecessor."""
import hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
old=p/'channel_lp.py';new=p/'weight_channel.py'
assert not new.exists()
s=old.read_text(encoding='utf-8')
changes=[
    ("OUT=HERE/'channel_lp.json'","OUT=HERE/'weight_channel.json'"),
    ("RAW=HERE/'channel_lp_raw.json'","RAW=HERE/'weight_channel_raw.json'"),
    ('beta_index','a_index'),
    ("('beta',)","('a',)"),
    ('def sign(x):','def weight(x):'),
    ('return (-1)**(c&1)','return c.bit_count()'),
    ('F(-sign(x),2)','F(-weight(x))'),
    ('rhs[row]=F(1,2)','rhs[row]=F(0)'),
    ("beta=str(primal[-1]),success_probability=str((1+primal[-1])/2)",
     "a=str(primal[-1]),minimum_wrong_acceptance=str(3*primal[-1])"),
    ("Optimal symmetric binary channel for selected Q coordinate with <=5 raw queries; count5/6 adapter.",
     "Optimal depth-five channel with acceptance a*weight(Q(x)); count5/6 adapter.")]
for before,after in changes:
    assert before in s,before
    s=s.replace(before,after)
s='# Derived from channel_lp.py SHA256 '+hashlib.sha256(old.read_bytes()).hexdigest()+'\n'+s
new.write_text(s,encoding='utf-8')
print(new.name,hashlib.sha256(new.read_bytes()).hexdigest())
