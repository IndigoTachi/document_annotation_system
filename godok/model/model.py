from PyQt6.QtCore import QStringListModel

class Model(QStringListModel):
    def __init__(self):
        super().__init__()
        self.setStringList(["Hello World!"])