import maya.cmds as mc  
import maya.mel as mm 
class CreatJointCtrls():
    def __init__(self):
        self.shoulderJoints=[]
        self.handJoints=[]
    def CreatCtrls(self,rootJoint):
        self.creatFKSystemGRP()
        self.creatFKCtrls(rootJoint)
        self.DeformationSystem(rootJoint)
        if (len(self.shoulderJoints)>=1)&(len(self.handJoints)>=1):
            self.creatIKCtrls(self.shoulderJoints,self.handJoints)
    def mainCtrls(self):
        self.strMaster = mm.eval("curve -d 1 -p -1 0 -1 -p -1 0 -5 -p -2 0 -5 -p 0 0 -7 -p 2 0 -5 -p 1 0 -5 -p 1 0 -1 -p 5 0 -1 -p 5 0 -2 -p 7 0 0 -p 5 0 2 -p 5 0 1 -p 1 0 1 -p 1 0 5 -p 2 0 5 -p 0 0 7 -p -2 0 5 -p -1 0 5 -p -1 0 1 -p -5 0 1 -p -5 0 2 -p -7 0 0 -p -5 0 -2 -p -5 0 -1 -p -1 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 ")
        self.strMaster=mc.rename(self.strMaster,'Master')
        self.strMasterGrp = mc.group(self.strMaster,n='Master_GRP')
        self.strWorld = mc.circle(r=7,nr=(0,1,0),n='World');mc.DeleteHistory()
        self.strWorldGrp = mc.group(self.strWorld[0],n='RIG')
        mc.parent(self.strMasterGrp,self.strWorld[0])
        masterShape=mc.listRelatives(self.strMaster,s=1)[0]
        mc.setAttr(masterShape+'.overrideEnabled',1)
        mc.setAttr(masterShape+'.overrideColor',17)
    #---------------------------------------------------------------
    #-------------------------IKSystem------------------------------
    #---------------------------------------------------------------
    def creatIKCtrls(self,shoulders,hands):
        for i in shoulders:
            for n in hands:
                if mm.eval('isParentOf %s %s'%(i,n))==1:
                    self.IKFKBlendCtrl(i,n)
                    hendleJointsAndFKCtrls=self.creatIKJoints(i,n)
                    hendleJoints=hendleJointsAndFKCtrls[0]
                    FKCtrls=hendleJointsAndFKCtrls[1]
                    self.connectFKCtrls(i,n,FKCtrls)
                    IKHendleName=self.creatIKHendle(hendleJoints[0],hendleJoints[1])
                    self.handIKCtrl(i,n,IKHendleName)
                    if mc.listRelatives(i,c=1,pa=1)[0]!=n:
                        self.poleCtrl(i,n,IKHendleName)
    def IKFKBlendCtrl(self,shoulder,hand):
        CtrlName=mm.eval('curve -d 1 -p -0.45 0.15 0 -p -0.15 0.15 0 -p -0.15 0.45 0 -p 0.15 0.45 0 -p 0.15 0.15 0 -p 0.45 0.15 0 -p 0.45 -0.15 0 -p 0.15 -0.15 0 -p 0.15 -0.45 0 -p -0.15 -0.45 0 -p -0.15 -0.15 0 -p -0.45 -0.15 0 -p -0.45 0.15 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;')
        CtrlName=mc.rename(CtrlName,shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend')
        CtrlNameGRP=mc.group(CtrlName,n=CtrlName+'_GRP')
        self.shoulderPos=mc.xform(shoulder,q=1,ws=1,t=1)
        self.handPos=mc.xform(hand,q=1,ws=1,t=1)
        self.midJoint=mc.listRelatives(shoulder,c=1,pa=1)[0]
        self.midPos=mc.xform(self.midJoint,q=1,ws=1,t=1)
        mc.camera(n='xformCamera1')
        mm.eval('cameraMakeNode 3 \"xformCamera1\"')
        mc.xform('xformCamera1',ws=1,t=self.shoulderPos)
        mc.xform('xformCamera1_aim',ws=1,t=self.handPos)
        mc.xform('xformCamera1_up',ws=1,t=self.midPos)
        self.cameraRot=mc.xform('xformCamera1',q=1,ws=1,ro=1)
        vectorShouldToHand=[self.handPos[0]-self.shoulderPos[0],self.handPos[1]-self.shoulderPos[1],self.handPos[2]-self.shoulderPos[2]]
        self.distance=pow(pow(vectorShouldToHand[0],2)+pow(vectorShouldToHand[1],2)+pow(vectorShouldToHand[2],2),0.5)
        mc.xform(CtrlNameGRP,ws=1,t=self.shoulderPos,ro=self.cameraRot)
        mc.xform(CtrlNameGRP,os=1,r=1,t=[-self.distance/6,self.distance/6,-self.distance/3])
        mc.delete('xformCamera1_group')
        mc.setAttr(CtrlName+'.overrideEnabled',1)
        mc.setAttr(CtrlName+'.overrideColor',6)
        mc.addAttr(CtrlName,ln='IK_FKBlend',at='enum',en='FK:IK:',k=1)
        mc.setAttr(CtrlName+'.tx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.ty',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.tz',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.rx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.ry',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.rz',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.sx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.sy',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.sz',lock=True,keyable=False,channelBox=False)
        mc.setAttr(CtrlName+'.v',lock=True,keyable=False,channelBox=False)
        mc.shadingNode('plusMinusAverage',asUtility=1,n=CtrlName+'_FKOutput')
        mc.setAttr(CtrlName+'_FKOutput.operation',2)
        mc.setAttr(CtrlName+'_FKOutput.input3D[0].input3Dx',1)
        mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',CtrlName+'_FKOutput.input3D[1].input3Dx')
        mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend_FKOutput.output3Dx',shoulder.replace('|','_')+'_parentConstraint.'+shoulder.replace('|','_')+'_firstCtrlJointW0')
        IKFKSystemGRP=mc.group(CtrlNameGRP,n=shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFKSystem')
        try:
            mc.select('IKFKSystem',r=1)
        except:
            mc.group(em=1,n='IKFKSystem')
            mc.parent('IKFKSystem','MotionSystem')
        mc.parent(IKFKSystemGRP,'IKFKSystem')
        mc.select(cl=1)
    def poleCtrl(self,shoulder,hand,ikHendle):
        PoleCtrl=mm.eval('curve -d 1 -p -8.19564e-008 0 0.5 -p 0.0975451 0 0.490393 -p 0.191342 0 0.46194 -p 0.277785 0 0.415735 -p 0.353553 0 0.353553 -p 0.415735 0 0.277785 -p 0.46194 0 0.191342 -p 0.490393 0 0.0975452 -p 0.5 0 0 -p 0.490392 0 -0.0975448 -p 0.461939 0 -0.191341 -p 0.415734 0 -0.277785 -p 0.353553 0 -0.353553 -p 0.277785 0 -0.415734 -p 0.191342 0 -0.461939 -p 0.0975453 0 -0.490392 -p 2.23517e-007 0 -0.5 -p -0.0975448 0 -0.490392 -p -0.191341 0 -0.461939 -p -0.277785 0 -0.415735 -p -0.353553 0 -0.353553 -p -0.415734 0 -0.277785 -p -0.461939 0 -0.191342 -p -0.490392 0 -0.0975453 -p -0.5 0 -1.63913e-007 -p -0.490392 0 0.097545 -p -0.46194 0 0.191341 -p -0.415735 0 0.277785 -p -0.353553 0 0.353553 -p -0.277785 0 0.415735 -p -0.191342 0 0.46194 -p -0.0975452 0 0.490392 -p -8.19564e-008 0 0.5 -p -8.03816e-008 0.0975452 0.490392 -p -7.57178e-008 0.191342 0.46194 -p -6.81442e-008 0.277785 0.415735 -p -5.79519e-008 0.353553 0.353553 -p -4.55325e-008 0.415735 0.277785 -p -3.13634e-008 0.46194 0.191342 -p -1.59889e-008 0.490393 0.0975451 -p 0 0.5 0 -p 4.36061e-008 0.490393 -0.0975451 -p 8.55364e-008 0.46194 -0.191342 -p 1.2418e-007 0.415735 -0.277785 -p 1.58051e-007 0.353553 -0.353553 -p 1.85848e-007 0.277785 -0.415734 -p 2.06503e-007 0.191342 -0.461939 -p 2.19223e-007 0.0975452 -0.490392 -p 2.23517e-007 0 -0.5 -p 2.19223e-007 -0.0975452 -0.490392 -p 2.06503e-007 -0.191342 -0.461939 -p 1.85848e-007 -0.277785 -0.415734 -p 1.58051e-007 -0.353553 -0.353553 -p 1.2418e-007 -0.415735 -0.277785 -p 8.55364e-008 -0.46194 -0.191342 -p 4.36061e-008 -0.490393 -0.0975451 -p 0 -0.5 0 -p -1.59889e-008 -0.490393 0.0975451 -p -3.13634e-008 -0.46194 0.191342 -p -4.55325e-008 -0.415735 0.277785 -p -5.79519e-008 -0.353553 0.353553 -p -6.81442e-008 -0.277785 0.415735 -p -7.57178e-008 -0.191342 0.46194 -p -8.03816e-008 -0.0975452 0.490392 -p -8.19564e-008 0 0.5 -p -0.0975452 0 0.490392 -p -0.191342 0 0.46194 -p -0.277785 0 0.415735 -p -0.353553 0 0.353553 -p -0.415735 0 0.277785 -p -0.46194 0 0.191341 -p -0.490392 0 0.097545 -p -0.5 0 -1.63913e-007 -p -0.490392 -0.0975452 -1.60763e-007 -p -0.461939 -0.191342 -1.51436e-007 -p -0.415735 -0.277785 -1.36288e-007 -p -0.353553 -0.353553 -1.15904e-007 -p -0.277785 -0.415735 -9.10651e-008 -p -0.191342 -0.46194 -6.27267e-008 -p -0.0975451 -0.490393 -3.19778e-008 -p 0 -0.5 0 -p 0.0975452 -0.490393 0 -p 0.191342 -0.46194 0 -p 0.277785 -0.415735 0 -p 0.353553 -0.353553 0 -p 0.415735 -0.277785 0 -p 0.46194 -0.191342 0 -p 0.490393 -0.0975452 0 -p 0.5 0 0 -p 0.490393 0.0975452 0 -p 0.46194 0.191342 0 -p 0.415735 0.277785 0 -p 0.353553 0.353553 0 -p 0.277785 0.415735 0 -p 0.191342 0.46194 0 -p 0.0975452 0.490393 0 -p 0 0.5 0 -p -0.0975451 0.490393 -3.19778e-008 -p -0.191342 0.46194 -6.27267e-008 -p -0.277785 0.415735 -9.10651e-008 -p -0.353553 0.353553 -1.15904e-007 -p -0.415735 0.277785 -1.36288e-007 -p -0.461939 0.191342 -1.51436e-007 -p -0.490392 0.0975452 -1.60763e-007 -p -0.5 0 -1.63913e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104')
        PoleCtrl=mc.rename(PoleCtrl,self.midJoint.replace('|','_')+"_PoleCtrl")
        PoleCtrlDriven=mc.group(PoleCtrl,n=PoleCtrl+'_driven')
        PoleCtrlGRP=mc.group(PoleCtrlDriven,n=PoleCtrl+'_GRP')
        mc.setAttr(PoleCtrl+'.overrideEnabled',1)
        mc.setAttr(PoleCtrl+'.overrideColor',13)
        mc.xform(PoleCtrlGRP,ws=1,t=self.midPos)
        mc.spaceLocator(p=[0,0,0],n='xformLocator')
        mc.xform('xformLocator',ws=1,t=self.shoulderPos)
        mc.xform('xformLocator',ws=1,ro=self.cameraRot)
        mc.parentConstraint('xformLocator',PoleCtrlGRP,w=1,mo=1)
        mc.xform('xformLocator',os=1,wd=1,r=1,t=[0,self.distance/2,0])
        mc.select(PoleCtrlGRP,r=1)
        mm.eval('setConstraintRestPosition;')
        mc.parentConstraint('xformLocator',PoleCtrlGRP,rm=1)
        mc.delete('xformLocator')
        mc.poleVectorConstraint(PoleCtrl,ikHendle)
        mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',PoleCtrl+'.visibility') 
        annotateShape=mc.annotate(PoleCtrl,p=self.midPos)
        annotateName=mc.listRelatives(annotateShape,p=1,pa=1)[0]
        annotateName=mc.rename(annotateName,self.midJoint.replace('|','_')+'_annotate')
        mc.parentConstraint(self.midJoint.replace('|','_')+'_IKCtrlJoint',annotateName,w=1,mo=1)
        mc.setAttr(annotateName+'.overrideEnabled',1)
        mc.setAttr(annotateName+'.overrideDisplayType',2)
        mc.parentConstraint(hand.replace('|','_')+'_IKCtrl',PoleCtrlGRP,w=1,mo=1,n=PoleCtrlGRP.replace('|','_')+'_parentConstraint')
        mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',annotateName+'.visibility') 
        mc.parent(PoleCtrlGRP,self.IKSystemGRP)
        mc.parent(annotateName,self.IKSystemGRP)
        mc.addAttr(PoleCtrl,ln='Follow',at='float',hnv=1,hxv=1,min=0,max=1,dv=1,k=1)
        mc.connectAttr(PoleCtrl+'.Follow',PoleCtrl+'_GRP_parentConstraint.'+hand.replace('|','_')+'_IKCtrlW0')
        mc.setAttr(PoleCtrl+'.rx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(PoleCtrl+'.ry',lock=True,keyable=False,channelBox=False)
        mc.setAttr(PoleCtrl+'.rz',lock=True,keyable=False,channelBox=False)
        mc.setAttr(PoleCtrl+'.sx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(PoleCtrl+'.sy',lock=True,keyable=False,channelBox=False)
        mc.setAttr(PoleCtrl+'.sz',lock=True,keyable=False,channelBox=False)
        mc.setAttr(PoleCtrl+'.v',lock=True,keyable=False,channelBox=False)
        mc.select(cl=1)
    def handIKCtrl(self,shoulder,hand,IKHendle):
        pos=mc.xform(hand,q=1,ws=1,t=1)
        rot=mc.xform(hand,q=1,ws=1,ro=1)
        handIKCtrlName=mm.eval("curve -d 1 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16")
        handIKCtrlName=mc.rename(handIKCtrlName,hand.replace('|','_')+'_IKCtrl')
        handIKCtrlDriven=mc.group(handIKCtrlName,n=handIKCtrlName+'_driven')
        handIKCtrlGRP=mc.group(handIKCtrlDriven,n=handIKCtrlName+'_GRP')
        mc.xform(handIKCtrlGRP,ws=1,t=pos,ro=rot)
        mc.parent(IKHendle,handIKCtrlName)
        mc.orientConstraint(handIKCtrlName,hand.replace('|','_')+'_IKCtrlJoint',w=1,mo=0)
        mc.setAttr(handIKCtrlName+'.overrideEnabled',1)
        mc.setAttr(handIKCtrlName+'.overrideColor',13)
        mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',handIKCtrlName+'.visibility')  
        mc.parent(handIKCtrlGRP,shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKSystem')
        mc.setAttr(handIKCtrlName+'.sx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(handIKCtrlName+'.sy',lock=True,keyable=False,channelBox=False)
        mc.setAttr(handIKCtrlName+'.sz',lock=True,keyable=False,channelBox=False)
        mc.setAttr(handIKCtrlName+'.v',lock=True,keyable=False,channelBox=False)
        handChildren=mc.listRelatives(hand,c=1,type='joint',pa=1)
        if handChildren!=None:
            for child in handChildren:
                try:
                    childFKCtrlGRP=child.replace('|','_')+'_FKCtrl_GRP'
                    ConstraintName=mc.parentConstraint(handIKCtrlName,childFKCtrlGRP,w=1,mo=1)[0]
                    ConstraintAttrName=ConstraintName+'.'+handIKCtrlName+'W0'
                    mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',ConstraintAttrName)
                except:
                    pass
    def creatIKHendle(self,Joint1,Joint2):
        IKHendleName=mc.ikHandle(sol='ikRPsolver',sj=Joint1,ee=Joint2,n=Joint1+'_'+Joint2+'_ikHandle')[0]
        mc.hide(IKHendleName)
        return IKHendleName
    def creatIKJoints(self,shoulder,hand):
        IKHendleJoints=[]
        FKCtrls=[]
        try:
            mc.select('IKSystem',r=1)
        except:
            mc.group(em=1,n='IKSystem')
            mc.parent('IKSystem','MotionSystem')
        FKCtrls.append(shoulder.replace('|','_')+'_FKCtrl')
        pos=mc.xform(shoulder,q=1,ws=1,t=1)
        rot=mc.xform(shoulder,q=1,ws=1,ro=1)
        shoulderParentJoint=mc.listRelatives(shoulder,p=1,pa=1)[0]
        self.IKSystemGRP=mc.group(em=1,n=shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKSystem')
        firstIKCtrlJoint=mc.joint(self.IKSystemGRP,p=pos,sc=0,n=shoulder.replace('|','_')+'_IKCtrlJoint')
        IKHendleJoints.append(firstIKCtrlJoint)
        mc.xform(firstIKCtrlJoint,ws=1,t=pos,ro=rot)
        mc.makeIdentity(firstIKCtrlJoint,apply=1,t=1,r=1,s=1,n=0)
        mc.parentConstraint(firstIKCtrlJoint,shoulder,w=1,mo=0,n=shoulder.replace('|','_')+'_parentConstraint')
        mc.parentConstraint(shoulderParentJoint,firstIKCtrlJoint,w=1,mo=1,n=firstIKCtrlJoint.replace('|','_')+'_parentConstraint')
        mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',shoulder.replace('|','_')+'_parentConstraint.'+shoulder.replace('|','_')+'_IKCtrlJointW1')
        mc.parent(self.IKSystemGRP,'IKSystem')
        def creatMidIKCtrlJoint(bone):
            FKCtrls.append(bone.replace('|','_')+'_FKCtrl')
            pos=mc.xform(bone,q=1,ws=1,t=1)
            rot=mc.xform(bone,q=1,ws=1,ro=1)
            parentJoint=mc.listRelatives(bone,p=1,pa=1)[0]
            midIKCtrlJoint=mc.joint(parentJoint.replace('|','_')+'_IKCtrlJoint',p=pos,sc=0,n=bone.replace('|','_')+'_IKCtrlJoint')
            mc.xform(midIKCtrlJoint,ws=1,t=pos,ro=rot)
            mc.makeIdentity(midIKCtrlJoint,apply=1,t=1,r=1,s=1,n=0)
            mc.parentConstraint(midIKCtrlJoint,bone,w=1,mo=0,n=bone.replace('|','_')+'_parentConstraint')
            mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',bone.replace('|','_')+'_parentConstraint.'+bone.replace('|','_')+'_IKCtrlJointW1')
            mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend_FKOutput.output3Dx',bone.replace('|','_')+'_parentConstraint.'+bone.replace('|','_')+'_firstCtrlJointW0')
            childJoint=mc.listRelatives(bone,c=1,pa=1)[0]
            if childJoint!=hand:
                creatMidIKCtrlJoint(childJoint)
            else:
                creatHandIKCtrlJoint(hand)
        def creatHandIKCtrlJoint(bone):
            pos=mc.xform(bone,q=1,ws=1,t=1)
            rot=mc.xform(bone,q=1,ws=1,ro=1)
            parentJoint=mc.listRelatives(bone,p=1,pa=1)[0]
            lastIKCtrlJoint=mc.joint(parentJoint.replace('|','_')+'_IKCtrlJoint',p=pos,sc=0,n=bone.replace('|','_')+'_IKCtrlJoint')
            IKHendleJoints.append(lastIKCtrlJoint)
            mc.xform(lastIKCtrlJoint,ws=1,t=pos,ro=rot)
            mc.makeIdentity(lastIKCtrlJoint,apply=1,t=1,r=1,s=1,n=0)
            if mc.listRelatives(bone,c=1,pa=1)!=None:
                FKCtrls.append(bone.replace('|','_')+'_FKCtrl')
                mc.parentConstraint(lastIKCtrlJoint,bone,w=1,mo=0,n=bone.replace('|','_')+'_parentConstraint')
                mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend.IK_FKBlend',bone.replace('|','_')+'_parentConstraint.'+bone.replace('|','_')+'_IKCtrlJointW1')
                mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend_FKOutput.output3Dx',bone.replace('|','_')+'_parentConstraint.'+bone.replace('|','_')+'_firstCtrlJointW0')             
        if self.midJoint!=hand:
            creatMidIKCtrlJoint(self.midJoint)
        else:
            creatHandIKCtrlJoint(hand)
        mc.hide(firstIKCtrlJoint)
        return [IKHendleJoints,FKCtrls]
    #---------------------------------------------------------------
    #-------------------------FKSystem------------------------------
    #---------------------------------------------------------------
    def creatFKSystemGRP(self):
        try:
            mc.select('Master',r=1)
        except:
            self.mainCtrls()
        try:
            mc.select('FKSystem',r=1)
        except:
            mc.group(em=1,n='FKSystem')
            mc.group('FKSystem',n='MotionSystem')
            mc.parent('MotionSystem','Master') 
    def creatFKCtrls(self,rootJoint):
        self.JointLabType=mc.getAttr(rootJoint+'.type')          
        if self.JointLabType==10:
            if not rootJoint in self.shoulderJoints:
                self.shoulderJoints.append(rootJoint)
        if self.JointLabType==12:
            if not rootJoint in self.handJoints:
                self.handJoints.append(rootJoint)        
        self.parentJoint=mc.listRelatives(rootJoint,p=1,pa=1)
        self.childJoint=mc.listRelatives(rootJoint,c=1,pa=1)
        if self.childJoint!=None:
            rootCtrlGRP=self.creatFKCtrl(rootJoint)
            if self.parentJoint!=None:
                try:
                    mc.parent(rootCtrlGRP,self.parentJoint[0].replace('|','_')+'_FKCtrl')
                except:
                    mc.parent(rootCtrlGRP,'FKSystem')
            else:
                mc.parent(rootCtrlGRP,'FKSystem')
            for one in self.childJoint:
                self.creatFKCtrls(one)
    def creatFKCtrl(self,bone):
        self.CtrlPos=mc.xform(bone,q=1,ws=1,t=1)
        self.CtrlRot=mc.xform(bone,q=1,ws=1,ro=1)
        self.CtrlName=mc.circle(nr=[1,0,0],n=bone+'_FKCtrl')[0];mc.DeleteHistory()
        self.CtrlDriven=mc.group(self.CtrlName,n=self.CtrlName+'_driven')
        self.CtrlGRP=mc.group(self.CtrlDriven,n=self.CtrlName+'_GRP')
        mc.xform(self.CtrlGRP,ws=1,t=self.CtrlPos,ro=self.CtrlRot)
        self.firstCtrlJoint=mc.joint(self.CtrlName,sc=0,p=self.CtrlPos,n=bone+'_firstCtrlJoint')
        mc.xform(self.firstCtrlJoint,ws=1,t=self.CtrlPos,ro=self.CtrlRot)
        mc.makeIdentity(self.firstCtrlJoint,apply=1,t=1,r=1,s=1,n=0)
        self.ChildJoints=mc.listRelatives(bone,c=1,pa=1)
        for one in self.ChildJoints:
            ChildPos=mc.xform(one,q=1,ws=1,t=1)
            ChildRot=mc.xform(one,q=1,ws=1,ro=1)
            lastCtrlJoint=mc.joint(self.firstCtrlJoint,sc=0,p=ChildPos,n=bone+'_lastCtrlJoint')
            mc.xform(lastCtrlJoint,ws=1,t=ChildPos,ro=ChildRot)
            mc.makeIdentity(lastCtrlJoint,apply=1,t=1,r=1,s=1,n=0)
        mc.hide(self.firstCtrlJoint)
        mc.parentConstraint(self.firstCtrlJoint,bone,w=1,mo=1,n=bone.replace('|','_')+'_parentConstraint')
        mc.scaleConstraint(self.firstCtrlJoint,bone,w=1,mo=1,n=bone.replace('|','_')+'_scaleConstraint')
        mc.setAttr(self.CtrlName+'.overrideEnabled',1)
        mc.setAttr(self.CtrlName+'.overrideColor',18)
        '''mc.setAttr(self.CtrlName+'.sx',lock=True,keyable=False,channelBox=False)
        mc.setAttr(self.CtrlName+'.sy',lock=True,keyable=False,channelBox=False)
        mc.setAttr(self.CtrlName+'.sz',lock=True,keyable=False,channelBox=False)'''
        mc.setAttr(self.CtrlName+'.v',lock=True,keyable=False,channelBox=False)
        return self.CtrlGRP
    def connectFKCtrls(self,shoulder,hand,Ctrls):
        for i in Ctrls:
            CtrlShape=mc.listRelatives(i,s=1,pa=1)[0]
            mc.connectAttr(shoulder.replace('|','_')+'_'+hand.replace('|','_')+'_IKFK_Blend_FKOutput.output3Dx',CtrlShape+'.visibility') 
    def DeformationSystem(self,rootJoint):
        try:
            mc.select('DeformationSystem',r=1)
        except:
            mc.group(em=1,n='DeformationSystem')
            mc.parent('DeformationSystem','Master')
        mc.parent(rootJoint,'DeformationSystem')
        mc.select(cl=1)