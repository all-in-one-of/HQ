#!/usr/bin/env python
#coding=cp936
#coding=utf-8


import maya.cmds as mc
import maya.mel as mm

def softSelCtrl():
    if window('softSelCtrlWin',ex=1):
        deleteUI('softSelCtrlWin')
    window('softSelCtrlWin',t='软选择创建控制器')
    columnLayout(rs=10)
    text('软选择蒙皮模型上的点，把软选择转换成骨骼权重，生成控制器')
    rowLayout( numberOfColumns=2, columnWidth2=(80, 215), adjustableColumn=2, columnAlign=(1, 'left'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])    
    text(l='控制器前缀：')
    textField('ctrlName',tx='null')
    setParent( '..' )     
    button('CreatCtrl',l='创建',w=300,h=50,c='doCreateCtrl()')
    window('softSelCtrlWin',edit=True, widthHeight=(320, 130))
    showWindow('softSelCtrlWin')

class compCtrl():
    n=0
    compName=''
    def addCompCtrl(self):
        self.selVetices=mc.ls(sl=1,fl=1)
        self.objShape=mc.ls(sl=1,o=1)
        self.obj=mc.listRelatives(self.objShape,p=1)[0]
        self.allVetices=mc.polyEvaluate(self.obj,v=1)
        self.souceAllPos=[]
        for i in range(0,self.allVetices):
            soucePos=mc.xform(self.obj+'.vtx['+str(i)+']',q=1,ws=1,t=1)
            self.souceAllPos.append(soucePos)
        mc.move(0,100,0,r=1,ws=1,wd=1)
        self.allPos=[]
        for i in range(0,self.allVetices):
            pos=mc.xform(self.obj+'.vtx['+str(i)+']',q=1,ws=1,t=1)
            self.allPos.append(pos)
        mc.move(0,-100,0,r=1,ws=1,wd=1)
        self.weights=[]
        for i in range(0,self.allVetices):
            self.weights.append((self.allPos[i][1]-self.souceAllPos[i][1])*0.01)
        self.jointPos=self.centerPos(self.selVetices)
        self.strCtrl = mm.eval("curve -d 1 -p -8.19564e-008 0 0.5 -p 0.0975451 0 0.490393 -p 0.191342 0 0.46194 -p 0.277785 0 0.415735 -p 0.353553 0 0.353553 -p 0.415735 0 0.277785 -p 0.46194 0 0.191342 -p 0.490393 0 0.0975452 -p 0.5 0 0 -p 0.490392 0 -0.0975448 -p 0.461939 0 -0.191341 -p 0.415734 0 -0.277785 -p 0.353553 0 -0.353553 -p 0.277785 0 -0.415734 -p 0.191342 0 -0.461939 -p 0.0975453 0 -0.490392 -p 2.23517e-007 0 -0.5 -p -0.0975448 0 -0.490392 -p -0.191341 0 -0.461939 -p -0.277785 0 -0.415735 -p -0.353553 0 -0.353553 -p -0.415734 0 -0.277785 -p -0.461939 0 -0.191342 -p -0.490392 0 -0.0975453 -p -0.5 0 -1.63913e-007 -p -0.490392 0 0.097545 -p -0.46194 0 0.191341 -p -0.415735 0 0.277785 -p -0.353553 0 0.353553 -p -0.277785 0 0.415735 -p -0.191342 0 0.46194 -p -0.0975452 0 0.490392 -p -8.19564e-008 0 0.5 -p -8.03816e-008 0.0975452 0.490392 -p -7.57178e-008 0.191342 0.46194 -p -6.81442e-008 0.277785 0.415735 -p -5.79519e-008 0.353553 0.353553 -p -4.55325e-008 0.415735 0.277785 -p -3.13634e-008 0.46194 0.191342 -p -1.59889e-008 0.490393 0.0975451 -p 0 0.5 0 -p 4.36061e-008 0.490393 -0.0975451 -p 8.55364e-008 0.46194 -0.191342 -p 1.2418e-007 0.415735 -0.277785 -p 1.58051e-007 0.353553 -0.353553 -p 1.85848e-007 0.277785 -0.415734 -p 2.06503e-007 0.191342 -0.461939 -p 2.19223e-007 0.0975452 -0.490392 -p 2.23517e-007 0 -0.5 -p 2.19223e-007 -0.0975452 -0.490392 -p 2.06503e-007 -0.191342 -0.461939 -p 1.85848e-007 -0.277785 -0.415734 -p 1.58051e-007 -0.353553 -0.353553 -p 1.2418e-007 -0.415735 -0.277785 -p 8.55364e-008 -0.46194 -0.191342 -p 4.36061e-008 -0.490393 -0.0975451 -p 0 -0.5 0 -p -1.59889e-008 -0.490393 0.0975451 -p -3.13634e-008 -0.46194 0.191342 -p -4.55325e-008 -0.415735 0.277785 -p -5.79519e-008 -0.353553 0.353553 -p -6.81442e-008 -0.277785 0.415735 -p -7.57178e-008 -0.191342 0.46194 -p -8.03816e-008 -0.0975452 0.490392 -p -8.19564e-008 0 0.5 -p -0.0975452 0 0.490392 -p -0.191342 0 0.46194 -p -0.277785 0 0.415735 -p -0.353553 0 0.353553 -p -0.415735 0 0.277785 -p -0.46194 0 0.191341 -p -0.490392 0 0.097545 -p -0.5 0 -1.63913e-007 -p -0.490392 -0.0975452 -1.60763e-007 -p -0.461939 -0.191342 -1.51436e-007 -p -0.415735 -0.277785 -1.36288e-007 -p -0.353553 -0.353553 -1.15904e-007 -p -0.277785 -0.415735 -9.10651e-008 -p -0.191342 -0.46194 -6.27267e-008 -p -0.0975451 -0.490393 -3.19778e-008 -p 0 -0.5 0 -p 0.0975452 -0.490393 0 -p 0.191342 -0.46194 0 -p 0.277785 -0.415735 0 -p 0.353553 -0.353553 0 -p 0.415735 -0.277785 0 -p 0.46194 -0.191342 0 -p 0.490393 -0.0975452 0 -p 0.5 0 0 -p 0.490393 0.0975452 0 -p 0.46194 0.191342 0 -p 0.415735 0.277785 0 -p 0.353553 0.353553 0 -p 0.277785 0.415735 0 -p 0.191342 0.46194 0 -p 0.0975452 0.490393 0 -p 0 0.5 0 -p -0.0975451 0.490393 -3.19778e-008 -p -0.191342 0.46194 -6.27267e-008 -p -0.277785 0.415735 -9.10651e-008 -p -0.353553 0.353553 -1.15904e-007 -p -0.415735 0.277785 -1.36288e-007 -p -0.461939 0.191342 -1.51436e-007 -p -0.490392 0.0975452 -1.60763e-007 -p -0.5 0 -1.63913e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104");mc.DeleteHistory()
        self.findNestCompCtrl()
        self.strCtrl =mc.rename(self.strCtrl,self.compName)
        self.strCtrlDrv = mc.group(self.strCtrl,n=self.strCtrl +'_C')
        self.strCtrlGrp = mc.group(self.strCtrlDrv,n=self.strCtrl +'_G')
        mc.xform(self.strCtrlGrp,a=True,ws=True,t=self.jointPos)
        mc.makeIdentity(self.strCtrlGrp,apply=1,t=0,r=0,s=1,n=0)
        self.softSelJoint=mc.joint(self.strCtrl,p=self.jointPos,n=self.strCtrl+'_joint');mc.hide(self.softSelJoint)
        self.softSelJointGrp = mc.group(self.softSelJoint,n=self.strCtrl+'_joint_G')
        mc.setAttr(self.strCtrl+'.overrideEnabled',1)
        mc.setAttr(self.strCtrl+'.overrideColor',13) 
        mc.skinCluster(self.obj,e=1,wt=0,ai=self.softSelJoint)
        self.ObjSkinClusterNode=mm.eval('findRelatedSkinCluster(%s)'%('\"'+self.obj+'\"'))
        for i in range(0,self.allVetices):
            mc.skinPercent(self.ObjSkinClusterNode,self.obj+'.vtx['+str(i)+']',tv=[self.softSelJoint,self.weights[i]])
        mc.skinCluster(self.obj,e=1,lw=1,inf=self.softSelJoint)
        try:
            mc.select('Master',r=1)
        except:
            pass
        else:
            mc.parent(self.strCtrlGrp,'Master')
        mc.select(self.strCtrl,r=1)
    def findNestCompCtrl(self):
        
        getCtrlName=textField('ctrlName',q=1,text=1)
        
        if mc.objExists(getCtrlName+'_ctrl'+str(self.n))==True:
            self.n+=1
            self.findNestCompCtrl()
        else:
            self.compName=getCtrlName+'_ctrl'+str(self.n)
    def centerPos(self,selections):
        sel=mc.ls(mc.polyListComponentConversion(selections,tv=1),fl=1)
        sizeSel=len(sel)
        allSelPos=[]
        allSelPosX=[]
        allSelPosY=[]
        allSelPosZ=[]
        for i in range(0,sizeSel):
            pos=mc.xform(sel[i],q=1,ws=1,t=1)
            allSelPos.append(pos)
        for i in range(0,sizeSel):
            allSelPosX.append(allSelPos[i][0])
            allSelPosY.append(allSelPos[i][1])
            allSelPosZ.append(allSelPos[i][2])
        centerPosition=[(max(allSelPosX)+ min(allSelPosX))/2,(max(allSelPosY)+ min(allSelPosY))/2,(max(allSelPosZ)+ min(allSelPosZ))/2]
        return centerPosition
        
def doCreateCtrl():
    a=compCtrl()
    a.addCompCtrl()

softSelCtrl()