#!/usr/bin/env python
#coding=cp936
#coding=utf-8


#----shuai_polyAttach.py----------
from maya.cmds import *
def shuai_polyAttach():
    sel=ls(sl=1,fl=1)[0]
    if sel.find('.vtx[')!=-1:
        edgeInfo=polyInfo(sel,ve=1)[0]
        edge=sel.split('.')[0]+'.e[%s]'%(edgeInfo.split()[3])
        parameter=2
        if sel.find(polyInfo(edge,ev=1)[0].split()[2])!=-1:
            parameter=1
        curveInfo=pointOnCurve(edge,ch=1,pr=parameter,p=1)
        attachLoc=spaceLocator(n='attachLoc#')[0]
        connectAttr(curveInfo+'.position',attachLoc+'.t')
        normalCstrt=normalConstraint(sel.split('.')[0],attachLoc,weight=1,aimVector=[0,0,1],upVector=[1,0,0],worldUpType='vector',worldUpVector=[1,0,0])[0]
        connectAttr(curveInfo+'.tangent',normalCstrt+'.worldUpVector')
        return attachLoc
    else:
        warning('Please select a single vertex ！！')
shuai_polyAttach()