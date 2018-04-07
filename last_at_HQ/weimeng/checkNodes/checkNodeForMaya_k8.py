#!/usr/bin/env python
#coding=cp936
#coding=utf-8
__author__ = 'huangshuai'
import maya.cmds as mc
from maya import OpenMayaUI as omui
from shiboken import wrapInstance
from PySide import QtCore, QtGui
import sys
path='E:/k/shuai/checkNodes/checkNodes/'
path2='O:/hq_tool/Maya/hq_maya/scripts/fantabox/common'
if not path in sys.path:
    sys.path.append(path)
if not path2 in sys.path:
    sys.path.append(path2)
    
import check
    
from checkNodesWidget_ui import Ui_checkNodesWindow
import weimeng
#import checkNodes_json as js
import json 
class Communicate(QtCore.QObject):
        buttonSignal=QtCore.Signal(QtGui.QWidget)

class checkNodes(Ui_checkNodesWindow,QtCore.QObject):
    kcb=[]
    k_Treturn={}
    def __init__(self,checkNodesWidget):
        QtCore.QObject.__init__(self)
        Ui_checkNodesWindow.setupUi(self,checkNodesWidget)
        self.close_Button.clicked.connect(checkNodesWidget.close)
        self.jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')

        self.checkBoxKeys=self.jsDir.keys()
        self.checkBoxKeys.sort()
        self.buttonList=[]
        self.buttonText=[]
        for cb in self.checkBoxKeys:
            button=self.jsDir[cb][3]
            Text=self.jsDir[cb][4]
            if not button in self.buttonList:
                self.buttonList.append(button)
                self.buttonText.append(Text)
        self.widgetList=[]
        self.klayoutList=[]
        for i in range(len(self.buttonList)):

            self.kframe_1 = QtGui.QFrame(self.scrollAreaWidgetContents)
            self.kframe_1.setFrameShape(QtGui.QFrame.Box)
            self.kframe_1.setFrameShadow(QtGui.QFrame.Raised)
            self.kframe_1.setObjectName(self.buttonList[i]+"kframe_1") 

            self.verticalLayout_2.addWidget(self.kframe_1)

            self.kQVB_1 = QtGui.QVBoxLayout(self.kframe_1)
            self.kQVB_1.setObjectName(self.buttonList[i]+"kQVB_1")
            self.kQVB_1.setContentsMargins(3, 3, 3, 3)
            

            bt=QtGui.QPushButton()
            bt.setObjectName(self.buttonList[i])
            bt.setText(self.buttonText[i])
            
            self.kQVB_1.addWidget(bt)

            bt.clicked.connect(self.signalEmit)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/newPrefix/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            bt.setIcon(icon)
            font = QtGui.QFont()
            font.setPointSize(12)
            bt.setFont(font)


            wd=QtGui.QWidget()
            wd.setObjectName(self.buttonList[i]+'_widget')
            wd.setMinimumSize(QtCore.QSize(100, 20))
            self.kQVB_1.addWidget(wd)

            self.khorizontalLayout = QtGui.QHBoxLayout(wd)
            self.khorizontalLayout.setObjectName('khorizontalLayout')
            self.khorizontalLayout.setContentsMargins(0, 0, 0, 0)    

            self.k_frame=QtGui.QFrame(wd)
            self.k_frame.setObjectName("k_frame")
            self.k_frame.setFrameShape(QtGui.QFrame.Box)
            self.k_frame.setFrameShadow(QtGui.QFrame.Sunken)


            self.khorizontalLayout.addWidget(self.k_frame)

            self.kverticalLayout = QtGui.QVBoxLayout(self.k_frame)
            self.kverticalLayout.setObjectName(self.buttonList[i]+"_kverticalLayout")

            selectAllBt=QtGui.QPushButton()
            selectAllBt.setObjectName(self.buttonList[i]+'_selAll')
            selectAllBt.setText(u'全选')
            selectAllBt.setGeometry(0,0,75,20)
            selectAllBt.setMinimumSize(QtCore.QSize(75, 20))
            selectAllBt.setParent(wd)
            selectAllBt.clicked.connect(self.signalEmit)

            cancelAllBt=QtGui.QPushButton()
            cancelAllBt.setObjectName(self.buttonList[i]+'_canAll')
            cancelAllBt.setText(u'清除')
            cancelAllBt.setGeometry(80,0,75,20)
            cancelAllBt.setMinimumSize(QtCore.QSize(75, 20))
            cancelAllBt.setParent(wd)
            cancelAllBt.clicked.connect(self.signalEmit)

            kspacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        

            self.kHbLayout = QtGui.QHBoxLayout()
            self.kHbLayout.setObjectName(self.buttonList[i]+"_kHbLayout")


            self.kHbLayout.addWidget(selectAllBt)
            self.kHbLayout.addWidget(cancelAllBt)
            self.kHbLayout.addItem(kspacerItem)

            self.kverticalLayout.addLayout(self.kHbLayout)

            self.widgetList.append(wd)

            self.klayoutList.append(self.kverticalLayout)

        for n in range(len(self.checkBoxKeys)):
            for wd in self.klayoutList:
                if wd.objectName()==self.jsDir[self.checkBoxKeys[n]][3]+'_kverticalLayout':
                    cbwd=wd
                    #size=cbwd.minimumHeight()
                    #size+=20
                    #cbwd.setMinimumHeight (size)

                    cb=QtGui.QCheckBox()
                    cb.setObjectName(self.checkBoxKeys[n])
                    #cb.setGeometry(QtCore.QRect(0, (size-20), 409, 16))
                    cb.setText(self.jsDir[self.checkBoxKeys[n]][2])
                    cb.setChecked(self.jsDir[self.checkBoxKeys[n]][0])

                    #layout=str(wd.objectName())+'_kverticalLayout'
                    #print layout
                    wd.addWidget(cb)

                    if not self.jsDir[self.checkBoxKeys[n]][1]=='true':
                        cb.setEnabled(0)
                        
                    self.kcb.append(cb)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        
        self.doIt_Button.clicked.connect(self.kcheckbox)

        self.someone=Communicate()
        self.someone.buttonSignal.connect(self.buttonCmd)
    def signalEmit(self):
        sender=self.sender()
        self.someone.buttonSignal.emit(sender)
    def buttonCmd(self,sender):
        btName= sender.objectName()
        parentWd=sender.parent()
        childrenItems=parentWd.children()
        for i in self.widgetList:
            if btName+'_widget'==i.objectName():
                if i.isVisible():
                    i.setVisible(0)
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/newPrefix/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    sender.setIcon(icon)
                else:
                    i.setVisible(1)
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(":/newPrefix/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    sender.setIcon(icon)
        if btName.split('_')[-1]=='selAll':
            for n in childrenItems:
                if n.metaObject().className()=='QCheckBox':
                    if n.isChecked ()==False and n.isEnabled():
                        n.setChecked(True)
        if btName.split('_')[-1]=='canAll':
            for n in childrenItems:
                if n.metaObject().className()=='QCheckBox':
                    if n.isChecked ()==True and n.isEnabled():
                        n.setChecked(False)
                        
              
    def kcheckbox(self):
        #self.k_Treturn={}
        self.k_Treturn.clear()
        for cbs in self.kcb:
            cbv=cbs.checkState()
            if cbv:
                cbsname=cbs.objectName()
                k_gocheck=('check.'+cbsname+'()')
                k_checklist=eval(k_gocheck)
                k_update={cbsname:k_checklist}
                self.k_Treturn.update(k_update)
                
                
        #print self.k_Treturn
        k_replyNodes(self.k_Treturn)
        return self.k_Treturn
        

class k_replyNodes(weimeng.Ui_MainWindow,QtGui.QMainWindow):
    def __init__(self,k_Treturn):
        #print k_Treturn
        super(k_replyNodes,self).__init__()
        self.setupUi(self)
        self.show()
        Window2=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
        Window2.setGeometry(1040,114,380,845)
        
        self.jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')

        self.k_reply=k_Treturn.keys()
        self.k_reply.sort()

        for k_reply in self.k_reply:
            if k_Treturn[k_reply]:
                #print k_Treturn[k_reply]
                pagename=self.jsDir[k_reply][2]

                self.addpage = QtGui.QWidget()
                self.addpage.setObjectName(k_reply+"_replyPage")
                self.toolBox.insertItem(0,self.addpage,pagename)
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
                self.addTabwidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

                self.addTabwidget.itemClicked.connect(self.listItemSelect)


                for k_reply_node in k_Treturn[k_reply]:
                    TabItemname=QtGui.QTableWidgetItem(k_reply_node)
                    #TabItemname.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
                    TabItemname.setToolTip('False')
                    self.addTabwidget.insertRow(0)
                    self.addTabwidget.setItem(0,0,TabItemname)
                    self.addTabwidget.setRowHeight(0,20)
                    
                    #self.addTabwidget.setColumnWidth(0,140)
        #self.toolBox.removeItem(0)



        Window2.setCentralWidget(self)
        Window2.show()

    def listItemSelect(self):
        kcurrentpage=self.toolBox.currentWidget()
        kcurrentpagechild = kcurrentpage.children()
        for kcurrentpagechild in kcurrentpagechild:
            if '_replyPageTabWidget' in kcurrentpagechild.objectName():
                #kcurrentpagechildname=kcurrentpagechild.objectName()
                kslItem=kcurrentpagechild.selectedItems()
                kslItemname= kslItem[0].text()

                mc.select(kslItemname)  



if(mc.window('checkNodesWindow',ex=1)):
    mc.deleteUI('checkNodesWindow')
Window=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
ui=checkNodes(Window)
Window.show()


