from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from data.database import DocumentDatabase
from data.document import Document


document_database = DocumentDatabase()


class DatabaseModel(QAbstractListModel):
    def __init__(self, documents=None):
        super().__init__()
        self.documents = documents or []

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            document = self.documents[index.row()]
            return document.title

    def rowCount(self, index=QModelIndex()):
        return len(self.documents)

    def add_document(self, document: Document):
        document_id = document_database.insert_document(document)
        document.document_id = document_id
        self.beginInsertRows(QModelIndex(), len(self.documents), len(self.documents))
        self.documents.append(document)
        self.endInsertRows()

    def update_document(self, index: QModelIndex, document: Document):
        document_database.update_document(document)
        self.documents[index.row()] = document
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])

    def remove_document(self, index: QModelIndex):
        document = self.documents[index.row()]
        document_database.delete_document(document.document_id)
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        del self.documents[index.row()]
        self.endRemoveRows()

    def load_documents(self):
        self.beginResetModel()
        self.documents = document_database.load_documents()
        self.endResetModel()
