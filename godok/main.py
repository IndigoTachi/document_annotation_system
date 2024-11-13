from model.database_model import DatabaseModel
from view.main_view import MainView
from PyQt6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    model = DatabaseModel()
    view = MainView(model)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
