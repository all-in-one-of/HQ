# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################


import maya.cmds as cmds
import maya.mel as mel
import os, re
from functools import partial

import maya.cmds as cmds
import maya.mel as mel
import os, re
#----------------------------w04 start-----------------------------------------
#imagePath = cmds.workspace(q =True, rootDirectory=True)+'images'
#renderLayer = cmds.editRenderLayerGlobals( q=True, currentRenderLayer=True)
#renEngine = cmds.getAttr("defaultRenderGlobals.ren")
#cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
#resWidth = cmds.getAttr("defaultResolution.width")
#resHeight = cmds.getAttr("defaultResolution.height")
#ifprefix = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
#paddingzero = cmds.getAttr ("defaultRenderGlobals.extensionPadding")
#startframe = cmds.getAttr("defaultRenderGlobals.startFrame")
#endframe = cmds.getAttr("defaultRenderGlobals.endFrame")
#camrenderable = cmds.getAttr("frontShape.renderable")


class w04_renderingWin(object):
    _menuStr = '''{'path':'Rendering/Render/w04_renderingWin()',
'icon':':/render.png',
'tip' : '前台拍屏渲染',
'html':True,
'usage':'$fun()',
}
'''
    def __init__(self):
        if cmds.window("w04", q=True, exists=True):
            cmds.deleteUI( "w04")
        
        cmds.window('w04', title="w04_Rendering", tbm=False, widthHeight=(410, 1000), sizeable=True)
        cmds.columnLayout( 'w04_L01', p='w04' )
    
    
        self.jobNum = cmds.scriptJob( e= ["renderLayerManagerChange", self.w04_updataUI ], protected=True)
        cmds.rowColumnLayout('w04_rcLayout02', p='w04_L01', numberOfColumns=3, columnWidth=[(1,150), (2,150), (3,100)], columnAlign=[(1,'left'), (2,'left'),(3,'right')] )
        cmds.checkBox('w04_pbStart', p='w04_rcLayout02', label='Play from start frame', h=50, v=False)
        cmds.button('w04_renderButton', p='w04_rcLayout02', label='Render', command=self.w04_renderButtonCommand      )
        cmds.button('w04_colseButton', p='w04_rcLayout02', label='Close',command= self.close    )
        #cmds.textFieldGrp('w04_filename', p='w04_L01', label='File Name', w=400, columnWidth=[10,300], editable=False)
    
        cmds.text( 'w04_filename', p='w04_L01', label='File name:',  align='left', h=30, w=410, font="boldLabelFont" )
    
        cmds.rowColumnLayout('w04_rcLyout', p='w04_L01', numberOfColumns=2, columnWidth=[(1,100), (2,280)] )
        cmds.text('w04_curLayer', p='w04_rcLyout', label='Current Layer')
        cmds.progressBar('w04_pbCurLay', p='w04_rcLyout')
    
        cmds.text('w04_all', p='w04_rcLyout', label='Total')
        cmds.progressBar('w04_pbTotal', p='w04_rcLyout')
    
    
        cmds.text('w04_all',p='w04_L01', label='Only:  gif,  pic,  rla,  tif,  tiff16,  als,  iff,  jpg,  eps,  iff16,\n  cin,  yuv,  sgi,  tga,  psd,  png,  dds,  PSDLayered\nDefault:    tga',
                    font="boldLabelFont", w=410, h=60, align='center' )
    
        cmds.textFieldGrp( "w04_Imageformat", p='w04_L01', label='Image format', text=str(self.w04_getExtension())[1:-1], editable=False)
    
        cmds.textFieldGrp( 'w04_path', p='w04_L01', label='Path:',                  text=cmds.workspace(q =True, rootDirectory=True)+'images', editable=False)
        cmds.textFieldGrp( "w04_RenderLayer", p='w04_L01', label='Render Layer',    text=cmds.editRenderLayerGlobals( q=True, currentRenderLayer=True), editable=False)
        cmds.textFieldGrp( "w04_RenderUsing", p='w04_L01', label='Render Using',    text=cmds.getAttr("defaultRenderGlobals.ren"),                      editable=False)
        cmds.textFieldGrp( "w04_RenderableCams",      p='w04_L01', label='Renderable Cameras',
                           text=str(self.w04_renderableCams())[1:-1].replace("u'", '').replace("'", ''),
                           editable=False)
    
        cmds.textFieldGrp( "w04_Extension", p='w04_L01', label='Frame/Animation ext',   text=self.w04_animationType(), editable=False)
        cmds.textFieldGrp( "w04_paddingzero", p='w04_L01', label='Frame padding',       text=cmds.getAttr ("defaultRenderGlobals.extensionPadding"), editable=False)
        #cameraList
        cmds.textFieldGrp( "w04_imageSize", p='w04_L01', label='ImageSize',
                           text='%s*%s'%(  cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")  ),
                           editable=False)
    
        cmds.radioButtonGrp( 'w04_renderingModel', p='w04_L01', labelArray2=['Frame By Frame', 'Layer By Layer'], height=25, numberOfRadioButtons=2, select=1 )
    
    
        cmds.rowColumnLayout( 'w04_uiFramRangeLay', p='w04_L01', numberOfColumns=2)
        cmds.checkBox('w04_setFrameRange', p='w04_uiFramRangeLay', label='Set Frame Range', al='right', h=30, v=False, cc=self.w04_updataUI )
        cmds.radioButtonGrp( 'w04_uiFrameRangeStyle', p='w04_uiFramRangeLay', cw2=(100, 110), labelArray2=['Start-End','Frame Segments'], numberOfRadioButtons=2,\
                            select=1, en=False, cc=self.w04_updataUI )
    
        cmds.rowColumnLayout( 'w04_uiFramRangeLay_02', p='w04_L01', numberOfColumns=3)
        cmds.intFieldGrp( "w04_startFrame", p='w04_uiFramRangeLay_02', label='Start frame', cw2=(75,45), value1=cmds.getAttr("defaultRenderGlobals.startFrame"), en=False)
        cmds.intFieldGrp( "w04_endFrame", p='w04_uiFramRangeLay_02',   label='End frame', cw2=(75,45), value1=cmds.getAttr("defaultRenderGlobals.endFrame"), en=False)
        cmds.intFieldGrp( "w04_byFrame", p='w04_uiFramRangeLay_02',   label='By frame', cw2=(75,45), value1=1, enable=False)
        
        cmds.frameLayout('w04_uiFrameSegLayout', p='w04_L01', label="Frame segments", w=410, collapsable=True,  borderStyle="in", collapse=True)
        cmds.scrollField( 'w04_uiFrameSegments', p='w04_uiFrameSegLayout', editable=True,  h=200, wordWrap=False, en=False,\
                            text= '%d-%d'%( cmds.getAttr("defaultRenderGlobals.startFrame"), cmds.getAttr("defaultRenderGlobals.endFrame") ),\
                            cc=self.w04_uiFrameSegments_cmd )
        cmds.checkBox('w04_closeMaya', p='w04_L01', label='Close Maya', h=25, v=False)
        cmds.checkBox('w04_shutdown', p='w04_L01', label='Shutdown', h=25, v=False)
        
        cmds.showWindow( "w04" )
        #cmds.RenderViewWindow()
    
    def close(self, *args):
        cmds.scriptJob( kill=self.jobNum, force=True)
        cmds.deleteUI('w04' )
    
    def w04_renderableCams(self, *args):
        cameras = []
        for camShape in cmds.ls(type='camera', l=True):
            if cmds.getAttr(camShape+'.renderable'):
                cameras.append(cmds.listRelatives(camShape, p=True)[0])
        return cameras
    
    #str(w04_renderableCams())[1:-1].replace("u'", '').replace("'", '')
    
    
    def w04_animationType(self, *args):
        cmds.setAttr("defaultRenderGlobals.animation", True)
        if cmds.getAttr("defaultRenderGlobals.animation"):
            return "name.#.ext"
    
    
    
    def w04_getExtension(self, *args):
        formats = {0:('GIF', 'gif'),           1:('SoftImage', 'pic'),    2:('RLA', 'rla'),     3:('Tiff','tif'),                     4:('Tiff16','tif'),     5:('SGI','sgi'),
                    6:('Alias PIX','als'),     7:('Maya IFF','iff'),     8:('JPEG', 'jpg'),    9:('Encapsulated Postscript','eps'),   10:('Maya16 IFF','iff'),
                    11:('Cineon', 'cin'),      12:('Quantel','yuv'),     13:('SGI16','sgi'),   19:('Targa','tga'),                   20:('Windows Bitmap','bmp'),
                    31:('PSD','psd'),          32:('PNG','png'),        35:('DDS','dds'),     36:('PSD Layered','psd')
                    }
        extIndex = cmds.getAttr("defaultRenderGlobals.imageFormat")
        if formats.has_key(extIndex):
            extension = formats[extIndex]
        else:
            extension = formats[19]
        return extension
    
    
    
    
    def w04_updataUI(self, *args):
        cmds.text( 'w04_filename', e=True)
        cmds.textFieldGrp( "w04_Imageformat",   e=True, text=str(self.w04_getExtension())[1:-1])
        cmds.textFieldGrp( 'w04_path',          e=True, text=cmds.workspace(q =True, rootDirectory=True)+'images' )
        cmds.textFieldGrp( "w04_RenderLayer",   e=True, text=cmds.editRenderLayerGlobals( q=True, currentRenderLayer=True) )
        cmds.textFieldGrp( "w04_RenderUsing",   e=True, text=cmds.getAttr("defaultRenderGlobals.ren") )
        cmds.textFieldGrp( "w04_RenderableCams",e=True, text=str(self.w04_renderableCams())[1:-1].replace("u'", '').replace("'", '')   )
        cmds.textFieldGrp( "w04_Extension",     e=True, text=self.w04_animationType() )
        cmds.textFieldGrp( "w04_paddingzero",   e=True, text=str(cmds.getAttr ("defaultRenderGlobals.extensionPadding") )  )
        cmds.textFieldGrp( "w04_imageSize",     e=True, text='%s*%s'%(  cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")  ) )
        enValue = cmds.checkBox('w04_setFrameRange',    q=True, v=True)
    
        cmds.radioButtonGrp( 'w04_uiFrameRangeStyle', e=True, en=enValue)
        if cmds.radioButtonGrp( 'w04_uiFrameRangeStyle', q=True, select=True)==1 and cmds.checkBox('w04_setFrameRange', q=True, v=True):
            ranV, segV = True, False
        else:
            ranV, segV = False, True
    
        cmds.intFieldGrp( "w04_startFrame",    e=True,  en=ranV  )
        cmds.intFieldGrp( "w04_endFrame",      e=True,  en=ranV  )
        cmds.intFieldGrp( "w04_byFrame",       e=True,  en=ranV)
    
        cmds.frameLayout('w04_uiFrameSegLayout', e=True, collapse=not segV)
        cmds.scrollField( 'w04_uiFrameSegments', e=True, en=segV )
    
        self.w04_uiFrameSegments_cmd()
    
    
    
    
    def w04_uiFrameSegments_cmd(self, *args):
        segFormat = re.compile(r'^(\d+)-(\d+)$')
        sinFormat = re.compile(r'^\d+$')
    
        fraSegStr = cmds.scrollField( 'w04_uiFrameSegments', q=True, text=True ).rstrip()
        filtedStr = ''
        for seg in fraSegStr.split('\n'):
            if seg:
                print seg
                if segFormat.search( seg ) or sinFormat.search( seg ):
                   filtedStr += seg+'\n'
        cmds.scrollField( 'w04_uiFrameSegments', e=True, text=filtedStr.rstrip() )
    
    
    def w04_renderFrameSequence(self, *args):
        self.w04_uiFrameSegments_cmd()
        fraSegStr = cmds.scrollField( 'w04_uiFrameSegments', q=True, text=True ).rstrip()
        renderFrames = []
        for seg in fraSegStr.split('\n'):
            if seg.count('-'):
                s, e = seg.split('-')
                for i in range(int(s), int(e)+1):
                    renderFrames.append( i )
            else:
                renderFrames.append( int(seg) )
        renderFrames = list( set(renderFrames) )
        renderFrames.sort()
        return renderFrames
    
    
    
    
    def w04_renderButtonCommand(self, *args):
        cmds.progressWindow(    title='Rendering', progress=0, status='Rendering: ', isInterruptable=True)
        self.w04_rendering( )
    
    
    def w04_rendering(self, *args):
        #Get RenderLayers
        cmds.RenderViewWindow()
        mel.eval( "setTestResolutionVar 1")
        cmds.optionVar( intValue=[ "renderViewRenderSelectedObj", 0])
    
        currentLayer = cmds.editRenderLayerGlobals( q=True, currentRenderLayer=True)
    
    
        allLayers = cmds.listConnections("renderLayerManager.renderLayerId", s=False,d=True)
        layerData = []
        for layer in allLayers:
            disOrder = cmds.getAttr(layer+'.displayOrder')
            layerData.append((disOrder, layer))
        layerData.sort()
        allRenderLayers = []
        for layer in layerData:
            allRenderLayers.append(layer[1])
    
        #renderableLayers = []
        renderLayerInfo = {}
        frameRangeMode = cmds.checkBox('w04_setFrameRange', q=True, v=True)
        if frameRangeMode:
            if cmds.radioButtonGrp( 'w04_uiFrameRangeStyle', q=True, select=True)==1:
                startframe = cmds.intFieldGrp( "w04_startFrame",    q=True,  v1=True  )
                endframe = cmds.intFieldGrp( "w04_endFrame",      q=True,  v1=True  )
                step = cmds.intFieldGrp( "w04_byFrame", q=True, v1=True)
                if step==0:
                    step=1
                toRenderFrames = range(startframe, endframe+1, step)
            else:
                toRenderFrames = self.w04_renderFrameSequence()
    
        totalCount = 0
        for curLay in allRenderLayers:
            if cmds.getAttr(curLay+'.renderable'):
    
                cmds.editRenderLayerGlobals( currentRenderLayer=curLay)
                if frameRangeMode == False:
                    #Get default frame range
                    startframe = int( cmds.getAttr("defaultRenderGlobals.startFrame") )
                    endframe = int( cmds.getAttr("defaultRenderGlobals.endFrame") )
                    toRenderFrames = range(startframe, endframe+1)
    
    
                cameras = self.w04_renderableCams()
                currentLayerFrames = len(toRenderFrames) * len(cameras)
                totalCount += currentLayerFrames
    
                renderLayerInfo[curLay]=( toRenderFrames, cameras)
    
        if renderLayerInfo.keys() == []:
            raise IOError('No renderable render layers')
    
        #print totalCount
    
        pbStart = cmds.checkBox('w04_pbStart', q=True, v=True)
        pbmin = cmds.playbackOptions(q=True, min=True)
        sceneName = cmds.file(q=True,sceneName=True).rsplit("/", 1)[-1].rsplit('.',1)[0]
        paddingzero = cmds.getAttr ("defaultRenderGlobals.extensionPadding")
        imagePath = cmds.workspace(q =True, rootDirectory=True)+'images'
        frameRangeMode = cmds.checkBox('w04_setFrameRange', q=True, v=True)
    
        #loop renderableLayers
        curframenum = 0
    
    
    
        cmds.progressWindow( edit=True, isInterruptable=True, maxValue=totalCount)
    
        #Do Rendering
        savedC = False
        if cmds.radioButtonGrp( 'w04_renderingModel', q=True, select=True) == 2:
            #######Rendering layer by layer
            #def layerbylayer():
            cmds.progressBar( 'w04_pbTotal',  edit=True, beginProgress=True, isInterruptable=True, maxValue=totalCount  )
            for layerName, layerData in renderLayerInfo.iteritems():
                #startframe, endframe = int(layerData[0][0]), int(layerData[0][1])
                toRenderFrames = layerData[0]
                cameras = layerData[1]
                cmds.progressBar( 'w04_pbCurLay',  edit=True, endProgress=True)
                cmds.progressBar( 'w04_pbCurLay', edit=True, beginProgress=True,isInterruptable=True, maxValue=len(toRenderFrames)*len(cameras)  )
    
                #break render
                if cmds.progressWindow( query=True, isCancelled=True ):
                    cmds.checkBox('w04_closeMaya', e=True, v=False)
                    cmds.checkBox('w04_shutdown', e=True, v=False)
                    cmds.progressWindow(endProgress=True)
                    raise IOError( 'Rendering is Escape')
    
                #Updata UI
                self.w04_updataUI()
    
                if pbStart:
                    for i in range(pbmin, toRenderFrames[0]):
                        cmds.currentTime(i)
    
                cmds.editRenderLayerGlobals( currentRenderLayer=layerName)
    
                #path = cmds.workspace(q =True, rootDirectory=True)+'images'
                filename = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
                filename = re.sub('<Scene>', sceneName, filename)
                filename = re.sub('<RenderLayer>', layerName, filename)
                filename = filename.replace('\\', '/')
                imFormat = w04_getExtension()
    
                #do render, Loop frame range
                for curframe in toRenderFrames:
                #break render
                    if cmds.progressWindow( query=True, isCancelled=True ):
                        cmds.checkBox('w04_closeMaya', e=True, v=False)
                        cmds.checkBox('w04_shutdown', e=True, v=False)
                        cmds.progressWindow(endProgress=True)
                        raise IOError( 'Rendering is Escape')
    
                    cmds.currentTime(curframe)
                    if curframe%10==0:
                        cmds.flushUndo()
                    #loop Cameras
                    for renderCam in w04_renderableCams():
                        #break render
                        if cmds.progressWindow( query=True, isCancelled=True ):
                            cmds.checkBox('w04_closeMaya', e=True, v=False)
                            cmds.checkBox('w04_shutdown', e=True, v=False)
                            cmds.progressWindow(endProgress=True)
                            raise IOError( 'Rendering is Escape')
    
    
                        #get images path and name
                        addCamera = re.sub('<Camera>', renderCam, filename)
                        addFrameStr = addCamera + '.%0' + '%sd'%(paddingzero)
                        exec('addFrame = addFrameStr%(curframe)')
                        finalName = addFrame# + '.'+ w04_getExtension()
                        #print finalName
    
                        finalPath = imagePath+'/'+finalName
                        #finalPath = finalPath.replace('/', '\\')
                        try:
                            if os.path.exists(finalPath.rsplit('/', 1)[0]) == False:
                                os.makedirs(finalPath.rsplit('/', 1)[0])
                        except:
                            os.makedirs('C' +  finalPath.rsplit('/', 1)[0][1:]  )
                            savedC = True
    
    
                        finalImagesFullPath = finalPath+'.'+imFormat[1]
                        try:
                            if os.path.exists(finalImagesFullPath):
                                os.remove(finalImagesFullPath)
                        except:
                            finalPath='C' + finalPath[1:]
                            print "No has %s"%(finalPath)
                            savedC = True
    
    
    
                        cmds.text( 'w04_filename', e=True, label="File Name:  "+finalName+'.'+imFormat[1])
                        print finalPath+'.'+imFormat[1]
    
    
    
                        #rendering images
                        try:
                            mel.eval( 'renderWindowRenderCamera render renderView %s'%(renderCam) )
                            mel.eval( 'renderWindowSaveImageCallback( "renderView", "%s", "%s")'%( finalPath, imFormat[0] )   )
                        except:
                            pass
    
    
                        curframenum += 1
                        #laybarValue = mel.eval(  'linstep(%s, %s, %s)'%(toRenderFrames[0]-1, toRenderFrames[1], curframe) )  *100
                        #totalbarValue = (curframenum / totalCount)*100
                        cmds.progressBar( 'w04_pbCurLay', edit=True, step=1   )
                        #print curframenum
                        cmds.progressBar( 'w04_pbTotal',  edit=True, step=1  )
                        cmds.progressWindow( edit=True, step=1, status='Rendering: '+`curframenum` + ' of ' + `totalCount`)
    
        else:
            #########Rendering frame by frame
            cmds.progressBar( 'w04_pbTotal',  edit=True, beginProgress=True, isInterruptable=True, maxValue=totalCount  )
            cmds.progressBar( 'w04_pbCurLay', edit=True, beginProgress=True, isInterruptable=True, maxValue=totalCount  )
    
            #get minimum maximum frames
            toRenderFrames = []
            for layerName, layerData in renderLayerInfo.iteritems():
                toRenderFrames.extend( layerData[0] )
            toRenderFrames = list( set(toRenderFrames)  )
            toRenderFrames.sort()
    
            if pbStart:
                for i in range(pbmin, toRenderFrames[0]):
                    cmds.currentTime(i)
    
    
    
            for curframe in toRenderFrames:
                if cmds.progressWindow( query=True, isCancelled=True ):
                    cmds.checkBox('w04_closeMaya', e=True, v=False)
                    cmds.checkBox('w04_shutdown', e=True, v=False)
                    cmds.progressWindow(endProgress=True)
                    raise IOError( 'Rendering is Escape')
    
                cmds.currentTime(curframe)
                if curframe%10==0:
                    cmds.flushUndo()
    
    
                for layerName, layerData in renderLayerInfo.iteritems():
                    curLayerFrames = layerData[0]
    
                    #print layerName, startframe, endframe,curframe
                    if curframe not in curLayerFrames:
                        continue
    
                    cameras = layerData[1]
    
                    #break render
                    if cmds.progressWindow( query=True, isCancelled=True ):
                        cmds.checkBox('w04_closeMaya', e=True, v=False)
                        cmds.checkBox('w04_shutdown', e=True, v=False)
                        cmds.progressWindow(endProgress=True)
                        raise IOError( 'Rendering is Escape')
    
                    #Updata UI
                    self.w04_updataUI()
    
    
    
                    cmds.editRenderLayerGlobals( currentRenderLayer=layerName)
    
                    #renderLayerName = layerName
                    #if renderLayerName ==  'defaultRenderLayer':
                        #renderLayerName = 'masterLayer'
    
                    #path = cmds.workspace(q =True, rootDirectory=True)+'images'
                    filename = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
                    filename = re.sub('<Scene>', sceneName, filename)
                    filename = re.sub('<RenderLayer>', layerName, filename)
                    imFormat = self.w04_getExtension()
    
                    #loop Cameras
                    for renderCam in self.w04_renderableCams():
                        #break render
                        if cmds.progressWindow( query=True, isCancelled=True ):
                            cmds.checkBox('w04_closeMaya', e=True, v=False)
                            cmds.checkBox('w04_shutdown', e=True, v=False)
                            cmds.progressWindow(endProgress=True)
                            raise IOError( 'Rendering is Escape')
    
    
                        #get images path and name
                        addCamera = re.sub('<Camera>', renderCam, filename)
                        addFrameStr = addCamera + '.%0' + '%sd'%(paddingzero)
                        exec('addFrame = addFrameStr%(curframe)')
                        finalName = addFrame# + '.'+ w04_getExtension()
                        #print finalName
    
                        finalPath = imagePath+'/'+finalName
                        #finalPath = finalPath.replace('/', '\\')
                        if os.path.exists(finalPath.rsplit('/', 1)[0]) == False:
                            os.makedirs(finalPath.rsplit('/', 1)[0])
    
    
                        finalImagesFullPath = finalPath+'.'+imFormat[1]
                        cmds.text( 'w04_filename', e=True, label="File Name:  "+finalName+'.'+imFormat[1])
                        print finalPath+'.'+imFormat[1]
                        if os.path.exists(finalImagesFullPath):
                            os.remove(finalImagesFullPath)
    
    
    
                        #rendering images
                        try:
                            mel.eval( 'renderWindowRenderCamera render renderView %s'%(renderCam) )
                            mel.eval( 'renderWindowSaveImageCallback( "renderView", "%s", "%s")'%( finalPath, imFormat[0] )   )
                        except:
                            pass
    
    
                        curframenum += 1
                        #laybarValue = mel.eval(  'linstep(%s, %s, %s)'%(curLayerFrames[0]-1, curLayerFrames[-1], curframe) )  *100
                        #totalbarValue = (curframenum / totalCount)*100
                        cmds.progressBar( 'w04_pbCurLay', edit=True, step=1  )
                        print curframenum
                        cmds.progressBar( 'w04_pbTotal',  edit=True, step=1  )
                        cmds.progressWindow( edit=True, step=1, status='Rendering: '+`curframenum` + ' of ' + `totalCount`)
    
    
    
    
        cmds.progressBar( 'w04_pbCurLay',  edit=True, endProgress=True)
        cmds.progressBar( 'w04_pbTotal',   edit=True, endProgress=True)
        cmds.progressWindow(endProgress=True)
        if savedC:
            os.startfile( 'C:/')
            #from subprocess import Popen
            #Popen('explorer C:\\', shell=True)
        if cmds.checkBox('w04_closeMaya', q=True, v=True):
            os._exit(0)
        if cmds.checkBox('w04_shutdown', q=True, v=True):
            mel.eval('system("shutdown -s -t 300")')

#w04_renderingWin()
#------------------w04_End------------------------------------------