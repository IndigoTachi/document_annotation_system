from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDialog, QWidget, QMessageBox, QListWidget,
    QLineEdit, QTextEdit, QComboBox, QInputDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from data.database import DocumentDatabase
from data.annotation import Annotation
from helpers.image_label import ImageLabel
import os


class DocumentWindow(QDialog):
    def __init__(self, model, document, parent=None):
        super().__init__(parent)
        self.document = document
        self.model = DocumentDatabase()
        self.current_page_index = 0
        self.current_annotation = None
        self.setWindowTitle(f"Edytowanie dokumentu: {self.document.name}")
        self.setMinimumSize(1000, 700)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)

        self.padding = 150

        # document
        document_layout = QVBoxLayout()

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_document)
        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.cancel_window)

        document_layout.addWidget(self.save_button)
        document_layout.addWidget(self.cancel_button)

        self.title_label = QLabel(f"Tytuł: {self.document.name}")
        document_layout.addWidget(self.title_label)

        self.image_label = ImageLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: lightgray;")
        document_layout.addWidget(self.image_label)

        navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("<")
        self.prev_button.clicked.connect(self.previous_page)
        self.page_number_label = QLabel(f"Strona {self.current_page_index + 1} / {len(self.document.pages)}")
        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.next_page)

        navigation_layout.addWidget(self.prev_button)
        navigation_layout.addWidget(self.page_number_label)
        navigation_layout.addWidget(self.next_button)
        document_layout.addLayout(navigation_layout)

        self.save_rectangle_button = QPushButton("Zapisz wycinek")
        self.save_rectangle_button.clicked.connect(self.save_rectangle)
        self.save_rectangle_button.setEnabled(False)
        document_layout.addWidget(self.save_rectangle_button)

        main_layout.addLayout(document_layout)

        # annotation list
        center_layout = QVBoxLayout()
        self.annotation_list = QListWidget()
        self.update_annotation_list()
        self.annotation_list.itemSelectionChanged.connect(self.select_annotation)

        self.add_annotation_button = QPushButton("Dodaj adnotację")
        self.add_annotation_button.clicked.connect(self.add_annotation)

        self.remove_annotation_button = QPushButton("Usuń adnotację")
        self.remove_annotation_button.clicked.connect(self.remove_annotation)

        center_layout.addWidget(QLabel("Adnotacje"))
        center_layout.addWidget(self.annotation_list)
        center_layout.addWidget(self.add_annotation_button)
        center_layout.addWidget(self.remove_annotation_button)

        main_layout.addLayout(center_layout)

        # annotation info
        right_layout = QVBoxLayout()
        self.annotation_name_label = QLabel("Nazwa: Brak")
        self.annotation_image_placeholder = QLabel("Brak obrazu")
        self.annotation_image_placeholder.setMinimumSize(300, 300)
        self.annotation_image_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.annotation_author_input = QLineEdit()
        self.annotation_author_input.setPlaceholderText("Autor")
        self.annotation_author_input.textChanged.connect(self.update_annotation_author)

        self.annotation_content_input = QTextEdit()
        self.annotation_content_input.setPlaceholderText("Opis")
        self.annotation_content_input.textChanged.connect(self.update_annotation_content)

        self.dropdown_label = QLabel("Rozpoznawanie tekstu:")
        self.dropdown = QComboBox()
        self.dropdown.addItems(["1", "2", "3"])
        self.dropdown_button = QPushButton("Wykonaj OCR")
        self.dropdown_button.clicked.connect(self.perform_ocr)

        right_layout.addWidget(self.annotation_name_label)
        right_layout.addWidget(self.annotation_image_placeholder)
        right_layout.addWidget(QLabel("Autor"))
        right_layout.addWidget(self.annotation_author_input)
        right_layout.addWidget(QLabel("Opis"))
        right_layout.addWidget(self.annotation_content_input)
        right_layout.addWidget(self.dropdown_label)
        right_layout.addWidget(self.dropdown)
        right_layout.addWidget(self.dropdown_button)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        # Set dialog layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_page_image()

    def update_page_image(self):
        if not self.document.pages:
            self.image_label.setText("Brak stron")
            return

        current_page = self.document.pages[self.current_page_index]
        path = os.path.abspath(os.path.join('../images/', current_page.path))
        current_page = self.document.pages[self.current_page_index]
        try:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                raise FileNotFoundError(f"Nie znaleziono: {path}")

            available_width = self.width() - 2 * self.padding
            available_height = self.height() - 2 * self.padding

            available_width = max(1, available_width)
            available_height = max(1, available_height)

            scaled_pixmap = pixmap.scaled(
                available_width,
                available_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.rect_coords = None
            self.annotation_list.clear()
            for annotation in current_page.annotations:
                self.annotation_list.addItem(annotation.name)

            self.current_annotation = None

        except FileNotFoundError:
            self.image_label.setText("Nie znaleziono pliku")
        except Exception as e:
            self.image_label.setText(f"Błąd: {e}")

    def next_page(self):
        if self.current_page_index < len(self.document.pages) - 1:
            self.current_page_index += 1
            self.update_page_image()
            self.update_annotation_list()
            self.page_number_label.setText(f"Strona {self.current_page_index + 1} / {len(self.document.pages)}")

    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.update_page_image()
            self.update_annotation_list()
            self.page_number_label.setText(f"Strona {self.current_page_index + 1} / {len(self.document.pages)}")

    def save_document(self):
        self.model.update_document(self.document)

    def cancel_window(self):
        confirm = QMessageBox.question(
            self, "Anuluj", "Czy na pewno chcesz anulować? Niezapisane zmiany zostaną utracone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.accept()

    def update_annotation_list(self):
        self.annotation_list.clear()
        if not self.document.pages:
            return
        current_page = self.document.pages[self.current_page_index]
        for annotation in current_page.annotations:
            self.annotation_list.addItem(annotation.name)

    def add_annotation(self):
        name, ok = QInputDialog.getText(self, "Dodaj adnotację", "Wpisz nazwę:")
        if ok and name.strip():
            annotation = Annotation(name=name.strip())
            self.document.pages[self.current_page_index].insert_annotation(annotation)
            self.update_annotation_list()

    def remove_annotation(self):
        index = self.annotation_list.currentRow()
        if index >= 0:
            del self.document.pages[self.current_page_index].annotations[index]
            self.update_annotation_list()

    def update_annotation_author(self):
        if self.current_annotation:
            self.current_annotation.author = self.annotation_author_input.text()

    def update_annotation_content(self):
        if self.current_annotation:
            self.current_annotation.content = self.annotation_content_input.toPlainText()

    def perform_ocr(self):
        print(f"{self.dropdown.currentText()}")

    def save_rectangle(self):
        if not self.current_annotation:
            self.annotation_image_placeholder.setText("Nie wybrano adnotacji")
            return

        rect_coords = self.image_label.rect_coords
        if not rect_coords:
            self.annotation_image_placeholder.setText("Brak wycinka")
            return

        pixmap = self.image_label.pixmap()
        if pixmap.isNull():
            return

        img_width, img_height = pixmap.width(), pixmap.height()
        x1, y1, x2, y2 = (
            rect_coords[0] / img_width,
            rect_coords[1] / img_height,
            (rect_coords[0] + rect_coords[2]) / img_width,
            (rect_coords[1] + rect_coords[3]) / img_height,
        )
        self.current_annotation.coords = [x1, y1, x2, y2]

        self.display_cropped_image()

    def display_cropped_image(self):
        if not self.current_annotation or not self.current_annotation.coords:
            self.annotation_image_placeholder.setText("Brak wycinka")
            return

        coords = self.current_annotation.coords
        current_page = self.document.pages[self.current_page_index]
        path = os.path.abspath(os.path.join('../images/', current_page.path))
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.annotation_image_placeholder.setText(f"Błąd ładowania: {current_page.path}")
            return

        img_width, img_height = pixmap.width(), pixmap.height()
        x, y = int(coords[0] * img_width), int(coords[1] * img_height)
        width, height = int((coords[2] - coords[0]) * img_width), int((coords[3] - coords[1]) * img_height)
        cropped_pixmap = pixmap.copy(x, y, width, height)

        label_width = self.annotation_image_placeholder.width()
        label_height = self.annotation_image_placeholder.height()

        scaled_cropped_pixmap = cropped_pixmap.scaled(
            label_width,
            label_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.annotation_image_placeholder.setPixmap(scaled_cropped_pixmap)

    def select_annotation(self):
        selected_items = self.annotation_list.selectedItems()
        if selected_items:
            annotation_name = selected_items[0].text()
            current_page = self.document.pages[self.current_page_index]
            print(annotation_name)
            print(current_page.annotations)
            self.current_annotation = next(
                (a for a in current_page.annotations if a.name == annotation_name), None
            )
            self.image_label.can_draw = True
            self.save_rectangle_button.setEnabled(True)
            self.annotation_name_label.setText(f"Nazwa: {self.current_annotation.name}")
            self.annotation_author_input.setText(self.current_annotation.author)
            self.annotation_content_input.setPlainText(self.current_annotation.content)
            self.image_label.clear_rectangle()
            self.display_annotation_rectangle()
            self.display_cropped_image()
        else:
            self.current_annotation = None
            self.annotation_name_label.setText("Nazwa: Brak")
            self.annotation_author_input.clear()
            self.annotation_content_input.clear()
            self.image_label.can_draw = False
            self.image_label.clear_rectangle()
            self.save_rectangle_button.setEnabled(False)
            self.annotation_image_placeholder.setText("Nie wybrano adnotacji")

        self.image_label.rect_coords = None if not self.current_annotation else self.image_label.rect_coords
        self.image_label.update()

    def display_annotation_rectangle(self):
        if not self.current_annotation or not self.current_annotation.coords:
            self.image_label.clear_rectangle()
            return

        coords = self.current_annotation.coords
        pixmap = self.image_label.pixmap()
        if pixmap.isNull():
            return

        label_width = self.image_label.width()
        label_height = self.image_label.height()
        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()

        width_ratio = label_width / pixmap_width
        height_ratio = label_height / pixmap_height
        scaling_ratio = min(width_ratio, height_ratio)

        img_width = pixmap.width()
        img_height = pixmap.height()
        x = int(coords[0] * img_width * scaling_ratio)
        y = int(coords[1] * img_height * scaling_ratio)
        width = int((coords[2] - coords[0]) * img_width * scaling_ratio)
        height = int((coords[3] - coords[1]) * img_height * scaling_ratio)

        self.image_label.set_rect_coords([x, y, width, height])
