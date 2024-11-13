from PyQt6.QtWidgets import QMainWindow, QHeaderView
from view.main_view_ui import Ui_MainWindow
from model.main_table_model import DocumentTableModel


class MainView(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = model
        self.model.load_documents()
        documents = self.model.documents
        self.tableModel = DocumentTableModel(documents)
        self.ui.tableView.setModel(self.tableModel)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.ui.tableView.setColumnWidth(1, 80)
