"""Platform-invariant JSON artifact writing for future experiment versions.

The v1/v1.1 runners are frozen, source-hashed evidence and must not be edited
retroactively. New protocol versions should use this helper so their JSON
bytes are UTF-8 with LF newlines on every supported platform.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def write_json_lf(path: Path, value: Any, *, atomic: bool = True) -> None:
    """Write sorted, indented UTF-8 JSON with exactly LF line endings."""

    destination = Path(path)
    output = destination.with_name(destination.name + ".tmp") if atomic else destination
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, default=str)
        handle.write("\n")
    if atomic:
        os.replace(output, destination)
