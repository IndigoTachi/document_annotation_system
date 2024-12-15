from PyQt6.QtCore import QAbstractTableModel, Qt
from model.database_model import DatabaseModel


class DocumentTableModel(QAbstractTableModel):
    def __init__(self, database_model: DatabaseModel):
        super().__init__()
        self.database_model = database_model

    def rowCount(self, parent=None):
        return self.database_model.rowCount()

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        document = self.database_model.documents[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return document.name
            elif index.column() == 1:
                return document.year
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section == 0:
                    return 'Tytuł'
                elif section == 1:
                    return 'Rok'
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        return None

    def refresh(self):
        self.beginResetModel()
        self.endResetModel()
