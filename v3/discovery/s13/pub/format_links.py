"""Join split Markdown link syntax in new unbound narrative notes only."""
from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
for path in root.glob('*.md'):
    old=path.read_bytes()
    new=re.sub(rb'(\[[^\]\r\n]+\])\r?\n(\([^\)\r\n]+\))',rb'\1\2',old)
    if new!=old:
        path.write_bytes(new)
        print(path.name)
