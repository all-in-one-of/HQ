#!usr/bin/env python
#coding:utf-8
import maya.cmds as cmds
import maya.mel as mel
def wicket():
    if  cmds.window("ToalWin",q=1,ex=1):
        cmds.deleteUI("ToalWin")
    win = cmds.window("ToalWin",title = 'Total_Ctrl')
    cmds.columnLayout()
    texts = cmds.text(l = '' , h = 10)
    texts = cmds.text(l = '' , h = 10)
    texts = cmds.text(l = '模型在原点，不用选择模型直接可以点击插件使用' , h = 10)
    #se = cmds.checkBox( label = '模型在原点，不用选择模型直接可以点击插件使用',v=1 )
    cmds.rowColumnLayout( numberOfColumns=3)
    texts = cmds.text(l = '' , w = 70)
    cmds.button("origin",label = '模型在原点',h= 40,w = 100,command = 'CenterPivots()',bgc = (0.6,1,0))
    texts = cmds.text(l = '' , w = 50)
    cmds.setParent("..")
    texts = cmds.text(l = '模型不在原点处，要选择模型才可以使用' , h = 10)
    #ses = cmds.checkBox( label = '模型不在原点处，要选择模型才可以使用',v=1 )
    cmds.rowColumnLayout( numberOfColumns=3)
    texts = cmds.text(l = '' , w = 70)
    cmds.button("origins",label = '模型不在原点处',h= 40,w=100,command = 'CenterPivotss()',bgc = (1,1,0.5))
    texts = cmds.text(l = '' , w =50)
    cmds.setParent("..")
    texts = cmds.text(l = '请不要有重命名，否则插件使用异常！！！' , h = 10)
    #ses = cmds.checkBox( label = '请不要有重命名，否则插件使用异常！！！',v=1 )
    texts = cmds.text(l = '' , h = 10)
    cmds.button("war",label = '温馨提示：由于是（总控）所以创建都是世界坐标',h= 20,bgc = (0.4,0,0))
    cmds.showWindow(win)
def CenterPivots():
	sel=cmds.ls(sl=1) 
	curves = mel.eval('curve -d 1 -p -0.984151 0 1.018023 -p 0.984151 0 1.018023 -p 0.984151 0 -1.018023 -p -0.984151 0 -1.018023 -p -0.984151 0 1.018023 -k 0 -k 1 -k 2 -k 3 -k 4 -n "Character";')
	circles = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='Main')
	selects = cmds.select(curves, add=1)
	history = cmds.listHistory(curves, circles[0], ha=1)
	groups = cmds.group(curves, n='Character_C', w=1)
	groupcurve = cmds.group(groups, n='Character_G', w=1)
	groupss = cmds.group(circles[0], n='Main_C',w=1)
	groupcircles = cmds.group(groupss, n='Main_G', w = 1)
	prant = cmds.parent(groupcircles, curves)
	cmds.select(circles[0],curves)
	cmds.setAttr(circles[0]+'.scaleX',lock=1,k=0)
	cmds.setAttr(circles[0]+'.scaleY',lock=1,k=0)
	cmds.setAttr(circles[0]+'.scaleZ',lock=1,k=0)
	cmds.setAttr(circles[0]+'.visibility',lock=1,k=0)
	cmds.setAttr(curves+'.visibility',lock=1,k=0)
	color = cmds.setAttr(circles[0]+".overrideEnabled",1)
	colors = cmds.setAttr(circles[0]+".overrideColor",13)
	showmod=  cmds.addAttr (circles[0],ln='showMod',at='double',min=0,max=1,dv=1,k=1)
def CenterPivotss():
	sel=cmds.ls(sl=1) 
	curves = mel.eval('curve -d 1 -p -0.984151 0 1.018023 -p 0.984151 0 1.018023 -p 0.984151 0 -1.018023 -p -0.984151 0 -1.018023 -p -0.984151 0 1.018023 -k 0 -k 1 -k 2 -k 3 -k 4 -n "Character";')
	circles = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='Main')
	history = cmds.listHistory(curves, circles[0], ha=1)
	cmds.makeIdentity(apply=True,r=1,t=1,s=1)
	groups = cmds.group(curves, n='Character_C', w=1)
	groupcurve = cmds.group(groups, n='Character_G', w=1)
	groupss = cmds.group(circles[0], n='Main_C',w=1)
	groupcircles = cmds.group(groupss, n='Main_G', w = 1)
	prant = cmds.parent(groupcircles, curves)
	cmds.delete(cmds.parentConstraint(sel,groupcurve,mo=0))
	cmds.select(circles[0],curves)
	cmds.setAttr(circles[0]+'.scaleX',lock=1,k=0)
	cmds.setAttr(circles[0]+'.scaleY',lock=1,k=0)
	cmds.setAttr(circles[0]+'.scaleZ',lock=1,k=0)
	cmds.setAttr(circles[0]+'.visibility',lock=1,k=0)
	cmds.setAttr(curves+'.visibility',lock=1,k=0)
	color = cmds.setAttr(circles[0]+".overrideEnabled",1)
	colors = cmds.setAttr(circles[0]+".overrideColor",13)
	showmod=  cmds.addAttr (circles[0],ln='showMod',at='double',min=0,max=1,dv=1,k=1)
	
	

#def Pro_Ctrl():
if __name__=='__main__':
    wicket()


