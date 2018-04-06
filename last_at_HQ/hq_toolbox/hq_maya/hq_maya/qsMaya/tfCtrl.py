# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds


def wrapTFNode(objectList, shellPoly,tfGrp=None):
    '''{'del_path':'TfCtrl/Add/wrapTFNode(objectList, shellPoly)ONLYSE',
'usage':'\
objectList = cmds.ls(sl=True,l=True)[:-2]\\n\
shellPoly = cmds.ls(sl=True,l=True)[-2]\\n\
tfGrp = cmds.ls(sl=True,l=True)[-1]\\n\
$fun(objectList, shellPoly,tfGrp)\\n\\n\
objectList = cmds.ls(sl=True,l=True)[:-1]\\n\
shellPoly = cmds.ls(sl=True,l=True)[-1]\\n\
$fun(objectList, shellPoly)',
}
'''
    
    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]    
    
    #Delete attributes
    delAttr(objectList, ['pBNode','follicleNodeState','atU', 'atV', 'pBNode1', 'pBWeight', 'pBInT2', 'pBInR2'])
    
    #load plugin   
    if cmds.pluginInfo("nearestPointOnMesh",query=True,l=True)==False:
        cmds.loadPlugin("nearestPointOnMesh")
    #print 'Loaded plugin'
    
    cmds.lockNode(shellPoly, l=False)
    
    #get shellPolyShape
    meshList = cmds.listRelatives(shellPoly,type='mesh')
    for mesh in meshList:
        if cmds.getAttr(mesh+'.intermediateObject') == 0:
            shellPolyShape = mesh
    #print 'Get shellPolyShape'
    
    #create and set foGrp
    if cmds.objExists( '%s_foGrp'%(shellPoly) ) == False:
        cmds.group(em=True, n='%s_foGrp'%(shellPoly) ) 
    foGrp = '%s_foGrp'%(shellPoly)
    #cmds.setAttr(foGrp+'.intermediateObject',1)
    
    if cmds.attributeQuery('foGrp', n=shellPoly, exists=True) == False:
        cmds.addAttr(shellPoly,ln="foGrp", dt="string")
    cmds.setAttr('%s.foGrp'%(shellPoly), l=False)
    cmds.setAttr('%s.foGrp'%(shellPoly), foGrp, type='string', l=True)
      
    cmds.lockNode(foGrp, l=False)
    
    
    if tfGrp != None:
        attrExists = cmds.attributeQuery('shellPoly', n=tfGrp, exists=True)  and  cmds.attributeQuery('foGrp', n=tfGrp, exists=True)
        
        sameShellPoly = True
        if cmds.attributeQuery('shellPoly', n=tfGrp, exists=True):
            sameShellPoly = (cmds.getAttr('%s.shellPoly'%(tfGrp)) == shellPoly)
            
        cmds.lockNode(tfGrp, l=False)
        if attrExists == False  or  sameShellPoly == False:   
            tfGrp = cmds.group(em=True, n='%s_tfGrp'%(shellPoly) )
            cmds.addAttr(tfGrp,ln="shellPoly", dt="string")        
            cmds.addAttr(tfGrp,ln="foGrp", dt="string")
    
    else:
        tfGrp = cmds.group(em=True, n='%s_tfGrp'%(shellPoly) )
        cmds.addAttr(tfGrp,ln="shellPoly", dt="string")
        cmds.addAttr(tfGrp,ln="foGrp", dt="string")
        
    
    cmds.setAttr('%s.shellPoly'%(tfGrp), l=False)
    cmds.setAttr('%s.foGrp'%(tfGrp), l=False)
    cmds.setAttr('%s.shellPoly'%(tfGrp), shellPoly, type='string', l=True)
    cmds.setAttr('%s.foGrp'%(tfGrp), foGrp, type='string', l=True)
    #print '%s   %s   %s'%(shellPoly, tfGrp, foGrp)
    
    intfGrp = cmds.listRelatives(tfGrp, type='transform', f=True)
    if intfGrp != None:
        foRemove = []
        for tfNode in objectList:
            if tfNode in intfGrp:
                foRemove.append(tfNode)
        for tfNode in foRemove:
            objectList.remove(tfNode) 


    #create nearestPointOnMesh node add connection to shellPolyShape       
    uvNode = cmds.createNode("nearestPointOnMesh", n="setUV")
    cmds.connectAttr(shellPolyShape+'.worldMesh[0]', uvNode+'.inMesh',f=True)
    
    for tfNode in objectList:
        tfNodeCenter=cmds.objectCenter(tfNode)
        cmds.setAttr(uvNode+'.inPosition', tfNodeCenter[0], tfNodeCenter[1], tfNodeCenter[2], type="double3")
        pairBlendNode = cmds.createNode('pairBlend')
        
        u = cmds.getAttr(uvNode+'.parameterU')
        v = cmds.getAttr(uvNode+'.parameterV')
            
        #create follicle and set attribute     
        folShape = cmds.createNode("follicle")
                        
        
        folTransform = cmds.listRelatives(folShape, p=True,f=True)[0]
               
        cmds.setAttr(folShape + '.parameterU', u, l=True)
        cmds.setAttr(folShape + '.parameterV', v, l=True)
        cmds.setAttr(folShape + ".simulationMethod", 0)
        cmds.setAttr(folShape + ".collide", 0)
        cmds.setAttr(folShape + ".degree", 1)
        cmds.setAttr(folShape + ".sampleDensity", 0)        
        
            
        #connection follicles
        cmds.connectAttr(shellPolyShape+'.worldMatrix[0]', folShape + '.inputWorldMatrix', f=True)
        cmds.connectAttr(shellPolyShape+'.outMesh', folShape + '.inputMesh', f=True) 
        cmds.connectAttr(folShape + '.outRotate', folTransform+'.rotate', f=True)
        cmds.connectAttr(folShape + '.outTranslate', folTransform+'.translate', f=True)
        
       
        
        parentConNode =  cmds.parentConstraint( folTransform, tfNode, mo=True )[0]
                
        #connection pairBlendNode
        cmds.connectAttr(parentConNode+'.constraintTranslate', pairBlendNode+'.inTranslate1', f=True)
        cmds.connectAttr(parentConNode+'.constraintRotate', pairBlendNode+'.inRotate1', f=True)
        
        cmds.disconnectAttr(parentConNode+'.constraintTranslateX', tfNode+'.translateX')
        cmds.disconnectAttr(parentConNode+'.constraintTranslateY', tfNode+'.translateY')
        cmds.disconnectAttr(parentConNode+'.constraintTranslateZ', tfNode+'.translateZ')
        cmds.disconnectAttr(parentConNode+'.constraintRotateX', tfNode+'.rotateX')
        cmds.disconnectAttr(parentConNode+'.constraintRotateY', tfNode+'.rotateY')
        cmds.disconnectAttr(parentConNode+'.constraintRotateZ', tfNode+'.rotateZ')
        
        cmds.connectAttr(pairBlendNode+'.outTranslate', tfNode+'.translate', f=True)
        cmds.connectAttr(pairBlendNode+'.outRotate', tfNode+'.rotate', f=True)
      
          
       
        cmds.addAttr(tfNode, ln="follicleNodeState",  at="enum", en="Normal:PassThrough:Blocking")
        cmds.connectAttr(tfNode+'.follicleNodeState', folShape+'.nodeState')
        cmds.addAttr(tfNode, ln='atU', at='double', dv=u)
        cmds.addAttr(tfNode, ln='atV', at='double', dv=v)
        cmds.setAttr(tfNode+'.atU', l=True)
        cmds.setAttr(tfNode+'.atV', l=True)
        
        
        cmds.addAttr(tfNode, ln='pBNode1', dt='string')
        cmds.setAttr(tfNode+'.pBNode1', pairBlendNode, type='string', l=True)
        cmds.addAttr(tfNode, ln='pBWeight', at='double', min=0, max=1, dv=0)
        cmds.connectAttr(tfNode+'.pBWeight', pairBlendNode+'.weight')    
        cmds.addAttr(tfNode, ln='pBInT2',   at='double3')
        cmds.addAttr(tfNode, ln='pBInT2X',  p='pBInT2', at='doubleLinear')
        cmds.addAttr(tfNode, ln='pBInT2Y',  p='pBInT2', at='doubleLinear')
        cmds.addAttr(tfNode, ln='pBInT2Z',  p='pBInT2', at='doubleLinear')
        cmds.connectAttr(tfNode+'.pBInT2', pairBlendNode+'.inTranslate2')        
        cmds.addAttr(tfNode, ln='pBInR2', at='double3')
        cmds.addAttr(tfNode, ln='pBInR2X',  p='pBInR2', at='doubleAngle')
        cmds.addAttr(tfNode, ln='pBInR2Y',  p='pBInR2', at='doubleAngle')
        cmds.addAttr(tfNode, ln='pBInR2Z',  p='pBInR2', at='doubleAngle')
        cmds.connectAttr(tfNode+'.pBInR2', pairBlendNode+'.inRotate2')    
       
        
        cmds.setAttr(folTransform+'.intermediateObject',1)
        cmds.setAttr(parentConNode+'.intermediateObject',1)
        cmds.parent( folTransform,  foGrp)
        
        cmds.parent(tfNode, tfGrp)
        
    cmds.delete(uvNode)
    #print 'Location 2'
    
    #Lock nodes
    ##Lock foGrp
    cmds.setAttr(foGrp+'.t', l=True)
    cmds.setAttr(foGrp+'.r', l=True)
    cmds.setAttr(foGrp+'.s', l=True)
    cmds.setAttr(foGrp+'.visibility', 0)
    cmds.lockNode(foGrp, l=True)
    
    
    ##Lock objGrp 
    cmds.setAttr(tfGrp+'.t', l=True)
    cmds.setAttr(tfGrp+'.r', l=True)
    cmds.setAttr(tfGrp+'.s', l=True)
    cmds.lockNode(tfGrp, l=True)
    cmds.lockNode(shellPoly, l=True)
    
    cmds.lockNode(cmds.listRelatives(tfGrp), l=True)


#-----------tfCtrl/Add---------------------
def addDriverByParForWrapedTFNode(tfGrp):
    '''{'del_path':'TfCtrl/Add/Group/addDriverByParForWrapedTFNode(cmds.ls(sl=True)[0])',
'usage':'$fun(cmds.ls(sl=True)[0])',
}
'''
        
    #get tfNodeGrp
    cmds.lockNode(tfGrp, l=False)
    if cmds.attributeQuery('shellPoly', n=tfGrp, exists=True) == False:
        raise IOError('This is not tfGrp object')
    else:
        shellPoly = cmds.getAttr('%s.shellPoly'%(tfGrp))
        
    if cmds.attributeQuery('nParShapeNode', n=tfGrp, exists=True) == False:
        cmds.addAttr(tfGrp,ln="nParShapeNode", dt="string")
    else:
        raise IOError('%s object has a nParShapeNode to control it')  
                
    tfNodeGrp = tfGrp
    #print '%s, %s'%(shellPoly, tfNodeGrp)        
    
    tfNodeGrpVarStr = tfNodeGrp.replace('|', '__')        
    objects = cmds.listRelatives(tfNodeGrp, type='transform',f=True)
        
    cmds.lockNode([shellPoly, tfNodeGrp], l=False)    
    
      
    ####################create and set nParticle etc.######################################
    #create nParticle
    nPar = cmds.nParticle(n='%s_nPar'%(tfNodeGrp) )
    cmds.setAttr(nPar[0]+'.t', l=True)
    cmds.setAttr(nPar[0]+'.r', l=True)
    cmds.setAttr(nPar[0]+'.s', l=True)
    cmds.lockNode(nPar[0], l=True)
    
    nParShape = nPar[1]
    
    #setAttr to get_tfGrpNode
    
    cmds.setAttr(tfNodeGrp+'.nParShapeNode', nParShape, type='string', l=True)
    cmds.lockNode([shellPoly, tfNodeGrp], l=True)
    cmds.setAttr('%s.computeRotation'%(nParShape), 1)
    cmds.goal( nParShape, g=shellPoly, w=.99 )
    #set attributes
    cmds.setAttr(nParShape+'.goalSmoothness', .01)
    cmds.setAttr(nParShape+'.radius', .01)
    
    #add attributes
    cmds.addAttr(nParShape,ln="cus_toObjPos", dt='doubleArray')
    cmds.addAttr(nParShape,ln="cus_toObjPos0", dt='doubleArray')
        
    #Add particles and set attributes(goalU, goalV, cus_bbsiRadius) initialize states
    posLi, radiusLi, atULi, atVLi = [], [], [], []
    for tfNode in objects:
        objPos = cmds.objectCenter(tfNode)
        bbsize = cmds.getAttr(tfNode+'.bbsi')[0]
        radius = vectorLen(bbsize)/2
        atU = cmds.getAttr(tfNode+'.atU')
        atV = cmds.getAttr(tfNode+'.atV')
        posLi.append(objPos)
        radiusLi.append(radius)
        atULi.append(atU)
        atVLi.append(atV)

    qsEmit(object = nParShape, position=posLi, attributes=( ('cus_radiusPP', 'floatValue', radiusLi), ('goalU', 'floatValue', atULi),\
                                                               ('goalV', 'floatValue', atVLi) )\
              )
    
    ##creation expression
    #parCExpStr = cmds.dynExpression(nParShape, q=True,s=True, c=True)
    parCExpStr = '\n\n\
/*string $tfNode = $%s[int(particleId)];\n\
goalU = `getAttr ($tfNode+".atU")`;\n\
goalV = `getAttr ($tfNode+".atV")`;\n\
cus_toObjPos = 0;*/'%(tfNodeGrpVarStr)
    
    cmds.dynExpression(nParShape,s=parCExpStr, c=True)
    
    ##runtime after dynamics expression
    #parRADExpStr = cmds.dynExpression(nParShape, q=True, s=True, rad=True)
    parRADExpStr = '\n\n\
/*string $tfNode = $%s[int(particleId)];\n\n\
\
if (cus_toObjPos == 1){\n\
    float $pos[] = position;\n\
    vector $rotate = rotationPP;\n\
    setAttr ($tfNode + ".pBInT2") -type "double3" ($pos[0]) ($pos[1]) ($pos[2]);\n\
    setAttr ($tfNode + ".pBInR2") -type "double3" ($rotate.x) ($rotate.y) ($rotate.z);\n\
}\n\n\
\
\
if (goalPP==0 && cus_toObjPos==0){\n\
    cus_toObjPos = 1;\n\
    float $pos[] = `getAttr ($tfNode+".translate")`;\n\
    position = <<$pos[0], $pos[1], $pos[2]>>;\n\
    vector $rotate = rotationPP;\n\
    setAttr ($tfNode + ".pBInT2") -type "double3" ($pos[0]) ($pos[1]) ($pos[2]);\n\
    setAttr ($tfNode + ".pBInR2") -type "double3" ($rotate.x) ($rotate.y) ($rotate.z);\n\
    setAttr ($tfNode+".pBWeight") 1;\n\
    setAttr ($tfNode+".follicleNodeState") 2;\n\
}*/'%(tfNodeGrpVarStr)
    cmds.dynExpression(nParShape,s=parRADExpStr, rad=True)
    
    ######################################create script nodes########################################
    ####openCloseMel script node   Execute On:Open/close
    openCloseMelStr = '\n\n\
///////////for TFNode by Particles/////////////////////\n\
global string $%s[];\n\
$%s = `listRelatives -f "%s"`;\n'%(tfNodeGrpVarStr,tfNodeGrpVarStr,tfNodeGrp)
    mel.eval(openCloseMelStr)
    if cmds.objExists("QS_VFX_M_OC"):
        existsStr = cmds.scriptNode('QS_VFX_M_OC', q=True, bs=True )
        openCloseMelStr += existsStr
        cmds.scriptNode('QS_VFX_M_OC', e=True, bs=openCloseMelStr)
    else:
        cmds.scriptNode(n='QS_VFX_M_OC',scriptType=1, bs=openCloseMelStr, sourceType='mel')
        cmds.setAttr('QS_VFX_M_OC.scriptType', l=True)
        
    ####timeChangedMel script Node    Execute on: Time changed
    timeChangedMelStr = '\n\n\
///////////for TFNode by Particles/////////////////////\n\
int $current = `currentTime -q`;\n\
int $start = `playbackOptions -q -min`;\n\
if ($current == $start){\n\
    //%s is a global variable, Declare in QS_VFX_M_QC script node.\n\
    $%s = `listRelatives -type "transform" "%s"`; \n\
    for ($tfNode in $%s){\n\
        setAttr($tfNode+".follicleNodeState") 0;\n\
        setAttr($tfNode+".pBWeight") 0;\n\
    }\n\
}'%(tfNodeGrpVarStr,tfNodeGrpVarStr,tfNodeGrp,tfNodeGrpVarStr)
    mel.eval(timeChangedMelStr)
    if cmds.objExists("QS_VFX_M_TC"): 
        existsStr = cmds.scriptNode('QS_VFX_M_TC', q=True, bs=True )
        timeChangedMelStr += existsStr
        cmds.scriptNode('QS_VFX_M_TC', e=True, bs=timeChangedMelStr)
    else:
        cmds.scriptNode(n='QS_VFX_M_TC',scriptType=7, bs=timeChangedMelStr, sourceType='mel')
        cmds.setAttr('QS_VFX_M_TC.scriptType', l=True)


def resetDriverParFroWrapedTFNode(tfGrp):
    '''{'del_path':'TfCtrl/Group/resetDriverParFroWrapedTFNode(cmds.ls(sl=True)[0])',
'usage':'$fun(cmds.ls(sl=True)[0])',
}
'''
    
    if cmds.attributeQuery('nParShapeNode', n=tfGrp, exists=True) == False:
        raise IOError ('%s have not particle to modify') 
    else:
        nParShape = cmds.getAttr( '%s.nParShapeNode'%(tfGrp) )
        if nParShape == None or cmds.objExists(nParShape) == False:
            raiseIOError ('%s not exists') 
                     
    objects = cmds.listRelatives(tfGrp, type='transform',f=True)
            
    posLi, radiusLi, atULi, atVLi = [], [], [], []
    for tfNode in objects:
        objPos = cmds.objectCenter(tfNode)
        bbsize = cmds.getAttr(tfNode+'.bbsi')[0]
        radius = vectorLen(bbsize)/2
        atU = cmds.getAttr(tfNode+'.atU')
        atV = cmds.getAttr(tfNode+'.atV')
        posLi.append(objPos)
        radiusLi.append(radius)
        atULi.append(atU)
        atVLi.append(atV)    
    
    qsEmit(object = nParShape, position=posLi, attributes=( ('cus_radiusPP', 'floatValue', radiusLi), ('goalU', 'floatValue', atULi),\

                                                               ('goalV', 'floatValue', atVLi) )     )

def addParByTFSet( tfSet = cmds.ls(sl=True, exactType='objectSet') ):
    '''{'del_path':'TfCtrl/Add/Set/addParByTFSet( tfSet = cmds.ls(sl=True, exactType="objectSet") )',
'usage':'$fun( tfSet = cmds.ls(sl=True, exactType="objectSet") )',
}
'''
    #tfSet = cmds.ls(sl=True, type='objectSet')[0]
    if isinstance( tfSet, list):
        tfSet = tfSet[0]
    cmds.lockNode(tfSet, l=False)
    objects = cmds.listConnections(tfSet+'.dagSetMembers', d=False)
    
    createNewPar=True
    
    if cmds.attributeQuery('setType', n=tfSet, exists=True) and cmds.getAttr(tfSet+'.setType')==1:
        raise IOError('This set type is three particle controls!')
    
    if cmds.attributeQuery('setType', n=tfSet, exists=True) and cmds.attributeQuery('posPar', n=tfSet, exists=True) and cmds.objExists( cmds.getAttr(tfSet+'.posPar') ):
        createNewPar = False
    
    
    if createNewPar:
        for attr in ['posPar', 'aimPar', 'upPar']:
            if cmds.attributeQuery(attr, n=tfSet, exists=True) and cmds.objExists( cmds.getAttr('%s.%s'%(attr)) ):
                cmds.delete(  cmds.getAttr('%s.%s'%(attr))  )
        
        delAttr(tfSet,['setType', 'posPar', 'aimPar', 'upPar'] )
        
        cmds.addAttr(tfSet, ln="setType", at="enum", en="singlePar:threePar:", k=False, r=False )
        cmds.setAttr(tfSet+'.setType', 0, l=True)   
        cmds.addAttr(tfSet,ln="posPar", dt="string")
        nPar = cmds.nParticle(n='%s_nPar'%(tfSet) )
        cmds.setAttr(nPar[0]+'.t', l=True)
        cmds.setAttr(nPar[0]+'.r', l=True)
        cmds.setAttr(nPar[0]+'.s', l=True)
        
        nParShape = nPar[1]
        cmds.setAttr(tfSet+'.posPar', nParShape, type='string', l=True)
        cmds.setAttr("%s.computeRotation"%(nParShape), 1)
        
        cmds.addAttr(nParShape,ln="cus_toObjPos", dt='doubleArray')
        cmds.addAttr(nParShape,ln="cus_toObjPos0", dt='doubleArray')
    else:
        nParShape = cmds.getAttr(tfSet+'.posPar')
        cmds.lockNode(nParShape, l=False)
    


       
    #Add particles and set attributes(goalU, goalV, cus_bbsiRadius) initialize states
    posLi, radiusLi, atULi, atVLi = [], [], [], []
    for tfNode in objects:
        objPos = cmds.objectCenter(tfNode)
        bbsize = cmds.getAttr(tfNode+'.bbsi')[0]
        radius = newom.MVector(bbsize).length()/2
        atU = cmds.getAttr(tfNode+'.atU')
        atV = cmds.getAttr(tfNode+'.atV')
        posLi.append(objPos)
        radiusLi.append(radius)
        atULi.append(atU)
        atVLi.append(atV)
    
    qsEmit(object = nParShape, position=posLi, attributes=( ('cus_radiusPP', 'floatValue', radiusLi), ('goalU', 'floatValue', atULi),\
                                                                   ('goalV', 'floatValue', atVLi) )\
                  )

    cmds.lockNode(tfSet, l=True)

    if createNewPar:
        ##creation expression
        #parCExpStr = cmds.dynExpression(nParShape, q=True,s=True, c=True)
        parCExpStr = '\n\n\
/*string $tfNode = $%s[int(particleId)];\n\
goalU = `getAttr ($tfNode+".atU")`;\n\
goalV = `getAttr ($tfNode+".atV")`;\n\
cus_toObjPos = 0;*/'%(tfSet)
    
        cmds.dynExpression(nParShape,s=parCExpStr, c=True)
    
        ##runtime after dynamics expression
        #parRADExpStr = cmds.dynExpression(nParShape, q=True, s=True, rad=True)
        parRADExpStr = '\n\n\
/*string $tfNode = $%s[int(particleId)];\n\n\
\
if (cus_toObjPos == 1){\n\
    float $pos[] = position;\n\
    vector $rotate = rotationPP;\n\
    setAttr ($tfNode + ".pBInT2") -type "double3" ($pos[0]) ($pos[1]) ($pos[2]);\n\
    setAttr ($tfNode + ".pBInR2") -type "double3" ($rotate.x) ($rotate.y) ($rotate.z);\n\
}\n\n\
\
\
if (goalPP==0 && cus_toObjPos==0){\n\
    cus_toObjPos = 1;\n\
    float $pos[] = `getAttr ($tfNode+".translate")`;\n\
    position = <<$pos[0], $pos[1], $pos[2]>>;\n\
    vector $rotate = rotationPP;\n\
    setAttr ($tfNode + ".pBInT2") -type "double3" ($pos[0]) ($pos[1]) ($pos[2]);\n\
    setAttr ($tfNode + ".pBInR2") -type "double3" ($rotate.x) ($rotate.y) ($rotate.z);\n\
    setAttr ($tfNode+".pBWeight") 1;\n\
    setAttr ($tfNode+".follicleNodeState") 2;\n\
}*/'%(tfSet)
        cmds.dynExpression(nParShape,s=parRADExpStr, rad=True)
    
        ######################################create script nodes########################################
        ####openCloseMel script node   Execute On:Open/close
        openCloseMelStr = '\n\n\
///////////for TFNode by Particles/////////////////////\n\
global string $%s[];\n\
$%s = `listConnections  -d off "%s.dagSetMembers"`;\n'%(tfSet,tfSet, tfSet)
        mel.eval(openCloseMelStr)
        if cmds.objExists("QS_VFX_M_OC"):
            existsStr = cmds.scriptNode('QS_VFX_M_OC', q=True, bs=True )
            openCloseMelStr += existsStr
            cmds.scriptNode('QS_VFX_M_OC', e=True, bs=openCloseMelStr)
        else:
            cmds.scriptNode(n='QS_VFX_M_OC',scriptType=1, bs=openCloseMelStr, sourceType='mel')
            cmds.setAttr('QS_VFX_M_OC.scriptType', l=True)
        
        ####timeChangedMel script Node    Execute on: Time changed
        timeChangedMelStr = '\n\n\
///////////for TFNode by Particles/////////////////////\n\
int $current = `currentTime -q`;\n\
int $start = `playbackOptions -q -min`;\n\
if ($current == $start){\n\
    //%s is a global variable, Declare in QS_VFX_M_QC script node.\n\
    $%s = `listConnections  -d off "%s.dagSetMembers"`; \n\
    for ($tfNode in $%s){\n\
        setAttr($tfNode+".follicleNodeState") 0;\n\
        setAttr($tfNode+".pBWeight") 0;\n\
    }\n\
}'%(tfSet,tfSet,tfSet, tfSet)

        mel.eval(timeChangedMelStr)
        if cmds.objExists("QS_VFX_M_TC"): 
            existsStr = cmds.scriptNode('QS_VFX_M_TC', q=True, bs=True )
            timeChangedMelStr += existsStr
            cmds.scriptNode('QS_VFX_M_TC', e=True, bs=timeChangedMelStr)
        else:
            cmds.scriptNode(n='QS_VFX_M_TC',scriptType=7, bs=timeChangedMelStr, sourceType='mel')
            cmds.setAttr('QS_VFX_M_TC.scriptType', l=True)
#----------TfCtrl/Utilities----------------------

def addAtUVAttr(objectList, shellPoly):
    '''{'del_path':'TfCtrl/Utilities/addAtUVAttr(cmds.ls(sl=True)[:-1], cmds.ls(sl=True)[-1] )',
'icon':':/attributes.png',
'usage':'$fun(cmds.ls(sl=True)[:-1], cmds.ls(sl=True)[-1] )',
}
'''

    
    if isinstance(objectList, str) or isinstance(objectList, unicode):
        objectList = [objectList]
    
    #Delete attributes
    delAttr(objectList, ['atU', 'atV'])
    
    #load plugin   
    if cmds.pluginInfo("nearestPointOnMesh",query=True,l=True)==False:
        cmds.loadPlugin("nearestPointOnMesh")
    #print 'Loaded plugin'
    
    
    #get shellPolyShape
    meshList = cmds.listRelatives(shellPoly,type='mesh')
    for mesh in meshList:
        if cmds.getAttr(mesh+'.intermediateObject') == 0:
            shellPolyShape = mesh
    #print 'Get shellPolyShape'    
    
 
    #create nearestPointOnMesh node add connection to shellPolyShape       
    uvNode = cmds.createNode("nearestPointOnMesh", n="setUV")
    cmds.connectAttr(shellPolyShape+'.worldMesh[0]', uvNode+'.inMesh',f=True)
    
    for tfNode in objectList:
        tfNodeCenter=cmds.objectCenter(tfNode)
        cmds.setAttr(uvNode+'.inPosition', tfNodeCenter[0], tfNodeCenter[1], tfNodeCenter[2], type="double3")
       
        u = cmds.getAttr(uvNode+'.parameterU')
        v = cmds.getAttr(uvNode+'.parameterV')
            

        cmds.addAttr(tfNode, ln='atU', at='double', dv=u)
        cmds.addAttr(tfNode, ln='atV', at='double', dv=v)
        cmds.setAttr(tfNode+'.atU', l=True)
        cmds.setAttr(tfNode+'.atV', l=True)

    cmds.delete(uvNode)
    



def removeTFNodeformTFGrp(objects):
    '''{'del_path':'TfCtrl/Remove/removeTFNodeformTFGrp(cmds.ls(sl=True,exactType="transform", l=True))',
'usage':'\
Delete attributes and follicle Node ect.\\n\
Put these objects to newPapa\\n\
$fun( cmds.ls(sl=True,exactType="transfororm", l=True) )',
}   
'''
    if isinstance(objects, (str, unicode ) ):
        objects = [objects]
    
    cmds.lockNode(objects, l=False)
    for tfNode in objects:
        tSource =  cmds.connectionInfo(tfNode+'.t',sfd=True)
        if tSource:
            cmds.disconnectAttr(tSource, tfNode+'.t')
        rSource = cmds.connectionInfo(tfNode+'.r',sfd=True)
        if rSource:
            cmds.disconnectAttr(rSource, tfNode+'.r')
        
        if cmds.attributeQuery('follicleNodeState', n=tfNode, exists=True):
            folObj = cmds.listConnections(tfNode+'.follicleNodeState')
            if folObj:
                cmds.delete( folObj )     
  
    delAttr(objects,['pBNode','follicleNodeState','atU', 'atV', 'pBNode1', 'pBWeight', 'pBInT2', 'pBInR2'])
    
    if not cmds.objExists('newPapa'):
        cmds.group(n='newPapa',em=True)    
    cmds.parent(objects, 'newPapa' )



def noiseVertex(objectList,noiseSize=1,resultScale=.01):
    '''{'del_path':'TfCtrl/Utilities/noiseVertex(cmds.ls(sl=True)[0], noiseSize=1,resultScale=.1)',
'usage':'\
#Use dnoise mel function to Noise per polyVertex\\n\
$fun(cmds.ls(sl=True)[0], noiseSize=1,res"ltScale=.1)',
}
'''
    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]
    objectList = __childCheck(objectList, 'mesh')
       
    for polyObj in objectList:
        for i in range(cmds.polyEvaluate(polyObj,v=True)):
            pos = cmds.pointPosition("%s.vtx[%s]"%(polyObj,i))
            noisePos =  mel.eval("dnoise(<<%s,%s,%s>>)"%(pos[0]*noiseSize,pos[1]*noiseSize,pos[2]*noiseSize) )
            oriPos = cmds.getAttr("%s.vtx[%s]"%(polyObj,i))[0]
            cmds.setAttr("%s.vtx[%s]"%(polyObj,i), noisePos[0]*resultScale+oriPos[0], noisePos[1]*resultScale+oriPos[1], noisePos[2]*resultScale+oriPos[2], type="double3")



def dupAndConnect(objectList):
    '''{'del_path':'TfCtrl/Extend/dupAndConnect(cmds.ls(sl=True,exactType="transform",l=True))',
'usage':'\
objectList = cmds.ls(sl=True,exactType="transform",l=True)\\n\
$fun(objectList)',
}
'''
    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]
        
    newGrp = cmds.group(em=True, name='newGrp')
    for obj in objectList:
        newObj = cmds.duplicate(obj, rr=True)[0]
        cmds.connectAttr(obj+'.t', newObj+'.t')
        cmds.connectAttr(obj+'.r', newObj+'.r')
        cmds.parent(newObj, newGrp)


