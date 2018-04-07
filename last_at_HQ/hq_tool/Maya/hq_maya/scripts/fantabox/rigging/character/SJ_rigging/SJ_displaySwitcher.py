#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-06-20
import pymel.core as pm
import maya.mel as mel
import maya.cmds as cmds
def SJ_displaySwitcher():
    '''
    {'load':'maya_rigging','defaultOption':1,'CNname':'Arnold”≤º˛œ‘ æ«–ªª£®Ã˘Õº”ÎID£©'}
    '''
    sels=[a.getShape() for a in pm.ls(sl=1) if pm.nodeType(a)=='transform']
    atrvails = ['diffuseColor','color','shallowScatterColor']
    if sels!=[]:
        for sel in sels:
            SGs= sel.listConnections(s=0,type="shadingEngine")
            for SG in SGs:
                allCons =  pm.listHistory(SG,ac=1)
                displayshaderlists = pm.ls('display_shader*')
                displayshaderjudge = pm.listConnections(SG+".surfaceShader",d=0)
                if  displayshaderjudge[0] not in displayshaderlists:
                    AWsels = [a for a in  pm.ls(allCons,type="aiWriteColor") if cmds.nodeType(cmds.listConnections(a+".beauty",d=0)[0])!="aiWriteColor"]
                    for AWsel in AWsels:
                        AWshaders = [a for a in cmds.listConnections(AWsel+".beauty",d=0) if cmds.nodeType(a)!="aiWriteColor"]
                        for AWshader in AWshaders:
                            for atrvail in atrvails:
                                if cmds.objExists(AWshader+'.'+atrvail):
                                    shader = cmds.listConnections(AWshader+'.'+atrvail,d=0)
                                    if shader!=None:
                                        shderfiletype =  cmds.nodeType(shader[0])
                                        if shderfiletype !="file":
                                            shderfiles = [b for b in cmds.listHistory(shader[0],ac=1) if cmds.ls(b,type="file")!=[]]
                                        else:
                                            shderfiles = shader
                                        Aiorginalshader =  pm.listConnections(SG+'.aiSurfaceShader',d=0)
                                        if Aiorginalshader==[]:
                                            orginalConnect =  pm.listConnections(SG+'.surfaceShader',d=0,plugs=1)
                                            disShader = pm.shadingNode('lambert',asShader=1,name='display_shader')
                                            pm.connectAttr(shderfiles[0]+".outColor",disShader+".color",f=1)
                                            pm.connectAttr(orginalConnect[0],SG+'.aiSurfaceShader',f=1)
                                            pm.connectAttr(disShader+".outColor",SG+'.surfaceShader',f=1)
                                            pm.setAttr("hardwareRenderingGlobals.enableTextureMaxRes",1)
                                            pm.setAttr("hardwareRenderingGlobals.textureMaxResolution",1024)
                                            mel.eval('generateAllUvTilePreviews')
                                        else:
                                            pm.warning('aiSurfaceShaderAttr has already been Connected!!')
                else:
                    AiorginalConnect =  pm.listConnections(SG+'.aiSurfaceShader',d=0,plugs=1)
                    if AiorginalConnect!=[]:
                        for displayshaderlist in displayshaderlists:
                            pm.connectAttr(AiorginalConnect[0],SG+".surfaceShader",f=1)
                            pm.disconnectAttr(AiorginalConnect[0],SG+".aiSurfaceShader")
                            pm.delete(displayshaderjudge)
                    else:
                        pm.warning(sel+"'s shader has lost!!")
    else:
        pm.warning('please select A mesh!!')