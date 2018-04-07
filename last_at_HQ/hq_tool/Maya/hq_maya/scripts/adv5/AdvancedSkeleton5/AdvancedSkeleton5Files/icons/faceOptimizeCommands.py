#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm

####

def ChangeToCurve():
	if mc.objExists('FaceControlSet'):
		dir={'Blue':6,'Brown':21,'Cyan':18,'Green':26,'Red':13}
		FaceControlSet=mc.sets('FaceControlSet',q=1)
		for i in FaceControlSet:
			shapeNode=mc.listRelatives(i,s=1)[0]
			if mc.nodeType(shapeNode)=='nurbsSurface':
				SGNode=mc.listConnections(shapeNode,type='shadingEngine')[0]
				shadeNode=mc.listConnections(SGNode,type='lambert')[0]
				key=shadeNode.split('asFace')[1]
				BallCtrl(i)
				mc.setAttr(shapeNode+'.overrideEnabled',1)
				mc.setAttr(shapeNode+'.overrideColor',dir[key])
def BallCtrl(one):       
	oneBB=mc.xform(one,q=1,ws=1,bb=1)
	size=(oneBB[3]-oneBB[0]+oneBB[5]-oneBB[2])/2
	ballCtrl=mm.eval('curve -d 1 -p -8.19564e-008 0 0.5 -p 0.0975451 0 0.490393 -p 0.191342 0 0.46194 -p 0.277785 0 0.415735 -p 0.353553 0 0.353553 -p 0.415735 0 0.277785 -p 0.46194 0 0.191342 -p 0.490393 0 0.0975452 -p 0.5 0 0 -p 0.490392 0 -0.0975448 -p 0.461939 0 -0.191341 -p 0.415734 0 -0.277785 -p 0.353553 0 -0.353553 -p 0.277785 0 -0.415734 -p 0.191342 0 -0.461939 -p 0.0975453 0 -0.490392 -p 2.23517e-007 0 -0.5 -p -0.0975448 0 -0.490392 -p -0.191341 0 -0.461939 -p -0.277785 0 -0.415735 -p -0.353553 0 -0.353553 -p -0.415734 0 -0.277785 -p -0.461939 0 -0.191342 -p -0.490392 0 -0.0975453 -p -0.5 0 -1.63913e-007 -p -0.490392 0 0.097545 -p -0.46194 0 0.191341 -p -0.415735 0 0.277785 -p -0.353553 0 0.353553 -p -0.277785 0 0.415735 -p -0.191342 0 0.46194 -p -0.0975452 0 0.490392 -p -8.19564e-008 0 0.5 -p -8.03816e-008 0.0975452 0.490392 -p -7.57178e-008 0.191342 0.46194 -p -6.81442e-008 0.277785 0.415735 -p -5.79519e-008 0.353553 0.353553 -p -4.55325e-008 0.415735 0.277785 -p -3.13634e-008 0.46194 0.191342 -p -1.59889e-008 0.490393 0.0975451 -p 0 0.5 0 -p 4.36061e-008 0.490393 -0.0975451 -p 8.55364e-008 0.46194 -0.191342 -p 1.2418e-007 0.415735 -0.277785 -p 1.58051e-007 0.353553 -0.353553 -p 1.85848e-007 0.277785 -0.415734 -p 2.06503e-007 0.191342 -0.461939 -p 2.19223e-007 0.0975452 -0.490392 -p 2.23517e-007 0 -0.5 -p 2.19223e-007 -0.0975452 -0.490392 -p 2.06503e-007 -0.191342 -0.461939 -p 1.85848e-007 -0.277785 -0.415734 -p 1.58051e-007 -0.353553 -0.353553 -p 1.2418e-007 -0.415735 -0.277785 -p 8.55364e-008 -0.46194 -0.191342 -p 4.36061e-008 -0.490393 -0.0975451 -p 0 -0.5 0 -p -1.59889e-008 -0.490393 0.0975451 -p -3.13634e-008 -0.46194 0.191342 -p -4.55325e-008 -0.415735 0.277785 -p -5.79519e-008 -0.353553 0.353553 -p -6.81442e-008 -0.277785 0.415735 -p -7.57178e-008 -0.191342 0.46194 -p -8.03816e-008 -0.0975452 0.490392 -p -8.19564e-008 0 0.5 -p -0.0975452 0 0.490392 -p -0.191342 0 0.46194 -p -0.277785 0 0.415735 -p -0.353553 0 0.353553 -p -0.415735 0 0.277785 -p -0.46194 0 0.191341 -p -0.490392 0 0.097545 -p -0.5 0 -1.63913e-007 -p -0.490392 -0.0975452 -1.60763e-007 -p -0.461939 -0.191342 -1.51436e-007 -p -0.415735 -0.277785 -1.36288e-007 -p -0.353553 -0.353553 -1.15904e-007 -p -0.277785 -0.415735 -9.10651e-008 -p -0.191342 -0.46194 -6.27267e-008 -p -0.0975451 -0.490393 -3.19778e-008 -p 0 -0.5 0 -p 0.0975452 -0.490393 0 -p 0.191342 -0.46194 0 -p 0.277785 -0.415735 0 -p 0.353553 -0.353553 0 -p 0.415735 -0.277785 0 -p 0.46194 -0.191342 0 -p 0.490393 -0.0975452 0 -p 0.5 0 0 -p 0.490393 0.0975452 0 -p 0.46194 0.191342 0 -p 0.415735 0.277785 0 -p 0.353553 0.353553 0 -p 0.277785 0.415735 0 -p 0.191342 0.46194 0 -p 0.0975452 0.490393 0 -p 0 0.5 0 -p -0.0975451 0.490393 -3.19778e-008 -p -0.191342 0.46194 -6.27267e-008 -p -0.277785 0.415735 -9.10651e-008 -p -0.353553 0.353553 -1.15904e-007 -p -0.415735 0.277785 -1.36288e-007 -p -0.461939 0.191342 -1.51436e-007 -p -0.490392 0.0975452 -1.60763e-007 -p -0.5 0 -1.63913e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104')
	mc.xform(ballCtrl,ws=1,s=[size,size,size])
	mc.makeIdentity(ballCtrl,apply=1,t=0,r=0,s=1,n=0)
	ballCtrlShape=mc.listRelatives(ballCtrl,s=True)
	oneShape=mc.listRelatives(one,s=True)
	mc.parent(ballCtrlShape,one,s=True,add=True)
	mc.delete(oneShape,ballCtrl)
	mc.rename(ballCtrlShape,oneShape)
def adv_tongueCtrl():
	
	face_joint0="faceRigTongue0_M"
	face_joint1="faceRigTongue1_M"
	face_joint2="faceRigTongue2_M"
	face_joint3="faceRigTongue3_M"
	tongue_joint=[face_joint0,face_joint1,face_joint2,face_joint3]
	
	mc.disconnectAttr("ctrlTongue_M.rotX1","faceRigTongue1_M.rx")
	mc.disconnectAttr("ctrlTongue_M.rotY1","faceRigTongue1_M.ry")
	mc.disconnectAttr("ctrlTongue_M.rotZ1","faceRigTongue1_M.rz")
	mc.disconnectAttr("ctrlTongue_M.sizeX","faceRigTongue1_M.sx")
	mc.disconnectAttr("ctrlTongue_M.sizeY","faceRigTongue1_M.sy")
	mc.disconnectAttr("ctrlTongue_M.sizeZ","faceRigTongue1_M.sz")
	
	mc.disconnectAttr("ctrlTongue_M.rotX2","faceRigTongue2_M.rx")
	mc.disconnectAttr("ctrlTongue_M.rotY2","faceRigTongue2_M.ry")
	mc.disconnectAttr("ctrlTongue_M.rotZ2","faceRigTongue2_M.rz")
	mc.disconnectAttr("ctrlTongue_M.sizeX","faceRigTongue2_M.sx")
	mc.disconnectAttr("ctrlTongue_M.sizeY","faceRigTongue2_M.sy")
	mc.disconnectAttr("ctrlTongue_M.sizeZ","faceRigTongue2_M.sz")
	
	mc.disconnectAttr("ctrlTongue_M.rotX3","faceRigTongue3_M.rx")
	mc.disconnectAttr("ctrlTongue_M.rotY3","faceRigTongue3_M.ry")
	mc.disconnectAttr("ctrlTongue_M.rotZ3","faceRigTongue3_M.rz")
	mc.disconnectAttr("ctrlTongue_M.sizeX","faceRigTongue3_M.sx")
	mc.disconnectAttr("ctrlTongue_M.sizeY","faceRigTongue3_M.sy")
	mc.disconnectAttr("ctrlTongue_M.sizeZ","faceRigTongue3_M.sz")
	
	mc.select(cl=True)
	mc.group(n="Aim_TongueJoint_G",em=True)
	mc.xform(os=True,piv=(0,0,0))
	del_par=mc.parentConstraint(tongue_joint[0],"Aim_TongueJoint_G",weight=1)
	mc.delete(del_par)
	mc.parentConstraint(tongue_joint[0],"Aim_TongueJoint_G",weight=1,mo=1)
	
	tongueCtrl_n="TongueCtrl"
	tongue_ctrl=[]
	for i in range(1,4):
		str_i=str(i)
		tongue_ctrl.append(tongueCtrl_n+str_i)
		cur_n=mc.curve(d=1,p=((0,0,0),(0,4.81692e-010,0.0195488),(0,0.00393608,0.023481),(0,6.75474e-010,0.0274132),(0,-0.00393608,0.023481),(0,4.81692e-010,0.0195488)),k=(0,1,2,3,4,5))
		mc.rename(cur_n,tongue_ctrl[i-1])
		ctrl_shape=mc.listRelatives(tongue_ctrl[i-1],s=True)
		mc.setAttr((ctrl_shape[0]+".overrideEnabled"),1)
		mc.setAttr((ctrl_shape[0]+".overrideColor"),17)
		mc.setAttr((tongue_ctrl[i-1]+".tx"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((tongue_ctrl[i-1]+".ty"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((tongue_ctrl[i-1]+".tz"),lock=True,keyable=False,channelBox=False) 
		mc.setAttr((tongue_ctrl[i-1]+".v"),lock=True,keyable=False,channelBox=False)
		
		mc.group(n=(tongue_ctrl[i-1]+"_C"))
		mc.xform(os=True,piv=(0,0,0))
		mc.group(n=(tongue_ctrl[i-1]+"_G"))
		mc.xform(os=True,piv=(0,0,0))
		
		p3=tongue_joint[i]
		p4=tongue_ctrl[i-1]+"_G"
		par_n=mc.parentConstraint(p3,p4,weight=1)
		mc.delete(par_n)
		mc.parent(p4,"Aim_TongueJoint_G")
		
	mc.parentConstraint("TongueCtrl1","TongueCtrl2_G",weight=1,mo=1)
	mc.parentConstraint("TongueCtrl2","TongueCtrl3_G",weight=1,mo=1)
	mc.select(cl=True)
	
	
	
	attr_x="ctrlTongue_M.rotX"
	attr_y="ctrlTongue_M.rotY"
	attr_z="ctrlTongue_M.rotZ"
	attr_sx="ctrlTongue_M.sizeX"
	attr_sy="ctrlTongue_M.sizeY"
	attr_sz="ctrlTongue_M.sizeZ"
	for i in range(1,4):
		str_i=str(i)
		mc.connectAttr((attr_x+str_i),(tongue_ctrl[i-1]+"_C"+".rx"),f=True)
		mc.connectAttr((attr_y+str_i),(tongue_ctrl[i-1]+"_C"+".ry"),f=True)
		mc.connectAttr((attr_z+str_i),(tongue_ctrl[i-1]+"_C"+".rz"),f=True)
		mc.connectAttr(attr_sx,(tongue_ctrl[i-1]+"_C"+".sx"),f=True)
		mc.connectAttr(attr_sy,(tongue_ctrl[i-1]+"_C"+".sy"),f=True)
		mc.connectAttr(attr_sz,(tongue_ctrl[i-1]+"_C"+".sz"),f=True)
		
		
		pMA1_n=tongue_joint[i]+"_M_pMA1"
		mc.shadingNode("plusMinusAverage",n=pMA1_n,asUtility=True)
		mc.connectAttr((attr_x+str_i),(pMA1_n+".input3D[0].input3Dx"),f=True)
		mc.connectAttr((attr_y+str_i),(pMA1_n+".input3D[0].input3Dy"),f=True)
		mc.connectAttr((attr_z+str_i),(pMA1_n+".input3D[0].input3Dz"),f=True)
		mc.connectAttr((tongue_ctrl[i-1]+".rx"),(pMA1_n+".input3D[1].input3Dx"),f=True)
		mc.connectAttr((tongue_ctrl[i-1]+".ry"),(pMA1_n+".input3D[1].input3Dy"),f=True)
		mc.connectAttr((tongue_ctrl[i-1]+".rz"),(pMA1_n+".input3D[1].input3Dz"),f=True)
		
		
		pMA2_n=tongue_joint[i]+"_M_pMA2"
		mc.shadingNode("plusMinusAverage",n=pMA2_n,asUtility=True)
		mc.connectAttr((attr_sx),(pMA2_n+".input3D[0].input3Dx"),f=True)
		mc.connectAttr((attr_sy),(pMA2_n+".input3D[0].input3Dy"),f=True)
		mc.connectAttr((attr_sz),(pMA2_n+".input3D[0].input3Dz"),f=True)
		mc.connectAttr((tongue_ctrl[i-1]+".sx"),(pMA2_n+".input3D[1].input3Dx"),f=True)
		mc.connectAttr((tongue_ctrl[i-1]+".sy"),(pMA2_n+".input3D[1].input3Dy"),f=True)
		mc.connectAttr((tongue_ctrl[i-1]+".sz"),(pMA2_n+".input3D[1].input3Dz"),f=True)
		mc.setAttr((pMA2_n+".input3D[3].input3Dx"),-1)
		mc.setAttr((pMA2_n+".input3D[3].input3Dy"),-1)
		mc.setAttr((pMA2_n+".input3D[3].input3Dz"),-1)
		
		
		mc.connectAttr((pMA1_n+".output3Dx"),(tongue_joint[i]+".rx"),f=True)
		mc.connectAttr((pMA1_n+".output3Dy"),(tongue_joint[i]+".ry"),f=True)
		mc.connectAttr((pMA1_n+".output3Dz"),(tongue_joint[i]+".rz"),f=True)
		mc.connectAttr((pMA2_n+".output3Dx"),(tongue_joint[i]+".sx"),f=True)
		mc.connectAttr((pMA2_n+".output3Dy"),(tongue_joint[i]+".sy"),f=True)
		mc.connectAttr((pMA2_n+".output3Dz"),(tongue_joint[i]+".sz"),f=True)
		
	
	mc.parent("Aim_TongueJoint_G","TongueSetup")
	mc.select(cl=True)


####
def adv_EyeCtrl():
	
	mc.disconnectAttr("EyeAimBlend_L.outputR","Eye_L.rx")
	mc.disconnectAttr("EyeAimBlend_L.outputG","Eye_L.ry")
	mc.disconnectAttr("EyeAimBlend_L.outputB","Eye_L.rz")
	
	mc.disconnectAttr("EyeAimBlend_R.outputR","Eye_R.rx")
	mc.disconnectAttr("EyeAimBlend_R.outputG","Eye_R.ry")
	mc.disconnectAttr("EyeAimBlend_R.outputB","Eye_R.rz")
	
	mc.disconnectAttr("EyeAim_L.rotate","EyeAimBlend_L.color1")
	mc.disconnectAttr("EyeAim_R.rotate","EyeAimBlend_R.color1")
	
	L_R=["L","R"]
	for i in L_R:
		
		ctrl_n="Eyectrl_"+i
		Eye_joint="Eye_"+i
		Eye_B="EyeAimBlend_"+i
		Eye_Aim="EyeAim_"+i
		
		cur_n=mc.curve(d=1,p=((0.10618,0,0),(0.0799858,0.0173783,0),(0.0799858,0.00868914,0),(0.031339,0.00868914,0),(0.031339,-0.00868914,0),(0.0799858,-0.00868914,0),(0.0799858,-0.0173783,0),(0.10618,0,0)),k=(0,1,2,3,4,5,6,7))
		mc.rename(cur_n,ctrl_n)
		ctrl_shape=mc.listRelatives(ctrl_n,s=True)
		mc.setAttr((ctrl_shape[0]+".overrideEnabled"),1)
		mc.setAttr((ctrl_shape[0]+".overrideColor"),17)
		mc.setAttr((ctrl_n+".tx"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((ctrl_n+".ty"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((ctrl_n+".tz"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((ctrl_n+".sx"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((ctrl_n+".sy"),lock=True,keyable=False,channelBox=False)
		mc.setAttr((ctrl_n+".sz"),lock=True,keyable=False,channelBox=False) 
		mc.setAttr((ctrl_n+".v"),lock=True,keyable=False,channelBox=False)
		
		mc.group(n=(ctrl_n+"_C"))
		mc.xform(os=True,piv=(0,0,0))
		mc.group(n=(ctrl_n+"_G"))
		mc.xform(os=True,piv=(0,0,0))
		
		del_par=mc.parentConstraint(Eye_joint,(ctrl_n+"_G"),weight=1)
		mc.delete(del_par)
		
		mD1=Eye_Aim+"_mD"
		mc.shadingNode("multiplyDivide",n=mD1,asUtility=True)
		mc.setAttr((mD1+".input2X"),-1)
		mc.setAttr((mD1+".input2Y"),-1)
		mc.setAttr((mD1+".input2Z"),-1)
		
		mc.connectAttr((Eye_Aim+".rotate"),(mD1+".input1"))
		mc.connectAttr((mD1+".output"),(Eye_B+".color1"))
		
		mD=Eye_B+"_mD"
		mc.shadingNode("multiplyDivide",n=mD,asUtility=True)
		mc.setAttr((mD+".input2X"),-1)
		mc.setAttr((mD+".input2Y"),-1)
		mc.setAttr((mD+".input2Z"),-1)
		
		mc.connectAttr((Eye_B+".outputR"),(mD+".input1X"))
		mc.connectAttr((Eye_B+".outputG"),(mD+".input1Y"))
		mc.connectAttr((Eye_B+".outputB"),(mD+".input1Z"))
		
		mc.connectAttr((mD+".outputX"),(ctrl_n+"_C.rx"))
		mc.connectAttr((mD+".outputY"),(ctrl_n+"_C.ry"))
		mc.connectAttr((mD+".outputZ"),(ctrl_n+"_C.rz"))
		
		pMA=Eye_B+"_pMA"
		mc.shadingNode("plusMinusAverage",n=pMA,asUtility=True)
		mc.connectAttr((mD+".outputX"),(pMA+".input3D[0].input3Dx"))
		mc.connectAttr((mD+".outputY"),(pMA+".input3D[0].input3Dy"))
		mc.connectAttr((mD+".outputZ"),(pMA+".input3D[0].input3Dz"))
		mc.connectAttr((ctrl_n+".rx"),(pMA+".input3D[1].input3Dx"))
		mc.connectAttr((ctrl_n+".ry"),(pMA+".input3D[1].input3Dy"))
		mc.connectAttr((ctrl_n+".rz"),(pMA+".input3D[1].input3Dz"))
		
		mc.connectAttr((pMA+".output3Dx"),(Eye_joint+".rx"))
		mc.connectAttr((pMA+".output3Dy"),(Eye_joint+".ry"))
		mc.connectAttr((pMA+".output3Dz"),(Eye_joint+".rz"))
	
	mc.group(n="EyeCtrl_G",em=True)
	mc.xform(os=True,piv=(0,0,0))
	del_p=mc.parentConstraint("FaceAttachToHead","EyeCtrl_G",weight=1)
	mc.delete(del_p)
	mc.parent("Eyectrl_L_G","EyeCtrl_G")
	mc.parent("Eyectrl_R_G","EyeCtrl_G")
	mc.parent("EyeCtrl_G","EyeSetup")
	mc.parentConstraint("FaceAttachToHead","EyeCtrl_G",weight=1,mo=1)
	mc.select(cl=True)

def advFace_optimize():
	if mc.objExists("FaceGroup"):
		adv_tongueCtrl()
		adv_EyeCtrl()
		return "//////////accomplish FaceSetup"
	else:
		return "////////// No object matches name: FaceSetup"

def face_Scale():
	name=["Aimcontrols","EyeSetup","TongueSetup"]
	for n in name:
		n1=n+"_scaleConstraint1"
		if not mc.objExists(n1):
			mc.scaleConstraint("Character",n,mo=1,weight=1)
def adv_hideVisiblity():
    if mc.objExists('FaceControlSet'):
        FaceControlSet=mc.sets('FaceControlSet',q=1)
        for i in FaceControlSet:
            visStatus=mc.attributeQuery('visibility',n=i,h=1)
            if not visStatus:
                mc.setAttr(i+'.visibility',lock=True,keyable=False,channelBox=False)