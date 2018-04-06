import maya.cmds as mc
allJoints=[u'Hips', u'Spine', u'Spine1', u'Spine2', u'Spine3', u'Neck', u'Neck1', u'Head', u'Head_End', u'Chin', u'Chin01', u'Tongue01', u'Tongue02', u'Tongue03', u'Tongue04', u'Tongue05', u'Tongue06', u'LeftShoulder', u'LeftArm', u'LeftArmRoll', u'LeftForeArm', u'LeftForeArmRoll', u'LeftHand', u'Leftjoint', u'LeftHandThumb1', u'LeftHandThumb2', u'LeftHandThumb3', u'LeftHandThumb4', u'LeftHandIndex1', u'LeftHandIndex2', u'LeftHandIndex3', u'LeftHandIndex4', u'LeftHandMiddle1', u'LeftHandMiddle2', u'LeftHandMiddle3', u'LeftHandMiddle4', u'LeftHandRing1', u'LeftHandRing2', u'LeftHandRing3', u'LeftHandRing4', u'LeftHandPinky1', u'LeftHandPinky2', u'LeftHandPinky3', u'LeftHandPinky4', u'RightShoulder', u'RightArm', u'RightArmRoll', u'RightForeArm', u'RightForeArmRoll', u'RightHand', u'Rightjoint', u'RightHandThumb1', u'RightHandThumb2', u'RightHandThumb3', u'RightHandThumb4', u'RightHandIndex1', u'RightHandIndex2', u'RightHandIndex3', u'RightHandIndex4', u'RightHandMiddle1', u'RightHandMiddle2', u'RightHandMiddle3', u'RightHandMiddle4', u'RightHandRing1', u'RightHandRing2', u'RightHandRing3', u'RightHandRing4', u'RightHandPinky1', u'RightHandPinky2', u'RightHandPinky3', u'RightHandPinky4', u'LeftHips_Dummy', u'LeftUpLeg', u'LeftUpLegRoll', u'LeftLeg', u'LeftLegRoll', u'LeftFoot', u'LeftToeBase', u'LeftToes_End', u'RightHips_Dummy', u'RightUpLeg', u'RightUpLegRoll', u'RightLeg', u'RightLegRoll', u'RightFoot', u'RightToeBase', u'RightToes_End']
leftJoints=[]
rightJoints=[]
centerJoints=[]
for x in allJoints:
    if 'Left' in x:
        leftJoints.append(x)
    elif 'Right' in x:
        rightJoints.append(x)
    else:
        centerJoints.append(x)
for one in leftJoints:
    anCurves=mc.listConnections(one,type='animCurve')
    if anCurves:
        for oneCurve in anCurves:
            Joint=oneCurve.split('_')[0]
            Attr=oneCurve.split('_')[1]
            mc.connectAttr(oneCurve.replace('Left','Right')+'.output',Joint+'.'+Attr,f=1)
for one in rightJoints:
    anCurves=mc.listConnections(one,type='animCurve')
    if anCurves:
        for oneCurve in anCurves:
            Joint=oneCurve.split('_')[0]
            Attr=oneCurve.split('_')[1]
            mc.connectAttr(oneCurve.replace('Right','Left')+'.output',Joint+'.'+Attr,f=1)
for one in centerJoints:
    anCurves=mc.listConnections(one,type='animCurve')
    if anCurves:
        for oneCurve in anCurves:
            if '_translateX' in oneCurve or '_rotateY' in oneCurve or '_rotateZ' in oneCurve:
                v=mc.keyframe( oneCurve,query=True, valueChange=True);
                t=mc.keyframe( oneCurve,query=True, timeChange=True);
                for i in t:
                    mc.setKeyframe( oneCurve, time=i,value=v[t.index(i)]*-1);
for one in allJoints:
    anCurves=mc.listConnections(one,type='animCurve')
    if anCurves:
        for oneCurve in anCurves:
            if 'Left' in oneCurve or 'Right' in oneCurve:
                mc.rename(oneCurve,'tmp_'+oneCurve)
for one in allJoints:
    anCurves=mc.listConnections(one,type='animCurve')
    if anCurves:
        for oneCurve in anCurves:
            if 'Left' in oneCurve:
                mc.rename(oneCurve,oneCurve.replace('Left','Right')[4:])
            if 'Right' in oneCurve:
                mc.rename(oneCurve,oneCurve.replace('Right','Left')[4:])