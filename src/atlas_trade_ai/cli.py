from __future__ import annotations

import json
from pathlib import Path

from .agent import FollowUpAgent
from .models import AgentContext


def main() -> None:
    sample_path = Path("examples/followup_event.json")
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    context = AgentContext.from_dict(payload)
    result = FollowUpAgent().run(context)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
