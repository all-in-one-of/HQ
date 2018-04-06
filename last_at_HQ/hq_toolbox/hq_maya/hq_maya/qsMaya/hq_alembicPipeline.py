# -*- coding: utf-8 -*-
import json
import os, sys
import socket
import re
import time
import maya.cmds as cmds
import maya.mel as mel
import qsMaya as qm
#import window
import re


def renameAllMaterials():
    '''{'del_path':'Pipeline Cache/Material/renameAllMaterials( )',
'icon':':/rename.png',
'tip':'给所有材质加个命名空间',
'html':True,
'usage':"""
#给场景中的所有的材质重命名，并添加到以当前场景名字相同的namespace下
$fun( )""",
}
'''
    sceneName = cmds.file( q=True, sceneName=True, shortName=True).replace( '.', '_')
    if not sceneName:
        return 
    #matAndSG = cmds.ls(exactType='shadingEngine',  materials=True, textures=True)
    matAndSG = cmds.ls( materials=True, textures=True, l=True)
    
    cmds.namespace( set=':' )
    newNamespace = ':%s'%(sceneName)
    if not cmds.namespace( exists= newNamespace  ):
        newNamespace = ':'+cmds.namespace( add= sceneName )
    
    for shader in matAndSG:
        if shader.rsplit(':', 1)[0] != newNamespace:
            try: #Skip read only nodes
                cmds.rename( shader,   '%s:%s'%( newNamespace, shader.rsplit( ':', 1)[-1]  )      )
            except:
                pass



def alembic_output_createMatAttr(objects=None, invisible=False):
    '''{'path':'Pipeline Cache/Material/alembic_output_createMatAttr( )',
'icon':':/render_lambert.png',
'tip':'创建matInfo属性，保存材质信息',
'html':'http://10.99.17.61/hq_maya/alembicPipeline',
'usage':"""
#对选择的mesh, nurbsSurface物体创建matInfo属性，保存材质信息
#使用方法：选择要创建matInfo物体或组
$fun( )""",
}
'''
    startTime = time.time()
    #Function in there
    if objects==None:
        selectedObj = cmds.ls(sl=True, l=True)
    else:
        selectedObj = objects

    #cmds.select(all=True, ado=True, r=True)

    allMeshFullPath = cmds.listRelatives(selectedObj, type=['mesh','nurbsSurface'], noIntermediate=True, ad=True, f=True )
    #allMeshFullPath = cmds.ls(exactType=['mesh','nurbsSurface'], noIntermediate=False, l=True)
    allMeshFullPath = [child for child in allMeshFullPath if not cmds.getAttr( child+'.intermediateObject') ]
    
    if not invisible:
        toRemove = []
        for obj in allMeshFullPath:
            for papa in [obj.rsplit( '|', i)[0] for i in range(obj.count('|') ) ]:
                if not cmds.getAttr( papa+'.visibility'):                                               
                    toRemove.append( obj )
                    break
        allMeshFullPath = tuple( set(allMeshFullPath).difference(toRemove)  )

    
    seInfo = {}
    shadingEngines = cmds.ls( exactType='shadingEngine' )
    for se in shadingEngines:
        surShader = cmds.listConnections( se+'.surfaceShader', d=False)
        if not surShader:
            continue
        seInfo[se] = surShader[0]


    attrInfo = {}
    qm.delAttr( allMeshFullPath, ['matInfo','papa'] )
    papaPrefix =  socket.gethostbyname( socket.gethostname() ) +  str( time.time() )
    papaPrefix = papaPrefix.replace('.', '')
    for mesh in allMeshFullPath:
        #print mesh
        objMatInfo = {}
        mats = cmds.listConnections( mesh, c=True, s=False, type='shadingEngine')
        if not mats:
            continue

        for i in range( 0, len(mats), 2):
            if '.instObjGroups' not in mats[i] or  mats[i+1] not in seInfo.keys():
                continue
            
            surShader = seInfo[ mats[i+1] ]
            if not objMatInfo.has_key(surShader):
                objMatInfo[surShader] = []
            
            if mats[i].endswith('instObjGroups'):                
                objMatInfo[surShader] = 'All'
                break
            else:# '.instObjGroups.' in mats[i]:
                objAssigned = cmds.getAttr(mats[i]+'.objectGrpCompList')
                objMatInfo[surShader].extend( objAssigned )
        
        objMatInfo =objMatInfo if objMatInfo else None
        #jsonStr = json.dumps( objMatInfo )
        cmds.addAttr(mesh, ln='matInfo', dt='string')#, h=True)
        #cmds.setAttr( mesh+'.matInfo', jsonStr, type='string', l=True)
        cmds.setAttr( mesh+'.matInfo', str(objMatInfo), type='string', l=True)
        #cmds.addAttr(mesh, ln='papa', dt='string')#, h=True)
        #papaName = papaPrefix +  mesh.split("|", 2)[1]
        #cmds.setAttr( mesh+'.papa', papaName, type='string', l=True)

    allMat = cmds.ls(materials=True )
    qm.delAttr( allMat, ['ori_name'] )
    cmds.addAttr( allMat, ln='ori_name', dt='string' )
    for mat in allMat:
        cmds.setAttr( mat+'.ori_name', mat, type='string', l=True)

    print time.time() - startTime




def alembic_import_assignMaterialsFromAttr(objects=None ):
    '''{'path':'Pipeline Cache/Material/alembic_import_assignMaterialsFromAttr( )',
'html':'http://10.99.17.61/hq_maya/alembicPipeline',
'icon':':/render_lambert.png',
'tip':'根据matInfo属性，恢复材质',
'usage':"""
#根据选择物体的matInfo属性，将材质恢复回来。
#使用方法：选择要物体材质物体或组
$fun( )""",
}
'''
    startTime = time.time()
    #Function in there
    if objects==None:
        selectedObj = cmds.ls(sl=True, l=True)        
    else:
        selectedObj = objects

    #cmds.select(all=True, ado=True, r=True)
    #selectedObj = cmds.ls('*_AbcGrp', sl=True, type='transform')

    allMeshFullPath = cmds.listRelatives(selectedObj, type=['mesh','nurbsSurface'], noIntermediate=True, ad=True, f=True)
    #allMeshFullPath = cmds.ls(exactType=['mesh','nurbsSurface'], noIntermediate=False, l=True)
    for child in allMeshFullPath[:]:
        if cmds.getAttr( child+'.intermediateObject')==True:
            allMeshFullPath.remove( child )
    
    
    allMeshFullPath = [mesh for mesh in allMeshFullPath if cmds.attributeQuery('matInfo', node=mesh, exists=True) ]
    for mesh in allMeshFullPath:
        cmds.setAttr( mesh+'.matInfo', l=True)
        matDic = eval( cmds.getAttr( mesh +'.matInfo') )#json.loads( cmds.getAttr( mesh+'.matInfo') )

        if not matDic:
            continue        
        
        for mat, fSet in matDic.items():            
            if fSet == 'All':
                cmds.select( mesh, r=True)                
            else:
                faces = ['%s.%s'%(mesh,f) for f in fSet]                    
                cmds.select(faces, r=True )
                
            if cmds.objExists(mat):
                cmds.hyperShade( assign=mat )
    cmds.select( cl=True )

    print time.time() - startTime




def output_createHiarOutputCurve(hairSystemObjs = None, hasPfxHair=True, createMarked=False):
    if not hairSystemObjs:
        if not cmds.ls(sl=True):
            cmds.warning( 'Select a hairSystem node!' )
            return
        hairSystemObjs = cmds.ls(sl=True, l=True, exactType='hairSystem')
    if not hairSystemObjs:
        hairSystemObjs = cmds.listRelatives(  cmds.ls(sl=True, l=True), shapes=True, type='hairSystem' )
    
    if not hairSystemObjs:
        return
    
    
    if isinstance(hairSystemObjs, (str,unicode) ):
        hairSystemObjs = [hairSystemObjs]
    
    
    #hairSystemObjs, hasPfxHair, createMarked = cmds.ls(exactType='hairSystem', l=True), False, False
    resultCruveGrps = []
    allHairData = {}
    numFollicle = 0
    
    for hair in hairSystemObjs: 
        pfxHair = cmds.listConnections( hair+'.outputRenderHairs', s=False, shapes=True)
        if hasPfxHair and not pfxHair:
            continue
        
        
        allHairData[hair] = {}
        follicles = cmds.listConnections( hair+'.inputHair', d=False, shapes=True)
        if not follicles:
            continue
        
        #Connected attributes infomations to attributes of materials
        materialsInfo = []
        mayaShader = cmds.listConnections( hair, d=False, p=True, c=True, type='shadingDependNode', shapes=True)
        aiHairs = cmds.listConnections( hair, d=False, p=True, c=True, type='aiHair', shapes=True )
        if mayaShader:
            materialsInfo.extend(  
                                    [  (mayaShader[i+1],mayaShader[i].split('.', 1)[-1] ) for i in range(0, len(mayaShader), 2)     ]
                                    )
        if aiHairs:
            materialsInfo.extend(     
                                    [   (aiHairs[i+1],aiHairs[i].split('.', 1)[-1] ) for i in range(0, len(aiHairs), 2)     ]
                                    )
        if materialsInfo:
            
            qm.delAttr( hair, ['shaderData', 'brushAttrs'])
            cmds.addAttr( hair, ln='shaderData', dt='string')
            cmds.setAttr( hair+'.shaderData', json.dumps(materialsInfo), type='string' )
            
        
        
        if not createMarked:
            tempFollicles = []
            for fol in follicles:
                markedCurves = cmds.listConnections( fol+'.outCurve', s=False, shapes=True)
                if not markedCurves:
                    tempFollicles.append( fol )
                    continue
                
                if not [c for c in markedCurves if cmds.attributeQuery('hairData', node=c, exists=True)  ]:
                    tempFollicles.append( fol )
                    continue
                
            if not tempFollicles:
                continue
            follicles = tempFollicles
        
        allHairData[hair] = follicles 
        numFollicle = numFollicle+len( follicles )
        
    if not numFollicle:
        return []
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    cmds.progressBar( gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True,
                    status='Creating curve...', maxValue=numFollicle )
        
    curNum = 1
    folAttrs = {'clumpWidthMult':1,
                'densityMult':    1,
                'curlMult':    1,
                'clumpTwistOffset':    0,
                'colorBlend':    0,
                'colorR':   0,
                'colorG':   0,
                'colorB':   0,
                }
    
    for hair, follicles in allHairData.iteritems():
        outCurvesGrp = cmds.group( em=True, name='hairSystem_OutputCurves_#')
        for fol in follicles:
            if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ):
                break
            
            newCurve = cmds.createNode( "nurbsCurve")
            hairValue = {}
            hairValue['hairSystem'] = hair
            for attr, v in folAttrs.iteritems():
                curV = cmds.getAttr( fol+'.'+attr )
                if curV!=v:
                    hairValue[attr] = curV
            jsonStr = json.dumps( hairValue )
                
            cmds.addAttr( newCurve, ln='hairData', dt='string' )            
            cmds.setAttr( newCurve+'.hairData', jsonStr, type='string')
            
            curvePapa = cmds.listRelatives( newCurve, p=True, pa=True )[0]
            cmds.connectAttr( fol+'.outCurve', newCurve+'.create')
            if not cmds.listConnections( fol+'.currentPosition', d=False):
                hairSysAttr = cmds.listConnections( fol+'.outHair', p=True, s=False, shapes=True, type='hairSystem', exactType=True)[0]
                pIndex = re.match( r'.+\[(\d+)\]$', hairSysAttr).groups()[0]
                cmds.connectAttr( hair+'.outputHair[%s]'%(pIndex), fol+'.currentPosition')
                
            cmds.parent( curvePapa, outCurvesGrp, r=True  )                
            cmds.progressBar(gMainProgressBar, edit=True, step=1, status='Creating curve %s/%s'%(curNum, numFollicle) )
         
            curNum = curNum+1
        resultCruveGrps.append( outCurvesGrp )
        
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    groupAll = '|hairSystem_OutputCurves_all'
    if not cmds.objExists( groupAll ):
        cmds.group( em=True, name=groupAll)
    cmds.parent( resultCurves, groupAll)





def createAttr_shaveObjId():
    allHairs = cmds.ls(exactType='shaveHair', l=True)
    allShaveSkinObjs = []
    curSecond = int( time.time() )
    for shave in allHairs:
        inputMesh = cmds.listConnections( shave+'.inputMesh', d=False, shapes=True )
        inputSurface = cmds.listConnections( shave+'.inputSurface', d=False, shapes=True )
        inputCurve = cmds.listConnections( shave+'.inputCurve', d=False, shapes=True )
        allShaveSkinObjs.extend(   inputMesh if inputMesh else [] )
        allShaveSkinObjs.extend(   inputSurface if inputSurface else [] )
        allShaveSkinObjs.extend(   inputCurve if inputCurve else [] )
    allShaveSkinObjs = tuple( set(allShaveSkinObjs) )
    
    qm.delAttr( allShaveSkinObjs, ['shaveObjId'] )
    cmds.addAttr( allShaveSkinObjs, ln='shaveObjId', dt='string')
    for i, obj in enumerate( allShaveSkinObjs ):
        idValue = json.dumps(  (curSecond,i )  )
        cmds.setAttr( obj+'.shaveObjId', idValue, type='string')
    return allShaveSkinObjs
    


def alembic_output_hairAndShave(**kwargs):
    '''{'delpath':'Pipeline Cache/Alembic/alembic_output_hairAndShave( )ONLYSE',
'html':'http://10.99.17.61/hq_maya/alembicPipeline',
'icon':'$ICONDIR/alembic.png',
'usage':"""
#这个命令对场景中所有的hair和shave节点进行以下操作
#    对和hair,shave相关的物体创建hairData和shaveData属性，保存相关信息
#    创建hair的曲线
#    将hair和shave的属性信息保存到名为 "文件名_INOF"的locator的shaveHairInitialState, attributePresets属性上
#使用方法：直接执行就好了，什么都不用选择
$fun( )""",
}
'''
    savePresetObjs = []
    
    #Shave
    shaveLoaded=False
    if cmds.pluginInfo( 'shaveNode.mll', query=True, registered=True):
        if not cmds.pluginInfo( 'shaveNode.mll', query=True, loaded=True):
            cmds.loadPlugin( 'shaveNode.mll' )
        if cmds.pluginInfo( 'shaveNode.mll', query=True, loaded=True): 
            shaveLoaded=True
    
    if shaveLoaded: 
        shaveHairs = cmds.ls(exactType='shaveHair', l=True)
        if shaveHairs:              
            for shave in cmds.ls( exactType='shaveHair', l=True):
                if not cmds.listConnections( shave+'.growthSet', d=False, shapes=True):
                    #qmw.w21_checkObjectSetOfShaveHair()
                    #return
                    pass
            
            createAttr_shaveObjId()
            savePresetObjs.extend( shaveHairs )    
    
    
    
    
    #HairSystem
    hairSystemObjs = cmds.ls(l=True, exactType='hairSystem')
    if hairSystemObjs:
        savePresetObjs.extend( hairSystemObjs )
        #Connect time.outTime to hairSystem currentTime if that not;
        #Get hairSystem brushNode
        brushNodes = []
        qm.delAttr( hairSystemObjs, ['brushNode',])
        for hair in hairSystemObjs:
            if not cmds.listConnections( hair+'.currentTime', d=False):
                cmds.connectAttr( 'time1.outTime', hair+'.currentTime', f=True)
            
            pfxHair = cmds.listConnections( hair+'.outputRenderHairs', s=False, shapes=True)
            if pfxHair:
                brushNode = cmds.listConnections( pfxHair[0]+'.brush', d=False, shapes=True)
                if brushNode:      
                    cmds.addAttr( hair, ln='brushNode', dt='string' )
                    cmds.setAttr( hair+'.brushNode', brushNode[0], type='string' )
                    brushNodes.append( brushNode[0] )
        if brushNodes:
            savePresetObjs.extend( brushNodes )
        
        
        output_createHiarOutputCurve(hairSystemObjs = hairSystemObjs, hasPfxHair=True, createMarked=False)
    
    if savePresetObjs:        
        qm.saveJsonAttrsPreset( objects=savePresetObjs, outJsonFile=False, outLocatorAttr=True)


def groupShaveObjs():
    allHairs = cmds.ls(exactType='shaveHair', l=True)
    shaveDatas = {}
    for shave in allHairs:
        shaveData = {'objects':[] }
        inputMesh = cmds.listConnections( shave+'.inputMesh', d=False, shapes=True )
        inputSurface = cmds.listConnections( shave+'.inputSurface', d=False, shapes=True )
        inputCurve = cmds.listConnections( shave+'.inputCurve', d=False, shapes=True )
        
        for objs in (inputMesh, inputSurface, inputCurve):
            if objs:
                shaveData['objects'].extend( objs )
        shaveDis = cmds.listConnections( shave+'.outputMesh', s=False )
        if shaveDis:
            shaveData['shaveDis'] = shaveDis
            
        shaveDatas[shave] = shaveData
    
    shaveObjsGrp = cmds.group( empty=True, name='shaveObjsGrp')
    shaveHairGrps = cmds.group( empty=True, name='shaveHairGrps')
    allShaveObjs = []
    for shave, objs in shaveDatas.iteritems():
        #shaveGrp = cmds.group( empty=True, name='shaveGrp_#' )    
        children = objs.get( 'shaveDis', [])
        children.append( shave )
        if children:
            curShaveGrp = cmds.group( empty=True, name='shaveHairGrp_#')
            cmds.parent( children, curShaveGrp )
            cmds.parent( curShaveGrp, shaveHairGrps )
        
        if objs.get( 'objects', [] ):
            allShaveObjs.extend( objs.get('objects',[])   )
    cmds.delete( allShaveObjs, ch=True )
    cmds.parent( allShaveObjs, shaveObjsGrp )
#groupShaveObjs()

def connectShaveObjs():
    #selected = cmds.ls(sl=True, l=True)
    shaveObjs = cmds.ls( exactType=('mesh', 'nurbsSurface', 'nurbsCurve'), l=True)
    #shaveObjs = cmds.listRelatives( selected, type=('mesh', 'nurbsSurface', 'nurbsCurve'), ad=True, f=True)
    shaveObjs = [obj for obj in shaveObjs if cmds.attributeQuery('shaveObjId', node=obj, exists=True)  ]
    
    shaveObjsData = {}
    for obj in shaveObjs:
        shaveId = json.loads( cmds.getAttr( obj+'.shaveObjId' ) )
        if not shaveObjsData.has_key( shaveId[0] ):
            shaveObjsData[shaveId[0] ] = {}
        if not shaveObjsData[shaveId[0]].has_key( shaveId[1] ):
            shaveObjsData[shaveId[0]][shaveId[1]] = []
        
        shaveObjsData[shaveId[0]][shaveId[1]].append( obj )
    skipedObjs = []  
    for shaveGrpValue in shaveObjsData.itervalues():
        for objs in shaveGrpValue.itervalues():
            if len(objs)!=2:
                skipedObjs.extend( objs )
                continue
            
            objType = cmds.nodeType( objs[0] )
            inputAttr = {'mesh': '.inMesh', 'nurbsCurve': '.worldSpace', 'nurbsSurface' : '.worldSpace' }[objType]
            animObj, shaveObj = '', ''
            if cmds.listConnections( objs[0], s=False, type='shaveHair', exactType=True ) and not cmds.listConnections( objs[0]+inputAttr, d=False ):
                shaveObj, animObj = objs
            elif cmds.listConnections( objs[1], s=False, type='shaveHair', exactType=True ) and not cmds.listConnections( objs[1]+inputAttr, d=False ):
                animObj, shaveObj = objs
            else:
                skipedObjs.extend( objs )
                continue
            
            if not qm.objConstrain( animObj, shaveObj):
                skipedObjs.extend( objs )
    ret = False if skipedObjs else True
    return ret






def import_createHairSystemByCurveAttr():    
    beforeHairSystem = set( cmds.ls( exactType='hairSystem', l=True) )
    selectedObj = cmds.ls(sl=True, l=True)
    curves = cmds.ls( selectedObj, l=True, exactType='nurbsCurve' )
    temp = cmds.listRelatives( selectedObj, ad=True, f=True, type='nurbsCurve')
    if temp:
        temp = [c for c in temp if not cmds.getAttr( c+".intermediateObject") ]
        curves.extend( temp )
    curves = tuple( set(curves) )
    curvesList = {}
    curves = [c for c in curves if cmds.attributeQuery( 'hairData', node=c, exists=True)]
    for c in curves:
        try:
            hairData = json.loads( cmds.getAttr(c+'.hairData') )
            hairName = hairData[ 'hairSystem']
            if not curvesList.has_key( hairName ):
                curvesList[hairName] = []
        except:
            print cmds.warning( '%s.hairData value loaded failed!'%(c)  )
            continue
        curvesList[hairName].append( c )
    
    numHairSystem = len(curvesList.keys())
    if not numHairSystem:
        return
    
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    cmds.progressBar( gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True,
                    status='Creating Hair System ...', maxValue=numHairSystem  )
    
    for hairName, curves in curvesList.iteritems():
        cmds.progressBar(gMainProgressBar, edit=True, step=1 )
        if not curves:
            continue
        cmds.select( curves, r=True)
        mel.eval( 'makeCurvesDynamic 2 { "0", "0", "0", "0", "1"}' )
        
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    
        
    #Transfer attributes from curve to hairSystem and follicle attributes
    objs = cmds.ls(l=True, exactType='hairSystem')
    #folAttrs = ('clumpWidthMult',  'densityMult', 'curlMult', 'clumpTwistOffset', 'colorBlend', 'colorR', 'colorG', 'colorB')
    
    for hair in objs:
        fols = cmds.listConnections( hair+'.inputHair', d=False, shapes=True)
        c = cmds.listConnections( fols[0]+'.startPosition', d=False, shapes=True)[0]
        
        hairData = json.loads( cmds.getAttr( c+'.hairData') )
        hairSysName = hairData.get( 'hairSystem', None)
        if hairSysName and not cmds.attributeQuery('originalName', node=hair, exists=True):
            cmds.addAttr( hair, ln='originalName', dt='string' )
            cmds.setAttr( hair+'.originalName', hairSysName, type='string')
            
            cmds.setAttr( hair+'.active', False)
            cmds.setAttr( hair+'.simulationMethod', 1)
            
        for fol in fols:
            c = cmds.listConnections( fol+'.startPosition', d=False, shapes=True)[0]
            hairData = json.loads( cmds.getAttr( c+'.hairData') )
            hairData.pop( 'hairSystem', None)
            if hairData and not cmds.attributeQuery('oriAttrs', node=fol, exists=True):
                cmds.addAttr(fol, ln='oriAttrs', dt='string' )
                cmds.setAttr( fol+'.oriAttrs', json.dumps(hairData), type='string' )
                
    afterHairSystem = set(  cmds.ls(exactType='hairSystem', l=True)  )
    
    newHairSystems = tuple( afterHairSystem.difference( beforeHairSystem )    )
    
    hairSysGrp = cmds.group( newHairSystems, name='hairsystemGrp_#')
    newHairSystems = cmds.listRelatives(hairSysGrp, ad=True, type='hairSystem', f=True)
    pfxHairs = []
    for hair in newHairSystems:
        pfxHairs.extend( cmds.listConnections( hair+'.outputRenderHairs', s=False) )    
    cmds.group( pfxHairs, name='pfxHairGrp_#' ) 
    
    return newHairSystems





#Exprot materials and shading groups to a maya file

def alembic_import_hairAndShave( **kwargs):
    '''{'delpath':'Pipeline Cache/Alembic/alembic_import_hairAndShave( )ONLYSE',
'tip':'恢复shave和hair',
'icon':'$ICONDIR/alembic.png',
'html':'http://10.99.17.61/hq_maya/alembicPipeline',
'usage':"""
#根据选择物体的hairData和shaveData以及messenger物体的attributePresets和shaveHairInitialState属性来恢复hair和shave
#使用方法：    1.将保存了attributePresets和shaveHairInitialState属性的locator的名字赋给messenger
#        2.选择要恢复hair和shave的物体的组。
messenger = 'F2_HanJXN_SC03_AN_mb_INOF'
$fun( messenger=messenger)""",
}
'''
    selectedObj =  kwargs.get( 'objects', cmds.ls(sl=True, l=True))
    if not selectedObj:
        raise IOError( "Select objects to create hair and shave!")
    
    #得到属性的json对象
    hairAndShave = []
    messenger = kwargs.get( 'messenger', None)
    if messenger:
        if not cmds.objExists( messenger):
            raise IOError( '%s is not exists!'%(messenger) )
        if not cmds.attributeQuery( 'attributePresets', node=messenger, exists=True):
            raise IOError( '%s.attributePresets is not exists!'%(messenger) )
        
        if not cmds.attributeQuery( 'shaveHairInitialState', node=messenger, exists=True):
            shaveInitialState = None
        else:
            shaveInitialState = cmds.getAttr( messenger+'.shaveHairInitialState' )
            shaveInitialState = json.loads(shaveInitialState)
            #raise IOError( '%s.shaveHairInitialState is not exists!'%(messenger) )
        jsonPreset = cmds.getAttr(  messenger+'.attributePresets'  )
    else:
        jsonPreset = kwargs.get( 'jsonPreset', None)
    
    keyFromAttr = kwargs.get( 'keyFromAttr', 'originalName')   
    
        
    #创建hairSystem
    hairSystems = import_createHairSystemByCurveAttr()
    if hairSystems:        
        hairAndShave.extend( hairSystems )   
    
    
    #检查shave插件
    loadedShave = False
    if not cmds.pluginInfo( 'shaveNode.mll', query=True, loaded=True):
        try: cmds.loadPlugin( 'shaveNode.mll' )
        except: pass    
    if cmds.pluginInfo( 'shaveNode.mll', query=True, loaded=True):
        loadedShave=True
    
    #创建shaveHair    
    if loadedShave:
        connectShaveObjs()
    
    
    if hairAndShave:
        #载入shaveHair和hairSystem的预设，从json对象中
        qm.loadJsonAttrsPreset( objects=hairAndShave, jsonPreset=jsonPreset, keyFromAttr=keyFromAttr )
        
        #创建并载入hairSystem的brush节点，并从jsonPrest中载入预设
        if hairSystems:
            brushNodes = []
            for hair in hairSystems:
                if cmds.attributeQuery('brushNode', node=hair, exists=True):                   
                    
                    pfxHair = cmds.listConnections( hair+'.outputRenderHairs', s=False, shapes=True)
                    brushNode = cmds.listConnections( pfxHair[0]+'.brush', d=False, shapes=True)                    
                    if not brushNode:
                        cmds.select( hair, r=True)
                        mel.eval('assignBrushToHairSystem;')
                        brushNode = cmds.listConnections( pfxHair[0]+'.brush', d=False, shapes=True)              
                    
                    qm.delAttr( brushNode, ['originalName',] )
                    cmds.addAttr( brushNode[0], ln='originalName', dt='string' )
                    cmds.setAttr( brushNode[0]+'.originalName', cmds.getAttr( hair+'.brushNode' ),
                                  type='string')
                    brushNodes.append( brushNode[0] )
                    
            #Load brush attributes from jsonPreset
            if brushNodes:
                qm.loadJsonAttrsPreset( objects=brushNodes, jsonPreset=jsonPreset, keyFromAttr=keyFromAttr )
                    
        
        #Connect texture or shader to shaveHair
        for shave in hairAndShave:
            if cmds.attributeQuery( 'shaderData', node=shave, exists=True):
                shaderData = json.loads( cmds.getAttr( shave+'.shaderData')    )
                for fromAttr, toAttr in shaderData:
                    try:
                        cmds.connectAttr( fromAttr, shave+'.'+toAttr, f=True)
                    except:
                        pass

    return hairAndShave

