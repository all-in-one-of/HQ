import PyQt4.QtCore as QtCore,PyQt4.QtGui as QtGui
import sys
path='E:/program/edward/python'
if not path in sys.path:
    sys.path.append(path)

#import maya.cmds as cmds
import edo_riggingToolMainUI.edo_riggingToolMainUIDesign as RTMUD
#import edo_common
import PyQt4.uic as uic

#reload(RTMUD)
class edo_riggingToolMainUI(RTMUD.Ui_edo_riggingToolMainUI):
    def setupUi(self, edo_riggingToolMainUI):
        RTMUD.Ui_edo_riggingToolMainUI.setupUi(self,edo_riggingToolMainUI)
        #self.basicCtrl_bt.setText(_fromUtf8("aaaaa"))
        self.IkFkChainCtrlTool_Bt.clicked.connect(self.IkFkChainCtrlTool_Bt_cmd_)
        self.blendshapeTool_Bt.clicked.connect(self.blendshapeTool_Bt_cmd_)
        
    def IkFkChainCtrlTool_Bt_cmd_(self):
        print 'opening IkFkChainCtrlTool...'
        import edo_buildControlerFromSkeletonUI.showUi as edo_buildControlerFromSkeletonUIShowUi
        reload(edo_buildControlerFromSkeletonUIShowUi)
        
    def blendshapeTool_Bt_cmd_(self):
        print 'opening blendshapeTool...'
        import edo_autoConnectBlendshapesInbetweenUI.showUi as edo_autoConnectBlendshapesInbetweenUIShowUi
        reload(edo_autoConnectBlendshapesInbetweenUIShowUi)


app=QtGui.QApplication(sys.argv)
#if cmds.window('edo_riggingToolMainUI',q=1,ex=1):
#    cmds.deleteUI('edo_riggingToolMainUI')
#mayawindow=edo_common.edo_getMayaWindow()
ui=edo_riggingToolMainUI()
qtwindow=QtGui.QMainWindow()
ui.setupUi(qtwindow)
qtwindow.show()
sys.exit(app.exec_())
