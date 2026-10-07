"""Arithmetic verification of P3-02 finite-information certificates.

ChatGPT (GPT-6 Astra Pro), 2026-10-07. DEVELOPMENT.
This checker imports no row-reduction routine or generator. It checks row
identities, actual normalized-law collisions, and repair necessity/sufficiency
certificates using exact rational arithmetic. Summary rank fields are not
independently certified here. Semantic payoff/source/nuisance premises remain
external. This is separate from the inherited native-language proof checker.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def number(x):
    require(type(x) in {str,int} or isinstance(x,F),'Expected an exact rational.')
    try:
        return F(x)
    except (ValueError,ZeroDivisionError) as exc:
        raise InvalidCertificate('Malformed rational.') from exc


def vector(v,n):
    require(isinstance(v,list) and len(v)==n,'Vector dimension mismatch.')
    return [number(x) for x in v]


def rows(v,n):
    require(isinstance(v,list),'Rows must be a list.')
    return [vector(row,n) for row in v]


def dot(a,b):
    require(len(a)==len(b),'Dot dimensions differ.')
    return sum((x*y for x,y in zip(a,b)),F(0))


def combination(weights,matrix,n):
    weights=vector(weights,len(matrix))
    return [sum((weights[j]*matrix[j][i] for j in range(len(matrix))),F(0)) for i in range(n)]


def effective(losses,offset_unknown):
    if offset_unknown:
        return [[row[i]-losses[0][i] for i in range(len(row))] for row in losses[1:]] if losses else []
    return losses


def verify_target(c,cert,losses,matrix,n,scale_unknown,offset_unknown,counts):
    require(type(cert.get('recoverable')) is bool,'Missing Boolean target verdict.')
    kind=cert.get('kind')
    if cert['recoverable']:
        if kind=='constant':
            require(c==[number(cert['value'])]*n,'False constant target.')
        elif kind=='affine':
            require(not scale_unknown,'An uncalibrated scale cannot use this affine certificate.')
            represented=combination(cert['effective_coefficients'],matrix,n)
            require([x+number(cert['constant']) for x in represented]==c,'Affine row identity fails.')
        elif kind=='ratio_of_scaled_linear_targets':
            require(scale_unknown,'Unexpected ratio certificate for a known-scale contract.')
            require(combination(cert['normalizer_coefficients'],matrix,n)==[F(1)]*n,
                    'Normalizer does not equal the constant-one row.')
            require(combination(cert['numerator_coefficients'],matrix,n)==c,'Numerator row identity fails.')
        else:
            raise InvalidCertificate('Unknown positive certificate type.')
        counts['positive_target_certificates']+=1
        return
    require(kind=='indistinguishable_laws','Unknown negative certificate type.')
    w=cert['witness']
    p,q=vector(w['p'],n),vector(w['q'],n)
    require(min(p)>0 and min(q)>0 and sum(p)==sum(q)==1,'Witness laws are not interior normalized laws.')
    sp,sq=number(w['scale_p']),number(w['scale_q'])
    bp,bq=number(w['offset_p']),number(w['offset_q'])
    require(sp>0 and sq>0,'Witness scale is not positive.')
    if not scale_unknown:
        require(sp==sq==1,'Witness changed a known scale.')
    if not offset_unknown:
        require(bp==bq==0,'Witness changed a known offset.')
    vp=[sp*dot(row,p)+bp for row in losses]
    vq=[sq*dot(row,q)+bq for row in losses]
    require(vp==vq==vector(w['observation'],len(losses)),'Witness records do not coincide.')
    tp,tq=dot(c,p),dot(c,q)
    require(tp!=tq,'Witness target does not separate.')
    require(tp==number(w['target_p']) and tq==number(w['target_q']),'Saved witness target is wrong.')
    counts['negative_target_certificates']+=1


def verify(record):
    require(record.get('schema')=='P3-02-finite-information-audit/v1','Unknown artifact schema.')
    require(record.get('stage')=='development','This is a development certificate format.')
    n=record.get('n_states')
    require(type(n) is int and n>=1,'Invalid state count.')
    cal=record.get('calibration')
    require(type(cal) is str and cal in {'known','unknown_offset','unknown_scale','unknown_affine'},'Invalid calibration contract.')
    su=cal in {'unknown_scale','unknown_affine'}
    ou=cal in {'unknown_offset','unknown_affine'}
    L,C=rows(record['losses'],n),rows(record['targets'],n)
    M=effective(L,ou)
    require(rows(record['effective_rows'],n)==M,'Effective rows do not match the declared calibration.')
    counts={'positive_target_certificates':0,'negative_target_certificates':0,'repair_dual_pairings':0}
    require(type(record.get('all_targets_recoverable')) is bool and type(record.get('full_law_recoverable')) is bool,
            'Summary verdicts must be Boolean.')
    certs=record['target_certificates']
    require(len(certs)==len(C),'Target certificate count differs.')
    for c,cert in zip(C,certs):
        verify_target(c,cert,L,M,n,su,ou,counts)
    require(record['all_targets_recoverable']==all(c['recoverable'] for c in certs),'Target summary flag differs.')
    law=record['law_certificate']
    if record['full_law_recoverable']:
        require(law['kind']=='coordinate_decoders' and len(law['coordinates'])==n,'Missing full-law decoders.')
        for i,cert in enumerate(law['coordinates']):
            require(cert['recoverable'],'A full-law coordinate is not recovered.')
            verify_target([F(i==j) for j in range(n)],cert,L,M,n,su,ou,counts)
    else:
        i=law['coordinate']
        require(law['kind']=='separating_coordinate' and type(i) is int and 0<=i<n,'Missing full-law obstruction.')
        require(not law['certificate']['recoverable'],'No separating coordinate was supplied.')
        verify_target([F(i==j) for j in range(n)],law['certificate'],L,M,n,su,ou,counts)
    rep=record['repair']
    extra=rows(rep['extra_loss_rows'],n)
    Q=rows(rep.get('added_effective_rows',[]),n)
    H=rows(rep.get('lower_bound_hidden_directions',[]),n)
    nonconstant=any(any(x!=c[0] for x in c) for c in C)
    ref_needed=int(ou and not L and nonconstant)
    r=rep['effective_rank_deficit']
    require(type(r) is int and r>=0 and r==len(Q)==len(H),'Repair dimension certificate differs.')
    require(rep['new_reference_queries']==ref_needed,'Wrong extra reference count.')
    require(rep['minimum_extra_raw_queries']==len(extra)==r+ref_needed,'Repair count differs.')
    if not nonconstant:
        require(r==0 and not extra,'A constant-only target does not need a repair.')
    required=([[F(1)]*n]+C) if su else C
    require(all(q in required for q in Q),'A selected lower-bound row is not required by the target contract.')
    B=M if su else [[F(1)]*n]+M
    for j,h in enumerate(H):
        require(all(dot(b,h)==0 for b in B),'Repair direction is visible in old information.')
        require([dot(q,h) for q in Q]==[F(i==j) for i in range(r)],'Repair pairing is not the identity.')
        counts['repair_dual_pairings']+=r
    reference=L[0] if ou and L else [F(0)]*n
    expected=([[F(0)]*n] if ref_needed else [])
    expected += [[x+y for x,y in zip(reference,q)] if ou else q for q in Q]
    require(extra==expected,'Raw repair rows do not implement the certified effective rows.')
    newL=L+extra
    newM=effective(newL,ou)
    repaired=rep['repaired_target_certificates']
    require(len(repaired)==len(C),'Repaired target count differs.')
    for c,cert in zip(C,repaired):
        require(cert['recoverable'],'Proposed repair leaves a target unresolved.')
        verify_target(c,cert,newL,newM,n,su,ou,counts)
    return counts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact',type=Path)
    args=parser.parse_args()
    counts=verify(json.loads(args.artifact.read_text()))
    print(json.dumps({'status':'verified','artifact':str(args.artifact),'checked':counts},sort_keys=True))


if __name__=='__main__':
    main()
