#import edo_cutPolygonsToolUI.showUi as showUi
#reload(ESWIOCMD)
import PyQt4.QtCore as QtCore,PyQt4.QtGui as QtGui
import maya.cmds as cmds
import maya.mel as mel
import edo_common
import edo_skinWeightIoUI.edo_skinWeightIoUI as ESWIOUI
import edo_skinWeightIoUI.edo_skinWeighIoCmd as ESWIOCMD
global fobj

class edo_skinWeightIoUI(ESWIOUI.Ui_edo_skinWeightIoUI):
    def setupUi(self,edo_skinWeightIoUI):
        ESWIOUI.Ui_edo_skinWeightIoUI.setupUi(self,edo_skinWeightIoUI)
        self.source_bt.clicked.connect(self.edo_loadSelectListToSList_)
        self.direct_bt.clicked.connect(self.edo_loadSelectListToDList_)
        self.addTemp_bt.clicked.connect(self.edo_addTemplateTo_)
        self.saveTemp_bt.clicked.connect(self.edo_saveTemplate_)
        self.sourseInfluence.itemSelectionChanged.connect(self.edo_SlistSelectChanged_)
        self.directInfluence.itemSelectionChanged.connect(self.edo_DlistSelectChanged_)
        self.ex_bt.clicked.connect(ESWIOCMD.edo_exPolyWeights)
        self.im_bt.clicked.connect(ESWIOCMD.edo_imPolyWeights)
        self.md_bt.clicked.connect(self.edo_modifySkinWeightData)

    def edo_modifySkinWeightData(self):
        print 'edo_modifySkinWeightData'
        datas=''
        datas=str(self.sw_line.text())
        print datas
        if datas=='':
            return False
        temps=''
        temps=str(self.rp_line.text())
        if temps=='':
            return False
        ESWIOCMD.edo_modifySkinWeightData(datas,temps)
        
    def edo_loadSelectListToSList_(self):
        print 'load to sourseInfluence'
        sels=cmds.ls(sl=1)
        self.sourseInfluence.clear()
        #tx=''
        #for sel in sels:
            #sel=sels[0]
        #    tx=tx+sel+':'
        #tx=tx[:-1]
        self.sourseInfluence.addItems(sels)
        print sels
        
        
    def edo_loadSelectListToDList_(self):
        print 'load to directInfluence'
        sels=cmds.ls(sl=1)
        self.directInfluence.clear()
        self.directInfluence.addItem(sels[0])
        print sels[0]
    
    def edo_addTemplateTo_(self):
        global fobj
        print 'add the template'
        if fobj==None:
            path=''
            paths=cmds.fileDialog2(fileFilter='*.skt',dialogStyle=2)
            if paths:
                path=paths[0]
            if path=='':
                return False
            fobj=open(path,'w')
        sl=self.edo_callbackListAsStr(self.sourseInfluence)
        dl=self.edo_callbackListAsStr(self.directInfluence)
        tx=sl[:-1]+' '+dl[:-1]+'\n'
        print tx
        fobj.write(tx)
        
    def edo_callbackListAsStr(self,list):
        #list=ui.sourseInfluence
        c=list.count()
        tx=''
        for i in range(0,c):
            #i=0
            it=list.item(i)
            tx=tx+str(it.text())+':'
        return tx
    
    def edo_saveTemplate_(self):
        global fobj
        print 'save the template'
        if not fobj==None:
            fobj.close()
        fobj=None
        
    def edo_SlistSelectChanged_(self):
        #cmds.select(cl=1)
        sels=self.edo_findSelectItems_(self.sourseInfluence)
        #sels=ui.edo_findSelectItems_(ui.sourseInfluence)
        if sels:
            cmds.select(sels,r=1)
        print 'change selected...'
        
    def edo_DlistSelectChanged_(self):
        #cmds.select(cl=1)
        sels=self.edo_findSelectItems_(self.directInfluence)
        #sels=ui.edo_findSelectItems_(ui.sourseInfluence)
        if sels:
            cmds.select(sels,r=1)
        print 'change selected...'
        
    def edo_findSelectItems_(self,list):
        cw=list.count()
        print cw
        sels=[]
        for c in range(cw):    
            it=list.item(c)
            sl=list.isItemSelected(it)
            if sl==True:
                sels.append(str(it.text()))
        print sels
        return sels
        
if cmds.window('edo_skinWeightIoUI',q=1,ex=1):
    cmds.deleteUI('edo_skinWeightIoUI')
mayawindow=edo_common.edo_getMayaWindow()
ui=edo_skinWeightIoUI()
qtwindow=QtGui.QMainWindow(mayawindow)
ui.setupUi(qtwindow)
qtwindow.show()