#!usr/bin/env python
#coding:utf-8

import maya.cmds as cmds
def windows():
    i = 'cici'
    try:
        cmds.deleteUI(i)
    except:pass  
    window = cmds.window('cici',title='面部<骨骼>次级添加',iconName='Short Name',widthHeight=(380,130))
    cmds.columnLayout(columnAttach=('both',20),rowSpacing=20,columnWidth=400)
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth=[(1,300),(2,300),])
    cmds.setParent('..') 
    cmds.rowColumnLayout(numberOfRows=3)
    cmds.columnLayout(columnAttach=('both',-100),adjustableColumn = True,rowSpacing=2)
    cmds.radioButtonGrp("pipei",label='配适: ',labelArray2=['ADV专用','通用版'],numberOfRadioButtons=2,select=1)
    cmds.setParent('..') 
    cmds.rowColumnLayout(numberOfRows=2)
    cmds.frameLayout(label='通用版点开',cll=1,cl=1,borderStyle='in',bgc=(0.3,0.3,1))
    cmds.columnLayout(columnAttach=('both',-80),adjustableColumn = True,rowSpacing=2)
    bb=cmds.textFieldButtonGrp('zong',label="载入骨骼",buttonLabel="载入")  
    cmds.textFieldButtonGrp(bb,e=1,bc='bb("'+bb+'"),')  
    cmds.setParent('..') 
    cmds.setParent('..') 
    cmds.rowColumnLayout(numberOfRows=3)
    cmds.text('选择面部曲线')
    cmds.textField('w',tx='',w=350,h=30)
    cmds.rowLayout(numberOfColumns=1,)
    cmds.button(command="cici()",label='确定',w=350,h=50) 
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=1)
    cmds.text('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') 
    cmds.setParent('..')
    cmds.showWindow(window)
def bb(y):
    les=cmds.ls(sl=1)
    if (len(les)>0):
        cmds.textFieldButtonGrp(y,e=1,tx=les[0])
def cici():
    import maya.cmds as lj
    import maya.mel as mm
    sele = cmds.ls(sl=1)
    pipei = cmds.radioButtonGrp('pipei',q=1,sl=1)
    maya=cmds.textFieldButtonGrp('zong',q=1,tx=1)
    name = cmds.textField('w',q=1,tx=1)
    for i in sele:
        a = []
        a =i.split('.')
        c=a[1][2:-1]
        curve1 = cmds.polyToCurve(i,form=2,degree=3)
        cmds.DeleteHistory(curve1)
        edge =cmds.createNode("curveFromMeshEdge",n='new_CFME_#')
        poc =cmds.createNode("pointOnCurveInfo",n='new_poc_#')
        joint_t =cmds.createNode("joint",n=name+'_Jt_#')
        jt_grp = cmds.group(joint_t,n=name+'_Jt_Gp_#')
        cmds.setAttr(poc+'.turnOnPercentage',1)
        cmds.setAttr(poc+'.parameter',1)
        MD =cmds.createNode("multiplyDivide",n='new_MD_#')
        cmds.setAttr(MD+'.input2Z',-1)
        cmds.setAttr(MD+'.input2X',-1)
        cmds.setAttr(MD+'.input2Y',-1)
        shape = cmds.listRelatives(a[0],s=1)
        shape1 = cmds.listRelatives(curve1[0],s=1)
        cmds.setAttr(edge+'.edgeIndex[0]',int(c))
        kong = cmds.curve(n=name,d=1,p=[(0,0,1),(0,0.5,0.866025),(0,0.866025,0.5),(0,1,0),(0,0.866025,-0.5),(0,0.5,-0.866025),(0,0,-1),(0,-0.5,-0.866025),(0,-0.866025,-0.5),(0,-1,0),(0,-0.866025,0.5),(0,-0.5,0.866025),(0,0,1),(0.707107,0,0.707107),(1,0,0),(0.707107,0,-0.707107),(0,0,-1),(-0.707107,0,-0.707107),(-1,0,0),(-0.866025,0.5,0),(-0.5,0.866025,0),(0,1,0),(0.5,0.866025,0),(0.866025,0.5,0),(1,0,0),(0.866025,-0.5,0),(0.5,-0.866025,0),(0,-1,0),(-0.5,-0.866025,0),(-0.866025,-0.5,0),(-1,0,0),(-0.707107,0,0.707107),(0,0,1)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])
        grp0 = cmds.group(kong,n=name+'_Subtract')
        grp1 = cmds.group(grp0,n=name+'_Offset')
        grp2 = cmds.group(grp1,n=name+'_Attach')
        cmds.connectAttr(shape[0]+'.worldMesh[0]',edge+'.inputMesh')
        cmds.connectAttr(edge+'.outputCurve',shape1[0]+'.create')
        cmds.connectAttr(shape1[0]+'.worldSpace[0]',poc+'.inputCurve')
        cmds.connectAttr(poc+'.position',grp2+'.translate')
        cmds.connectAttr(kong+'.translate',MD+'.input1')
        cmds.connectAttr(MD+'.output',grp0+'.translate')
        cmds.delete(cmds.parentConstraint(kong,jt_grp,w=1))
        cmds.connectAttr(kong+'.translate',joint_t+'.translate')
        cmds.connectAttr(kong+'.rotate',joint_t+'.rotate')
        cmds.connectAttr(kong+'.scale',joint_t+'.scale')
        cmds.select(kong+'.cv[0:32]')
        cmds.scale(0.01,0.01,0.01)
        se = cmds.listRelatives(kong,shapes=True)
        cmds.setAttr(se[0]+'.overrideEnabled',1)
        cmds.setAttr(se[0]+'.overrideColor',17)
        cmds.select(cl=1)
        if (pipei == 1):
            cmds.connectAttr('Brs.rotate',grp2+'.rotate')
            cmds.connectAttr('Brs.scale',grp2+'.scale')
            cmds.parent(curve1[0],'ClusterSetup')
            cmds.parent(jt_grp,'FaceAttachToHead')
            cmds.setAttr(curve1[0]+'.v',0)
        if (pipei == 2):
            cmds.connectAttr(maya+'.rotate',grp2+'.rotate')
            cmds.connectAttr(maya+'.scale',grp2+'.scale')
            
#def advFaceCtrlAdd():  
if __name__=='__main__':
    windows()
    
        