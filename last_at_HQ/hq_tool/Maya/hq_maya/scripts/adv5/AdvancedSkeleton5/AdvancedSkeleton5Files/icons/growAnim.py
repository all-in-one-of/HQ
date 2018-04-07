#coding:utf-8
import maya.cmds as mc
def growAnim():
	if not mc.pluginInfo('growNode',q=1,l=1):
		mc.loadPlugin('O:/hq_tool/Maya/hq_maya/scripts/adv5/adv5/mll/maya2015/growNode.mll')
	maxBegin=0
	minBegin=10000
	objs=mc.ls(sl=1)
	Master='Master'
	masterAttrs=mc.listAttr(Master,k=1)
	if not 'grow' in masterAttrs:
		mc.addAttr(Master,ln="grow",k=1,at='double',min=0,dv=0)
		
		mc.addAttr(Master,ln="WaveAnim",at="enum",en="=======:",k=1)
		mc.setAttr(Master+'.WaveAnim',lock=1)
		
		mc.addAttr(Master,ln="wave",k=1,at="enum",en="Off:On:")
		mc.setAttr(Master+'.wave',1)
		mc.addAttr(Master,ln="amplitude",k=1,at='double',min=0,dv=1)
		mc.addAttr(Master,ln="speed",k=1,at='double',dv=1)
		mc.addAttr(Master,ln="wavelength",k=1,at='double',min=0,dv=0.01)
		mc.addAttr(Master,ln="offset",k=1,at='double',dv=0)
	if not mc.objExists('growGrp'):
		growGrp=mc.group(em=1,n='growGrp')
		mc.parent(growGrp,Master)
		mc.addAttr(growGrp,ln="grow",k=1,at='double',min=0,dv=0)
		
		mc.addAttr(growGrp,ln="WaveAnim",at="enum",en="=======:",k=1)
		mc.setAttr(growGrp+'.WaveAnim',lock=1)
		
		mc.addAttr(growGrp,ln="wave",k=1,at="enum",en="Off:On:")
		mc.setAttr(growGrp+'.wave',1)
		mc.addAttr(growGrp,ln="amplitude",k=1,at='double',min=0,dv=1)
		mc.addAttr(growGrp,ln="speed",k=1,at='double',dv=1)
		mc.addAttr(growGrp,ln="wavelength",k=1,at='double',min=0,dv=0.01)
		mc.addAttr(growGrp,ln="offset",k=1,at='double',dv=0)
		mc.connectAttr('Master.grow','growGrp.grow')
		mc.connectAttr('Master.wave','growGrp.wave')
		mc.connectAttr('Master.amplitude','growGrp.amplitude')
		mc.connectAttr('Master.speed','growGrp.speed')
		mc.connectAttr('Master.wavelength','growGrp.wavelength')
		mc.connectAttr('Master.offset','growGrp.offset')
		mc.hide(growGrp)
	else:
		growGrp='growGrp'
	for one in objs:
	    parentGrp=mc.listRelatives(one,p=1)[0]
	    path=mc.ls(one,l=1)[0]
	    parentNum=len(path.split('|'))
	    if(parentNum>maxBegin):
	    	maxBegin=parentNum
	    if(parentNum<minBegin):
	    	minBegin=parentNum
	    mc.addAttr(one,ln="growBegin",k=1,at='double',min=0,dv=parentNum)
	    mc.addAttr(one,ln="growRange",k=1,at='double',min=0,dv=5)
	    mc.addAttr(one,ln="grow",at='double',dv=1)
	    mc.connectAttr(one+'.grow',parentGrp+'.sx',f=1)
	    mc.connectAttr(one+'.grow',parentGrp+'.sy',f=1)
	    mc.connectAttr(one+'.grow',parentGrp+'.sz',f=1)
	    growNode=mc.createNode('growNode')
	    mc.connectAttr(growGrp+'.grow',growNode+'.input')
	    mc.connectAttr(growGrp+'.wave',growNode+'.envelope')
	    mc.connectAttr(growGrp+'.amplitude',growNode+'.amplitude')
	    mc.connectAttr(growGrp+'.speed',growNode+'.speed')
	    mc.connectAttr(growGrp+'.wavelength',growNode+'.wavelength')
	    mc.connectAttr(growGrp+'.offset',growNode+'.offset')
	    mc.connectAttr(one+'.growBegin',growNode+'.growBegin')
	    mc.connectAttr(one+'.growRange',growNode+'.growRange')
	    
	    mc.connectAttr(growNode+'.outSine',parentGrp+'.rz')
	    mc.connectAttr(growNode+'.outSmoothstep',one+'.grow')

	waveLengh=(mc.getAttr(Master+'.grow')*mc.getAttr(Master+'.speed')+maxBegin-minBegin+mc.getAttr(Master+'.offset'))/6.2831853
	mc.setAttr(Master+'.wavelength',waveLengh)