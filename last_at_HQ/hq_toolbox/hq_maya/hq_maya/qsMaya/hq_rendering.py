# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import maya.mel as mel
import json

def bakeTextureTool(obj, xRes, yRes, imFormat, alpha=True):
    '''{'del_path':'Rendering/Render/bakeTextureTool()ONLYSE',
'usage':'$fun(cmds.ls(sl=True)[0], 512, 512, "iff", alpha=True)',
}    
'''
    #if str(type(objects)) == "<type 'str'>" or str(type(objects)) == "<type 'unicode'>":
        #objects = [objects]
    #obj = cmds.ls(sl=True)[0]
    #xRes=1024
    #yRes=1024
    #imFormat = "tif"
    #alpha=True
    imFormatV = ["tif", "iff", "jpg", "rgb", "rla", "tga", "bmp", "hdr"].index(imFormat)+1
    
    cmds.scriptEditorInfo(sr=True,suppressWarnings=True)
    #set path
    prj = cmds.workspace(q=True,rd=True)
    
    if not os.path.exists(prj+"sourceimages"):    
        os.mkdir(prj+"sourceimages")
    
    os.chdir(prj+"sourceimages")
    
    if os.path.exists("lightMap"):
        os.rename("lightMap", "lightMapOrig")
    os.mkdir("lightMap")
    
    #create and set textureBakeSet
    if cmds.objExists("tempBakeSet*"):
        cmds.delete("tempBakeSet*")
    tempBakeSet = mel.eval(r'createBakeSet( "tempBakeSet", "textureBakeSet")')
    
    cmds.setAttr("%s.colorMode"%tempBakeSet, 0)
    cmds.setAttr("%s.xResolution"%tempBakeSet, xRes)
    cmds.setAttr("%s.yResolution"%tempBakeSet, yRes)
    cmds.setAttr("%s.fileFormat"%tempBakeSet, imFormatV)
    if alpha:
        cmds.setAttr("%s.bakeAlpha"%tempBakeSet, 1)
    
    
    #copy new renderLayer for bake
    bakeSetRL = cmds.createRenderLayer(g=True,n="tempBakeSetL")
    
    #get shape and shadingEngine
    if not cmds.objectType(obj,i="mesh"):
        obj = cmds.listRelatives(obj,f=True,type="mesh")
        if obj != None:
            obj=obj[0]        
            sE = cmds.listConnections(obj,type="shadingEngine")
            if sE != None:sE = sE[0]
            #print obj,sE
    
    if obj != None and sE != None:
        mel.eval('assignBakeSet( "%s", "%s")'%(tempBakeSet,obj))
        startF = cmds.playbackOptions(q=True, min=True)
        endF = cmds.playbackOptions(q=True, max=True)
        for curF in range(startF, endF+1):
            cmds.currentTime(curF, e=True)        
            mapName = cmds.convertLightmap(sE, obj,camera="persp", prj=prj+"sourceimages")[0]
            if os.path.exists("lightMap/%s.%04d.%s"%(mapName,curF,imFormat)):
                os.remove("lightMap/%s.%04d.%s"%(mapName,curF,imFormat))
            os.rename("lightMap/%s.%s"%(mapName, imFormat), "lightMap/%s.%04d.%s"%(mapName,curF,imFormat) )
            print "saved image %s.%04d.%s"%(mapName,curF,imFormat)
        if os.path.exists(mapName):
            shutil.rmtree(mapName)
        print "saved images squeuence to %s\%s"%(os.getcwd(),mapName)
        os.rename("lightMap", mapName)
        os.rename("lightMapOrig", "lightMap")
    cmds.delete(tempBakeSet)
    cmds.scriptEditorInfo(sr=False,suppressWarnings=False)



#--------------miSequence
def miSequence(start=None, end=None):
    '''{'path':'Rendering/Render/miSequence()ONLYSE',
'icon' : ':/menuIconRender.png',
'tip' : '将物体转为mentalray代理的粒子替代',
'usage':'$fun( start=0, end=100)',
}
'''
    projDir = cmds.workspace(q =1, rootDirectory=1)
    proxyFolder = os.path.join(projDir, 'data/mrProxyFiles')

    if os.path.exists( proxyFolder )==False:
        os.makedirs( proxyFolder )


    exportObjs = cmds.ls(sl=True)

    if start==None:
        start = cmds.playbackOptions(q=True, min=True)

    if end==None:
        end = cmds.playbackOptions(q=True, max=True)

    end = end+1

    pad = 5

    padStr = '%0'+'%sd'%(pad)

    #print padStr

    subFolder = exportObjs[0]

    finalFolder = proxyFolder+'/'+subFolder
    if os.path.exists(finalFolder )==False:
        os.makedirs( finalFolder )

    import mentalray.renderProxyUtils

    proxyObjs = []
    for i in range( start, end):
        cmds.currentTime( i )
        exec('frameStr = padStr%(i)')
        miName = '%s_s.%s.mi'%(exportObjs[0], frameStr)
        miFilePath = finalFolder+'/'+miName
        print miFilePath
        #miFilePath = 'F:/t.mi'
        cmds.select( exportObjs, r=True)
        mel.eval( 'Mayatomr -mi  -exportFilter 721600 -active -binary -fe  -fem  -fma  -fis  -fcd  -pcm  -as -asn "%s" -xp "3313333333" -file "%s";'%(exportObjs[0]+"_s", miFilePath ) )

        proxyName = miName.replace( '.', '-' )
        proxyObj = cmds.polyCube(ch=False, name=proxyName)[0]
        proxyObjs.append(proxyObj)
        boxShape = cmds.listRelatives( proxyObj, shapes=True)[0]

        cmds.setAttr( proxyObj+'.miProxyFile', miFilePath, type='string')

        mentalray.renderProxyUtils.resizeToBoundingBox(boxShape)
        cmds.setAttr( proxyObj+".t", lock=True)
        cmds.setAttr( proxyObj+".r", lock=True)
        cmds.setAttr( proxyObj+".s", lock=True)

    cmds.currentTime( start )
    nPar, parShape = cmds.nParticle()
    cmds.setAttr( parShape+'.collide', 0)
    cmds.setAttr( parShape+".conserve", 0)
    cmds.setAttr( parShape+".dynamicsWeight", 0)
    cmds.setAttr( parShape+".particleRenderType", 2)

    #cmds.setAttr( parShape+".selectedOnly", 1)

    cmds.addAttr(parShape, ln="cus_index0", dt="doubleArray")
    cmds.addAttr(parShape, ln="cus_index",  dt="doubleArray")

    mel.eval( 'emit -object nParticle1 -pos 0 0 0' )

    expString = "cus_index = clamp(0, %i, frame-%i);"%( end-start-1, start)

    cmds.dynExpression( parShape, s=expString, c=True)
    cmds.dynExpression( parShape, s=expString, rbd=True)


    instancerObj = cmds.particleInstancer( parShape, addObject=True, object=proxyObjs, cycle='None', cycleStep=1, cycleStepUnits='Frames', levelOfDetail='Geometry', rotationUnits='Degrees', rotationOrder='XYZ', position='worldPosition', age='age')
    cmds.particleInstancer( parShape, e=True, name=instancerObj, objectIndex='cus_index')

    cmds.saveInitialState( parShape )

    miGrp = cmds.group( proxyObjs, n= exportObjs[0]+'_s_mi' )
    cmds.setAttr( miGrp+'.v', False)
    cmds.setAttr( miGrp+'.v', lock=True)
    papaGrp = cmds.group( [nPar, miGrp, instancerObj], n=exportObjs[0]+'_mi_group')

    for obj in (nPar, miGrp, instancerObj, papaGrp):
        cmds.setAttr( obj+".t", lock=True)
        cmds.setAttr( obj+".r", lock=True)
        cmds.setAttr( obj+".s", lock=True)



def out_mapInfo(indent=None):
    allSE = cmds.ls(exactType='shadingEngine', l=True)
    if not allSE:
        return
    
    mapsData = {}
    allSE  = [se for se in allSE if cmds.listConnections( se+'.surfaceShader') ]
    for se in allSE:    
        #cmds.select( se, ne=True, r=True)
        shader = cmds.listConnections( se+'.surfaceShader')[0]    
        mapsData[se] = {'type': cmds.nodeType( shader ) }
        mapsData[se]['maps'] = []
        connectedNode = cmds.listConnections( shader, d=False, c=True)
        if not connectedNode:
            continue
        for i in range( 0, len( connectedNode), 2):
            shaderAttr = connectedNode[i].split('.', 1)[-1]
            sourceNode = connectedNode[i+1]
            fileNodes = [ f for f in cmds.listHistory( sourceNode ) if cmds.nodeType(f)=='file' ]
            filePaths = [cmds.getAttr(f+'.fileTextureName') for f in fileNodes ]
            if fileNodes:            
                mapsData[se]['maps'].append( (shaderAttr, filePaths) )
    
    jsonStr = json.dumps( mapsData, indent=indent)
    sceneName = cmds.file( q=True,  sceneName=True)
    jsonFilePath = os.path.splitext( sceneName )[0]+'_mapInfo.json'.replace('\\', '/')
    jsonFile = open( jsonFilePath, 'w' )        
    jsonFile.write( jsonStr )
    jsonFile.close()
    os.startfile(  os.path.dirname( jsonFilePath )   )
    return jsonFilePath





