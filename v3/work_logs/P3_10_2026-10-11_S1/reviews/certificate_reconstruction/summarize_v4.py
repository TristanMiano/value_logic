#!/usr/bin/env python3
"""Summarize only the sealed independent observer JSON; no official execution."""
from pathlib import Path
from fractions import Fraction
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json

BASE = Path(__file__).resolve().parent
OUT = BASE / 'final_review_v1'
OUT.mkdir(exist_ok=False)
source = BASE / 'final_observation_v4/results.json'
raw = source.read_bytes()
r = json.loads(raw)
b = r['B2']
assert r['status'] == 'PASS' and not r['frozen_analysis_mismatches']
now = datetime.now(timezone.utc).isoformat()
SIGNER = 'ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction'

def pair(a, b):
    value = Fraction(a, b)
    return [value.numerator, value.denominator]

def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(str(v) for v in row) + ' |' for row in rows])

def short(scope):
    return scope.removeprefix('certificates-').removeprefix('family:')

history = b['per_history']
by_history = {(h['unit']['group_id'], h['unit']['recipient'], h['unit']['budget_condition'], h['unit']['method']): h for h in history}
by_summary = {(h['scope'], h['recipient'], h['budget_condition'], h['method']): h for h in b['complete_histories']}
methods = ['P-REUSE', 'P-FRESH', 'O-ADD-COLD', 'O-ADD-WARM', 'O-ENUM-RECEIVER', 'O-ADD-PORTFOLIO', 'O-ADD-WARM-PRUNED']
families = sorted({h['scope'] for h in b['complete_histories'] if h['scope'].startswith('family:')})
full_comparisons = []
for scope in families:
    for recipient in ('fresh', 'resident'):
        p, o, fresh = (by_summary[(scope,recipient,'full',method)] for method in ('P-REUSE','O-ENUM-RECEIVER','P-FRESH'))
        full_comparisons.append({'scope':scope,'recipient':recipient,'history_count':2,'attempt_count':8,
            'reuse_units':p['total_units'],'ordinary_direct_units':o['total_units'],'fresh_rebuild_units':fresh['total_units'],
            'reuse_to_direct_ratio':pair(p['total_units'],o['total_units']),
            'reuse_to_fresh_ratio':pair(p['total_units'],fresh['total_units']),
            'same_full_coverage':p['delivered_request_ids']==o['delivered_request_ids']==fresh['delivered_request_ids']})
operational = []
for budget in ('full','capped'):
    for recipient in ('fresh','resident'):
        for method in ('P-REUSE','O-ENUM-RECEIVER'):
            hs=[h for h in history if h['unit']['budget_condition']==budget and h['unit']['recipient']==recipient and h['unit']['method']==method]
            operational.append({'budget':budget,'recipient':recipient,'method':method,'histories':len(hs),
                'attempts':4*len(hs),'delivered':sum(len(h['delivered_request_ids']) for h in hs),
                'complete_histories':sum(h['full_service_delivered'] for h in hs),'total_units':sum(h['total_units'] for h in hs)})
failures=[a for a in b['all_attempts'] if a['status']!='DELIVERED']
fail_groups=defaultdict(list)
for a in failures: fail_groups[(a['method'],a['failure']['type'],a['failure']['stage'])].append(a)
failure_table=[]
for (method,error,stage),values in sorted(fail_groups.items()):
    failure_table.append({'method':method,'error_type':error,'stage':stage,'fresh_count':sum(x['recipient']=='fresh' for x in values),
        'resident_count':sum(x['recipient']=='resident' for x in values),'attempts':len(values),
        'paid_failed_attempt_units':sum(x['total_units'] for x in values)})
cap_differences=[x for x in b['actual_cap_history_comparisons'] if not x['retrospective_equals_actual_ids']]
primitive_full=[x for x in b['primitive_price_diagnostics_exploratory'] if x['budget_condition']=='full']
primitive_cap=[x for x in b['primitive_price_diagnostics_exploratory'] if x['budget_condition']=='capped']
source_charges=Counter(a['source_enrollment_units_this_attempt'] for a in b['all_attempts'])
summary={'schema':'p310.independent_certificate_interpretation.v1','signed_by':SIGNER,'signed_utc':now,
    'status':'PASS_WITH_SCOPED_NEGATIVE_ECONOMIC_RESULT','source_observer_results_sha256':hashlib.sha256(raw).hexdigest(),
    'observer_source_sha256':hashlib.sha256((BASE/'observer_v4.py').read_bytes()).hexdigest(),
    'counts':{'histories':104,'requests':416,'full_histories':52,'capped_histories':52,'delivered':356,'unavailable':60,
        'complete_histories':70,'complete_full_histories':sum(h['full_service_delivered'] for h in history if h['unit']['budget_condition']=='full'),
        'complete_capped_histories':sum(h['full_service_delivered'] for h in history if h['unit']['budget_condition']=='capped'),
        'full_deliveries':sum(len(h['delivered_request_ids']) for h in history if h['unit']['budget_condition']=='full'),
        'capped_deliveries':sum(len(h['delivered_request_ids']) for h in history if h['unit']['budget_condition']=='capped')},
    'certificate_bill_units':b['known_all_attempt_units_descriptive_arm_sum'],'failed_attempt_bill_units':b['failed_attempt_units'],
    'nonbudget_certificate_errors':0,'failure_stages':dict(Counter(a['failure']['stage'] for a in failures)),
    'source_enrollment':{'one_installation_units':561239,'charge_distribution':dict(sorted(source_charges.items())),
        'all_failed_attempts_follow_completed_source_enrollment':all(a['source_enrollment_confirmed_after'] for a in failures),
        'all_post_failure_sizes_consistent_with_evicted_scientific_state':all(a['post_failure_evicted_producer_record_size_consistent'] for a in failures),
        'subsequent_to_failure_statuses':dict(Counter(a['status'] for a in b['all_attempts'] if a['follows_failed_attempt']))},
    'full_family_comparisons':full_comparisons,'four_stream_operational_totals_descriptive':operational,
    'all_failure_method_type_stage_counts_and_fees':failure_table,'capped_history_retrospective_mismatches':cap_differences,
    'full_direct_ordinary_componentwise_primitive_no_greater':{'verified_cells':len(primitive_full),
        'group_cells':sum(not x['scope'].startswith('family:') for x in primitive_full),
        'family_cells':sum(x['scope'].startswith('family:') for x in primitive_full),
        'all':all(x['ordinary_direct_cheaper_under_all_nonnegative_primitive_prices'] for x in primitive_full),
        'interpretation':'No greater, not strictly lower when all differing coordinates have zero price; fixed records only'},
    'capped_direct_universal_price_claim':all(x['ordinary_direct_cheaper_under_all_nonnegative_primitive_prices'] for x in primitive_cap),
    'global_end_to_end_positive_cost_claim_permitted':False,'original_unknown_public_prefix':r['unknown_unsealed_public_attempts'],
    'original_failure_classification':'AttributeError deterministic conformance bootstrap defect; separate from all60 typed certificate budget denials',
    'observer_failures_this_final_run':0,'principal_clock_credit_ns':0}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')

lines=[]
lines += ['# Independent P3-10 certificate reconstruction and interpretation', '',
          '**Disposition: PASS for numerical reconstruction; valid finite certificate service, with no advantage over the strongest completed ordinary service on this tariff.**', '',
          f'Signed: {SIGNER}  ',f'UTC: {now}  ',
          'Role: independent implementation, same model, source-aware review; not a blind replication. Concurrent review adds zero principal Research90 credit.', '',
          '## Provenance and validation', '',
          'The preserved `observer_v4.py` ran once after the principal\'s explicit release and returned PASS with no observer failure and no disagreement with the frozen analysis. It imported no project module and did not call a generator, paid method, private scorer or frozen analyzer. It read sealed JSON, evaluated exact expression tables with `Fraction`, and reconstructed every invoice and comparison from raw rows. The 17 preexisting mathematical/invoice/comparison helpers are unchanged from observer_v3; the preserved v4 revision only added explicit A1 lineage validation.', '',
          'All 50 original live/frozen source pairs match the original manifest. All 1,365 original evidence files match the sealed amendment inventory. The 12 original input seals, 440 unchanged original public seals and 60 amended conformance seals form the exact ordered 500-unit composite. All 500 evaluation records bind the matching input/public result bytes, and all evaluations precede the unchanged analysis. The original public completion remains absent and its original unsealed `AttributeError` prefix remains present. A1 manifest SHA is `36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359`.', '',
          'The result JSON preserves all 104 certificate histories, 416 attempts, 3,680 packet hash checks, 156 frozen group/family summaries, 864 directed comparisons, 352 descriptive prefix comparisons, 52 actual-cap comparisons and 24 primitive-price diagnostic cells. These summary/comparison counts are overlapping views of four deterministic streams, not independent samples.', '',
          'Evidence: [observer results](../final_observation_v4/results.json), [source/output hashes](../final_observation_v4/source_hashes.json), [run receipt](../final_observation_v4/run_receipt.json), [explicit release](../completion_release_A1.json), and [machine-readable interpretation](summary.json).', '',
          '## B0 and B1: what was certified', '',
          '**356 of 416 attempts delivered current warrants; all 356 are valid under independent exact scalar reconstruction.** The other 60 are explicit unavailable replies. No delivered warrant has a false bound, stale/current identity confusion, wrong source/request scope or missing required sublevel coverage. All 104 private history scores pass validity; this is distinct from full-service completion, which holds for 70 histories.', '',
          'Both structural families reduce pointwise to D = 2z − 1 on the entire Boolean cube. The last edit adds 1/2, giving D = 2z − 1/2. The independent tables check the identity at every assignment rather than assuming it from the source. The following counts apply to both families; entries are n=4 / n=7.', '',
          table(['Slot','Hard-feasible','Current sublevel','Minimizers','Incumbent rank','Exact current D range','Bound'],[
              ['1: initial','16 / 128','16 / 128','16 / 128','0','[-1, 1]','1'],
              ['2: hard/rank edit','12 / 96','6 / 48','6 / 48','0','[-1, 1]','1'],
              ['3: nonoptimal incumbent','12 / 96','12 / 96','6 / 48','1','[-1, 1]','1'],
              ['4: weight/loss edit','12 / 96','6 / 48','6 / 48','0','[-1/2, 3/2]','3/2']]), '',
          'The two old domains are disjoint halves of the cube, of size 8 / 64 each, with exact bounds −1 and +1. All old receipts are stale for the edited current requests. The nonoptimal third-slot incumbent correctly expands the certified sublevel to include 6 / 48 nonminimal assignments; all minimizers remain included. z is unrestricted by the rank edits, so both extrema are attained. These are positive upper bounds, not proofs that an action improves, that every incumbent is optimal, or that a positive bound implies an improved action. The workload tests paid transport and current coverage on a fixed finite task.', '',
          '## B2: full histories and the direct ordinary comparator', '',
          'All 52 full-budget histories deliver all four requests (208/208 attempts). The fresh-recipient roster has seven methods and the resident roster six; the pruned warm ADD method is deliberately ineligible for resident service, not a missing run. Within every one of the eight full group/recipient cells, O-ENUM-RECEIVER is the unique cheapest complete ordinary method. It is also the unique minimum in all four corresponding family/recipient aggregates.', '',
          'The next table sums the two sizes within each family: two histories and eight covered requests per method. Ratios are P-REUSE divided by direct enumeration. Exact integer totals are in the declared certificate tariff.', '',
          table(['Family','Recipient','P-REUSE units','Direct ordinary units','Ratio','Fresh rebuild units'],[
              [short(x['scope']),x['recipient'],f"{x['reuse_units']:,}",f"{x['ordinary_direct_units']:,}",
               f"{float(Fraction(*x['reuse_to_direct_ratio'])):.6f}",f"{x['fresh_rebuild_units']:,}"] for x in full_comparisons]), '',
          'Across the eight individual group/recipient histories, P-REUSE costs 2.356317–3.864761 times direct enumeration at identical full coverage. Resident delivery reduces reuse cost compared with fresh recipients, but does not erase the ordinary advantage. P-REUSE does show a completed-path 5% saving against P-FRESH for the n=7 streams (both recipients), and against O-ADD-PORTFOLIO for the n=4 streams; these narrower comparisons do not establish advantage over the cheapest ordinary service. For example, the majority fresh family aggregate costs 15,294,823 for reuse versus 16,081,726 for the portfolio: its ratio exceeds 0.95, so even that seemingly favorable aggregate misses the frozen 5% threshold.', '',
          '**The full-service direct advantage survives every nonnegative repricing of the recorded primitive counts.** Direct enumeration has no larger count in any primitive category in all eight full group/recipient cells and the four family aggregates. At prices that assign zero to all differing coordinates there can be a tie, so this is “no more expensive,” not strict saving at every price. The statement holds the executed paths fixed; it does not claim that services would take identical paths under newly funded price-dependent policies.', '',
          '## Actual caps, fees and coverage', '',
          'The consumer cap is 1,048,576 units per attempt, alongside the common 134,217,728 total per-attempt budget. All 60 unavailable replies occur among the 52 capped histories. Those capped histories deliver 148/208 requests and achieve full service in 18/52 histories. The full-budget arm has no unavailable requests.', '',
          table(['Budget','Recipient','Method','Delivered /16','Complete histories /4','All-attempt units'],[
              [x['budget'],x['recipient'],x['method'],f"{x['delivered']}/16",f"{x['complete_histories']}/4",f"{x['total_units']:,}"] for x in operational]), '',
          'In every n=4 capped P-REUSE history, request 1 is unavailable and requests 2–4 are delivered. In every n=7 capped P-REUSE history, all four requests are unavailable. Direct enumeration delivers all four n=4 requests and requests 2–4 at n=7. Thus the candidate\'s actual capped coverage is strictly smaller in each group/recipient cell, in addition to its higher completed-path bill. Even an arbitrary accounting adjustment cannot repair that sealed coverage deficit. This is stronger than a primary economic flag being false merely because the outer cost gate is unavailable.', '',
          'Every failed certificate attempt is typed `ResourceExhausted`. There are no unexpected deterministic or semantic certificate exceptions hidden by the broad delivery catch. The complete failure census is:', '',
          table(['Method','Failure stage','Fresh','Resident','Total failures','All paid failed-attempt units'],[
              [x['method'],x['stage'],x['fresh_count'],x['resident_count'],x['attempts'],f"{x['paid_failed_attempt_units']:,}"] for x in failure_table]), '',
          f"The failure fees sum to **{b['failed_attempt_units']:,} units**, retained in the certificate arm's complete known all-attempt total of **{b['known_all_attempt_units_descriptive_arm_sum']:,} units**. These totals are operational accounting over the fixed executed roster, not an exchange into another arm's tariff or an independent statistical estimate.", '',
          'Every history pays source enrollment of 561,239 once: 104 such charges, then 312 zero source charges. All 60 failed attempts occur after source installation is complete; failure does not uninstall that program. The source-defined failure transition withdraws the current receipt and clears scientific producer/receiver caches. Observed retained sizes agree with the independently serialized evicted producer record, and receiver retained bytes are zero. This checks size consistency with the source-defined transition; the public record does not reveal an entire retained producer-state body for separate content inspection.', '',
          'There are 52 attempts following a failed attempt within the scheduled histories: 28 later deliver and 24 fail again. The effect of retained scientific state is clearest in four resident n=7 histories. Full traces show requests 2–4 under the cap, but the separately executed capped histories never acquired the required successful bootstrap and deliver none. Retrospectively thresholding full traces would invent 12 delivered request positions across these four histories. The exact counterexamples are:', '',
          table(['Family/size','Method','Full-trace threshold predicts','Actual capped IDs','Actual capped all-attempt units'],[
              [short(x['group_id']),x['method'],'2, 3, 4','none',f"{x['actual_capped_total_units']:,}"] for x in cap_differences]), '',
          'These are the only four coverage-set disagreements among all 52 full-versus-actual-cap pairs. The actual capped history is authoritative. At capped coverage, direct enumeration also incurs more publication/receipt-output units in some cells because it delivers more answers, so the full-service componentwise-price conclusion must not be transplanted to capped vectors.', '',
          '## Outer failure, economic scope and review conclusion', '',
          'The certificate denials are ordinary budget outcomes with complete internal invoices. They are separate from the original structural conformance `AttributeError` that escaped without an invoice. A1 preserves that old failed prefix and all 1,365 original files while completing the missing conformance stage under an amended identity. The 440 unchanged broker/certificate public records retain their original prospective finite-cohort acquisition status; conformance and overall execution are explicitly amended.', '',
          '**The global positive end-to-end economic gate remains false.** Every frozen certificate practical-dominance flag is therefore suppressed, while raw completed-path ratios, weak/componentwise flags and separately labeled threshold results remain descriptive. An unknown gate alone is not evidence of inferiority. Here the separate recorded evidence does establish that P-REUSE has neither a lower full-service primitive vector than direct enumeration nor sufficient actual capped coverage to dominate it.', '',
          'The source-only cost review is now corroborated as to the original failure identity. Its lost structural meter counter can be bounded conservatively by 85,976 to 49,900,000 conditional on faithful execution of the reported source path; the exact invoice and primitive breakdown are still unknown. There is no declared exchange rate from those structural units into the certificate tariff. For a hypothetical genuinely common nonnegative same-tariff overhead u, the 5% test is C+u <= (19/20)(O+u), equivalent to u <= 19O−20C. Failure of that threshold cannot become success under common overhead; cost differences and componentwise orders also stay unchanged. These algebraic observations do not relax the frozen gate. See [cost uncertainty source review](../cost_uncertainty_source_review_v1/review.md).', '',
          'This review establishes exact finite service validity, coverage, paid failure behavior and adverse comparison against a strong fixed ordinary service. It makes no IID, population-generalization, asymptotic, physical-efficiency, improved-action or P3-11 novelty claim. All relevant zeros, unavailable services, old scopes, nonoptimal sublevel members, full/fresh/resident/capped distinctions, ordinary comparisons and failed fees remain in the sealed independent JSON.', '',
          '## Audit anchors', '',
          f"- Observer source SHA-256: `{summary['observer_source_sha256']}`.",
          f"- Independent result SHA-256: `{summary['source_observer_results_sha256']}`.",
          '- Independent run: 2026-10-11T15:37:43.868665+00:00 to 15:37:47.196488+00:00; exit 0; zero principal credit.',
          '- Existing observer versions v1–v3, preparation records, source reviews and draft/final amendment source snapshots remain preserved.',
          '- `summary.json` contains exact rational comparison values and every failure method/type/stage fee total; `results.json` contains every underlying history and attempt.', '',
          '## Appendix: all 104 history bills and delivered request slots', '',
          'Each row is one original sealed four-attempt history. “None” is explicit unavailable service, not a dropped case.', '',
          table(['Stream','Recipient','Budget','Method','Delivered slots','Total units'],[
              [short(h['unit']['group_id']),h['unit']['recipient'],h['unit']['budget_condition'],h['unit']['method'],
               ', '.join(x.rsplit('.',1)[-1][1:] for x in h['delivered_request_ids']) or 'None',f"{h['total_units']:,}"] for h in history]), '']
(OUT/'review.md').write_text('\n'.join(lines))
outputs=[]
for name in ('summary.json','review.md'):
    data=(OUT/name).read_bytes();outputs.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(OUT/'signature.json').write_text(json.dumps({'schema':'p310.signed_independent_certificate_review.v1','signed_by':SIGNER,
    'signed_utc':now,'source_observer_result':{'path':str(source),'sha256':hashlib.sha256(raw).hexdigest()},
    'summary_script':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    'outputs':outputs,'principal_clock_credit_ns':0,'paid_method_generator_private_scorer_frozen_analysis_calls':0},indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'SIGNED_REVIEW_SAVED','output_dir':str(OUT),'outputs':outputs},indent=2))
