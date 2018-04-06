# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import pymel.core as pm
import math
import maya.OpenMaya as om   
import maya.api.OpenMaya as newom 
import time


from qsMaya.utility import *
import qsMaya as qm


def deleteUVSet(objectList,searchPattern):
    '''{'del_path':'Polygons/EditUVs/deleteUVSet(cmds.ls(sl=True,exactType="transform"),"forEm")',
'icon':':/uvChooser.svg',
'usage':'$fun(cmds.ls(sl=True,exactType="transform"),"forEm")'
}
'''

    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]

    for tfNode in objectList:
        if cmds.listRelatives(tfNode,shapes=True, type='mesh', f=True ) is not None:
            for uvSet in cmds.polyUVSet(tfNode, q=True, allUVSets=True):
                if re.search(searchPattern, uvSet):
                    cmds.polyUVSet(tfNode, delete=True, uvSet=uvSet)



def setCurrentUVSet(objectList, matchPattern):
    '''{'del_path':'Polygons/EditUVs/setCurrentUVSet(cmds.ls(sl=True),"forEm")',
'icon':'uvChooser.svg',
'usage':'$fun(cmds.ls(sl=True),"forEm")',
}
'''

    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]

    for tfNode in objectList:
        if cmds.listRelatives(tfNode,shapes=True, type='mesh', f=True ) is not None:
            for uvSet in cmds.polyUVSet(tfNode, q=True, allUVSets=True):
                if re.search(matchPattern, uvSet):
                    cmds.polyUVSet(tfNode, currentUVSet=True, uvSet=uvSet)
                    break


#-----NurbsCurve functions
def nurbsCurve_reverse( *args):
    '''{'path':'Surfaces/EditNURBS/nurbsCurve_reverse( )',
'icon':':/reverse.png',
'usage':"""
#先选择曲线，再选择一个物体，这个命令根据曲线和物体的远近，对这些曲线进行reverse操作
$fun( )"""
}
'''
    if len(args):
        curvesNode = args[0]
        refPos = args[1]
    else:
        curvesNode = cmds.ls(sl=True, l=True)[:-1]
        refPos = cmds.objectCenter( cmds.ls(sl=True, l=True)[-1] )
    for obj in curvesNode:
        try:
            startPos = cmds.pointOnCurve(obj, pr=0, ch=False, p=True)
            endPos = cmds.pointOnCurve(obj, pr=1, ch=False, p=True)

            startLen = math.sqrt( math.pow(refPos[0]-startPos[0], 2) +
                        math.pow(refPos[1]-startPos[1], 2) +
                        math.pow(refPos[2]-startPos[2], 2)
                        )
            endLen = math.sqrt( math.pow(refPos[0]-endPos[0], 2) +
                        math.pow(refPos[1]-endPos[1], 2) +
                        math.pow(refPos[2]-endPos[2], 2)
                        )
            if startLen>endLen:
                cmds.reverseCurve(obj, ch=False, rpo=True)
                print 'Reversed %s'%obj
        except:
            print obj, " is not nurbscurve!"



def nurbsCurve_findParamFromLength( nurCurve, length=0):
    '''{'del_path':'Surfaces/EditCurves/nurbsCurve_findParamFromLength( nurCurve, length )ONLYSE',
'icon':':/nurbsCurve.svg',
'usage':"""
#返回指定的曲线长度的所在u的位置
$fun( "curve1", 0.0 )""",
}
'''
    if cmds.objectType(nurCurve)!='nurbsCurve':
        nurCurve = cmds.listRelatives( nurCurve, shapes=True)[0]
    
    curFn = om.MFnNurbsCurve( nameToNode(nurCurve, old=True) )
    return curFn.findParamFromLength( length )
    #curNode = pm.PyNode( nurCurve )
    #curNode = curNode.getShape() if curNode.type()=='transform' else curNode
    #return curNode.findParamFromLength( length )



def nurbsCurve_findPointFromLength( nurCurve, length=0):
    '''{'del_path':'Surfaces/EditCurves/nurbsCurve_findPointFromLength( nurCurve, length )ONLYSE',
'icon':':/nurbsCurve.svg',
'usage':"""
#返回指定的曲线长度的所在位置
$fun( "curve1", 0.0 )""",
}
'''
    if cmds.objectType(nurCurve)!='nurbsCurve':
        nurCurve = cmds.listRelatives( nurCurve, shapes=True)[0]
    
    curFn = om.MFnNurbsCurve( nameToNode(nurCurve, old=True) )
    param = curFn.findParamFromLength( length )
    pos = om.MPoint()
    curFn.getPointAtParam(param, pos, om.MSpace.kWorld)
    return tuple(pos)[:3]


def nurbsCurve_closestPoint( nurCurve, position=(0,0,0) ):
    '''{'del_path':'Surfaces/EditCurves/nurbsCurve_closestPoint( nurCurve, position )ONLYSE',
'icon':':/nurbsCurve.svg',
'usage':"""
#返回离指定点的，最近的曲线上的点
$fun( "curve1", (0,0,0) )""",
}
'''
    if cmds.objectType(nurCurve)!='nurbsCurve':
        nurCurve = cmds.listRelatives( nurCurve, shapes=True)[0]    
    curFn = om.MFnNurbsCurve( nameToNode(nurCurve, old=True) )
    
    fromPoint = om.MPoint( position[0], position[1], position[2], 0 )
    return tuple( curFn.closestPoint( fromPoint, None, .0000000001, om.MSpace.kWorld ) )[:3]

def nurbsCurve_getPointAtParam( nurCurve, param=0.0 ):
    '''{'del_path':'Surfaces/EditCurves/nurbsCurve_getPointAtParam( nurCurve, param )ONLYSE',
'icon':':/nurbsCurve.svg',
'usage':"""
#返回距指定的曲线的u的值，最近的曲线上的位置
$fun( "curve1", 0.0 )""",
}
'''
    if cmds.objectType(nurCurve)!='nurbsCurve':
        nurCurve = cmds.listRelatives( nurCurve, shapes=True)[0]    
    curFn = om.MFnNurbsCurve( nameToNode(nurCurve, old=True) )
    pos = om.MPoint()
    curFn.getPointAtParam( param, pos, om.MSpace.kWorld )
    return tuple( pos )[:3]

def nurbsCurve_getParamAtPoint( nurCurve, position=(0.0, 0.0, 0.0) ):
    '''{'del_path':'Surfaces/EditCurves/nurbsCurve_getParamAtPoint( nurCurve, position )ONLYSE',
'icon':':/nurbsCurve.svg',
'usage':"""
#返回距指定位置，最近的曲线的u值
$fun( "curve1", (0,0,0) )""",
}
'''
    if cmds.objectType(nurCurve)!='nurbsCurve':
        nurCurve = cmds.listRelatives( nurCurve, shapes=True)[0]    
    curFn = om.MFnNurbsCurve( nameToNode(nurCurve, old=True) )
    util = om.MScriptUtil(0.0)
    paramPtr = util.asDoublePtr()
    curFn.getParamAtPoint( om.MPoint(position[0], position[1], position[2], 0), paramPtr, om.MSpace.kWorld )
    return util.getDouble(paramPtr)


def nurbsCurve_distanceToPoint( nurCurve, position=(0.0, 0.0, 0.0) ):
    '''{'del_path':'Surfaces/EditCurves/nurbsCurve_distanceToPoint( nurCurve, position )ONLYSE',
'icon':':/nurbsCurve.svg',
'usage':"""
#返回距指定位置，到曲线最近的点之间的距离
$fun( "curve1", (0,0,0) )""",
}
'''
    curNode = pm.PyNode( nurCurve )
    curNode = curNode.getShape() if curNode.type()=='transform' else curNode
    return curNode.distanceToPoint( position, space='world')



#------Mesh functions
def mesh_uvToWorld_02():
    '''{'ddel_path':'Polygons/EditMesh/mesh_uvToWorld_02( )ONLYSE',
'icon':':/mesh.svg',
'usage':"""
#选择两个mesh物体，将第一个按uv匹配到第二个
$fun(  )""",
}
'''
    #import maya.cmds as cmds
    
    #import time
    startTime = time.time()
    
    fromObj = cmds.ls(sl=True)[0]#'pPlane1'
    
    toObj =  cmds.ls(sl=True)[1]#'pPlane2'
    
    iterVertex = om.MItMeshVertex( nameToNode(fromObj, old=True)  )
    
    iterPolygon = om.MItMeshPolygon( nameToNode(toObj, old=True ) )
    
    while not iterVertex.isDone():
        uv_util = om.MScriptUtil( )
        uv_ptr = uv_util.asFloat2Ptr( )
        iterVertex.getUV(uv_ptr)
        #print 'uv:', uv_util.getFloat2ArrayItem( uv_ptr, 0, 0), uv_util.getFloat2ArrayItem( uv_ptr, 0, 1)
      
        while not iterPolygon.isDone():
            pos = om.MPoint()
            try:
                iterPolygon.getPointAtUV(pos, uv_ptr, om.MSpace.kWorld )
                #print 'pos:',pos.x, pos.y, pos.z
                iterVertex.setPosition( pos, om.MSpace.kWorld)
                break
            except:
                pass        
            iterPolygon.next()
        iterPolygon.reset()    
        iterVertex.next()
    
    print time.time()-startTime
    
def mesh_uvToWorld():
    '''{'path':'Polygons/EditMesh/mesh_uvToWorld( )ONLYSE',
'icon':':/mesh.svg',
'usage':"""
#选择两个mesh物体，将第一个按uv匹配到第二个
$fun(  )""",
}
'''
    
    fromObj = cmds.ls(sl=True)[0]#'pPlane1'

    toObj =  cmds.ls(sl=True)[1]#'pPlane2'
    iterVertex = om.MItMeshVertex( nameToNode(fromObj, old=True)  )
        
    try:
        uv_util = om.MScriptUtil( )
        uv_ptr = uv_util.asFloat2Ptr( )
        uArray, vArray = [], []
        posArray = []
        while not iterVertex.isDone():
            posArray.append( tuple(iterVertex.position(om.MSpace.kWorld))[:3] )
            iterVertex.getUV(uv_ptr)
            uArray.append( uv_util.getFloat2ArrayItem( uv_ptr, 0, 0) )
            vArray.append( uv_util.getFloat2ArrayItem( uv_ptr, 0, 1) )
            iterVertex.next()
        parName = cmds.particle()[1]
        cmds.goal( parName, g=toObj, w=1 )
        cmds.setAttr(parName+'.goalSmoothness', 0)        
        cmds.setAttr(parName+".conserve", 0)
        startFrame = cmds.playbackOptions(q=True, min=True)
        cmds.setAttr(parName+".startFrame",startFrame)
        cmds.currentTime( startFrame, e=True)
        parName = qm.qsEmit( object=parName, position=posArray,
                attributes=[("goalU", "floatValue", uArray), ("goalV", "floatValue", vArray) ] 
                )        
        
        #cmds.setAttr(parName+".collide", 0)
        #cmds.setAttr(parName+".ignoreSolverGravity", 1)
        #cmds.setAttr(parName+".ignoreSolverWind", 1)
        #cmds.setAttr(parName+".drag", 0)
        #nculeus = cmds.listConnections(parName + '.nextState')[0]
        #startFrame = cmds.getAttr( nculeus+".startFrame")
        cmds.currentTime( startFrame, e=True)
        cmds.currentTime( int(startFrame+1), e=True)
        
        targetPos = cmds.getParticleAttr( parName, at='position', array=True )
        
        
        targetPos = [ newom.MPoint(targetPos[i],targetPos[i+1],targetPos[i+2]) 
                     for i in range(0, len(targetPos),3)
                     ]
        
        fromMesh = newom.MFnMesh( nameToNode(fromObj ) )
        fromMesh.setPoints( targetPos, newom.MSpace.kWorld)
    except:
        cmds.delete( cmds.listRelatives( parName, parent=True) )
        raise IOError( 'Got a error!')
    cmds.delete( cmds.listRelatives( parName, parent=True) )