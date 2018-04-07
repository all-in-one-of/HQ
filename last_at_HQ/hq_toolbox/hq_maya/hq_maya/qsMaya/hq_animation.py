# -*- coding: utf-8 -*-
import os




import maya.cmds as cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as newom
import math
import qsMaya as qm



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
        
