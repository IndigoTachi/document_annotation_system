from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QFileDialog, QDialogButtonBox, QLabel,
    QDialog, QLineEdit, QSpinBox, QHBoxLayout
)


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
