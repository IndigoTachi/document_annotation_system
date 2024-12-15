from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDialog, QTextEdit, QRadioButton, QProgressBar
)
from PyQt6.QtCore import (pyqtSignal, QThread)
from helpers import ocr
from PIL import ImageQt


class WorkerThread(QThread):
    results_ready = pyqtSignal(list)

    def __init__(self, image, checkbox_values):
        super().__init__()
        self.image = image
        self.checkbox_values = checkbox_values

    def run(self):
        results = []

        if self.checkbox_values["tesseract"]:
            results.append(ocr.ocr_tesseract(self.image))

        if self.checkbox_values["google"]:
            results.append(ocr.ocr_google_vision(self.image))

        if self.checkbox_values["azure"]:
            results.append(ocr.ocr_azure(self.image))

        if self.checkbox_values["ocrwebservice"]:
            results.append(ocr.ocr_ocrwebservice(self.image))

        self.results_ready.emit(results)


class OcrWindow(QDialog):
    def __init__(self, image, checkbox_values, original_text_box):
        super().__init__()

        self.setWindowTitle('OCR')
        self.setMinimumSize(700, 500)
        self.image = ImageQt.fromqimage(image.toImage())
        self.checkbox_values = checkbox_values
        self.original_text_box = original_text_box

        new_layout = QVBoxLayout(self)

        self.progress_bar = QProgressBar(self)
        new_layout.addWidget(self.progress_bar)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.worker = WorkerThread(self.image, self.checkbox_values)
        self.worker.results_ready.connect(self.display_results)
        self.worker.start()

    def display_results(self, results):
        text_label = QLabel("Wyniki OCR:")
        self.layout().addWidget(text_label)
        self.progress_bar.setValue(100)
        self.result_widgets = []
        self.result_radio_buttons = []

        for result_text in results:
            self.create_result_box(result_text)

        self.confirm_button = QPushButton('Potwierdź', self)
        self.cancel_button = QPushButton('Anuluj', self)
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.cancel_button.clicked.connect(self.reject)
        self.layout().addWidget(self.confirm_button)
        self.layout().addWidget(self.cancel_button)
        for radio_button in self.result_radio_buttons:
            radio_button.toggled.connect(self.toggle_confirm_button)

    def create_result_box(self, result_text):
        result_layout = QHBoxLayout()
        radio_button = QRadioButton(self)
        text_edit = QTextEdit(self)
        text_edit.setText(result_text)
        text_edit.setReadOnly(True)
        result_layout.addWidget(radio_button)
        result_layout.addWidget(text_edit)
        self.result_widgets.append(text_edit)
        self.result_radio_buttons.append(radio_button)
        self.layout().addLayout(result_layout)

    def toggle_confirm_button(self):
        any_selected = any(radio_button.isChecked() for radio_button in self.result_radio_buttons)
        self.confirm_button.setEnabled(any_selected)

    def confirm_selection(self):
        for i, radio_button in enumerate(self.result_radio_buttons):
            if radio_button.isChecked():
                selected_text = self.result_widgets[i].toPlainText()
                self.original_text_box.setText(selected_text)
                self.close()
                break
