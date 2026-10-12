#!/usr/bin/env python3
"""Fixed-action vertex certificates and prior-free finite audit decision trees.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT.
Input witnesses and lower proofs must actually be admitted. No logical search,
no hidden outcomes and no prior occur in these interfaces. Exact rationals.
"""
from __future__ import annotations
from fractions import Fraction as F


def dot(mask, weights, meter):
    meter.pay('vertex_query', 'mask_weight_products_and_sum', 2*len(weights))
    return sum(w for j,w in enumerate(weights) if mask & (1 << j))


def anchor_certificate(action, vertices, checked_lowers, price, meter):
    """Admitted scalar bounds at hull anchors suffice, even without repricing.

    action=None is replacement; otherwise it is a checked violation mask.
    Source identity and exact objective matching are admission obligations of
    the caller. The declared source W must be contained in conv(vertices).
    """
    if not vertices or len(vertices) != len(checked_lowers):
        raise ValueError('One admitted lower bound for every nonempty anchor list')
    if any(len(v) != len(vertices[0]) or any(F(w)<0 for w in v) for v in vertices):
        raise ValueError('Common ordered nonnegative cost coordinates required')
    terms = []
    for v, lower in zip(vertices, checked_lowers):
        cost = F(price) if action is None else dot(action,v,meter)
        terms.append(cost-min(F(price),F(lower)))
    meter.pay('vertex_certificate','anchor_clipping_gap_and_maximum',4*len(vertices))
    return max([F(0)]+terms)


class Regions:
    """Compile all fixed-action point bounds from the same admitted bank.

    A region contains the hypotheses at which one fixed action's point bound
    closes. Per-vertex proof choice is safe because true regret is convex, not
    because the maximum of retained concave lower functions is concave.
    """
    def __init__(self, profiles, vertices, price, tolerance, meter):
        self.profiles,self.vertices = profiles,[tuple(map(F,v)) for v in vertices]
        self.price,self.tolerance,self.meter=F(price),F(tolerance),meter
        if not vertices or any(len(v)!=len(vertices[0]) or any(x<0 for x in v) for v in self.vertices):
            raise ValueError('Finite common nonnegative cost vectors required')
        self.records=[]
        for profile in profiles:
            trees=profile['trees'] or [dict(leaf_masks=[0],receipt_id='nonnegative_objective')]
            lower=[]
            for vertex in self.vertices:
                one=[]
                for tree in trees:
                    if not tree['leaf_masks']:
                        raise ValueError('Empty unadmitted proof support')
                    value=min(dot(z,vertex,meter) for z in tree['leaf_masks'])
                    one.append((value,tree['receipt_id']))
                    meter.pay('vertex_compile','proof_leaf_minimum',len(tree['leaf_masks']))
                lower.append(one)
            actions=[]
            for witness in profile['witnesses']+[None]:
                mask=None if witness is None else witness['violation_mask']
                model=None if witness is None else witness['model']
                costs=[self.price if mask is None else dot(mask,v,meter) for v in self.vertices]
                table=[[max(F(0),costs[h]-min(self.price,l)) for l,_ in ll] for h,ll in enumerate(lower)]
                stitched=[min(row) for row in table]
                proof_ids=[lower[h][min(range(len(row)),key=lambda j:row[j])][1] for h,row in enumerate(table)]
                actions.append(dict(model=model,mask=mask,witness_id=None if witness is None else witness['receipt_id'],
                                    point_bounds=stitched,point_proof_ids=proof_ids,per_proof_bounds=table))
                meter.pay('vertex_compile','action_vertex_proof_table',4*len(vertices)*len(trees)+6)
            self.records.append(dict(row=profile['row'],source_identity=profile['source_identity'],actions=actions))

    def best(self, row, subset, method='stitched'):
        if not subset:
            raise ValueError('An impossible/empty source is not a certificate')
        record=self.records[row]
        options=[]
        for index,a in enumerate(record['actions']):
            if method=='stitched':
                value=max(a['point_bounds'][h] for h in subset)
            elif method=='single_proof':
                value=min(max(a['per_proof_bounds'][h][t] for h in subset)
                          for t in range(len(a['per_proof_bounds'][0])))
            else:
                raise ValueError('Unknown proof policy')
            self.meter.pay('region_query','fixed_action_subset_check',len(subset)*(1 if method=='stitched' else len(a['per_proof_bounds'][0])))
            options.append((value,index))
        value,index=min(options)
        a=record['actions'][index]
        return dict(row=record['row'],bound=value,action='replace' if a['mask'] is None else 'repair',
                    model=a['model'],mask=a['mask'],witness_id=a['witness_id'],
                    point_proof_ids=[a['point_proof_ids'][h] for h in subset] if method=='stitched' else None)


class AuditPlan:
    """Exact minimax observation count for this fixed finite evidence state.

    No outcome probabilities. Every test outcome is a declared coordinate of
    a possible *single-row* mode. Terminal each requested source has one fixed
    checked action over the remaining hull. The bounded state table is paid.
    No logical acquisition or unknown economic tariff is inferred by the DP.
    """
    def __init__(self,regions,rows,method='stitched',prices=None,max_states=128):
        self.regions,self.rows,self.method=regions,tuple(rows),method
        self.prices=tuple(map(F,prices or [1]*len(regions.vertices[0])))
        if len(self.prices)!=len(regions.vertices[0]) or any(c<=0 for c in self.prices):
            raise ValueError('Positive complete audit prices required')
        self.memo,self.max_states={},max_states

    def solve(self,subset=None):
        subset=tuple(range(len(self.regions.vertices))) if subset is None else tuple(subset)
        if not subset or len(set(subset))!=len(subset):
            raise ValueError('Nonempty distinct source hypotheses required')
        if subset in self.memo:
            self.regions.meter.pay('audit_plan','memo_lookup')
            return self.memo[subset]
        if len(self.memo)>=self.max_states:
            raise ValueError('Planning state cap: unresolved')
        terminal=[self.regions.best(r,subset,self.method) for r in self.rows]
        self.regions.meter.pay('audit_plan','terminal_request_checks',len(terminal))
        if all(t['bound']<=self.regions.tolerance for t in terminal):
            result=dict(subset=subset,cost=F(0),status='stop',actions=terminal)
            self.memo[subset]=result
            return result
        # Install a placeholder so the resource cap includes in-flight states.
        self.memo[subset]=dict(subset=subset,cost=None,status='unresolved')
        choices=[]
        for j,cost in enumerate(self.prices):
            parts={}
            for h in subset:
                parts.setdefault(self.regions.vertices[h][j],[]).append(h)
            self.regions.meter.pay('audit_plan','declared_outcome_partition',2*len(subset)+1)
            if len(parts)<=1:
                continue
            children=[(value,self.solve(tuple(ids))) for value,ids in sorted(parts.items())]
            if any(child['cost'] is None for _,child in children):
                continue
            quote=cost+max(child['cost'] for _,child in children)
            choices.append((quote,j,[(value,child['subset']) for value,child in children]))
            self.regions.meter.pay('audit_plan','complete_worst_outcome_quote',2*len(children)+2)
        if choices:
            cost,j,branches=min(choices)
            result=dict(subset=subset,cost=cost,status='audit',coordinate=j,branches=branches)
        else:
            result=dict(subset=subset,cost=None,status='unresolved',
                        reason='No audit-only guaranteed completion with the currently admitted bank and declared menu')
        self.memo[subset]=result
        self.regions.meter.pay('audit_plan','state_storage',6+len(subset))
        return result

    def record(self):
        return [self.memo[s] for s in sorted(self.memo,key=lambda s:(len(s),s))]
