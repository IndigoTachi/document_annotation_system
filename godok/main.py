from model.model import Model
from view.view import View
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    model = Model()
    view = View(model)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()