import maya.cmds as mc
import maya.mel as mm
def backToDynamics():
	selections=mc.ls(sl=1)
	for i in selections:
	    constraint=i+'_parentConstraint1'
	    mc.connectAttr(constraint+'.constraintTranslateX',i+'.tx',f=1)
	    mc.connectAttr(constraint+'.constraintTranslateY',i+'.ty',f=1)
	    mc.connectAttr(constraint+'.constraintTranslateZ',i+'.tz',f=1)
	    mc.connectAttr(constraint+'.constraintRotateX',i+'.rx',f=1)
	    mc.connectAttr(constraint+'.constraintRotateY',i+'.ry',f=1)
	    mc.connectAttr(constraint+'.constraintRotateZ',i+'.rz',f=1)