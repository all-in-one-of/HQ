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
import socket
import urllib
import urllib2
import webbrowser

class Communicate(QtCore.QObject):
        buttonSignal=QtCore.Signal(QtGui.QWidget)
        kpreSignal=QtCore.Signal(QtGui.QWidget)

class checkNodes(Ui_checkNodesWindow,QtGui.QMainWindow):
    def __init__(self,parent=None):
        self.kcb=[]
        self.k_Treturn={}
        self.k_preset=[]
        super(checkNodes,self).__init__()
        self.setupUi(self)
        self.show()
        self.scrollArea.setWidgetResizable(True)
        self.close_Button.clicked.connect(self.close)
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
        karray = []
        karray.append(QtGui.QWidget)
        self.kopenicon = QtGui.QIcon()
        self.kopenicon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kcloseicon = QtGui.QIcon()
        self.kcloseicon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/kclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        for i in range(len(self.buttonList)):
            self.kframe_1 = QtGui.QFrame(self.scrollAreaWidgetContents)
            self.kframe_1.setFrameShape(QtGui.QFrame.Box)
            self.kframe_1.setFrameShadow(QtGui.QFrame.Raised)
            self.kframe_1.setObjectName(self.buttonList[i]+"kframe_1") 
            self.kQVB_1 = QtGui.QVBoxLayout(self.kframe_1)
            self.kQVB_1.setObjectName(self.buttonList[i]+"kQVB_1")
            self.kQVB_1.setContentsMargins(3, 3, 3, 3)
            self.kQVB_1.setSpacing(2)
            self.verticalLayout_2.addWidget(self.kframe_1)
            bt=QtGui.QPushButton()
            bt.setObjectName(self.buttonList[i]+'_button')
            bt.setStyleSheet("background-color: #595959;height:20px;border-style:inset;border-width:1px;border-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop:0.5 #616161 stop:1 #616161);font-size: 12px;text-align: left;\n"
            "")
            bt.setText(self.buttonText[i]) 
            self.kQVB_1.addWidget(bt)
            bt.clicked.connect(self.signalEmit)
            bt.setIcon(self.kopenicon)
            font = QtGui.QFont()
            font.setPointSize(12)
            bt.setFont(font)
            wd=QtGui.QWidget()
            wd.setObjectName(self.buttonList[i]+'_widget')
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
                    cb=QtGui.QCheckBox()
                    cb.setMinimumSize(QtCore.QSize(0, 20))
                    cb.setObjectName(self.jsDir[self.checkBoxKeys[n]][3]+"."+self.checkBoxKeys[n])
                    cb.setText(self.jsDir[self.checkBoxKeys[n]][2])
                    cb.setChecked(self.jsDir[self.checkBoxKeys[n]][0])
                    wd.addWidget(cb)
                    if not self.jsDir[self.checkBoxKeys[n]][1]=='true':
                        cb.setEnabled(0)
                    self.kcb.append(cb)
        for i in self.kcb:
            if 'common.' in i.objectName():
                pass
            else:
                obj = self.findChild(karray[0],i.objectName())
                if self.jsDir[obj.objectName().split('.')[-1]][1]=='true':
                    obj.setChecked(0)
        for i in self.widgetList:
            if 'common_' in i.objectName():
                pass
            else:
                io=i.objectName()
                io=io.split("_")[0]

                obj = self.findChild(karray[0],i.objectName())
                abj = self.findChild(karray[0],(io+'_button'))
                obj.setVisible(0)
                abj.setIcon(self.kcloseicon)
        for klayout in self.klayoutList:
            kvbspacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            klayout.addItem(kvbspacerItem)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.doIt_Button.clicked.connect(self.kcheckbox)
        self.someone=Communicate()
        self.someone.buttonSignal.connect(self.buttonCmd)
        self.someone.kpreSignal.connect(self.kpresetcommand)
        self.kpresetbuild()

    def kpresetbuild(self):
        ktip=u'N为common（普通），R为rig（设置），C为cluster（角色），M为model（模型），A为animation（动画），F为fx（特效），L为lighting（灯光组装），HQ为华强'
        for i in self.checkBoxKeys:
            try:
                k_presets=self.jsDir[i][5]
                if k_presets:
                    for preset in k_presets:
                        dir_preset={preset:self.jsDir[i][5][preset]}
                        if dir_preset not in self.k_preset:                    
                            self.k_preset.append(dir_preset)
            except:
                pass
        krow=6
        ksize=len(self.k_preset)
        kclosize=ksize/krow
        hass=ksize%krow
        if hass:
            kclosize=kclosize+1
        self.kQVB_3 = QtGui.QVBoxLayout(self.kframe_3)
        self.kQVB_3.setObjectName("kQVB_3")
        self.kQVB_3.setContentsMargins(3, 3, 3, 3)
        self.kQVB_3.setSpacing(2)
        self.k_presetlayout= QtGui.QGridLayout()
        self.kQVB_3.addLayout(self.k_presetlayout)
        pos = [(x, y) for x in range(kclosize) for y in range(krow)]
        for i in range(len(self.k_preset)):
            self.k_presetbutton = QtGui.QPushButton(self.k_preset[i].keys()[0])
            self.k_presetbutton.setObjectName(self.k_preset[i].keys()[0]+'_preset')
            self.k_presetbutton.setToolTip(self.k_preset[i].values()[0])
            try:
                self.k_presetlayout.addWidget(self.k_presetbutton, pos[i][0], pos[i][1])
                self.k_presetbutton.clicked.connect(self.kpresetEmit)
            except:
                pass

    def kpresetEmit(self):
        sender=self.sender()
        self.someone.kpreSignal.emit(sender)

    def kpresetcommand(self,sender):
        cpreset=[]
        for i in self.kcb:
            i.setChecked(0)
        btName = sender.objectName()
        btName=btName.split('_')[0]
        
        for i in self.kcb:
            o=i.objectName()
            o=o.split('.')[-1]
            try:
                k_presets=self.jsDir[o][5]
                for k_preset in k_presets:
                    if btName in k_preset:
                        cpreset.append(i)
            except:
                pass

        karray = []
        karray.append(QtGui.QWidget)
        for c in cpreset:
            precb = self.findChild(karray[0],c.objectName())
            precb.setChecked(1)

    def signalEmit(self):
        sender=self.sender()
        self.someone.buttonSignal.emit(sender)

    def buttonCmd(self,sender):

        btName= sender.objectName()
        parentWd=sender.parent()
        childrenItems=parentWd.children()
        for i in self.widgetList:
            if btName.split("_")[0]+'_widget'==i.objectName() and 'All' not in btName.split('_')[-1]:
                if i.isVisible():
                    i.setVisible(0)
                    sender.setIcon(self.kcloseicon)
                else:
                    i.setVisible(1)
                    sender.setIcon(self.kopenicon)        
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

    def cbcol(self,r,g,b,R, G, B):
        brush = QtGui.QBrush(QtGui.QColor(r,g,b))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(r,g,b))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(R, G, B))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
    def kcheckbox(self):
        karray = []
        karray.append(QtGui.QWidget)
        module={'modeling':'mod','rendering':'ren','fx':'fx','common':'com','animation':'ani','rigging':'rig'}
        self.k_Treturn.clear()
        for cbs in self.kcb:
            self.palette = QtGui.QPalette()
            cbsname=cbs.objectName()
            obj = self.findChild(karray[0],cbsname)
            cbv=cbs.checkState()
            if cbv:
                kprefix=cbsname.split('.')[0]
                ksuffix=cbsname.split('.')[-1]
                new_cbsname=(module[kprefix]+'.'+ksuffix)
                k_gocheck=('fantaTexClass.'+new_cbsname+'()')
                k_checklist=eval(k_gocheck)
                k_update={new_cbsname.split(".")[-1]:k_checklist}
                if k_checklist:
                    self.cbcol(250,0,0,180,0,0)
                    obj.setPalette(self.palette)
                else:
                    self.cbcol(200,200,200,130,130,130)
                    obj.setPalette(self.palette)
                self.k_Treturn.update(k_update)
            else:
                self.cbcol(200,200,200,130,130,130)
                obj.setPalette(self.palette)
        self.k_replyNodes(self.k_Treturn)

    def k_replyNodes(self,k_Treturn):
        ip = socket.gethostbyname(socket.gethostname())
        values ={'data':{'ip':ip,'check_json':self.jsDir,'post_json':{'maya_check':k_Treturn}}}
        jsonValues = urllib.urlencode(values)
        url = "http://10.99.40.240/FTManager/index.php/Home/MayaCheck/index"
        request = urllib2.Request(url=url, data=jsonValues)
        response = urllib2.urlopen(request)
        the_page = response.read()
        the_page = the_page + "?ip=" + ip;
        webbrowser.open(the_page, new=0, autoraise=True)             
                
class loadcheckNode():
    def __init__(self):
        if(mc.window('kcheckNodes',ex=1)):
            mc.deleteUI('kcheckNodes')
        Window=QtGui.QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QtGui.QWidget))
        Window.setObjectName('kcheckNodes')
        window=checkNodes()
        Window.setCentralWidget(window)
        Window.setGeometry(650,127,380,820)
        Window.show()


