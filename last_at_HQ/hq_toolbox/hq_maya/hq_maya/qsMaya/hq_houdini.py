# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
#import qsMaya as qm


def show_pw_mGeo():
    '''{'path':'Houdini/show_pw_mGeo( )',
'icon':'$ICONDIR/houdini.png',
'html':True,
'usage':'$fun( )',
}
'''
    import pw_mGeo
    pw_mGeo.show()



def mayaConnect_th( ):
    '''{'del_path':'Houdini/mayaConnect_th( )',
'icon':'$ICONDIR/houdini.png',
'usage':'$fun( )',
}
'''
    from MayaConnectionTest import MayaModule
    ui = MayaModule.MayaConnectionUI()
    ui.show()



def toHouCam():
    '''{'path':'Houdini/toHouCam()',
'icon':':/camera.svg',
'usage':'$fun()',
"help":"""
选择相机或包含相机的组；执行之前先把分辨率设置对；
"""
}
'''
    if cmds.ls(sl=True)!=[]:
        selected = cmds.ls(sl=True, exactType='camera')
        selChildren = cmds.listRelatives( cmds.ls(sl=True, l=True), type='camera', ad=True, f=True )
        camShapes = []
        if selected!=[]:
            camShapes = selected
        if selChildren!=None:
            camShapes.extend( selChildren )

        newCameras = []
        for camShape in camShapes:
            newCameras.append( __toHouCamSingle(camShape) )
        if newCameras!=[]:
            cmds.group( newCameras, name='toHouCameras', world=True)



def __toHouCamSingle(camShape):
    camShape = camShape
    cam = cmds.listRelatives( camShape, parent=True )[0]
    newCam = cmds.duplicate( cam, name=cam+'_baked', rc=True )[0]


    #cam = cmds.ls(sl=True)[0]
    #camShape = cmds.listRelatives( cam, shapes=True)[0]
    #newCam = cmds.duplicate( cam, name=cam+'_baked', rc=True )[0]
    if cmds.listRelatives(newCam, parent=True)!=None:
        newCam = cmds.parent( newCam, world=True)[0]
    newCamShape = cmds.listRelatives( newCam, shapes=True)[0]


    #Unlock newCam and newCamShape locked attributes
    for node in (newCam, newCamShape):
        lockedAttrs = cmds.listAttr( node, locked=True)
        if lockedAttrs != None:
            for attr in lockedAttrs:
                cmds.setAttr( '%s.%s'%(node,attr), lock=False )


    #get connected attributes of cameraShape
    attrs = cmds.listConnections( camShape, d=False, c=True )
    shapeAttrs = []
    if attrs:
        for i in range(0, len(attrs), 2):
            shapeAttrs.append( attrs[i].split('.')[1] )
        for attr in ('horizontalFilmOffset','verticalFilmOffset'):
            if attr in shapeAttrs:
                shapeAttrs.remove(attr)



    #Set new camera and shape Attributes
    cmds.addAttr( newCam, ln='hFilmOffset', at='double' )
    cmds.addAttr( newCam, ln='vFilmOffset', at='double' )
    cmds.setAttr(newCamShape+'.filmFit', 1)



    #Get original attributes
    deviceAspectRatio = float( cmds.getAttr('defaultResolution.width')) / cmds.getAttr('defaultResolution.height')

    horFilmAperture = cmds.getAttr(camShape+'.horizontalFilmAperture')
    verFilmAperture = cmds.getAttr(camShape+'.verticalFilmAperture')
    filmAspectRatio = horFilmAperture / verFilmAperture

    horFilmOffset = cmds.getAttr(camShape+'.horizontalFilmOffset')
    verFilmOffset = cmds.getAttr(camShape+'.verticalFilmOffset')

    fitResolutionGate = cmds.getAttr(camShape+'.filmFit')
    fitResolutionGate = ('Fill', 'Horizontal', 'Vertical')[fitResolutionGate]

    #Calculate film offset
    newHorFilmAperture = horFilmAperture
    newVerFilmAperture = verFilmAperture



    if filmAspectRatio>deviceAspectRatio:
        if fitResolutionGate=='Fill' or fitResolutionGate=='Vertical':#Fill equal Vertical
            newHorFilmAperture = verFilmAperture * deviceAspectRatio
        else:#fitResolutionGate=='Horizontal'
            newVerFilmAperture = horFilmAperture / deviceAspectRatio
    else:#filmAspectRatio=<diviceAspectRatio Fill equal horizontal
        if fitResolutionGate=='Fill' or fitResolutionGate=='Horizontal':
            newVerFilmAperture =  horFilmAperture / deviceAspectRatio
        else:#fitResolutionGate==verAspectRatio
            newHorFilmAperture = verFilmAperture * deviceAspectRatio

    newHorFilmOffset = horFilmOffset/newHorFilmAperture
    newVerFilmOffset = verFilmOffset/newVerFilmAperture

    cmds.setAttr(newCamShape+'.horizontalFilmAperture', newHorFilmAperture)
    cmds.setAttr(newCamShape+'.verticalFilmAperture', newVerFilmAperture)

    cmds.setKeyframe( newCam+'.hFilmOffset',  v=newHorFilmOffset)
    cmds.setKeyframe( newCam+'.vFilmOffset',  v=newVerFilmOffset)

    cmds.setAttr(newCamShape+'.horizontalFilmOffset', horFilmOffset)
    cmds.setAttr(newCamShape+'.verticalFilmOffset', verFilmOffset)


    #Bake animated attributes
    minTime = int( cmds.playbackOptions(q=True,min=True) )
    maxTime = int( cmds.playbackOptions(q=True,max=True)+1 )
    for i in range(minTime, maxTime):
        cmds.currentTime(int(i))
        camXform = cmds.xform(cam,q=True, ws=True, m=True)
        cmds.xform(newCam,ws=True, m=camXform)
        cmds.setKeyframe(newCam,at=["tx","ty","tz","rx","ry","rz"])

        #Key shape attributes
        for attr in shapeAttrs:
            #cmds.setAttr( newCamShape+'.'+attr, cmds.getAttr(camShape+'.'+attr) )
            cmds.setKeyframe(newCamShape, at=attr, v=cmds.getAttr(camShape+'.'+attr) )
    return newCam



def createShadingEngineByHoudiniPrimGroupName():
    '''{'path':'Houdini/Materials/createShadingEngineByHoudiniPrimGroupName()',
'icon':':/camera.svg',
'usage':"""
#将所有的Shading engine复制一个，并将其名字转为为Houdini Primitive Group的命名方式。
#这些新创建的Shading engine会放在一个名为primgroup_adingEngines的sets中，选择这个sets，并在Node editor中，可以查其包含的Shading engine.
$fun()""",
}
'''
    allSE = cmds.ls(exactType='shadingEngine', l=True)
    newSEs = []
    for se in allSE:
        primGrpName = se
        for s in ':|':
            primGrpName = primGrpName.replace(s, '_')
        if cmds.objExists(primGrpName) and cmds.objectType(primGrpName)=='shadingEngine':
            continue
        newSE = cmds.duplicate( se, ic=True)[0]
        newSE = cmds.rename( newSE, primGrpName )
        newSEs.append( newSE )

    if newSEs:
        existSet = cmds.ls( 'primGroup_shadingEngines*', exactType='objectSet' )
        if not existSet:
            primGroupSE = cmds.sets( name='primGroup_shadingEngines', empty=True)
        else:
            primGroupSE = existSet[0]
        cmds.sets( newSEs, e=True, add=primGroupSE )

        return primGroupSE
    return None



def connectToHou():
    '''{'del_path':'Houdini/connectToHou( )',
'icon':'$ICONDIR/houdini.png',
'usage':'$fun( )',
}
'''
    try:
        import hrpyc
        global connection, hou
        connection, hou=hrpyc.import_remote_module()
        print '--Connected to Houdini--'
    except:
        print '--Houdini no have opened--'
