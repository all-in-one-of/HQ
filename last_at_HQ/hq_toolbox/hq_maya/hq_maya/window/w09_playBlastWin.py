# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import os

#---------w09 Start
class w09_playBlastWin(object):
    _menuStr = '''{'path':'Window/w09_playBlastWin()',
'icon':':/timeplay.png',
'tip' : '拍屏，自动绽放防止切屏',
'html':True,
'usage':'$fun()',
}
'''
    def __init__(self):
        windowName = 'w09_pb'
        
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        sceneName = cmds.file(q=True,sn=True,shortName=True).split('.')[0]
        cmds.window(windowName, title="w09_playBlastWin",w=450, sizeable=1)
        cmds.columnLayout("w09_L01", p=windowName, adj=True)
        #cmds.floatSliderGrp( 'w09_uiScale', p="w09_L01", field=True, label="Scale", h=50, cw=([1,50],[2, 50], [3, 300]), minValue=.1, maxValue=1,value=1, pre=2)
        #cmds.textFieldGrp( 'w09_uiFiles', p="w09_L01", label='Files  ', cw=([1,50],[2, 340]), h=40,en=False,text=sceneName)
        cmds.textScrollList( 'w09_uiCameras', p="w09_L01", numberOfRows=8, allowMultiSelection=True, en=0, h=300, bgc=[.2,.2,.2], showIndexedItem=4)
        cmds.button( 'w09_uiGetCameras', p="w09_L01", label="Get Cameras", h=40, c=self.w09_getCameras_cmds )
        cmds.separator( p="w09_L01", st="double", h=15)
        cmds.button( 'w09_uiPbutton', p="w09_L01", label="Playblast", h=40, c=self.w09_playblast_cmd )
        cmds.showWindow(windowName)
        self.w09_getCameras_cmds()
    
    
    def w09_playblast_cmd(self, *args):
        #Clamp resolution to view port
        import maya.OpenMayaUI as omui
        curView = omui.M3dView.active3dView()
        portWidth =  curView.portWidth()
        portHeight = curView.portHeight()    
        resWidth = cmds.getAttr( 'defaultResolution.width' )
        resHeight = cmds.getAttr( 'defaultResolution.height' )
        resAspect = float(resWidth)/resHeight
        if resWidth>portWidth or resHeight>portHeight:
            if portWidth<portHeight:
                resWidth, resHeight = portWdith, int(portWidth/resAspect)
            else: #protHeight<portWidth
                resWidth, resHeight = int(portHeight*resAspect), portHeight
        
        #Get model panel
        for mPanel in cmds.getPanel(vis=True):
            if cmds.modelPanel(mPanel, exists=True):
                break
        else:
            raise IOError( 'No found modelPanel!' )
         
        sceneName = cmds.file(q=True,sn=True,shortName=True).split('.')[0]    
        for ca in cmds.textScrollList( 'w09_uiCameras', q=True, si=True):
            camShortName = ca.split('|')[-1].replace(":", '_')   
            #Set Model panel camera         
            cameraShape = cmds.listRelatives( ca, shapes=True, typ='camera', f=True)[0]
            cmds.modelPanel(mPanel, e=True, camera=cameraShape)
            cmds.camera(cameraShape, e=True, displayResolution=False, displayGateMask=False, displayFilmGate=False)
    
            filenameV =  'playblast/%s/%s/%s'%(sceneName,camShortName, camShortName);        
            cmds.playblast( format='iff', filename=filenameV, sequenceTime=False, viewer=False, clearCache=True,  showOrnaments=True, fp=4, percent=100, compression="jpg", quality=100, wh=[resWidth, resHeight] )
        imDir = cmds.workspace(q=True,rd=True)
        imDir = os.path.join( imDir, 'images/playblast/%s'%(sceneName)  )
        if os.path.exists(imDir):        
            os.startfile( imDir )
    
    def w09_getCameras_cmds(self, *args):
        cmds.textScrollList('w09_uiCameras', e=True, en=True, removeAll=True)    
        for ca in cmds.ls(cameras=True):
            camPapa = cmds.listRelatives( ca, parent=True, f=True)
            cmds.textScrollList('w09_uiCameras', e=True, append=camPapa)
    #---------------w09 End
