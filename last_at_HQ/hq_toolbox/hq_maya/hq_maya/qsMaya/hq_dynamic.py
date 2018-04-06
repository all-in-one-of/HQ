# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################
import sys
reload( sys)
sys.setdefaultencoding('utf-8')
import random
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import pymel.core.datatypes as dt
import math
from qsMaya.utility import *
import qsMaya as qm



def geoConnectorOnCurveOrMesh():
    '''{'del_path':'Dynamics/geoConnectorOnCurveOrMesh( )',
'icon':':/default.svg',
'tip':'计算点的速度',
'usage':'$fun( )'
}
'''
    geoObj = cmds.ls(sl=True)
    if geoObj!=[]:
        geoObj = geoObj[0]
    else:
        raise IOError( 'select nurbsCurve or mesh object')
    
    objType = cmds.objectType( geoObj )
    
    if objType!='nurbsCurve' and objType!='mesh':
        children = cmds.listRelatives(geoObj, children=True)
        if children==[]:
            raise IOError( 'select nurbsCurve or mesh object')
        objType = cmds.objectType( children[0] )
        if objType!='nurbsCurve' and objType!='mesh':
            raise IOError( 'select nurbsCurve or mesh object')
        else:
            geoObj = children[0]
    
    hasGeo = False
    connectedGeo = cmds.listConnections( geoObj+'.message', destination=True)
    if connectedGeo!=None:
        for node in connectedGeo:
            if cmds.objectType( node ) == 'geoConnector':
                geoConnector = node
                hasGeo=True
                break
    
    if hasGeo==False:
        geoConnector = cmds.createNode( 'geoConnector', name=geoObj+'_geoConnector' )
        
        cmds.connectAttr( geoObj+'.local', geoConnector+'.localGeometry')
        cmds.connectAttr( geoObj+'.message', geoConnector+'.owner')
        cmds.connectAttr( geoObj+'.worldMatrix[0]', geoConnector+'.worldMatrix')
        cmds.connectAttr( 'time1.outTime', geoConnector+'.currentTime')
    
       
    if cmds.attributeQuery( 'geoConnector', node=geoObj, exists=True)==False:
        cmds.addAttr( geoObj, ln='geoConnector', dataType='string')
    else:
        if cmds.getAttr( geoObj+'.geoConnector', lock=True):
            cmds.setAttr( geoObj+'.geoConnector', lock=Flase)
    
    cmds.setAttr( geoObj+'.geoConnector', geoConnector, type='string')
    return geoConnector

def lookFluidEmitter(  ):
    '''{'del_path':'Dynamics/Fluid Effects/lookFluidEmitter( )',
'icon':':/fluidCreate3DEmitter.png',
'tip':'帮助查看fluidEmitter的设置',
'usage':'$fun( )'
}
'''
    fluEm = pm.ls(sl=True, exactType='fluidEmitter')
    if not fluEm:
        raise IOError( 'Select a fluidEmitter!')
    fluEm = fluEm[0]
    fluEm = pm.ls(sl=True, exactType='fluidEmitter')[0]
    type = cmds.getAttr(fluEm.name()+'.emitterType')
    if type==2 or type==4:
        temp = fluEm.visibility.get()
        fluEm.v.set(True)
        size = cmds.getAttr(fluEm.name()+'.bbsi')[0]
        fluEm.v.set(temp)
        if type == 2:
            temp = fluEm.getParent().v.get()
            fluEm.getParent().v.set(True)
            size = cmds.getAttr(fluEm.getParent().name()+'.bbsi')[0]
            fluEm.getParent().v.set(temp)
        size = dt.Vector(math.ceil(size[0]), math.ceil(size[1]), math.ceil(size[2]))
        shape = pm.createNode('fluidShape')
        papa = shape.getParent().rename(fluEm.name()+'_attr')
        papa.setTranslation(fluEm.getTranslation('world'), space='world')
        shape = papa.getShape()
        cmds.connectAttr('time1.outTime', shape.name()+'.currentTime')
        pm.connectDynamic(shape, em=fluEm)
        cmds.setAttr(shape.name()+'.velocityMethod', 0)
        shape.setSize( 20, 20, 20, size.x, size.y, size.z, False)
        shape.ambientBrightness.set(1)
        shape.selfShadowing.set(True)
        shape.primaryVisibility.set(False)
    else:
        raise IOError('fluid emitter work when emitterType is Surface and Volume only')

def addInputForceAttrForPar():
    '''{'del_path':'Dynamics/Particles/addInputForceAttrForPar()',
'icon':':/particle.png',
'tip':'创建和粒子相关的inputforce属性',
'usage':'$fun( )',
'help':"""
<p>inputforce属性可以用来判断哪些field作用于粒子的强度是多少。</p>
<p>属性是创建在粒子节点下面的，可以很方便查看哪个field是和粒子的inputfouce[*]相关联的。</p>
"""
}
'''
    #if isinstance( parShapeList, str) or isinstance( parShapeList, unicode ):
        #parShapeList = [parShapeList]
    parShapeList = cmds.ls( type='particle', l=True)
    if not parShapeList:
        return
    
    for parShape in parShapeList:
        attrLi =  cmds.listAttr(parShape, st='*_to')
        if attrLi:
            delAttr(parShape, attrLi )

        ifLi = cmds.getAttr('%s.inputForce'%(parShape),mi=True)
        if ifLi:
            for ifOrder in ifLi:
                forceName = cmds.listConnections('%s.inputForce[%s]'%(parShape,ifOrder), d=False, scn=True)
                if forceName is not None:
                    forceName = cmds.ls(forceName, shortNames=True)[0]
                    print forceName
                    cmds.addAttr(parShape, ln='%s_to'%(forceName), dt='string')
                    cmds.setAttr('%s.%s_to'%(parShape,forceName), 'inputForce[%s]'%(ifOrder), type='string', l=True)



def qsEmit(object, position, attributes, clearAndSaveState=True, **kwargs):
    '''{'del_path':'Dynamics/Particles/qsEmit("particleShape", position=posLi, attributes=(("cus_bbsi", "vectorValue", bbsiLi), ("cus_area", "floatValue", areaLi) ), clearAndSaveState=True  )ONLYSE',
'icon':':/particle.svg',
'tip':'创建粒子',
'usage':'\
objects = cmds.listRelatives(cmds.ls(sl=True, exactType="transform", l=True), type="transform",f=True)\\n\
posLi, radiusLi, atULi, atVLi = [], [], [], []\\n\
for tfNode in objects:\\n\
    objPos = cmds.objectCenter(tfNode)\\n\
    bbsize = cmds.getAttr(tfNode+".bbsi")[0]\\n\
    radius = qm.vectorLen(bbsize)/2\\n\
    atU = cmds.getAttr(tfNode+".atU")\\n\
    atV = cmds.getAttr(tfNode+".atV")\\n\
    posLi.append(objPos)\\n\
    radiusLi.append(radius)\\n\
    atULi.append(atU)\\n\
    atVLi.append(atV)\\n\
$fun(object = "new", position=posLi, attributes=[("cus_bbsi", "floatValue", radiusLi), ("cus_area", "floatValue", areaLi) ]    )',
'help':'对emit command重新进行了一下打包',
}
'''

    createNew = True
    parType = ('particle', 'nParticle')
    if cmds.objExists(object):
        if cmds.objectType(object) in parType:
            createNew = False
        else:
            shapes = cmds.listRelatives(object, shapes=True)[0]
            if cmds.objExists(shapes) in parType:
                object=shapes
                createNew = False


    if createNew:
        if kwargs.get( 'type', None)=='particle':
            nPar = cmds.particle()
        else:
            nPar = cmds.nParticle()
        object = nPar[1]


    #if cmds.objectType(object) != 'nParticle':
        #raise IOError('%s is not nParticle object'%object)

    posLen = len(position)

    for attr in list(attributes):
        if len(attr[2]) != posLen:
            if createNew:
                cmds.delete( cmds.listRelatives(object, parent) )
            raise IOError('%s count is difence with position count'%(attr[0]) )

    for attr in attributes:
        if cmds.attributeQuery(attr[0], node=object, exists=True) == False:
            print attr[1]
            if attr[1] == 'floatValue': attrType = 'doubleArray'
            elif attr[1] == 'vectorValue': attrType = 'vectorArray'
            else:
                raise IOError('value type is not floatValue or vectorValue')
            cmds.addAttr(object,ln=attr[0]+'0', dt=attrType)
            cmds.addAttr(object,ln=attr[0], dt=attrType)

    emitStr = 'emit -object %s '%(object)
    for data in position:
        emitStr += ' -pos %s %s %s '%(data[0], data[1], data[2])

    if clearAndSaveState:
        startF = cmds.playbackOptions(q=True,min=True)
        cmds.currentTime(startF+1,e=True)
        mel.eval("clearParticleStartState %s"%(object) )
        cmds.currentTime(startF,e=True)

    for attr in attributes:
        emitStr +='\n\n-attribute %s '%(attr[0])
        if attr[1] == 'floatValue':
            for data in attr[2]:
                emitStr += ' -%s %s  '%(attr[1], data)
        elif attr[1] == 'vectorValue':
            for data in attr[2]:
                emitStr += ' -%s %s %s %s  '%(attr[1], data[0], data[1], data[2])
        else:
            raise IOError('value type is not floatValue or vectorValue')
    #return emitStr
    mel.eval(emitStr)
    if clearAndSaveState:
        cmds.saveInitialState( object )
    return object

def objsToPar(parName=None, initialState=True):
    """{'del_path':'Dynamics/Particles/objsToPar(parName=None, initialState=True)ONLYSE',
'icon':':/particle.png',
'tip':'选择的组下面的每个物体中心创建一个粒子',
'usage':'$fun(parName=None, initialState=True)',
'help':'''<pre>
parName:
    如果不指定粒子节点的名字，则创建一个新的粒子；
initialState:
    为粒子设不设置初始状态。
''',
}
"""
    grp = cmds.ls(sl=True)
    objects = cmds.listRelatives(grp, type='transform',f=True)
    posLi, radiusLi, cus_objGrp = [], [], []
    for tfNode in objects:
        objPos = cmds.objectCenter(tfNode)
        posLi.append(objPos)

    qsEmit(object = parName, position=posLi, attributes=[], clearAndSaveState=initialState     )

def createCurveFromParticles(parObj, replace=False, disCVOnly=True):
    '''{'del_path':'Dynamics/Particles/createCurveFromParticles( cmds.ls(sl=True)[0], replace=False, disCVOnly=True )',
'usage':'$fun(  cmds.ls(sl=True)[0] )',
'icon':':/menuIconCurves.png',
'tip':'在每个位置上创建一根曲线',
}
'''

    #parObj='nParticle2'
    if cmds.objectType(parObj)=='transform':
        if cmds.listRelatives(parObj, shapes=True, type=('particle', 'nParticle') ) == None:
            raise IOError( '%s is not particle or nParticle'%(parObj) )
    elif cmds.objectType(parObj)!='particle' and cmds.objectType(parObj)!='nParticle':
        raise IOError( '%s is not particle or nParticle'%(parObj) )

    cvPos = []
    parPos = cmds.getParticleAttr(parObj, at='position', array=True)
    for i in range(0, len(parPos), 3 ):
        cvPos.append( (parPos[i], parPos[i+1], parPos[i+2]) )



    curveName = parObj+'_01'
    if replace==True:
        if cmds.objExists(curveName)==False:
            curveNode = cmds.curve(name=curveName, d=1, p=([0,0,0]))
            curveShape =  cmds.listRelatives(curveNode, shapes=True)[0]
    else:
        curveNode = cmds.curve(name=curveName, d=1, p=([0,0,0]))
        curveShape =  cmds.listRelatives(curveNode, shapes=True)[0]

    cmds.curve(curveNode, r=True, p=cvPos)
    if disCVOnly:
        cmds.setAttr(curveShape+'.dispCV', 1)
        cmds.setAttr(curveShape+'.dispGeometry', 0)

    cmds.select(curveNode, r=True)
    return curveNode

def createCurveFromObjectsPos(objects, useConnectAttr=False, usePointConstraint=False, name=None):
    '''{'del_path':'Dynamics/Particles/createCurveFromObjectsPos( cmds.ls(sl=True, exactType="transform", l=True), useConnectAttr=False, usePointConstraint=False, name=None )',
'tip':'从选择的物体的位置，创建曲线',
'icon':':/menuIconCurve.png',
'usage':"""
$fun(  cmds.ls(sl=True, exactType="transform"), useConnectAttr=False, usePointConstraint=False, name=None )
#global string $emitList[];
#$emitList = `listRelatives -ad -type "pointEmitter" "group"`;""",
'help':"""<pre>
useConnectAttr:
    将物体的translate关联到曲线的cvpos属性；
usePointConstraint:
    将曲线的cvpos约束到物体的位置上。
</pre>
""",
}
'''
    if isinstance( objects, str) or isinstance( objects, unicode ):
        objects = [objects]

    if len(objects) == 0:
        raise IOError('No objects selected!')

    if name==None:
        name = 'pointObj'

    #name = 'pointObj_secCurve'
    createNew = True
    if name!=None:
        if cmds.objExists(name):
            shapes = cmds.listRelatives(name, type='nurbsCurve')
            if cmds.objectType(name)=='nurbsCurve':
                curveNode = cmds.listRealtives(name, p=True)[0]
                curveShape = name
                createNew = False
            elif shapes!=[] and cmds.objectType(shapes[0])=='nurbsCurve':
                curveNode = name
                curveShape = shapes[0]
                createNew = False

    if createNew:
        curveNode = cmds.curve(name=name, d=1, p=([0,0,0]))
        curveShape =  cmds.listRelatives(curveNode, shapes=True)[0]


    pointsPos = []
    for obj in objects:
        #pointsPos.append( cmds.getAttr(obj+'.t')[0] )
        pointsPos.append( cmds.objectCenter(obj) )


    cmds.curve(curveNode, r=True, p=pointsPos)
    #curveNode = cmds.curve(name=name, d=1,  p=pointsPos)
    #curveShape = cmds.listRelatives(curveNode, shapes=True)[0]


    if useConnectAttr:
        for i in range( len(objects) ):
            cmds.connectAttr( objects[i]+'.translate', '%s.controlPoints[%s]'%(curveShape, i)  )
    elif usePointConstraint==True:
        for tfObj in objects:
            pointCon = cmds.createNode('pointConstraint',p=curveNode)
            cmds.connectAttr('%s.rotatePivotTranslate'%tfObj, '%s.target[0].targetRotateTranslate'%pointCon)
            cmds.connectAttr('%s.parentMatrix[0]'%tfObj, '%s.target[0].targetParentMatrix'%pointCon)
            cmds.connectAttr('%s.translate'%tfObj, '%s.target[0].targetTranslate'%pointCon)
            cmds.connectAttr('%s.rotatePivot'%tfObj, '%s.target[0].targetRotatePivot'%pointCon)

            cmds.connectAttr('%s.constraintTranslate'%pointCon, '%s.controlPoints[%s]'%(curveShape, objects.index(tfObj)) )
            cmds.setAttr('%s.intermediateObject'%pointCon, 1)

    cmds.setAttr('%s.template'%curveShape, 1)
    cmds.select(curveNode, r=True)
    return curveNode

def pointEmitterVel(pointEmitterList, vertexCount=5):
    '''{'del_path':'Dynamics/Particles/Emitter/pointEmitterVel()ONLYSE',
'icon':':/posEmitter.png',
'tip':'获得粒子发射的速度',
'usage':'\
##########Get geoConnector node to connected pointEmitterNode\\n\
poEmLi = cmds.listRelatives(  cmds.ls(sl=True)[0], ad=True, type="pointEmitter", f=True )\\n\
geoConNode = cmds.listConnections("%s.sweptGeometry"%(poEm), d=False, scn=True, type="geoConnector")\\n\
if  geoConNode:\\n\
    geoConNode = geoConNode[0]\\n\\n\
else:\\n\
    print "%s not have geoConnector node to connected it"\\n\\n\
$fun(cmds.ls(sl=True, exactType="pointEmitter", l=True), vertexCount=5)\\n\
pointEmitterList = cmds.listRelatives(  cmds.ls(slTrue), ad=True, type="pointEmitter", f=True )\\n\
$fun(pointEmitterList, vertexCount=5)'
}
'''

    if isinstance( pointEmitterList, str) or isinstance( pointEmitterList, unicode ):
        pointEmitterList = [pointEmitterList]


    resultList = []
    for pointEmitter in pointEmitterList:
        velLi = cmds.getAttr( '%s.ownerVelData'%(pointEmitter)   )
        velLen = len(velLi)
        step = velLen/vertexCount
        vertexCount = step
        if step < 5:
            step = 1
            vertexCount = velLen
        speed = 0
        for vel in velLi[:-1:step]:
            speed +=math.sqrt(vel[0]*vel[0] + vel[1]*vel[1] + vel[2]*vel[2])
            #speed+= newom.MVector(vel).length()

        resultList.append( speed/vertexCount )
    return resultList


def getPointEmitterFromCurveCPs(curveShape):
    '''{'del_path':'Dynamics/Particles/Emitter/getEmitterFromCurveControlPoints(curveShape)ONLYSE',
'icon':':/posEmitter.png',
'tip':'?_?',
'usage':'emitters = $fun(curveShape)',
}
'''
    #if str( cmds.getAttr(meshPntsAttr, type=True) ) != 'TdataCompound':
        #raise IOError('%s is not TdataCompound attribute'%meshPntsAttr)
    attr = curveShape+'.controlPoints'
    #compoundAttr = 'pointObjShape.pnts'
    resultList = []
    sequence = cmds.getAttr(attr, mi=True)
    if sequence:
        for index in sequence:
            pointCon = cmds.listConnections('%s[%s]'%(attr,index), d=False, scn=True)
            if pointCon is not None:
                tfObj = cmds.listConnections('%s.target[0].targetTranslate'%(pointCon[0]), d=False, scn=True)
                if tfObj is not None:
                    resultList.append(tfObj[0])
    return resultList



def objectsFromPolyEmitter(meshPntsAttr):
    '''{'del_path':'Dynamics/Particles/Emitter/objectsFromPolyEmitter(meshPntsAttr)ONLYSE',
'icon':':/emitter.png',
'tip':'?_?',
'usage':'objects = $fun("mesh.pnts")',
}
'''
    if str( cmds.getAttr(meshPntsAttr, type=True) ) != 'TdataCompound':
        raise IOError('%s is not TdataCompound attribute'%meshPntsAttr)

    #compoundAttr = 'pointObjShape.pnts'
    resultList = []
    sequence = cmds.getAttr(meshPntsAttr, mi=True)
    if sequence:
        for index in sequence:
            pointCon = cmds.listConnections('%s[%s]'%(meshPntsAttr,index), d=False, scn=True)
            if pointCon is not None:
                tfObj = cmds.listConnections("%s.target[0].targetTranslate"%(pointCon[0]), d=False, scn=True)
                if tfObj is not None:
                    resultList.append(tfObj[0])
    return resultList




def createPoEmByShaderAndObjList(includeObjects,shaderList, **kwargs):
    '''{'del_path':'Dynamics/Particles/Emitter/createPoEmByShaderAndObjList()ONLYSE',
'icon':':/emitter.png',
'tip':'指定某些材质的面创建pointEmitter',
'usage':'\
    ########## No creation new uvsets##########\\n\
    objectList = cmds.ls(sl=True)\\n\
    for obj in objectList:\\n\
        fCount = cmds.polyEvaluate(obj,f=True)\\n\
        cmds.polyProjection("%s.f[0:%s]"%(obj,fCount), ch=False, type="Planar", ibd=False, cm=False, md="x")\\n\
    ##########################################\\n\
includeObjects = cmds.ls(sl=True,exactType="transform")\\n\
shaderList = cmds.ls(sl=True,mat=True)\\n\
$fun(includeObjects, shaderList, uvSetName="forEm", plannarMapping=False,mapDirectionValue="x")\\n\\n\
shaderList = cmds.ls(sl=True,mat=True)\\n\
includeObjects = cmds.listRelatives(cmds.ls(sl=True)[0],type="transform")\\n\
$fun(includeObjects, shaderList, uvSetName="forEm", plannarMapping=False,mapDirectionValue="x")'
}
'''
    if isinstance(includeObjects, str) or isinstance( includeObjects, unicode ):
        includeObjects = [includeObjects]
    if isinstance(shaderList, str) or isinstance( shaderList, unicode ):
        shaderList = [shaderList]


    defalutKwargs = dict(\
                         uvSetName='forEm', \
                         plannarMapping=False,\
                         mapDirectionValue='x'\
                         )


    execStr = __check_kwargs(defalutKwargs, kwargs)
    exec execStr
    print plannarMapping, uvSetName

    cmds.constructionHistory(toggle=False)


    includeObjects += cmds.listRelatives(includeObjects, type='mesh')
    #create ramp for emitter of textureRate
    if not cmds.objExists("uvEmMap"): #and not cmds.objectType('uvEmMap')=="ramp":
        emitMat = cmds.shadingNode('ramp',asTexture=True,n="uvEmMap")
        cmds.removeMultiInstance(emitMat+'.colorEntryList[2]', b=True)
        cmds.setAttr(emitMat+'.interpolation',0)
        cmds.setAttr(emitMat+'.colorEntryList[0].color', 0,0,0, type='double3')
        cmds.setAttr(emitMat+'.colorEntryList[1].position', 0.05)
        cmds.setAttr(emitMat+'.colorEntryList[1].color',1, 1, 1, type='double3')
    else:
        emitMat = "uvEmMap"

    for inSideShader in shaderList:
        cmds.hyperShade(objects=inSideShader)
        faceList = cmds.ls(sl=True)

        cmds.select(cl=True)
        emitObjList,faceSet = [],[]

        for faceGrp in faceList:
            emitObj = re.split(r'\.f',faceGrp)[0]
            #worldarea = cmds.polyEvaluate( emitObj, wa=True )
            #if emitObj not in emitObjList and worldarea>maxArea:
            if emitObj not in emitObjList and emitObj in includeObjects:
                emitObjList.append(emitObj)
                #print emitObj
                #append list to faceSet List
                faceSet.append([])

            if emitObj in emitObjList:
                faceSetIndex = emitObjList.index(emitObj)
                #add faceGrp to faceSet[]
                faceSet[faceSetIndex].append(faceGrp)


        #create uvSet for pointEmitter and create pointEmitter for emitObj
        for objFaceGrp in faceSet:
            emitObjIndex = faceSet.index(objFaceGrp)

            parEmit = cmds.emitter(emitObjList[emitObjIndex], type='surf', nsp=.1, tsp=1, srn=1, n='shtterEmit##')[1]

            if objFaceGrp[0] != emitObjList[emitObjIndex]:
                #Delete uvSetName uvset if it exists
                temp = cmds.polyUVSet(emitObjList[emitObjIndex],q=True,allUVSets=True)
                if temp != None and uvSetName in temp:
                    cmds.polyUVSet(emitObjList[emitObjIndex], delete=True, uvSet=uvSetName)

                #create new uvsets
                if plannarMapping:
                    cmds.polyProjection(objFaceGrp, ch=False, type='Planar', ibd=False, cm=True, uvSetName=uvSetName, md=mapDirectionValue)
                #copy uv to uvSetName from map1
                else:
                    emitterUVSet = cmds.polyUVSet(emitObjList[emitObjIndex],  create=True, uvSet=uvSetName)[0]
                    cmds.polyCopyUV( objFaceGrp, uvi='map1', uvs=emitterUVSet, ch=False)

                    firstUVSet = cmds.polyUVSet(emitObjList[emitObjIndex],q=True,allUVSets=True)[0]
                    cmds.polyUVSet(emitObjList[emitObjIndex],currentUVSet=True,uvSet=firstUVSet)

                cmds.setAttr(parEmit+'.enableTextureRate', 1)
                cmds.connectAttr(emitMat+'.outColor', parEmit +'.textureRate')
                geoConnectNodeList = cmds.ls(cmds.listHistory(emitObjList[emitObjIndex],f=True,levels=1), exactType='geoConnector')
                if geoConnectNodeList != []:
                    for geoConnectNode in geoConnectNodeList:
                        cmds.setAttr(geoConnectNode+'.guv', uvSetName, type='string', l=True)

    cmds.constructionHistory(toggle=True)



def inMeshForParExp_str():
    '''{'del_path':'Dynamics/Particles/inMeshForParExp_str()ONLYSE',
'icon':':/polyMesh.png',
'tip':'判断一个位置是不是在多边形内部',
'usage':'\
def inMeshForPar(meshFn, pos):\\n\
    hitPoints = meshFn.allIntersections( newom.MFloatPoint( pos ), newom.MFloatVector( 0, -1, 0 ), newom.MSpace.kWorld, 9999.0,\\n\
                                        False\\n\
                                        )[0]\\n\
    return True if len(hitPoints)%2==1 else False\\n\
meshObj = "pPlaneShape1"\\n\
meshs = newom.MSelectionList()\\n\
meshs.add( meshObj )\\n\
meshDagPath = meshs.getDagPath(0)\\n\
meshFn = newom.MFnMesh(meshDagPath)\\n\
pos = (0,0,0)\\n\\n\
print inMeshForPar(meshFn, pos)'
}
'''

def printParticleInBoundingbox( start, end, parName, once=True):
    '''{'path':'Dynamics/Particles/printParticleInBoundingbox()ONLYSE',
'icon':':/particle.png',
'tip':'和物体穿插的粒子',
'usage':"""
#返回在指定的时间断内和选择的物体的boundingbox相穿插的粒子的id.
#在outline中选择，例如选择每个动画角色的组。
$fun( 1, 48, "nParticle1", once=True)
#start:
#    开始帧
#end:
#    结束帧
#parName:
#    粒子节点的名字
#once:
#    每次穿插都返回，还是每个粒子最多返回一次
""",
'help':"""<pre>
返回在指定的时间断内和选择的物体的boundingbox相穿插的粒子的id.
在outline中选择，例如选择每个动画角色的组。
start:
    开始帧
end:
    结束帧
parName:
    粒子节点的名字
once:
    每次穿插都返回，还是每个粒子最多返回一次
""",
}
'''
    import maya.api.OpenMaya as newom
    objects = cmds.ls(sl=True, type='transform')
    allIds = set()
    allDatas = []
    end = end+1
    for curF in range( start, end):
        cmds.currentTime(curF, e=True)
        parIds = cmds.getParticleAttr(parName, at='particleId', array=True)
        if not parIds:
            continue
        parIds = [int(id) for id in parIds]
        
        bboxes = []
        for obj in objects:
            bbox = cmds.exactWorldBoundingBox( obj, ii=True)
            bboxes.append(  (obj, 
                             newom.MBoundingBox( newom.MPoint(bbox[:3]), newom.MPoint(bbox[3:]))
                             )
                          )
        

        parPos = cmds.getParticleAttr(parName, at='position', array=True)
        
        
        parIdWithPos = [ (  parIds[i], newom.MPoint(parPos[i*3], parPos[i*3+1], parPos[i*3+2]) )
                        for i in range(len(parIds))   ] 
        
        
        
        curFrameContainedIds = set( )
        objsWithIds = []
        for obj, bbox in bboxes:
            curObjContained = []
            for id, pos, in parIdWithPos:
                if bbox.contains( pos ):
                    if once and id in allIds:
                        continue                        
                    curObjContained.append( id )
            
            if curObjContained:
                objsWithIds.append(  (obj, curObjContained) )
                curFrameContainedIds = curFrameContainedIds.union( curObjContained )
        
        if objsWithIds:
            allIds = allIds.union( curFrameContainedIds )
            allDatas.append( (curF, tuple(curFrameContainedIds), objsWithIds)   )
                        
    #allDatas.sort()
    ttCount = 0
    dataStr = 'All ParticleId:%s\n'%( str(tuple(allIds)) )
    for data in allDatas:        
        dataStr += 'Frame:%s\n\t%s\n'%( data[0],  data[1] )
        ttCount += len( data[0] )
  
    #infoFile = open( '.txt', 'w')
    #infoFile.write( dataStr )
    #os.startfile( '.txt' )
    print dataStr
    #print len( allIds ), ttCount
    
    #return allDatas
                
                    

def surfaceFlow_parOrNpar( nPar=True ):
    '''{'path':'Dynamics/Particles/surfaceFlow_parOrNpar(nPar=True)',
'icon':':/flowSurface.png',
'tip':'surfaceFlow改成nParticle或particle',
'usage':"""
#将flowSurface在particle和nParticle之间进行切换
objects = $fun(nPar=True)""",
}
'''
    surMelPath = os.path.join( os.environ['MAYA_LOCATION'], 'scripts/others/includeSurfaceFlowGlobals.mel').replace( '\\', '/' )
    if os.path.exists( surMelPath ):
        if nPar:
            searchStr = 'string $particleObj[] = `particle`;'
            repWithStr = 'string $particleObj[] = `nParticle`;'
            print 'particle to nParticle'
        else:
            searchStr = 'string $particleObj[] = `nParticle`;'
            repWithStr = 'string $particleObj[] = `particle`;'
            print 'nParticle to par'


        melFile = open(surMelPath, 'r')
        melStr = melFile.read( )
        melFile.close()
        if melStr.find( searchStr )!=-1:
            melStr = melStr.replace( searchStr, repWithStr )
            melFile = open( surMelPath, 'w')
            melFile.write( melStr )
            melFile.close()
            mel.eval( 'source "%s"'%(surMelPath) )
            return True
        else:
            return True
    else:
        raise IOError( 'includeSurfaceFlowGlobals.mel is not found')


def curveFlow_parOrNpar(nPar = True):
    '''{'path':'Dynamics/Particles/curveFlow_parOrNpar(nPar=True)',
'icon':':/flow.png',
'tip':'curveFlow改成nParticle或particle',
'usage':"""
#将curveFlow在particle和nParticle间进行切换
objects = $fun(nPar=True)""",
}
'''
    surMelPath = os.path.join( os.environ['MAYA_LOCATION'], 'scripts/others/flowAlongCurves.mel').replace( '\\', '/' )
    if os.path.exists( surMelPath ):
        if nPar:
            searchStr = 'string $resultArray[] = `particle -name ($setGroupName+"_particle")`;'
            repWithStr = 'string $resultArray[] = `nParticle -name ($setGroupName+"_particle")`;'
            print 'particle to nParticle'
        else:
            searchStr = 'string $resultArray[] = `nParticle -name ($setGroupName+"_particle")`;'
            repWithStr = 'string $resultArray[] = `particle -name ($setGroupName+"_particle")`;'
            print 'nParticle to par'


        melFile = open(surMelPath, 'r')
        melStr = melFile.read( )
        melFile.close()
        if melStr.find( searchStr )!=-1:
            melStr = melStr.replace( searchStr, repWithStr )
            melFile = open( surMelPath, 'w')
            melFile.write( melStr )
            melFile.close()
            mel.eval( 'source "%s"'%(surMelPath) )
            return True
        else:
            return True
    else:
        raise IOError( 'flowAlongCurves.mel is not found')


#---Crowd
def dupObjByTimeSlider(oriObj=None, timeStep=1):
    '''{'path':'Dynamics/Particles/Instance/crowd/dupObjByTimeSlider( )',
'icon':':/instancer.svg',
'tip':'复制动画物体的快照',
'usage':"""
#根据时间滑条范置复制特体，timeStep是每隔多少帧复制一个，可以是小数
$fun(timeStep = 1)""",
}
'''
    if oriObj is None:
        oriObj = cmds.ls(sl=True)
    max = cmds.playbackOptions(q=True,maxTime=True)
    cur = cmds.playbackOptions(q=True,minTime=True)
    while True:
        cmds.currentTime(cur)
        cmds.duplicate(oriObj, rr=True)
        if cur>=max:
            break
        cur +=timeStep




def curveEditPointsOnMesh( *args, **kwargs):
    '''{'path':'Dynamics/Particles/Crowd/curveEditPointsOnMesh( )',
'icon':':/curveCV.png',
'tip':'把曲线吸附到多边形上',
'usage':"""
#选择曲线，再选择mesh;当closest=False，曲线按垂直方向投射到mesh上，为True，投射到最终的mesh的位置上
$fun( closest=False )"""
}
'''
    if len(args)>1:
        nurCurves = args[0]
        if type(nurCurves) == type( '' ):
            nurCurve = ( nurCurves, )
        mesh = args[1]
    else:
        sel = cmds.ls(sl=True)
        if len( sel )>1:
            nurCurves, mesh = sel[:-1], sel[-1]
        else:
            print 'Select two objects or assign arguments to the function!'
            return False

    mesh = checkArg( mesh, nodeType='mesh' )
    if not mesh:
        print 'Least object is not mesh'
        return False

    closest = kwargs.get( 'closest', False)

    for nurCurve in nurCurves:
        nurCurve = checkArg( nurCurve, nodeType='nurbsCurve' )

        if not nurCurve:
            print '%s is not nurbsCurve object'%( nurCurve )
            continue


        curveNode = nameToNode( nurCurve, old=True )
        curFn = om.MFnNurbsCurve( curveNode )
        numEPs = curFn.numCVs() - curFn.degree()+1

        meshNode = nameToNode( mesh  )
        meshFn = newom.MFnMesh( meshNode )

        #print closest
        for i in range( numEPs ):
            ep = '%s.ep[%s]'%(nurCurve, i)
            pos = newom.MPoint( cmds.pointPosition(  ep ) )

            meshPoint = meshFn.closestIntersection( newom.MFloatPoint(pos), newom.MFloatVector(0,1,0), newom.MSpace.kWorld, 9999.0, True)
            if meshPoint[2]!=-1:
                #print meshPoint
                dis = (meshPoint[0][0]-pos[0], meshPoint[0][1]-pos[1], meshPoint[0][2]-pos[2] )
                cmds.move( dis[0], dis[1], dis[2], ep, r=True)
            elif closest==True:
                closestPoint = meshFn.getClosestPoint( pos, newom.MSpace.kWorld)
                dis = (closestPoint[0][0]-pos[0], closestPoint[0][1]-pos[1], closestPoint[0][2]-pos[2] )
                cmds.move( dis[0], dis[1], dis[2], ep, r=True)


def particlesToLocator( par=None, locGrp=None ):
    '''{'path':'Dynamics/Particles/Crowd/particlesToLocator( )ONLYSE',
'icon':':/locator.svg',
'tip':'每个粒子创建一个locator',
'usage':"""
#在每一个粒子的位置上创建一个locator
$fun( par="nParticle1" )""",
}
'''
    par = checkArg( par, nodeType='nParticle', tryToShape=True)
    if not par:
        raise IOError( 'Select a particles node!')    
    parId = cmds.getParticleAttr( par, a=True, at='particleId')
    if not parId:
        return     
    pos = cmds.getParticleAttr( par, a=True, at='position')
    
    locGrp = locGrp if locGrp else par+'_locGrp'
    if not cmds.objExists( locGrp ):
        locGrp = cmds.group( name=par+'_locGrp', empty=True)
    
    
    for i, id in enumerate( parId ):
        locName = '|%s|%s_loc_id_%d'%(locGrp, par, id)  
        if not cmds.objExists( locName ):
            loc = cmds.spaceLocator( name='%s_loc_id_%d'%(par, id)  )[0]
            cmds.parent( loc, locGrp)
        cmds.setAttr( locName+'.t', pos[i*3], pos[i*3+1], pos[i*3+2], type='double3' )
  

#parToLocator( par='nParticle1')
#parToLocator()

def particlesToCurve( par=None, reset=False, curvesGrp=None ):
    '''{'path':'Dynamics/Particles/particlesToCurve( )ONLYSE',
'icon':':/curveCV.png',
'tip':'粒子拖尾曲线',
'usage':"""
#粒子拖尾出曲线：
    #reset:将曲线重置
    #下面这个例子：从1到100帧，第隔5帧创建一个曲线点
#－－－－－－－－－－－－－－－－－－－－－－－－－－
$fun( "nParticle1",reset=True )
start = 1
end = 100
step = 5
for i in range( start, end, step):
    cmds.currentTime( i, e=True)
    $fun( "nParticle1" )""",
}
''' 
    par = checkArg( par, nodeType='nParticle', tryToShape=True)
    if not par:
        raise IOError( 'Select a particles node!')
    
    curGrp = curvesGrp if curvesGrp else par+'_curGrp'
    
    if reset and cmds.objExists( curGrp):
        curs = cmds.listRelatives( curGrp, type='nurbsCurve', ad=True, f=True)
        for c in curs:
            if cmds.getAttr( c+'.spans')>1:
                #cmds.curve( c, a=True, p=[(0,0,0)] )
                cmds.curve( c, r=True, d=3, p=[ ( 0,0,0),(0,0,0), (0,0,0),(0,0,0) ] )
    
    else:
        parId = cmds.getParticleAttr( par, a=True, at='particleId')
        if not parId:
            return 
        
        pos = cmds.getParticleAttr( par, a=True, at='position' )
        
        if not cmds.objExists( curGrp ):
            curGrp = cmds.group( name=curGrp, empty=True )
        
        for i, id in enumerate( parId ):
            curName = '|%s|%s_cur_id_%d'%(curGrp, par, id)
            tpos = (pos[i*3], pos[i*3+1], pos[i*3+2])

            if not cmds.objExists( curName ):
                cur = cmds.curve(  d=3, p=[ tpos, tpos, tpos, tpos ] )            
                #cur = cmds.createNode( 'nurbsCurve', parent=curGrp )
                newName = cmds.rename( cur, '%s_cur_id_%d'%(par, id) )
                cmds.parent( newName, curGrp )
            elif cmds.getAttr( curName+'.spans')<2:
                cmds.curve( curName, r=True, p=[ tpos, tpos, tpos, tpos ]  )
            #else:                
            cmds.curve( curName, a=True, p=[ tpos ]  )


def crowd_curveToLocator( curGrp=None ):
    '''{'path':'Dynamics/Particles/Crowd/crowd_curveToLocator( )ONLYSE',
'icon':':/nurbsCurve.svg',
'tip':'为每个曲线创建一个locator',
'usage':"""
#每个曲线的中间的位置创建一个locator,并将这个locator放到这个曲线下面
$fun( curGrp=None  )""",
}
'''
    curGrp = curGrp if curGrp else cmds.ls(sl=True) 
    
    curves = cmds.listRelatives( curGrp, ad=True, type='nurbsCurve' )
    #if curves and not cmds.objExists(curGrp+'_locGrp'):
    #    locGrp = cmds.group( name=curGrp+'_locGrp', empty=True)
    for cur in curves:        
        curNode = pm.PyNode( cur )  
        pos = qm.nurbsCurve_findPointFromLength( cur, random.uniform(0, curNode.length()) )
        loc = cmds.spaceLocator(name=cur+'_loc')[0]
        cmds.setAttr( loc+'.t', pos[0], pos[1], pos[2], type='double3' )
        cmds.parent(loc, cmds.listRelatives( cur, parent=True)[0] )


def locatorOnCurve(locGrp=None, curGrp=None):
    '''{'del_path':'Dynamics/Particles/Crowd/locatorOnCurve( )ONLYSE',
'icon':':/locator.png',
'usage':"""
#每个曲线节点下面会创建两个属性curLength, length的属性，curLength值是当前位置所在曲线上的长度,length是曲线的总长度
$fun( locGrp="nParticleShape1_locGrp", curGrp="nParticleShape1_curGrp" )""",
}
'''
    #locGrp = 'HD_nParticleShape_locGrp'
    #curGrp = 'HD_nParticleShape_curGrp'
    locators = cmds.listRelatives( locGrp, f=True )
    
    curves = cmds.listRelatives( curGrp, f=True )
    finalCount = min( len(locators), len( curves) )
    locators = locators[:finalCount]
    curves = curves[:finalCount]
    
    for cur in curves:
        if cmds.getAttr( cur+'.minValue') != 0:
            cmds.rebuildCurve( cur, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=0, d=3,  tol=0.01)
   
    
    qm.delAttr( curves, ['length', 'curLength'] )
    cmds.addAttr( curves, ln='length', at='double')
    cmds.addAttr( curves, ln='curLength', at='double')
    
      
    #locators.sort()
    
    detachNode = cmds.createNode( 'detachCurve' )
    detachedCurve = pm.createNode( 'nurbsCurve' )
    cmds.setAttr( detachNode+'.parameter[0]', .1)
    cmds.connectAttr( detachNode+'.outputCurve[0]', detachedCurve.name()+'.create' )
    
    
    try:
        for i, loc in enumerate( locators ):
            cur = curves[i]
            if pm.objExists( cur ):
                #print cur
                curNode = pm.PyNode( cur ).getShape()
                pos = curNode.closestPoint( cmds.getAttr(loc+'.t')[0], space='world' )
                cmds.setAttr( loc+'.t', pos[0], pos[1], pos[2], type='double3' )
                
                param = curNode.getParamAtPoint( pos, space='world')
                
                cmds.connectAttr( cur+'.worldSpace', detachNode+'.inputCurve', f=True)
                
                cmds.setAttr( cur+'.length', curNode.length() )
                
                cmds.setAttr( detachNode+'.parameter[0]', param )
                curLength = detachedCurve.length() if param else 0
                cmds.setAttr( cur+'.curLength', curLength )
    except:       
        cmds.delete( detachNode, cmds.listRelatives( detachedCurve.name(), parent=True ) )
        raise IOError( 'Got a error!')
    cmds.delete( detachNode, cmds.listRelatives( detachedCurve.name(), parent=True ) )


def crowd_LocatorsToParentCurve( crowdGrp=None ):
    '''{'path':'Dynamics/Particles/Crowd/crowd_LocatorsToParentCurve( )ONLYSE',
'icon':':/locator.png',
'usage':"""
#这个命令是将nParticleShape1_locGrp组中locator， 放到nParticleShape1_curGrp组中对应曲线上；
$fun( crowdGrp="curve_grp" )""",
}
''' 
    if not crowdGrp or not cmds.objExists( crowdGrp ):
        raise IOError( '%s does not exists!'%(crowdGrp) )
    
    for cur in cmds.listRelatives( crowdGrp, f=True):
        if not cmds.listRelatives(cur, type='nurbsCurve'):
            cmds.parent( cur, w=True)
    
    allLoc = cmds.listRelatives( crowdGrp, ad=True, type='locator', f=True)
    allLoc = cmds.listRelatives( allLoc, parent=True, f=True)
    
    qm.delAttr( allLoc, ['curveId', 'curveLength', 'currentLength'] )
    cmds.addAttr( allLoc, ln='curveId', at='long')
    cmds.addAttr( allLoc, ln='curveLength', at='double')
    cmds.addAttr( allLoc, ln='currentLength', at='double')
    
    
    detachNode = cmds.createNode( 'detachCurve' )
    detachedCurve = pm.createNode( 'nurbsCurve' )
    cmds.setAttr( detachNode+'.parameter[0]', .1)
    cmds.connectAttr( detachNode+'.outputCurve[0]', detachedCurve.name()+'.create' )
    
    try:
        for i, cur in enumerate( cmds.listRelatives( crowdGrp, f=True) ):
            curShape = cmds.listRelatives( cur, type='nurbsCurve' )[0]
            locs = cmds.listRelatives( cur, ad=True, type='locator', f=True )
            if not locs:
                continue
            curNode = pm.PyNode( curShape )
            cmds.connectAttr( curShape+'.worldSpace', detachNode+'.inputCurve', f=True)
            for loc in cmds.listRelatives(locs, parent=True, f=True):
                if cmds.getAttr( cur+'.minValue') != 0:
                    cmds.rebuildCurve( cur, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=0, d=3,  tol=0.01)
                    
                pos = curNode.closestPoint( cmds.objectCenter(loc), space='world' )
                cmds.xform( loc, ws=True, translation=pos )
                wScale = [1/s for s in cmds.xform( loc,q=True, ws=True, scale=True ) ]
                cmds.xform( loc, ws=True, scale=wScale )
                
                param = curNode.getParamAtPoint( pos, space='world')        
                
                cmds.setAttr( detachNode+'.parameter[0]', param )
                curLength = detachedCurve.length() if param else 0
                      
                cmds.setAttr( loc+'.curveId', i  )
                cmds.setAttr( loc+'.curveLength', curNode.length() )                
                cmds.setAttr( loc+'.currentLength', curLength )
                
    except:        
        cmds.delete( detachNode, cmds.listRelatives( detachedCurve.name(), parent=True ) )
        raise IOError( 'Got a error!')
    cmds.delete( detachNode, cmds.listRelatives( detachedCurve.name(), parent=True ) )


def crowd_convertLocatorToParticles(particleNode = 'new', crowdGrp=None ):
    '''{'path':'Dynamics/Particles/Crowd/crowd_convertLocatorToParticles( )ONLYSE',
'icon':':/locator.png',
'usage':"""
#这个命令是将nParticleShape1_locGrp组中locator， 放到nParticleShape1_curGrp组中对应曲线上；
$fun( particleNode="nParticleShape1", crowdGrp="curve_grp" )""",
}
'''  
    if not crowdGrp or not cmds.objExists(crowdGrp):
        raise IOError( '%s does not exists!'%(crowdGrp) )
    
    posLi, curveId, length, curLength = [], [], [], []
    for i, cur in enumerate( cmds.listRelatives( crowdGrp, f=True) ):
        curShape = cmds.listRelatives( cur, type='nurbsCurve' )[0]
        locs = cmds.listRelatives( cur, ad=True, type='locator', f=True )
        if not locs:
            continue
        
        for loc in cmds.listRelatives(locs, parent=True, f=True):
            posLi.append( cmds.objectCenter( loc ) )
            curveId.append( cmds.getAttr(loc+'.curveId') )
            length.append( cmds.getAttr(loc+'.curveLength') )
            curLength.append( cmds.getAttr(loc+'.currentLength') )
    
    parName = qm.qsEmit(object = particleNode, position=posLi, attributes=[("cus_curveId", "floatValue", curveId), ("cus_length", "floatValue", length), ("cus_currentLength", "floatValue", curLength) ]    )
    melStr = 'global string $%s_curves[];\n$%s_curves = `listRelatives -f "%s"`;'%(parName, parName, crowdGrp)
    print melStr
    mel.eval( melStr )
    



def walkingOnCurve( *args ):
    curveNode = args[0]
    curLen = args[1]
    
    curveNode = nameToNode( curveNode, old=True )

    curFn = om.MFnNurbsCurve( curveNode )
    param = curFn.findParamFromLength( curLen )
    #return param
    pos = om.MPoint()
    curFn.getPointAtParam( param, pos)
    parentNode = cmds.listRelatives( args[0], parent=True)[0]
    parentPos = cmds.xform( parentNode, q=True, ws=True, translation=True)

    return ( pos.x+parentPos[0], pos.y+parentPos[1], pos.z+parentPos[2] )

#--------------------python string

def getParticleAttrStr():
    '''{
'del_path':'Dynamics/Particles/getParticleAttrStr()ONLYSE',
'icon':':/particle.png',
'tip':'api获得粒子属性',
'usage':"""
particleShapeNode = "nParticleShape1"
particleAttr = 'position'

attrType = 2
if attrType = 1:
    attrPPArray = om.MIntArray()
elif attrType = 2:
    attrPPArray = om.MDoubleArray()
else:
    attrPPArray = om.MVectorArray()

selectionList = om.MSelectionList()
selectionList.add(particleShapeNode)
particleObject = om.MObject()
selectionList.getDependNode(0,particleObject)
particleDataFn = omFX.MFnParticleSystem(particleObject)
particleDataFn.getPerParticleAttribute("position",attrPPArray)""",
}
'''