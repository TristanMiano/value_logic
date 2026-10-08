#!/usr/bin/env python3
"""Finite edit-information adapters for P3-05. Python 3.10+, standard library.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08.
The supplied finite record/edit graph is the semantic premise. This module does
not learn it, decide arbitrary program equivalence, or give a free history oracle.
Exact-output quotients and some-acceptable-output covers are different services.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from itertools import combinations
import json

VERSION='p305-edit-information-v1'
MAX_STATES=64
MAX_EDITS=16
MAX_ACTIONS=32
MAX_LABEL_CHARS=8192
MAX_SEARCH_STATES=7
MAX_SEARCH_TRIALS=200000

class Rejected(ValueError):pass

def inc(work,key,n=1):
    if work is not None:work[key]=work.get(key,0)+n

def text(s):
    if type(s) is not str or not s or len(s)>MAX_LABEL_CHARS:raise Rejected('Bounded nonempty exact text label required.')
    return s

def index(i,n):
    if type(i) is not int or not 0<=i<n:raise Rejected('Integer index outside the supplied finite table.')
    return i

def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

@dataclass(frozen=True)
class Edit:
    name:str
    successors:tuple[int,...]
    observations:tuple[str,...]

@dataclass(frozen=True)
class Graph:
    scope:str
    states:tuple[str,...]
    outputs:tuple[str,...]
    edits:tuple[Edit,...]

    def validate(self):
        text(self.scope)
        if type(self.states) is not tuple or not 1<=len(self.states)<=MAX_STATES:raise Rejected('Finite nonempty state cap.')
        n=len(self.states)
        for s in self.states:text(s)
        if len(set(self.states))!=n:raise Rejected('State record identities must be distinct.')
        if type(self.outputs) is not tuple or len(self.outputs)!=n:raise Rejected('One exact output per state.')
        for o in self.outputs:text(o)
        if type(self.edits) is not tuple or len(self.edits)>MAX_EDITS:raise Rejected('Finite named edit cap.')
        names=[]
        for e in self.edits:
            if type(e) is not Edit:raise Rejected('Edit type.')
            names.append(text(e.name))
            if type(e.successors) is not tuple or len(e.successors)!=n:raise Rejected('Edits must be total over the declared state set.')
            if type(e.observations) is not tuple or len(e.observations)!=n:raise Rejected('One declared edge observation per state.')
            for t in e.successors:index(t,n)
            for o in e.observations:text(o)
        if len(set(names))!=len(names):raise Rejected('Named edit identities must be distinct.')

    def record(self):
        self.validate()
        return canonical({'version':VERSION,'scope':self.scope,'states':self.states,'outputs':self.outputs,
            'edits':[{'name':e.name,'successors':e.successors,'observations':e.observations} for e in self.edits]})

    def label(self,s,preserve_edges):
        return (self.outputs[s],tuple(e.observations[s] for e in self.edits) if preserve_edges else ())


def _flag(x):
    if type(x) is not bool:raise Rejected('Service flags must be Boolean.')
    return x


def partition_vector(blocks,n):
    if type(blocks) is not tuple or not 1<=len(blocks)<=n:raise Rejected('Nonempty partition required.')
    code=[None]*n
    for j,block in enumerate(blocks):
        if type(block) is not tuple or not block:raise Rejected('Nonempty immutable block required.')
        for s in block:
            index(s,n)
            if code[s] is not None:raise Rejected('Partition blocks overlap or repeat a state.')
            code[s]=j
    if any(c is None for c in code):raise Rejected('Partition omits a declared state.')
    return tuple(code)


def _classes(keys):
    groups={}
    for s,k in enumerate(keys):groups.setdefault(k,[]).append(s)
    return tuple(tuple(g) for g in groups.values())


def distinguishing_word(graph,s,t,preserve_edges=False,work=None):
    """Producer BFS, returning a word or None; no claim about unlisted edits."""
    graph.validate();_flag(preserve_edges);index(s,len(graph.states));index(t,len(graph.states))
    queue=deque([(s,t,())]);seen=set()
    while queue:
        x,y,word=queue.popleft();key=tuple(sorted((x,y)))
        if key in seen:continue
        seen.add(key);inc(work,'pair_states_visited')
        if graph.label(x,preserve_edges)!=graph.label(y,preserve_edges):return word
        for e,edit in enumerate(graph.edits):
            inc(work,'distinguishing_edges_read')
            queue.append((edit.successors[x],edit.successors[y],word+(e,)))
    return None

@dataclass(frozen=True)
class QuotientProof:
    graph_record:str
    preserve_edges:bool
    blocks:tuple[tuple[int,...],...]
    separations:tuple[tuple[int,int,tuple[int,...]],...]
    strict_refinements:int

    def record(self):return {'graph_record':self.graph_record,'preserve_edges':self.preserve_edges,
        'blocks':self.blocks,'separations':self.separations,'strict_refinements':self.strict_refinements}


def build_quotient(graph,preserve_edges=False,work=None):
    graph.validate();_flag(preserve_edges);n=len(graph.states)
    blocks=_classes(graph.label(s,preserve_edges) for s in range(n));rounds=0
    while True:
        code=partition_vector(blocks,n)
        keys=[]
        for s in range(n):
            inc(work,'refinement_states_read');inc(work,'refinement_edges_read',len(graph.edits))
            keys.append((code[s],tuple(code[e.successors[s]] for e in graph.edits)))
        new=_classes(keys)
        if new==blocks:break
        blocks=new;rounds+=1
        if rounds>=n:raise Rejected('Internal partition refinement invariant failed.')
    code=partition_vector(blocks,n);seps=[]
    for s,t in combinations(range(n),2):
        if code[s]==code[t]:continue
        word=distinguishing_word(graph,s,t,preserve_edges,work)
        if word is None:raise Rejected('Distinct quotient classes have no continuation witness.')
        seps.append((s,t,word))
    return QuotientProof(graph.record(),preserve_edges,blocks,tuple(seps),rounds)


def verify_quotient(proof,graph,expected_record,work=None,*,preserve_edges=False):
    if type(proof) is not QuotientProof or type(graph) is not Graph:raise Rejected('Quotient proof/graph types.')
    record=graph.record();_flag(proof.preserve_edges);_flag(preserve_edges)
    if proof.preserve_edges!=preserve_edges:raise Rejected('Different requested observation service.')
    if type(proof.graph_record) is not str:raise Rejected('Exact graph record text required.')
    if type(expected_record) is not str or expected_record!=record or proof.graph_record!=record:raise Rejected('Different current graph record.')
    inc(work,'record_characters_compared',len(record)*2)
    n=len(graph.states);code=partition_vector(proof.blocks,n);transitions=[]
    for j,block in enumerate(proof.blocks):
        r=block[0];label=graph.label(r,proof.preserve_edges)
        successors=tuple(code[e.successors[r]] for e in graph.edits)
        for s in block:
            inc(work,'quotient_states_checked')
            if graph.label(s,proof.preserve_edges)!=label:raise Rejected('Merged current outputs or declared edge observations disagree.')
            for e,c in zip(graph.edits,successors):
                inc(work,'quotient_edges_checked')
                if code[e.successors[s]]!=c:raise Rejected('Partition does not commute with a named edit.')
        transitions.append(successors)
    needed={(s,t) for s,t in combinations(range(n),2) if code[s]!=code[t]}
    if type(proof.separations) is not tuple or len(proof.separations)!=len(needed):raise Rejected('Separation coverage incomplete.')
    for item in proof.separations:
        if type(item) is not tuple or len(item)!=3:raise Rejected('Malformed separation witness.')
        s,t,word=item;index(s,n);index(t,n)
        if (s,t) not in needed:raise Rejected('Duplicate or irrelevant separation pair.')
        needed.remove((s,t))
        if type(word) is not tuple or len(word)>n*n:raise Rejected('Distinguishing word size cap.')
        x,y=s,t
        for e in word:
            index(e,len(graph.edits));x=graph.edits[e].successors[x];y=graph.edits[e].successors[y]
            inc(work,'separation_transitions_checked',2)
        if graph.label(x,proof.preserve_edges)==graph.label(y,proof.preserve_edges):raise Rejected('Claimed word does not distinguish outputs.')
    # The number of producer rounds is documentary, not the basis of acceptance.
    if type(proof.strict_refinements) is not int or not 0<=proof.strict_refinements<n:raise Rejected('Malformed producer-round field.')
    return {'status':'EXACT_MINIMUM_OUTPUT_QUOTIENT','classes':len(proof.blocks),'encoder':code,
        'updates':tuple(transitions),'outputs':tuple(graph.outputs[b[0]] for b in proof.blocks),
        'preserves_edge_observation_menu':proof.preserve_edges,'self_contained_stationary_contract':True,
        'minimum_meaning':'number of codes for exact output continuations in this supplied finite graph',
        'graph_record':record}

@dataclass(frozen=True)
class DecisionSystem:
    graph:Graph
    actions:tuple[str,...]
    acceptable:tuple[tuple[str,...],...]

    def validate(self):
        if type(self.graph) is not Graph:raise Rejected('Graph type.')
        self.graph.validate()
        if type(self.actions) is not tuple or not 1<=len(self.actions)<=MAX_ACTIONS:raise Rejected('Action alphabet cap.')
        for a in self.actions:text(a)
        if len(set(self.actions))!=len(self.actions):raise Rejected('Duplicate action labels.')
        if type(self.acceptable) is not tuple or len(self.acceptable)!=len(self.graph.states):raise Rejected('One acceptability set per record.')
        for aa in self.acceptable:
            if type(aa) is not tuple or not aa or len(aa)!=len(set(aa)):raise Rejected('Nonempty distinct acceptable labels required; use an explicit failure service where appropriate.')
            if any(type(a) is not str or a not in self.actions for a in aa):raise Rejected('Unknown acceptable action.')

    def record(self):
        self.validate();return canonical({'graph_record':self.graph.record(),'actions':self.actions,'acceptable':self.acceptable})

@dataclass(frozen=True)
class CoverProof:
    system_record:str
    blocks:tuple[tuple[int,...],...]
    actions:tuple[str,...]
    successors:tuple[tuple[int,...],...]
    initial_codes:tuple[int,...]
    preserve_edges:bool=False

    def record(self):return {'system_record':self.system_record,'blocks':self.blocks,'actions':self.actions,
        'successors':self.successors,'initial_codes':self.initial_codes,'preserve_edges':self.preserve_edges}


def _common(system,block):
    allowed=set(system.actions)
    for s in block:allowed.intersection_update(system.acceptable[s])
    return tuple(a for a in system.actions if a in allowed)


def make_cover(system,blocks,preserve_edges=False):
    """Producer chooses deterministic ties; receiver checks every entry again."""
    system.validate();_flag(preserve_edges)
    n=len(system.graph.states);actions=[];updates=[]
    if type(blocks) is not tuple:raise Rejected('Immutable block list required.')
    for b in blocks:
        if type(b) is not tuple or not b or len(set(b))!=len(b):raise Rejected('Distinct nonempty block states required.')
        for s in b:index(s,n)
        aa=_common(system,b)
        if not aa:return None
        actions.append(aa[0]);targets=[]
        for e in system.graph.edits:
            if preserve_edges and len({e.observations[s] for s in b})!=1:return None
            image={e.successors[s] for s in b}
            choices=[j for j,c in enumerate(blocks) if image.issubset(c)]
            if not choices:return None
            targets.append(choices[0])
        updates.append(tuple(targets))
    initial=[]
    for s in range(n):
        choices=[j for j,b in enumerate(blocks) if s in b]
        if not choices:return None
        initial.append(choices[0])
    return CoverProof(system.record(),blocks,tuple(actions),tuple(updates),tuple(initial),preserve_edges)


def verify_cover(proof,system,expected_record,work=None,*,require_partition=False,preserve_edges=False):
    if type(proof) is not CoverProof or type(system) is not DecisionSystem:raise Rejected('Cover proof/system types.')
    system.validate();_flag(proof.preserve_edges);_flag(require_partition);_flag(preserve_edges);record=system.record()
    if proof.preserve_edges!=preserve_edges:raise Rejected('Different requested edge-observation service.')
    if type(proof.system_record) is not str:raise Rejected('Exact system record text required.')
    if type(expected_record) is not str or record!=expected_record or proof.system_record!=record:raise Rejected('Different current decision/edit contract.')
    inc(work,'record_characters_compared',len(record)*2)
    n=len(system.graph.states);blocks=proof.blocks
    if type(blocks) is not tuple:raise Rejected('Immutable cover blocks required.')
    k=len(blocks)
    if not 1<=k<=n:raise Rejected('Capped nonempty finite cover required.')
    seen=set()
    for b in blocks:
        if type(b) is not tuple or not b or len(set(b))!=len(b):raise Rejected('Distinct nonempty block states required.')
        for s in b:index(s,n)
        key=tuple(sorted(b))
        if key in seen:raise Rejected('Duplicate cover block.')
        seen.add(key)
    if require_partition:partition_vector(blocks,n)
    if set().union(*(set(b) for b in blocks))!=set(range(n)):raise Rejected('Cover omits states.')
    if type(proof.actions) is not tuple or len(proof.actions)!=k:raise Rejected('One readable output action per code.')
    if type(proof.successors) is not tuple or len(proof.successors)!=k:raise Rejected('One update row per code.')
    if type(proof.initial_codes) is not tuple or len(proof.initial_codes)!=n:raise Rejected('Initial encoder must cover every admitted state.')
    for s,c in enumerate(proof.initial_codes):
        index(c,k)
        if s not in blocks[c]:raise Rejected('Initial code does not contain the actual input record.')
        inc(work,'initial_memberships_checked')
    for j,b in enumerate(blocks):
        a=proof.actions[j]
        if type(a) is not str or a not in system.actions:raise Rejected('Unknown action output.')
        for s in b:
            inc(work,'acceptable_memberships_checked')
            if a not in system.acceptable[s]:raise Rejected('No common acceptable action in the supplied block.')
        nxt=proof.successors[j]
        if type(nxt) is not tuple or len(nxt)!=len(system.graph.edits):raise Rejected('Incomplete edit update row.')
        for e,c in zip(system.graph.edits,nxt):
            index(c,k)
            if proof.preserve_edges and len({e.observations[s] for s in b})!=1:raise Rejected('Declared edge observations are not retained.')
            for s in b:
                inc(work,'cover_edges_checked')
                if e.successors[s] not in blocks[c]:raise Rejected('An edited state escapes its next cover block.')
    return {'status':'ALL_EDIT_SEQUENCES_ACTION_CERTIFIED','codes':k,'partition_required':require_partition,
        'overlap_allowed':not require_partition,'preserves_edge_observations':proof.preserve_edges,
        'code_bits':(k-1).bit_length(),'minimum_claim':False,'graph_construction_cost_included':False,
        'meaning':'one admissible output from the readable code; no external history or hidden-state read',
        'system_record':record}


def minimum_cover(system,*,partition=False,preserve_edges=False,max_trials=MAX_SEARCH_TRIALS,work=None):
    """Finite exact enumeration when completed; otherwise a valid explicit upper bound.

    Search caps govern combinations tested, not CPU/RAM. Whole intersections,
    not pairwise compatibility, determine candidate blocks. No optimized BDD or
    SAT implementation is claimed. Returned minimality is an enumeration result,
    while verify_cover checks only the supplied machine's validity.
    """
    system.validate();_flag(partition);_flag(preserve_edges)
    n=len(system.graph.states)
    if n>MAX_SEARCH_STATES:raise Rejected('Minimum-cover search state cap; the verifier supports larger tables.')
    if type(max_trials) is not int or not 0<=max_trials<=MAX_SEARCH_TRIALS:raise Rejected('Trial cap must be an explicit bounded integer.')
    singleton=tuple((s,) for s in range(n));fallback=make_cover(system,singleton,preserve_edges)
    if fallback is None:raise Rejected('Internal singleton existence invariant failed.')
    candidates=[]
    for mask in range(1,1<<n):
        b=tuple(s for s in range(n) if mask>>s&1);inc(work,'candidate_subsets_tested')
        if _common(system,b):candidates.append((mask,b))
    tested=0;completed=[];full=(1<<n)-1
    for k in range(1,n+1):
        for choice in combinations(candidates,k):
            if tested==max_trials:
                return {'status':'SEARCH_BUDGET_EXHAUSTED','lower_bound':k,'upper_bound':n,
                    'completed_sizes':tuple(completed),'combinations_tested':tested,'proof':fallback}
            tested+=1;inc(work,'cover_combinations_tested');union=0;overlap=False
            for mask,b in choice:
                if union&mask:overlap=True
                union|=mask
            if union!=full or (partition and overlap):continue
            proof=make_cover(system,tuple(b for _,b in choice),preserve_edges)
            if proof is not None:
                return {'status':'EXACT_MINIMUM_BY_FINITE_ENUMERATION','lower_bound':k,'upper_bound':k,
                    'completed_sizes':tuple(completed),'combinations_tested':tested,'proof':proof}
        completed.append(k)
    raise Rejected('The complete search failed to find the valid singleton cover.')
