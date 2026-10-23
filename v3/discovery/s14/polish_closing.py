"""Administrative spacing in newly written closing prose; no scientific edits."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
replacements={
 'October23,2026':'October 23, 2026', 'October23.':'October 23.',
 'approximately75%':'approximately 75%', 'development,20%':'development, 20%',
 'and5%':'and 5%', 'The35':'The 35', "s14's45":"s14's 45", 'not45':'not 45',
 's14:14,':'s14: 14,', 'Program:109,':'Program: 109,', 'Phase:174,':'Phase: 174,',
 ',000ns':',000 ns', ',147ns':',147 ns', ',996ns':',996 ns',
 '=240.':'= 240.', '=1818.':'= 1818.', '=2904.':'= 2904.',
 'checks142':'checks 142', 'ended02:':'ended 02:', 'runtime02:':'runtime 02:',
 'every15':'every 15', 'synthesis82.':'synthesis 82.', 'X/R88.':'X/R 88.',
 'about30.':'about 30.', 'the16-hour':'the 16-hour', 'next40/100':'next 40/100',
 'value<0.24':'value < 0.24', 'permits0.256':'permits 0.256',
 'admits0.256':'admits 0.256', 'value>0.045':'value > 0.045',
 'budget1→5':'budget 1→5', 'upper17.':'upper 17.', 'with980':'with 980',
 'has12.5%':'has 12.5%', 'least6.0834%':'least 6.0834%', 'reset100':'reset 100',
 'historical55':'historical 55', 'central65%':'central 65%', 'central30%':'central 30%',
 "v1's55":"v1's 55", "V1's20":"V1's 20", "F01's20":"F01's 20",
 'new80%':'new 80%', 'all24':'all 24', "s10's57.12%":"s10's 57.12%",
 'and9.53%':'and 9.53%', 'age4':'age 4', 'adds240.':'adds 240.',
 'Program1818.':'Program 1818.', 'phase2904.':'phase 2904.',
 'after240.':'after 240.', 'ended2026-':'ended 2026-', 'at02:':'at 02:',
 'minutes:163.':'minutes: 163.', '/41.':'/ 41.', '/34.':'/ 34.',
 'is0.862':'is 0.862', 'synthesis:82.':'synthesis: 82.', 'X/R:88.':'X/R: 88.',
 'is40 program':'is 40 program', 'upper20→1':'upper 20→1',
 'at12.5%':'at 12.5%', 'radius0.001':'radius 0.001',
 'width972507':'width 972507', 'about49.68%':'about 49.68%',
 'uses23':'uses 23', 'than30':'than 30', 'cap7 rather than8':'cap 7 rather than 8',
 'records45':'records 45',
}
files=['v3/discovery/CONTINUE.md','v3/discovery/s14/checkpoint.md',
       'v3/discovery/s14/findings.md']
for name in files:
    p=ROOT/name;s=p.read_bytes().decode('utf-8')
    for old,new in replacements.items():s=s.replace(old,new)
    p.write_bytes(s.encode('utf-8'))
for name,marker in [('v3/README.md','## Research direction'),
                    ('TODO_v3.md','Established October 6, 2026 UTC.')]:
    p=ROOT/name;s=p.read_bytes().decode('utf-8');head,tail=s.split(marker,1)
    for old,new in replacements.items():head=head.replace(old,new)
    p.write_bytes((head+marker+tail).encode('utf-8'))
print('Closing prose spacing updated; scientific evidence unchanged.')
