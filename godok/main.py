from model.database_model import DatabaseModel
from view.main_view import MainView
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys


def main():
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("GODok")
    app.setWindowIcon(QIcon("book.png"))
    model = DatabaseModel()
    view = MainView(model)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
