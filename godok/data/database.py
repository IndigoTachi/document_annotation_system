import sqlite3
from data.document import Document
import json


class DocumentDatabase:
    def __init__(self, db_name='documents.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    year INT,
                    pages TEXT
                )
                '''
            )

    def insert_document(self, document: Document) -> int:
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO documents (title, year, pages) VALUES (?, ?, ?)',
                (document.name, document.year, document.to_json_pages(),)
            )
            return cursor.lastrowid

    def update_document(self, document: Document):
        with self.conn:
            self.conn.execute(
                'UPDATE documents SET title = ?, year = ?, pages = ? WHERE id = ?',
                (document.name, document.year, document.to_json_pages(), document.document_id,)
            )

    def delete_document(self, document: Document):
        with self.conn:
            self.conn.execute('DELETE FROM documents WHERE id = ?', (document.document_id,))

    def load_documents(self) -> list:
        cursor = self.conn.execute('SELECT id, title, year, pages FROM documents')
        rows = cursor.fetchall()
        documents = []
        for row in rows:
            doc_data = {
                'name': row[1],
                'year': row[2],
                'pages': json.loads(row[3]),
                'document_id': row[0]
            }
            document = Document.from_dict(doc_data)
            documents.append(document)
        return documents
