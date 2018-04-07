#!/usr/bin/env python
#coding=cp936
#coding=utf-8
__author__ = 'huangshuai,dengtao'
import maya.cmds as mc
from maya import OpenMayaUI as omui
from shiboken import wrapInstance
from PySide import QtCore, QtGui
import sys
#���湤��λ��
path='E:/work/7_0616_CheckNode/'
#pyģ��λ��
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
        #��showһ�鲻Ȼtabweiget����BUG
        self.show()
        #QtCore.QObject.__init__(self)
        #Ui_checkNodesWindow.setupUi(self,checkNodesWidget)
        #������Χ��������Ӧ���ڵ�
        self.scrollArea.setWidgetResizable(True)
        self.close_Button.clicked.connect(self.close)

        self.jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')
        self.checkBoxKeys=self.jsDir.keys()
        #����
        self.checkBoxKeys.sort()
        self.buttonList=[]
        self.buttonText=[]
        for cb in self.checkBoxKeys:
            button=self.jsDir[cb][3]
            Text=self.jsDir[cb][4]
            if not button in self.buttonList:
                self.buttonList.append(button)
                self.buttonText.append(Text)

        #Ϊ�˺����Կؼ���ѭ���޸Ĵ����ؼ���
        self.widgetList=[]
        self.klayoutList=[]

        #Ϊ���ݿؼ������ҿؼ� �趨һ�������ؼ�
        karray = []
        karray.append(QtGui.QWidget)

        #����ͼ��
        self.kopenicon = QtGui.QIcon()
        self.kopenicon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kcloseicon = QtGui.QIcon()
        self.kcloseicon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        #��ʼ������������
        for i in range(len(self.buttonList)):
            #�����߿�
            #self.scrollAreaWidgetContents
            self.kframe_1 = QtGui.QFrame(self.scrollAreaWidgetContents)
            self.kframe_1.setFrameShape(QtGui.QFrame.Box)
            self.kframe_1.setFrameShadow(QtGui.QFrame.Raised)
            self.kframe_1.setObjectName(self.buttonList[i]+"kframe_1") 
            #�ϼ�layout������ӽ�ȥ
            #self.verticalLayout_2.addWidget(self.kframe_1)
            #�߿��½�������Ӳ���
            self.kQVB_1 = QtGui.QVBoxLayout(self.kframe_1)
            self.kQVB_1.setObjectName(self.buttonList[i]+"kQVB_1")
            self.kQVB_1.setContentsMargins(3, 3, 3, 3)
            self.kQVB_1.setSpacing(2)

            self.verticalLayout_2.addWidget(self.kframe_1)
            bt=QtGui.QPushButton()
            bt.setObjectName(self.buttonList[i]+'_button')
            #��ť��ӷ��
            bt.setStyleSheet("background-color: #595959;height:20px;border-style:inset;border-width:1px;border-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop:0.5 #616161 stop:1 #616161);font-size: 12px;text-align: left;\n"
            "")
            bt.setText(self.buttonText[i]) 

            self.kQVB_1.addWidget(bt)

            bt.clicked.connect(self.signalEmit)
            #icon = QtGui.QIcon()
            #icon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            #Ϊ��ť���ͼ��
            bt.setIcon(self.kopenicon)
            #������壬��������
            font = QtGui.QFont()
            font.setPointSize(12)
            bt.setFont(font)

            wd=QtGui.QWidget()
            wd.setObjectName(self.buttonList[i]+'_widget')
            #wd.setMinimumSize(QtCore.QSize(100, 120))
            self.kQVB_1.addWidget(wd)
            self.khorizontalLayout = QtGui.QHBoxLayout(wd)
            self.khorizontalLayout.setObjectName('khorizontalLayout')
            #layout���¼��ؼ��ı�Եλ��
            self.khorizontalLayout.setContentsMargins(0, 0, 0, 0) 

            #
            self.k_frame=QtGui.QFrame(wd)
            self.k_frame.setObjectName("k_frame")
            self.k_frame.setFrameShape(QtGui.QFrame.Box) 
            self.k_frame.setFrameShadow(QtGui.QFrame.Sunken)

            #��������������
            #self.k_scroll = QtGui.QScrollArea(wd)
            #��������Ϊ����Ӧ
            #self.k_scroll.setWidgetResizable(True)
            #self.k_scroll.setObjectName(self.buttonList[i]+"_scroll")
            #���û�������ı߿�
            #self.k_scroll.setFrameShape(QtGui.QFrame.Box)
            #self.k_scroll.setFrameShadow(QtGui.QFrame.Sunken)
            #Ϊ����������ӿؼ��������
            #self.k_scrollwc = QtGui.QWidget()
            #self.k_scrollwc.setObjectName(self.buttonList[i]+"_scrollwc")
            #self.k_scroll.setWidget(self.k_scrollwc)

            #layout��ӿؼ� ע����ӵ��ǻ�������
            self.khorizontalLayout.addWidget(self.k_frame)

            self.kverticalLayout = QtGui.QVBoxLayout(self.k_frame)
            self.kverticalLayout.setObjectName(self.buttonList[i]+"_kverticalLayout")


            selectAllBt=QtGui.QPushButton()
            selectAllBt.setObjectName(self.buttonList[i]+'_selAll')
            selectAllBt.setText(u'ȫѡ')
            selectAllBt.setGeometry(0,0,65,10)
            selectAllBt.setMinimumSize(QtCore.QSize(65, 10))
            selectAllBt.setParent(wd)
            selectAllBt.clicked.connect(self.signalEmit)

            cancelAllBt=QtGui.QPushButton()
            cancelAllBt.setObjectName(self.buttonList[i]+'_canAll')
            cancelAllBt.setText(u'���')
            cancelAllBt.setGeometry(80,0,65,10)
            cancelAllBt.setMinimumSize(QtCore.QSize(65, 10))
            cancelAllBt.setParent(wd)
            cancelAllBt.clicked.connect(self.signalEmit)
            #���һ�����򵯻�
            kspacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            #�����������������ť
            self.kHbLayout = QtGui.QHBoxLayout()
            self.kHbLayout.setObjectName(self.buttonList[i]+"_kHbLayout")
            self.kHbLayout.addWidget(selectAllBt)
            self.kHbLayout.addWidget(cancelAllBt)
            self.kHbLayout.addItem(kspacerItem)
            #������Ӳ���
            self.kverticalLayout.addLayout(self.kHbLayout)

            #Ϊѭ�������Ŀؼ���ӵ��б��� �������ѭ������
            self.widgetList.append(wd)
            self.klayoutList.append(self.kverticalLayout)

        #ѭ�����checkbox�ؼ� self.checkBoxKeysΪjson��key
        for n in range(len(self.checkBoxKeys)):
            #����checkbox�ĸ�����λ��������
            for wd in self.klayoutList:
                #�ж������Ƿ��غ�
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
                    #����json�趨�Ƿ��
                    cb.setChecked(self.jsDir[self.checkBoxKeys[n]][0])
                    wd.addWidget(cb)
                    #����json�趨�Ƿ���
                    if not self.jsDir[self.checkBoxKeys[n]][1]=='true':
                        cb.setEnabled(0)
                    self.kcb.append(cb)


        #���ݿؼ����� �޸Ŀؼ�������
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
                
        #��checkbox������֮�����һ������
        for klayout in self.klayoutList:
            kvbspacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            klayout.addItem(kvbspacerItem)
        #��������һ������
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)


        self.doIt_Button.clicked.connect(self.kcheckbox)

        #�ź����ӵ���
        self.someone=Communicate()
        self.someone.buttonSignal.connect(self.buttonCmd)

    def signalEmit(self):
        #senderΪ ����İ�ť
        sender=self.sender()
        #������˭��ť�����ź�
        self.someone.buttonSignal.emit(sender)
    #�ۺ���
    def buttonCmd(self,sender):
        #��ȡ��ť����
        btName= sender.objectName()
        #print btName
        #btNamew=btName.split("_")[0]
        #print btNamew
        #��ȡͬ���İ�ť  ͨ����ȡ�������ٻ�ȡ���Ӽ�
        parentWd=sender.parent()
        childrenItems=parentWd.children()
        #��ť���ƴ����۵�Ч��
        for i in self.widgetList:
            #print i.objectName()
            #���ݰ�ť�������ֹ���
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
        #ȫѡ�������ť�Ŀ���Ч��        
        if btName.split('_')[-1]=='selAll':
            #print btName
            for n in childrenItems:
                #�жϿؼ�����
                if n.metaObject().className()=='QCheckBox':
                    if n.isChecked ()==False and n.isEnabled():
                        n.setChecked(True)
        if btName.split('_')[-1]=='canAll':
            for n in childrenItems:
                if n.metaObject().className()=='QCheckBox':
                    if n.isChecked ()==True and n.isEnabled():
                        n.setChecked(False)

    # ִ������ ����ִ��py�ű�ģ��
    def kcheckbox(self):
        #ÿ�ζ���շ��ؽ��
        self.k_Treturn.clear()
        for cbs in self.kcb:
            #�ж�checkbox�Ƿ���
            cbv=cbs.checkState()
            if cbv:
                cbsname=cbs.objectName()
                #k_gocheck=('check.'+cbsname+'()')
                #����checkbox��ȡpy�ű�ģ������
                k_gocheck=('fantaTexClass.'+cbsname+'()')
                #ִ��py
                k_checklist=eval(k_gocheck)
                #k_update_old={cbsname:k_checklist}
                #print k_update_old
                #���ֵ���ʽ��¼
                k_update={cbsname.split(".")[-1]:k_checklist}
                #print k_update
                #�����ֵ�
                self.k_Treturn.update(k_update)

        #���ó������ݣ��ֵ䣩�������ʾ����Ľ���
        k_replyNodes(self.k_Treturn)

#��ʾ����Ľ���
class k_replyNodes(checkNodeForMayaReplyWin.Ui_MainWindow,QtGui.QMainWindow):
    def __init__(self,k_Treturn):
        super(k_replyNodes,self).__init__()
        self.setupUi(self)
        #��showһ�飬��ȻTabwidget���BUG
        self.show()
        if(mc.window("k_replywin",ex=1)):
            mc.deleteUI("k_replywin")
        #maya������PYQTת����pyside   
        Window2=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
        Window2.setObjectName('k_replywin')
        Window2.setGeometry(1048,127,380,820)

        self.jsDir=json.loads(open(path+'k_enable.json').read(),encoding='gbk')
        self.k_reply=k_Treturn.keys()
        self.k_reply.sort()
        krow=0
        for k_reply in self.k_reply:
            #�ж���������д���������ִ�о�������
            if k_Treturn[k_reply]:

                pagename=self.jsDir[k_reply][2]
                knodesize=len(k_Treturn[k_reply])

                #���page
                self.addpage = QtGui.QWidget()
                self.addpage.setObjectName(k_reply+"_replyPage")
                self.toolBox.insertItem(0,self.addpage,(pagename+'  ('+str(knodesize)+u'��)'))
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
                #���ÿ��ʱ��Ҫ��ӵ�һ������           
                self.addTabwidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
                #��Ҫ����  �ڶ�ѡ�������ȷѡ��maya���壨��ѡ��ctrl+A��shift��ѡ��
                self.addTabwidget.itemSelectionChanged.connect(self.listItemSelect)
                krow+=1
                for k_reply_node in k_Treturn[k_reply]:
                    TabItemname=QtGui.QTableWidgetItem(k_reply_node)
                    self.addTabwidget.insertRow(0)
                    self.addTabwidget.setItem(0,0,TabItemname)
                    self.addTabwidget.setRowHeight(0,20)
        #ֻҪ��һ�����ݴ���ִ���������� ��ɾ���޴���������
        if krow:
            self.toolBox.setItemText(krow,'')

        Window2.setCentralWidget(self)
        Window2.show()
    #����ѡ��tabwidget����������maya��ѡ�����
    def listItemSelect(self):
        #��ȡ��ǰ��pageҳ�棬ͨ����ǰҳ��ȷ��������
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
#���ִ��
class loadcheckNode():
    def __init__(self):
        if(mc.window('kcheckNodes',ex=1)):
            mc.deleteUI('kcheckNodes')
        #maya�̶���ʽ
        Window=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
        Window.setObjectName('kcheckNodes')
        window=checkNodes()
        #��pyside����maya��pyside����
        Window.setCentralWidget(window)
        Window.setGeometry(650,127,380,820)
        Window.show()


