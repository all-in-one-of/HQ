# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as newom
import pymel.core as pm
import qsMaya as qm

import re, os
import math
import json


def openProject():
    projDir = cmds.workspace(q =True, rootDirectory=True)
    if projDir.startswith('//'):
        projDir = projDir.replace('/', '\\')    
    os.startfile(  projDir )



def removeNamespace():
    '''{'path':'Edit/removeNamespace( )',
'icon':':/SP_TrashIcon.png',
'tip':'移除namespace',
'usage':"""
#移除namesapce，有reference时，可以会移除不成功；得闲再修改一下吧
$fun( )""",
}
'''
    for num in range(255):
        pm.namespace(set=unicode(":"))
        ns = pm.namespaceInfo(lon=1)
        if len(ns) < 3:
            print(str(num)+" levels")
            break
        for nss in ns:
            tli = ["UI", "shared"]
            if nss not in tli:
                pm.namespace(f=1, mv=(nss,unicode(":")))
                pm.namespace(f=1, rm=nss)


def removeTSMMenu():
    '''{'path':'Edit/removeTSMMenu( )',
'icon':':/SP_TrashIcon.png',
'tip':'移除TSM菜单',
'usage':'$fun( )'
}
'''
    scrNodes = pm.ls(type = 'script')
    len(scrNodes)
    for scrNode in scrNodes:
        if re.search('Switch',str(scrNode)):
            pm.delete(str(scrNode))



def cachedObjToTransform(*args):
    '''{'ath':'Animation/Transform/cachedObjToTransform( )',
'ath':'Dynamics/RBD',
'icon':':/transform.svg',
'usage':"""
#将缓存物体bake成关键帧物体。
$fun(  )""",
}
'''
    if len( args ):
        cachedObj = qm.checkArg( args[0], nodeType='mesh', tryToShape=True )
    else:
        cachedObj = qm.checkArg( nodeType='mesh', tryToShape=True )

    cmds.constructionHistory(toggle=False)
    #cachedObj = cmds.ls(sl=True,l=True)[0]
    #sepratate cachedObj
    minTime = int( cmds.playbackOptions(q=True,min=True) )
    cmds.currentTime(minTime)
    temp = cmds.polySeparate(cachedObj, ch=True)[0]
    rbdGrp = cmds.listRelatives(temp, p=True, f=True)[0]
    childGrp = cmds.duplicate(rbdGrp,rr=True)[0]
    parentList = cmds.listRelatives(rbdGrp, type='transform', f=True)
    childList = cmds.listRelatives(childGrp, type='transform', f=True)
    cmds.delete(cmds.listRelatives(childGrp,f=True),ch=True)


    forRemove = []
    for obj in parentList:
        meshNode = cmds.listRelatives(obj,type='mesh', f=True)
        if meshNode == [] or cmds.getAttr(meshNode[0]+'.intermediateObject') == 1:
            forRemove.append(obj)
    if obj in forRemove:
        parentList.remove(obj)


    forRemove = []
    for obj in childList:
        meshNode = cmds.listRelatives(obj,type='mesh', f=True)
        if meshNode == [] or cmds.getAttr(meshNode[0]+'.intermediateObject') == 1:
            forRemove.append(obj)
    if obj in forRemove:
        childList.remove(obj)
    cmds.delete(forRemove)


    unfreeze(childList)

    folGrp = cmds.group(em=True,n=rbdGrp+'_FoGrp')

    for papa in parentList:
        index = parentList.index(papa)
        child = childList[index]
        meshShape = cmds.listRelatives(papa, type='mesh', f=True)[0]

        faceCount = cmds.polyEvaluate(papa,f=True)-1
        if faceCount > 10:
            faceCount = 10

        newFace = '%s.f[0:%s]'%(papa, faceCount)
        cmds.select(newFace)
        mel.eval('polySplitTextureUV')

        mel.eval('PolySelectConvert 4')
        map = cmds.ls(sl=True)

        cmds.polyNormalizeUV( map, normalizeType=0, preserveAspectRatio=False)

        cmds.polyEditUV(map,pu=.5, pv=.5, su=2, sv=2)

        #create follicle and set attribute
        folShape = cmds.createNode("follicle")

        folTransform = cmds.listRelatives(folShape, p=True,f=True)[0]
        cmds.setAttr(folTransform+'.intermediateObject',1)

        cmds.setAttr(folShape + '.parameterU', .5, l=True)
        cmds.setAttr(folShape + '.parameterV', .5, l=True)
        cmds.setAttr(folShape + ".simulationMethod", 0)
        cmds.setAttr(folShape + ".collide", 0)
        cmds.setAttr(folShape + ".degree", 1)
        cmds.setAttr(folShape + ".sampleDensity", 0)

        #connection follicles
        cmds.connectAttr(meshShape+'.worldMatrix[0]', folShape + '.inputWorldMatrix', f=True)
        cmds.connectAttr(meshShape+'.outMesh', folShape + '.inputMesh', f=True)
        cmds.connectAttr(folShape + '.outRotate', folTransform+'.rotate', f=True)
        cmds.connectAttr(folShape + '.outTranslate', folTransform+'.translate', f=True)

        parentConNode =  cmds.parentConstraint( folTransform, child, mo=True )[0]

        cmds.parent( folTransform,  folGrp)

    minTime = int( cmds.playbackOptions(q=True,min=True) )
    maxTime = int( cmds.playbackOptions(q=True,max=True) )
    cmds.bakeResults(childList,simulation=True, t=(minTime,maxTime),sampleBy=1,\
                    disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, \
                    bakeOnOverrideLayer=False,at=['tx','ty','tz','rx','ry','rz'])

    cmds.delete([folGrp,rbdGrp])
    cmds.delete(cmds.listRelatives(childGrp,f=True),ch=True)

    cmds.constructionHistory(toggle=True)



#------------------------Polygon------------------------------
def positionsOnMesh(meshObj, position, rayDirection=False ):
    '''{'del_path':'Polygons/QueryMesh/positionsOnMesh()ONLYSE',
'usage':'\
meshObj = cmds.ls(sl=True)[-1]\\n\
objs = cmds.ls(sl=True)[:-1]\\n\
position = []\\n\
for obj in objs:\\n\
    position.append( cmds.getAttr(obj+".t")[0] )\\n\
newPos = $fun(meshObj, position, rayDirection=(0,-1,0) )\\n\
for obj in objs:\\n\
    pos = newPos[ objs.index(obj) ]\\n\
    cmds.setAttr(obj+""t", pos[0], pos[1], pos[2], type="double3")',
}
'''
    meshs = newom.MSelectionList()
    meshs.add( meshObj )
    meshDagPath = meshs.getDagPath(0)
    meshFn = newom.MFnMesh(meshDagPath)

    newPos = []
    if rayDirection==False:
        print rayDirection
        for pos in position:
            newPos.append(  tuple(meshFn.getClosestPoint( newom.MPoint(pos), newom.MSpace.kWorld)[0])  )
    else:
        rayDirection = newom.MFloatVector( rayDirection )
        for pos in position:
            raySource = newom.MFloatPoint( pos )
            hitPoint = tuple( meshFn.closestIntersection(raySource, rayDirection, newom.MSpace.kWorld, 9999.0, False)[0] )
            hitPos = pos if hitPoint==(0, 0, 0, 1) else hitPoint
            newPos.append(  hitPos  )
    return newPos

def objOnMesh():
    '''{'path':'Polygons/QueryMesh/objOnMesh(  )',
'icon':':/transform.svg',
'usage':"""
#选择投射到mesh的一个或多个物体，再选择mesh。将选择的物体的放到mesh上面
$fun( )""",
}
'''
    meshObj = cmds.ls(sl=True)[-1]
    objs = cmds.ls(sl=True)[:-1]
    unfreeze(objs)
    position = []
    for obj in objs:
        position.append( cmds.getAttr(obj+'.t')[0] )
    newPos = positionsOnMesh(meshObj, position, rayDirection=(0,-1,0) )
    for obj in objs:
        pos = newPos[ objs.index(obj) ]
        cmds.setAttr(obj+'.t', pos[0], pos[1], pos[2], type='double3')
    cmds.select( objs, r=True )

def emfx_getVoxelSize(obj, maxRes):
    bbox = cmds.exactWorldBoundingBox(obj, ignoreInvisible=False)
    sizeLi = [math.fabs(bbox[3]-bbox[0]), math.fabs(bbox[4]-bbox[1]), math.fabs(bbox[5]-bbox[2])]
    sizeLi.sort()
    divSize = sizeLi[2]/maxRes
    if divSize > sizeLi[0]/4:
        divSize = sizeLi[0]/4
    return divSize

def inMesh(meshObj, positions, maxRes=100):
    '''{'del_path':'Polygons/QueryMesh/inMesh()ONLYSE',
'icon':':/polyMesh.png',
'usage':'\
meshObj = cmds.ls(sl=True)[-1]\\n\
objs = cmds.ls(sl=True)[:-1]\\n\
positions = []\\n\
for obj in objs:\\n\
    positions.append( cmds.getAttr(obj+".t")[0] )\\n\\n\
inMeshData = $fun(meshObj, positions )\\n\
inMeshObjs=[]\\n\
for obj in objs:\\n\
    if inMeshData[ objs.index(obj) ]:\\n\
        inMeshObjs.append( obj )\\n\
if inMeshObjs:\\n\
    cmds.select(inMeshObjs, r=True)\\n\
mel:\\n\
string $object = "pCube1";\\n\
vector $pos = <<0,0,0>>;\\n\
python("$fun(\""+$object+"\",["+$pos.x+"," +$pos.y+"," +$pos.z+"])");',
}
'''
    meshs = newom.MSelectionList()
    meshs.add( meshObj )
    meshDagPath = meshs.getDagPath(0)
    meshFn = newom.MFnMesh(meshDagPath)

    divSize = emfx_getVoxelSize(meshObj, maxRes)
    bbox = cmds.exactWorldBoundingBox(meshObj, ignoreInvisible=False)
    xDiv = math.fabs(bbox[3]-bbox[0])  /divSize
    yDiv = math.fabs(bbox[4]-bbox[1])  /divSize
    zDiv = math.fabs(bbox[5]-bbox[2])  /divSize


    meshAcceleration = meshFn.uniformGridParams( int(xDiv), int(yDiv), int(zDiv) )


    whethers = []
    rayDirection = newom.MFloatVector( 0, -1, 0 )
    for pos in positions:
        hitPoints = meshFn.allIntersections( newom.MFloatPoint( pos ), rayDirection, newom.MSpace.kWorld, 9999.0,
                                            False,
                                            accelParams=meshAcceleration
                                            )[0]
        whethers.append( True if len(hitPoints)%2==1 else False )
    meshFn.clearGlobalIntersectionAcceleratorInfo()

    return whethers

def unfreeze(*args):
    '''{'path':'Modify/unfreeze( )',
'icon':':/transform.svg',
'tip' : '将translate属性设置按时界坐标位置',
'usage':'$fun( )',
}
'''
    if len( args ):
        objects=args[0]
    else:
        objects = cmds.ls(sl=True,exactType='transform')

    if isinstance( objects, str) or isinstance( objects, unicode):
        objects = [objects]

    for obj in objects:
        cmds.makeIdentity(obj,apply=True, t=True)
        cmds.move(obj, rpr=True)
        oriPos = cmds.getAttr(obj+'.t')[0]
        cmds.makeIdentity(obj,apply=True, t=True)
        cmds.setAttr(obj+'.t', oriPos[0]*-1, oriPos[1]*-1, oriPos[2]*-1, type='double3')


def unFreezeScale():
    '''{'path':'Modify/unFreezeScale( )',
'icon':':/transform.svg',
'tip' : '将scale属性设为物体的真实大小',
'usage':'$fun( )',
}
'''
    objects = cmds.ls(sl=True,exactType='transform')

    if isinstance( objects, str) or isinstance( objects, unicode):
        objects = [objects]

    for obj in objects:
        bbsi = cmds.getAttr(obj+".bbsi")[0]
        scaleValue = cmds.getAttr(obj+".scale")[0]
        multV = [1/bbsi[0], 1/bbsi[1], 1/bbsi[2]]
        cmds.setAttr(obj+".scale", scaleValue[0]*multV[0], scaleValue[1]*multV[1], scaleValue[2]*multV[2], type="double3")
        cmds.makeIdentity(obj,apply=True, s=True)
        cmds.setAttr(obj+".scale", bbsi[0],bbsi[1],bbsi[2], type="double3")


def maxAxisTo1(objects):
    '''{'del_path':'Modify/maxAxisTo1(cmds.ls(sl=True,exactType="transform"))',
'icon':':/transform.svg',
'tip' : '将物体的最大轴向的缩放为1个单位大小',
'usage':'$fun(cmds.ls(sl=True,exactType="transf"rm"))',
}
'''

    if isinstance( objects, str) or isinstance( objects, unicode):
        objects = [objects]

    for obj in objects:
        scaleV = cmds.getAttr(obj+".scale")[0]
        maxV = 1/max(scaleV[0],scaleV[1],scaleV[2])
        cmds.setAttr(obj+".scale", scaleV[0]*maxV, scaleV[1]*maxV, scaleV[2]*maxV, type="double3")


def lockSwitch(objectList,lock=None):
    '''{'path':'Modify/lockSwitch(cmds.ls(sl=True))',
'icon':':/lock.png',
'tip' : '锁定、解锁选择的节点',
'usage':'$fun( cmds.ls(sl=True) )',
}
'''
    if isinstance( objectList, str) or isinstance( objectList, unicode):
        objectList = [objectList]

    lockState = lock
    for obj in objectList:
        if lockState == None:
            lockState = not cmds.lockNode(obj, q=True, l=True)[0]
        cmds.lockNode(obj, l=lockState)

    if lock == None:
        print 'Lock or unlock mode'
    else:
        print 'object lock is %s'%(lock)




def delAttr(objects, attributes):
    '''{'del_path':'Modify/Attributes/delAttr()ONLYSE',
'icon':':/attributes.png',
'usage':'\
cmds.listRelatives(cmds.ls(sl=True)[0], type="transform")\\n\
objects = cmds.listRelatives(cmds.ls(sl=True)[0], type="transform")\\n\
$fun(cmds.ls(sl=True),["pBNode","follicleNodeState","atU", "atV", "pBNode1", "pB1Weight", "pB1InT2", "pB1InR2","BlindData3","pdiCutIn"ex"])',
}
'''
    if isinstance( objects, str) or isinstance( objects, unicode):
        objects = [objects]


    if isinstance( attributes, str) or isinstance( attributes, unicode):
        attributes = [attributes]

    for attribute in attributes:
        for object in objects:
            if cmds.attributeQuery(attribute, n=object, exists=True):
                cmds.setAttr(object+'.'+attribute, l=False)
                cmds.deleteAttr(object+'.'+attribute)



def getConnectedTdataCompoundObj(compoundAttr, sourceSide=True, destinationSide=True):
    '''{'del_path':'Modify/Attributes/getConnectedTdataCompoundObj(compoundAttr)ONLYSE',
'icon':':/attributes.png',
'usage':'objects = $fun("pointEmitter_sets.dagSetMembers")',
}
'''
    if str( cmds.getAttr(compoundAttr, type=True) ) != 'TdataCompound':
        raise IOError('%s is not TdataCompound attribute'%compoundAttr)

    resultList = []
    setLi = cmds.getAttr(compoundAttr, mi=True)
    if setLi:
        for ifOrder in setLi:
            forceName = cmds.listConnections('%s[%s]'%(compoundAttr,ifOrder), d=sourceSide, shapes=True, scn=destinationSide )
            if forceName is not None:
                resultList.append(forceName[0])
    return resultList



def makeNameUnique():
    '''{'path':'Modify/makeNameUnique( )',
'icon':':/rename.png',
'tip' : '对选择的物体中的重名物体进行重命名',
'usage':"""
#如果选择的物体，在场景中是有重名的，将会对选择的这些物体进行重命名操作
#Select objects or parent\\n\
$fun( )""",
}
'''
    allNode = cmds.ls(sl=True)
    temp = cmds.listRelatives( cmds.ls(sl=True), ad=True, f=True )
    if temp:
        allNode.extend( temp )


    #allNode[1].rsplit('|',1)[-1]

    for node in allNode:
        shortName = node.rsplit('|',1)[-1]
        if len( cmds.ls( shortName ) ) >1:
        #if shortName in newNodeNames:
            #Get postfix num
            shortPattern = list(shortName)
            shortPattern.reverse()
            postfix = ''
            for char in shortPattern:
                if re.match( r'[0-9]', char ):
                    postfix = char + postfix
                else:
                    break
            if postfix == '':
                postfix = '0'
                prefixName = shortName
            else:
                prefixName = shortName.replace( postfix, '' )


            #Get unique name
            padding = len(postfix)

            i = int( postfix )+1
            get = True
            while get:
                if cmds.objExists( '%s%s'%(prefixName, i) ) == False:
                    evalStr = r'"%0'+str(padding)+'d"'+r'%( i )'
                    newPadding = eval(evalStr)
                    newName = '%s%s'%(prefixName, newPadding)
                    get = False
                i += 1
            cmds.rename( node, newName)


def cleanerUpLoad():
    '''{'del_path':'Dynamics/QS/cleanerUpLoad()',
'icon':':/SP_TrashIcon.png',
'usage':'$fun()',
'help':'删除指定脚本，所有粒子表达式',
}
'''
    #Delete 'QS_VFX*' nodes
    node = cmds.ls('QS_VFX*')
    if node != []:
        cmds.delete(node)
        print 'Deleted %s node'%(node)

    #Delete 'All expressions of particles
    for parShape in cmds.ls(type = 'particle'):
        cmds.dynExpression(parShape, s='', c=True, rbd=True, rad=True )
    print 'Deleted all expressions of particles'

    #Delete inputForce attributes for particle nodes
    addInputForceAttrForPar(cmds.ls(exactType='particle'))

def setCachePath():
    '''{'del_path':'Cache/setCachePath()',
'icon':':/createCache.png',
'usage':'$fun()',
}
'''
    return
    #check cacheSetsq Node existing
    if not pm.objExists('cacheSetSQ'):
        cacheSetNode = pm.scriptNode( n='cacheSetSQ',st=1, bs='//')
    else:
        cacheSetNode = pm.PyNode('cacheSetSQ')

    projDir = cmds.workspace(q =1, rootDirectory=1)

    scriptStr=""

    dynG=pm.ls(exactType="dynGlobals")

    if dynG and dynG[0].useParticleDiskCache.get():
        dynPath = dynG[0].cacheDirectory.get()
        dynPath = re.sub(projDir,"",dynPath)
        scriptStr = 'setAttr -type "string" ' + str(dynG[0]) + ".cacheDirectory " + "\"" + dynPath +"\";" +"\n"


    cacheNodes = pm.ls(exactType="cacheFile")
    if cacheNodes:
        for cacheNode in cacheNodes:
            attrPath = cacheNode.cachePath.get()
            if not re.search(projDir,attrPath):
                print str(cacheNode)+"file path no in data folder"
            else:
                attrPath = re.sub(projDir,"",attrPath)
                scriptStr = scriptStr + 'setAttr -type "string" ' + str(cacheNode) + ".cachePath " + "\"" + attrPath +"\";" +"\n"


    pm.scriptNode( cacheSetNode, e=True, bs=unicode(scriptStr))
    print "Current project: " + str(projDir)



def objToBBox():
    '''{'del_path':'Modify/objToBBox( )',
'icon':':/geometryToBoundingBox.png',
'tip' : '将物体转为box',
'usage':"""
#maya 2013.5已经有这个命令了，在convert menu下面
$fun( )""",
}
'''
    objectList=cmds.ls(sl=True,l=True, exactType='transform')
    if isinstance( objectList, str) or isinstance( objectList, unicode):
        objectList = [objectList]

    for object in objectList:
        bbsi = cmds.exactWorldBoundingBox(object,ii=True)
        bbsi = ( math.fabs( bbsi[3]-bbsi[0]), math.fabs( bbsi[4]-bbsi[1]), math.fabs( bbsi[5]-bbsi[2])   )
        pos = cmds.objectCenter(object)
        shortName = cmds.ls(object, sn=True)[0]
        box = cmds.polyCube( w=bbsi[0], h=bbsi[1], d=bbsi[2], ch=False, name=shortName+'_bbox')[0]
        cmds.setAttr(box+'.t', pos[0], pos[1], pos[2], type='double3')


def saveSwatch():
    '''{'del_path':'Rendering/Render/saveSwatch()',
'icon':':/rvGrbSwatch.png',
'usage':'\
#formats:JPEG,Targa\\n\
$fun()',
}
'''

    imageName = cmds.file(q=True,sceneName=True).rsplit(".", 1)[0]
    imageName = ('C:/'+'mayaTempImage') if imageName == '' else imageName

    #if imformat == None:
    ext = '.jpg'

    if os.path.exists(imageName+ext):
        os.remove(imageName+ext)
    try:
        mel.eval('renderWindowSaveImageCallback ("renderView", "%s", "%s")'%(imageName, "JPEG"))
        return imageName+ext
    except:
        return False
        print "No Succeed"


def QSInitialSet():
    '''{'del_path':'Dynamics/QS/QSInitialSet()',
'usage':'$fun()',
}
'''
    melTimeChanged = 'QS_Mel_timeChanged'
    melOpenClose = 'QS_Mel_openClose'
    pythonTimeChanged = 'QS_Python_timeChanged'
    pythonOpenClose = 'QS_Python_OpenClose'

    if cmds.objExists( melTimeChanged ) == False:
        timeChangedStr='\
/*int $current = `currentTime -q`;\n\
int $start = `playbackOptions -q -min`;\n\
int $end = `playbackOptions -q -max`+5;\n\
if ($current == $start){\n\
//\n\
}*/'
        cmds.scriptNode(st=7,n=melTimeChanged,bs=timeChangedStr)
        cmds.setAttr(melTimeChanged+'.scriptType', l=True)

    if cmds.objExists(melOpenClose) == False:
        cmds.scriptNode(st=1,n=melOpenClose, bs='//')
        cmds.setAttr(melOpenClose+'.scriptType', l=True)

    if cmds.objExists(pythonTimeChanged) == False:
        cmds.scriptNode(st=7,n=pythonTimeChanged, bs='if True:\n    pass',sourceType='python')
        cmds.setAttr(pythonTimeChanged+'.scriptType', l=True)

    if cmds.objExists(pythonOpenClose) == False:
        cmds.scriptNode(st=1,n=pythonOpenClose, bs='if True:\n    pass',sourceType='python')
        cmds.setAttr(pythonOpenClose+'.scriptType', l=True)


def getPrefix(shortName):
    prefix = shortName
    splitedName = obj.rsplit('_')
    if len( splitedName ) ==2:
        postfix = splitedName[-1]
        for c in postfix:
            if re.match(r'[0-9]', c)==None:
                break
        else:
            prefix = splitedName[0]
    return prefix



#---------Other ------------------------------------
def toMaxVRCam():
    """{'path':'Max/toMaxVRCam()',
'icon':':/camera.svg',
'tip' : '烘赔选择的camera',
'html':True,
'usage':'$fun()',
}
"""
    if cmds.ls(sl=True)!=[]:
        selected = cmds.ls(sl=True, type='camera')
        selChildren = cmds.listRelatives( cmds.ls(sl=True, l=True), type='camera', ad=True, f=True )
        camShapes = []
        if selected!=[]:
            camShapes = selected
        if selChildren!=None:
            camShapes.extend( selChildren )

        newCameras = []
        for camShape in camShapes:
            newCameras.extend( __toMaxVRCamSingle(camShape) )
        if newCameras!=[]:
            cmds.group( newCameras, name='toMaxVRCameras')


def __toMaxVRCamSingle(camShape):
    camShape = camShape
    #camShape = 'Screen2RcamShape'
    #print cams
    cam = cmds.listRelatives( camShape, parent=True )[0]
    newCam = cmds.parent(
                        cmds.duplicate( cam, name=cam+'_baked' )[0],
                        w=True
                        )[0]


    newCamShape = cmds.listRelatives( newCam, shapes=True, f=True )[0]
    #Unlock newCam and newCamShape locked attributes
    for node in (newCam, newCamShape):
        lockedAttrs = cmds.listAttr( node, locked=True)
        if lockedAttrs != None:
            for attr in lockedAttrs:
                cmds.setAttr( '%s.%s'%(node,attr), lock=False )



    loc = cmds.spaceLocator(name=newCam+'_loc')[0]


    minTime = int( cmds.playbackOptions(q=True,min=True) )
    maxTime = int( cmds.playbackOptions(q=True,max=True)+1 )

    bakeFilmOffset = 1

    #set filmOffset
    if not cmds.connectionInfo(camShape+'.horizontalFilmOffset',id=True) and \
            not cmds.connectionInfo(camShape+'.verticalFilmOffset',id=True):

        horFilmOffset = -(cmds.getAttr(camShape+'.horizontalFilmOffset')/cmds.getAttr(camShape+'.horizontalFilmAperture'))
        verFilmOffset = -(cmds.getAttr(camShape+'.verticalFilmOffset')/cmds.getAttr(camShape+'.horizontalFilmAperture'))
        #cmds.getAttr(fCameraShape+'.verticalFilmAperture'))
        cmds.setAttr(loc+'.tx', horFilmOffset)
        cmds.setAttr(loc+'.ty', verFilmOffset)
        bakeFilmOffset = 0



    #setKeyframe Transform attribute and filmOffset
    keyAttr=["tx","ty","tz","rx","ry","rz"]
    for i in range(minTime, maxTime):
        cmds.currentTime(i)
        xformLi = cmds.xform(cam,q=True, ws=True, m=True)
        cmds.xform(newCam,ws=True, m=xformLi)
        cmds.setKeyframe(newCam,at=keyAttr)

        cmds.setKeyframe(str(newCamShape), at='focalLength', v=cmds.getAttr(camShape+'.focalLength') )


        #bake filmOffset
        if bakeFilmOffset:
            horFilmOffset = -(cmds.getAttr(camShape+'.horizontalFilmOffset')/cmds.getAttr(camShape+'.horizontalFilmAperture'))
            verFilmOffset = -(cmds.getAttr(camShape+'.verticalFilmOffset')/cmds.getAttr(camShape+'.horizontalFilmAperture'))
            cmds.setAttr(loc+'.tx', horFilmOffset)
            cmds.setAttr(loc+'.ty', verFilmOffset)
            cmds.setKeyframe(loc,at='tx')
            cmds.setKeyframe(loc,at='ty')




    #setAttr
    #set attribute fitResolutionGate to Vertical
    cmds.setAttr('%s.filmFit'%(newCamShape),1)

    #deviceAspectRatio = cmds.getAttr('defaultResolution.deviceAspectRatio')
    #vfa = cmds.getAttr(fCameraShape+'.verticalFilmAperture')


    cmds.setAttr(newCamShape+'.horizontalFilmAperture', cmds.getAttr(camShape+'.horizontalFilmAperture'))
    cmds.setAttr(newCamShape+'.verticalFilmAperture',cmds.getAttr(camShape+'.verticalFilmAperture'))
    return [newCam, loc]





def toNukeCam():
    '''{'path':'Nuke/toNukeCam()',
'icon':':/camera.png',
'tip' : '烘赔camera',
'usage':'$fun()',
}
'''
    cam = cmds.ls(sl=True)
    bakeCam = cmds.camera(n='%sBake'%cam[0])[0]

    fCameraShape = pm.PyNode(cam[0]).getShape()
    bakeCamShape = pm.PyNode(bakeCam).getShape()

    minTime = int( cmds.playbackOptions(q=True,min=True) )
    maxTime = int( cmds.playbackOptions(q=True,max=True)+1 )

    bakeFilmOffset = 1
    cmds.setAttr('%s.filmFit'%(bakeCamShape),2)
    #set filmOffset
    if not cmds.connectionInfo(fCameraShape+'.horizontalFilmOffset',id=True) and \
            not cmds.connectionInfo(fCameraShape+'.verticalFilmOffset',id=True):
        #filmOffset = cmds.getAttr(fCameraShape+'.filmOffset')
        hfa = cmds.getAttr(fCameraShape+'.horizontalFilmAperture')
        hfo = cmds.getAttr(fCameraShape+'.horizontalFilmOffset')
        hFilmOffset = hfo/hfa*2

        #resH = float(cmds.getAttr('defaultResolution.height'))
        #resW = cmds.getAttr('defaultResolution.width')
        #vfa = cmds.getAttr(fCameraShape+'.verticalFilmAperture')
        vfo = cmds.getAttr(fCameraShape+'.verticalFilmOffset')
        vFilmOffset = vfo/hfa*2

        cmds.setAttr(bakeCamShape+'.filmOffset', hFilmOffset,vFilmOffset, type='double2' )

        bakeFilmOffset = 0




    #setKeyframe Transform attribute and filmOffset
    keyAttr=["tx","ty","tz","rx","ry","rz"]
    for i in range(minTime, maxTime):
        cmds.currentTime(i)
        xformLi = cmds.xform(cam[0],q=True, ws=True, m=True)
        cmds.xform(bakeCam,ws=True, m=xformLi)
        cmds.setKeyframe(bakeCam,at=keyAttr)


        cmds.setKeyframe(str(bakeCamShape), at='focalLength', v=cmds.getAttr(fCameraShape+'.focalLength') )

        #bake filmOffset
        if bakeFilmOffset:
            filmOffset = cmds.getAttr(fCameraShape+'.filmOffset')
            hfa = cmds.getAttr(fCameraShape+'.horizontalFilmAperture')
            hfo = cmds.getAttr(fCameraShape+'.horizontalFilmOffset')
            hFilmOffset = hfo/hfa*2

            #resH = float(cmds.getAttr('defaultResolution.height'))
            #resW = cmds.getAttr('defaultResolution.width')
            #vfa = cmds.getAttr(fCameraShape+'.verticalFilmAperture')
            vfo = cmds.getAttr(fCameraShape+'.verticalFilmOffset')
            vFilmOffset = vfo/hfa*2

            cmds.setAttr(bakeCamShape+'.filmOffset', hFilmOffset,vFilmOffset, type='double2' )
            cmds.setKeyframe(str(bakeCamShape),at='filmOffset')
            
            
def renameX(objects=None, prefix=None):
    '''{'path':'Modify/renameX( )',
'icon':'rename.png',
'tip' : '修复选择物体的shape节点的命名',
'usage':'$fun( )',
}
'''
    if isinstance(objects, (str, unicode)):
        objects = [objects]
    
    if objects:
        objects = [obj for obj in objects if cmds.objExists(obj)]
    
    if not objects:
        objects = cmds.ls(sl=True, exactType='transform', l=True)
    
    if not objects:
        raise IOError( 'Select a object or assign object from first arguments!')
    newName = []
    for obj in objects:
        if prefix:
            obj = cmds.rename( obj, prefix+'#')
        shortName = obj.rsplit('|', 1)[-1]
        shape = cmds.listRelatives( obj, shapes=True, f=True)[0]
        shapeShortName = shape.rsplit('|', 1)[-1]
        if shapeShortName != shortName+'Shape':
            cmds.rename( shape, shortName+'Shape')
        newName.append( obj )
    return newName

          
def getAllAttrs(object=None, excludeAttrs=None, frameRange=None):
    frameRange = frameRange if frameRange else (cmds.playbackOptions( q=True, min=True ), cmds.playbackOptions( q=True, max=True )   )
    frameRange = ( int(frameRange[0]),  int(frameRange[1])+1  )
 
   
    attrsData = {}
    stringAttrs = [attr
                   for attr in cmds.listAttr(object,  write=True, read=True, visible=True, hasData=True) 
                   if cmds.objExists( '%s.%s'%(object, attr) ) and cmds.getAttr( '%s.%s'%(object, attr), sl=True, type=True)=='string'
                   ]
    attrs = cmds.listAttr( object, multi=True, write=True, scalar=True, visible=True, hasData=True)
    attrs = stringAttrs+attrs
    animAttrs = [attr for attr in attrs if cmds.listConnections(object+'.'+attr, d=False, shapes=True) ]
    attrs = set( attrs ).difference( set(animAttrs) )
    
    animAttrs = list( set(animAttrs).difference(excludeAttrs) )  if excludeAttrs  else  animAttrs
    attrs = list( attrs.difference( excludeAttrs ) ) if excludeAttrs else list( attrs )
    
    attrs.sort()
    for attr in attrs:
        try:
            value = cmds.getAttr( '%s.%s'%(object, attr), sl=True )
        except:        
            raise AttributeError( '%s.%s'%(object,attr) )
        if value!=None:
            attrsData[attr] = value
    
    
    #Get animation data
    animData = {}
    for key in animAttrs:
        animData[key] = []
    for i in range( frameRange[0], frameRange[1]):
        for attr in animAttrs:
            value = cmds.getAttr( object+'.'+attr, time=i )
            animData[attr].append( (i,value) )
            
    #Optimize animation data
    for attr, values in animData.iteritems():        
        toRemove = []
        for i in range( 1, len(values)-1 ):
            if values[i-1][1]==values[i][1]==values[i+1][1]:
                toRemove.append( values[i] )
                
        for v in toRemove:
            values.remove( v )
        
        if len( values )==2 and values[0][1]==values[1][1]:
            values = values[0][1]
        attrsData[attr] = values
    
    return attrsData



def saveJsonAttrsPreset( **kwargs):
    '''{'del_path':'Cache/saveJsonAttrsPreset( )',
'icon':'$ICONDIR/json.png',
'html':True,
'usage':"""
$fun(objects=cmds.ls(sl=True, l=True), jsonFilePath=None, outJsonFile=True, outLocatorAttr=False )
""",
}
'''
    indentNum = kwargs.get('indent', None)
    objects = kwargs.get('objects', None)
    outJsonFile = kwargs.get( 'outJsonFile', True)
    
    outLocatorAttr = kwargs.get( 'outLocatorAttr', None)
    
    
    jsonFilePath = kwargs.get( 'jsonFilePath', None )
    
    
    if objects:
        if isinstance(objects, (str, unicode) ):
            objects = [objects, ]
        objects = [obj for obj in objects if cmds.objExists(obj) ]
    else:
        objects = cmds.ls(sl=True, l=True)
    hairSysAttrs = {}
    hairSysAttrs['fileName'] = cmds.file( q=True, shortName=True, sceneName=True)
    for obj in objects:
        nodeT = cmds.nodeType( obj )
        if not hairSysAttrs.has_key(nodeT):
            hairSysAttrs[nodeT] = {}        
        attrsDir = getAllAttrs(object=obj, excludeAttrs=['currentTime', 'startFrame'] )
        hairSysAttrs[nodeT][obj] = attrsDir
    
    
    jsonStr = json.dumps( hairSysAttrs, indent=indentNum )
    sceneName = cmds.file( q=True, shortName=True, sceneName=True)
    if outJsonFile:
        if not jsonFilePath:
            sceneName = cmds.file( q=True,  sceneName=True)
            jsonFilePath = os.path.splitext( sceneName )[0]+'.json'.replace('\\', '/')
        
        jsonFile = open( jsonFilePath, 'w' )        
        jsonFile.write( jsonStr )
        jsonFile.close()
        os.startfile(  os.path.dirname( jsonFilePath )   )
        return jsonFilePath
    
    if outLocatorAttr:
        createNewLocator = True
        if isinstance(outLocatorAttr, (str,unicode) ):
            locatorName, locAttr = outLocatorAttr.split('.')
            if cmds.objExists( locObj ):
                createNewLocator = False
        
        if createNewLocator:
            sceneName = cmds.file( q=True,  sceneName=True, shortName=True).replace( '.', '_')
            locatorName = sceneName + '_INFO'
            locAttr = 'attributePresets'
            if not cmds.objExists( locatorName ):
                locatorName = cmds.spaceLocator( name = locatorName )[0]
            
        qm.delAttr( locatorName, [locAttr,])
        cmds.addAttr( locatorName, ln=locAttr, dt='string', hidden=True )
        
        cmds.setAttr( '%s.%s'%(locatorName, locAttr), jsonStr, type='string', l=True)
        return locatorName


def loadJsonAttrsPreset( **kwargs ):
    '''{'del_path':'Cache/loadJsonAttrsPreset( )',
'icon':'$ICONDIR/josn.png',
'html':True,
'usage':"""
$fun( objects=None, jsonPreset=None, keyFromAttr=None )""",
}
'''
    
    objects = kwargs.get( 'objects', None)
    jsonPreset = kwargs.get( 'jsonPreset', None)
    keyFromAttr = kwargs.get( 'keyFromAttr', None)
    
    
    if not jsonPreset:
        raise IOError( 'First arguments must be Json File or Json string!')
    
    if objects:
        if isinstance(objects, (str, unicode) ):
            objects = [objects, ]
        objects = [obj for obj in objects if cmds.objExists(obj) ]
    else:
        objects = cmds.ls(sl=True, l=True)
    
    if not objects:
        raise IOError( 'Select a object or assign!')
    
    try:
        if os.path.exists( jsonPreset ):
            jsonFile = open( jsonPreset )
            jsonData = json.load( jsonFile )
            jsonFile.close()
        else:
            jsonData = json.loads( jsonPreset )
    except:
        raise IOError( 'Got a error from second argument jsonString!')
    
    
    #print 'File Name:\t', jsonData.get( 'fileName', None)
    for obj in objects:
        nodeT = cmds.nodeType( obj )
        
        if not jsonData.get( nodeT, None):            
            continue
        
        keyName = obj
        if keyFromAttr:
            if not cmds.attributeQuery( keyFromAttr, node=obj, exists=True):
                cmds.warning( "%s.%s is not exists!"%(obj, keyFromAttr)  )
                continue           
            keyName = cmds.getAttr( obj+'.'+keyFromAttr)
            if not keyName:
                cmds.warning( "%s.%s value is empty!"%(obj, keyFromAttr) )
        
        if not jsonData[nodeT].get(keyName, None):
            cmds.warning( "%s key is not exists!"%(keyName) )
            continue
        
        
        for attr, value in jsonData[nodeT][keyName].iteritems():
            if not cmds.attributeQuery( attr, node=obj, exists=True):
                createNewAttr = True
                if '.' in attr or '[' in attr:
                    sepAttr = attr.split('.')[0].split('[')[0]
                    if cmds.attributeQuery( sepAttr, node=obj, exists=True):
                        createNewAttr = False
                if createNewAttr:
                    if isinstance( value, (str, unicode) ):
                        cmds.addAttr( obj, ln=attr, dt='string' )
                    else:
                        cmds.addAttr( obj, ln=attr, dt='double')
            
            fullAttrName = obj+'.'+attr
            if cmds.getAttr( fullAttrName, l=True  ):
                cmds.setAttr( fullAttrName, l=False)
            
            if cmds.listConnections( fullAttrName, d=False):
                continue
            
            if isinstance( value, list):
                for f, v in value:
                    cmds.setKeyframe( obj, at=attr, t=f, v=v)
            elif isinstance( value, (str, unicode) ):
                cmds.setAttr( fullAttrName, value, type='string' )                
            else:
                cmds.setAttr( fullAttrName, value)
                


def selectDisplaySmoothnessObjects():
    '''{'path':'Polygons/EditMesh/selectDisplaySmoothnessObjects( )',
'icon':':/subdivPolyMode.png',
'html':False,
'usage':"""
#选择当前选择的物体中按3显示的mesh物体
$fun( )""",
}
'''
    allMeshFullPath = cmds.listRelatives(cmds.ls(sl=True), type='mesh', noIntermediate=True, ad=True, f=True )
    allMeshFullPath = [child for child in allMeshFullPath if not cmds.getAttr( child+'.intermediateObject') ]
    smoothed = [obj for obj in allMeshFullPath if cmds.displaySmoothness( obj, q=True, polygonObject=True)[0]>1  ]
    cmds.select( smoothed, r=True)



class OutCacheInfo(object):
    _menuStr = '''{'del_path':'Cache/OutCacheInfo().getAllCache_maya(saveJson=True)',
'icon':'$ICONDIR/json.png',
'tip' :  '输出缓存信息到一个json文件',
'usage':"""
#选择当前选择的物体中按3显示的mesh物体
#包括的节点缓存类型有：
#   cacheFile
#   AlembicNode(*.abc)
#   mental ray proxy(*.mi）
#   aiStandIn(*.ass)
#   VRayMesh(*.vrmesh)
$fun().getAllCache_maya(saveJson=True)""",
}
'''
    def __init__(self):
        self.__nodeAttrs = {
                            'cacheFile':      [None, self.__get_cacheFile ],
                            'AlembicNode':    ["AbcImport.mll", self.__get_AlembicNode ],
                            'miProxy':        ['Mayatomr.mll', self.__get_miProxy ],
                            'aiStandIn':      ['mtoa.mll',    self.__get_aiStadin ],
                            'VRayMesh':       ['vrayformaya.mll', self.__get_VRayMesh ]
                  }

        self.__loadedNodes = []
        for k, v in self.__nodeAttrs.iteritems():
            if not v[0] or\
                    ( v[0] and cmds.pluginInfo( v[0], query=True, registered=True) and cmds.pluginInfo( v[0], query=True, loaded=True)  ):
                self.__loadedNodes.append( k )


    def __get_cacheFile(self,*args):
        cacheFileData = {}
        nodes = cmds.ls( exactType='cacheFile' )
        for node in nodes:
            curData = []
            cacheDir = cmds.getAttr( node+'.cachePath', x=True)
            cacheName = cmds.getAttr( node+'.cacheName', x=True )
            xmlFile = (cacheDir + cacheName + '.xml').replace( '\\', '/')
            if not xmlFile or not os.path.exists( xmlFile ):
                continue
            curData.extend( [os.path.join(cacheDir, fileName).replace('\\', '/')
                             for fileName in os.listdir(cacheDir)
                             if fileName.startswith(cacheName)  ]
                           )

            cacheFileData[node] = curData
        return cacheFileData

    def __get_AlembicNode(self, *args):
        abcData = {}
        alembicNodes = cmds.ls( exactType='AlembicNode' )
        for node in alembicNodes:
            cacheDir = cmds.getAttr( node+'.abc_File', x=True)
            if cacheDir and os.path.exists( cacheDir ):
                abcData[node] = [cacheDir]
        return abcData

    def __get_miProxy(self, *args):
        miData = {}
        allMesh = cmds.ls(exactType=['mesh','nurbsSurface'], noIntermediate=False)
        allMesh = [child for child in allMesh if not cmds.getAttr( child+'.intermediateObject') ]
        for mesh in allMesh:
            mi = cmds.getAttr( mesh+'.miProxyFile', x=True)
            if mi and os.path.exists( mi ):
                miData[mesh] = [mi]
        return miData


    def __get_aiStadin(self, *args):
        assData = {}
        assNodes = cmds.ls( exactType='aiStandIn' )
        for node in assNodes:
            assFilePath = cmds.getAttr( node +'.dso', x=True )
            dirName = os.path.dirname(assFilePath)
            if not assFilePath or not os.path.exists(dirName):
                continue

            if os.path.exists(assFilePath):
                assData[node] = [assFilePath]
                continue

            baseName = os.path.basename( assFilePath )
            sindex = baseName.find('#')
            if sindex==-1:
                continue
            startStr = baseName[:sindex]
            assData[node] = [os.path.join(dirName, f).replace('\\', '/')
                             for f in os.listdir( dirName )
                             if f.startswith(startStr) ]
        return assData


    def __get_VRayMesh(self, *args):
        vrayData = {}
        nodes = cmds.ls( exactType='VRayMesh' )
        for node in nodes:
            vrmeshCache = cmds.getAttr( node+'.fileName2', x=True)
            if not vrmeshCache or not os.path.exists( vrmeshCache ):
                continue
            vrayData[node] = [vrmeshCache]
        return vrayData



    def getAllCache_maya( self, *args, **kwargs ):

        scenePath = cmds.file(q=True, sceneName =True )
        cacheData = {  }

        for nt in self.__loadedNodes:
            #if nodes:
            #    cacheData[nt] = {}
            temp = self.__nodeAttrs[nt][1]( )
            if temp:
                cacheData.update( temp )
                #cacheData[nt][node] = nodeAttrs[k][1]( node )

        dirnames = {}
        for caches in cacheData.values():
            for cache in caches:
                dirname = os.path.dirname( cache )
                if not dirnames.has_key(dirname):
                    dirnames[dirname] = []
                dirnames[dirname].append( cache )

        fullFolder = set()
        for dirname, filenames in dirnames.iteritems():
            if len( os.listdir(dirname) ) == len(filenames):
                fullFolder.add( dirname )
        fullFolder = tuple( fullFolder )


        resultCaches = {'caches': {},
                     'files': [  scenePath  ]
                     }
        for node, caches in cacheData.iteritems():
            tempCaches = []
            for cache in caches:
                dirname = os.path.dirname( cache )
                tempCaches.append(  dirname if dirname in fullFolder else cache )
            resultCaches['caches'][node] = tuple( set(tempCaches) )


        if kwargs.get( 'saveJson', None):
            fin = open( scenePath + '_cacheData.json', 'w')
            fin.write( json.dumps( resultCaches, indent=4 ) if kwargs.get('indent', None) else json.dumps( resultCaches ) )
            fin.close()
            print scenePath + '_cacheData.json'
            return scenePath + '_cacheData.json'
        return resultCaches

def app_cacheManage():
    '''{'del_path':'Cache/app_cacheManage( )',
'icon':'$ICONDIR/json.png',
'html':False,
'usage':"""
#\\10.99.1.6\Digital\Library\hq_toolbox\apps\cacheManage_Main.exe
#这个应用的一个快捷方式
$fun( )""",
}
'''
    os.startfile( r"\\10.99.1.6\Digital\Library\hq_toolbox\apps\cacheManage_Main.exe" )
