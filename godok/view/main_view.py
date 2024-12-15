from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QDialog,
    QMessageBox, QProgressDialog, QHeaderView, QApplication
)
from PyQt6.QtCore import Qt
from view.main_view_ui import Ui_MainWindow
from model.main_table_model import DocumentTableModel
import os
import uuid
import shutil
from data.document import Document
from data.document_page import DocumentPage
from view.add_document_view import AddDocumentDialog
from view.editor_view import DocumentWindow
from view.help_view import HelpDialog


def create_document(name: str, year: int, source_dir: str, destination_base_dir: str, parent=None) -> Document:
    file_list = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'))]
    progress_dialog = QProgressDialog("Tworzenie dokumentu...", "Anuluj", 0, len(file_list), parent)
    progress_dialog.setWindowTitle("Postęp")
    progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    progress_dialog.show()

    if not os.path.exists(destination_base_dir):
        os.makedirs(destination_base_dir)

    unique_folder_name = uuid.uuid4().hex
    document_dir = os.path.join(destination_base_dir, unique_folder_name)
    os.makedirs(document_dir)

    document = Document(name=name, year=year)

    for i, filename in enumerate(file_list):
        if progress_dialog.wasCanceled():
            raise Exception("Anulowano.")

        source_path = os.path.join(source_dir, filename)
        destination_path = os.path.join(document_dir, filename)

        shutil.copy(source_path, destination_path)

        relative_path = os.path.relpath(destination_path, start=destination_base_dir)
        page = DocumentPage(path=relative_path)
        document.insert_page(page)

        progress_dialog.setValue(i + 1)

    return document


class MainView(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.databaseModel = model
        self.tableModel = DocumentTableModel(self.databaseModel)
        self.databaseModel.dataChangedSignal.connect(self.tableModel.refresh)
        self.databaseModel.load_documents()
        self.ui.tableView.setModel(self.tableModel)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.ui.tableView.setColumnWidth(1, 80)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ui.tableView.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.ui.addButton.clicked.connect(self.add_document)
        self.ui.deleteButton.clicked.connect(self.delete_document)
        self.ui.openButton.clicked.connect(self.open_document)
        self.ui.actionhelp.triggered.connect(self.show_help)
        self.ui.actionexit.triggered.connect(self.quit_application)

    def quit_application(self):
        QApplication.quit()

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

    def add_document(self):
        dialog = AddDocumentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            name = data['title']
            year = data['year']
            source_dir = data['directory']

            if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
                QMessageBox.warning(self, "Nieprawidłowy folder", "Wybrany folder jest nieprawidłowy.")
                return

            destination_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "images"))

            try:
                new_document = create_document(name, year, source_dir, destination_base_dir, parent=self)
                self.databaseModel.add_document(new_document)
                QMessageBox.information(self, "Sukces", f"Dokument '{name}' został utworzony.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Błąd tworzenia dokumentu: {e}")

    def delete_document(self):
        selected_indexes = self.ui.tableView.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Brak wyboru", "Wybierz dokument do usunięcia.")
            return

        confirm = QMessageBox.question(
            self, "Usuń", "Czy na pewno chcesz usunąć wybrany dokument?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            index = selected_indexes[0]
            self.databaseModel.remove_document(index)

    def open_document(self):
        selected_indexes = self.ui.tableView.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Brak wyboru", "Wybierz dokument do otwarcia.")
            return

        # print(self.databaseModel.documents)
        # print(selected_indexes[0].row())
        selected_document = self.databaseModel.documents[selected_indexes[0].row()]
        document_window = DocumentWindow(model=self.databaseModel, document=selected_document, parent=self)
        document_window.exec()
