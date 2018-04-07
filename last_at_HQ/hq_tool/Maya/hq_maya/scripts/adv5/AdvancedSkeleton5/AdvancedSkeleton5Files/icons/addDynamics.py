import maya.cmds as mc
import maya.mel as mm
def addDynamics():
	selections=mc.ls(sl=1)
	if mc.objExists('HairBakeSet')==0:
	    mc.sets(n='HairBakeSet',em=1)
	if mc.objExists('HairFollicleSet')==0:
	    mc.sets(n='HairFollicleSet',em=1)
	lenSel=len(selections)
	positions=[]
	Joints=[]                     
	ConstraintWeightS=[]
	for i in selections:
	    mc.sets(i,add='HairBakeSet')
	    pos=mc.xform(i,q=1,ws=1,rp=1)
	    positions.append(pos)
	mc.select('Master',r=1)
	#-----HairJoints------
	for i in range(0,lenSel):
	    Joint=mc.joint(p=positions[i])
	    Joints.append(Joint)
	    Constraint=mc.parentConstraint(Joint,selections[i],mo=1)[0]
	    ConstraintWeightS.append(Constraint+'.'+Joint+'W0')
	mc.hide(Joints)
	#-----HairCurve------    
	Curve=mc.curve(d=3,ep=positions)
	#-----HairCurve------
	mm.eval('makeCurvesDynamicHairs 1 0 1')
	 
	follicle=mc.listRelatives(Curve,p=1)[0]
	mc.sets(follicle,add='HairFollicleSet')
	follicleShape=mc.listRelatives(follicle,s=1)[0]
	mc.setAttr(follicleShape+'.pointLock',0)
	mc.setAttr(follicleShape+'.stiffness',1)
	mc.setAttr(follicleShape+'.startCurveAttract',1)
	hairSystem=mc.listConnections(follicleShape,t='hairSystem')[0];mc.hide(hairSystem)
	hairSystemShape=mc.listRelatives(hairSystem,s=1)[0]
	mc.setAttr(hairSystemShape+'.startCurveAttract',1)
	mainParent=mc.listRelatives(selections[0],p=1)[0]
	folliclesGRP=mc.listRelatives(follicle,p=1)[0];mc.hide(folliclesGRP)
	mc.parent(folliclesGRP,mainParent)
	mc.parent(Joints[0],folliclesGRP)
	outputCurve=mc.listConnections(follicleShape,t='nurbsCurve',s=0)[0];mc.hide(outputCurve)
	SplineIkHadle=mc.ikHandle(sol='ikSplineSolver',ccv=0,pcv=0,sj=Joints[0],ee=Joints[-1],c=outputCurve);mc.hide(SplineIkHadle)
	if mm.eval('attributeExists "HairStart" "Master"')==0:
	    mc.addAttr('Master',ln="HairStart",at="enum",en="=======:",k=1)
	    mc.setAttr("Master.HairStart",lock=1)
	if mm.eval('attributeExists "HairSimulation" "Master"')==0:
	    mc.addAttr('Master',ln="HairSimulation",at="enum",en="Off:On:",k=1)
	if mm.eval('attributeExists "Stiffness" "Master"')==0:
	    mc.addAttr('Master',ln="Stiffness",at="double",min=0,max=1,dv=0.15,k=1)
	if mm.eval('attributeExists "BaseAttract" "Master"')==0:
	    mc.addAttr('Master',ln="BaseAttract",at="double",min=0,max=1,dv=1,k=1)
	if mm.eval('attributeExists "TipAttract" "Master"')==0:
	    mc.addAttr('Master',ln="TipAttract",at="double",min=0,max=1,dv=0.05,k=1)    
	if mm.eval('attributeExists "HairStartFrame" "Master"')==0:
	    mc.addAttr('Master',ln="HairStartFrame",at="long",dv=1,k=1) 
	if mm.eval('attributeExists "Gravity" "Master"')==0:
	    mc.addAttr('Master',ln="Gravity",at="double",dv=0,k=1)
	if mm.eval('attributeExists "Drag" "Master"')==0:
	    mc.addAttr('Master',ln="Drag",at="double",min=0,dv=0.05,k=1)
	if mm.eval('attributeExists "Damp" "Master"')==0:
	    mc.addAttr('Master',ln="Damp",at="double",min=0,dv=0,k=1)  
	if mm.eval('attributeExists "Mass" "Master"')==0:
	    mc.addAttr('Master',ln="Mass",at="double",min=0,dv=1,k=1)      
	if mm.eval('attributeExists "DynamicsWeight" "Master"')==0:
	    mc.addAttr('Master',ln="DynamicsWeight",at="double",min=0,max=1,dv=1,k=1)    
	if mm.eval('attributeExists "HairEnd" "Master"')==0:
	    mc.addAttr('Master',ln="HairEnd",at="enum",en="=======:",k=1)
	    mc.setAttr("Master.HairEnd",lock=1)   
	mc.setDrivenKeyframe(hairSystem+'.simulationMethod',cd='Master.HairSimulation',v=1,dv=0)
	mc.setDrivenKeyframe(hairSystem+'.simulationMethod',cd='Master.HairSimulation',v=2,dv=1)
	for i in ConstraintWeightS:
	    mc.connectAttr('Master.HairSimulation',i,f=1)
	mc.connectAttr('Master.Stiffness',hairSystemShape+'.stiffness',f=1)
	mc.connectAttr('Master.BaseAttract',hairSystemShape+'.attractionScale[0].attractionScale_FloatValue',f=1)
	mc.connectAttr('Master.TipAttract',hairSystemShape+'.attractionScale[1].attractionScale_FloatValue',f=1)
	mc.connectAttr('Master.HairStartFrame',hairSystemShape+'.startFrame',f=1)
	mc.connectAttr('Master.Gravity',hairSystemShape+'.gravity',f=1)
	mc.connectAttr('Master.Drag',hairSystemShape+'.drag',f=1)
	mc.connectAttr('Master.Damp',hairSystemShape+'.damp',f=1)
	mc.connectAttr('Master.Mass',hairSystemShape+'.mass',f=1)
	mc.connectAttr('Master.DynamicsWeight',hairSystemShape+'.dynamicsWeight',f=1)
	FX_Grp=mc.group(em=1,n=hairSystem+'_FX')
	mc.parent(hairSystem,FX_Grp)
	mc.parent(SplineIkHadle[0],FX_Grp)
	mc.parent(hairSystem+'OutputCurves',FX_Grp)