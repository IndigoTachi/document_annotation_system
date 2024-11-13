from dataclasses import dataclass, field
from typing import List
from annotation import Annotation


@dataclass
class Document:
    name: str
    year: int = None
    pages: List[Annotation] = field(default_factory=list)

    def export(self) -> List:
        return [self.name, self.year, self.pages.to_json()]

    def insert_page(self, page):
        page.number = len(self.pages) + 1
        self.pages.append(page)
