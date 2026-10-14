"""Added ordinary control: source-free invoice learning with syntax pruning."""
from pathlib import Path
import json
import sys
import invoice_bandit as ib
import invoice_syntax as sy
import check_invoice_syntax as checker

HERE=Path(__file__).resolve().parent


def prepare(data,meter):
    arena=sy.Arena();all_records={};groups={};bank={};certs={};ranges={};duplicates={}
    for r in ib.mk.MENU:
        proposal=ib.mk.plan(data['audit_costs'],r);meter.pay('preparation','same_ordinary_policy_proposals',proposal['invoice']['total'])
        edge,tables=sy.compile_policy(arena,data['audit_costs'],proposal['roots'])
        checked=checker.check(arena.nodes,data['audit_costs'],proposal['roots'],tables,edge)
        meter.pay('preparation','independent_syntax_recurrence_check',checked['total'])
        all_records[r]=dict(roots=proposal['roots'],edge=edge,tables=tables,checking=checked)
        if edge in groups:duplicates[r]=groups[edge]
        else:groups[edge]=r;bank[r]=proposal['roots']
        meter.pay('preparation','checked_invoice_equivalence_lookup',4)
    meter.pay('preparation','shared_syntax_compilation',arena.meter.total)
    for r,roots in bank.items():
        cert=ib.ic.produce(data['audit_costs'],roots,{});checked=ib.ic.check(data['audit_costs'],roots,{},cert)
        meter.pay('preparation','retained_policy_global_invoice_range',cert['invoice']['total'])
        meter.pay('preparation','retained_policy_range_check',checked['total'])
        certs[r]=dict(proof=cert,checking=checked);ranges[r]=(cert['lower'],cert['upper'])
    return bank,ranges,dict(roots=bank,ranges=ranges,certificates=certs,duplicates=duplicates,
        syntax=dict(nodes=arena.nodes,policies=all_records))


if __name__=='__main__':
    directory=Path(sys.argv[1]);name=sys.argv[2];directory.mkdir(exist_ok=False)
    case=next(c for c in json.loads((HERE/'cs01/design.json').read_text())['cases'] if c['name']==name)
    ib.prepare=prepare;ib.VERSION='s08-pruned-invoice-bandit-v1'
    rows=ib.ms.draw(len(case['costs']),case['r'],1024,case['seed'])
    ib.g01.save(directory/'result.json',ib.run_arm(directory,case,rows))
