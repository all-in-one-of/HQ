#!/usr/bin/env python
#-*- coding:utf-8 -*-   
#######################
##autor<<yanzhili>>----
##ToolName<<yzl_cam>>--
##buildTime<<2010.09>>
##QQ<<342555216>>------
#######################

import maya.cmds as cmd
import maya.mel as mel

def smooth_UI():
	if cmd.window("sm_win",exists=True):
		cmd.deleteUI("sm_win")
	cmd.window("sm_win",title="smooth节点关联")
	
	cmd.columnLayout(height=200,width=280)
	cmd.text("s_UI_text1",height=10,label="                   ")
	cmd.text("s_UI_text2",height=10,label="           读取头部骨骼名称，总位移控制器名称")
	cmd.text("s_UI_text4",height=30,label="            再选择需要smooth模型,之后执行即可")
	cmd.text("s_UI_text5",label="")
	cmd.textFieldButtonGrp("s_UI_tfbg1",text="",cw3=(100,80,80),label="头部骨骼名称",buttonLabel="读取",bc=s_UI_command1)
	cmd.textFieldButtonGrp("s_UI_tfbg2",text="",cw3=(100,80,80),label="总位移控制器名称",buttonLabel="读取",bc=s_UI_command2)
	cmd.rowLayout(nc=2,height=60)
	cmd.text("s_UI_text6",width=90,label="")
	cmd.button("button_1",height=30,width=100,label="执   行",c=smooth_connectAttr)
	
	cmd.showWindow("sm_win")

def HeadJoint_name():
	j_name_N=cmd.ls(selection=True)
	cmd.select(cl=True)
	if (len(j_name_N)==0):
		j_name=""
		print"请选择头部骨骼"
	else:
		j_name=j_name_N[0]
	return j_name
	
def s_UI_command1(*args):
	cmd.textFieldButtonGrp("s_UI_tfbg1",edit=True,text=HeadJoint_name())
	
def allmoveCtrl_name():
	c_name_N=cmd.ls(selection=True)
	cmd.select(cl=True)
	if (len(c_name_N)==0):
		c_name=""
		print"请选择总位移控制器"
	else:
		c_name=c_name_N[0]
	return c_name

def s_UI_command2(*args):
	cmd.textFieldButtonGrp("s_UI_tfbg2",edit=True,text=allmoveCtrl_name())

def smooth_connectAttr(*args):
	ploy_n=cmd.ls(selection=True)
	cmd.select(cl=True)
	mel.eval("smoothRig")
	sm_ctrl="smooth_ctrl"
	sm_ctrl_G="smooth_ctrl_G"
	sm_ctrl_attr="smooth_ctrl.smooth"
	HeadJoint_n=cmd.textFieldButtonGrp("s_UI_tfbg1",query=True,text=True)
	moveCtrl_n=cmd.textFieldButtonGrp("s_UI_tfbg2",query=True,text=True)
	
	cmd.parentConstraint(HeadJoint_n,sm_ctrl_G,weight=1,mo=1)
	cmd.parent(sm_ctrl_G,moveCtrl_n)
	
	
	if (len(ploy_n)==0):
		print "请选择已经smooth模型"
	else:
		num=len(ploy_n)
		i=1
		for one in ploy_n:
			str_num=str(num)
			str_i=str(i)
			polySmooth_n=cmd.polySmooth(one,mth=0,sdt=2,ovb=1,ofb=3,ofc=0,ost=1,ocr=0,dv=1,bnr=1,c=1,kb=1,ksb=1,khe=0,kt=1,kmb=1,suv=1,peh=0,sl=1,dpe=1,ps=0.1,ro=1,ch=1)
			smooth_attr1=polySmooth_n[0]+".continuity"
			smooth_attr2=polySmooth_n[0]+".divisions"
			cmd.connectAttr(sm_ctrl_attr,smooth_attr1)
			cmd.connectAttr(sm_ctrl_attr,smooth_attr2)
			print("////完成smooth关联 "+str_i+" 个，共 "+str_num + " 个")
			i=i+1
		
	cmd.setAttr((sm_ctrl+".tx"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".ty"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".tz"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".rx"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".ry"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".rz"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".sx"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".sy"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".sz"),lock=True,keyable=False,channelBox=False)
	cmd.setAttr((sm_ctrl+".v"),lock=True,keyable=False,channelBox=False)
	
	cmd.select(cl=True)
	print"///////完成工作"
smooth_UI()