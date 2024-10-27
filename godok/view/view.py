from PyQt6.QtWidgets import QMainWindow, QListView, QVBoxLayout, QWidget

class View(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.setWindowTitle("GODok")
        list_view = QListView()
        list_view.setModel(model)
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(list_view)
        self.setCentralWidget(central_widget)