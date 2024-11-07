from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Annotation:
    name: str
    content: str = ''
    author: str = ''
    coords: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "content": self.content,
            "author": self.author,
            "coords": self.coords
        }
