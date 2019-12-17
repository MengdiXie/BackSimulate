# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BackSimulate.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QIcon,QPalette
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 554)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 430, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)

        fcolor=QtGui.QPalette()
        fcolor.setColor(QPalette.WindowText,Qt.yellow)
        self.label.setPalette(fcolor)

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.tableView_cmd = QtWidgets.QTableView(self.centralwidget)
        self.tableView_cmd.setGeometry(QtCore.QRect(20, 120, 430, 401))
        self.tableView_cmd.setObjectName("tableView_cmd")


        self.tableView_data = QtWidgets.QTableView(self.centralwidget)
        self.tableView_data.setGeometry(QtCore.QRect(470, 120, 541, 401))
        self.tableView_data.setObjectName("tableView_data")


        self.machine_1 = QtWidgets.QRadioButton("嵌入式1号机值班",self)
        self.machine_2 = QtWidgets.QRadioButton("嵌入式2号机值班",self)
        self.machine_1.setGeometry(QtCore.QRect(20, 50, 200, 25))
        self.machine_2.setGeometry(QtCore.QRect(20, 75, 200, 25))
        self.machine_1.setChecked(True)
        self.machine_2.setChecked(False)
        self.machine_1.setPalette(fcolor)
        #self.machine_1.setFont(font)
        self.machine_2.setPalette(fcolor)
        #self.machine_2.setFont(font)
        self.machine_1.move(20,50)
        self.machine_2.move(20,75)

        self.light_lable=QtWidgets.QLabel(self.centralwidget)
        self.light_lable.setGeometry(QtCore.QRect(90, 10, 60, 40))

        self.light_lable.setPalette(fcolor)

        self.light_text = QtWidgets.QLabel(self.centralwidget)
        self.light_text.setGeometry(QtCore.QRect(25, 10, 55, 40))
        self.light_text.setPalette(fcolor)
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.light_text.setFont(font)

        font.setBold(True)
        self.cmd_text = QtWidgets.QLabel(self.centralwidget)
        self.cmd_text.setGeometry(QtCore.QRect(200, 90, 70, 40))
        self.cmd_text.setPalette(fcolor)
        self.cmd_text.setFont(font)


        self.data_text = QtWidgets.QLabel(self.centralwidget)
        self.data_text.setGeometry(QtCore.QRect(670, 90, 120, 40))
        self.data_text.setPalette(fcolor)
        self.data_text.setFont(font)



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "XX-5X 动力系统模拟后端测控软件"))
        MainWindow.setWindowIcon(QIcon('amc.ico'))
        #MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());
        #MainWindow.setStyleSheet("#MainWindow{background-color:yellow}")
        MainWindow.setStyleSheet("#MainWindow{border-image:url(background.jpg);}")
        self.label.setText(_translate("MainWindow", "XX-5X 动力系统模拟后端测控软件V2.0"))
        self.light_lable.setText(_translate("MainWindow", ""))
        self.light_text.setText(_translate("MainWindow", "网络状态:"))
        self.cmd_text.setText(_translate("MainWindow", "指 令 列 表"))
        self.data_text.setText(_translate("MainWindow", "回 采 模 拟 量 列 表"))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(366, 150)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(130, 60, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_cmdname = QtWidgets.QLabel(Dialog)
        self.label_cmdname.setGeometry(QtCore.QRect(130, 30, 111, 16))
        self.label_cmdname.setText("")
        self.label_cmdname.setObjectName("label_cmdname")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "指令窗口"))
        self.label.setText(_translate("Dialog", "指令名称："))
        self.label_2.setText(_translate("Dialog", "参   数："))