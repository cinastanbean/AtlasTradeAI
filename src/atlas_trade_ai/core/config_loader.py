from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonConfigLoader:
    def __init__(self, base_dir: str | Path = "config") -> None:
        self.base_dir = Path(base_dir)

    def load(self, filename: str) -> dict[str, Any]:
        path = self.base_dir / filename
        return json.loads(path.read_text(encoding="utf-8"))
