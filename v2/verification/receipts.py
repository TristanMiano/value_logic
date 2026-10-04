"""Bounded JSON transport around the reviewed F06 codec and F07 receiver.

Receipt metadata is checked, not trusted as a consumer request. The current
source/query must be supplied separately. No pickle or executable payloads.
"""
from fractions import Fraction as Q
import json
from pathlib import Path
import re

from v2.checks import f06_inference_rules as K
from v2.checks import f06_derived_cases as C
from v2.checks import f07_soundness as A
from .model import Evidence, InputError, Query, exact
from . import native

MAX_BYTES = 262144
MAX_TERMS = 512
MAX_DEPTH = 48
MAX_OCCURRENCES = 20000
CODEC_LIMITS = C.Limits(nodes=128, term_occurrences=MAX_OCCURRENCES)
_RATIONAL = re.compile(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z', re.ASCII)


class ReceiptError(ValueError):
    """Malformed, stale or mismatched transport, never a semantic refutation."""


def _keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ReceiptError(f'Malformed {label} fields.')


def _rational(value, bits=2048):
    if (not isinstance(value, str) or len(value) > 1250
            or _RATIONAL.fullmatch(value) is None):
        raise ReceiptError('Rationals must be bounded integer or numerator/denominator strings.')
    result = Q(value)
    if max(abs(result.numerator).bit_length(), result.denominator.bit_length()) > bits:
        raise ReceiptError('Rational exceeds the declared bit limit.')
    return result


def _no_duplicate_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReceiptError('Duplicate JSON field.')
        result[key] = value
    return result


def _no_float(_):
    raise ReceiptError('JSON floating-point and nonfinite numbers are unsupported.')


def loads(text):
    if not isinstance(text, str) or len(text.encode('utf-8')) > MAX_BYTES:
        raise ReceiptError('JSON input exceeds the byte limit.')
    try:
        payload = json.loads(text, object_pairs_hook=_no_duplicate_fields,
                             parse_float=_no_float, parse_constant=_no_float)
    except (ValueError, RecursionError) as error:
        raise ReceiptError(f'Invalid bounded JSON: {error}') from error
    todo = [(payload, 0)]
    visited = 0
    while todo:
        value, depth = todo.pop()
        visited += 1
        if depth > MAX_DEPTH or visited > 20000:
            raise ReceiptError('JSON structure exceeds the traversal limit.')
        if isinstance(value, dict):
            todo.extend((v, depth + 1) for v in value.values())
        elif isinstance(value, list):
            todo.extend((v, depth + 1) for v in value)
        elif isinstance(value, str) and len(value) > 1250:
            raise ReceiptError('JSON string exceeds the transport limit.')
        elif isinstance(value, int) and value.bit_length() > 2048:
            raise ReceiptError('JSON integer exceeds the transport limit.')
    return payload


def read(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ReceiptError('File exceeds the transport byte limit.')
    try:
        return loads(raw.decode('utf-8'))
    except UnicodeDecodeError as error:
        raise ReceiptError('Transport must be UTF-8.') from error


def evidence_payload(evidence):
    evidence.validate()
    return dict(zip(('plus', 'minus', 'beta', 'gamma'),
                    (None if v is None else str(Q(v)) for v in evidence.bounds)),
                revision=evidence.revision)


def parse_evidence(value):
    _keys(value, ('plus', 'minus', 'beta', 'gamma', 'revision'), 'evidence')
    bounds = [None if value[k] is None else _rational(value[k], 256)
              for k in ('plus', 'minus', 'beta', 'gamma')]
    return Evidence(*bounds, revision=value['revision']).validate()


def request_payload(evidence, query):
    evidence.validate(); query.validate()
    return {'format': 'F11-request-v1', 'evidence': evidence_payload(evidence),
            'query': {'action': query.action, 'budget': str(exact(query.budget))}}


def parse_request(payload):
    _keys(payload, ('format', 'evidence', 'query'), 'request')
    if payload['format'] != 'F11-request-v1':
        raise ReceiptError('Unknown request format.')
    _keys(payload['query'], ('action', 'budget'), 'query')
    query = Query(payload['query']['action'], _rational(payload['query']['budget'], 256)).validate()
    return parse_evidence(payload['evidence']), query


def _preflight_proof(payload):
    _keys(payload, ('format', 'terms', 'steps', 'root'), 'proof')
    if not isinstance(payload['terms'], list) or len(payload['terms']) > MAX_TERMS:
        raise ReceiptError('Term table exceeds this receipt interface.')
    if not isinstance(payload['steps'], list) or len(payload['steps']) > 128:
        raise ReceiptError('Instruction table exceeds this receipt interface.')
    # The inherited codec bounds judgment-term occurrences after decoding.
    # Check the DAG first, and include instruction-data terms as well: a
    # shallow table with repeated children can encode exponential expansion.
    depths = []
    occurrences = []
    for term in payload['terms']:
        _keys(term, ('op', 'args', 'name', 'unit', 'value'), 'term')
        args = term['args']
        if not isinstance(args, list) or len(args) > 2:
            raise ReceiptError('Term has invalid or excessive arity.')
        if any(type(i) is not int or not 0 <= i < len(depths) for i in args):
            raise ReceiptError('Term references must be strictly backward.')
        depth = 1 + max((depths[i] for i in args), default=0)
        if depth > MAX_DEPTH:
            raise ReceiptError('Term DAG exceeds the depth limit.')
        depths.append(depth)
        expanded = 1 + sum(occurrences[i] for i in args)
        if expanded > MAX_OCCURRENCES:
            raise ReceiptError('Term DAG exceeds the expanded-occurrence limit.')
        occurrences.append(expanded)
        if term['value'] is not None:
            _rational(term['value'])
    if type(payload['root']) is not int or not 0 <= payload['root'] < len(payload['steps']):
        raise ReceiptError('Invalid proof root.')
    referenced_occurrences = 0
    def count_reference(index):
        nonlocal referenced_occurrences
        if type(index) is not int or not 0 <= index < len(occurrences):
            raise ReceiptError('Invalid instruction term reference.')
        referenced_occurrences += occurrences[index]
        if referenced_occurrences > MAX_OCCURRENCES:
            raise ReceiptError('Instruction terms exceed the expanded-occurrence limit.')
    for index, step in enumerate(payload['steps']):
        _keys(step, ('rule', 'parents', 'case', 'new', 'old', 'budget', 'context_id', 'data'), 'instruction')
        count_reference(step['new'])
        count_reference(step['old'])
        if step['case'] is not None and not isinstance(step['case'], str):
            raise ReceiptError('Invalid instruction case.')
        if not isinstance(step['parents'], list) or any(type(i) is not int or not 0 <= i < index for i in step['parents']):
            raise ReceiptError('Instruction parents must be strictly backward.')
        _rational(step['budget'])
        todo = [(step['data'], 0)]
        while todo:
            value, depth = todo.pop()
            if depth > MAX_DEPTH:
                raise ReceiptError('Instruction data exceeds the depth limit.')
            if isinstance(value, dict):
                if set(value) == {'rational'}:
                    _rational(value['rational'])
                elif set(value) == {'tuple'} and isinstance(value['tuple'], list):
                    todo.extend((x, depth + 1) for x in value['tuple'])
                elif set(value) == {'term'}:
                    count_reference(value['term'])
                else:
                    raise ReceiptError('Unknown instruction-data tag.')


def make_receipt(evidence, query, outcome):
    if outcome.proof is None or outcome.upper_bound is None:
        raise ReceiptError('Unavailable search produced no proof to save.')
    ctx = native.context(evidence)
    root = A.receive(ctx, outcome.proof, native.bound_request(ctx, query.action, outcome.upper_bound))
    if root.budget != outcome.upper_bound:
        raise ReceiptError('Advertised bound differs from the proof root.')
    return {'format': 'F11-receipt-v1', 'evidence': evidence_payload(evidence),
            'action': query.action, 'bound': str(outcome.upper_bound),
            'proof': C.pack_proof(outcome.proof)}


def _decode_payload(payload):
    """Decode and check the native trace; consumer binding remains a separate step."""
    # Normalize through the bounded wire parser even for in-process dictionaries.
    try:
        payload = loads(json.dumps(payload, separators=(',', ':'), allow_nan=False))
    except (TypeError, ValueError, RecursionError) as error:
        raise ReceiptError('Receipt is not bounded JSON data.') from error
    _keys(payload, ('format', 'evidence', 'action', 'bound', 'proof'), 'receipt')
    if payload['format'] != 'F11-receipt-v1':
        raise ReceiptError('Unknown receipt format.')
    origin = parse_evidence(payload['evidence'])
    advertised = _rational(payload['bound'])
    Query(payload['action']).validate()
    ctx = native.context(origin)
    _preflight_proof(payload['proof'])
    proof = C.unpack_proof(ctx, payload['proof'], CODEC_LIMITS)
    # unpack_proof has already checked this exact immutable proof and context.
    root = proof.steps[proof.root]
    if advertised != root.budget:
        raise ReceiptError('Receipt bound metadata differs from the checked root.')
    return origin, payload['action'], proof, root


def decode_receipt(payload):
    """Validate the archive against its own source; this does not accept a current request."""
    origin, action, proof, root = _decode_payload(payload)
    ctx = native.context(origin)
    A.receive(ctx, proof, native.bound_request(ctx, action, root.budget))
    return origin, action, proof


def receive_receipt(evidence, query, payload):
    """Accept only a proof of the independently supplied *current* request."""
    evidence.validate(); query.validate()
    origin, action, proof, _ = _decode_payload(payload)
    if origin != evidence:
        raise ReceiptError('Receipt source/version differs from the current source.')
    if action != query.action:
        raise ReceiptError('Receipt action differs from the current request.')
    ctx = native.context(evidence)
    return A.receive(ctx, proof, native.request(ctx, query))
