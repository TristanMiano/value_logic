"""Fixed descriptive-policy source primitives; DEVELOPMENT, Codex GPT-6."""
from fractions import Fraction as F
from bank_compact import log_upper


def gamma(n):
    assert type(n) is int and n>0
    b=bin(n)[2:]
    return '0'*(len(b)-1)+b


def read_gamma(bits,pos=0):
    start=pos
    while pos<len(bits) and bits[pos]=='0':pos+=1
    assert pos<len(bits)
    size=pos-start+1;end=pos+size;assert end<=len(bits)
    return int(bits[pos:end],2),end


def encode(payload):
    assert set(payload)<={'0','1'}
    return gamma(len(payload)+1)+payload


def decode(code):
    n,pos=read_gamma(code);n-=1
    assert len(code)==pos+n
    return code[pos:]


def parity_code(mask,dimension,invert=0):
    assert 0<=mask<1<<dimension and invert in (0,1)
    return encode('10'+format(mask,f'0{dimension}b')+str(invert))


def table_code(positive_ids,dimension):
    ids=sorted(set(positive_ids));assert all(0<=x<1<<dimension for x in ids)
    return encode('11'+gamma(len(ids)+1)+''.join(format(x,f'0{dimension}b') for x in ids))


def parse(code,dimension):
    payload=decode(code);tag=payload[:2]
    if tag in ('00','01'):
        assert len(payload)==2
        return 'constant',int(tag[1])
    if tag=='10':
        assert len(payload)==3+dimension
        return 'parity',(int(payload[2:2+dimension],2),int(payload[-1]))
    assert tag=='11';n,pos=read_gamma(payload,2);n-=1
    assert len(payload)==pos+n*dimension
    ids=[int(payload[pos+i*dimension:pos+(i+1)*dimension],2) for i in range(n)]
    assert ids==sorted(set(ids))
    return 'table',frozenset(ids)


def predict(parsed,x):
    kind,arg=parsed
    if kind=='constant':return arg
    if kind=='parity':return (arg[0]&x).bit_count()%2^arg[1]
    assert kind=='table'
    return int(x in arg)


def point_bound(total,t,length,alpha=F(1,20),max_k=16):
    assert isinstance(total,F) and 0<=total<=t and type(t) is int and t>0 and type(length) is int and length>0
    choices=[]
    for k in range(max_k+1):
        lam=F(1,1<<k);risk=alpha/F((k+1)*(k+2));penalty=length*log_upper(F(2))+log_upper(1/risk)
        lower=total/t-penalty/(lam*t)-lam/8
        choices.append((lower,k))
    value,k=max(choices)
    return dict(lower=max(F(0),value),raw=value,k=k,lambda_=F(1,1<<k),length=length)
