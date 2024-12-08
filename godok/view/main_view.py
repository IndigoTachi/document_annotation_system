from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QPushButton,
    QDialog, QLineEdit, QSpinBox, QFileDialog, QDialogButtonBox, QLabel, QHBoxLayout, 
    QMessageBox, QProgressDialog, QHeaderView
)
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from view.main_view_ui import Ui_MainWindow
from model.main_table_model import DocumentTableModel
import os
import uuid
import shutil
from data.document import Document
from data.document_page import DocumentPage


class AddDocumentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj dokument")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tytuł:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Rok:"))
        self.year_input = QSpinBox()
        self.year_input.setRange(1000, 2100)
        self.year_input.setValue(2023)
        layout.addWidget(self.year_input)

        layout.addWidget(QLabel("Folder:"))
        directory_layout = QHBoxLayout()
        self.directory_input = QLineEdit()
        self.browse_button = QPushButton("Przeglądaj")
        self.browse_button.clicked.connect(self.browse_directory)
        directory_layout.addWidget(self.directory_input)
        directory_layout.addWidget(self.browse_button)
        layout.addLayout(directory_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Wybierz folder")
        if directory:
            self.directory_input.setText(directory)

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "year": self.year_input.value(),
            "directory": self.directory_input.text(),
        }


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
        self.database_model = model
        self.table_model = DocumentTableModel(self.database_model)
        self.database_model.dataChangedSignal.connect(self.table_model.refresh)
        self.database_model.load_documents()
        self.ui.tableView.setModel(self.table_model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.ui.tableView.setColumnWidth(1, 80)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ui.tableView.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.ui.pushButton_2.clicked.connect(self.add_document)
        self.ui.pushButton_3.clicked.connect(self.delete_document)

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
                self.database_model.add_document(new_document)
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
            self.database_model.remove_document(index)
