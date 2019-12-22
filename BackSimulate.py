# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BackSimulate.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap
from PyQt5.QtCore import Qt
import openpyxl
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 700)#554
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 20, 530, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)

        fcolor=QtGui.QPalette()
        fcolor.setColor(QPalette.WindowText,Qt.yellow)
        self.label.setPalette(fcolor)

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.tableView_cmd = QtWidgets.QTableView(self.centralwidget)
        self.tableView_cmd.setGeometry(QtCore.QRect(20, 140, 550, 640))
        self.tableView_cmd.setObjectName("tableView_cmd")


        self.tableView_data = QtWidgets.QTableView(self.centralwidget)
        self.tableView_data.setGeometry(QtCore.QRect(590, 140, 681, 640))
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

        self.tablebutton=QtWidgets.QPushButton("开始填表",self)
        self.tablebutton.setGeometry(QtCore.QRect(1150, 70, 100, 25))
        #self.tablebutton.setPalette(fcolor)
        self.tablebutton.move(1150, 70)

        self.light_lable=QtWidgets.QLabel(self.centralwidget)
        self.light_lable.setGeometry(QtCore.QRect(100, 10, 60, 40))

        self.light_lable.setPalette(fcolor)

        self.light_text = QtWidgets.QLabel(self.centralwidget)
        self.light_text.setGeometry(QtCore.QRect(25, 10, 74, 40))
        self.light_text.setPalette(fcolor)
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.light_text.setFont(font)

        font.setBold(True)
        self.cmd_text = QtWidgets.QLabel(self.centralwidget)
        self.cmd_text.setGeometry(QtCore.QRect(220, 110, 90, 40))
        self.cmd_text.setPalette(fcolor)
        self.cmd_text.setFont(font)


        self.data_text = QtWidgets.QLabel(self.centralwidget)
        self.data_text.setGeometry(QtCore.QRect(830, 110, 150, 40))
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
        #MainWindow.setFixedSize(3*MainWindow.width()/2,3*MainWindow.height()/2)
        MainWindow.setFixedSize(1300,800)#700
        #MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());
        #MainWindow.setStyleSheet("#MainWindow{background-color:yellow}")
        MainWindow.setStyleSheet("#MainWindow{border-image:url(background.jpg);}")
        self.label.setText(_translate("MainWindow", "XX-5X 动力系统模拟后端测控软件V2.0"))
        self.light_lable.setText(_translate("MainWindow", ""))
        self.light_text.setText(_translate("MainWindow", "网络状态:"))
        self.cmd_text.setText(_translate("MainWindow", "指 令 列 表"))
        self.data_text.setText(_translate("MainWindow", "回 采 模 拟 量 列 表"))

class Ui_mainDialog(object):
    def setupUi(self,Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(366, 180)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 125, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)

        fcolor = QtGui.QPalette()
        fcolor.setColor(QPalette.WindowText, Qt.yellow)



        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 180, 16))
        self.label.setObjectName("label")
        self.label.setFont(font)
        self.label.setPalette(fcolor)


        self.comboxdemo = QtWidgets.QComboBox(Dialog)
        self.comboxdemo.setGeometry(QtCore.QRect(10, 70, 341, 32))

        palette=QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("./dmainbg.jpg")))
        self.setPalette(palette)



        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Dialog", "XX-5X 动力系统数据处理平台"))
            Dialog.setWindowIcon(QIcon('amc.ico'))
            self.label.setText(_translate("Dialog", "请选择子处理系统："))

class Ui_tableDialog(object):
    def setupUi(self,Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(366, 450)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 400, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 16, 81, 16))
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(130, 10, 200, 30))
        self.lineEdit.setObjectName("lineEdit")

        #self.lineEdit.textChanged.connect(self.handleTextChanged)

        self.labe2 = QtWidgets.QLabel(Dialog)
        self.labe2.setGeometry(QtCore.QRect(40, 55, 81, 16))
        self.labe2.setObjectName("产品编号：")

        self.lineEdit2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit2.setGeometry(QtCore.QRect(130, 50, 200, 30))
        self.lineEdit2.setObjectName("lineEdit")



        self.labe3 = QtWidgets.QLabel(Dialog)
        self.labe3.setGeometry(QtCore.QRect(40, 95, 81, 16))
        self.labe3.setObjectName("产品编号：")

        self.lineEdit3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit3.setGeometry(QtCore.QRect(130, 90, 200, 30))
        self.lineEdit3.setObjectName("lineEdit")


        self.labe4 = QtWidgets.QLabel(Dialog)
        self.labe4.setGeometry(QtCore.QRect(40, 133, 81, 16))
        self.labe4.setObjectName("产品编号：")

        self.lineEdit4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit4.setGeometry(QtCore.QRect(130, 130, 200, 30))
        self.lineEdit4.setObjectName("lineEdit")

        self.labe5 = QtWidgets.QLabel(Dialog)
        self.labe5.setGeometry(QtCore.QRect(40, 172, 81, 16))
        self.labe5.setObjectName("产品编号：")

        self.lineEdit5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit5.setGeometry(QtCore.QRect(130, 170, 200, 30))
        self.lineEdit5.setObjectName("lineEdit")


        self.button_load = QtWidgets.QPushButton(Dialog)
        self.button_load.setGeometry(QtCore.QRect(30, 210, 200, 30))
        self.button_load.setObjectName("lineEdit")
        self.button_load.clicked.connect(self._reloaddata)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def _reloaddata(self):
        target = self.lineEdit.text()
        if target!="":
            target = str('./嵌入式测试表/') + target + '.xlsx'
            print(target)
            if os.path.exists(target) == True:
                _sheet1 = ['D5', 'D6', 'D10', 'D11']
                excel_obj = openpyxl.load_workbook(target)
                new_sheet = excel_obj.worksheets[0]
                print(new_sheet[_sheet1[0]].value)
                self.lineEdit2.setText(str(new_sheet[_sheet1[0]].value))
                self.lineEdit3.setText(str(new_sheet[_sheet1[1]].value))
                print(new_sheet[_sheet1[2]].value)
                self.lineEdit4.setText(str(new_sheet[_sheet1[2]].value))
                self.lineEdit5.setText(str(new_sheet[_sheet1[3]].value))

                excel_obj.close()
            else:
                print("文件不存在!")
        else:
            print("文件名输入为空！")



    def handleTextChanged(self):
        #print(self.lineEdit.text())
        pass


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "填表窗口"))
        Dialog.setWindowIcon(QIcon('amc.ico'))
        self.label.setText(_translate("Dialog", "表格名称："))
        self.labe2.setText(_translate("Dialog", "产品编号："))
        self.labe3.setText(_translate("Dialog", "测试人员："))
        self.labe4.setText(_translate("Dialog", "湿    度："))
        self.labe5.setText(_translate("Dialog", "温    度："))
        self.button_load.setText(_translate("Dialog", "重载文件"))


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