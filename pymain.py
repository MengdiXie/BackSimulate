
from  BackSimulate import *
from socket import *
from PyQt5 import  QtWidgets,sip
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from xml.dom.minidom import parse
from enum import Enum
import struct
import datetime
import time
import threading
import binascii
import sys
import inspect
import ctypes
import openpyxl
import shutil


import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']




class EmptyDelegate(QItemDelegate):
    def __init__(self,parent):
        super(EmptyDelegate,self).__init__(parent)
    def createEditor(self,QWidgt,QStyleOptionViewItem,QModelIndex):
        return None


#最后帧技术变量初始化
MCS_Global_lastFrameCount=1
TargetAddr_global=("",0)
global_time_start=time.time()
global_time_end=time.time()
global_getdataornot=False  #是否检测到保存数据操作
global_targetfile=''
global_alocation=['I4','I6','I8','I10','I12','I14','I16','I18','I20','I22','I24','I26','I28','I30','I32']


#class MyModel(QSqlTableModel):
#  def __init__(self):
#      QSqlTableModel.__init__(self)

# 指令回令处理线程类
# 参数1：cmdupd_socket-网络接收用套接字
# 参数2：cmdtype-网络指令类型
class CmdThread_Process(threading.Thread):
    def __init__(self, cmdupd_socket, _cmdtype):
        threading.Thread.__init__(self)
        self.cmd_socket = cmdupd_socket
        self.cmd_type = _cmdtype
        self._stop_event=threading.Event()


    def run(self):
        print("开始线程:")
        self._CmdThread_Process()
    def stop(self):
        print("准备结束线程cmd")
        self._stop_event.set()
        print("设置完结束线程cmd")
        
    def stopped(self):
        return self._stop_event.is_set()

    def _CmdThread_Process(self):
        while True:
            global MCS_Global_lastFrameCount
            data, addr = self.cmd_socket.recvfrom(1500)
            #print("接收信息的来源 ,%s:%s" % addr)
            #print("接收信息的数据 ", data)
            #CmdTP_S = struct.Struct('!2sHBBBBHBBIHHII4sIHHIHHI')
            CmdTP_S = struct.Struct('2sHBBBBHBBIHHII4sI')
            CmdTP_table = CmdTP_S.unpack(data)
            #print(CmdTP_table)
            #print(CmdTP_table[10])

            #print(self.cmd_type)
            if CmdTP_table[10] == int(self.cmd_type):
                MCS_Global_lastFrameCount = CmdTP_table[12]
                #print("MCS_Global_lastFrameCount=",MCS_Global_lastFrameCount)
                print("Excute Normal Command ok,Ack ok!")
            else:
                print("非法回令帧，请检查!")
            

class amc_form(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(amc_form,self).__init__()
        self.setupUi(self)
        #载入网络显示灯图片
        pix=QPixmap("light_off.jpg")
        self.light_lable.setPixmap(pix)
        # 表格模板相对路径
        self.sourcefilepath="./嵌入式测试表/嵌入式整机模板.xlsx"

        self.model=QStandardItemModel(4,4)
        self.model.setHorizontalHeaderLabels(['表号','编号','类型','指令名称'])#,'符号'

        self.mode2=QStandardItemModel(5,5)
        self.mode2.setHorizontalHeaderLabels(['表号','编码号','类型','参数名称','结果'])

        # 存储配置文件使用字典类型
        self.InfoKeyData={}
        #载入配置文件
        self.LoadXML()
        #绑定填表按钮事件
        self.tablebutton.clicked.connect(self.Inputtable)

        self.QRZ=int(0x0b)
        self.PCSJ = 0x06
        self.YDHL = 0x02
        self.CSZL = 0x01
        self.PTZL=0x04
        self.DCZL=0x05


        self.InfoHead_HeadFlag = bytes(2)
        self.InfoHead_FrameLength = 0
        self.InfoHead_SourceSystemCode = int(self.InfoKeyData["LocalSysCode"][0])#帧头 ：HeadFlag[0] = 0xeb;HeadFlag[1] = 0x90
        self.InfoHead_SourceMachineCode = int(self.InfoKeyData["LocalNodeCode"][0])
        self.InfoHead_TargetSystemCode = int(self.InfoKeyData["RemoteSysCode"][0])
        self.InfoHead_TargetMachineCode = int(self.InfoKeyData["RemoteNodeCode"][0])
        self.InfoHead_Year = datetime.datetime.now().strftime('%Y')
        self.InfoHead_Month = datetime.datetime.now().strftime('%m')
        self.InfoHead_Day = datetime.datetime.now().strftime('%d')
        self.InfoHead_Time = int(round(time.time()*1000))
        self.InfoHead_FrameType = self.CSZL
        self.InfoHead_RetryNum = 0
        self.InfoHead_FrameNum = 0
        self.InfoHead_InfoWordCount = 0
        self.InfoHead_Reserved = bytes(4)
        self.InfoHead_CheckSum = 0

        self.InfoHead_Len = 36        #帧头

        self.InfoWords_TableNum = 0
        self.InfoWords_CodeNum = 0
        self.InfoWords_Data = 0
        self.InfoWords_OOTType = 0
        self.InfoWords_DataType = 0
        self.InfoWords_Reserved = 0

        self.InfoWords_Len = 16  # 帧头

        self.MCS_mode = False
        self.MCS_targetPort = 8080
        self.MCS_targetIP = bytes(20)
        self.MCS_nettype = 0
        self.MCS_frametype = int(self.PTZL)#初始值0x04
        self.MCS_wordnum = 0
        self.MCS_FrameRecognize = 0
        self.MCS_FrameSum = 0
        self.MCS_TotalBytes = 0




        #配置1号机IP和port信息
        self.TargetAddr_1=(self.InfoKeyData["TartGetIP1"][0],int(self.InfoKeyData["TargetPort"][0]))
        #配置2号机IP和port信息
        self.TargetAddr_2= (self.InfoKeyData["TartGetIP2"][0], int(self.InfoKeyData["TargetPort"][0]))

        #初始化设置为1号机（初始化）
        self.TargetAddr=self.TargetAddr_1

        #创建网络指令接收套接字
        self.CmdProcess_udp_socket=socket(AF_INET,SOCK_DGRAM)
        self.DataProcess_udp_socket=socket(AF_INET,SOCK_DGRAM)
        self.RcvHeartBeat_udp_socket=socket(AF_INET,SOCK_DGRAM)
        #设置本地IP和接收端口
        self.CmdProcess_udp_socket.bind(("",int(self.InfoKeyData["SendPort"][0])))
        #print(("127.0.0.1",int(self.InfoKeyData["SendPort"][0])))

        self.DataProcess_udp_socket.bind(("", int(self.InfoKeyData["RevDataPort"][0])))

        self.RcvHeartBeat_udp_socket.bind(("", int(self.InfoKeyData["HeartBeatPort"][0])))

        #print("MCS_Global_lastFrameCount=",MCS_Global_lastFrameCount)
        #创建接收线程
        self.Cmd_thread1=CmdThread_Process(self.CmdProcess_udp_socket,self.QRZ)

        #self.Cmd_thread1.setDaemon(True)#开启守护线程机制，主线程结束，子线程退出
        self.Cmd_thread1.start()

        self.Dialog = QtWidgets.QDialog()
        self.cmd_dialog = Ui_Dialog()#引用对话框
        self.cmd_dialog.setupUi(self.Dialog)#对话框初始化

        self.InputTableDialog = QtWidgets.QDialog()
        self.inputtable_dialog = Ui_tableDialog()
        self.inputtable_dialog.setupUi(self.InputTableDialog)


        #palette=QPalette()
        #palette.setBrush(QPalette.Background,QBrush(QPixmap("./dmainbg.jpg")))
        #self.inputtable_dialog.setPalette(palette)

        self.para_edit = self.cmd_dialog.lineEdit
        #设置一次选中一行
        self.tableView_cmd.setSelectionBehavior(QAbstractItemView.SelectRows)

        #设置禁止编辑
        #self.tableView_cmd.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_cmd.setModel(self.model)
        self.tableView_cmd.doubleClicked.connect(self.tableview_clicked)
        self.tableView_cmd.setColumnWidth(0, 70)
        self.tableView_cmd.setColumnWidth(1, 70)
        self.tableView_cmd.setColumnWidth(3, 200)

        #self.tableView_data.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_data.setModel(self.mode2)

        self.Data_thread1 = self.DataThread_Process(self.DataProcess_udp_socket,self.mode2,self.TargetAddr,self.machine_1,self.machine_2)
        #self.Data_thread1.setDaemon(True)#开启守护线程机制，主线程结束，子线程退出
        self.Data_thread1.start()

        self.Listening_thread=self.Listening_Thread(self.light_lable,self.Cmd_thread1)
        #self.Listening_thread.setDaemon(True)#开启守护线程机制，主线程结束，子线程退出
        self.Listening_thread.start()

        self.RcvHeartBeat_Process_thread=self.RcvHeartBeat_Process(self.RcvHeartBeat_udp_socket)
        #self.RcvHeartBeat_Process_thread.setDaemon(True)#开启守护线程机制，主线程结束，子线程退出
        self.RcvHeartBeat_Process_thread.start()

        self.machine_1.toggled.connect(self.machine_1_clicked)
        self.machine_2.toggled.connect(self.machine_2_clicked)
    # 载入xml配置文件处理函数，将xml配置文件加载存储全局变量
    def LoadXML(self):
        domTree=parse("./customer.xml")

        #文件根元素
        rootNode=domTree.documentElement
        #所有顾客
        Networks=rootNode.getElementsByTagName("netWork")
        #Networks 是一个数组

        Protocols=Networks[0].getElementsByTagName("Protocol")
        #print("*********所有protocol信息**************")
        for protocol in Protocols:
            if protocol.hasAttribute("LocalSysCode"):
                self.addInfo(self.InfoKeyData, "LocalSysCode", protocol.getAttribute("LocalSysCode"))
                self.addInfo(self.InfoKeyData, "LocalNodeCode", protocol.getAttribute("LocalNodeCode"))
                self.addInfo(self.InfoKeyData, "RemoteSysCode", protocol.getAttribute("RemoteSysCode"))
                self.addInfo(self.InfoKeyData, "RemoteNodeCode", protocol.getAttribute("RemoteNodeCode"))

        Networks = rootNode.getElementsByTagName("netWork")
        Cmd1s=Networks[0].getElementsByTagName("Cmd1")
        #print("*********所有Cmd1信息**************")
        for cmd1 in Cmd1s:
            if cmd1.hasAttribute("SendPort"):
                self.addInfo(self.InfoKeyData,"SendPort",cmd1.getAttribute("SendPort"))
                self.addInfo(self.InfoKeyData, "TargetPort", cmd1.getAttribute("TargetPort"))
                self.addInfo(self.InfoKeyData, "RevDataPort", cmd1.getAttribute("RevDataPort"))
                self.addInfo(self.InfoKeyData, "HeartBeatPort", cmd1.getAttribute("HeartBeatPort"))
                self.addInfo(self.InfoKeyData, "TartGetIP1", cmd1.getAttribute("TartGetIP1"))
                self.addInfo(self.InfoKeyData, "TartGetIP2", cmd1.getAttribute("TartGetIP2"))


        Commands = rootNode.getElementsByTagName("Command")

        Cmds=Commands[0].getElementsByTagName("Cmd")
        i_row=0
        Cmd_listName=["table","Code","Type","Name"]

        for cmdtemp in Cmds:
            self.tableView_cmd.setItemDelegateForColumn(i_row, EmptyDelegate(self))
            Cmd_list = []
            for i in range(4):
                Cmd_list.append(cmdtemp.getAttribute(Cmd_listName[i]))
            for j_col in range(4):
                 item = QStandardItem(Cmd_list[j_col])
                 self.model.setItem(i_row, j_col, item)
                 self.model.item(i_row, j_col).setBackground(QtGui.QBrush(QtGui.QColor(133, 196, 123)))  # 设置背景颜色
            i_row+=1

        DataCollects = rootNode.getElementsByTagName("DataCollect")
        Datas=DataCollects[0].getElementsByTagName("Data")
        Data_listName = ["table", "Code", "Type", "Name"]
        for i,x in enumerate(Datas):
            self.tableView_data.setItemDelegateForColumn(i, EmptyDelegate(self))
            Data_list=[]
            for i_row in range(4):
                Data_list.append(x.getAttribute(Data_listName[i_row]))
            for j_col in range(4):
                items=QStandardItem(Data_list[j_col])
                self.mode2.setItem(i, j_col, items)
                self.mode2.item(i, j_col).setBackground(QtGui.QBrush(QtGui.QColor(133, 196, 123)))#设置背景颜色
                if j_col==3:
                    self.mode2.setItem(i, 4, QStandardItem(str("xx")))
                    self.mode2.item(i, 4).setBackground(QtGui.QBrush(QtGui.QColor(133, 196, 123)))  # 设置背景颜色
                    self.mode2.item(i, 4).setFont(QtGui.QFont("Times", 14, QtGui.QFont.Black))


    def machine_1_clicked(self):
        global TargetAddr_global
        TargetAddr_global=self.TargetAddr_1

    def machine_2_clicked(self):
        global TargetAddr_global
        TargetAddr_global=self.TargetAddr_2



    # 指令列表双击事件处理函数,响应指令发送
    def tableview_clicked(self,index):
        #获取行号，并获取所在列元素
        text = self.model.item(index.row(), 3).text()
        self.cmd_dialog.label_cmdname.setText(text)
        #可以编辑
        self.cmd_dialog.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        if index.row() <= 86:
            #不可编辑
            self.cmd_dialog.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.Dialog.show()
        rsp = self.Dialog.exec()
        cmdType=True
        if rsp == QtWidgets.QDialog.Accepted:
            if index.row()<=86:
                cmdType=True
                self.InfoWords_CodeNum = int(self.model.item(index.row(), 1).text())
                self.InfoWords_TableNum = int(self.model.item(index.row(), 0).text())
                self.InfoWords_Data = 0
                self.InfoWords_OOTType = 0
                self.InfoWords_DataType = 0
                self.MCS_frametype = int(self.PTZL)

                self.MCS_mode = 1
                self.MCS_nettype = 0
                self.MCS_targetPort = self.InfoKeyData["TargetPort"][0]
                self.MCS_targetIP = self.InfoKeyData["TartGetIP1"][0]
                self.MCS_wordnum = 1

                self.InfoHead_HeadFlag=b'\xeb\x90'
                self.InfoHead_FrameLength = self.InfoHead_Len+self.InfoWords_Len
                self.InfoHead_Year = int(datetime.datetime.now().strftime('%Y'))
                self.InfoHead_Month = int(datetime.datetime.now().strftime('%m'))
                self.InfoHead_Day = int(datetime.datetime.now().strftime('%d'))
                self.InfoHead_Time =0# int(round(time.time()*1000)
                self.InfoHead_FrameType=self.MCS_frametype
                self.InfoHead_FrameNum+=1
                self.InfoHead_RetryNum=0
                self.InfoHead_Reserved=bytes(4)
                self.InfoHead_InfoWordCount=self.MCS_wordnum

                List_temp = []
                List_temp.append(self.InfoHead_HeadFlag)
                List_temp.append(self.InfoHead_FrameLength)
                List_temp.append(self.InfoHead_SourceSystemCode)
                List_temp.append(self.InfoHead_SourceMachineCode)
                List_temp.append(self.InfoHead_TargetSystemCode)
                List_temp.append(self.InfoHead_TargetMachineCode)
                List_temp.append(self.InfoHead_Year)
                List_temp.append(self.InfoHead_Month)
                List_temp.append(self.InfoHead_Day)
                List_temp.append(self.InfoHead_Time)
                List_temp.append(self.InfoHead_FrameType)
                List_temp.append(self.InfoHead_RetryNum)
                List_temp.append(self.InfoHead_FrameNum)
                List_temp.append(self.InfoHead_InfoWordCount)
                List_temp.append(self.InfoHead_Reserved)
                List_temp.append(self.InfoHead_CheckSum)

                List_temp.append(self.InfoWords_TableNum)
                List_temp.append(self.InfoWords_CodeNum)
                List_temp.append(self.InfoWords_Data)
                List_temp.append(self.InfoWords_OOTType)
                List_temp.append(self.InfoWords_DataType)
                List_temp.append(self.InfoWords_Reserved)

                MCS_Table = tuple(List_temp)
                #print("step5", MCS_Table)
                MCS_S = struct.Struct('2sHBBBBHBBIHHII4sIHHIHHI')  # 网络发送标准 大端
                # print("step5.5")
                MCS_para1 = MCS_S.pack(*MCS_Table)
                # print("step6")
                # print("source", MCS_para1)
                MCS_Unpack = MCS_S.unpack(MCS_para1)
                List_temp = list(MCS_Unpack)
                List_temp[15] = self.MCS_CalCheckOut(MCS_para1)
                MCS_Table = tuple(List_temp)
                MCS_para1 = MCS_S.pack(*MCS_Table)

            else:
                cmdType=False
                print("获取参数1")
                self.InfoWords_CodeNum = int(self.model.item(index.row(), 1).text())
                self.InfoWords_TableNum = int(self.model.item(index.row(), 0).text())
                self.InfoWords_Data = self.cmd_dialog.lineEdit.text().encode('utf-8')# str
                #print(self.cmd_dialog.lineEdit.text())
                #print(type(self.InfoWords_Data ))
                #print(self.InfoWords_Data)
                self.InfoWords_OOTType = 0
                self.InfoWords_DataType = int(0xffff)

                self.MCS_frametype = int(self.DCZL)

                self.MCS_mode = 1
                self.MCS_nettype = 0
                self.MCS_targetPort = self.InfoKeyData["TargetPort"][0]
                self.MCS_targetIP = self.InfoKeyData["TartGetIP1"][0]
                self.MCS_wordnum = 2#两个信息字

                self.InfoHead_HeadFlag=b'\xeb\x90'
                self.InfoHead_FrameLength = self.InfoHead_Len+self.InfoWords_Len*self.MCS_wordnum
                self.InfoHead_Year = int(datetime.datetime.now().strftime('%Y'))
                self.InfoHead_Month = int(datetime.datetime.now().strftime('%m'))
                self.InfoHead_Day = int(datetime.datetime.now().strftime('%d'))
                self.InfoHead_Time =0# int(round(time.time()*1000)
                self.InfoHead_FrameType=self.MCS_frametype
                self.InfoHead_FrameNum+=1
                self.InfoHead_RetryNum=0
                self.InfoHead_Reserved=bytes(4)
                self.InfoHead_InfoWordCount=self.MCS_wordnum

                List_temp = []
                List_temp.append(self.InfoHead_HeadFlag)
                List_temp.append(self.InfoHead_FrameLength)
                List_temp.append(self.InfoHead_SourceSystemCode)
                List_temp.append(self.InfoHead_SourceMachineCode)
                List_temp.append(self.InfoHead_TargetSystemCode)
                List_temp.append(self.InfoHead_TargetMachineCode)
                List_temp.append(self.InfoHead_Year)
                List_temp.append(self.InfoHead_Month)
                List_temp.append(self.InfoHead_Day)
                List_temp.append(self.InfoHead_Time)
                List_temp.append(self.InfoHead_FrameType)
                List_temp.append(self.InfoHead_RetryNum)
                List_temp.append(self.InfoHead_FrameNum)
                List_temp.append(self.InfoHead_InfoWordCount)
                List_temp.append(self.InfoHead_Reserved)
                List_temp.append(self.InfoHead_CheckSum)

                List_temp.append(self.InfoWords_TableNum)
                List_temp.append(self.InfoWords_CodeNum)
                List_temp.append(self.InfoWords_Data)
                List_temp.append(self.InfoWords_OOTType)
                List_temp.append(self.InfoWords_DataType)
                List_temp.append(self.InfoWords_Reserved)


                self.InfoWords_CodeNum = int(self.model.item(index.row(), 1).text())
                self.InfoWords_TableNum = int(self.model.item(index.row(), 0).text())
                self.InfoWords_Data = int(0xaa)
                #print(type(self.InfoWords_Data ))
                #print(self.InfoWords_Data)
                self.InfoWords_OOTType = int(0x5555)
                self.InfoWords_DataType = int(0xaaaa)

                List_temp.append(self.InfoWords_TableNum)
                List_temp.append(self.InfoWords_CodeNum)
                List_temp.append(self.InfoWords_Data)
                List_temp.append(self.InfoWords_OOTType)
                List_temp.append(self.InfoWords_DataType)
                List_temp.append(self.InfoWords_Reserved)

                MCS_Table = tuple(List_temp)
                print("step5", MCS_Table)
                MCS_S = struct.Struct('2sHBBBBHBBIHHII4sI HH4sHHI HHIHHI')  # 网络发送标准 大端
                MCS_para1 = MCS_S.pack(*MCS_Table)
                print("step6")
                print("source", MCS_para1)
                MCS_Unpack = MCS_S.unpack(MCS_para1)
                List_temp = list(MCS_Unpack)
                List_temp[15] = self.MCS_CalCheckOut(MCS_para1)
                MCS_Table = tuple(List_temp)
                MCS_para1 = MCS_S.pack(*MCS_Table)

            global  TargetAddr_global

            #选择目标机
            if self.machine_1.isChecked()==True:
                #QMessageBox.information(self, '选择1号机', '选择1号机')
                self.TargetAddr=self.TargetAddr_1
                TargetAddr_global=self.TargetAddr_1
                #print("1号机",self.TargetAddr)
            if self.machine_2.isChecked()==True:
                QMessageBox.information(self, '选择2号机', '选择2号机')
                self.TargetAddr = self.TargetAddr_2
                TargetAddr_global = self.TargetAddr_2
                print("2号机", self.TargetAddr)



            udp_socket_=socket(AF_INET,SOCK_DGRAM)

            #self.TargetAddr=("127.0.0.1",8080)#测试用，正式使用删除次句子
            self.MCS_SendCmd(udp_socket_,MCS_para1,MCS_Global_lastFrameCount,cmdType)
            udp_socket_.close()

        else:
            #for info in self.InfoKeyData:#测试打印
            #    print(self.InfoKeyData[info][0])
            QMessageBox.information(self, 'cancel','退出指令发送！' )


    #定义校验函数
    #def MCS_CalCheckout():
    #整型转换为bytes流处理函数
    #参数1：value-待转换整型数据
    #参数2：length-bytes数据流长度
    #返回值：result_bytes-所转换的bytes数据流结果
    def intToBytes(self,value, length):
        result = []
        for i in range(0, length):
            result.append(value >> (i * 8) & 0xff)
        result.reverse()
        result_bytes = bytes(result)
        return result_bytes

    # 配置文件保存为字典数据结构处理函数
    # 参数1：theIndex-字典类型变量
    # 参数2：key-字典键值
    # 参数3: data-保存数据,与键值对应
    def addInfo(self,theIndex,key,data):
        theIndex.setdefault(key,[]).append(data)

    # 计算bytes流校验和处理函数
    # 参数1: data-待处理bytes数据流
    # 返回值：_checkout-校验和结果
    def MCS_CalCheckOut(self,data):
        _checkout=0
        for i,x in enumerate(data):
            if i<(self.InfoHead_Len-4) or i>(self.InfoHead_Len-1):
                _checkout+=x
        return _checkout

    def MCS_SendCmd(self,_udp_socket,data,lastFrameCount,_cmdtype):
        global  MCS_Global_lastFrameCount
        #_udp_socket.sendto(data, ("127.0.0.1", 8080))#TargetAddr_1
        _udp_socket.sendto(data, self.TargetAddr)
        if _cmdtype==True:#不带参数指令
            _MCS_S = struct.Struct('2sHBBBBHBBIHHII4sIHHIHHI')  # 网络发送标准 大端警告
        if _cmdtype==False:#带参数指令
            _MCS_S = struct.Struct('2sHBBBBHBBIHHII4sIHH4sHHIHHIHHI')
        _MCS_Unpack=_MCS_S.unpack(data)
        _List_temp=list(_MCS_Unpack)
        #print("frame=",_List_temp)
        _framecount=_List_temp[12]

        time.sleep(0.3)
        print("lastFrame=",MCS_Global_lastFrameCount,"head->FrameNum=",_framecount)
        if MCS_Global_lastFrameCount<_framecount:
            _MCS_Table = tuple(_List_temp)
            _MCS_para1 = _MCS_S.pack(*_MCS_Table)
            _List_temp[15] = self.MCS_CalCheckOut(_MCS_para1)
            _List_temp[11]=1   #重传一次
            MCS_Table = tuple(_List_temp)
            data = _MCS_S.pack(*MCS_Table)
            #_udp_socket.sendto(data, ("127.0.0.1", 8080))
            # _udp_socket.sendto(data, ("127.0.0.1", 8080))#TargetAddr_1
            _udp_socket.sendto(data, self.TargetAddr)

        time.sleep(0.3)
        if MCS_Global_lastFrameCount<_framecount:
            _MCS_Table = tuple(_List_temp)
            _MCS_para1 = _MCS_S.pack(*_MCS_Table)
            _List_temp[15] = self.MCS_CalCheckOut(_MCS_para1)
            _List_temp[11]=2   #重传一次
            MCS_Table = tuple(_List_temp)
            data = _MCS_S.pack(*MCS_Table)
            #_udp_socket.sendto(data, ("127.0.0.1", 8080))
            _udp_socket.sendto(data, self.TargetAddr)
    def Inputtable(self):
        #print("开始填表!")
        #self.InputTableDialog.show()

        f_txt=open('./嵌入式测试表/RecentFile.txt')
        self.inputtable_dialog.lineEdit.setText(f_txt.read())
        f_txt.close()
        self.inputtable_dialog._reloaddata()
        rsp = self.InputTableDialog.exec()
        if rsp == QtWidgets.QDialog.Accepted:#新建测试文件
            global  global_getdataornot
            global global_targetfile  # 全局变量
            target = self.inputtable_dialog.lineEdit.text()
            if target!='':
                global_targetfile = str('./嵌入式测试表/') + str(target)+'.xlsx'
                if os.path.exists(global_targetfile)==False:
                    print(target)
                    self.moveFileto(self.sourcefilepath,global_targetfile)
                    time.sleep(1)#等待1s保证 文件拷贝完成
                    global_getdataornot=True #可以开始保存数据了
                    self._inputalldata()
                else:
                    print('文件已经存在，不需要拷贝')#回读
                    self._inputalldata()
                    #self._reloaddata()
            else:
                print('输入为空')


    def _inputalldata(self):
        global global_targetfile
        _sheet1=['D5','D6','D10','D11']
        _sheet2=['B9','E9']
        _sheet3=['C38','F38']
        _sheet4=['C38','F38']
        _sheet5= ['C34','F34']
        _sheet6= ['C13', 'F13','C19', 'F19','I4','I6','I8','I10','E18']
        _sheet7 = ['B7', 'E7', 'B12', 'E12', 'B17', 'E17', 'B23', 'E23','A16','B16','E16','B22']
        RecentFile=self.inputtable_dialog.lineEdit.text()
        product=self.inputtable_dialog.lineEdit2.text()
        examname = self.inputtable_dialog.lineEdit3.text()
        humidity = self.inputtable_dialog.lineEdit4.text()
        temperature = self.inputtable_dialog.lineEdit5.text()
        list_模拟量输出采集值=self.inputtable_dialog.lineEdit_模拟量输出.text().split(",")
        print(list_模拟量输出采集值)

        time_双机切换时间=self.inputtable_dialog.lineEdit_双机切换时间.text()

        list_电流电压=self.inputtable_dialog.lineEdit_功耗.text().split(",")

        heart_data=self.inputtable_dialog.lineEdit_心跳.text()

        excel_obj = openpyxl.load_workbook(global_targetfile)
        new_sheet = excel_obj.worksheets[0]
        new_sheet[_sheet1[0]] = product
        new_sheet[_sheet1[1]] = examname+str(",")+str(datetime.datetime.now().strftime('%Y/%m/%d'))
        new_sheet[_sheet1[2]] = humidity
        new_sheet[_sheet1[3]] = temperature

        new_sheet = excel_obj.worksheets[1]
        new_sheet[_sheet2[0]] = examname
        new_sheet[_sheet2[1]] = datetime.datetime.now().strftime('%Y/%m/%d')
        new_sheet = excel_obj.worksheets[2]
        new_sheet[_sheet3[0]] = examname
        new_sheet[_sheet3[1]] = datetime.datetime.now().strftime('%Y/%m/%d')
        new_sheet = excel_obj.worksheets[3]
        new_sheet[_sheet4[0]] = examname
        new_sheet[_sheet4[1]] = datetime.datetime.now().strftime('%Y/%m/%d')

        new_sheet = excel_obj.worksheets[4]
        new_sheet[_sheet5[0]] = examname
        new_sheet[_sheet5[1]] = datetime.datetime.now().strftime('%Y/%m/%d')

        new_sheet = excel_obj.worksheets[5]
        new_sheet[_sheet6[0]] = examname
        new_sheet[_sheet6[1]] = datetime.datetime.now().strftime('%Y/%m/%d')
        new_sheet[_sheet6[2]] = examname
        new_sheet[_sheet6[3]] = datetime.datetime.now().strftime('%Y/%m/%d')

        if len(list_模拟量输出采集值) == 4:
            for i,d in enumerate(list_模拟量输出采集值):
                new_sheet[_sheet6[i+4]]=list_模拟量输出采集值[i]
        else:
            QMessageBox.information(self,'模拟量输出数量提示','数量不满等于4，请检查！')
            pass

        new_sheet[_sheet6[8]] = time_双机切换时间


        new_sheet = excel_obj.worksheets[6]
        new_sheet[_sheet7[0]] = examname
        new_sheet[_sheet7[1]] = datetime.datetime.now().strftime('%Y/%m/%d')
        new_sheet[_sheet7[2]] = examname
        new_sheet[_sheet7[3]] = datetime.datetime.now().strftime('%Y/%m/%d')
        new_sheet[_sheet7[4]] = examname
        new_sheet[_sheet7[5]] = datetime.datetime.now().strftime('%Y/%m/%d')
        new_sheet[_sheet7[6]] = examname
        new_sheet[_sheet7[7]] = datetime.datetime.now().strftime('%Y/%m/%d')

        new_sheet[_sheet7[8]]=list_电流电压[0]
        new_sheet[_sheet7[9]] = list_电流电压[1]
        new_sheet[_sheet7[10]]="{:.4f}".format(float(list_电流电压[0])*float(list_电流电压[1]))

        new_sheet[_sheet7[11]]=heart_data

        f_txt = open('./嵌入式测试表/RecentFile.txt','r+')
        f_txt.write(RecentFile)
        f_txt.truncate()#清空txt
        f_txt.close()


        excel_obj.save(global_targetfile)

    def moveFileto(self,source,target):
        shutil.copy(source, target)    #拷贝文件

    class DataThread_Process(threading.Thread):
        def __init__(self,data_socket,_viewmode,addr_,radiobutton_1,radiobutton_2):
            threading.Thread.__init__(self)
            self._data_socket=data_socket
            self._mode=_viewmode
            self._addr=addr_
            self._radiobutton_1=radiobutton_1
            self._radiobutton_2 = radiobutton_2
        def run(self):
            print("开始采集数据线程:")
            self._DataThread_Process()

        def _DataThread_Process(self):
            dataTP_S = struct.Struct('2sHBBBBHBBIHHII4sIHHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI HHfHHI')
            dataTP_headword = struct.Struct('2sHBBBBHBBIHHII4sIHHfHHI')
            collect_num=0#累计10周期计算一次
            while True:
                global TargetAddr_global
                global global_getdataornot
                global global_targetfile
                global global_alocation
                data,addr=self._data_socket.recvfrom(1500)
                #print(len(data))
                #print(addr)
                data_temp=data[0:52]#获取第一个字，判断当前数据
                Data_temptable=dataTP_headword.unpack(data_temp)
                #print(Data_temptable)
                collect_num+=1
                collect_data=[0 for i in range(16)]
                if Data_temptable[16]==20821:
                    Data_table=dataTP_S.unpack(data)
                    #print(Data_table)
                    data_temp=Data_table[18:len(Data_table):6]
                    #print(data_temp)
                    #print(self._radiobutton_1.isChecked())
                    self._mode.beginResetModel()#开始刷新数据
                    #print("addr[0]",addr[0])
                    #print("_addr[0]",TargetAddr_global[0])
                    if (addr[0]==TargetAddr_global[0]) and self._radiobutton_1.isChecked()==True :#如果数据来源地址与当前软件操作地址一致则显示，否则不显示，防止数据混叠
                        print("接收信息的来源：%s:%s" % addr)
                        #print("接收信息的数据 ", data)
                        for i,x in enumerate(data_temp):
                            item = QStandardItem("{:.4f}".format(data_temp[i]))#调试
                            self._mode.setItem(i, 4, item)

                    if (addr[0]==TargetAddr_global[0]) and self._radiobutton_2.isChecked()==True:
                        print("更新2号机接收信息的来源：%s:%s" % addr)
                    self._mode.endResetModel()#接收刷新

                    #检测到标志，进行数据保存
                    if global_getdataornot==True and data_temp[0]>4:

                        for i,d in enumerate(data_temp):
                            if d>4.5:
                                collect_data[i]+=d

                        print("开始保存数据")
                        if collect_num==1:
                            excel_obj = openpyxl.load_workbook(global_targetfile)
                            new_sheet = excel_obj.worksheets[4]

                        if collect_num==10:
                            for i,d in enumerate(collect_data):
                                    new_sheet[global_alocation[i]]=d/collect_num
                            excel_obj.save(global_targetfile)
                            collect_num = 0






                #if Data_temptable[16]==20822:
    class RcvHeartBeat_Process(threading.Thread):
        def __init__(self,data_socket):
            threading.Thread.__init__(self)
            self._data_socket=data_socket

        def run(self):
            print("开始心跳线程:")
            self._RcvHeartBeat_Process()
        def _RcvHeartBeat_Process(self):
            RcvHearBeat_S = struct.Struct('2sHBBBBHBBIHHII4sI')
            global  global_time_start
            pix = QPixmap("light_on.jpg")
            while True:#累计收到10帧表征网络准备ok
                global_time_start=time.time()#获取起始时间
                data, addr = self._data_socket.recvfrom(1500)
                RcvHearBeat_table = RcvHearBeat_S.unpack(data)
                if RcvHearBeat_table[10]==10:#判断心跳帧
                    self.light_lable.setPixmap(pix)


    class Listening_Thread(threading.Thread):
        def __init__(self,light_lable,cmd_thread):
            threading.Thread.__init__(self)
            self.light_lable=light_lable
            self.cmd_thread=cmd_thread
        def run(self):
            print("开始监听线程:")
            self._Listening_Thread()

        def _Listening_Thread(self):
            global global_time_end
            global global_time_start
            pix = QPixmap("light_off.jpg")
            while True:
                global_time_end=time.time()
                time.sleep(1)
                if (global_time_end-global_time_start)>3:#如果网络断3s
                    self.light_lable.setPixmap(pix)
            
    #结束一个线程
    def _async_raise(self,tid,exctype):
        tid=ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype=type(exctype)
        res=ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,ctypes.py_object(exctype))
        if res==0:
            raise ValueError("invalid thread id")
        elif res!=1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    #结束线程接口
    def Stop_thread(self,thread):
        self._async_raise(thread.ident,SystemExit)


    #关闭窗口时清理垃圾
    def closeEvent(self,event):
        reply=QtWidgets.QMessageBox.question(self,'退出测控软件提示','您确定要退出程序？',
                                             QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        if reply==QtWidgets.QMessageBox.Yes:
            #退出时关闭子线程，并清理套接字定义
            self.Stop_thread(self.Cmd_thread1)
            self.Stop_thread(self.Data_thread1)
            self.Stop_thread(self.RcvHeartBeat_Process_thread)
            self.Stop_thread(self.Listening_thread)
            
            self.CmdProcess_udp_socket.close()
            self.DataProcess_udp_socket.close()
            self.RcvHeartBeat_udp_socket.close()

            event.accept()                  
        else:
            event.ignore()
        

class main_form(QtWidgets.QDialog,Ui_mainDialog):
    def __init__(self):
        super(main_form, self).__init__()
        self.setupUi(self)


        self.comboxdemo.addItem("动力系统模拟后端测控软件平台")
        self.comboxdemo.addItem("信号调理组合整机自动化测试平台")
        self.comboxdemo.addItem("动力系统自研单板测试填表软件平台")

        self.icon=QIcon("amc.ico")
        self.comboxdemo.setItemIcon(0,self.icon)
        self.comboxdemo.setItemIcon(1, self.icon)
        self.comboxdemo.setItemIcon(2, self.icon)
        self.comboxdemo.iconSize()
        self.comboxdemo.currentIndexChanged.connect(self.selectionchange)

    def selectionchange(self,i):

        print("item",i,self.comboxdemo.currentText())





        #main_ui=amc_form()

        #main_ui.show()
        print("main_form")





def exitfunc(arg='hello world!'):
    print(arg)
    print('exit is done')

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    # ui=amc_form()
    ui=main_form()
    #ui.show()

    rsp = ui.exec()
    if rsp == QtWidgets.QDialog.Accepted:  # 新建测试文件
        if ui.comboxdemo.currentText()=="动力系统模拟后端测控软件平台":
            main_ui=amc_form()
            main_ui.show()
            sys.exit(app.exec())
    else:
        print("退出")
