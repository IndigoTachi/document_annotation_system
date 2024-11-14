from dataclasses import dataclass, field
from typing import List, Dict
from data.annotation import Annotation
from data.document_page import DocumentPage
import json


@dataclass
class Document:
    name: str
    document_id: int = None
    year: int = None
    pages: List[Annotation] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'year': self.year,
            'pages': [page.to_dict() for page in self.pages],
            'document_id': self.document_id
        }

    def to_json_pages(self) -> str:
        return json.dumps(self.to_dict()['pages'], indent=4)

    @staticmethod
    def from_dict(data: Dict) -> 'Document':
        document = Document(name=data['name'], year=data['year'], document_id=data['document_id'])
        document.pages = [
            DocumentPage(
                number=page_data['number'],
                path=page_data['path'],
                annotations=[
                    Annotation(**annotation_data)
                    for annotation_data in page_data['annotations']
                ]
            )
            for page_data in data['pages']
        ]
        return document

    def insert_page(self, page):
        page.number = len(self.pages) + 1
        self.pages.append(page)
