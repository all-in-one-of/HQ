# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import maya.mel as mel
class w06_T_nParticlesBakeWin(object):
    
    _menuStr = '''{'path':'Dynamics/Particles/w06_T_nParticlesBakeWin()',
'icon':':/instancer.svg',
'tip' :  '烘赔粒子替代', 
'usage':'$fun()',
}
'''
    def __init__(self):
        if cmds.window('w06', exists=True):
            cmds.deleteUI('w06')
            
        cmds.window('w06',title='w06_T_nParticlesBake', wh=[320,400], sizeable=False)
        cmds.columnLayout( 'w06_L01', p='w06', adj=True)
        cmds.button( 'w06_uiSelParticles', p='w06_L01', l="Bake", h=50, bgc=[.3, 1, .3], c=self.w06_MainCmd )
       
    
        cmds.separator(p='w06_L01',h=10, en=False, style='in')
        
        cmds.rowColumnLayout('w06_L04', p='w06', nc=2, columnWidth=[(1, 250), (2, 70)])
        cmds.textField('w06_uiMessage', p='w06_L04', en=0, text="Select a particle object and click Get")
        cmds.button('w06_uiGetPar', p='w06_L04', l='Get', bgc=[.4,.4,.4], c= self.w06_setPartileName )
        
        cmds.optionMenu( 'w06_uiInstancers', p='w06_L04', label='Instancer Node' ) 
        cmds.separator(p='w06_L01',h=10, en=False, style='in')
        cmds.text( label='Duplicate Options', p='w06_L01')
        cmds.checkBox('w06_uiRenameChildren', p='w06_L01', l="Assign unique name to child nodes", align="left", v=1)
        cmds.checkBox('w06_uiInputCon', p='w06_L01', l="Duplicate input connections", align="left", v=0)    
        cmds.checkBox('w06_uiInstanceLeaf', p='w06_L01', l="Instance leaf nodes", align="left", v=0) 
        
        cmds.separator(p='w06_L01',h=10, en=False, style='in')
        cmds.separator(p='w06_L01',h=10, en=False, style='in')
        cmds.checkBox('w06_uiBakePosition', p='w06_L01', l="position", align="left", v=1)
        cmds.checkBox('w06_uiBakeRotate', p='w06_L01', l="rotation", align="left", v=1)
        cmds.checkBox('w06_uiBakeScale', p='w06_L01', l="scale", align="left", v=1)
        cmds.separator(p='w06_L01',h=10, en=False, style='in')
        
        cmds.rowColumnLayout('w06_L02', p='w06', nc=2,columnWidth=[(1, 155), (2, 155)])
        cmds.checkBox('w06_uiTimeRangeCBox', p='w06_L02', label="Timeline Range:", v=True,\
                     cc="w06_uiTimeRangeCBoxCmd()"  )
        cmds.text(label="", p='w06_L02')
        cmds.text(label="Start:", p='w06_L02')
        cmds.text(label="End:", p='w06_L02')
        cmds.intField('w06_startField', p='w06_L02', en=0, v=cmds.playbackOptions(q=True, min=True) ) 
        cmds.intField('w06_endField', p='w06_L02', en=0, v=cmds.playbackOptions(q=True, max=True) )
        
        cmds.separator(p='w06_L01',h=10,en=False, style='in')
        
        #my modify
        cmds.checkBox('w06_uiAttrListSwitch', p='w06_L01', label="Create New Attributes:", h=20,\
                     onc=self.w06_addAttrsListCmd, 
                     ofc="cmds.textScrollList('w06_uiAttrList', e=True, en=False)",\
                     v=False)
        
        cmds.paneLayout('w06_L03', p='w06')
        cmds.textScrollList('w06_uiAttrList', p='w06_L03', numberOfRows=8, allowMultiSelection=True, en=0, h=300, bgc=[.2,.2,.2], showIndexedItem=4)
        cmds.showWindow( 'w06')
    #-------------------w06  Start
    def w06_uiTimeRangeCBoxCmd(self, *args):
        if cmds.checkBox('w06_uiTimeRangeCBox', q=True, v=True):
            cmds.intField('w06_startField',e=True, en=0, v=cmds.playbackOptions(q=True, min=True) ) 
            cmds.intField('w06_endField', e=True, en=0, v=cmds.playbackOptions(q=True, max=True) )
        else:
            cmds.intField('w06_startField',e=True, en=1, v=cmds.playbackOptions(q=True, min=True) ) 
            cmds.intField('w06_endField', e=True, en=1, v=cmds.playbackOptions(q=True, max=True) )
                
    
    def w06_getParShape(self, parNode=None):
        if parNode:
            obj=parNode
        else:
            obj = cmds.ls(sl=True)
            if obj==[]:
                return False
            else:
                obj = obj[0]
        
        papa=None
        parShape = None
        if obj:       
            if cmds.objectType(obj)=='nParticle':
                papa = cmds.listRelatives(obj, parent=True)[0]
                parShape = obj            
            elif cmds.listRelatives(obj, shapes=True, type='nParticle')!=None:
                papa=obj
                parShape = cmds.listRelatives(obj, shapes=True, type='nParticle')[0]
                
        if papa==None:
            return False
        else:
            return (papa,parShape)
    
    
    def w06_getParAttrList(self, *args):
        parName = cmds.textField('w06_uiMessage',q=True,text=True)
        doAdd = False if parName=="Select a particle object and click Get" else True
        print doAdd
        if doAdd:
            parShape = w06_getParShape(parName)[1]
            print parShape
            attrList = cmds.listAttr(parShape, a=True)
            attrList.sort()
            print attrList
            for attr in attrList:
                try:attrType = str( cmds.getAttr('%s.%s'%(parShape,attr), type=True) )
                except: attrType=False
                
                
                if attr[-1] == '0' or (attrType!='vectorArray' and attrType!='doubleArray'):
                    attrList.remove(attr)
                    print attrType, attr
            return attrList
            
        else:
            return []
    
    def w06_addAttrsListCmd(self, *args):    
        cmds.textScrollList('w06_uiAttrList', e=True, en=True, removeAll=True)    
        for attr in self.w06_getParAttrList():
            cmds.textScrollList('w06_uiAttrList', e=True, append=attr)
    
    
    def w06_MainCmd(self, *args):
        parName = cmds.textField('w06_uiMessage',q=True,text=True)
        if parName!="Select a particle object and click Get":
            parNode = self.w06_getParShape(parName)[1]
            startFrame = int( cmds.intField('w06_startField', q=True, v=True ) )
            endFrame = int( cmds.intField('w06_endField', q=True, v=True ) )
            exclusiveAttrs=[]
            if cmds.checkBox('w06_uiBakePosition', q=True, v=True)==False:
                exclusiveAttrs.append('position')
            if cmds.checkBox('w06_uiBakeRotate', q=True, v=True)==False:
                exclusiveAttrs.append('rotation')
            if cmds.checkBox('w06_uiBakeScale', q=True, v=True)==False:
                exclusiveAttrs.append('scale')
            
            if cmds.checkBox('w06_uiAttrListSwitch', q=True, v=True):
                otherParAttrs = cmds.textScrollList( "w06_uiAttrList", q=True, si=True)
            else:
                otherParAttrs = []
            #print 'w06_doBake', parNode, startFrame, endFrame, exclusiveAttrs, otherParAttr
            insIndex = cmds.optionMenu( 'w06_uiInstancers', q=True, select=True)
            instancerNode = cmds.particleInstancer( parNode, q=True, name=True)[insIndex-1]
    
            self.w06_doBake(parNode=parNode, instancerNode=instancerNode, startFrame=startFrame, endFrame=endFrame, 
                       exclusiveAttrs=exclusiveAttrs, otherParAttr=otherParAttrs,
                       renameChild=cmds.checkBox('w06_uiRenameChildren',q=True,v=True),
                       dup_connect=cmds.checkBox('w06_uiInputCon', q=True, v=True),
                       dup_instance=cmds.checkBox('w06_uiInstanceLeaf', q=True, v=True),
                       )
    
    
    #w06_T_nParticlesBakeWin()
    
    def w06_doBake(self, parNode=None, instancerNode=None, startFrame=None, endFrame=None, exclusiveAttrs=[], otherParAttr=[], renameChild=True, dup_connect=False, dup_instance=False,  ):
        #import random
        temp = self.w06_getParShape(parNode)
        parPapa= temp[0]
        parShape = temp[1]
        insNode = instancerNode
        #if insNode!=None:
        #    insNode = insNode[0]
        
        poolGrp = '%s_ins_baked'%(parPapa)
        if cmds.objExists(poolGrp)==False:
            poolGrp = cmds.group(name=poolGrp, em=True)
        else:
            temp = cmds.listRelatives(poolGrp)
            if temp:
                cmds.delete(temp)
            
        grpLoc = '%s_loc_dup'%(parShape)
        if cmds.objExists(grpLoc)==False:
            grpLoc = cmds.group(name=grpLoc, em=True)
        
        oriObjs = mel.eval('particleInstancer -name %s -q -object %s'%(insNode, parShape) )    #cmds.particleInstancer(parShape, name=insNode, q=True, object=True)
        poolObjs = [] if cmds.listRelatives( poolGrp, f=True )==None else cmds.listRelatives( poolGrp, f=True )
        
        attrsData = {'position':['double3', ['tx','ty','tz'] ],\
                     'rotation':['double3', ['rx','ry','rz'] ],\
                     'scale':['double3', ['sx','sy','sz'] ],\
                     'aimDirection':['double3',['target[0].targetTranslate'] ], \
                     'aimPosition':['double3',['target[0].targetTranslate'] ],\
                     'aimAxis':['double3',['aimVector'] ],\
                     'aimUpAxis':['double3',['upVector'] ],\
                     'aimWorldUp':['double3',['worldUpVector'] ]\
                     }
        
        
        if 'position' in exclusiveAttrs and 'rotation' in exclusiveAttrs:
            attrsData.pop('position')
        
        if 'rotation' in exclusiveAttrs:
            for attr in  ('rotation', 'aimDirection', 'aimPosition', 'aimAxis','aimUpAxis', 'aimWorldUp'):
                if attr in attrsData.keys():
                    attrsData.pop(attr)
        
        if 'scale' in exclusiveAttrs:
            attrsData.pop('scale')
             
        for attr in attrsData.keys():
            parAttr = mel.eval('particleInstancer -n "%s" -q -%s "%s"'%(insNode, attr, parShape) )
            if parAttr==None:
                attrsData.pop(attr)
            else:
                attrType = cmds.getAttr('%s.%s'%(parShape,parAttr), type=True)
                if attrType=='doubleArray':
                    dataType='double'
                else:#dataType is vectorAttry
                    dataType='double3'
                attrsData[attr].extend( (dataType,parAttr,'') )
        
        aimConstraint=False
        if 'rotation' in attrsData.keys():
            for attr in  ('aimDirection', 'aimPosition', 'aimAxis','aimUpAxis', 'aimWorldUp'):
                if attr in attrsData.keys():
                    attrsData.pop(attr)
        elif 'aimDirection' in attrsData.keys() or 'aimPosition' in attrsData.keys() or\
            'aimAxis' in attrsData.keys() or 'aimWorldUp' in attrsData.keys() :
            aimConstraint=True
            aimCon = cmds.createNode('aimConstraint', name='%s_instanceAimConstraint'%(parPapa) )        
            aimAttrs = []
            if 'aimDirection' in attrsData.keys() and 'aimPosition' in attrsData.keys():
                attrsData.pop('aimPosition')
                
            for attr in  ('aimDirection', 'aimPosition', 'aimAxis','aimUpAxis', 'aimWorldUp'):
                if attr in attrsData.keys():
                    aimAttrs.append(attr)
                    
        notKeyAttrs = ['aimDirection', 'aimPosition', 'aimAxis','aimUpAxis', 'aimWorldUp']
        notKeyAttrs.extend(exclusiveAttrs)
        
        newAttrs = {}
        if otherParAttr:
            for attr in otherParAttr:
                attrType = 'double3' if str( cmds.getAttr('%s.%s'%(parShape,attr), type=True) )=='vectorArray' else 'double'
                if attrType=='double3':
                    subAttrs = [attr+'X', attr+'Y', attr+'Z']
                else:
                    subAttrs = [attr]
                newAttrs[attr] = [attrType, subAttrs, attrType, attr, '']
        
        keyModel = True
        curObjs = {}
        #startFrame = 1
        #endFrame = 100
        objectIndexAttr = mel.eval('particleInstancer -n "%s" -q -objectIndex "%s"'%(insNode, parShape) )
        
        #print attrsData
        
        
        for curF in range( startFrame, endFrame+1 ):
            objsVis = {}
            import time
            startTime = time.time()
            cmds.currentTime(curF, e=True)
            ids = cmds.getParticleAttr(parShape, at='particleId', array=True)
            ids = [] if ids ==None else ids
            print '\n\nFrame: '+str(curF)
            
            if ids:
                if objectIndexAttr:
                    objsIndex = [int(i) for i in cmds.getParticleAttr(parShape, at=objectIndexAttr, array=True)]
                else:
                    #objsIndex = [i for i in range(len(ids)) ]
                    objsIndex = [0 for i in range(len(ids)) ]
                #Get born particles
                #print 'poolObjs:', poolObjs
                for pId in ids:
                    pId = int(pId)        
                    #Get last frame born particles
                    if pId not in curObjs.keys():
                        attrIndex = ids.index(pId)
                        #print poolObjs
                        objIndex =  objsIndex[attrIndex]
                        oriObj = oriObjs[objIndex]
                        #renameChild=True, dup_connect=False, dup_instance=False
                        newObj = cmds.duplicate(oriObj, name='%s_ins_%05d'%(parPapa,pId), rr=True, rc=renameChild, ic=dup_connect, ilf=dup_instance )[0]
                        cmds.parent( newObj, poolGrp)
                        for newAttr in newAttrs.values():
                            if newAttr[0] == 'double3':
                                cmds.addAttr(newObj, ln=newAttr[3], at=newAttr[2])
                                for newAttrName in newAttr[1]:
                                    cmds.addAttr(newObj, ln=newAttrName,  p=newAttr[3], at='double',keyable=True)
                            else:#newAttr=='double'
                                cmds.addAttr(newObj, ln=newAttr[1][0], at='double', keyable=True)
                                    
                        #Create new attributes
                        curObjs[pId] = newObj
                        cmds.setKeyframe(newObj, at='visibility', t=curF-1, v=False)
                        cmds.setKeyframe(newObj, at='visibility', v=True)
            
                #Get die particles 
                diedList = []
                #print str(i), ': ', ids
                #print 'beforeFramesIds: ', curObjs.keys()
                for pId in curObjs.keys():
                    if pId not in ids:
                        diedList.append( pId )
                        cmds.setKeyframe(curObjs[pId], at='visibility', v=False)
    
                
                #Remove died particles from curObjs dictionary
                #print 'Before: ',  curObjs
                #print 'diedList', diedList
                for pId in diedList:
                    tempObj = curObjs[pId]        
                    curObjs.pop(pId)
                
            
            #Get particles data for bake
            #print attrsData
            if ids:
                for key, value in attrsData.iteritems():
                    #if key=='rotation' and value[3]=='aimConstraint':
                        #for aimAttr in aimAttrs.iteritems():
                            #pass
                    #else:
                    if value[0]==value[2]:
                        attrsData[key][4]= cmds.getParticleAttr(parShape, at=value[3], array=True)
                    elif value[0]=='double3' and value[2]=='double':
                        temp = []
                        for i in cmds.getParticleAttr(parShape, at=value[3], array=True):
                            temp.extend( (i,i,i) )
                        attrsData[key][4] = temp
                    elif value[0]=='double' and value[2]=='double3':
                        temp=[]
                        tempData = cmds.getParticleAttr(parShape, at=value[3], array=True)
                        attrsData[key][4] =   [tempData[i] for i in range(0, len(tempData), 3) ]                        
                    else:
                        raise IOError()
                #print  attrsData['aimDirection'][4]!=''
                if attrsData.has_key('aimDirection') and attrsData['aimDirection'][4]!='':
                    temp = []
                    #temp = [ attrsData['aimDirection'][4][aimi] + attrsData['position'][4][aimi]\
                             #for aimi in range(  len(attrsData['aimDirection'][4])  )      ]
                    #attrsData['aimDirection'][4] = temp[:]
                    
                    for aimi in range( len(attrsData['aimDirection'][4]) ):
                        temp.append(  attrsData['aimDirection'][4][aimi] + attrsData['position'][4][aimi]  )
                    attrsData['aimDirection'][4] = temp[:]
                
                #Get rotate attribute data
                if aimConstraint:
                    rotTemp = []
                    dataIndex = 0
                    for pId in ids:                
                        cmds.setAttr('%s.constraintTranslate'%(aimCon),\
                                     attrsData['position'][4][dataIndex],attrsData['position'][4][dataIndex+1],\
                                     attrsData['position'][4][dataIndex+2], type='double3')              
                        for aimAttr in aimAttrs:
                            value = attrsData[aimAttr]
                            cmds.setAttr('%s.%s'%(aimCon, value[1][0]), value[4][dataIndex], value[4][dataIndex+1], value[4][dataIndex+2], type='double3')
                        rotTemp.extend( cmds.getAttr(aimCon+'.constraintRotate')[0] )
                        dataIndex = dataIndex+3
                    #rotateData= ['double3', ['rx', 'ry', 'rz'], 'double3', 'aimConstraint', '']
                        
                    
                        
                for key, value in newAttrs.iteritems():
                    newAttrs[key][4] = cmds.getParticleAttr(parShape, at=value[3], array=True)
                
                #Combine attrsData with newAttrs together
                tempData = newAttrs.copy()
                if aimConstraint:
                    tempData['rotation'] = ['double3', ['rx', 'ry', 'rz'], 'double3', 'aimConstraint', rotTemp]
                for key, value in attrsData.iteritems():            
                    if key not in notKeyAttrs:
                        tempData[key] = value
                                
                for key, value in tempData.iteritems():
                    dataIndex = 0
                    for pId in ids:
                        obj=curObjs[pId]            
                        for attr in value[1]:
                            cmds.setKeyframe(obj, at=attr, v=value[4][dataIndex])
                            dataIndex = dataIndex+1
            
            print 'Current particle count: %s\nUsed Times: %s'\
                    %( len(ids), time.time()-startTime )
                    
            #if cmds.memory(freeMemory=True)[0]<800:        
                #cmds.flushUndo()
        if aimConstraint:
            cmds.delete(aimCon)
        cmds.delete( grpLoc )
        cmds.flushUndo()
    
    def w06_setPartileName(self, *args):
        parNode = self.w06_getParShape()
        fieldStr = parNode[0] if parNode else "Select a particle object and click Get" 
        cmds.textField("w06_uiMessage", e=True, text= fieldStr )    
        if not parNode:
            return
        
        ins = cmds.optionMenu( 'w06_uiInstancers', q=True, itemListLong=True)
        if ins:
            cmds.deleteUI( ins )
        
        insNodes = cmds.particleInstancer( parNode[1], q=True, name=True)
        print 'b', insNodes
        if insNodes:
            for ins in insNodes:
                cmds.menuItem( label=ins, p='w06_uiInstancers')
                
    

    
    #w06_T_nParticlesBakeWin()
    #----------------w06 End