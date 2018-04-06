#!/usr/bin/env python
#coding=cp936
#coding=utf-8


import maya.cmds as mc

def creatConstrainPlane_window():
    if mc.window('creatConstrainPlaneWin',ex=1):
        mc.deleteUI('creatConstrainPlaneWin')
    mc.window('creatConstrainPlaneWin',t='生成约束平面')
    mc.columnLayout(rs=5)
    mc.text('先选择所有要被约束的对象（如扣子或者扣子的控制器），点击“选择”按钮获取：')
    mc.textFieldButtonGrp('ConstrainObjsGrp',l='被约束对象：',bl='选择',bc='getConstrainObjs()')
    mc.text('再选择一个用于参考的平面（如衣服或者身体的模型），点击“选择”按钮获取:')
    mc.textFieldButtonGrp('RefrencePlaneGrp',l='参考平面：',bl='选择',bc='getRefrencePlane()')
    mc.text('点击“生成”按钮，每个被约束对象就会生成一个约束平面，约束平面的方向与参考平面的方向平行\n(生成出来的平面可以适当缩小)')
    mc.button(l='生成',h=50,w=500,c='creatConstrainPlane()')
    mc.showWindow('creatConstrainPlaneWin')

def getConstrainObjs():
    global ConstrainObjs
    ConstrainObjs=mc.ls(sl=1)
    fieldText=str(ConstrainObjs[0])
    for one in range(1,len(ConstrainObjs)):
        fieldText+=';'+ConstrainObjs[one]
    mc.textFieldButtonGrp('ConstrainObjsGrp',e=1,text=fieldText)
def getRefrencePlane():
    global RefrencePlane
    RefrencePlane=mc.ls(sl=1)[0]
    mc.textFieldButtonGrp('RefrencePlaneGrp',e=1,text=RefrencePlane)
def creatConstrainPlane():
    ConstrainObjs.append(RefrencePlane)
    objs=ConstrainObjs
    num=len(objs)
    lastObjShape=mc.listRelatives(objs[-1],s=1)[0]
    shapeType=mc.nodeType(lastObjShape)
    if num<2:
        mc.error('This command requires at least 2 arguments to be selected;  found %d.'%num)
    if shapeType != 'mesh':
        mc.error('The last selected object must be a mesh.')
    for i in range(num-1):
        BBox=mc.xform(objs[i],q=1,bb=1)
        size=(BBox[3]+BBox[4]+BBox[5]-BBox[0]-BBox[1]-BBox[2])/3
        pos=mc.xform(objs[i],q=1,ws=1,rp=1)
        rot=mc.xform(objs[i],q=1,ws=1,ro=1)
        Plane=mc.polyPlane(sx=2,sy=2,ax=[0,1,0],h=size,w=size,n=objs[i]+'_SkinPlane',ch=0)
        locator=mc.spaceLocator(p=[0,0,0],n=objs[i]+'_Loc')
        mc.hide(locator)
        Constraint=mc.pointOnPolyConstraint(Plane[0]+'.vtx[4]',locator[0])[0]
        mc.setAttr(Constraint+'.%sU0'%Plane[0],0.5)
        mc.setAttr(Constraint+'.%sV0'%Plane[0],0.5)
        mc.xform(Plane,t=pos,ro=rot)
        closestPointNode=mc.createNode("closestPointOnMesh")
        mc.connectAttr(objs[-1]+'.worldMesh[0]',closestPointNode+'.inMesh')
        mc.connectAttr(objs[-1]+'.worldMatrix[0]',closestPointNode+'.inputMatrix')
        mc.setAttr(closestPointNode+'.inPositionX',pos[0])
        mc.setAttr(closestPointNode+'.inPositionY',pos[1])
        mc.setAttr(closestPointNode+'.inPositionZ',pos[2])
        Constraint=mc.normalConstraint(objs[-1],Plane,aim=[0,1,0],u=[0,0,1])
        mc.delete(Constraint,closestPointNode)
        mc.parentConstraint(locator,objs[i],mo=1)
        
creatConstrainPlane_window()        