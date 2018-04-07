#coding=cp936
#coding=utf-8
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
def checkVer(arg):
    sel = cmds.ls(type = "aiUtility")
    selTarget = []
    selSource = []
    if len(sel)!= 0:
        for i in range(0,len(sel)):
            seladjust =cmds.listConnections(sel[i]+".color",d=0,type="aiWriteColor") 
            if seladjust != None:
                selTarget.append(sel[i])
    for i in range(0,len(selTarget)):
        AiWC = cmds.listConnections( selTarget[i]+".color", s=True )
        for i in range(0,len(AiWC)):
            selTSource = cmds.listConnections( AiWC[i]+".input", s=True )
            selSource.append(selTSource[i])
    for t in range(0,len(selTarget)):
        selTSColor = pm.getAttr(selSource[t]+".color")
        pm.setAttr(selTarget[t]+".hardwareColor",selTSColor)
        
        
def recdisplay(arg):
	aucsel = cmds.ls(type="aiUtility")
	for i in range(0,len(aucsel)):
		aucHcolorn= aucsel[i]+".hardwareColor"
		aucHcolor = pm.getAttr(aucHcolorn)
		if aucHcolor !=(1,1,1):
			cmds.setAttr(aucHcolorn,0.5,0.5,0.5)

def feetctrl(arg):
	value=pm.textField('cmm',q=True,tx=True)
	ctrsel = ["Ankle_L","ToesEnd_L","Ankle_R","ToesEnd_R"]
	fmsel = []
	fmseladjust = ["footmask_LB","footmask_LF","footmask_RB","footmask_RF"]
	LBcube = pm.polyCube(n="footmask_LB",w=0.13,h=0.03,d=0.2)
	pm.move(0.095,-0.015,0.013)
	fmsel.append(LBcube)
	LFcube = pm.polyCube(n="footmask_LF",w=0.13,h=0.03,d=0.08)
	pm.move(0.095,-0.015,0.143)
	fmsel.append(LFcube)
	RBcube = pm.polyCube(n="footmask_RB",w=0.13,h=0.03,d=0.2)
	pm.move(-0.095,-0.015,0.013)
	fmsel.append(RBcube)
	RFcube = pm.polyCube(n="footmask_RF",w=0.13,h=0.03,d=0.08)
	pm.move(-0.095,-0.015,0.143)
	fmsel.append(RFcube)
	
	fmselNew = [i for i in fmseladjust if i not in fmsel]
	AiUNode = pm.shadingNode("aiUtility",asShader=True)
	SGNode = pm.createNode("shadingEngine")
	pm.setAttr(AiUNode+".hardwareColor",0,1,1)
	pm.setAttr(AiUNode+".shadeMode",2)
	for i in range(0,len(fmselNew)):
	    shapeNode = pm.listRelatives(fmselNew[i],s=True,f=True)
	    pm.defaultNavigation(source=AiUNode,destination =shapeNode[0]+".instObjGroups[0]" ,connectToExisting=True)
	    pm.setAttr(shapeNode[0]+".castsShadows",0)
	    pm.setAttr(shapeNode[0]+".receiveShadows",0)
	    pm.setAttr(shapeNode[0]+".motionBlur",0)
	    pm.setAttr(shapeNode[0]+".primaryVisibility",0)
	    pm.setAttr(shapeNode[0]+".smoothShading",0)
	    pm.setAttr(shapeNode[0]+".visibleInReflections",0)
	    pm.setAttr(shapeNode[0]+".visibleInRefractions",0)
	    pm.setAttr(shapeNode[0]+".doubleSided",0)
	    pm.setAttr(shapeNode[0]+".aiSelfShadows",0)
	    pm.setAttr(shapeNode[0]+".aiOpaque",0)
	    pm.setAttr(shapeNode[0]+".aiVisibleInDiffuse",0)
	    pm.setAttr(shapeNode[0]+".aiVisibleInGlossy",0)
	for i in range(0,len(fmselNew)):
		pm.makeIdentity(fmselNew[i],apply=True,t=1,r=1,s=1,n=0)
	pm.select(fmselNew,r=1)	
	mel.eval('DeleteHistory')
	pm.group(fmselNew,name=value+'_feetMask_g')
	pm.rename(AiUNode,value)
	for i in range(0,len(ctrsel)):
	        if pm.objExists(ctrsel[i]):
	            pm.select(ctrsel[i])
	            pm.parentConstraint(ctrsel[i],fmselNew[i],mo=True,weight = 1)
	            pm.scaleConstraint(ctrsel[i],fmselNew[i],mo=True,weight = 1)
	            pm.setAttr(fmselNew[i] + '.primaryVisibility',0)
	            pm.setAttr(fmselNew[i] + '.castsShadows',0)
	            pm.setAttr(fmselNew[i] + '.receiveShadows',0)
	            pm.rename(fmselNew[i],value +"_" + fmselNew[i])  
def Opcom(arg):
    selAs = cmds.ls(type='aiStandard')
    editedm=cmds.ls(typ=('aiUtility','aiStandard','aiWriteColor','file','place2dTexture','displacementShader','bump2d','shadingEngine','ramp','blendColors','condition','gammaCorrect','luminance','samplerInfo','surfaceLuminance','aiSkin','aiHair'))
    
    for i in range(0,len(selAs)):
        AsOp=cmds.listConnections(selAs[i] + '.opacity',plugs=True,d=0)
        AsOpfile = cmds.listConnections(selAs[i] + '.opacity',d=0)
        AsOpjust=cmds.connectionInfo(selAs[i] + '.opacity',id=True)
        AsOptO = selAs[i] + '.opacity'
        AsOpt = cmds.getAttr(AsOptO)
        if AsOpt != [(1.0,1.0,1.0)]:
            AsOptOname = AsOptO[0:len(AsOptO)-len(".opacity")]#去除opacity属性后缀
            AsOptAi2WT = cmds.listConnections(AsOptOname,s=0,type='aiWriteColor')
            AsTrueOPAU = cmds.listConnections(AsOptAi2WT,d=0,type='aiUtility')
            AsOptSG2WT2 = cmds.listConnections(AsOptAi2WT,s=0,type='aiUtility')
            AsOptSG = cmds.listConnections(AsOptSG2WT2,s=0,type='shadingEngine')
            AsOptSGs = cmds.listConnections(AsOptSG,d=0)
            AsTrueshapes = [b for b in AsOptSGs if b not in editedm]
            AsTrueshapesS = cmds.listRelatives(AsTrueshapes)
            for b in range(0,len(AsTrueshapesS)):
                cmds.setAttr(AsTrueshapesS[b] + ".aiOpaque",0)
            if AsOpjust == True:
                for c in range(0,len(AsOpfile)):
                    cmds.connectAttr(AsOpfile[c] + '.outAlpha',AsTrueOPAU[c] + '.opacity',f=True)
                    cmds.setAttr(AsOpfile[c]+'.alphaIsLuminance',1)
                    cmds.setAttr(AsOptAi2WT[c] +'.blend',1)

def Opclear(arg):
    sel = cmds.ls(sl=True)
    selshape = cmds.listRelatives(sel,shapes=True)
    for i in range(0,len(selshape)):
        cmds.setAttr(selshape[i]+".aiOpaque",0)
def rigcleantool(arg):
    if cmds.pluginInfo("Fur",q=1,loaded=1,name=1)==0:
        cmds.loadPlugin("Fur")
    if cmds.pluginInfo("Mayatomr",q=1,loaded=1,name=1)==0:
        cmds.loadPlugin("Mayatomr")
    if cmds.pluginInfo("mtoa",q=1,loaded=1,name=1)==0:
        cmds.loadPlugin("mtoa")
    delsel =[]
    aiAov = cmds.ls(type="aiAOV")
    aiAovnum=[]
    for a in range(len(aiAov)):
        aovadj = cmds.listConnections(aiAov[a]+".message",s=0,type="aiOptions")
        if aovadj ==None:
           delsel.append(aiAov[a]) 
           
    camv = cmds.ls(type="cameraView")
    for c in range(len(camv)):  
        delsel.append(camv[c])
        
    jointlayer = cmds.ls(type="displayLayer")
    jointlayernum = []
    for j in range(len(jointlayer)):
        adj =  cmds.listConnections( jointlayer[j], d=True)
        if adj ==None:
            delsel.append(jointlayer[j])
     
    mrOptions = cmds.ls(type="mentalrayOptions")
    for m in range(len(mrOptions)):
        delsel.append(mrOptions[m])
    
    swfursel =cmds.ls(type="FurGlobals")
    for s in range(len(swfursel)):
        delsel.append(swfursel[s])
            
    animcurve = cmds.ls(type="animCurveUL")
    delancv = []
    for a in range(len(animcurve)):
        unitconup = cmds.listConnections(animcurve[a],s=0)
        unitcondn = cmds.listConnections(animcurve[a],d=0)
        if unitconup==None and unitcondn==None:
            delancv.append(animcurve[a])
            delsel.append(animcurve[a])
            
    hpginfo = cmds.ls(type="hyperGraphInfo")
    delhpginfo = []
    for h in range(len(hpginfo)):
        if hpginfo[h]!="hyperGraphInfo":
            delhpginfo.append(hpginfo[h]) 
            delsel.append(hpginfo[h])
    
    hpview = cmds.ls(type="hyperView")
    delhpview = []
    for p in range(len(hpview)):
        delsel.append(hpview[p])
        delhpview.append(hpview[p])
    
    hplayout = cmds.ls(type="hyperLayout")
    delhplayout = []
    for h in range(len(hplayout)):
        delhplayout.append(hplayout[h]) 
        delsel.append(hplayout[h])
            
    groupid = cmds.ls(type="groupId")
    delgroupid = []
    for i in range(len(groupid)):
        unitcon = cmds.listConnections(groupid[i],s=0)
        if unitcon==None:
            delgroupid.append(groupid[i]) 
            delsel.append(groupid[i]) 
    
    unit = cmds.ls(type="unitConversion")
    delunit = []
    for i in range(len(unit)):
        unitcon = cmds.listConnections(unit[i],s=0)
        if unitcon==None:
            delunit.append(unit[i]) 
            delsel.append(unit[i])  
              
    for d in range(len(delsel)):
        cmds.delete(delsel[d])
        print ".............\n",
    
    
    print "已删除"+str(len(delunit))+"个无用的unitConversion节点，"+str(len(delancv))+"个无用的animCurveUL节点，"+str(len(delhpginfo))+"个无用的hyperGraphInfo节点，"+str(len(delhpview))+"个无用的hyperView节点，"+str(len(delhplayout))+"个无用的hyperLayout节点，"+str(len(delgroupid))+"个无用的groupId节点，"+str(len(camv))+"个无用的cameraView节点，"+str(len(jointlayernum))+"个无用的displayLayer节点，"+str(len(mrOptions))+"个无用的mentalrayOptions节点，"+str(len(aiAovnum))+"个无用的aiAov节点，"+str(len(swfursel))+"个无用的FurGlobals节点!!", 

def hwcolorsel(arg):
	vail=["file","ramp"]
	chsel = pm.ls(type="choice")
	if chsel !=[]:
		if len(chsel)!=1:
			mainchsel = [i for i in chsel if pm.listConnections(i,s=0,type="choice")!=[]]
			filesel =  [a for a in pm.listConnections(mainchsel[0],s=0) if pm.nodeType(a) in vail]
			pm.select(filesel,r=1)
			print "已选择显示颜色参考节点！！",
		else:
			filesel =  [a for a in pm.listConnections(chsel[0],s=0) if pm.nodeType(a) in vail]
			pm.select(filesel,r=1)
			print "已选择显示颜色参考节点！！",		
	else:
		print "没有choice节点！！",

def HDD():
    if cmds.window('HDDisplayColor',ex=True):
        cmds.deleteUI('HDDisplayColor',wnd=True)
    cmds.window('HDDisplayColor',t='SJ_riggingTool')
    cmds.columnLayout(adj=True)
    cmds.text(l="专供设置_穿插检查版工具V2.1",h=50,ann="2.1更新说明：增加ID与贴图切换显示")
    cmds.button(l='检查穿插版一键生成',c=checkVer,h=50)
    cmds.button(l='模型颜色显示着色器',c= "fb.mod.SJ_hardwareColorchangerwdUI()",h=50)
    cmds.button(l='恢复默认显示材质',c=recdisplay,h=50)
    cmds.button(l='智能选中衣服颜色参考节点',c=hwcolorsel,h=50)
    cmds.button(l='显示贴图ID切换',c="fb.rig.SJ_rigging.SJ_displaySwitcher()",h=50)
    cmds.button(l='清理文件',c=rigcleantool,h=50)
    cmds.text(l="将以文本框名字重命名所生成模型和节点",h=50)
    cmds.textField('cmm',tx="AovsName",h=30)
    cmds.button(l='添加脚底方块',c=feetctrl,h=50)
    cmds.showWindow()
#def SJ_RiggingTool():
if __name__=='__main__':
    HDD()