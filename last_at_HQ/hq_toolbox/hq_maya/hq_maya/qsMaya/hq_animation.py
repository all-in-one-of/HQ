# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################



import maya.cmds as cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as newom
import math
import qsMaya as qm

from qsMaya.utility import *

def objConstrain( fromObj, toObj ):
    objType = cmds.nodeType( fromObj )
    shapeAttrs = {'mesh':('.outMesh', '.inMesh'), 
                  'nurbsCurve':('.worldSpace', '.create'), 
                  'nurbsSurface':('.worldSpace', '.create') }.get(objType, None)
    if shapeAttrs:        
        cmds.connectAttr( fromObj+shapeAttrs[0], toObj+shapeAttrs[1])
        fromObjTrans = cmds.listRelatives( fromObj, parent=True, f=True)[0]
        toObjTrans = cmds.listRelatives( toObj, parent=True, f=True)[0]
        cmds.parentConstraint( fromObjTrans, toObjTrans, mo=False, weight=1) 
                            
        #deMatrix = cmds.createNode( 'decomposeMatrix' )
        #toObjTrans = cmds.listRelatives( toObj, parent=True, f=True)[0]
        #cmds.connectAttr( fromObj+'.worldMatrix', deMatrix+'.inputMatrix')        
        #cmds.connectAttr( deMatrix+'.outputTranslate', toObjTrans+'.translate' )
        #cmds.connectAttr( deMatrix+'.outputRotate', toObjTrans+'.rotate' )
        #cmds.connectAttr( deMatrix+'.outputScale', toObjTrans+'.scale' )
        #cmds.connectAttr( deMatrix+'.outputShear', toObjTrans+'.shear' )        
        return True
    
    return False



def animKeyScale(objects, attributes, baseValueAtTime=0, scaleValue=.5):
    '''{"del_path02":"Edit/Keys/animKeyScale( )ONLYSE",
"icon02":"animCurveTT.svg",
'icon':":/animCurveTT.svg",
'tip':'缩放动画曲线',
"usage":"""
objects = cmds.ls(sl=True, exactType="transform", l=True)
attributes = ["tx", "ty", "tz"]
$fun(objects, attributes, 0, .5)""",
}
'''
    if isinstance(objects, str) or isinstance( objects, unicode ):
        objects = [objects]
    if isinstance( attributes, str) or isinstance( attributes, unicode):
        attributes = [attributes]


    for obj in objects:
        for attr in attributes:
            valueLi = cmds.keyframe('%s.%s'%(obj,attr), vc=True, q=True)
            if cmds.attributeQuery(attr, n=obj, exists=True) and valueLi:
                kfCount = cmds.keyframe('%s.%s'%(obj,attr), keyframeCount=True, q=True)
                baseValue = cmds.getAttr('%s.%s'%(obj,attr), t=baseValueAtTime)
                for i in range(kfCount):
                    newValue = (valueLi[i] - baseValue) * scaleValue + baseValue
                    cmds.keyframe('%s.%s'%(obj,attr), index=(i,i), vc=newValue)


def simplifyCurves( *args, **kwargs): #objList, attributes, threshold=.01):
    '''{"path":"Edit/Keys/simplifyCurves( )ONLYSE",
"tip":"优化动画曲线，减少文件大小",
"icon":":/animCurveTT.svg",
"usage":"""
$fun( attrs=["tx", "ty", "tz", "rx", "ry", "rz"], threshold=0 )
""",
"help":"""
对选择的物体，对指定的属性的动画进行优化，两个关键帧值的差小于threshold的关键帧删除。这个命令不会像maya自带的一样，对动画造成破坏
"""
}
'''
    if len(args):
        if isinstance( (args[0]), str):
            objList = [objList]
        else:
            objList = args[0]

        temp = objList[:]
        objList = []
        for obj in temp:
            newObj = checkArg(obj, nodeType='transform', tryToShape=False)
            if newObj:
                objList.append( newObj )
    else:
        objList = cmds.ls(sl=True, exactType='transform' )

    attrs = kwargs.get( 'attrs', ["tx", "ty", "tz", "rx", "ry", "rz", 'sx', 'sy', 'sz', 'v'] )
    threshold = kwargs.get( 'threshold', .001)
    
    objAttrs = {}
    for obj in objList:
        hasAttrs = []
        for attr in attrs:
            if cmds.attributeQuery(attr, n=obj, exists=True) and cmds.listConnections('%s.%s'%(obj,attr), d=False, type='animCurve', scn=True):
                hasAttrs.append( attr )
        if hasAttrs:
            objAttrs[obj] = hasAttrs
    
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    
    cmds.progressBar( gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True,
                    status='Optimize animation curves.....', maxValue=len(objAttrs.keys())  )
    
    curCount = 0
    for obj, attrs in objAttrs.iteritems(): #enumerate(objList):
        if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ):
            break
        cmds.progressBar(gMainProgressBar, edit=True, step=1 )
        
        for attr in attrs:            
            keyValues = cmds.keyframe(obj+"."+attr,query=True,vc=True)
            timeValues = cmds.keyframe(obj+"."+attr,query=True,tc=True)
            clTime = []
            for curIndex in range(2,len(keyValues)):
                bfIndex, bf2Index = curIndex-1, curIndex-2
                curValue, bfValue, bf2Value = keyValues[curIndex], keyValues[bfIndex], keyValues[bf2Index]
                if curValue-threshold <= bfValue \
                        and curValue+threshold >= bfValue \
                        and curValue-(threshold*2) <= bf2Value \
                        and curValue+(threshold*2) >= bf2Value:
                    #cmds.cutKey(obj, index=(bfIndex,bfIndex),at='rx', option="keys")
                    clTime.append(timeValues[bfIndex])
                    #print cmds.keyframe(obj+'.rx',index=(curIndex-1, curIndex-1),query=True)
            for t in clTime:
                cmds.cutKey(obj, time=(t,t),at=attr, option="keys")
        curCount += 1
        if curCount%400==0:
            cmds.flushUndo()
    cmds.flushUndo()
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)


def removeFractionalKeys( *args, **kwargs):
    '''{'path':'Edit/Keys/removeFractionalKeys( )',
'tip':'删除transform属性的小数关键帧',
'usage':"""
#删除选择物体的translate, rotate, scale, visibility的小数帧
$fun( )""",
}
    '''
    if len(args):
        if isinstance( args[0], tuple ):
            objs = ( args[0], )
        else:
            temp = objs[:]
            objs = []
            for obj in temp:
                newObj = checkArg( nodeType='transform', tryToShape=False)
                if newObj:
                    objs.append( newObj )
    else:
        objs = cmds.ls(sl=True)

    attrs = kwargs.get( 'attrs', ("tx", "ty", "tz", "rx", "ry", "rz", 'sx', 'sy', 'sz', 'v') )
    start = cmds.playbackOptions(q=True,minTime=True)
    start = int( kwargs.get('startFrame', start ) )

    end = cmds.playbackOptions(q=True,maxTime=True)+1
    end = int( kwargs.get('endFrame', end ) )
    end = end if start<end else start+1

    cmds.select( objs, r=True )
    for i in range(start, end):
        cmds.cutKey(time=(i+.01,i+.99), at=attrs, option='keys')


def reTime(*args, **kwargs ):
    '''{'del_path':'Edit/Keys/reTime( speed=1 )ONLYSE',
'usage':'$fun( speed=1 )',
}
'''
    #speed = 1
    #obj = cmds.ls(sl=True)[0]

    if len( args ):
        obj = checkArg( args[0], nodeType='transform', tryToShape=False )
    else:
        obj = checkArg( nodeType='transform', tryToShape=False )

    speed = kwargs.get( 'speed', 1)


    transformAttrs = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz')
    mappingAttrs = ('m_tx', 'm_ty', 'm_tz', 'm_rx', 'm_ry', 'm_rz', 'm_sx', 'm_sy', 'm_sz')
    testAttrs = ('t_tx', 't_ty', 't_tz', 't_rx', 't_ry', 't_rz', 't_sx', 't_sy', 't_sz')
    attrData = {}
    activeAttrs = []
    for attr in transformAttrs:
        #hasCon = cmds.connectionInfo('%s.%s'%(obj,attr), id=True)
        hasCon = cmds.listConnections('%s.%s'%(obj,attr), d=False, scn=True)
        if hasCon is not None:
            print hasCon[0]
            #attrData[attr] = [True,hasCon[0]]
            attrData[attr] = hasCon[0]
            activeAttrs.append(attr)
        else:
            attrData[attr] = False

    #print activeAttrs

    if 'tx' not in activeAttrs and 'ty' not in activeAttrs and 'tz' not in activeAttrs:
        raise IOError('%s translate attributes has not connection or keyframe'%obj)



    frameRange = []
    for attr in activeAttrs:
        if attrData[attr]:
            frames = cmds.keyframe(obj+"."+attr,query=True,tc=True)
            #print frames
            frameRange.extend( [frames[0], frames[-1]] )

    frameRange.sort()
    frameRange=( int(frameRange[0]), int(frameRange[-1]) )
    print frameRange

    createT = True if 'tx' in activeAttrs or 'ty' in activeAttrs or 'tz' in activeAttrs else False
    createR = True if 'rx' in activeAttrs or 'ry' in activeAttrs or 'rz' in activeAttrs else False
    createS = True if 'sx' in activeAttrs or 'sy' in activeAttrs or 'sz' in activeAttrs else False

    activeChannels = ['t']
    if createR:  activeChannels.append('r')
    if createS:  activeChannels.append('s')

    #QM.delAttr(obj, ['b_s', 'm_f', 'geoCacheTime', 'm_t', 'm_r', 'm_s', 'test_t', 'test_r', 'test_s', 't_deacc', 'simRate'] )


    if cmds.attributeQuery('b_s', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='base_speed', sn='b_s', at='double' )

    if cmds.attributeQuery('m_f', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='mapping_frame', sn='m_f', at='time' )

    if cmds.attributeQuery('simRate', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='simulationRate', sn='simRate', at='double' )

    if cmds.attributeQuery('geoCacheTime', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='geoCacheTime', at='time' )

    if cmds.attributeQuery('m_t', n=obj, exists=True) == False :
        cmds.addAttr(obj, ln='mapping_t',  sn='m_t',  at='double3')
        cmds.addAttr(obj, ln='mapping_tx', sn='m_tx', p='mapping_t', at='doubleLinear')
        cmds.addAttr(obj, ln='mapping_ty', sn='m_ty', p='mapping_t', at='doubleLinear')
        cmds.addAttr(obj, ln='mapping_tz', sn='m_tz', p='mapping_t', at='doubleLinear')

    if cmds.attributeQuery('m_r', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='mapping_r',   sn='m_r', at='double3')
        cmds.addAttr(obj, ln='mapping_rx',  sn='m_rx', p='mapping_r', at='doubleAngle')
        cmds.addAttr(obj, ln='mapping_ry',  sn='m_ry', p='mapping_r', at='doubleAngle')
        cmds.addAttr(obj, ln='mapping_rz',  sn='m_rz', p='mapping_r', at='doubleAngle')

    if cmds.attributeQuery('m_s', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='mapping_s',   sn='m_s', at='double3')
        cmds.addAttr(obj, ln='mapping_sx',  sn='m_sx', p='mapping_s', at='double')
        cmds.addAttr(obj, ln='mapping_sy',  sn='m_sy', p='mapping_s', at='double')
        cmds.addAttr(obj, ln='mapping_sz',  sn='m_sz', p='mapping_s', at='double')



    cmds.setAttr(obj+'.b_s', l=False)
    cmds.setAttr(obj+'.m_f', l=False)
    cmds.setAttr(obj+'.simRate', l=False)
    cmds.setAttr(obj+'.geoCacheTime', l=False)

    cmds.cutKey(obj, at='b_s', option='keys')
    cmds.cutKey(obj, at='m_f', option="keys")
    cmds.cutKey(obj, at='simRate', option="keys")
    cmds.cutKey(obj, at='geoCacheTime', option="keys")

    cmds.cutKey(obj, at='m_t', option="keys")
    cmds.setAttr(obj+'.m_t', l=False)
    cmds.setAttr(obj+'.m_tx', l=False)
    cmds.setAttr(obj+'.m_ty', l=False)
    cmds.setAttr(obj+'.m_tz', l=False)

    cmds.cutKey(obj, at='m_r', option="keys")
    cmds.setAttr(obj+'.m_r', l=False)
    cmds.setAttr(obj+'.m_rx', l=False)
    cmds.setAttr(obj+'.m_ry', l=False)
    cmds.setAttr(obj+'.m_rz', l=False)

    cmds.cutKey(obj, at='m_s', option="keys")
    cmds.setAttr(obj+'.m_s', l=False)
    cmds.setAttr(obj+'.m_sx', l=False)
    cmds.setAttr(obj+'.m_sy', l=False)
    cmds.setAttr(obj+'.m_sz', l=False)


    #--------------------Get Attributes Data
    attrValues = []
    for f in range(frameRange[0], frameRange[1]+1):
        temp = [f]
        for attr in activeChannels:
            temp.append( cmds.getAttr('%s.%s'%(obj,attr), t=f)[0] )

        attrValues.append(  tuple(temp)     )

    #print attrValues


    #Mapping channel
    curFrame = attrValues[0][0]
    frameMap = []
    mappingValues = []

    speed=float(speed)
    newValue = [curFrame, attrValues[0][1]  ]
    if createR:     newValue.append( attrValues[0][2] )
    if createS:     newValue.append( attrValues[0][3] )
    mappingValues.append( tuple(newValue)  )
    frameMap.append( (curFrame, curFrame) )
    simRate = []

    for index in range(1, len(attrValues)):
        disVector = tuple(  newom.MVector( attrValues[index][1] ) - newom.MVector( attrValues[index-1][1])  )
        if createR:
            rotDisVector = tuple(  newom.MVector( attrValues[index][2] ) - newom.MVector( attrValues[index-1][2])  )
        if createS:
            scaleDisVector = tuple( newom.MVector( attrValues[index][3]) - newom.MVector( attrValues[index-1][3])  )
        #print attrValues[index][1]
        #print disVector
        #dif = attrValues[index][1]- attrValues[index-1][1]
        distance = newom.MVector(disVector).length()
        try:    rate= speed/distance
        except(ZeroDivisionError):     rate = 0.0
        if distance > speed:
            divideCount = math.ceil( distance/speed )
            precent = 1.0/divideCount
            #print distance, divideCount, 'precent:',precent,'\n'
            #step = dif/insertCount
            #print values[index], int(insertCount), int(curFrame), ':', int(curFrame+insertCount)
            #curFrame+=insertCount
            for i in range(1, int( divideCount) ):
                curFrame +=1
                #newValue = (curFrame, values[index-1][1]+(step*i))
                value = tuple(\
                              newom.MVector( attrValues[index-1][1] ) + ( newom.MVector(disVector)*precent*i )\
                              )
                newValue = [ curFrame, value ]

                if createR:
                    rotValue = tuple(\
                                    newom.MVector( attrValues[index-1][2] ) + ( newom.MVector(rotDisVector)*precent*i )\
                                    )
                    newValue.append(rotValue)
                if createS:
                    scaleValue = tuple(\
                                      newom.MVector( attrValues[index-1][3] ) + ( newom.MVector(scaleDisVector)*precent*i )\
                                      )
                    newValue.append(scaleValue)

                #newValue = ( curFrame, value, rotValue )
                newValue = tuple( newValue )
                mappingValues.append(newValue)
                simRate.append( (curFrame, rate) )
                #print newValue
        curFrame +=1
        newValue = [curFrame, attrValues[index][1]  ]

        if createR:     newValue.append( attrValues[index][2] )

        if createS:     newValue.append( attrValues[index][3] )


        mappingValues.append(  tuple(newValue)  )
        #print newValue
        frameMap.append( (attrValues[index][0], curFrame) )
        simRate.append( (curFrame, rate) )



    #-----------------Set Mapping attributes----------------------------------
    cmds.setAttr('%s.%s'%(obj,'b_s' ), speed, lock=True)


    for f, value in frameMap:
        cmds.setKeyframe(obj, at='m_f', t=f, v=value)
        cmds.setKeyframe(obj, at='geoCacheTime', t=value, v=f)

    for f, value in simRate:
        cmds.setKeyframe(obj, at='simRate', t=f, v=value)





    for element in mappingValues:
        f = element[0]
        t = element[1]
        if 'tx' in activeAttrs: cmds.setKeyframe(obj, at='m_tx', t=f, v=t[0] )
        if 'ty' in activeAttrs: cmds.setKeyframe(obj, at='m_ty', t=f, v=t[1] )
        if 'tz' in activeAttrs: cmds.setKeyframe(obj, at='m_tz', t=f, v=t[2] )
        if createR:
            r = element[2]
            if 'rx' in activeAttrs: cmds.setKeyframe(obj,at='m_rx', t=f, v=r[0] )
            if 'ry' in activeAttrs: cmds.setKeyframe(obj,at='m_ry', t=f, v=r[1] )
            if 'rz' in activeAttrs: cmds.setKeyframe(obj,at='m_rz', t=f, v=r[2] )
        if createS:
            s = element[3]
            if 'sx' in activeAttrs: cmds.setKeyframe(obj,at='m_sx', t=f, v=s[0] )
            if 'sy' in activeAttrs: cmds.setKeyframe(obj,at='m_sy', t=f, v=s[1] )
            if 'sz' in activeAttrs: cmds.setKeyframe(obj,at='m_sz', t=f, v=s[2] )


    for attr in transformAttrs:
        if attr not in activeAttrs:
            value = cmds.getAttr('%s.%s'%(obj,attr) )
            mAttr = mappingAttrs[ transformAttrs.index(attr) ]
            if cmds.attributeQuery(mAttr, n=obj, exists=True):
                cmds.setAttr('%s.%s'%(obj,mAttr ), lock=False)
                cmds.cutKey(obj, at=mAttr, option="keys")
                cmds.setAttr('%s.%s'%(obj,mAttr ), value, lock=True)



    #-------------------------------------------test for deretimes

    if cmds.attributeQuery('t_t', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='test_t',  sn='t_t',  at='double3')
        cmds.addAttr(obj, ln='test_tx', sn='t_tx', p='test_t', at='doubleLinear')
        cmds.addAttr(obj, ln='test_ty', sn='t_ty', p='test_t', at='doubleLinear')
        cmds.addAttr(obj, ln='test_tz', sn='t_tz', p='test_t', at='doubleLinear')

    if cmds.attributeQuery('t_r', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='test_r',   sn='t_r', at='double3')
        cmds.addAttr(obj, ln='test_rx',  sn='t_rx', p='test_r', at='doubleAngle')
        cmds.addAttr(obj, ln='test_ry',  sn='t_ry', p='test_r', at='doubleAngle')
        cmds.addAttr(obj, ln='test_rz',  sn='t_rz', p='test_r', at='doubleAngle')

    if cmds.attributeQuery('test_s', n=obj, exists=True) == False:
        cmds.addAttr(obj, ln='test_s',   sn='t_s', at='double3')
        cmds.addAttr(obj, ln='test_sx',  sn='t_sx', p='test_s', at='double')
        cmds.addAttr(obj, ln='test_sy',  sn='t_sy', p='test_s', at='double')
        cmds.addAttr(obj, ln='test_sz',  sn='t_sz', p='test_s', at='double')



    cmds.cutKey(obj, at='t_t', option="keys")
    cmds.setAttr(obj+'.t_t', l=False)
    cmds.setAttr(obj+'.t_tx', l=False)
    cmds.setAttr(obj+'.t_ty', l=False)
    cmds.setAttr(obj+'.t_tz', l=False)

    cmds.cutKey(obj, at='t_r', option="keys")
    cmds.setAttr(obj+'.t_r', l=False)
    cmds.setAttr(obj+'.t_rx', l=False)
    cmds.setAttr(obj+'.t_ry', l=False)
    cmds.setAttr(obj+'.t_rz', l=False)

    cmds.cutKey(obj, at='t_s', option="keys")
    cmds.setAttr(obj+'.t_s', l=False)
    cmds.setAttr(obj+'.t_sx', l=False)
    cmds.setAttr(obj+'.t_sy', l=False)
    cmds.setAttr(obj+'.t_sz', l=False)


    oriFrame = cmds.keyframe(obj+'.m_f', query=True,tc=True)
    mapFrame = cmds.keyframe(obj+'.m_f', query=True,vc=True)
    cmds.cutKey(obj, at='t_t', option="keys")
    cmds.cutKey(obj, at='t_r', option="keys")
    cmds.cutKey(obj, at='t_s', option="keys")

    for attr in transformAttrs:
        if attr in activeAttrs:
            for index in range( len(oriFrame) ):
                attrIndex = transformAttrs.index(attr)
                mAttr = mappingAttrs[ attrIndex ]
                value = cmds.getAttr('%s.%s'%(obj, mAttr), t=mapFrame[index])

                tAttr = testAttrs[ attrIndex ]
                cmds.setKeyframe(obj, at=tAttr, t=oriFrame[index], v=value)
        else:
            attrIndex = transformAttrs.index(attr)
            mAttr = mappingAttrs[ attrIndex ]
            tAttr = testAttrs[ attrIndex ]
            value = cmds.getAttr('%s.%s'%(obj, mAttr))
            cmds.setAttr('%s.%s'%(obj,tAttr), value, l=True)





    #--------------------------------result mapped data on locator---------------------------------
    choiceTime01 = cmds.listConnections(obj+'.m_f', s=False, type='choice')
    if  choiceTime01 == None:
        choiceTime01 = cmds.createNode('choice', name='choiceTimer_DynCache')
        cmds.connectAttr('time1.outTime', choiceTime01+'.input[0]')
        cmds.connectAttr(obj+'.m_f', choiceTime01+'.input[1]')
    else:
       choiceTime01 = choiceTime01[0]

    choiceTime02 = cmds.listConnections(obj+'.geoCacheTime', s=False, type='choice')
    if  choiceTime02 == None:
        choiceTime02 = cmds.createNode('choice', name='choiceTimer_GeoCache')
        cmds.connectAttr('time1.outTime', choiceTime02+'.input[0]')
        cmds.connectAttr(obj+'.geoCacheTime', choiceTime02+'.input[1]')
    else:
       choiceTime02 = choiceTime02[0]

    choiceT = cmds.listConnections(obj+'.m_t', s=False, type='choice')
    if choiceT == None:
        choiceT = cmds.createNode('choice', name='choiceTranslate')
        cmds.connectAttr(obj+'.t_t', choiceT+'.input[0]')
        cmds.connectAttr(obj+'.m_t', choiceT+'.input[1]')
    else:
        choiceT = choiceT[0]

    choiceR = cmds.listConnections(obj+'.m_r', s=False, type='choice')
    if choiceR == None:
        choiceR = cmds.createNode('choice', name='choiceRotate')
        cmds.connectAttr(obj+'.t_r', choiceR+'.input[0]')
        cmds.connectAttr(obj+'.m_r', choiceR+'.input[1]')
    else:
        choiceR = choiceR[0]

    choiceS = cmds.listConnections(obj+'.m_s', s=False, type='choice')
    if choiceS == None:
        choiceS = cmds.createNode('choice', name='choiceScale')
        cmds.connectAttr(obj+'.t_s', choiceS+'.input[0]')
        cmds.connectAttr(obj+'.m_s', choiceS+'.input[1]')
    else:
        choiceS = choiceS[0]


    if cmds.listConnections(choiceTime01+'.output', s=False, type='transform') is None:
        testLoc = cmds.spaceLocator(name=obj+'_mappingTest')[0]
        cmds.addAttr(testLoc, ln='reTime', at='bool')
        for choiceNode in [choiceTime01, choiceTime02, choiceT, choiceR, choiceS]:
            try:    cmds.connectAttr(testLoc+'.reTime', choiceNode+'.selector')
            except:    pass
        cmds.addAttr(testLoc, ln='dyn_time', at='time' )
        cmds.addAttr(testLoc, ln='geo_time', at='time' )
        cmds.connectAttr(choiceTime01+'.output', testLoc+'.dyn_time')
        cmds.connectAttr(choiceTime02+'.output', testLoc+'.geo_time')
        cmds.connectAttr(choiceT+'.output', testLoc+'.translate')
        cmds.connectAttr(choiceR+'.output', testLoc+'.rotate')
        cmds.connectAttr(choiceS+'.output', testLoc+'.scale')
        
        
        
def timeScale( factor=3 ):
    '''{'del_path':'Edit/Keys/timeScale( factor=3 )ONLYSE',
'usage':'$fun( factor=3 )',
}
'''
    obj = cmds.ls(sl=True)
    obj = obj[0]
    start = int( cmds.playbackOptions(q=True, min=True) )
    end = int( cmds.playbackOptions(q=True, max=True) )
    attrs = ( 'cus_time', 'cus_time02', 'cus_emitRate')
    
    for att in attrs:
        if cmds.attributeQuery(att, n=obj, exists=True):
            cmds.cutKey(obj, at=att, option='keys')
        else:
            cmds.addAttr( obj, longName=att, at='time')


    factor = int( factor )
    for f in range(start, end+2 ):
        value = ((f-start)*factor)+start + 1
        #cmds.setKeyframe(obj, at='cus_oriTime', t=f,  v=f, ott='step' )
        cmds.setKeyframe(obj, at='cus_time', t=value,  v=f, ott='step' )
        cmds.setKeyframe(obj, at='cus_emitRate', t=value, v=1)
        cmds.setKeyframe(obj, at='cus_emitRate', t=value+factor-.01, v=0)
        cmds.setKeyframe( obj, at ='cus_time02', t=f, v=value+factor-1, ott='step')



def centerPivot_anim():
    '''{'path':'Modify/Transform/centerPivot_anim( )',
'icon':':/transform.svg',
'tip':'将关键帧物体的坐标轴放到物体中心',
'usage':"""
#对选择的动画的物体进行centerPivot操作
$fun( )"""
}
'''
    objs = cmds.ls(sl=True, l=True, type='transform')#cmds.listRelatives( cmds.ls(sl=True, l=True)[0], type='transform', f=True)
    locs = {}
    for obj in objs:
        #shortName = cmds.ls( obj, shortNames=True )[0]
        loc = cmds.spaceLocator( n=obj+'_tempTrans' )[0]
        initPos = cmds.objectCenter( obj )
        cmds.setAttr( loc+'.t', initPos[0], initPos[1], initPos[2], type='double3' )
        cmds.parentConstraint( obj, loc, maintainOffset=True)
        locs[obj]= loc

    minTime, maxTime = cmds.playbackOptions( q=True, min=True), cmds.playbackOptions( q=True,max=True)
    attrs = ('tx','ty','tz','rx','ry','rz')

    cmds.bakeResults(locs.values(), at=attrs, t=(minTime,maxTime),sampleBy=1)

    animCurves = []
    for obj in objs:
        for attr in attrs:
            animCurve = cmds.listConnections('%s.%s'%(obj,attr),d=False)
            if animCurve:
                animCurves.extend( animCurve )

    if  animCurves:
        cmds.delete( animCurves )
    cmds.xform( objs, centerPivots=True)
    cmds.makeIdentity(objs, apply=True, t=True)
    qm.unfreeze(objs)
    for obj in objs:
        for attr in attrs:
            animCurve = cmds.listConnections('%s.%s'%(locs[obj],attr),d=False)
            if animCurve:
                cmds.connectAttr( animCurve[0]+'.output', '%s.%s'%(obj,attr) )
    cmds.delete( locs.values() )
    

def bakeTransform(separate=False, keepOriginal=True):
    '''{'path':'Edit/Keys/bakeTransform( )',
'html':True,
'tip':'将特定的物体的烘焙关键帧',
'icon':':/transform.svg',
'usage':"""
#对选择的物体进行bake关键帧的操作
$fun( separate=False )"""
}
'''
    if separate:
        cachedObj = checkArg( nodeType='mesh', tryToShape=True )
        originalObj = cmds.listRelatives( cachedObj, parent=True, f=True)
         
        cmds.constructionHistory(toggle=False)
        #cachedObj = cmds.ls(sl=True,l=True)[0]
        #sepratate cachedObj
        minTime = int( cmds.playbackOptions(q=True,min=True) )
        cmds.currentTime(minTime)
        cachedObj = cmds.duplicate( cachedObj, rr=True, renameChildren=True, un=True)
        cachedObj = cmds.listRelatives( cachedObj, shapes=True, f=True)[0]
        temp = cmds.polySeparate(cachedObj, ch=True)[0]
        rbdGrp = cmds.listRelatives(temp, p=True, f=True)[0]
        childGrp = cmds.duplicate(rbdGrp,rr=True)[0]
        parentList = cmds.listRelatives(rbdGrp, type='transform', f=True)
        childList = cmds.listRelatives(childGrp, type='transform', f=True)
        cmds.delete(cmds.listRelatives(childGrp,f=True),ch=True)
    
    
        forRemove = []
        for obj in parentList:
            meshNode = cmds.listRelatives(obj,type='mesh', f=True)
            if meshNode == [] or cmds.getAttr(meshNode[0]+'.intermediateObject') == 1:
                forRemove.append(obj)
        if obj in forRemove:
            parentList.remove(obj)
    
    
        forRemove = []
        for obj in childList:
            meshNode = cmds.listRelatives(obj,type='mesh', f=True)
            if meshNode == [] or cmds.getAttr(meshNode[0]+'.intermediateObject') == 1:
                forRemove.append(obj)
        if obj in forRemove:
            childList.remove(obj)
        cmds.delete(forRemove)
    
    
        qm.unfreeze(childList)
    
        folGrp = cmds.group(em=True,n=rbdGrp+'_FoGrp')
        cons = []
        for papa in parentList:
            index = parentList.index(papa)
            child = childList[index]
            meshShape = cmds.listRelatives(papa, type='mesh', f=True)[0]
    
            faceCount = cmds.polyEvaluate(papa,f=True)-1
            if faceCount > 10:
                faceCount = 10
    
            newFace = '%s.f[0:%s]'%(papa, faceCount)
            #cmds.select(newFace)
            #mel.eval('polySplitTextureUV')
    
            #mel.eval('PolySelectConvert 4')
            #map = cmds.ls(sl=True)
    
            #cmds.polyNormalizeUV( map, normalizeType=0, preserveAspectRatio=False)
    
            #cmds.polyEditUV(map,pu=.5, pv=.5, su=2, sv=2)
            meshShape = cmds.listRelatives(papa, type='mesh', f=True)[0]
            faceZero = '%s.f[0]'%( meshShape )
            cmds.polyForceUV( faceZero, unitize=True)
            
            
            
            #create follicle and set attribute
            folShape = cmds.createNode("follicle")
    
            folTransform = cmds.listRelatives(folShape, p=True,f=True)[0]
            cmds.setAttr(folTransform+'.intermediateObject',1)
    
            cmds.setAttr(folShape + '.parameterU', .5, l=True)
            cmds.setAttr(folShape + '.parameterV', .5, l=True)
            cmds.setAttr(folShape + ".simulationMethod", 0)
            cmds.setAttr(folShape + ".collide", 0)
            cmds.setAttr(folShape + ".degree", 1)
            cmds.setAttr(folShape + ".sampleDensity", 0)
    
            #connection follicles
            cmds.connectAttr(meshShape+'.worldMatrix[0]', folShape + '.inputWorldMatrix', f=True)
            cmds.connectAttr(meshShape+'.outMesh', folShape + '.inputMesh', f=True)
            cmds.connectAttr(folShape + '.outRotate', folTransform+'.rotate', f=True)
            cmds.connectAttr(folShape + '.outTranslate', folTransform+'.translate', f=True)
    
            parentConNode =  cmds.parentConstraint( folTransform, child, mo=True )[0]
            cons.append( parentConNode )
    
            cmds.parent( folTransform,  folGrp)
    
        minTime = int( cmds.playbackOptions(q=True,min=True) )
        maxTime = int( cmds.playbackOptions(q=True,max=True) )
        cmds.bakeResults(childList,simulation=True, t=(minTime,maxTime),sampleBy=1,\
                        disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, \
                        bakeOnOverrideLayer=False,at=['tx','ty','tz','rx','ry','rz'])
    
        cmds.delete([folGrp,rbdGrp])        
        cmds.delete(cmds.listRelatives(childGrp,f=True),ch=True)
        if not keepOriginal:
            cmds.delete( originalObj )
    
        cmds.constructionHistory(toggle=True)
        
    else:        
        objs = cmds.ls(sl=True, exactType='transform', l=True)      
        objsData = {}
        cmds.constructionHistory(toggle=False)
        for obj in objs:
            keyObj = cmds.duplicate(obj,rr=True)[0]
            keyObj = cmds.parent( keyObj, world=True)[0]
            cmds.xform(keyObj, centerPivots=True)
            qm.unfreeze( keyObj )
            
            
            meshShape = cmds.listRelatives(obj, type='mesh', f=True)[0]
            faceZero = '%s.f[0]'%( obj )
            cmds.polyForceUV( faceZero, unitize=True)
            #cmds.polyNormalizeUV( faceZero, normalizeType=0, preserveAspectRatio=False)
            
            #create follicle and set attribute
            folShape = cmds.createNode("follicle")
        
            folTransform = cmds.listRelatives(folShape, p=True,f=True)[0]
            cmds.setAttr(folTransform+'.intermediateObject',1)
        
            cmds.setAttr(folShape + '.parameterU', .5, l=True)
            cmds.setAttr(folShape + '.parameterV', .5, l=True)
            cmds.setAttr(folShape + ".simulationMethod", 0)
            cmds.setAttr(folShape + ".collide", 0)
            cmds.setAttr(folShape + ".degree", 1)
            cmds.setAttr(folShape + ".sampleDensity", 0)
        
            #connection follicles
            cmds.connectAttr(meshShape+'.worldMatrix[0]', folShape + '.inputWorldMatrix', f=True)
            cmds.connectAttr(meshShape+'.outMesh', folShape + '.inputMesh', f=True)
            cmds.connectAttr(folShape + '.outRotate', folTransform+'.rotate', f=True)
            cmds.connectAttr(folShape + '.outTranslate', folTransform+'.translate', f=True)
        
            parentConNode =  cmds.parentConstraint( folTransform, keyObj, mo=True )[0]
            objsData[obj] = [keyObj, folTransform, parentConNode]
        minTime = int( cmds.playbackOptions(q=True,min=True) )
        maxTime = int( cmds.playbackOptions(q=True,max=True) )
        toBake = [t[0] for t in objsData.itervalues() ]
        cmds.bakeResults(toBake,simulation=True, t=(minTime,maxTime),sampleBy=1,\
                        disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, \
                        bakeOnOverrideLayer=False,at=['tx','ty','tz','rx','ry','rz'])
        
        
        toDelete = []
        for helper in objsData.itervalues():
            temp = [t for t in helper[1:] if cmds.objExists(t) ]
            if temp:
                toDelete.extend( temp )
        cmds.delete( toDelete )
        
        if not keepOriginal:
            toDelete = [t for t in objsData.keys() if cmds.objExists(t) ]
            cmds.delete( toDelete )
        
        newObjs = [t[0] for t in objsData.values() if cmds.objExists(t[0]) ]
        newObjsGrp = cmds.group( empty=True, world=True, name='bakeTransform_#')
        cmds.parent( newObjs, newObjsGrp)
        
        cmds.constructionHistory(toggle=True)