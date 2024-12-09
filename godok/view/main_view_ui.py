from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("GODok")

        MainWindow.setMinimumSize(600, 400)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(40, 40, 40, 40)

        self.tableLayout = QtWidgets.QVBoxLayout()
        self.tableLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.tableLabel.setObjectName("tableLabel")
        self.tableLayout.addWidget(self.tableLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableView = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.tableLayout.addWidget(self.tableView)
        self.layout.addLayout(self.tableLayout)

        self.layout.addSpacing(100)

        self.buttonLayout = QtWidgets.QVBoxLayout()

        self.openButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.openButton.setObjectName("openButton")
        self.buttonLayout.addWidget(self.openButton)

        self.addButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.buttonLayout.addWidget(self.addButton)

        self.deleteButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.buttonLayout.addWidget(self.deleteButton)

        self.importButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.importButton.setObjectName("importButton")
        self.buttonLayout.addWidget(self.importButton)

        self.exportButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exportButton.setObjectName("exportButton")
        self.buttonLayout.addWidget(self.exportButton)

        self.layout.addLayout(self.buttonLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionhelp = QtGui.QAction(parent=MainWindow)
        self.actionhelp.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionhelp.setObjectName("actionhelp")
        self.actionexit = QtGui.QAction(parent=MainWindow)
        self.actionexit.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionexit.setObjectName("actionexit")
        self.toolBar.addAction(self.actionhelp)
        self.separator = QtWidgets.QWidget(parent=MainWindow)
        self.separator.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.toolBar.addWidget(self.separator)
        self.toolBar.addAction(self.actionexit)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GODok"))
        self.openButton.setText(_translate("MainWindow", "Otwórz"))
        self.addButton.setText(_translate("MainWindow", "Dodaj"))
        self.deleteButton.setText(_translate("MainWindow", "Usuń"))
        self.importButton.setText(_translate("MainWindow", "Importuj"))
        self.exportButton.setText(_translate("MainWindow", "Eksportuj"))
        self.actionhelp.setText(_translate("MainWindow", "Pomoc"))
        self.actionexit.setText(_translate("MainWindow", "Wyjdź"))
        self.tableLabel.setText(_translate("MainWindow", "Dokumenty"))
