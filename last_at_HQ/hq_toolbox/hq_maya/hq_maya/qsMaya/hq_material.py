# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################



import maya.cmds as cmds

from qsMaya.utility import nameToNode
import maya.api.OpenMaya as newom
from functools import partial
import json



def transferMaterials(objects=None):

    renderAttrs = (
    "aiSelfShadows",
    "aiOpaque",
    "aiVisibleInDiffuse",
    "aiVisibleInGlossy",
    "aiMatte",
    "aiExportTangents",
    "aiExportColors",
    "aiExportRefPoints",
    "aiExportRefNormals",
    "aiExportRefTangents",
    "aiMotionVectorUnit",
    "aiMotionVectorUnit" ,
    "aiMotionVectorScale",
    "aiSubdivType",
    "aiSubdivIterations",
    "aiSubdivAdaptiveMetric",
    "aiSubdivPixelError",
    "aiSubdivUvSmoothing",
    "aiSubdivSmoothDerivs",
    "aiDispHeight",
    "aiDispPadding",
    "aiDispAutobump",
    "aiDispZeroValue"
    )


    #----getMats
    sel = objects if objects else cmds.ls(sl=True, l=True)
    if len( sel )<2:
        raise IOError('Select two objects')

    #Get from object
    if cmds.objectType( sel[-1] ) in ('mesh','nurbsSurface'):
        fromObj = sel[-1]
    else:
        temp = cmds.listRelatives( sel[-1], type=['mesh','nurbsSurface'], ni=True, f=True, shapes=True)
        if temp:
            fromObj = temp[0]
            '''for t in temp:
                if not cmds.getAttr( t+'.intermediateObject'):
                    fromObj = t
                    break'''
        else:
            raise IOError( '% is not a mesh node'%(fromObj) )

    print fromObj

    toObjs = sel[:-1]


    #Get data from fromObj
    seData = cmds.listConnections( fromObj, c=True, s=False, type='shadingEngine')

    if seData==None:
        raise IOError('%s have not materials'%(fromObj)  )

    matData = []
    for i in range( 0, len(seData), 2):
        meshAttr, se = seData[i], seData[i+1]
        for attr in ('.surfaceShader', '.miMaterialShader', '.aiSurfaceShader'):
            surShader = cmds.listConnections( se+attr, d=False)
            if surShader:
                break
        if '.instObjGroups' not in meshAttr or surShader==None:
            continue

        temp = [surShader[0]]
        if meshAttr.endswith('instObjGroups'):
            temp.append( 'All' )
        else:# '.instObjGroups.' in mats[i]:
            objAssigned = cmds.getAttr( meshAttr+'.objectGrpCompList')
            temp.append( tuple(objAssigned) )
        matData.append( temp )

    print matData

    renderAttrsValue = {}
    for attr in renderAttrs:
        #print attr
        if cmds.attributeQuery( attr, node=fromObj, exists=True):
            renderAttrsValue[attr] = cmds.getAttr( "%s.%s"%(fromObj, attr) )


    #Get to object
    for obj in toObjs:
        for attr, value in renderAttrsValue.iteritems():
            if cmds.attributeQuery( attr, node=obj, exists=True):
                cmds.setAttr( "%s.%s"%(obj, attr), value )

        if cmds.objectType( obj ) not in ('mesh','nurbsSurface'):
            temp = cmds.listRelatives( obj, type=['mesh','nurbsSurface'], shapes=True, ni=True)
            if temp!=None:
                obj = temp[0]

        if cmds.objectType( fromObj ) != cmds.objectType( obj ):
            raise IOError( '%s and %s is not some object type'%(fromObj, obj)  )

        print obj

        #Assign materials from fromObj to toObj
        if len( matData )!=1:
            if cmds.objectType( fromObj )=='mesh':
                if cmds.polyEvaluate( fromObj, f=True) != cmds.polyEvaluate( obj, f=True):
                    raise IOError('%s have multi shader , %s and %s face count is not same'%(fromObj, obj, fromObj) )
            if cmds.objectType( fromObj )=='nurbsSurface':
                raise IOError('%s is nurbsSurface and %s have multi shader'%(fromObj, fromObj)  )

        #seData = cmds.listConnections( toObj, c=True, s=False, type='shadingEngine')
        for temp in matData:
            shader, objects = temp
            objects = obj if objects=='All' else [ '%s.%s'%( obj, f) for f in objects ]

            cmds.select( objects, r=True)
            cmds.hyperShade( assign=shader )
    cmds.select( cl=True )

def transferRenderAttrs(fromObj=None, toObjs=None, *args):
    '''{"del_path":"Rendering/Lighting Shading/transferRenderAttrs( )",
"tip":"将选择的第一个物体上的Arnold渲染属性转传递选择的其它物体上",
"usage":"""
$fun()
""",
"help":"""
将选择的第一个物体上的Arnold渲染属性转传递选择的其它物体上
"""
}
'''
    if not fromObj and not toObjs and len(cmds.ls(sl=True))<2:
        raise IOError( 'Select two object!')
    fromObj = [ fromObj if fromObj else cmds.ls(sl=True)[0] ]
    toObjs = toObjs if toObjs else cmds.ls( sl=True )[1:]

    fromObj = [ mesh for mesh in cmds.listRelatives( fromObj, f=True, ad=True, ni=True, type='mesh' )  if cmds.getAttr(mesh+'.intermediateObject')==False ]

    toObjs = [ mesh for mesh in cmds.listRelatives( toObjs, f=True, ad=True, ni=True, type='mesh' )  if cmds.getAttr(mesh+'.intermediateObject')==False ]

    toObjs = list(
                  set(toObjs).difference( set(fromObj)  )
                  )
    fromObj = fromObj[0]
    renderAttrs = (
    "aiSelfShadows",
    "aiOpaque",
    "aiVisibleInDiffuse",
    "aiVisibleInGlossy",
    "aiMatte",
    "aiExportTangents",
    "aiExportColors",
    "aiExportRefPoints",
    "aiExportRefNormals",
    "aiExportRefTangents",
    "aiMotionVectorUnit",
    "aiMotionVectorUnit" ,
    "aiMotionVectorScale",
    "aiSubdivType",
    "aiSubdivIterations",
    "aiSubdivAdaptiveMetric",
    "aiSubdivPixelError",
    "aiSubdivUvSmoothing",
    "aiSubdivSmoothDerivs",
    "aiDispHeight",
    "aiDispPadding",
    "aiDispAutobump",
    "aiDispZeroValue"
    )

    renderAttrsValue = {}
    for attr in renderAttrs:
        #print attr
        if cmds.attributeQuery( attr, node=fromObj, exists=True):
            renderAttrsValue[attr] = cmds.getAttr( "%s.%s"%(fromObj, attr) )

    #Get to object
    for obj in toObjs:
        for attr, value in renderAttrsValue.iteritems():
            if cmds.attributeQuery( attr, node=obj, exists=True):
                cmds.setAttr( "%s.%s"%(obj, attr), value )








#------------------------batch Model--------------
def w18_A_transferMaterials_cmd(fromObjs, toObjs, *args):
    
    fromObjs = [ mesh for mesh in cmds.listRelatives( fromObjs, f=True, ad=True, ni=True, type='mesh' )  if cmds.getAttr(mesh+'.intermediateObject')==False ]
    
    toObjs = [ mesh for mesh in cmds.listRelatives( toObjs, f=True, ad=True, ni=True, type='mesh' )  if cmds.getAttr(mesh+'.intermediateObject')==False ]
    
    toObjs = list( 
                  set(toObjs).difference( set(fromObjs)  ) 
                  )
    
    pairData = {}
    finderData = {}
    for mesh in fromObjs:
        omMesh = nameToNode( mesh )
        uv = None if cmds.polyEvaluate(mesh, uvcoord=True)==0 else newom.MFnMesh( omMesh ).getPolygonUV(0, 0 )
        key = str( cmds.polyEvaluate( mesh, vertex=True, edge=True, face=True) ) + str( uv )
        pairData[mesh] = []
        finderData[key] = mesh
    

    for mesh in toObjs:
        omMesh = nameToNode( mesh )
        uv = None if cmds.polyEvaluate(mesh, uvcoord=True)==0 else newom.MFnMesh( omMesh ).getPolygonUV(0, 0 )
        key = str( cmds.polyEvaluate( mesh, vertex=True, edge=True, face=True) ) + str( uv )
        if finderData.has_key( key ):
            objKey = finderData[key]
            pairData[objKey].append( mesh )

    for fObj, toObj in pairData.items():
        try:
            if toObj:
                toObj.append( fObj )
                transferMaterials( toObj )
        except:
            print '%s is failed!'(toObj)
            pass


def exportAllMaterials(includeObjects=None):
    '''{'path':'Pipeline Cache/exportAllMaterials( )',
'icon':':/render_lambert.png',
'tip' : '导出选择的物体及场景中所有的材质',
'html':True,
'usage':"""
#导出场景中的所有的材质和当前选择的物体，到当前文件的目录下
$fun( )""",
}
'''
    matAndSG = cmds.ls(exactType='shadingEngine',  materials=True, textures=True)
    #matAndSG = cmds.ls( materials=True, textures=True, l=True)
    if includeObjects:
        if isinstance(includeObjects, (str, unicode) ) :
            includeObjects=[includeObjects]
        includeObjects = [obj for obj in includeObjects if cmds.objExists(obj) ]
    else:
        includeObjects = cmds.ls(sl=True, l=True)
    
    if includeObjects:
        matAndSG.extend( includeObjects )     
    
    cmds.select( matAndSG, ne=True, r=True)
    print len( cmds.ls(sl=True) )
    #sceneName = cmds.file( q=True, shortName=True, sceneName=True)[:-3]+'_export.mb'
    #wspace = cmds.workspace(q =True, rootDirectory=True)
    sceneName = cmds.file( q=True,  sceneName=True)
    mbPath = os.path.splitext( sceneName )[0]+'_abc.mb'.replace('\\', '/')
    #mbPath = jsonFilePath = os.path.join( wspace, sceneName).replace( '\\', '/')
    cmds.file( mbPath, op="v=0;", typ="mayaBinary", pr=False, es=True, force=True )
    cmds.select( cl=True )
    os.startfile(  os.path.dirname( cmds.file( q=True, sceneName=True) )   )
    return mbPath
    #cmds.select( allDagObjects=True, r=True)
    #cmds.delete( )



def getImRes(filePath ):
    maya_version = int( cmds.about(v=True)[:4] )
    if maya_version>2015:
        imFile = newom.MImage()
        imFile.readFromFile( filePath )
        imSize = imFile.getSize()
        imSize = (int(imSize[0]), int(imSize[1]) )
    else:
        imFile = om.MImage()
        imFile.readFromFile( filePath )
        x_util = om.MScriptUtil( 0 )
        x_ptr = x_util.asUintPtr()
        y_util = om.MScriptUtil( 0 )
        y_ptr = y_util.asUintPtr()
        imFile.getSize(x_ptr, y_ptr)
        imSize = ( x_util.getUint( x_ptr ), y_util.getUint( y_ptr )  )

    return imSize


def compositeTexture( node=None, **kwargs):
    if not node:
        return None
    nodeT = cmds.nodeType(node)
    if cmds.getClassification( nodeT, satisfies='utility') or cmds.getClassification( nodeT, satisfies='texture'):
        if len(cmds.listConnections( node, s=False, d=True))<2:
            return None
        else:
            xRes = kwargs.get('xRes', 1024)
            yRes = kwargs.get('yRes', 1024)
            imageName = kwargs.get('imageName', node.replace(':', '-') )
            imageFormat = 'tga'
            filePath = kwargs.get('filePath', 'images' )
            startFrame = kwargs.get('startFrame', int( cmds.currentTime( q=True) )  )
            endFrame = kwargs.get( 'endFrame', startFrame)
            by = kwargs.get('by', 1)
            padding = kwargs.get('padding', 4)
            loadInImageViewer = 1


            filePath = 'images' if os.path.isabs( filePath ) else filePath
            fullPath = os.path.join( cmds.workspace( q=True, rootDirectory=True ), filePath)
            if not os.path.exists( fullPath ):
                os.makedirs( fullPath )


            #composite 512 512 "aaa" "tga" "images/compositedTexture"  1.000000 1.000000 1 4 1
            oriSel = cmds.ls(sl=True)
            cmds.select( node, r=True)
            mel.eval( 'composite %d %d "%s" "%s" "%s"  %d %f %d %d %d'%(xRes, yRes, imageName, imageFormat, filePath, startFrame, endFrame, by, padding, loadInImageViewer) )
            fullImagePath = (os.path.join( fullPath, imageName) + '.' + str(startFrame).zfill(padding)  + '.' + imageFormat)\
                            .replace('\\', '/')

            if oriSel:
                cmds.select( oriSel, r=True )
            return fullImagePath


def out_mapInfo( **kwargs ):
    '''{'path':'Houdini/Materials/out_mapInfo( )',
'icon':'$ICONDIR/houdini.png',
'html':False,
'usage':"""
#输出一个json文件，这个文件中保存的是一些材质的信息。这个json文件是保存在maya文件相同目录下的。
#这些信息可以在Houdini恢复Primitive Groups时使用。
$fun( )""",
}
'''
    #out_mapInfo(  filePath='images',  indent=4, tryComposite=False, resByMax=False, maxRes=256 )

    filePath = kwargs.get( 'filePath', 'images' )
    indent = kwargs.get( 'indent', 0 )
    tryComposite = kwargs.get('tryComposite', False)
    resByMax = kwargs.get( 'resByMax', False )
    maxRes = kwargs.get( 'maxRes', 1024 )

    allSE = cmds.ls(exactType='shadingEngine', l=True)
    if not allSE:
        return

    mapsData = {}
    allSE  = [se for se in allSE if cmds.listConnections( se+'.surfaceShader') ]
    for se in allSE:
        #cmds.select( se, ne=True, r=True)
        shader = cmds.listConnections( se+'.surfaceShader')[0]
        primGrpName = se
        for s in ':|':
            primGrpName = primGrpName.replace(s, '_')

        mapsData[se] = {'nodeType': cmds.nodeType( shader ), 'primGroupName':primGrpName }

        #Get objects
        meshes = cmds.listConnections( se+'.dagSetMembers', sh=True, p=True)
        if meshes:
            shapes = [cmds.ls(shape.split('.', 1)[0], l=True)[0] \
                      for shape in meshes if shape.endswith('instObjGroups') ]
            if shapes:
                mapsData[se]['objects'] = shapes

        mapsData[se]['maps'] = {}
        connectedNode = cmds.listConnections( shader, d=False, c=True)
        if not connectedNode:
            continue
        for i in range( 0, len( connectedNode), 2):
            shaderAttr = connectedNode[i].split('.', 1)[-1]
            sourceNode = connectedNode[i+1]
            fileNodes = [ f for f in cmds.listHistory( sourceNode ) if cmds.nodeType(f)=='file' ]
            filePaths = [cmds.getAttr(f+'.fileTextureName') for f in fileNodes ]
            if fileNodes:
                nodeMapData = {'files':filePaths}

                if tryComposite:
                    if resByMax:
                        resList = []
                        for fname in filePaths:
                            resList.extend( getImRes(fname) )
                        maxRes = max( resList )

                    compositeImg = compositeTexture(  sourceNode, xRes=maxRes, yRes=maxRes, filePath=filePath )
                    #compositeImg = None
                    if compositeImg:
                        nodeMapData['compositeImg'] = compositeImg

                mapsData[se]['maps'][shaderAttr] = nodeMapData


    for k in mapsData.keys():
        if not mapsData[k]['maps'] and not mapsData[k].has_key('objects'):
            mapsData.pop(k)

    jsonStr = json.dumps( mapsData, indent=indent) if indent else json.dumps( mapsData )
    sceneName = cmds.file( q=True,  sceneName=True)
    jsonFilePath = os.path.splitext( sceneName )[0]+'_mapInfo.json'.replace('\\', '/')
    jsonFile = open( jsonFilePath, 'w' )
    jsonFile.write( jsonStr )
    jsonFile.close()
    os.startfile(  os.path.dirname( jsonFilePath )   )
    print jsonFilePath
    return jsonFilePath


