from dataclasses import dataclass, field, asdict
from typing import List, Dict
import json


@dataclass
class Annotation:
    name: str
    content: str = ''
    author: str = ''
    coords: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)
