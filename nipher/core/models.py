from dataclasses import dataclass, field
from typing import Any

@dataclass
class Result:
    module: str
    target: str
    success: bool = True
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self):
        return {
            "module": self.module,
            "target": self.target,
            "success": self.success,
            "data": self.data,
            "error": self.error,
        }
