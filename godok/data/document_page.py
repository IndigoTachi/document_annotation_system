from dataclasses import dataclass, field
from typing import List, Dict
from annotation import Annotation
import json


@dataclass
class DocumentPage:
    number: int = None
    path: str
    annotations: List[Annotation] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "number": self.number,
            "path": self.path,
            "annotations": [annotation.to_dict() for annotation in self.annotations]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def insert_annotation(self, annotation):
        self.annotations.append(annotation)
