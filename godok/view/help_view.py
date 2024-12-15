from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QSplitter, QListWidget, QLabel, QTextEdit, QHBoxLayout, QStackedWidget, QWidget


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Pomoc")
        self.setGeometry(100, 100, 800, 400)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.list_widget = QListWidget()
        self.list_widget.addItem("Dodawanie dokumentu")
        self.stacked_widget = QStackedWidget(self)
        self.create_content_for_item("Dodawanie dokumentu", "Aby dodać dokument, kliknij Dodaj. Następnie wpisz nazwę dokumentu i wybierz lokalizację, z której chcesz go wczytać.", "obrazek.jpg")

        splitter.addWidget(self.list_widget)
        splitter.addWidget(self.stacked_widget)
        splitter.setSizes([200, 600])

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)
        self.list_widget.itemClicked.connect(self.on_item_clicked)

    def create_content_for_item(self, item_name, text, image_path):
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        content_text = QTextEdit()
        content_text.setPlainText(text)
        content_text.setReadOnly(True)
        layout.addWidget(content_text)

        label_image = QLabel()
        # pixmap = QPixmap(image_path)
        # label_image.setPixmap(pixmap)
        label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_image)
        self.stacked_widget.addWidget(content_widget)

    def on_item_clicked(self, item):
        index = self.list_widget.row(item)
        self.stacked_widget.setCurrentIndex(index)
