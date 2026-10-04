"""Run F11's deterministic producer/reference experiment."""
import argparse
import json
from pathlib import Path
import sys

from .experiment import assess_with_proof, core_report
from .producer import Limits
from .model import InputError
from . import receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='Also save the full deterministic report.')
    parser.add_argument('--request', type=Path, help='Run one separately supplied F11-request-v1 JSON file.')
    parser.add_argument('--receipt-out', type=Path, help='Save the generated bound receipt for one request.')
    parser.add_argument('--check-receipt', type=Path, help='Check a saved receipt against --request.')
    parser.add_argument('--max-bases', type=int, default=440, help='Bound template search (0..440).')
    parser.add_argument('--max-steps', type=int, default=128, help='Bound emitted proof size (0..128).')
    args = parser.parse_args()
    if (args.receipt_out or args.check_receipt) and not args.request:
        parser.error('Receipt operations require a separately supplied --request.')
    if args.receipt_out and args.check_receipt:
        parser.error('Choose receipt generation or checking.')
    if args.check_receipt and (args.max_bases != 440 or args.max_steps != 128):
        parser.error('Search limits apply to generation, not receipt checking.')
    if not args.request and (args.max_bases != 440 or args.max_steps != 128):
        parser.error('Custom search limits apply to a single --request.')
    try:
        if args.request:
            evidence, query = receipts.parse_request(receipts.read(args.request))
            if args.check_receipt:
                root = receipts.receive_receipt(evidence, query, receipts.read(args.check_receipt))
                report = {'status': 'ACCEPTED', 'action': query.action,
                          'bound': str(root.budget), 'requested_budget': str(query.budget),
                          'current_revision': evidence.revision, 'context_id': root.context_id}
            else:
                limits = Limits(args.max_bases, args.max_steps)
                report, outcome = assess_with_proof(evidence, query, limits)
                if args.receipt_out:
                    if outcome.proof is None:
                        report['receipt_saved'] = False
                    else:
                        encoded_receipt = json.dumps(receipts.make_receipt(evidence, query, outcome),
                                                     indent=2, sort_keys=True) + '\n'
                        args.receipt_out.write_text(encoded_receipt, encoding='utf-8')
                        report['receipt_saved'] = True
        else:
            report = core_report()
    except (ValueError, OSError) as error:
        # A rejected external receipt is an input outcome. A native checker
        # failure in our own generator is an implementation error and must not
        # be disguised as a user's bad request or a semantic refutation.
        if not args.check_receipt and not isinstance(error, (InputError, receipts.ReceiptError, OSError)):
            raise
        print(json.dumps({'status': 'REJECTED_INPUT_OR_RECEIPT', 'reason': str(error)}), file=sys.stderr)
        return 2
    encoded = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.json:
        args.json.write_text(encoded, encoding='utf-8')
    summary = {key: value for key, value in report.items() if key != 'cases'}
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
