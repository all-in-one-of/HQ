#!/usr/bin/env python
#coding=cp936
#coding=utf-8
#----shuai_creatSubCtrls-------
import maya.cmds as mc
import maya.mel as mm
import maya.OpenMaya as om
import re
def shuai_creatSubCtrls():
    if mc.window('createSubCtrlWin',ex=1):
        mc.deleteUI('createSubCtrlWin')
    mc.window('createSubCtrlWin',t='创建次级控制器面板',h=500,w=300,sizeable=1)
    mc.rowLayout('mainLayout',numberOfColumns=2,adjustableColumn=1,adjustableColumn2=1,rat=[(1,'both',1),(2,'both',1)])
    
    mc.columnLayout('treeLayout',adjustableColumn=1)
    mc.treeView('familyTree', numberOfButtons = 0, allowDragAndDrop = False ,allowHiddenParents = False,allowMultiSelection = False,allowReparenting=False,w=200,h=400,selectCommand=selectItemCmd,idc=doubleClickCmd)
    mc.button('getFamilyTreeBt',w=200,h=50,l='获取层级关系',c='shuai_creatSubCtrls.getFamilyTreeCmd()')
    mc.button('cleanViewBt',w=200,h=50,l='清除',c='shuai_creatSubCtrls.cleanViewCmd()')
    mc.setParent('..')
    
    mc.columnLayout('buttonLayout',adjustableColumn=1)
    mc.button('addNewLavelBt',l='创建新次级模型',w=100,h=100,c='shuai_creatSubCtrls.addNewLavelCmd()')
    mc.button('createSubCtrlBt',l='创建控制器',w=100,h=100,c='shuai_creatSubCtrls.createSubCtrlButtonCmd()')
    mc.setParent('..')
    
    mc.showWindow('createSubCtrlWin')
def addNewLavelCmd():
    sels=mc.ls(sl=1)
    meshes=[]
    for i in sels:
        shapeNode=mc.listRelatives(i,s=1,ni=1)
        if shapeNode:
            if mc.nodeType(shapeNode)=='mesh' and mc.nodeType(i)=='transform':
                meshes.append(i)
    if meshes:
        for n in meshes:
            creatNextLeval(n)
    else:
        mc.error('No polymesh was selected!!')
def cleanViewCmd():
    mc.treeView( 'familyTree', edit=True, removeAll=True)
def getFamilyTreeCmd():
    sels=mc.ls(sl=1)
    meshList=[]
    for i in sels:
        shape=mc.listRelatives(i,s=1)[0]
        if mc.nodeType(shape)=='mesh':
            meshList.append(i)
    if len(meshList):
        listSubHierarchy(meshList)
    else:
        mc.error('No polymesh was selected!!!')
def doubleClickCmd(item):
    allItems=mc.treeView( 'familyTree', q=True, ch=True)
    for i in allItems:
        if item==i:
            try:
                mc.setAttr(i+'.visibility',1)
            except:
                pass
        else:
            try:
                mc.setAttr(i+'.visibility',0)
            except:
                pass
        if mc.getAttr(i+'.v'):
            mc.treeView( 'familyTree', e=True, ch=True,tc=[i,1,1,1])
        else:
            mc.treeView( 'familyTree', e=True, ch=True,tc=[i,0.3,0.3,0.3])
def selectItemCmd(sel,state):
    if state:
        mc.treeView( 'familyTree', edit=True, si=[sel,1])
        mc.select(sel,r=1)
    else:
        mc.treeView( 'familyTree', edit=True, si=[sel,0])
        mc.select(sel,d=1)
def listSubHierarchy(objs):
    mc.treeView( 'familyTree', edit=True, removeAll=True)
    for obj in objs:
        rootLavelObj=findRootObj(obj)
        descendents=findAllDescendents(rootLavelObj,[])
        if not mc.treeView('familyTree', q=True, iex = rootLavelObj):
            mc.treeView('familyTree', e=True, addItem = (rootLavelObj, ""))
        for i in descendents:
            parentLavel=mc.listConnections(i+'.firstObject',d=0)[0]
            if not mc.treeView('familyTree', q=True, iex = i):
                mc.treeView('familyTree', e=True, addItem = (i,parentLavel))
    allItems=mc.treeView( 'familyTree', q=True, ch=True)
    for n in allItems:
        if mc.getAttr(n+'.v'):
            mc.treeView( 'familyTree', e=True, ch=True,tc=[n,1,1,1])
        else:
            mc.treeView( 'familyTree', e=True, ch=True,tc=[n,0.3,0.3,0.3])
        if n in objs:
            mc.treeView( 'familyTree', edit=True, si=[n,1])
        else:
            mc.treeView( 'familyTree', edit=True, si=[n,0])
def createSubCtrlButtonCmd():
    sels=mc.ls(sl=1)
    if not len(sels)==1 or not '.vtx[' in sels[0]:
        mc.error('必须只选择一个poly顶点（Vertex）！！')
    meshShape=mc.ls(sels[0],o=1)
    mesh=mc.listRelatives(meshShape,p=1)[0]
    if not mc.attributeQuery('firstObject',ex=1,node=mesh):
        mc.error('所选顶点（Vertex）并不是次级模型上的顶点，需要首先创建次级模型！！')
    if not mc.listConnections(mesh+'.firstObject',d=0):
        mc.error('丢失首级模型，无法创建次级控制器！！')
    createSubCtrl(sels[0])
def findAllDescendents(rootObj,descendents=[]):
    if mc.attributeQuery('secondaryObjectList',ex=1,node=rootObj):
        secObjs=mc.listConnections(rootObj+'.secondaryObjectList',d=0)
        descendents+=secObjs
        for i in secObjs:
            findAllDescendents(i,descendents)
    return descendents
def findRootObj(obj):
    global rootObj
    if mc.attributeQuery('firstObject',ex=1,node=obj):
        firObj=mc.listConnections(obj+'.firstObject',d=0)
        if firObj:
            findRootObj(firObj[0])
        else:
            rootObj=obj
    else:
        rootObj=obj
    return rootObj
def createSubCtrl(polyComp):
    meshShape=mc.ls(polyComp,o=1)
    mesh=mc.listRelatives(meshShape,p=1)[0]
    deformers=mm.eval('findRelatedDeformer("%s")'%mesh)
    skinNode,blendNodes=[],[]
    for i in deformers:
        if mc.nodeType(i)=='skinCluster':
            skinNode.append(i)
        if mc.nodeType(i)=='blendShape':
            blendNodes.append(i)
    blendValue=[]
    for i in blendNodes:
        blendValue.append(mc.getAttr(i+'.envelope'))
        mc.setAttr((i+'.envelope'),0)
        
    allVetices=mc.polyEvaluate(mesh,v=1)
    souceAllPos=[]
    for i in range(0,allVetices):
        soucePos=mc.xform(mesh+'.vtx['+str(i)+']',q=1,ws=1,t=1)
        souceAllPos.append(soucePos)
    mc.move(0,100,0,r=1,ws=1,wd=1)
    allPos=[]
    for i in range(0,allVetices):
        pos=mc.xform(mesh+'.vtx['+str(i)+']',q=1,ws=1,t=1)
        allPos.append(pos)
    mc.move(0,-100,0,r=1,ws=1,wd=1)
    weights=[]
    for i in range(0,allVetices):
        weights.append((allPos[i][1]-souceAllPos[i][1])*0.01)
    
    jointPos=mc.xform(polyComp,q=1,ws=1,t=1)
    strCtrl = mm.eval("curve -d 1 -p -8.19564e-008 0 0.5 -p 0.0975451 0 0.490393 -p 0.191342 0 0.46194 -p 0.277785 0 0.415735 -p 0.353553 0 0.353553 -p 0.415735 0 0.277785 -p 0.46194 0 0.191342 -p 0.490393 0 0.0975452 -p 0.5 0 0 -p 0.490392 0 -0.0975448 -p 0.461939 0 -0.191341 -p 0.415734 0 -0.277785 -p 0.353553 0 -0.353553 -p 0.277785 0 -0.415734 -p 0.191342 0 -0.461939 -p 0.0975453 0 -0.490392 -p 2.23517e-007 0 -0.5 -p -0.0975448 0 -0.490392 -p -0.191341 0 -0.461939 -p -0.277785 0 -0.415735 -p -0.353553 0 -0.353553 -p -0.415734 0 -0.277785 -p -0.461939 0 -0.191342 -p -0.490392 0 -0.0975453 -p -0.5 0 -1.63913e-007 -p -0.490392 0 0.097545 -p -0.46194 0 0.191341 -p -0.415735 0 0.277785 -p -0.353553 0 0.353553 -p -0.277785 0 0.415735 -p -0.191342 0 0.46194 -p -0.0975452 0 0.490392 -p -8.19564e-008 0 0.5 -p -8.03816e-008 0.0975452 0.490392 -p -7.57178e-008 0.191342 0.46194 -p -6.81442e-008 0.277785 0.415735 -p -5.79519e-008 0.353553 0.353553 -p -4.55325e-008 0.415735 0.277785 -p -3.13634e-008 0.46194 0.191342 -p -1.59889e-008 0.490393 0.0975451 -p 0 0.5 0 -p 4.36061e-008 0.490393 -0.0975451 -p 8.55364e-008 0.46194 -0.191342 -p 1.2418e-007 0.415735 -0.277785 -p 1.58051e-007 0.353553 -0.353553 -p 1.85848e-007 0.277785 -0.415734 -p 2.06503e-007 0.191342 -0.461939 -p 2.19223e-007 0.0975452 -0.490392 -p 2.23517e-007 0 -0.5 -p 2.19223e-007 -0.0975452 -0.490392 -p 2.06503e-007 -0.191342 -0.461939 -p 1.85848e-007 -0.277785 -0.415734 -p 1.58051e-007 -0.353553 -0.353553 -p 1.2418e-007 -0.415735 -0.277785 -p 8.55364e-008 -0.46194 -0.191342 -p 4.36061e-008 -0.490393 -0.0975451 -p 0 -0.5 0 -p -1.59889e-008 -0.490393 0.0975451 -p -3.13634e-008 -0.46194 0.191342 -p -4.55325e-008 -0.415735 0.277785 -p -5.79519e-008 -0.353553 0.353553 -p -6.81442e-008 -0.277785 0.415735 -p -7.57178e-008 -0.191342 0.46194 -p -8.03816e-008 -0.0975452 0.490392 -p -8.19564e-008 0 0.5 -p -0.0975452 0 0.490392 -p -0.191342 0 0.46194 -p -0.277785 0 0.415735 -p -0.353553 0 0.353553 -p -0.415735 0 0.277785 -p -0.46194 0 0.191341 -p -0.490392 0 0.097545 -p -0.5 0 -1.63913e-007 -p -0.490392 -0.0975452 -1.60763e-007 -p -0.461939 -0.191342 -1.51436e-007 -p -0.415735 -0.277785 -1.36288e-007 -p -0.353553 -0.353553 -1.15904e-007 -p -0.277785 -0.415735 -9.10651e-008 -p -0.191342 -0.46194 -6.27267e-008 -p -0.0975451 -0.490393 -3.19778e-008 -p 0 -0.5 0 -p 0.0975452 -0.490393 0 -p 0.191342 -0.46194 0 -p 0.277785 -0.415735 0 -p 0.353553 -0.353553 0 -p 0.415735 -0.277785 0 -p 0.46194 -0.191342 0 -p 0.490393 -0.0975452 0 -p 0.5 0 0 -p 0.490393 0.0975452 0 -p 0.46194 0.191342 0 -p 0.415735 0.277785 0 -p 0.353553 0.353553 0 -p 0.277785 0.415735 0 -p 0.191342 0.46194 0 -p 0.0975452 0.490393 0 -p 0 0.5 0 -p -0.0975451 0.490393 -3.19778e-008 -p -0.191342 0.46194 -6.27267e-008 -p -0.277785 0.415735 -9.10651e-008 -p -0.353553 0.353553 -1.15904e-007 -p -0.415735 0.277785 -1.36288e-007 -p -0.461939 0.191342 -1.51436e-007 -p -0.490392 0.0975452 -1.60763e-007 -p -0.5 0 -1.63913e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104");mc.DeleteHistory()
    strCtrl =mc.rename(strCtrl,mesh.replace('_MO_','_')+'_subCtrl#')
    strCtrlDrv = mc.group(strCtrl,n=strCtrl +'_driven')
    strCtrlInverse=mc.group(strCtrlDrv,n=strCtrl+'_inverse')
    strCtrlGrp = mc.group(strCtrlInverse,n=strCtrl +'_GRP')
    mc.xform(strCtrlGrp,a=True,ws=True,t=jointPos)
    softSelJoint=mc.joint(strCtrl,p=jointPos,n=strCtrl+'_joint');mc.hide(softSelJoint)
    softSelJointGrp = mc.group(softSelJoint,n=strCtrl+'_joint_GRP')
    mc.setAttr(strCtrl+'.overrideEnabled',1)
    mc.setAttr(strCtrl+'.overrideColor',13) 
    mc.skinCluster(mesh,e=1,wt=0,ai=softSelJoint)
    
    for i in range(0,allVetices):
        if not weights[i]==0:
            mc.skinPercent(skinNode[0],mesh+'.vtx['+str(i)+']',tv=[softSelJoint,weights[i]])
    mc.skinCluster(mesh,e=1,lw=1,inf=softSelJoint)
    infJoints=mc.skinCluster(skinNode[0],q=1,inf=1)
    activeList=om.MSelectionList()
    om.MGlobal.getSelectionListByName(skinNode[0],activeList)
    depNode=om.MObject() 
    iter=om.MItSelectionList(activeList)
    iter.reset()
    iter.getDependNode(depNode)
    mfnDN=om.MFnDependencyNode(depNode)
    bindPreMatrixPlug=mfnDN.findPlug('bindPreMatrix')
    bindPreMatrix=bindPreMatrixPlug.elementByPhysicalIndex(len(infJoints)-1).info()
    mc.connectAttr(strCtrlInverse+'.worldInverseMatrix',bindPreMatrix,f=1)
    firstMesh=mc.listConnections(mesh+'.firstObject',s=1)[0]
    loca=polyAttach(firstMesh+'.vtx['+polyComp.split('.vtx[')[1])
    if not mc.objExists('attachLocators'):
        mc.group(em=1,n='attachLocators')
        if mc.objExists('secondarySystem'):
            mc.parent('attachLocators','secondarySystem')
    mc.parent(loca,'attachLocators')
    mc.parentConstraint(loca,strCtrlGrp,mo=1)
    mc.hide(loca)
    for i in blendNodes:
        index=blendNodes.index(i)
        mc.setAttr((i+'.envelope'),blendValue[index])
    mc.select(strCtrl,r=1)
def polyAttach(sel):
    edgeInfo=mc.polyInfo(sel,ve=1)[0]
    edge=sel.split('.')[0]+'.e[%s]'%(edgeInfo.split()[3])
    parameter=2
    if sel.find(mc.polyInfo(edge,ev=1)[0].split()[2])!=-1:
        parameter=1
    curveInfo=mc.pointOnCurve(edge,ch=1,pr=parameter,p=1)
    attachLoc=mc.spaceLocator(n=sel.split('.')[0]+'_Loc#')[0]
    mc.connectAttr(curveInfo+'.position',attachLoc+'.t')
    normalCstrt=mc.normalConstraint(sel.split('.')[0],attachLoc,weight=1,aimVector=[0,0,1],upVector=[1,0,0],worldUpType='vector',worldUpVector=[1,0,0])[0]
    mc.connectAttr(curveInfo+'.tangent',normalCstrt+'.worldUpVector')
    return attachLoc
def addSecondaryObjsAttr(node):
    activeList=om.MSelectionList()
    om.MGlobal.getSelectionListByName(node,activeList)
    depNode=om.MObject() 
    iter=om.MItSelectionList(activeList)
    iter.reset()
    iter.getDependNode(depNode)
    
    Mod=om.MDGModifier()
    
    mfnMsgAttr=om.MFnMessageAttribute()
    MsgAttr=mfnMsgAttr.create('secondaryObject','secondaryObject')
    mfnMsgAttr.setConnectable(True)
    mfnMsgAttr.setReadable(True)
    mfnMsgAttr.setWritable(True)
    
    mfnComAttr=om.MFnCompoundAttribute()
    comAttr=mfnComAttr.create('secondaryObjectList','secondaryObjectList')
    mfnComAttr.setReadable(True)
    mfnComAttr.setWritable(True)
    mfnComAttr.setArray(True)
    mfnComAttr.setUsesArrayDataBuilder(True)
    mfnComAttr.addChild(MsgAttr)
    Mod.addAttribute(depNode,comAttr)
    Mod.doIt()
def connectSecondaryObj(firObj,secObj):
    activeList=om.MSelectionList()
    om.MGlobal.getSelectionListByName(firObj,activeList)
    firPath=om.MDagPath()
    iter=om.MItSelectionList(activeList)
    iter.reset()
    iter.getDagPath(firPath)
    mfnFirAttr=om.MFnDependencyNode(firPath.node())
    numElements=mfnFirAttr.findPlug('secondaryObjectList').numElements()
    
    #add an secondaryObjectList item
    attr =firObj + '.secondaryObjectList'
    nextAvailable = 0
    if mc.getAttr(attr,s=1)> 0 :
        multi=mc.listAttr(attr,multi=1)
        for m in multi:
            match=re.search('\[\d+\]',m)
            if match:
                buffer = match.group()        
                indexMatch = re.search('\d+', buffer)
                if indexMatch:
                    index=int(indexMatch.group())
                    if index >= nextAvailable:
                        nextAvailable = index + 1
    plugName = attr + '[' + str(nextAvailable) + ']'
    mc.getAttr(plugName,type=1)
    
    firAttr=mfnFirAttr.findPlug('secondaryObjectList').elementByPhysicalIndex(numElements).child(0).partialName()
    activeList.clear()
    om.MGlobal.getSelectionListByName(secObj,activeList)
    secNode=om.MObject() 
    iter=om.MItSelectionList(activeList)
    iter.reset()
    iter.getDependNode(secNode)
    mfnsecAttr=om.MFnDependencyNode(secNode)
    secAttr=mfnsecAttr.findPlug('message').info()
    mc.connectAttr(secAttr,firObj+'.'+firAttr,f=1)
    
    
def creatNextLeval(souceObj):
    TmpMesh=mc.duplicate(souceObj,n=('tmpMesh'))[0]
    if mc.listRelatives(TmpMesh,p=1): 
        mc.parent(TmpMesh,world=1)    
    if mc.attributeQuery('secondaryObjectList',ex=1,node=TmpMesh):
        mc.deleteAttr(TmpMesh,attribute='secondaryObjectList')
    if mc.attributeQuery('firstObject',ex=1,node=TmpMesh):
        mc.deleteAttr(TmpMesh,attribute='firstObject')
    findIntermediateObj(TmpMesh,1)
    TmpMeshShape=mc.listRelatives(TmpMesh,s=1,pa=1)[0]
    souceInterObj=findIntermediateObj(souceObj)
    if souceInterObj:
        mc.connectAttr(souceInterObj+'.worldMesh',TmpMeshShape+'.inMesh',f=1)
    levalMesh=mc.duplicate(TmpMesh,n=souceObj.split('_MO_LV')[0]+'_MO_LV#')[0]
    mc.delete(TmpMesh)
    if not mc.attributeQuery('secondaryObjectList',ex=1,node=souceObj):
        addSecondaryObjsAttr(souceObj)
    if not mc.attributeQuery('firstObject',ex=1,node=levalMesh):
        mc.addAttr(levalMesh,at='message',ln='firstObject')
    mc.connectAttr(souceObj+'.message',levalMesh+'.firstObject',f=1)
    connectSecondaryObj(souceObj,levalMesh)
    
    levalBS=mc.blendShape(souceObj,levalMesh,foc=1,w=[(0,1)],n=levalMesh.replace('_MO_','_BS_'))[0]
    levalJoint=mc.joint(None,n=levalMesh.replace('_MO_','_JT_'))
    levalSC=mc.skinCluster([levalJoint,levalMesh],n=levalMesh.replace('_MO_','_SC_'))[0]
    infJoints=mc.skinCluster(levalSC,q=1,inf=1)
    mc.connectAttr(levalJoint+'.worldInverseMatrix',levalSC+'.bindPreMatrix[%d]'%(len(infJoints)-1))
    mc.hide([souceObj,levalJoint])
    mc.showHidden(levalMesh)
    if not mc.objExists('subMeshesGrp'):
        mc.group(em=1,n='subMeshesGrp')
    if not mc.objExists('subJointsGrp'):
        mc.group(em=1,n='subJointsGrp')
    if not mc.objExists('secondarySystem'):
        mc.group(em=1,n='secondarySystem')
        mc.parent(['subJointsGrp','subMeshesGrp'],'secondarySystem')
    mc.parent(levalMesh,'subMeshesGrp')
    mc.parent(levalJoint,'subJointsGrp')
    mc.select(levalMesh,r=1)
    listSubHierarchy([levalMesh])
def findIntermediateObj(obj,deleteUnusfull=False):
    souceMeshShapes=mc.listRelatives(obj,s=1,pa=1)
    souceMeshShapes1=mc.listRelatives(obj,s=1,ni=1,pa=1)
    intermediateShape=''
    for i in souceMeshShapes:
    	if not i in souceMeshShapes1:
            if mc.listConnections(i+'.worldMesh'):
                intermediateShape=i
            elif deleteUnusfull:
        	    mc.delete(i)
    return intermediateShape