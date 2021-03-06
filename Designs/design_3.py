# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_3.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 128)
        MainWindow.setMinimumSize(QtCore.QSize(370, 128))
        MainWindow.setMaximumSize(QtCore.QSize(370, 128))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Icons/add_class.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(200, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit{border-radius: 2px;\n"
"border: 1px solid #7cd0ef;\n"
"}\n"
"QLineEdit:hover{\n"
"border-color: #5487ee;\n"
"}\n"
"QLineEdit:focus{\n"
"border: 2px solid #54c5ee;\n"
"}")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(200, 30))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("QLineEdit{border-radius: 2px;\n"
"border: 1px solid #7cd0ef;\n"
"}\n"
"QLineEdit:hover{\n"
"border-color: #5487ee;\n"
"}\n"
"QLineEdit:focus{\n"
"border: 2px solid #54c5ee;\n"
"}")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(50)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"background-color: white;\n"
"border-radius: 5px;\n"
"border: 2px solid #6AF2F0;\n"
"}\n"
"QPushButton:hover {\n"
"color: white;\n"
"background-color: #6AF2F0;\n"
"}\n"
"QPushButton:pressed {\n"
"color: white;\n"
"background-color: rgb(47, 231, 247);\n"
"border: 2px solid rgb(47, 231, 247);\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Icons/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_10.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton {\n"
"background-color: white;\n"
"border-radius: 5px;\n"
"border: 2px solid #6AF2F0;\n"
"}\n"
"QPushButton:hover {\n"
"color: white;\n"
"background-color: #6AF2F0;\n"
"}\n"
"QPushButton:pressed {\n"
"color: white;\n"
"background-color: rgb(47, 231, 247);\n"
"border: 2px solid rgb(47, 231, 247);\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/Icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QtCore.QSize(22, 22))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_10.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yangi sinf"))
        self.label_3.setText(_translate("MainWindow", "Sinf nomi:"))
        self.label_4.setText(_translate("MainWindow", "Sinf raxbari:"))
        self.pushButton_2.setText(_translate("MainWindow", "   Bekor qilish"))
        self.pushButton.setText(_translate("MainWindow", "  Tasdiqlash"))
import Res_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
