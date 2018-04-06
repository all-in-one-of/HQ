#----------------w07 Start
presetsFolder = mel.eval('getenv "HOME"') + '/sq/scripts/sqFX/maya/emfxClouds/cloudsPresets/'
#------------------------Utilities-------------------
def getUniqueName(baseName='group_'):
    get=True
    i=0
    while get:
        if cmds.objExists('%s%04d'%(baseName,i) ):
            i += 1
        else:
            get=False
    return '%s%04d'%(baseName,i)

def emfx_getUniquePresetName( cloudPresetPath =presetsFolder):
    cloudPresetFiles = os.listdir( cloudPresetPath )
    if cloudPresetFiles:
        i = 1
        got = True
        while got:
            if 'Cloud_%03d.py'%(i) not in cloudPresetFiles:
                return 'Cloud_%03d'%(i)
                got=False
            else:
                i += 1
    else:
        return 'Cloud_001'
#--------------------------------------------

def cmd_getCloudGrp():     
    cloudGrp = cmds.ls(sl=True)
    a,b,c,d=False,False,False,False
    if cloudGrp:
        cloudGrp=cloudGrp[0]
        objs = cmds.listRelatives(cloudGrp)
        layoutGrp, sphereGrp, particleNode, fluidNode= '', '', '', ''
        #Get layoutGrp from children of cloudGrp
        for obj in objs:
            if obj.find('layoutGrp')!=-1:
                a = True
                layoutGrp = obj
                cmds.textFieldButtonGrp('uiGetLayoutGrp', e=True, text=layoutGrp)                
                break
        
        #Get sphereGrp from children of cloudGrp
        for obj in objs:
            if obj.find('sphereGrp')!=-1:
                b = True
                sphereGrp = obj
                cmds.textFieldButtonGrp('uiGetSphereGrp', e=True, text=sphereGrp)                
                break

        #Get nParticleNode from children of cloudGrp
        temp = cmds.listRelatives( cloudGrp, ad=True, type='nParticle')
        if temp:
            c=True
            particleNode = temp[0]
            cmds.textFieldButtonGrp('uiGetParticleNode', e=True, text=particleNode)
        
        #Get FluidShape Node from children of cloudGrp
        temp = cmds.listRelatives( cloudGrp, ad=True, type='fluidShape')
        if temp:
            d=True
            fluidNode = temp[0]
            cmds.textFieldButtonGrp('uiGetFluidNode', e=True, text=fluidNode)
            
    if a or b or c or d:
        cmds.textField('uiCloudGrpName', e=True, text=cloudGrp)

def cmd_createCloudGrp():
    cloudGrp = cmds.group(em=True,name=getUniqueName('CLOUD_'), w=True )
    
    #Create Layout Group
    cmds.parent( emfx_createLayoutGrp(),  cloudGrp) 
    
    #Create Spheres Group   
    sphereGrp = cmds.createNode('transform', name=getUniqueName('sphereGrp_'), p=cloudGrp)
    
    #Create nParticles Node
    cmds.parent(emfx_createFluidNode(), cloudGrp)
    cmds.select(cloudGrp)
    cmd_getCloudGrp()

def cmd_disButtons(uiName):
    temp = cmds.textFieldButtonGrp(uiName, q=True, text=True )
    if temp and cmds.objExists(temp):
        value = False if cmds.getAttr(temp+'.visibility') else True
        cmds.setAttr(temp+'.visibility', value)


def cmd_selButtons(uiName):
    temp = cmds.textFieldButtonGrp(uiName, q=True, text=True )
    if cmds.objExists(temp):
        cmds.select(temp)



def cmd_getLayoutGrp():
    sel = cmds.ls(sl=True, type='transform')
    value = '' if sel==[] else sel[0]
    cmds.textFieldButtonGrp('uiGetLayoutGrp', e=True, text=value )
    

def emfx_createLayoutGrp():
    layoutGrp = cmds.createNode('transform', name=getUniqueName('layoutGrp_'))
    for item in cmds.popupMenu('uiPopupMenuCreateLayoutGrp', q=True, itemArray=True):
        if cmds.menuItem(item ,q=True, radioButton=True):
            layoutStyle = cmds.menuItem(item ,q=True, label=True)
            break
    both = False
    height=.7
    print layoutStyle
    
    if layoutStyle=='Up':
        heightList=[-.7]
    elif layoutStyle=='Down':
        heightList=[.7]
    else:
        heightList = [.7,-.7]
    
    transformData=[]
    for height in heightList:
        totalH = 5*height
        for i in range(1,6):
            yPos = height*i
            xzPos = yPos*2
            boxData=[ random.uniform(-yPos*.75, yPos*.75), yPos-totalH, random.uniform(-yPos*.75, yPos*.75) ]
            boxData.extend( [yPos*2, random.uniform(height*1.5,height*3) , yPos*2] )        
            transformData.append( boxData )
    
    '''for data in transformData:
        layoutBox = cmds.polyCube(ch=False, n=getUniqueName('layoutBox_') )[0]
        cmds.polyColorPerVertex(layoutBox, r=.57,g=0.66,b=1,a=0.75, colorDisplayOption=True)
        cmds.setAttr(layoutBox+'.t', data[0], data[1], data[2], type='double3')
        cmds.setAttr(layoutBox+'.s', data[3], data[4], data[5], type='double3')
    transformData = ([(0,-1.75,0),  (5, 2.5, 5)],
                    [(1.7, -.6, 1.8), (3.9, 2, 3.9)],
                    [(-.6, -.6, -2),  (5.5, 2, 3.9)],
                    [(0, .3, -.1),  (3, 2.9, 3.6)],
                    [(.2, 2, -.1), (1.9, 1, 2.3)]
                   )'''
    for data in transformData:
        layoutBox = cmds.polyCube(ch=False, n=getUniqueName('layoutBox_') )[0]
        cmds.polyColorPerVertex(layoutBox, r=.57,g=0.66,b=1,a=0.75, colorDisplayOption=True)
        cmds.setAttr(layoutBox+'.t', data[0], data[1], data[2], type='double3')
        cmds.setAttr(layoutBox+'.s', data[3], data[4], data[5], type='double3')    
        cmds.parent(layoutBox, layoutGrp)
    return layoutGrp
   

def cmd_createLayoutGrp():
    layoutGrp = cmds.textFieldButtonGrp('uiGetLayoutGrp', q=True, text=True)
    if layoutGrp=='' or cmds.objExists(layoutGrp)==False:
        layoutGrp = emfx_createLayoutGrp()
        cmds.textFieldButtonGrp('uiGetLayoutGrp', e=True, text=layoutGrp)

def cmd_getSphereGrp():
    sel = cmds.ls(sl=True, type='transform')
    value = '' if sel==[] else sel[0]
    cmds.textFieldButtonGrp('uiGetSphereGrp', e=True, text=value )


def emfx_getVoxelSize(obj, maxRes):
    bbox = cmds.exactWorldBoundingBox(obj, ignoreInvisible=False)
    sizeLi = [math.fabs(bbox[3]-bbox[0]), math.fabs(bbox[4]-bbox[1]), math.fabs(bbox[5]-bbox[2])]
    sizeLi.sort()
    divSize = sizeLi[2]/maxRes
    if divSize > sizeLi[0]/4:
        divSize = sizeLi[0]/4
    return divSize

def cmd_getVoxelSize():
    layoutGrp = cmds.textFieldButtonGrp('uiGetLayoutGrp', q=True, text=True)
    maxRes = cmds.intFieldGrp("uiMaxAxisRes", q=True, v1=True)
    divSize = emfx_getVoxelSize(layoutGrp, maxRes)
    
    cmds.floatFieldGrp("uiRandomPos", e=True, v1=divSize)

def floatIterator(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def positionFromBBox(objects, maxRes):
    
    divSize = emfx_getVoxelSize(objects, maxRes)
    
    halfVoxelDist = .5 * divSize
    
    temp = cmds.exactWorldBoundingBox(objects, ignoreInvisible=False)
    minPoint = temp[:3]
    minPointX, minPointY, minPointZ = minPoint[0]+halfVoxelDist, minPoint[1]+halfVoxelDist, minPoint[2]+halfVoxelDist
    maxPoint = temp[3:]
    maxPointX, maxPointY, maxPointZ = maxPoint[0]+halfVoxelDist, maxPoint[1]+halfVoxelDist, maxPoint[2]+halfVoxelDist
    
    boxes = cmds.listRelatives(objects, f=True, ad=True, type='surfaceShape')
    if boxes==None:
        bboxArray=[
                   newom.MBoundingBox( newom.MPoint(minPoint), 
                                       newom.MPoint(maxPoint) 
                                       ) 
                   ]
    else:
        bboxForSort = []    
        for box in boxes:
            temp = cmds.exactWorldBoundingBox(box, ignoreInvisible=False)
            #length = newom.MPoint( temp[:3] ).distanceTo( newom.MPoint(temp[3:]) )        
            minTemp = newom.MPoint( temp[:3] )
            maxTemp = newom.MPoint( temp[3:] )
            objBBox = newom.MBoundingBox(minTemp, maxTemp)        
            bboxForSort.append(
                        (minTemp.distanceTo( maxTemp ), objBBox )
                        )
        bboxForSort.sort()
        bboxForSort.reverse()
        bboxArray = []
        for bbox in bboxForSort:
            bboxArray.append( bbox[1] )
        
    voxels = []
    for xCoord in floatIterator( minPointX, maxPointX, divSize ):
        for yCoord in floatIterator( minPointY, maxPointY, divSize ):
            for zCoord in floatIterator( minPointZ, maxPointZ, divSize ):
                for bound in bboxArray:
                    if bound.contains( newom.MPoint(xCoord,yCoord,zCoord) ):
                        voxels.append( [xCoord,yCoord,zCoord] )
                        break

    '''inBBoxes = []
    tempVoxels = voxels[:]
    boxes = cmds.listRelatives(objects, f=True, type='transform')
    for box in boxes:
        temp = cmds.exactWorldBoundingBox(box, ignoreInvisible=False)
        minPoint = newom.MPoint( temp[:3] )
        maxPoint = newom.MPoint( temp[3:] )
        objBBox = newom.MBoundingBox(minPoint, maxPoint)
        #containedList = []
        for pos in tempVoxels:
            if objBBox.contains( newom.MPoint(pos) ):
                inBBoxes.append( pos )
                voxels.pop( voxels.index(pos) )
                #containedList.append( voxels.index(pos) )
        tempVoxels = voxels[:]'''    
    return voxels

def positionFromMesh(object, maxRes):
    
    divSize = emfx_getVoxelSize(object, maxRes)
    halfVoxelDist = .5 * divSize
    
    
    temp = cmds.exactWorldBoundingBox(object, ignoreInvisible=False)
    minPoint = temp[:3]
    minPointX, minPointY, minPointZ = minPoint[0]+halfVoxelDist, minPoint[1]+halfVoxelDist, minPoint[2]+halfVoxelDist
    maxPoint = temp[3:]
    maxPointX, maxPointY, maxPointZ = maxPoint[0]+halfVoxelDist, maxPoint[1]+halfVoxelDist, maxPoint[2]+halfVoxelDist
    
    
    bbox = cmds.exactWorldBoundingBox(object, ignoreInvisible=False)
    xDiv = math.fabs(bbox[3]-bbox[0])  /divSize
    yDiv = math.fabs(bbox[4]-bbox[1])  /divSize
    zDiv = math.fabs(bbox[5]-bbox[2])  /divSize
    
    meshs = newom.MSelectionList()
    meshs.add( object )
    meshDagPath = meshs.getDagPath(0)
    meshFn = newom.MFnMesh(meshDagPath)
    meshAcceleration = meshFn.uniformGridParams( int(xDiv), int(yDiv), int(zDiv) )
    
    voxelsInMesh = []
    rayDirection = newom.MFloatVector( 0, -1, 0 )
    for xCoord in floatIterator( minPointX, maxPointX, divSize ):
        for yCoord in floatIterator( minPointY, maxPointY, divSize ):
            for zCoord in floatIterator( minPointZ, maxPointZ, divSize ):
                raySource=newom.MFloatPoint( [xCoord,yCoord,zCoord] )
                hitPoints = meshFn.allIntersections(raySource,
                                                    rayDirection,
                                                    newom.MSpace.kWorld,
                                                    9999.0,
                                                    False,
                                                    accelParams=meshAcceleration
                                                    )[0]
                if len(hitPoints)%2 == 1:
                    voxelsInMesh.append( raySource )
    meshFn.clearGlobalIntersectionAcceleratorInfo()    
    return voxelsInMesh


def emfx_createSphereFromVoxels(voxelsPos, numberSphere, randPos):    
    
    #divSize = cmds.floatFieldGrp("uiMaxAxisRes", q=True, v1=True)    
    #voxelsPos = positionFromBBox(layoutGrp, divSize)
    rRange = cmds.floatFieldGrp("uiRandRadius", q=True, v=True)
    
    spherePapa = cmds.textFieldButtonGrp('uiGetSphereGrp', q=True, text=True )
    
    
    if spherePapa=='' or cmds.objExists(spherePapa)==False:
        spherePapa = cmds.createNode('transform', name=getUniqueName('sphereGrp_') )
        #cloudGrp = cmds.textField('uiCloudGrpName', q=True, text=True)
        #if cloudGrp != '' and cmds.objExists(cloudGrp)==True:
            #cmds.parent(spherePapa, cloudGrp)        
    
    numberVoxels = len(voxelsPos)-1
    for i in range(numberSphere):
        numberVoxels = len(voxelsPos)-1
        if numberVoxels < 1:
            break
        rIndex = random.randint(0, numberVoxels)
    
        randedPos = (voxelsPos[rIndex][0]+random.uniform(-randPos, randPos),
                     voxelsPos[rIndex][1]+random.uniform(-randPos, randPos),
                     voxelsPos[rIndex][2]+random.uniform(-randPos, randPos)
                     )
        
        randedRad = random.uniform(rRange[0], rRange[1])
        sphereName = cmds.sphere(axis=[0,1,0], ch=False)[0]
        cmds.setAttr(sphereName+'.s', randedRad, randedRad, randedRad, type='double3')
        cmds.setAttr(sphereName+'.t', randedPos[0],randedPos[1],randedPos[2], type='double3')
        cmds.parent(sphereName, spherePapa)
        voxelsPos.pop(rIndex)
    return spherePapa


def cmd_createSpheres():
    import time
    startTime = time.time()
    if cmds.menuItem('uiCreateSpheresModel', q=True, checkBox=True):
        parShape = cmds.textFieldButtonGrp('uiGetParticleNode', q=True, text=True)
        if parShape!='' and cmds.objExists(parShape) and cmds.objectType(parShape)=='nParticle':
            #Get Spheres Parent
            spherePapa = cmds.textFieldButtonGrp('uiGetSphereGrp', q=True, text=True )   
            if spherePapa=='' or cmds.objExists(spherePapa)==False:
                spherePapa = cmds.createNode('transform', name=getUniqueName('sphereGrp_') )
            
            #Get Particles Position
            spheresPos = []
            poses = cmds.getParticleAttr(parShape, at='position', array=True )
            for i in range(0,len(poses),3):
                spheresPos.append( [ poses[i],poses[i+1],poses[i+2] ] ) 
            
            #Get Particles Radius
            if cmds.attributeQuery('radiusPP', node=parShape, exists=True):
                radiuses = cmds.getParticleAttr(parShape, at='radiusPP', array=True)
            else:    
                radius = cmds.getAttr(parShape+'.radius')
                parCount = cmds.getAttr(parShape+'.count')
                radiuses = [radius for i in range(parCount)]
                
            #Create Spheres
            for i in range(len(spheresPos)):
                sphereName = cmds.sphere( axis=[0,1,0], ch=False)[0]
                cmds.setAttr(sphereName+'.s', radiuses[i], radiuses[i], radiuses[i], type='double3')
                cmds.setAttr(sphereName+'.t', spheresPos[i][0],spheresPos[i][1],spheresPos[i][2], type='double3')
                cmds.parent(sphereName, spherePapa)
            cmds.textFieldButtonGrp('uiGetSphereGrp', e=True, text=spherePapa)
               
            
    else:
        samplingMethod = cmds.optionMenu( 'uiSamplingMethod', q=True, select=True)    
        layoutGrp = cmds.textFieldButtonGrp('uiGetLayoutGrp', q=True, text=True)
        maxRes = cmds.intFieldGrp("uiMaxAxisRes", q=True, v1=True)
        if maxRes<10:   maxRes = 10
        if maxRes>150: maxRes = 150
        
        if samplingMethod==1:
            voxelsPos = positionFromBBox(layoutGrp, maxRes)
        else: #samplingMethod==2:
            boxes = cmds.listRelatives(layoutGrp, ad=True, f=True, type='mesh')
            
            #Remove intermediate Object Mehs form boxes        
            if boxes:
                temp = boxes[:]
                for box in temp:
                    if cmds.getAttr(box+'.intermediateObject'):
                        boxes.pop( boxes.index( box ) )
            
            
            if len(boxes) > 1:
                forBoolObjs = cmds.duplicate(boxes)
                cmds.parent(forBoolObjs, w=True)
                booledObj = forBoolObjs[0]
                forBoolObjs.pop(0)
                for obj in forBoolObjs:
                    booledObj = cmds.polyBoolOp(booledObj, obj, op=1, ch=False )[0]
            else:
                booledObj = boxes[0]        
            voxelsPos = positionFromMesh(booledObj, maxRes)
            if len(boxes)>1:
                cmds.delete(booledObj)
        
        numberSphere = cmds.intFieldGrp("uiNumberSpheres", q=True, v1=True)
        randPos = cmds.floatFieldGrp("uiRandomPos", q=True, v1=True)*.5
        sphereGrp = emfx_createSphereFromVoxels(voxelsPos, numberSphere, randPos)    
        cmds.textFieldButtonGrp('uiGetSphereGrp', e=True, text=sphereGrp)
    cmds.menuItem('uiCreateSpheresModel', e=True, checkBox=False)
    print 'Used time(sec): ',time.time() - startTime


def cmd_getParticleNode():
    sel = cmds.ls(sl=True)
    value = ''    
    if sel:
        parShapes = cmds.ls(sel, type='nParticle' )
        if parShapes ==[]:
            parShapes = cmds.listRelatives(sel, type='nParticle')
        
        value = parShapes[0] if parShapes else ''
        
    cmds.textFieldButtonGrp('uiGetParticleNode', e=True, text=value )
    


def emfx_createNewParNode():
    temp = cmds.nParticle(name = getUniqueName('cloud_emitter_') )
    parShape = temp[1]
    
    cmds.setAttr(parShape+".particleRenderType",4);
    cmds.setAttr(parShape+".ignoreSolverGravity",1);
    cmds.setAttr(parShape+".selfCollide",0);
    cmds.setAttr(parShape+".collide", 0);
    cmds.setAttr(parShape+".enableSPH",0);
    cmds.setAttr(parShape+".conserve",0);
    cmds.setAttr(parShape+".opacity",1);
    cmds.setAttr(parShape+".template",1);
    cmds.addAttr(parShape,ln='radiusPP0', dt='doubleArray')
    cmds.addAttr(parShape,ln='radiusPP', dt='doubleArray')
    return temp


def emFx_getSpheresDistane():
    layoutGrp = cmds.textFieldButtonGrp('uiGetLayoutGrp', q=True, text=True)
      
    boxes = cmds.listRelatives(layoutGrp, ad=True, f=True, type='mesh')
    #Remove intermediate Mesh
    if boxes:
        temp = boxes[:]
        for box in temp:
            if cmds.getAttr(box+'.intermediateObject'):
                boxes.pop( boxes.index( box ) )
                
    if len(boxes) > 1:
        forBoolObjs = cmds.duplicate(boxes)
        cmds.parent(forBoolObjs, w=True)
        booledObj = forBoolObjs[0]
        forBoolObjs.pop(0)
        for obj in forBoolObjs:
            booledObj = cmds.polyBoolOp(booledObj, obj, op=1, ch=False )[0]
    else:
        booledObj = boxes[0]    
    
    spheres = cmds.listRelatives( cmds.textFieldButtonGrp('uiGetSphereGrp', q=True, text=True), type='transform')
    if spheres:
        posDistance = []
        meshs = newom.MSelectionList()
        meshs.add( booledObj )
        meshDagPath = meshs.getDagPath(0)
        meshFn = newom.MFnMesh(meshDagPath)
        for sph in spheres:
            pos = cmds.objectCenter( sph )
            posDistance.append(newom.MPoint(pos).distanceTo(
                                    meshFn.getClosestPoint( newom.MPoint( pos ), newom.MSpace.kWorld)[0]
                                                            )
                               )
        cmds.delete(booledObj)
        return posDistance
    else:
        return False


def cmd_clearState():
    parShape = cmds.textFieldButtonGrp('uiGetParticleNode', q=True, text=True)
    if parShape and cmds.objectType(parShape)=='nParticle':
        mel.eval('clearParticleStartState %s'%(parShape) )

def cmd_saveState():
    parShape = cmds.textFieldButtonGrp('uiGetParticleNode', q=True, text=True)
    if parShape and cmds.objectType(parShape)=='nParticle':
        cmds.saveInitialState( parShape )


def cmd_addParticles():
    sphereGrp = cmds.textFieldButtonGrp('uiGetSphereGrp', q=True, text=True)
    if sphereGrp=='' or cmds.objExists(sphereGrp)==False:
        raise IOError
    
    spheres = cmds.listRelatives( sphereGrp, ad=True, f=True, type=('nurbsSurface','mesh') )
    if spheres:
        posLi, radiusLi = [], []
        for tfNode in spheres:
            objPos = cmds.objectCenter(tfNode)
            bbox = cmds.exactWorldBoundingBox(tfNode, ignoreInvisible=False)       
            radius = (bbox[3]-bbox[0])/2
            posLi.append(objPos)
            radiusLi.append(radius)        
        parAttrs = [('radiusPP', 'floatValue', radiusLi) ]
        
        if cmds.checkBox('uiBlobbyAttr', q=True, v=True):
            distanceList = emFx_getSpheresDistane()
            if distanceList:
                parAttrs.append( ('cus_dis', 'floatValue', distanceList) )
                            
        parShape = cmds.textFieldButtonGrp('uiGetParticleNode', q=True, text=True)
        if parShape=='' or cmds.objExists(parShape)==False:
            temp = emfx_createNewParNode()
            parShape = temp[1]
            cloudGrp = cmds.textField('uiCloudGrpName', q=True, text=True)
            if cloudGrp != '' and cmds.objExists(cloudGrp)==True:
                cmds.parent(temp[0], cloudGrp)
              
        qm.qsEmit(object = parShape, position=posLi, attributes=parAttrs,  clearAndSaveState=False    )
        cmds.textFieldButtonGrp('uiGetParticleNode', e=True, text=parShape) 


def emfx_createFluidNode():
    sphereGrp = cmds.textFieldButtonGrp('uiGetSphereGrp', q=True, text=True)
    if sphereGrp and cmds.objExists(sphereGrp):
        bboxPos = cmds.exactWorldBoundingBox(sphereGrp, ignoreInvisible=False)
        pos = [(bboxPos[0]+bboxPos[3])/2,
               (bboxPos[1]+bboxPos[4])/2,
               (bboxPos[2]+bboxPos[5])/2
               ]
        fluidSize = [math.fabs(bboxPos[3]-bboxPos[0]) *1.1,
                     math.fabs(bboxPos[4]-bboxPos[1]) *1.1,
                     math.fabs(bboxPos[5]-bboxPos[2]) *1.1
                     ]
    else:
        pos = [0,0,0]
        fluidSize = [10,10,10]
    
    fluidShape = mel.eval('create3DFluid 20 20 20 %s %s %s'
                          %( int(fluidSize[0]), int(fluidSize[1]), int(fluidSize[2]) )
                          )
    fluidPapa = cmds.listRelatives(fluidShape, parent=True)[0]
    fluidPapa = cmds.rename(fluidPapa, getUniqueName('fluid_Cloud_') )
    fluidShape = cmds.listRelatives(fluidPapa)[0]
    cmds.setAttr(fluidPapa+'.t', pos[0], pos[1], pos[2], type='double3')
    #print fluidPapa, fluidShape
    cmds.setAttr(fluidShape+'.squareVoxels', 1)
    #cmds.setAttr(fluidShape+".baseResolution",20)
    cmds.setAttr(fluidShape+".velocityMethod",0)
    cmds.setAttr(fluidShape+".autoResize",1)
    cmds.setAttr(fluidShape+".autoResizeMargin",4)
    return fluidPapa

def cmd_getFluidNode():
    sel = cmds.ls(sl=True)
    value = ''
    if sel:
        fluidShapes = cmds.ls(sel, type='fluidShape')
        if fluidShapes==[]:
            fluidShapes = cmds.listRelatives(sel, type='fluidShape')
            
        value = fluidShapes[0] if fluidShapes else ''
    cmds.textFieldButtonGrp('uiGetFluidNode', e=True, text=value )

def cmd_fluidSizeFromSpheresGrp():
    sphereGrp = cmds.textFieldButtonGrp('uiGetSphereGrp', q=True, text=True)
    fluidShape = cmds.textFieldButtonGrp('uiGetFluidNode', q=True, text=True )
    if sphereGrp and cmds.objExists(sphereGrp) and\
            fluidShape and cmds.objExists(fluidShape) and cmds.objectType(fluidShape)=='fluidShape':
        fluidPapa = cmds.listRelatives(fluidShape, parent=True)[0]
        bboxPos = cmds.exactWorldBoundingBox(sphereGrp, ignoreInvisible=False)
        pos = cmds.objectCenter(sphereGrp)
        #pos = [(bboxPos[0]+bboxPos[3])/2,
               #(bboxPos[1]+bboxPos[4])/2,
               #(bboxPos[2]+bboxPos[5])/2
               #]
        fluidSize = [math.fabs(bboxPos[3]-bboxPos[0]) *1.1,
                     math.fabs(bboxPos[4]-bboxPos[1]) *1.1,
                     math.fabs(bboxPos[5]-bboxPos[2]) *1.1
                     ]
        cmds.setAttr(fluidPapa+'.t', pos[0], pos[1], pos[2], type='double3')
        cmds.setAttr(fluidShape+'.dimensionsW', fluidSize[0])
        cmds.setAttr(fluidShape+'.dimensionsH', fluidSize[1])
        cmds.setAttr(fluidShape+'.dimensionsD', fluidSize[2])

def emfx_saveFluidPresetFile(fluidShape, presetName, cloudPresetPath=presetsFolder):    
    
    fileName = presetName
    #fluidShape = cmds.ls(sl=True, type='fluidShape')[0]
    #Get Attributes
    saveAttrs = [
               'densityMethod', 'velocityMethod', \
               'transparency', 'edgeDropoff',   'colorInput',   'colorInputBias',\
               'opacityInput', 'opacityInputBias',  'quality',  'contrastTolerance',    'renderInterpolator',\
               'colorTexture',  'opacityTexture',   'textureType',  'colorTexGain', 'opacityTexGain',\
               'amplitude', 'ratio ',   'frequencyRatio',  'depthMax',  'invertTexture',    'inflection',\
               'textureTime',   'frequency',    'textureScaleX',    'textureScaleY',    'textureScaleZ',\
               'selfShadowing', 'shadowOpacity',    'lightType',    'lightBrightness',  'fluidLightColor',\
               'ambientBrightness', 'ambientDiffusion', 'ambientColor', 'directionalLightX',    'directionalLightY',\
               'directionalLightZ', 'pointLightX',  'pointLightY',  'pointLightZ',  'pointLightDecay'
               ]
    
    
    indices = cmds.getAttr( fluidShape+'.opacity', multiIndices=True)
    for index in indices:
        saveAttrs.extend(['opacity[%s].opacity_Position'%(index),
                        'opacity[%s].opacity_FloatValue'%(index),
                        'opacity[%s].opacity_Interp'%(index)]
                        )
    
    for multiAttr in ('color', 'incandescence'):
        indices = cmds.getAttr( fluidShape+'.'+multiAttr, multiIndices=True)
        for index in indices:
            saveAttrs.extend(['%s[%s].%s_Position'%(multiAttr,index,multiAttr),
                            '%s[%s].%s_Color'%(multiAttr,index,multiAttr),
                            '%s[%s].%s_Interp'%(multiAttr,index,multiAttr)]
                           )
    
    #Combine setAttr commands
    pyFileStr = 'fluidShape = cmds.ls(sl=True, type="fluidShape")[0]\n'
    for attr in saveAttrs:
        value = cmds.getAttr(fluidShape+'.'+attr)
        attrType = cmds.getAttr(fluidShape+'.'+attr, type=True)
        if attrType=='float3' or attrType=='double3':
            pyFileStr += 'cmds.setAttr(fluidShape+".%s", %s, %s, %s, type="%s")\n'%(attr,value[0][0],value[0][1],value[0][2],attrType)
        else:
            pyFileStr += 'cmds.setAttr(fluidShape+".%s", %s)\n'%(attr, value)

   
    #fileName = emfx_getUniquePresetName( cloudPresetPath )
    #Save attributes preset as python files
    presetFile = open(cloudPresetPath+fileName+'.py', 'w')
    presetFile.write(pyFileStr)
    presetFile.close()
    print 'Saved ', fileName



def cmd_confirm_saveFluidPreset( cloudPresetPath = presetsFolder):
    fluidShape = cmds.textFieldButtonGrp('uiGetFluidNode', q=True, text=True )
    presetName = cmds.textField('presetName', q=True, text=True)
    if presetName == '':
        presetName = emfx_getUniquePresetName( cloudPresetPath )
            
    if os.path.exists(cloudPresetPath+presetName+'.py') == False:
        emfx_saveFluidPresetFile(fluidShape, presetName)
        cmds.menuItem( label=presetName, p='uiFluidPresets')
        cmds.deleteUI('presetNameWin', window=True)
    else:
        confirmReturn = cmds.confirmDialog(title='Confirm',message='File Exists. Overwrite?',\
                        button=['Yes','No','Auto Rename'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirmReturn == 'Yes':
            emfx_saveFluidPresetFile(fluidShape, presetName)
            cmds.deleteUI('presetNameWin', window=True)
        elif confirmReturn == 'Auto Rename':
            presetName = emfx_getUniquePresetName( cloudPresetPath )
            emfx_saveFluidPresetFile(fluidShape, presetName)
            cmds.deleteUI('presetNameWin', window=True)
        else:#confirmReturn=='No'
            pass
        
        if confirmReturn != 'No':
            cmds.menuItem( label=presetName, p='uiFluidPresets')




def cmd_saveFluidPreset():
    fluidShape = cmds.textFieldButtonGrp('uiGetFluidNode', q=True, text=True )
    if fluidShape and cmds.objExists(fluidShape) and cmds.objectType(fluidShape)=='fluidShape':
        if cmds.window('presetNameWin', exists=True):
            cmds.deleteUI('presetNameWin')
        cmds.window('presetNameWin', title='Save FluidShape Attribute Preset', sizeable=False)
        cmds.columnLayout('tempLayout', p='presetNameWin')
        
        cmds.rowColumnLayout( 'tempLayout_02', p='tempLayout', numberOfColumns=2, columnWidth=[(1,80), (2,150)] )
        cmds.text(label='Preset name:', p='tempLayout_02')
        cmds.textField('presetName', p='tempLayout_02', text=cmds.textFieldButtonGrp('uiGetFluidNode', q=True, text=True) )
        
        cmds.separator(h=30)
        cmds.separator(h=30)
        cmds.rowColumnLayout( 'tempLayout_03', p='tempLayout', numberOfColumns=2, columnWidth=[(1,115), (2,115)] )
        cmds.button(p='tempLayout_03', label='Save Fluid Preset', h=30, command='cmd_confirm_saveFluidPreset()' )
        cmds.button(p='tempLayout_03', label='Close', h=30, command='cmds.deleteUI("presetNameWin")')
        cmds.showWindow('presetNameWin')

       



def cmd_fluidPresetsImages(cloudPresetPath=presetsFolder):
    imageName = cmds.optionMenu( 'uiFluidPresets', q=True, value=True)
    imageFullName = '%s%s.jpg'%(cloudPresetPath,imageName)
    if os.path.exists( imageFullName )==False:
        imageFullName = '%sCloud_defaultImage.jpg'%(cloudPresetPath)
    cmds.image("uiFluidPresetImage", e=True, i=imageFullName)


#Get python preset file apply to fluidShape
def emfx_applyFluidPresetFile(fluidShape, presetFullPath):
    if os.path.exists(presetFullPath ) and fluidShape and cmds.objExists(fluidShape) and cmds.objectType(fluidShape)=='fluidShape':
        #Remove exists multi attributes for the fluid shape
        for multiAttr in ('color', 'incandescence', 'opacity'):
            indices = cmds.getAttr( fluidShape+'.'+multiAttr, multiIndices=True)
            if len(indices)>1:
                for index in indices[1:]:
                    cmds.removeMultiInstance("%s.%s[%s]"%(fluidShape, multiAttr, index), b=True)
        cmds.select(fluidShape, r=True)
        #Apply preset file to fluidShape
        execfile(presetFullPath )

def cmd_applyFluidPreset(cloudPresetPath=presetsFolder):
    itemName = cmds.optionMenu( 'uiFluidPresets', q=True, value=True)
    presetFullPath = cloudPresetPath + itemName+'.py'
    fluidShape = cmds.textFieldButtonGrp('uiGetFluidNode', q=True, text=True )
    
    emfx_applyFluidPresetFile(fluidShape, presetFullPath)


def cmd_createFluidNode():
    fluidPapa = emfx_createFluidNode()
    fluidShape = cmds.listRelatives(fluidPapa, shapes=True)[0]
    cmds.textFieldButtonGrp('uiGetFluidNode', e=True, text=fluidShape)


def cmd_createLightBW():
    if cmds.objExists("LIGHT_RIG_CLOUD"):
        cmds.delete("LIGHT_RIG_CLOUD")
        
    loc = cmds.spaceLocator(n="LIGHT_RIG_CLOUD", p=(0,0,0) )[0]

    lightShape = cmds.directionalLight()
    lightTransform = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.setAttr(lightTransform+".rotate",-140,0,40,type="double3")
    cmds.setAttr(lightTransform+".scale",10,10,10,type="double3")
    cmds.setAttr(lightShape+".color",1,1,1, type="double3")
    cmds.setAttr(lightShape+".intensity",0.95)
    cmds.setAttr(lightShape+".shadowColor",0.333,0.333,0.333, type="double3")
    cmds.setAttr(lightShape+".useRayTraceShadows",1)
    nomTmp = cmds.rename(lightTransform,"Light_KEY")
    cmds.parent(nomTmp,loc)

    lightShape = cmds.directionalLight()
    lightTransform = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.setAttr(lightTransform+".rotate",80,-30,-35,type="double3")
    cmds.setAttr(lightTransform+".scale",10,10,10,type="double3")
    cmds.setAttr(lightShape+".color",1,1,1,type="double3")
    cmds.setAttr(lightShape+".intensity",-0.15)
    cmds.setAttr(lightShape+".useRayTraceShadows",1)
    nomTmp = cmds.rename(lightTransform,"Light_BOUNCE")
    cmds.parent(nomTmp,loc)

    lightShape = cmds.directionalLight()
    lightTransform = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.setAttr(lightTransform+".rotate",125,-60,85,type="double3")
    cmds.setAttr(lightTransform+".scale",10,10,10,type="double3")
    cmds.setAttr(lightShape+".color", 1,1,1,type="double3")
    cmds.setAttr(lightShape+".intensity",0.1)
    cmds.setAttr(lightShape+".useRayTraceShadows",1)
    nomTmp = cmds.rename(lightTransform,"Light_FILL")
    cmds.parent(nomTmp,loc)


def cmd_createLightRGB():
    if cmds.objExists("LIGHT_RIG_CLOUD"):
        cmds.delete("LIGHT_RIG_CLOUD")
        
    loc = cmds.spaceLocator(n="LIGHT_RIG_CLOUD", p=(0,0,0) )[0]
    
    lightShape = cmds.directionalLight()
    lightTransform = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.setAttr(lightTransform+".rotate",-140,0,40, type="double3")
    cmds.setAttr(lightTransform+".scale",10,10,10, type="double3")
    cmds.setAttr(lightShape+".color",0.9,0,0, type="double3")
    cmds.setAttr(lightShape+".useRayTraceShadows",1)
    nomTmp = cmds.rename(lightTransform,"Light_KEY_R")
    cmds.parent(nomTmp,loc)
    
    lightShape = cmds.directionalLight()
    lightTransform = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.setAttr(lightTransform+".rotate",80,-30,-35,type="double3")
    cmds.setAttr(lightTransform+".scale",10,10,10,type="double3")
    cmds.setAttr(lightShape+".color",0,0.9,0,type="double3")
    cmds.setAttr(lightShape+".useRayTraceShadows",1)
    nomTmp = cmds.rename(lightTransform,"Light_BOUNCE_G")
    cmds.parent(nomTmp,loc)
    
    lightShape = cmds.directionalLight()
    lightTransform = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.setAttr(lightTransform+".rotate",125,-60,85,type="double3")
    cmds.setAttr(lightTransform+".scale",10,10,10,type="double3")
    cmds.setAttr(lightShape+".color",0,0,0.9,type="double3")
    cmds.setAttr(lightShape+".useRayTraceShadows",1)
    nomTmp = cmds.rename(lightTransform,"Light_FILL_B")
    cmds.parent(nomTmp,loc)

    
def emfx_addCloudPresetItems(cloudPresetPath=presetsFolder):
    allPresetsFiles = os.listdir( cloudPresetPath )
    itemsName = []
    for presetFile in allPresetsFiles:
        if presetFile.endswith('.py'):
            itemName = presetFile.replace('.py', '') 
            itemsName.append(itemName)
    
    if itemsName:
        itemsName.sort()
        #cmds.deleteUI(cmds.optionMenu( 'uiFluidPresets', q=True, ill=True), menuItem=True)
        for item in itemsName:
            cmds.menuItem( item, label=item, p='uiFluidPresets')


def cmd_DeletePreset(cloudPresetPath=presetsFolder):
    itemName = cmds.optionMenu('uiFluidPresets', q=True, value=True)
    cmds.deleteUI(itemName, menuItem=True)    
    oldName = cloudPresetPath+itemName+'.py'
    newName = cloudPresetPath+itemName+'.py.deleted'
    os.path.exists(oldName)
    os.rename(oldName, newName)

def cmd_SavePresetImageFromRenderView(cloudPresetPath=presetsFolder):
    import maya.OpenMaya as om    
    presetName = cmds.optionMenu( 'uiFluidPresets', q=True, value=True)
    oriImage = qm.saveSwatch()
    if oriImage:
        newImage = presetsFolder+'/'+presetName+'.jpg'
        image = om.MImage()
        image.readFromFile(oriImage)
        image.resize( 256, 256 )
        image.writeToFile( newImage, 'jpg')
        os.remove(oriImage)
        cmd_fluidPresetsImages()
        return newImage

#----------Main Window

def w07_emfxClouds_Win():
    '''path:Dynamic/w07_emfxClouds_Win()
icon:menuIconWindow.png
usage:
w07_emfxClouds_Win()
'''
    if cmds.window("emfxCloudsUIT", exists=True):
        cmds.deleteUI("emfxCloudsUIT")
    
    
    cmds.window( "emfxCloudsUIT", title='w07_emfx_clouds', sizeable=False)
    
    cmds.formLayout('uiTopLayout', p="emfxCloudsUIT")
    
    #----------Get CoudGrp UI
    cmds.columnLayout('uiLayout_01', w=180, p='uiTopLayout')
    cmds.image(p='uiLayout_01', i=r"D:/Users/Administrator/Documents/sq/scripts/sqFX/maya/emfxClouds/structure.jpg", w=140, h=120)
    cmds.separator(p='uiLayout_01',h=10,style="in")
    cmds.textField('uiCloudGrpName', p='uiLayout_01', h=25, w=175, font="boldLabelFont", editable=False)
    cmds.separator(p='uiLayout_01',h=10,style="in")
    cmds.button("uiGetCloudGrp", p='uiLayout_01', label="Get CloudGrp From Selected", h=35,w=175, c='cmd_getCloudGrp()')
    cmds.separator(p='uiLayout_01',h=10,style="in")
    cmds.button("uiCreateCloudGrp", p='uiLayout_01', label="Create CloudGrp", h=35,w=175, c='cmd_createCloudGrp()' )
    
    
    #------------Display panel UI
    cmds.frameLayout('uiDisplayFL', p="uiTopLayout", label="Display", marginHeight=5, marginWidth=5, w=180, collapsable=False, cl=False, borderStyle="in")
    cmds.rowColumnLayout('uiDisplayFL_01', nc=2, p='uiDisplayFL',
                         columnWidth=[(1,115), (2,40)], rowSpacing=[1,4], columnSpacing=[(1,5),(2,5)] )
    cmds.button("uiDisLayout", p='uiDisplayFL_01', h=35, label="LyaoutGrp On / Off",  c='cmd_disButtons("uiGetLayoutGrp")' )
    cmds.button("uiSelLayout", p='uiDisplayFL_01', h=35, label="Sel",  c='cmd_selButtons("uiGetLayoutGrp")' )
    
    cmds.button("uiDisSphere", p='uiDisplayFL_01', h=35, label="SphereGrp On / Off",  c='cmd_disButtons("uiGetSphereGrp")' )
    cmds.button("uiSelSphere", p='uiDisplayFL_01', h=35, label="Sel",  c='cmd_selButtons("uiGetSphereGrp")')
    
    cmds.button("uiDisParticle", p='uiDisplayFL_01', h=35, label="Emitter(par) On / Off",  c='cmd_disButtons("uiGetParticleNode")' )
    cmds.button("uiSelParticle", p='uiDisplayFL_01', h=35, label="Sel",  c='cmd_selButtons("uiGetParticleNode")')
    
    cmds.button("uiDisFluid", p='uiDisplayFL_01', h=35, label="Fluid On / Off",  c='cmd_disButtons("uiGetFluidNode")' )
    cmds.button("uiSelFluid", p='uiDisplayFL_01', h=35, label="Sel",  c='cmd_selButtons("uiGetFluidNode")')
    
    
                            
    #--------------Volume Form Layout Panel UI
    cmds.frameLayout('uiVolumeFL', p="uiTopLayout", label="Volume From Layout",   marginHeight=5, marginWidth=5, w=250, bgc=(0.15,0.15,0.3),  collapsable=False,  borderStyle="in")
    #cmds.columnLayout("uiVolumeFL_01")
    cmds.textFieldButtonGrp('uiGetLayoutGrp',  p='uiVolumeFL', label='LayoutGrp', bgc=[.2,.2,.2],
                            h=25, cw3=[80,100,50], cl3=['right', 'left', 'right'],
                            buttonLabel='Get Sel', buttonCommand='cmd_getLayoutGrp()' )
    cmds.popupMenu('uiPopupMenuLayoutGrp', p='uiGetLayoutGrp')
    cmds.menuItem(p='uiPopupMenuLayoutGrp',label='Clear Texts', command="cmds.textFieldButtonGrp('uiGetLayoutGrp', e=True, text='' )")
    
    
    cmds.button('uiCreateLayoutGrp', p='uiVolumeFL', h=30,label='createLayoutGrp',  bgc=[.3,.4,.3], c='cmd_createLayoutGrp()')
    cmds.popupMenu('uiPopupMenuCreateLayoutGrp', p='uiCreateLayoutGrp')
    cmds.radioMenuItemCollection('uiRadioMenus', p='uiPopupMenuCreateLayoutGrp')   
    cmds.menuItem(p='uiPopupMenuCreateLayoutGrp',radioButton=True, label='Up')
    cmds.menuItem(p='uiPopupMenuCreateLayoutGrp',radioButton=False, label='Down')
    cmds.menuItem(p='uiPopupMenuCreateLayoutGrp',radioButton=False, label='Both')
    
    cmds.separator(p='uiVolumeFL',style="in")
    cmds.optionMenu( 'uiSamplingMethod', p='uiVolumeFL', label='Position From', h=30, changeCommand='print "aaa"')
    cmds.menuItem( label='Bounding Box', p='uiSamplingMethod' )
    cmds.menuItem( label='Poly Mesh', p='uiSamplingMethod' )
    
    cmds.intFieldGrp("uiMaxAxisRes", p='uiVolumeFL', label='Max Axis Resolution', h=30, cw2=[120,95], v1=40 )
    
    
    #---------------Spheres From Volume Panel UI
    cmds.frameLayout('uiSpheresFL',p='uiVolumeFL', label="Spheres From Volume", marginHeight=5, marginWidth=5, w=240, bgc=(0.15,0.15,0.3), collapsable=True, cl=False, borderStyle="in")
    #cmds.columnLayout("uiEmitterLayout")
    cmds.textFieldButtonGrp('uiGetSphereGrp', p='uiSpheresFL', label='SpheresGrp',  bgc=[.2,.2,.2],
                            h=25, cw3=[70,100,50], cl3=['right', 'left', 'right'],
                            buttonLabel='Get Sel', buttonCommand='cmd_getSphereGrp()' )
    cmds.popupMenu('uiPopupMenuSphereGrp', p='uiGetSphereGrp')
    cmds.menuItem(p='uiPopupMenuSphereGrp',label='Clear Texts', command="cmds.textFieldButtonGrp('uiGetSphereGrp', e=True, text='' )")
    
    cmds.separator(p='uiSpheresFL',style="in")
    cmds.rowColumnLayout('uiSpheresFL_01', nc=2, p='uiSpheresFL', columnWidth=[(1,150), (2,60)], columnSpacing=[(1,5),(2,5)] )
    cmds.floatFieldGrp("uiRandomPos", p='uiSpheresFL_01',label='Random Position', columnWidth2=(90,60),  h=20, precision=3, v1=1 )
    cmds.button('uiGetVoxelSize', p='uiSpheresFL_01', l='Voxel Size', h=25, c='cmd_getVoxelSize()')
    cmds.intFieldGrp("uiNumberSpheres",p='uiSpheresFL',label='Number Spheres', columnWidth2=(120,100), h=20, v1=100 )
    cmds.floatFieldGrp("uiRandRadius", p='uiSpheresFL', numberOfFields=2, label='Random Spheres Radius', columnWidth3=(120,50,50), h=20, precision=3, v1=1,v2=2 )
    
    cmds.button("uiCreateSpheres", p='uiSpheresFL', h=30, label="Create Spheres", bgc=[.3,.4,.3], c='cmd_createSpheres()')
    cmds.popupMenu('uiPopupMenuCreateSpheres', p="uiCreateSpheres")
    cmds.menuItem('uiCreateSpheresModel', p='uiPopupMenuCreateSpheres',checkBox=True, label='From ParticleNode')
    cmds.menuItem('uiCreateSpheresModel', e=True, checkBox=False)
    
    
    
    #----------------Fluid Emitter From Sphere Panel UI
    cmds.frameLayout('uiEmitterFL', p='uiVolumeFL', label="Fluid Emitter(par) From Spheres", marginHeight=5, marginWidth=5, w=240, bgc=(0.15,0.15,0.3), collapsable=True, cl=False, borderStyle="in")
    
    cmds.textFieldButtonGrp('uiGetParticleNode', p='uiEmitterFL', label='Particle Node',  bgc=[.2,.2,.2],
                            h=25, cw3=[70,100,50], cl3=['right', 'left', 'right'],
                            buttonLabel='Get Sel', buttonCommand='cmd_getParticleNode()' )
    cmds.popupMenu('uiPopupMenuParticleNode', p='uiGetParticleNode')
    cmds.menuItem(p='uiPopupMenuParticleNode',label='Clear Texts', command="cmds.textFieldButtonGrp('uiGetParticleNode', e=True, text='' )")
    
    cmds.separator(p='uiEmitterFL',style="in")
    #cmds.checkBoxGrp('uiBlobbyAttr',p='uiEmitterFL', label='Particless attrs form spheres', numberOfCheckBoxes=2, labelArray2=['Surface Dis', 'Two'], vertical=True )
    cmds.checkBox('uiBlobbyAttr',p='uiEmitterFL', label='Suface Distance to Par Attr', v=False)
                     
    cmds.rowColumnLayout('uiEmitterFL_02', nc=2, p='uiEmitterFL', columnWidth=[(1,105), (2,105)], columnSpacing=[(1,5),(2,5)] ) 
    cmds.button( 'uiClearState', p='uiEmitterFL_02', h=30, label="Clear Initial State", c='cmd_clearState()' )
    cmds.button('uiSaveState', p='uiEmitterFL_02', h=30, label="Save Initial State", c='cmd_saveState()' )
    
    cmds.button("uiAddParticles", p='uiEmitterFL',h=30, label="Add Particles", c='cmd_addParticles()')
    
    
    
    #--------------------Fluids Panel UI
    cmds.frameLayout('uiFluidFL',  p="uiTopLayout", label="Fluid", marginHeight=5,  marginWidth=5, w=240,  bgc=[.15,.15,.3], collapsable=False, cl=False, borderStyle="in")
    cmds.textFieldButtonGrp('uiGetFluidNode', p='uiFluidFL', label='Fluid Node', bgc=(.2,.2,.2),
                            h=25, cw3=[60,110,50], cl3=['right', 'left', 'right'], 
                            buttonLabel='Get Sel', buttonCommand='cmd_getFluidNode()' )
    cmds.popupMenu('uiPopupMenuFluidNode', p='uiGetFluidNode')
    cmds.menuItem(p='uiPopupMenuFluidNode',label='Clear Texts', command="cmds.textFieldButtonGrp('uiGetFluidNode', e=True, text='' )")
    cmds.menuItem(p='uiPopupMenuFluidNode',label='Fluid Size From ShperesGrp', command='cmd_fluidSizeFromSpheresGrp()')
    
    cmds.button('uiSavePresets', p='uiFluidFL', label='Save fluidShape Preset', c='cmd_saveFluidPreset()' )
    cmds.separator(  p='uiFluidFL',style="in")
    
    cmds.optionMenu( 'uiFluidPresets', p='uiFluidFL', label='Cloud Presets', h=25,   changeCommand='cmd_fluidPresetsImages()' )
    #cmds.menuItem( label='Cloud_001', p='uiFluidPresets')
    #cmds.menuItem( label='Cloud_002', p='uiFluidPresets')
    #cmds.menuItem( label='Cloud_003', p='uiFluidPresets')
    
    cmds.image("uiFluidPresetImage", p='uiFluidFL', i=presetsFolder+"cloud_defaultImage.jpg",  bgc=[.2,.2,.2], w=200,h=200)
    cmds.popupMenu('uiPopupMenuDeltePreset', p="uiFluidPresetImage")
    cmds.menuItem(p='uiPopupMenuDeltePreset',label='Delete Current Preset', command='cmd_DeletePreset()')
    cmds.menuItem(p='uiPopupMenuDeltePreset', divider=True)
    cmds.menuItem(p='uiPopupMenuDeltePreset', divider=True)
    cmds.menuItem(p='uiPopupMenuDeltePreset',label='Save Prset Image From Render View', command='cmd_SavePresetImageFromRenderView()')
    #cmds.button('uiDelteCurPreset', p='uiFluidFL')
    
    #cmds.rowColumnLayout('uiFluidFL_01', nc=2, p='uiFluidFL', columnWidth=[(1,115), (2,115)], columnSpacing=[(1,5),(2,5)] ) 
    cmds.button('uiApplyPresets', p='uiFluidFL', label='Applay fluidShape Preset', c='cmd_applyFluidPreset()' )
    
    
    cmds.separator(  p='uiFluidFL',style="in")
    cmds.button('uiCreateFluid', p='uiFluidFL', label='Create Fluid', h=30, w=235, c='cmd_createFluidNode()' )
    
    
    
    cmds.rowColumnLayout('uiLight', nc=2, p="uiTopLayout", columnWidth=[(1,120), (2,110)], columnSpacing=[(1,5),(2,5)] )
    cmds.separator(  p='uiLight', h=20, style="out")
    cmds.separator(  p='uiLight', h=20, style="out")
    cmds.button('uiLightsBW', p='uiLight', h=30, label='Create Lights BW', c='cmd_createLightBW()' )
    cmds.button('uiLightsRGB', p='uiLight', h=30, label='Create Lights RGB', c='cmd_createLightRGB()' )
    
    
    
    cmds.formLayout("uiTopLayout", edit=True,
                    attachForm=[("uiLayout_01", "top", 3),    ("uiLayout_01", "left", 3),
                                #('uiLayoutFL',  "top", 1),    ('uiLayoutFL',  'left', 3),
                                ("uiDisplayFL", "top", 1),    ("uiDisplayFL", "left", 3),                            
                                ("uiVolumeFL",  "top", 3),    ("uiVolumeFL",  "left", 3),
                                ('uiFluidFL',   'top', 3),    ("uiFluidFL",   "left", 3), ("uiFluidFL","right",3),
                                ('uiLight',     'top', 3),    ('uiLight',     'left', 3)
                                ],
                    attachControl=[#('uiLayoutFL',  "top",   1,  "uiLayout_01"),
                                   ("uiDisplayFL", "top",   1,  "uiLayout_01"),                               
                                   ("uiVolumeFL",  "left",  5,  "uiLayout_01"),
                                   ("uiFluidFL",   "left",  5,  "uiVolumeFL"),
                                   ('uiLight',     'top',   5,  'uiFluidFL'),('uiLight', 'left', 5, 'uiVolumeFL')
                                   ]
                   )
    emfx_addCloudPresetItems(cloudPresetPath=presetsFolder)
    cmds.showWindow("emfxCloudsUIT")
w07_emfxClouds_Win()