#!/usr/bin/env python
#coding=cp936
#coding=utf-8
__author__ = 'huangshuai,dengtao'
import maya.cmds as mc
from maya import OpenMayaUI as omui
from shiboken import wrapInstance
from PySide import QtCore, QtGui
import sys
#界面工程位置
path='E:/work/7_0616_CheckNode/'
#py模块位置
path2='C:/Users/dengtao/Documents/maya/2015-x64/scripts/fantaTexClass'
if not path in sys.path:
    sys.path.append(path)
if not path2 in sys.path:
    sys.path.append(path2)
    
import fantaTexClass

from k_checkNodesWidget import Ui_checkNodesWindow
import checkNodeForMayaReplyWin
import json 


class Communicate(QtCore.QObject):
        buttonSignal=QtCore.Signal(QtGui.QWidget)

class checkNodes(Ui_checkNodesWindow,QtGui.QMainWindow):
    def __init__(self,parent=None):
        self.kcb=[]
        self.k_Treturn={}
        super(checkNodes,self).__init__()
        self.setupUi(self)
        #先show一遍不然tabweiget会有BUG
        self.show()
        #QtCore.QObject.__init__(self)
        #Ui_checkNodesWindow.setupUi(self,checkNodesWidget)
        #设置外围滑条是适应窗口的
        self.scrollArea.setWidgetResizable(True)
        self.close_Button.clicked.connect(self.close)

        self.jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')
        self.checkBoxKeys=self.jsDir.keys()
        #排序
        self.checkBoxKeys.sort()
        self.buttonList=[]
        self.buttonText=[]
        for cb in self.checkBoxKeys:
            button=self.jsDir[cb][3]
            Text=self.jsDir[cb][4]
            if not button in self.buttonList:
                self.buttonList.append(button)
                self.buttonText.append(Text)

        #为了后续对控件做循环修改创建控件组
        self.widgetList=[]
        self.klayoutList=[]

        #为根据控件名字找控件 设定一个父级控件
        karray = []
        karray.append(QtGui.QWidget)

        #创建图标
        self.kopenicon = QtGui.QIcon()
        self.kopenicon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kcloseicon = QtGui.QIcon()
        self.kcloseicon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        #开始创建各种内容
        for i in range(len(self.buttonList)):
            #创建边框
            #self.scrollAreaWidgetContents
            self.kframe_1 = QtGui.QFrame(self.scrollAreaWidgetContents)
            self.kframe_1.setFrameShape(QtGui.QFrame.Box)
            self.kframe_1.setFrameShadow(QtGui.QFrame.Raised)
            self.kframe_1.setObjectName(self.buttonList[i]+"kframe_1") 
            #上级layout将其添加进去
            #self.verticalLayout_2.addWidget(self.kframe_1)
            #边框下紧跟着添加布局
            self.kQVB_1 = QtGui.QVBoxLayout(self.kframe_1)
            self.kQVB_1.setObjectName(self.buttonList[i]+"kQVB_1")
            self.kQVB_1.setContentsMargins(3, 3, 3, 3)
            self.kQVB_1.setSpacing(2)

            self.verticalLayout_2.addWidget(self.kframe_1)
            bt=QtGui.QPushButton()
            bt.setObjectName(self.buttonList[i]+'_button')
            #按钮添加风格化
            bt.setStyleSheet("background-color: #595959;height:20px;border-style:inset;border-width:1px;border-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop:0.5 #616161 stop:1 #616161);font-size: 12px;text-align: left;\n"
            "")
            bt.setText(self.buttonText[i]) 

            self.kQVB_1.addWidget(bt)

            bt.clicked.connect(self.signalEmit)
            #icon = QtGui.QIcon()
            #icon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            #为按钮添加图标
            bt.setIcon(self.kopenicon)
            #添加字体，设置字体
            font = QtGui.QFont()
            font.setPointSize(12)
            bt.setFont(font)

            wd=QtGui.QWidget()
            wd.setObjectName(self.buttonList[i]+'_widget')
            #wd.setMinimumSize(QtCore.QSize(100, 120))
            self.kQVB_1.addWidget(wd)
            self.khorizontalLayout = QtGui.QHBoxLayout(wd)
            self.khorizontalLayout.setObjectName('khorizontalLayout')
            #layout与下级控件的边缘位置
            self.khorizontalLayout.setContentsMargins(0, 0, 0, 0) 

            #
            self.k_frame=QtGui.QFrame(wd)
            self.k_frame.setObjectName("k_frame")
            self.k_frame.setFrameShape(QtGui.QFrame.Box) 
            self.k_frame.setFrameShadow(QtGui.QFrame.Sunken)

            #创建滑动条区域
            #self.k_scroll = QtGui.QScrollArea(wd)
            #滑条区域为自适应
            #self.k_scroll.setWidgetResizable(True)
            #self.k_scroll.setObjectName(self.buttonList[i]+"_scroll")
            #设置滑条区域的边框
            #self.k_scroll.setFrameShape(QtGui.QFrame.Box)
            #self.k_scroll.setFrameShadow(QtGui.QFrame.Sunken)
            #为滑条区域添加控件，必须的
            #self.k_scrollwc = QtGui.QWidget()
            #self.k_scrollwc.setObjectName(self.buttonList[i]+"_scrollwc")
            #self.k_scroll.setWidget(self.k_scrollwc)

            #layout添加控件 注意添加的是滑条区域
            self.khorizontalLayout.addWidget(self.k_frame)

            self.kverticalLayout = QtGui.QVBoxLayout(self.k_frame)
            self.kverticalLayout.setObjectName(self.buttonList[i]+"_kverticalLayout")


            selectAllBt=QtGui.QPushButton()
            selectAllBt.setObjectName(self.buttonList[i]+'_selAll')
            selectAllBt.setText(u'全选')
            selectAllBt.setGeometry(0,0,65,10)
            selectAllBt.setMinimumSize(QtCore.QSize(65, 10))
            selectAllBt.setParent(wd)
            selectAllBt.clicked.connect(self.signalEmit)

            cancelAllBt=QtGui.QPushButton()
            cancelAllBt.setObjectName(self.buttonList[i]+'_canAll')
            cancelAllBt.setText(u'清除')
            cancelAllBt.setGeometry(80,0,65,10)
            cancelAllBt.setMinimumSize(QtCore.QSize(65, 10))
            cancelAllBt.setParent(wd)
            cancelAllBt.clicked.connect(self.signalEmit)
            #添加一个横向弹簧
            kspacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            #布局添加上面两个按钮
            self.kHbLayout = QtGui.QHBoxLayout()
            self.kHbLayout.setObjectName(self.buttonList[i]+"_kHbLayout")
            self.kHbLayout.addWidget(selectAllBt)
            self.kHbLayout.addWidget(cancelAllBt)
            self.kHbLayout.addItem(kspacerItem)
            #布局添加布局
            self.kverticalLayout.addLayout(self.kHbLayout)

            #为循环出来的控件添加到列表里 方便后面循环操作
            self.widgetList.append(wd)
            self.klayoutList.append(self.kverticalLayout)

        #循环添加checkbox控件 self.checkBoxKeys为json的key
        for n in range(len(self.checkBoxKeys)):
            #根据checkbox的父级的位置来创建
            for wd in self.klayoutList:
                #判断名字是否重合
                if wd.objectName()==self.jsDir[self.checkBoxKeys[n]][3]+'_kverticalLayout':
                    cbwd=wd
                    cb=QtGui.QCheckBox()
                    cb.setMinimumSize(QtCore.QSize(0, 20))
                    #print self.jsDir[self.checkBoxKeys[n]][3]+"."+self.checkBoxKeys[n]
                    #cb.setObjectName(self.checkBoxKeys[n])
                    cb.setObjectName(self.jsDir[self.checkBoxKeys[n]][3]+"."+self.checkBoxKeys[n])
                    #print cb.objectName()
                    #cb.setObjectName(self.checkBoxKeys[n])
                    cb.setText(self.jsDir[self.checkBoxKeys[n]][2])
                    #根据json设定是否打勾
                    cb.setChecked(self.jsDir[self.checkBoxKeys[n]][0])
                    wd.addWidget(cb)
                    #根据json设定是否开启
                    if not self.jsDir[self.checkBoxKeys[n]][1]=='true':
                        cb.setEnabled(0)
                    self.kcb.append(cb)


        #根据控件名字 修改控件的属性
        for i in self.kcb:
            if 'common.' in i.objectName():
                pass
            else:
                obj = self.findChild(karray[0],i.objectName())
                obj.setChecked(0)

        for i in self.widgetList:
            if 'common_' in i.objectName():
                pass
            else:
                io=i.objectName()
                io=io.split("_")[0]

                obj = self.findChild(karray[0],i.objectName())
                abj = self.findChild(karray[0],(io+'_button'))
                obj.setVisible(1)
                #icon = QtGui.QIcon()
                #icon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                abj.setIcon(self.kcloseicon)
                
        #在checkbox创建完之后添加一个弹簧
        for klayout in self.klayoutList:
            kvbspacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            klayout.addItem(kvbspacerItem)
        #最外层添加一个弹簧
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)


        self.doIt_Button.clicked.connect(self.kcheckbox)

        #信号连接到槽
        self.someone=Communicate()
        self.someone.buttonSignal.connect(self.buttonCmd)

    def signalEmit(self):
        #sender为 具体的按钮
        sender=self.sender()
        #根据是谁按钮发射信号
        self.someone.buttonSignal.emit(sender)
    #槽函数
    def buttonCmd(self,sender):
        #获取按钮名字
        btName= sender.objectName()
        #print btName
        #btNamew=btName.split("_")[0]
        #print btNamew
        #获取同级的按钮  通过获取父级，再获取儿子级
        parentWd=sender.parent()
        childrenItems=parentWd.children()
        #按钮控制窗口折叠效果
        for i in self.widgetList:
            #print i.objectName()
            #根据按钮名字区分功能
            if btName.split("_")[0]+'_widget'==i.objectName() and 'All' not in btName.split('_')[-1]:
                if i.isVisible():
                    i.setVisible(0)
                    #icon = QtGui.QIcon()
                    #icon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    sender.setIcon(self.kcloseicon)
                else:
                    i.setVisible(1)
                    #icon = QtGui.QIcon()
                    #icon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    sender.setIcon(self.kopenicon)
        #全选与清除按钮的控制效果        
        if btName.split('_')[-1]=='selAll':
            #print btName
            for n in childrenItems:
                #判断控件类型
                if n.metaObject().className()=='QCheckBox':
                    if n.isChecked ()==False and n.isEnabled():
                        n.setChecked(True)
        if btName.split('_')[-1]=='canAll':
            for n in childrenItems:
                if n.metaObject().className()=='QCheckBox':
                    if n.isChecked ()==True and n.isEnabled():
                        n.setChecked(False)

    # 执行命令 具体执行py脚本模块
    def kcheckbox(self):
        #每次都清空返回结果
        self.k_Treturn.clear()
        for cbs in self.kcb:
            #判断checkbox是否勾上
            cbv=cbs.checkState()
            if cbv:
                cbsname=cbs.objectName()
                #k_gocheck=('check.'+cbsname+'()')
                #根据checkbox获取py脚本模块名字
                k_gocheck=('fantaTexClass.'+cbsname+'()')
                #执行py
                k_checklist=eval(k_gocheck)
                #k_update_old={cbsname:k_checklist}
                #print k_update_old
                #以字典形式记录
                k_update={cbsname.split(".")[-1]:k_checklist}
                #print k_update
                #更新字典
                self.k_Treturn.update(k_update)

        #将得出的数据（字典）传输给显示结果的界面
        k_replyNodes(self.k_Treturn)

#显示结果的界面
class k_replyNodes(checkNodeForMayaReplyWin.Ui_MainWindow,QtGui.QMainWindow):
    def __init__(self,k_Treturn):
        super(k_replyNodes,self).__init__()
        self.setupUi(self)
        #先show一遍，不然Tabwidget会出BUG
        self.show()
        if(mc.window("k_replywin",ex=1)):
            mc.deleteUI("k_replywin")
        #maya创建与PYQT转换成pyside   
        Window2=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
        Window2.setObjectName('k_replywin')
        Window2.setGeometry(1048,127,380,820)

        self.jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')
        self.k_reply=k_Treturn.keys()
        self.k_reply.sort()
        krow=0
        for k_reply in self.k_reply:
            #判断如果函数有错误内容则执行具体内容
            if k_Treturn[k_reply]:

                pagename=self.jsDir[k_reply][2]
                knodesize=len(k_Treturn[k_reply])

                #添加page
                self.addpage = QtGui.QWidget()
                self.addpage.setObjectName(k_reply+"_replyPage")
                self.toolBox.insertItem(0,self.addpage,(pagename+'  ('+str(knodesize)+u'个)'))
                self.kvbreply = QtGui.QVBoxLayout(self.addpage)
                self.kvbreply.setObjectName(k_reply+"_replyPageLayout")
                self.kvbreply.setContentsMargins(0, 0, 0, 0)
                self.addTabwidget=QtGui.QTableWidget(self.addpage)
                self.addTabwidget.setObjectName(k_reply+"_replyPageTabWidget")
                self.kvbreply.addWidget(self.addTabwidget)
                TabItem=QtGui.QTableWidgetItem()
                self.addTabwidget.setColumnCount(1)
                self.addTabwidget.setVerticalHeaderItem(0, TabItem)
                self.addTabwidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
                self.addTabwidget.setColumnWidth(0,9999)   
                #设置宽度时需要添加的一行命令           
                self.addTabwidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
                #重要设置  在多选情况下正确选择maya物体（拖选，ctrl+A，shift加选）
                self.addTabwidget.itemSelectionChanged.connect(self.listItemSelect)
                krow+=1
                for k_reply_node in k_Treturn[k_reply]:
                    TabItemname=QtGui.QTableWidgetItem(k_reply_node)
                    self.addTabwidget.insertRow(0)
                    self.addTabwidget.setItem(0,0,TabItemname)
                    self.addTabwidget.setRowHeight(0,20)
        #只要有一个内容错误执行下面命令 （删除无错误字样）
        if krow:
            self.toolBox.setItemText(krow,'')

        Window2.setCentralWidget(self)
        Window2.show()
    #设置选择tabwidget里面内容与maya的选择关联
    def listItemSelect(self):
        #获取当前的page页面，通过当前页面确定子内容
        kcurrentpage=self.toolBox.currentWidget()
        kcurrentpagechild = kcurrentpage.children()

        for kcurrentpagechild in kcurrentpagechild:
            if '_replyPageTabWidget' in kcurrentpagechild.objectName():
                kslItem=kcurrentpagechild.selectedItems()
                kslItemname=[]
                for kslItem in kslItem:
                    kslItemname.append(kslItem.text())
                
                if kslItemname:
                    try:
                        mc.select(kslItemname) 
                    except:
                        pass
                else:
                    mc.select(cl=1)
#打包执行
class loadcheckNode():
    def __init__(self):
        if(mc.window('kcheckNodes',ex=1)):
            mc.deleteUI('kcheckNodes')
        #maya固定格式
        Window=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
        Window.setObjectName('kcheckNodes')
        window=checkNodes()
        #将pyside放入maya的pyside窗口
        Window.setCentralWidget(window)
        Window.setGeometry(650,127,380,820)
        Window.show()


