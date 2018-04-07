#!/usr/bin/python
# -*- coding : utf-8 -*-
# -*- coding : GB2312 -*-
#--author-- : yujing
#--date-- : 2017.6.13
import maya.cmds as cmds
#######---- "Rig" ---- #############        
def check_listJoint_ExGroup():
    jointAdj =[]
    jointall = None
    if cmds.objExists("adv_Hips"):
        jointChild = cmds.listRelatives("adv_Hips",ad=1)
        gro = [o for o in jointChild if  cmds.nodeType(o)=="transform"]
        if gro !=[]:
            jointAdj+= gro  
    else:
        jointAdj.append(0)
    return jointAdj