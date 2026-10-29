"""Bind the partial-range and decision interfaces to one copied source model."""
from copy import deepcopy
from fractions import Fraction as F
from partial import PartialRange, V
import decision_cells as cells
import refinement_gap as refine
import incumbent_value as observe


class DecisionService:
    def __init__(self, problem):
        self._problem = deepcopy(problem)
        self._range = PartialRange(self._problem)
        self.revision = 0

    @property
    def problem_sha256(self):
        return self._range.problem_sha256

    def add_source(self, source, digest):
        V.require(digest == self.problem_sha256,'problem digest mismatch')
        V.require(len(source) == len(self._problem['generators']),'source block count')
        points = []
        for g,raw in zip(self._problem['generators'],source):
            x = V.vector(raw,len(g['c']))
            V.require(all(V.dot(V.vector(row,len(x)),x) <= V.rational(b)
                          for row,b in zip(g['A'],g['b'])),'source violates base')
            points.append(x)
        for receipt in self._problem['receipts']:
            q = min(V.dot(V.vector(f['c'],len(x)),x)+V.rational(f['d'])
                    for f,x in zip(receipt['forms'],points))
            V.require(V.rational(receipt['lo']) <= q <= V.rational(receipt['hi']),
                      'source violates receipt')
        pending = deepcopy(self._range)
        for i,x in enumerate(points):
            pending.add_point(i,list(map(str,x)),digest)
        self._range = pending
        self.revision += 1

    def propagate(self,passes=2):
        pending = deepcopy(self._range)
        visits,updates = 0,0
        for i in range(pending.n):
            for mask in range(1 << pending.k):
                r = pending.propagate_box(i,mask,passes)
                visits += r['row_visits']
                updates += r['coordinate_updates']
        self._range = pending
        self.revision += 1
        return dict(row_visits=visits,coordinate_updates=updates,optimizer_calls=0)

    def assess(self,breakpoints,losses,signals,incumbent,criterion='loss'):
        request = deepcopy(dict(breakpoints=breakpoints,losses=losses,
            signals=signals,incumbent=incumbent,criterion=criterion))
        bracket = self._range.bracket()
        common = dict(problem_sha256=self.problem_sha256,revision=self.revision,
            decision_sha256=V.digest(request),bracket=bracket,
            mathematical_source_nonempty_proved=bool(bracket['inner']),
            source_premises='conditional on the stated model and receipt bounds')
        if bracket['inconsistent']:
            return dict(common,status='INCONSISTENT_SOURCE')
        computation = refine.assess(bracket,breakpoints,losses,criterion)
        observation = observe.assess(bracket,breakpoints,losses,signals,incumbent,criterion)
        sources = {}
        for cell,q in computation['inner_witnesses'].items():
            witness = self._range.query(q,q)
            V.require(witness['status'] == 'ATTAINABLE','inner cell lacks source')
            sources[str(cell)] = witness
        return dict(common,status='CHECKED_DECISION' if sources else 'CONDITIONAL_ON_NONEMPTY_SOURCE',
            computation=computation,observation=observation,known_cell_sources=sources)

    def evidence_state(self):
        return self._range.state()
