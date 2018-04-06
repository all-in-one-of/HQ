#!usr/bin/env/ python
#coding:utf-8
#--------------------------
##脚本名称：polyCenterCurves.py
##脚本整合作者：lsy（刘升耀）
##整合时间：2016.5
##版本：v1.0
##备注：本脚本生成poly两边中心线
##说明：本脚本适用于设置组内部的使用
#--------------------------

import maya.cmds as cmd
import maya.mel as mel

class polyCenterCueves():
	def __init__(self):
		self.curve1=[]
		self.curve2=[]
		self.point=[]
	
	
	
	def polyCenterCurves(self,*args):
		cmd.select(self.curve1)
		cur1=cmd.polyToCurve(f=2,dg=3)
		cmd.DeleteHistory(cur1[0])
		cmd.select(self.curve2)
		cur2=cmd.polyToCurve(f=2,dg=3)
		cmd.DeleteHistory(cur2[0])
		
		self.point=[]
		self.pointOnCur(cur1[0],cur2[0])
		cmd.delete(cur1[0],cur2[0])
		
		int_i=len(self.point)
		for pi in range(0,int_i):
			if pi==0:
				centerCur=cmd.curve(d=3,p=self.point[pi],k=[0,0,0])
			else:
				cmd.curve(centerCur,a=1,p=self.point[pi])
		cmd.select(cl=1)
		print "////生成完毕"+"\n",
				
	
	def pointOnCur(self,cur1,cur2):
		inStr=raw_input()
		f=float(inStr)
		pf=1.0/f
		i=0.0
		while i<1.0:
			cur1_p=cmd.pointOnCurve(cur1,pr=i,p=1,top=1)
			cur2_p=cmd.pointOnCurve(cur2,pr=i,p=1,top=1)
			cur_p=[(x+y)/2.0 for x,y in zip(cur1_p,cur2_p)]
			self.point.append(cur_p)
			i=i+pf
	
	def ls_edge1(self,*args):
		self.curve1=[]
		ls_e=cmd.ls(sl=1)
		int=len(ls_e)
		if int==0:
			print "////请选择poly的边"+"\n",
		else:
			for e in ls_e:
				self.curve1.append(e)
			print "////获取到poly的边"+"\n",
		cmd.select(cl=1)
		
	
	def ls_edge2(self,*args):
		self.curve2=[]
		ls_e=cmd.ls(sl=1)
		int=len(ls_e)
		if int==0:
			print "////请选择poly的边"+"\n",
		else:
			for e in ls_e:
				self.curve2.append(e)
			print "////获取到poly的边"+"\n",
		cmd.select(cl=1)

	def polyCenterCurvesUI(self):
		win="polyCenterCuevesWin"
		if cmd.window(win,ex=1):
			cmd.deleteUI(win)
		cmd.window(win,t="生成poly中心曲线")
		cmd.columnLayout(w=250)
		cmd.text(l="           获取poly两条边，然后生成poly中心曲线         ")
		cmd.text(l="")
		cmd.button(l="获取边1",w=50,h=30,c=self.ls_edge1)
		cmd.text(l="",)
		cmd.button(l="获取边2",w=50,h=30,c=self.ls_edge2)
		cmd.text(l="",)
		cmd.button(l="生成曲线",w=50,h=30,c=self.polyCenterCurves)
		cmd.showWindow(win)
		
C_poly=polyCenterCueves()
C_poly.polyCenterCurvesUI()






















