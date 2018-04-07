import PyQt4.QtCore as QtCore,PyQt4.QtGui as QtGui
import maya.cmds as cmds
import edo_riggingToolMainUI.edo_riggingToolMainUIDesign as RTMUD
import edo_common
import headfile as headfile
from edo_EasyCtrlPlaneUI.edo_EasyCtrlPlaneUI import *


#reload(RTMUD)
class edo_riggingToolMainUI(RTMUD.Ui_edo_riggingToolMainUI):
    def setupUi(self, edo_riggingToolMainUI):
        RTMUD.Ui_edo_riggingToolMainUI.setupUi(self,edo_riggingToolMainUI)
        #self.basicCtrl_bt.setText(_fromUtf8("aaaaa"))
        self.IkFkChainCtrlTool_Bt.clicked.connect(self.IkFkChainCtrlTool_Bt_cmd_)
        self.blendshapeTool_Bt.clicked.connect(self.blendshapeTool_Bt_cmd_)
        self.riggingCtrlPanel_Bt.clicked.connect(self.riggingCtrlPanel_Bt_cmd_)
        self.riggingFileControler_Bt.clicked.connect(self.riggingFileControler_Bt_cmd_)
        self.BodyRigTool_Bt.clicked.connect(self.BodyRigTool_Bt_cmd_)
        
    def riggingFileControler_Bt_cmd_(self):
        print 'opening riggingFileControler...'
        import edo_animationSceneSpeedControlUI.showUi as edo_animationSceneSpeedControlUIShowUi
        reload(edo_animationSceneSpeedControlUIShowUi)
       
    def BodyRigTool_Bt_cmd_(self):
        print 'opening bodyRigTools...'
        bodyrigpath=headfile.__file__.replace('headfile.py','RIG/UI/MainUI.py').replace('\\','/')
        execfile(bodyrigpath)
        SK_IDMTRigUI()
        
    def IkFkChainCtrlTool_Bt_cmd_(self):
        print 'opening IkFkChainCtrlTool...'
        import edo_buildControlerFromSkeletonUI.showUi as edo_buildControlerFromSkeletonUIShowUi
        reload(edo_buildControlerFromSkeletonUIShowUi)
        
    def blendshapeTool_Bt_cmd_(self):
        print 'opening blendshapeTool...'
        import edo_autoConnectBlendshapesInbetweenUI.showUi as edo_autoConnectBlendshapesInbetweenUIShowUi
        reload(edo_autoConnectBlendshapesInbetweenUIShowUi)

    def riggingCtrlPanel_Bt_cmd_(self):
        print 'opening rigging ctrl panel...'
        edo_EasyCtrlPlaneUI()

if cmds.window('edo_riggingToolMainUI',q=1,ex=1):
    cmds.deleteUI('edo_riggingToolMainUI')
mayawindow=edo_common.edo_getMayaWindow()
ui=edo_riggingToolMainUI()
qtwindow=QtGui.QMainWindow(mayawindow)
ui.setupUi(qtwindow)
qtwindow.show()