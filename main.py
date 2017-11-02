# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PE_3.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QStandardItem, QStandardItemModel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 500)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vLayoutRight = QtWidgets.QVBoxLayout()
        self.vLayoutRight.setObjectName("vLayoutRight")
        self.btnLoad = QtWidgets.QPushButton(self.centralWidget)
        self.btnLoad.setObjectName("btnLoad")
        self.btnLoad.clicked.connect(self.btnLoad_on_click)
        self.vLayoutRight.addWidget(self.btnLoad)
        self.lblAddedRepo = QtWidgets.QLabel(self.centralWidget)
        self.lblAddedRepo.setObjectName("lblAddedRepo")
        self.vLayoutRight.addWidget(self.lblAddedRepo)
        self.lstRepo = QtWidgets.QListView(self.centralWidget)
        self.lstRepo.setObjectName("lstRepo")
        self.vLayoutRight.addWidget(self.lstRepo)
        self.btnAdd = QtWidgets.QPushButton(self.centralWidget)
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.clicked.connect(self.btnAdd_on_click)
        self.vLayoutRight.addWidget(self.btnAdd)
        self.horizontalLayout.addLayout(self.vLayoutRight)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jenkins Automator"))
        self.btnLoad.setText(_translate("MainWindow", "Загрузить из файла"))
        self.lblAddedRepo.setText(_translate("MainWindow", "Список добавленных репозиториев:"))
        self.btnAdd.setText(_translate("MainWindow", "Добавить"))

    @pyqtSlot()
    def btnAdd_on_click(self):
        print('Репозитории добавлены')

    @pyqtSlot()
    def btnLoad_on_click(self):
        fileName = QFileDialog.getOpenFileName(None, "Open File", "/home", "Text (*.txt)");
        f = open(fileName[0])

        model = QStandardItemModel()
        line = f.readline()
        text = line + " / "
        while line:
            model.appendRow(QStandardItem(line))
            line = f.readline()
            text += line + "/ "
        f.close()

        self.lstRepo.setModel(model)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

