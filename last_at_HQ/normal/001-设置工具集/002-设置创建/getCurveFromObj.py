#!/usr/bin/env python
#coding=cp936
#coding=utf-8

import maya.cmds as mc
import maya.mel as mm

def getCenterCurve_window():
    if mc.window('getCenterCurveWin',ex=1):
        mc.deleteUI('getCenterCurveWin')
    mc.window('getCenterCurveWin',t='提取中心线')
    mc.columnLayout()
    mc.text('\n先选择管状模型的两条对边，点击按钮生成通过管状模型中心的曲线\n')
    mc.button('提取中心线',c='getCenterCurve()')
    mc.showWindow('getCenterCurveWin')

def getCenterCurve():
    edges=mc.ls(sl=1)
    loftCurves=[]
    for i in edges:
        obj=i.split('.')[0]
        edgeID=int(i.split('.')[1].split('[')[1].split(']')[0])
        edgeLoop=mc.polySelect(obj,el=edgeID)
        loftCurves.append(mc.polyToCurve(form=2,degree=1)[0])
    mc.loft(loftCurves[0],loftCurves[1],ch=0,u=1,c=0,ar=1,d=1,ss=2,rn=0,po=0,rsn=1,n='NLoftPlane')
    loftPlane=mc.nurbsToPoly('NLoftPlane',mnd=1,ch=0,f=3,pt=0,pc=200,chr=0.1,ft=0.01,mel=0.001,d=0.1,ut=1,un=3,vt=1,vn=3,uch=0,ucr=0,cht=0.2,es=0,ntr=0,mrt=0,uss=1)[0]
    edgeLoop=mc.polySelect(loftPlane,el=2)
    centerCurve=mc.polyToCurve(form=2,degree=1)[0]
    mc.rebuildCurve(centerCurve,ch=0,rpo=1,rt=0,end=1,kr=0,kcp=1,kep=0,kt=0,s=16,d=3,tol=0.01);mc.DeleteHistory(centerCurve)
    mc.delete('NLoftPlane',loftPlane,loftCurves)
    mc.setAttr(centerCurve+'.overrideEnabled',1)
    mc.setAttr(centerCurve+'.overrideColor',16)
    loftCurves=[]

getCenterCurve_window()