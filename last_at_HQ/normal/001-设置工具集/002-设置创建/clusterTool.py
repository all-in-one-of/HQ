#!/usr/bin/env python
#coding=cp936
#coding=utf-8
from maya.cmds import*
import maya.mel as mm
#Creat A Group Named Temp To Ctrl Other Object's Visibility
def ClusterCtrl():
    if window('CreatClusterCtrlWin',ex=1):
        deleteUI('CreatClusterCtrlWin')
    window('CreatClusterCtrlWin',t='����c����������')
    columnLayout(rs=10)
    text('ѡ��Ԫ�أ��㣬�ߣ��棩������ѡ��Ȼ�������水ť')
    button('CreatClusterCtrlB',l='����c������',w=300,h=50,c='CreatClusterCtrl()')
    text('��ѡ��ԭģ�ͣ��ټ�ѡ����Ŀ��ģ�ͣ������ť����cȨ��')
    radioCollection('ClusterRadios')
    radioButton('allClustersRadio',l='����/�������е�cȨ��',sl=1)
    radioButton('someClustersRadio',l='����/����ָ����cȨ��',cc='radioChangeComd()')
    text('ѡ������c������Ȼ������ѡ�񡱰�ť��ȡ')
    textFieldButtonGrp('ClustersCtrlGrp',bl='ѡ��',en=0,bc='getClusterCtrls()')
    button('copyClusterWeightsB',l='����cȨ��',w=300,h=50,c='copyClusterWeights()')
    text('ѡ�����᣺')
    radioButtonGrp('mirrorAxisSel', numberOfRadioButtons=3,labelArray3=['x', 'y', 'z'],sl=1 )
    button('mirrorClusterWeightsB',l='����cȨ��',w=300,h=50,c='mirrorClusterWeights()')
    showWindow('CreatClusterCtrlWin')
def radioChangeComd():
    sel=radioButton('someClustersRadio',q=1,sl=1)
    textFieldButtonGrp('ClustersCtrlGrp',e=1,en=sel)
def getClusterCtrls():
    ClusterCtrls=ls(sl=1)
    fieldText=str(ClusterCtrls[0])
    for one in range(1,len(ClusterCtrls)):
        fieldText+=';'+ClusterCtrls[one]
    textFieldButtonGrp('ClustersCtrlGrp',e=1,text=fieldText)
def CreatClusterCtrl():
    result = promptDialog(
			title='Enter The Group Name',
			message='Enter Name:',
			button=['OK', 'Cancel'],
			defaultButton='OK',
			cancelButton='Cancel',
			dismissString='Cancel')

    if result == 'OK':
        Name = promptDialog(query=True, text=True)

    else :
        return
    ctrlName=getCtrlName(Name)
    transformNode=ls(sl=1)[0].split('.')[0]
    VtxWeights=getWeight(transformNode)
    TheCluster=cluster(n=ctrlName.replace("_Ctrl","_Cluster"),rel=0)
    for i in range(VtxNum):
        Vtx=transformNode+'.vtx[%d]'%i
        percent(TheCluster[0],Vtx,v=VtxWeights[i])
    TheCtrl=circle(n=ctrlName,nr=(0,0,1),r=0.3)
    TheCtrl=circle(n=ctrlName+"0",nr=(0,1,0),r=0.3)
    TheCtrl=circle(n=ctrlName+"1",nr=(1,0,0),r=0.3)
    
    parent(ctrlName+"0"+"Shape",ctrlName,s=1,add=1)
    parent(ctrlName+"1"+"Shape",ctrlName,s=1,add=1)
    delete (ctrlName+"0")
    delete (ctrlName+"1")
    
    TheM=xform(TheCluster[0]+"Handle",q = True, piv = True, ws = True)
    xform(ctrlName,ws=1,t=(TheM[0],TheM[1],TheM[2]))
    makeIdentity(ctrlName,apply=1,t=1)
    setAttr(TheCluster[0]+"HandleShape.v",0)
    setAttr(ctrlName+".overrideEnabled",1)
    setAttr(ctrlName+".overrideColor",18)
    TheTrNode=listConnections(TheCluster[0]+".clusterXforms",s=1)
    cluster(TheTrNode[0],e=1,wn=(ctrlName,ctrlName),bs=1,rel=1,g=transformNode)
    delete(TheTrNode[0])
    theCGroupName=group(ctrlName,n=ctrlName+"_C")
    theGGroupName=group(theCGroupName,n=ctrlName+"_G")
    connectAttr(theGGroupName+".worldInverseMatrix[0]",TheCluster[0]+".bindPreMatrix")
    return "����C��������ɣ���"
def getWeight(Mesh):
    global VtxNum
    VtxNum=polyEvaluate(Mesh,v=1)
    sousePos=[]
    weights=[]
    for i in range(VtxNum):
        Vtx=Mesh+'.vtx[%d]'%i
        pos=xform(Vtx,q=1,ws=1,t=1)
        sousePos.append(pos)
    move(0,100,0,r=1)
    for n in range(VtxNum):
        Vtx=Mesh+'.vtx[%d]'%n
        pos=xform(Vtx,q=1,ws=1,t=1)
        PointWeight=(pos[1]-sousePos[n][1])*0.01
        weights.append(PointWeight)
    move(0,-100,0,r=1)
    return weights
def copyClusterWeights():
    objs=ls(sl=1)
    ClusterCtrls=textFieldButtonGrp('ClustersCtrlGrp',q=1,text=1).split(';')
    radioSelect=radioCollection('ClusterRadios',q=1,sl=1)
    clusters=[]
    if radioSelect=='someClustersRadio':
        for one in ClusterCtrls:
            Cluster=listConnections(one,t='cluster')[0]
            clusters.append(Cluster)
    else:
        deformers=mm.eval("getChain(\"%s\")"%objs[0])
        clusters=ls(deformers,type='cluster')
    for one in clusters:
        Sets=listConnections(one,type='objectSet')[0]
        VtxNum=polyEvaluate(objs[0],v=1)
        duplicate(objs[0],n='souceSkinObj')
        joint(None,p=[0,0,0],n='mainObjJoint')
        skinCluster(['mainObjJoint','souceSkinObj'],nw=1,n='souceObjSkinCluster')
        joint(None,p=[0,1,0],n='clusterJoint')
        skinCluster('souceSkinObj',e=1,wt=0,ai='clusterJoint')
        for i in range(VtxNum):
            Vtx=objs[0]+'.vtx[%d]'%i
            setList=listSets(o=Vtx)
            if Sets not in setList:
                percent(one,Vtx,v=0)
            skinWeights=percent(one,Vtx,q=1,v=1)
            skinPercent('souceObjSkinCluster','souceSkinObj.vtx['+str(i)+']',tv=['clusterJoint',skinWeights[0]])
        sets(objs,include=Sets)
        for obj in objs[1:]:
            duplicate(obj,n='targetSkinObj')
            skinCluster(['mainObjJoint','clusterJoint','targetSkinObj'],nw=1,n='targetObjSkinCluster')
            select('souceSkinObj','targetSkinObj',r=1)
            copySkinWeights(sa='closestPoint',ia='oneToOne',nm=1)
            targetVtxNum=polyEvaluate(obj,v=1)
            for n in range(targetVtxNum):
                clusterWeight=skinPercent( 'targetObjSkinCluster', 'targetSkinObj.vtx[%d]'%n, transform='clusterJoint', query=True ,v=1)
                percent(one,obj+'.vtx[%d]'%n,v=clusterWeight)
            delete('targetSkinObj')
        delete(['souceSkinObj','mainObjJoint','clusterJoint'])
    return "����CȨ����ɣ���"
def mirrorClusterWeights():
    objs=ls(sl=1)
    ClusterCtrls=textFieldButtonGrp('ClustersCtrlGrp',q=1,text=1).split(';')
    radioSelect=radioCollection('ClusterRadios',q=1,sl=1)
    clusters=[]
    if radioSelect=='someClustersRadio':
        for one in ClusterCtrls:
            Cluster=listConnections(one,t='cluster')[0]
            clusters.append(Cluster)
    else:
        deformers=mm.eval("getChain(\"%s\")"%objs[0])
        clusters=ls(deformers,type='cluster')
    for one in clusters:
        Sets=listConnections(one,type='objectSet')[0]
        VtxNum=polyEvaluate(objs[0],v=1)
        duplicate(objs[0],n='souceSkinObj')
        joint(None,p=[0,0,0],n='mainObjJoint')
        skinCluster(['mainObjJoint','souceSkinObj'],nw=1,n='souceObjSkinCluster')
        joint(None,p=[0,1,0],n='clusterJoint')
        skinCluster('souceSkinObj',e=1,wt=0,ai='clusterJoint')
        setAttr('souceSkinObj.sx',lock=0)
        setAttr('souceSkinObj.sy',lock=0)
        setAttr('souceSkinObj.sz',lock=0)
        for i in range(VtxNum):
            Vtx=objs[0]+'.vtx[%d]'%i
            setList=listSets(o=Vtx)
            if Sets not in setList:
                percent(one,Vtx,v=0)
            skinWeights=percent(one,Vtx,q=1,v=1)
            skinPercent('souceObjSkinCluster','souceSkinObj.vtx['+str(i)+']',tv=['clusterJoint',skinWeights[0]])
        sets(objs,include=Sets)
        xyzAxis=['x','y','z']
        AxisIndex=radioButtonGrp('mirrorAxisSel', q=1,sl=1 )-1
        setAttr('souceSkinObj.s%s'%xyzAxis[AxisIndex],-1)
        for obj in objs:
            duplicate(obj,n='targetSkinObj')
            skinCluster(['mainObjJoint','clusterJoint','targetSkinObj'],nw=1,n='targetObjSkinCluster')
            select('souceSkinObj','targetSkinObj',r=1)
            copySkinWeights(sa='closestPoint',ia='oneToOne',nm=1)
            targetVtxNum=polyEvaluate(obj,v=1)
            clusterCtrl=connectionInfo(one+'.matrix',sfd=1).split('.')[0]
            pos=xform(clusterCtrl,q=1,ws=1,rp=1)
            polyCube(n='mirCube')
            xform('mirCube',ws=1,t=pos)
            setAttr('mirCube.t%s'%xyzAxis[AxisIndex],(-1*pos[AxisIndex]))
            select('mirCube')
            ctrlName=getMirCtrlName(one)
            TheCluster=cluster(n=ctrlName.replace('_Ctrl','_Cluster'),rel=0)
            TheCtrl=circle(n=ctrlName,nr=(0,0,1),r=0.3)
            TheCtrl=circle(n=ctrlName+"0",nr=(0,1,0),r=0.3)
            TheCtrl=circle(n=ctrlName+"1",nr=(1,0,0),r=0.3)
            
            parent(ctrlName+"0"+"Shape",ctrlName,s=1,add=1)
            parent(ctrlName+"1"+"Shape",ctrlName,s=1,add=1)
            delete (ctrlName+"0")
            delete (ctrlName+"1")
            
            TheM=xform(TheCluster[0]+"Handle",q = True, piv = True, ws = True)
            xform(ctrlName,ws=1,t=(TheM[0],TheM[1],TheM[2]))
            makeIdentity(ctrlName,apply=1,t=1)
            setAttr(TheCluster[0]+"HandleShape.v",0)
            setAttr(ctrlName+".overrideEnabled",1)
            setAttr(ctrlName+".overrideColor",18)
            TheTrNode=listConnections(TheCluster[0]+".clusterXforms",s=1)
            cluster(TheTrNode[0],e=1,wn=(ctrlName,ctrlName),bs=1,rel=1,g=obj)
            delete(TheTrNode[0])
            theCGroupName=group(ctrlName,n=ctrlName+"_C")
            theGGroupName=group(theCGroupName,n=ctrlName+"_G")
            connectAttr(theGGroupName+".worldInverseMatrix[0]",TheCluster[0]+".bindPreMatrix")
            for n in range(targetVtxNum):
                clusterWeight=skinPercent('targetObjSkinCluster','targetSkinObj.vtx[%d]'%n,transform='clusterJoint',query=True,v=1)
                percent(TheCluster[0],obj+'.vtx[%d]'%n,v=clusterWeight)
            select(objs)
            delete('targetSkinObj','mirCube')
        delete(['souceSkinObj','mainObjJoint','clusterJoint'])
    return "����CȨ����ɣ���"
def getCtrlName(inputName):
    index=0
    while objExists(inputName+'_Ctrl'+str(index)):
        index+=1
    ctrlName=inputName+'_Ctrl'+str(index)
    return ctrlName
def getMirCtrlName(inputCluster):
    index=0
    while objExists('mir_'+inputCluster.replace('_Cluster','_Ctrl').split('_Ctrl')[0]+'_Ctrl'+str(index)):
        index+=1
    ctrlName='mir_'+inputCluster.replace('_Cluster','_Ctrl').split('_Ctrl')[0]+'_Ctrl'+str(index)
    return ctrlName
ClusterCtrl()