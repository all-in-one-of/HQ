import maya.cmds as mc
def growAnim():
	maxBegin=0
	minBegin=10000
	objs=mc.ls(sl=1)
	Master='Master'
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
	    #Grow
	    setRangeNode=mc.createNode("setRange")
	    mc.setAttr(setRangeNode+'.maxX',1)
	    plusNode=mc.createNode("plusMinusAverage")
	    rampNode=mc.createNode("ramp")
	    mc.setAttr(rampNode+'.interpolation',4)
	    mc.setAttr(rampNode+'.colorEntryList[0].color',0,0,0)
	    mc.setAttr(rampNode+'.colorEntryList[1].color',1,1,1)
	    mc.setAttr(rampNode+'.colorEntryList[1].position',1)
	    mc.connectAttr('growGrp.grow',setRangeNode+'.valueX',f=1)
	    mc.connectAttr(one+'.growBegin',setRangeNode+'.oldMinX',f=1)
	    mc.connectAttr(one+'.growBegin',plusNode+'.input1D[0]',f=1)
	    mc.connectAttr(one+'.growRange',plusNode+'.input1D[1]',f=1)
	    mc.connectAttr(plusNode+'.output1D',setRangeNode+'.oldMaxX',f=1)
	    mc.connectAttr(setRangeNode+'.outValueX',rampNode+'.vCoord',f=1)
	    mc.connectAttr(rampNode+'.outColorR',one+'.grow',f=1)
	    #Wave
	    rampNode1=mc.createNode("ramp")
	    mc.setAttr(rampNode1+'.colorEntryList[0].color',0,0,0)
	    mc.setAttr(rampNode1+'.colorEntryList[1].color',1,1,1)
	    mc.setAttr(rampNode1+'.colorEntryList[2].color',0,0,0)
	    mc.setAttr(rampNode1+'.colorEntryList[1].position',0.5)
	    mc.setAttr(rampNode1+'.colorEntryList[2].position',1)
	    mc.setAttr(rampNode1+'.interpolation',4)
	    setRangeNode1=mc.createNode("setRange")
	    mc.setAttr(setRangeNode1+'.maxX',1)
	    multiplyNode1=mc.createNode("multiplyDivide")
	    mc.connectAttr('growGrp.grow',multiplyNode1+'.input1X',f=1)
	    mc.setAttr(multiplyNode1+'.input2X',-1)
	    
	    
	    
	    
	    multiplyNode3=mc.createNode("multiplyDivide")
	    mc.connectAttr(multiplyNode1+'.outputX',multiplyNode3+'.input1X',f=1)
	    mc.connectAttr('growGrp.speed',multiplyNode3+'.input2X',f=1)
	    
	    plusNode1=mc.createNode("plusMinusAverage")
	    mc.connectAttr(multiplyNode3+'.outputX',plusNode1+'.input1D[0]',f=1)
	    mc.connectAttr(one+'.growBegin',plusNode1+'.input1D[1]',f=1)
	    mc.connectAttr('growGrp.offset',plusNode1+'.input1D[2]',f=1)
	    
	    
	    
	    multiplyNode2=mc.createNode("multiplyDivide")
	    mc.connectAttr(plusNode1+'.output1D',multiplyNode2+'.input1X',f=1)
	    mc.connectAttr('growGrp.wavelength',multiplyNode2+'.input2X',f=1)
	    mc.connectAttr(multiplyNode2+'.outputX',setRangeNode1+'.valueX',f=1)
	    mc.connectAttr(setRangeNode1+'.outValueX',rampNode1+'.vCoord',f=1)
	    plusNode2=mc.createNode("plusMinusAverage")
	    mc.setAttr(plusNode2+'.operation',2)
	    mc.connectAttr(rampNode1+'.outColorR',plusNode2+'.input1D[0]',f=1)
	    mc.setAttr(plusNode2+'.input1D[1]',0.5)
	    multiplyNode3=mc.createNode("multiplyDivide")
	    mc.connectAttr(plusNode2+'.output1D',multiplyNode3+'.input1X',f=1)
	    mc.connectAttr('growGrp.amplitude',multiplyNode3+'.input2X',f=1)
	    
	    multiplyNode4=mc.createNode("multiplyDivide")
	    mc.connectAttr(multiplyNode3+'.outputX',multiplyNode4+'.input1X',f=1)
	    mc.connectAttr('growGrp.wave',multiplyNode4+'.input2X',f=1)
	    
	    mc.connectAttr(multiplyNode4+'.outputX',parentGrp+'.rz',f=1)
	waveLengh=6.2831853/(mc.getAttr(Master+'.grow')*mc.getAttr(Master+'.speed')+mc.getAttr(one+'.growBegin')+mc.getAttr(Master+'.offset'))*0.1
	mc.setAttr(Master+'.wavelength',waveLengh)