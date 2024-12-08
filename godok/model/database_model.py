from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal
from data.database import DocumentDatabase
from data.document import Document


document_database = DocumentDatabase()


class DatabaseModel(QAbstractListModel):
    dataChangedSignal = pyqtSignal()

    def __init__(self, documents=None):
        super().__init__()
        self.documents = documents or []

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            document = self.documents[index.row()]
            return document.name

    def rowCount(self, index=QModelIndex()):
        return len(self.documents)

    def add_document(self, document: Document):
        document_id = document_database.insert_document(document)
        document.document_id = document_id
        self.beginInsertRows(QModelIndex(), len(self.documents), len(self.documents))
        self.documents.append(document)
        self.endInsertRows()
        self.dataChangedSignal.emit()

    def update_document(self, index: QModelIndex, document: Document):
        document_database.update_document(document)
        self.documents[index.row()] = document
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
        self.dataChangedSignal.emit()

    def remove_document(self, index: QModelIndex):
        document = self.documents[index.row()]
        document_database.delete_document(document)
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        del self.documents[index.row()]
        self.endRemoveRows()
        self.dataChangedSignal.emit()

    def load_documents(self):
        self.beginResetModel()
        self.documents = document_database.load_documents()
        self.endResetModel()
        self.dataChangedSignal.emit()
