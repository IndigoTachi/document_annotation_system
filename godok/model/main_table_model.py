from PyQt6.QtCore import QAbstractTableModel, Qt


class DocumentTableModel(QAbstractTableModel):
    def __init__(self, documents):
        super().__init__()
        self.documents = documents

    def rowCount(self, parent=None):
        return len(self.documents)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        document = self.documents[index.row()]
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
