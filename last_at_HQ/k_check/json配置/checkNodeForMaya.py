#!/usr/bin/env python
#coding=cp936
#coding=utf-8
__author__ = 'huangshuai,dengtao,xusijian'
try:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from shiboken import wrapInstance 
except:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance 

import maya.cmds as mc
from maya import OpenMayaUI as omui
import sys
#import fantabox
#????1¤3ì????
path='O:/hq_tool/Maya/hq_maya/scripts/fantabox/'
#path ='D:/'

from k_checkNodesWidget import Ui_checkNodesWindow
import checkNodeForMayaReplyWin
import json 
import socket
import urllib
import urllib2
import webbrowser
import fantabox
from functools import partial
import getpass


class Communicate(QObject):
        buttonSignal=Signal(QWidget)
        kpreSignal=Signal(QWidget)

class checkNodes(Ui_checkNodesWindow,QMainWindow):
    def __init__(self,parent=None):
        super(checkNodes,self).__init__()
        self.setupUi(self)
        self.palette = QPalette()
        self.karray = QWidget
        self.scrollArea.setWidgetResizable(True)
        self.module={u'modeling':u'mod',u'rendering':u'ren',u'fx':u'fx',u'common':u'com',u'animation':u'ani',u'rigging':u'rig'}
        self.btnnum=-1
        self.kcb=[]
        self.k_preset=[]
        self.modLists=[]
        self.widgetList=[]
        self.klayoutList=[]
        self.k_Treturn={}
        self.close_Button.clicked.connect(self.kclose)
        self.jsfile = json.loads(open(path+'FantaBox_mayacheck.json').read(),encoding='gbk')
        self.ck_presets=self.jsfile["btndict"]
        self.jsfile.pop("btndict")
        self.jsDir=self.jsfile
        self.ck_mods=self.jsDir.keys()
        self.modLists = [u"common",u"modeling",u"rigging",u"animation",u"fx",u"rendering"]

        self.kopenicon = QIcon()
        self.kopenicon.addPixmap(QPixmap(":/newPrefix/icon/kopen.png"), QIcon.Normal,QIcon.Off)
        self.kcloseicon = QIcon()
        self.kcloseicon.addPixmap(QPixmap(":/newPrefix/icon/kclose.png"), QIcon.Normal, QIcon.Off)
        
        for i in range(len(self.modLists)):
            self.kframe_1 = QFrame(self.scrollAreaWidgetContents)
            self.kframe_1.setFrameShape(QFrame.Box)
            self.kframe_1.setFrameShadow(QFrame.Raised)
            self.kframe_1.setObjectName(self.modLists[i]+"kframe_1") 
            
            self.kQVB_1 = QVBoxLayout(self.kframe_1)
            self.kQVB_1.setObjectName(self.modLists[i]+"kQVB_1")
            self.kQVB_1.setContentsMargins(3, 3, 3, 3)
            self.kQVB_1.setSpacing(2)
            self.verticalLayout_2.addWidget(self.kframe_1)
            
            modPushbt=QPushButton()
            modPushbt.setObjectName(self.modLists[i]+'_button')
            modPushbt.setStyleSheet("background-color: #595959;height:20px;border-style:inset;border-width:1px;border-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop:0.5 #616161 stop:1 #616161);font-size: 12px;text-align: left;\n"
            "")
            modPushbt.setText(self.modLists[i]) 
            modPushbt.clicked.connect(self.signalEmit)
            modPushbt.setIcon(self.kopenicon)
            modPushbt.setFont(QFont().setPointSize(12))
            self.kQVB_1.addWidget(modPushbt)
            
            wd=QWidget()  
            wd.setObjectName(self.modLists[i]+'_widget')
            self.kQVB_1.addWidget(wd)
            self.khorizontalLayout = QHBoxLayout(wd)
            self.khorizontalLayout.setObjectName('khorizontalLayout')
            self.khorizontalLayout.setContentsMargins(0, 0, 0, 0) 
            self.k_frame=QFrame(wd)
            self.k_frame.setObjectName("k_frame")
            self.k_frame.setFrameShape(QFrame.Box) 
            self.k_frame.setFrameShadow(QFrame.Sunken)
            self.khorizontalLayout.addWidget(self.k_frame)
            self.kverticalLayout = QVBoxLayout(self.k_frame)
            self.kverticalLayout.setObjectName(self.modLists[i]+"_kverticalLayout")

            selectAllBt = self.selectbtn(self.modLists[i]+'_selAll',u'全选',wd)
            cancelAllBt = self.selectbtn(self.modLists[i]+'_canAll',u'重置',wd)
            kspacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            
            self.kHbLayout = QHBoxLayout()
            self.kHbLayout.setObjectName(self.modLists[i]+"_kHbLayout")
            self.kHbLayout.addWidget(selectAllBt)
            self.kHbLayout.addWidget(cancelAllBt)
            self.kHbLayout.addItem(kspacerItem)
            self.kverticalLayout.addLayout(self.kHbLayout)
            self.widgetList.append(wd)
            self.klayoutList.append(self.kverticalLayout)
            
        for n in range(len(self.ck_mods)):
            tabs= self.jsDir.get(self.ck_mods[n])
            for tab in tabs:
                for wd in self.klayoutList:
                    if wd.objectName()==self.ck_mods[n]+'_kverticalLayout':
                        self.cbhorizontalLayout = QHBoxLayout()
                        self.cbhorizontalLayout.setObjectName(tab+"_cbhorizontalLayout")
                        
                        wd.addLayout(self.cbhorizontalLayout)
                        cb=QCheckBox()
                        cb.setMinimumSize(QSize(0, 20))
                        cb.setObjectName(self.ck_mods[n]+"."+tab)
                        cb.setText(tabs[tab][0])
                        cb.setChecked(0)
                        selbtns=QPushButton()
                        selbtns.setObjectName(self.modLists[i]+'_selAll')
                        selbtns.setText(u'选择')
                        selbtns.setGeometry(0,0,20,20)
                        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
                        sizePolicy.setHorizontalStretch(0)
                        sizePolicy.setVerticalStretch(0)
                        sizePolicy.setHeightForWidth(selbtns.sizePolicy().hasHeightForWidth())
                        selbtns.setSizePolicy(sizePolicy)
                        selbtns.setMinimumSize(QSize(40, 20))
                        selbtns.clicked.connect(partial(self.selectcommand,self.ck_mods[n]+"."+tab))
                        self.cbhorizontalLayout.addWidget(cb)
                        self.cbhorizontalLayout.addWidget(selbtns)
                        cb.setEnabled(1)
                        self.kcb.append(cb)
        for i in self.widgetList:
            if 'common_' in i.objectName():
                pass
            else:
                io=i.objectName().split("_")[0]
                obj = self.findChild(self.karray,i.objectName())
                obj.setVisible(0)
                abj = self.findChild(self.karray,io+'_button')
                abj.setIcon(self.kcloseicon)
        for klayout in self.klayoutList:
            kvbspacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            klayout.addItem(kvbspacerItem)
        spacerItem = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.doIt_Button.clicked.connect(self.kcheckbox)
        self.someone=Communicate()
        self.someone.buttonSignal.connect(self.buttonCmd)
        self.someone.kpreSignal.connect(self.kpresetcommand)
        self.kpresetbuild()
        
    def selectbtn(self,objname,cnName,pawins):
        selbtns=QPushButton()
        selbtns.setObjectName(objname)
        selbtns.setText(cnName)
        selbtns.setGeometry(0,0,65,10)
        selbtns.setMinimumSize(QSize(65, 10))
        selbtns.setParent(pawins)
        selbtns.clicked.connect(self.signalEmit)
        return selbtns
        
    def kpresetbuild(self):
        jsBtnsInt =[int(a) for a in self.ck_presets.keys()]
        jsBtns =  list(set(jsBtnsInt))
        for jsBtn in jsBtns:
            self.k_preset.insert(jsBtn,self.ck_presets.get(str(jsBtn)))

        kclosize=len(self.k_preset)/6
        hass=len(self.k_preset)%6
        if hass:
            kclosize=kclosize+1
        self.kQVB_3 = QVBoxLayout(self.kframe_3)
        self.kQVB_3.setObjectName("kQVB_3")
        self.kQVB_3.setContentsMargins(3, 3, 3, 3)
        self.kQVB_3.setSpacing(2)
        self.k_presetlayout= QGridLayout()
        self.kQVB_3.addLayout(self.k_presetlayout)
        pos = [(x, y) for x in range(kclosize) for y in range(6)]
        for i in range(len(self.ck_presets)):
            self.k_presetbutton = QPushButton(self.k_preset[i])
            self.k_presetbutton.setObjectName(str(i)+'_preset')
            try:
                self.k_presetlayout.addWidget(self.k_presetbutton, pos[i][0], pos[i][1])
                self.k_presetbutton.clicked.connect(self.kpresetEmit)
            except:
                pass
    def kpresetEmit(self):
        self.someone.kpreSignal.emit(self.sender())
        


    def cbcol(self,r,g,b,R, G, B):
        brush = QBrush(QColor(r,g,b))
        brush.setStyle(Qt.SolidPattern)
        self.palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(r,g,b))
        brush.setStyle(Qt.SolidPattern)
        self.palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(R, G, B))
        brush.setStyle(Qt.SolidPattern)
        self.palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
    def flatten(self,ll):
        aa=[]
        if isinstance(ll, list):
            for i in ll:
                for element in self.flatten(i):
                    yield element
        else:
            yield ll
    def selectcommand(self,commandName):
        page =  self.jsDir[commandName.split(".")[0]][commandName.split(".")[1]][2]
        try:
            k_checklist = eval("fantabox."+str(commandName)+"()")
        except:
            k_checklist = eval("fantabox."+str(commandName)+"(-1)")
        sels = list(self.flatten(k_checklist))
        if sels!=[]:
            mc.select(cl=1)
            for sel in sels:
                try:
                    mc.select(sel,add=1)
                except:
                    mc.warning(sel)
            webbrowser.open_new_tab(page)

        

    def kpresetcommand(self,sender):
        cpreset={}
        
        for i in self.kcb:
            i.setChecked(0)
            i.setEnabled(1)
        self.btnnum=sender.objectName().split('_')[0]
        for i in self.kcb:
            modname= i.objectName().split('.')
            resetlists=  self.jsDir.get(modname[0])[modname[1]][1]
            for resetlist in resetlists:
                if int(resetlist[0])==int(self.btnnum):
                    cpreset[i]=resetlist[1]
                    
        for c in cpreset:
            precb = self.findChild(self.karray,c.objectName())
            precb.setChecked(1)
            if cpreset[c]:
                precb.setEnabled(1)
            else:
                precb.setEnabled(0)
            self.cbcol(200,200,200,130,130,130)
            precb.setPalette(self.palette) 

    def signalEmit(self):
        self.someone.buttonSignal.emit(self.sender())
        
    def btnselcmd(self,btcmdName,childrenItems):
        if btcmdName=='selAll':
            cmdsvalues = True
        else:
            cmdsvalues = False
        for n in childrenItems:
            if n.metaObject().className()=='QCheckBox':
                if n.isChecked ()!=cmdsvalues:
                    n.setEnabled(1)
                    n.setChecked(cmdsvalues)
                    self.cbcol(200,200,200,130,130,130)
                    n.setPalette(self.palette) 
                    
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
        self.btnselcmd(btName.split('_')[-1],childrenItems) 

    def kclose(self):
        mc.deleteUI('kcheckNodes')
        
    def kcheckbox(self):
        self.k_Treturn.clear() 
        for cbs in self.kcb:
            cbsname=cbs.objectName()
            obj = self.findChild(self.karray,cbsname)
            cbv=cbs.checkState()
            if cbv:
                kprefix=cbsname.split('.')[0]
                ksuffix=cbsname.split('.')[-1]
                new_cbsname=(self.module[kprefix]+'.'+ksuffix)
                k_gocheck=('fantabox.'+new_cbsname+'()')
                try:
                    k_checklist=eval(k_gocheck)
                except:
                    k_gocheck=('fantabox.'+new_cbsname+'('+str(self.btnnum)+')')
                    k_checklist = eval(str(k_gocheck))
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
        username =  getpass.getuser()
        mayajsonpath =r"//10.99.40.240/MayaJson/"+str(username)+r".json"
        check_values ={'data':{'ip':ip,'check_json':self.jsDir,'post_json':{'maya_check':k_Treturn}}}
        emptylists= [a for a in k_Treturn.values() if a!=[]]
        if emptylists !=[]:
            dd = json.dumps( check_values, indent=4,encoding='GBK')
            file = open(mayajsonpath, 'w')
            file.write(dd)
            file.close()
            url = "http://10.99.40.240/FTManager/index.php/API/MayaCheck/index?path="+mayajsonpath
            webbrowser.open(url, new=1, autoraise=True) 
        else:
            mc.confirmDialog( title=u"mayacheck", message=u'恭喜你，检查结果符合规范！', button=['确定'], defaultButton='Yes', cancelButton='No', dismissString='No')
from fantabox.common.k_check_unPlugin import *
def loadcheckNode():
    try:
        k_check_unPlugin()
    except:
        print "wrong"
    if(mc.window('kcheckNodes',ex=1)):
        mc.deleteUI('kcheckNodes')
    Window=QMainWindow(wrapInstance(long(omui.MQtUtil.mainWindow()), QWidget))
    Window.setObjectName('kcheckNodes')
    Window.setWindowTitle(u'提交规范检查工具')
    window=checkNodes()
    Window.setCentralWidget(window)
    Window.setGeometry(650,127,380,820)
    Window.show()

if __name__=="__main__":
    loadcheckNode()