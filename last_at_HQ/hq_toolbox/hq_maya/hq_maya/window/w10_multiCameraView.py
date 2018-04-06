# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################
#----------------------------------------
import maya.cmds as cmds

#-------w10_multiCameraView
class w10_multiCameraView(object):
    _menuStr = '''{'del_path':'Window/w10_multiCameraView()',
'icon':':/camera.svg',
'usage':'$fun()',
}
'''
    def __init__(self):
        windowName = 'w10_multiCameraView'
        
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        sceneName = cmds.file(q=True,sn=True,shortName=True).split('.')[0] 
        cmds.window(windowName, title=windowName,w=250, sizeable=0)
        cmds.columnLayout("w10_L01", p=windowName, adj=True)
        cmds.text(p="w10_L01", label='Camera', h=30, align='left')
        cmds.textScrollList( 'w10_uiCameras', p="w10_L01", numberOfRows=8, allowMultiSelection=True, en=0, h=300, width=800, bgc=[0,0,0], showIndexedItem=4)
        cmds.button( 'w10_uiTearOff', p="w10_L01", label="Tear Off Copy", h=40, c=self.w10_tearOff_cmd )
        
        cmds.showWindow(windowName)
    
        self.w10_getCameras_cmds()
    
    
    def w10_tearOff_cmd(self, *args):
        for modPanel in cmds.getPanel(vis=True):
            if cmds.modelPanel (modPanel, exists=True):
                break
        else:
            raise IOError( 'No found modelPanel!')        
        #perspView = cmds.getPanel(withLabel="Persp View")
        curCamera = cmds.modelPanel(modPanel, q=True,camera=True)
        for ca in cmds.textScrollList( 'w10_uiCameras', q=True, si=True):
            cameraShape = cmds.listRelatives( ca, shapes=True, typ='camera', f=True)[0]
            cmds.modelPanel(modPanel, e=True, camera=cameraShape)
            cmds.modelPanel(tearOffCopy=modPanel)    
        cmds.modelEditor(modPanel, e=True, camera=curCamera) 
    
    
    def w10_getCameras_cmds(self, *args):
        cmds.textScrollList('w10_uiCameras', e=True, en=True, removeAll=True)
        for ca in cmds.ls(cameras=True):
            camPapa = cmds.listRelatives( ca, parent=True, f=True)
            cmds.textScrollList('w10_uiCameras', e=True, append=camPapa)
    
    #-------w10 End