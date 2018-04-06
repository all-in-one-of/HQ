#!/usr/bin/env python
#coding=cp936
#coding=utf-8

import pymel.core as pm 
import maya.OpenMaya as OpenMaya
import logging 

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

class AvesPlumeJiont(object):
	def __init__(self , num = 6):

		self.frontJoint = []
		self.backJoint = []
		
		self.addFrontBackJoint = []
		
		self.FrontBackCtr = []
		
		self.frontIkHandList = []
		
		self.num = num
		
		self.featherDir = {}
		
		self.featherJointGroup = None 
		self.featherIkHandGroup = None
		self.featherIkCurGroup = None
		self.featherClusterGroup = None
		
		self.featherCtrlGroup = None
		
		self.globalScaleMD = None
		
		self.ctr = None
	
	
	def featherJoint(self , selectJoint = None):
		if selectJoint is None:
			selectJoint = pm.selected()
		if len(selectJoint) < 2:
			OpenMaya.MGlobal.displayError('@selectJoint : This is len < 2 : len(selectJoint) = %s'%(len(selectJoint)))
			logger.error('@selectJoint : This is len < 2 : len(selectJoint) = %s'%(len(selectJoint)))
		
		self._createGroup()
		
		self.FrontBackCtr = self._createMCurves(selectJoint)
		
		self.__createPlumeCurve(selectJoint[0])
		
		int = 1
		for index,value in enumerate(selectJoint):
			if index in range(len(selectJoint)-1):
				lastRootJoint = pm.listRelatives(value ,ad=1)[0]
				lastEndJoint = pm.listRelatives(selectJoint[index+1],ad=1)[0]
				objectName = value.name()
				name = self.getObjectName(objectName)
				if len(selectJoint) is 2:
					frontList = self.getObjectPoint(value.getTranslation(space = 'world'),selectJoint[index+1].getTranslation(space = 'world'),self.num )
					backList = self.getObjectPoint(lastRootJoint.getTranslation(space = 'world'),lastEndJoint.getTranslation(space = 'world'),self.num )
					featherList = self.cerateFeatherJoint(frontList , backList , name ,int)
					PlumejointList = self.ceratePlume(featherList)
					
					self.addFrontBackJoint += PlumejointList
					
					ikHandList = self._createFeatherJoint(PlumejointList)
					int += 1
					
					
					
				if len(selectJoint) > 2:
					if index is 0:
						frontList = self.getObjectPoint(value.getTranslation(space = 'world'),selectJoint[index+1].getTranslation(space = 'world'),self.num , 1 )
						backList = self.getObjectPoint(lastRootJoint.getTranslation(space = 'world'),lastEndJoint.getTranslation(space = 'world'),self.num , 1 )
						featherList = self.cerateFeatherJoint(frontList , backList , name ,int)
						featherAddList = self.featherRootEndJoint(featherList , value ,lastRootJoint , selectJoint[index+1] , lastEndJoint)
						
						
						PlumejointList = self.ceratePlume(featherAddList)
						
						self.addFrontBackJoint += PlumejointList
						
						ikHandList = self._createFeatherJoint(PlumejointList)
						
						ClusterList = self._cerateCurveIkHandle(featherAddList)
						self._parentConstraCulster(ClusterList , value , selectJoint[index+1] , 1)
						
						self.__createPlumeJiont(value , lastRootJoint , 1)
						
						
						
						int += 1
						
					if index is len(selectJoint)-2:
						frontList = self.getObjectPoint(value.getTranslation(space = 'world'),selectJoint[index+1].getTranslation(space = 'world'),self.num , 3 )
						backList = self.getObjectPoint(lastRootJoint.getTranslation(space = 'world'),lastEndJoint.getTranslation(space = 'world'),self.num , 3 )
						featherList = self.cerateFeatherJoint(frontList , backList , name ,int , 2)
						featherAddList = self.featherRootEndJoint(featherList , value ,lastRootJoint , selectJoint[index+1] , lastEndJoint , 3)
						
						PlumejointList = self.ceratePlume(featherAddList)
						
						self.addFrontBackJoint += PlumejointList
						
						ikHandList = self._createFeatherJoint(PlumejointList)	
						
						ClusterList = self._cerateCurveIkHandle(featherAddList)	
						self._parentConstraCulster(ClusterList , value , selectJoint[index+1] , 2)
						
						self.__createPlumeJiont(selectJoint[index+1] , lastEndJoint , (self.num+1))		 
		
						int += 1
						
						
					if index > 0 and index < len(selectJoint)-2:
						frontList = self.getObjectPoint(value.getTranslation(space = 'world'),selectJoint[index+1].getTranslation(space = 'world'),self.num , 2 )
						backList = self.getObjectPoint(lastRootJoint.getTranslation(space = 'world'),lastEndJoint.getTranslation(space = 'world'),self.num , 2 )
						featherList = self.cerateFeatherJoint(frontList , backList , name ,int ,2)
						featherAddList = self.featherRootEndJoint(featherList ,  value ,lastRootJoint , selectJoint[index+1] , lastEndJoint , 2)
						
						PlumejointList = self.ceratePlume(featherAddList)
						
						self.addFrontBackJoint += PlumejointList
						
						ikHandList = self._createFeatherJoint(PlumejointList)
						
						ClusterList = self._cerateCurveIkHandle(featherAddList)
						self._parentConstraCulster(ClusterList , value , selectJoint[index+1] )
						
						
						
						
						int += 1
						
		
			else:
				pass
		
		self.connectVectr()
		
		
	def connectVectr(self):
		for i in range(len(self.frontIkHandList)-1):
			pm.poleVectorConstraint(self.frontIkHandList[i+1] , self.frontIkHandList[i] , w = 1)
	
	
	def _jointOrient(self , object = None):
		'''
		@object : list Node , This is a joint Node list
		'''
		
		pos = [0 , 0 ,180]
		
		for o in object :
			
			o.setRotateAxis(pos)
		
			o.zeroScaleOrient()
		
		
	def __createPlumeCurve(self , object = None):
		'''
		@object : node 
		'''
		
		
		name = object.name()
		
		temp = name.split('_')
		
		nameEx = temp[0] + '_wingAttr_crtl'
		
		if pm.objExists(nameEx):
			
			self.ctr = Control()
			
			self.ctr.controlName = nameEx
			
			self.ctr.control = pm.PyNode(nameEx)
			
			self.ctr.controlGrp_C = self.ctr.control.getParent()
			
			self.ctr.controlGrp_C = self.ctr.controlGrp_C.getParent()
			
			return 
			
		
		self.ctr = Control(temp[0] , 'wingAttr')
		
		self.ctr.sphereCnt()
		
		self.ctr.controlGrp_G.setMatrix(object.wm.get())
		
		self.setAttrLock(self.ctr.control)
		
		attr = [['close' , 'bend'] , ['sinWing' , 'freQuency' , 'offset1' , 'offset2'] , ['wing']]
		
		a = '_'
		
		for att in attr :
			
			self.ctr.control.addAttr(a , at = 'enum' , en = ':' , k = 0 )
			
			self.ctr.control.setAttr(a , cb = 1)
			
			for ar in att:
				
				self.ctr.control.addAttr(ar , at = 'double' ,  k = 1)
				
			a += '_'
		
		self.ctr.control.addAttr('ctrl' , at = 'enum' , en = 'off:on' , k = 0 )
		
		self.ctr.control.setAttr('ctrl' , cb = 1)
		
		
				

	def _createMCurves(self , list = None):
		'''
		@list : list , This is the list is list
		'''
		if  list is None:
			OpenMaya.MGlobal_displayError('@list : This is the list is None : list = %s'%(list))
			return
		listCtrName = [] 
		
		for obj in list:
		
			ctrlMList = self.createCurves(obj.name() , 1)
						
			if ctrlMList[0].name().find('L') is -1:
				for a in ctrlMList:
					for s in a.getShapes():
						pm.rotate(s.cv , 0 , 180 , 0 , r = 1 )
					
			ctrlMList[0].getParent().getParent().setParent(self.featherCtrlGroup)
			obj.setParent(ctrlMList[0])
			#obj.v.set(0)
			self.featherDir[obj.name()] = ctrlMList
			
			listCtrName.append(ctrlMList)
		
		return listCtrName
		
	def _parentConstraCulster(self , clusterList = None , rootJoint = None , endJoint = None , type = 0):
		'''
		@clusterList : list , This is the clusterList is list
		@rootJoint : str  node , This is the rootJoint of is joint node
		@endJoint : str Node , This is the endJoint is joint node
		'''
		if rootJoint.name().find('L') is -1 and rootJoint.name().find('R') is -1 :
			OpenMaya.MGlobal_displayError('@rootJoint and @endJoint : This is the rootJoint and endJoint is no L and R : rootJoint and  rootJoint = %s and %s'%(rootJoint , endJoint))
			return

		listRootJoint = self.featherDir[rootJoint.name()]
		listendJoint = self.featherDir[endJoint.name()]

		for culs in clusterList:
			pm.parentConstraint(listRootJoint[1] , culs[0] , w = True , mo = True)
			pm.parentConstraint(listendJoint[2] , culs[1] , w = True , mo = True)
			
			culs[0].v.set(0)
			culs[1].v.set(0)
		
		if type is 1:
			name = listRootJoint[2].getParent().getParent()
			pm.delete(name) 
		if type is 2:
			name = listendJoint[1].getParent().getParent()
			pm.delete(name)
			

				 
	def _createFeatherJoint(self , jointList = None):
		'''
		@jointList : list , Thes is the jointList is joint list
		'''
		allIkHandle = []
		
		if jointList is  None:
			OpenMaya.MGlobal_clearSelectionList('@jointList : This is the jointList is None : jointList = %s'%(jointList))
		
		for index , value in enumerate(jointList):
			handle , effector = pm.ikHandle( n = value[0].name() + "_ikHandle" , sj = value[0] , ee = value[1] , sol="ikRPsolver" )
			OpenMaya.MGlobal_clearSelectionList()
			allIkHandle.append(handle)
			handleGroup = self._objectGroup(handle)
			pm.parentConstraint(value[1].name().replace('addBack' , 'back') , handle , w = 1 , mo = 1)
			pm.parent(handleGroup , self.featherIkHandGroup)
			handleGroup.v.set(0)

			
			name = value[0].name().replace('addFront', 'addFront_bottom')
			 
			
			jointGroup = self._PlumeJiont(value[0] , value[1] , name) 
			
			pm.parent(jointGroup , self.featherJointGroup)
			
			pm.parentConstraint(value[0].name().replace('addFront' , 'front') , jointGroup , w = 1 , mo = 1)
		
		self.frontIkHandList += allIkHandle	

			
		return 	allIkHandle

	def __createPlumeJiont(self , rootJoint = None , endJoint = None , int = 1):
		'''
		@rootJoint :  node , This is the rootJoint of is joint node
		@endJoint :  Node , This is the endJoint is joint node
		@int : int , This is int
		'''
		
		name1 = self.getObjectName(rootJoint.name())
		
		name = name1 + '_addFront_bottom_' +self.getTwoNnmber(int)
		
		jointGroup = self._PlumeJiont(rootJoint , endJoint , name)
		
		jointGroup.setParent(self.featherDir[rootJoint.name()][0])
		
		OpenMaya.MGlobal_clearSelectionList()
	

	def _PlumeJiont(self , rootJoint = None , endJoint = None , name = None):
		'''
		@rootJoint : str  node , This is the rootJoint of is joint node
		@endJoint : str Node , This is the endJoint is joint node
		@name : str , this is ths name that will be used as a base for all the names
		'''
		
		jointGroup = self._objectGroup(rootJoint)
		
		lsitJoint = self.getObjectPoint(rootJoint.getTranslation(space = 'world') , endJoint.getTranslation(space = 'world') , num = 5)
		
		tupleListJoint = [(t[0] , t[1] , t[2]) for t in lsitJoint]
		
		bottomJoint = [pm.joint(n = name + '_' + str(i+1) , p = point1 ) for i , point1 in enumerate(tupleListJoint)]
		
		bottomJoint[0].orientJoint( 'xyz' , sao = 'yup' , zso = 1 , ch = 1)
		bottomJoint[-1].orientJoint( 'none' , sao = 'yup' , zso = 1 )

		if name.find('L') is -1:
			self._jointOrient(bottomJoint)
			
		bottomJointGroup = self._objectGroup(bottomJoint[0])
		
		bottomCtril = self.createCurves(bottomJoint[0].name() , 0 , ['Rx' ,'Ry' , 'Rz' , 'Rx1' , 'Ry1' , 'Rz1'])			
			
		if bottomCtril.name().find('L') is -1:
			for s in bottomCtril.getShapes():
					pm.rotate(s.cv , 0 , 0 , 180 , r = 1 )	
		
		if self.ctr.control.hasAttr('ctrl'):
						
			self.ctr.control.ctrl.connect(bottomCtril.getParent().getParent().v)
		
		bottomJointGroup.setParent(bottomCtril)
		
		bottomCtril.getParent().getParent().setParent(rootJoint)	

		PMANode = pm.createNode('plusMinusAverage', n = bottomJoint[0] + '_plus')
		
		bottomCtril.Rx.connect(PMANode.input3D[0].input3Dx)
		bottomCtril.Ry.connect(PMANode.input3D[0].input3Dy)
		bottomCtril.Rz.connect(PMANode.input3D[0].input3Dz)
		
		bottomCtril.Rx1.connect(PMANode.input3D[1].input3Dx)
		bottomCtril.Ry1.connect(PMANode.input3D[1].input3Dy)
		bottomCtril.Rz1.connect(PMANode.input3D[1].input3Dz)
		
		for a in bottomJoint:
			PMANode.output3Dx.connect(a.rx)
			PMANode.output3Dy.connect(a.ry)
			PMANode.output3Dz.connect(a.rz)

		return	jointGroup		

	
	def _cerateCurveIkHandle(self , frontBackList = None):
		'''
		@frontBackList : list , This is the frontBackList of is List
		'''
		if frontBackList is None :
			OpenMaya.MGlobal_displayError('@frontBackList : This is the jointList is None : frontBackList = %s'%(frontBackList))
			return
		
		frontBackClusterList = []
		for jointList in frontBackList:
			swapName = jointList[0].name().split('_')[-1]
			name = jointList[0].name().replace('_'+swapName , '_cruve')
			
			jointList1 = [jointList[0] , jointList[-1]]
			
			pointList = [a.getTranslation(space = 'world') for a in jointList1]
			knotList = range(len(jointList1))
			
			curve = pm.curve(n = name , d = 1 , p = pointList , k = knotList )
			#pm.rebuildCurve(curve ,d = 3)
			
			
			ikHandleName = jointList[0].name().replace('_'+swapName , '_ikHandle')
			handle , effector = pm.ikHandle( n = ikHandleName , sj = jointList[0] , ee = jointList[-1] , c = curve , sol="ikSplineSolver" , ccv = 0, pcv = 0 , ns = 3)
			
			jointListGroup = self._objectGroup(jointList[0])
			handleGroup = self._objectGroup(handle)
			curveGroup = self._objectGroup(curve)
			
			curve.getParent().inheritsTransform.set(0)
			
			curveGroup.setParent(handleGroup)
			handleGroup.setParent(jointListGroup)
			jointListGroup.setParent(self.featherIkCurGroup)
			
			jointList[0].getParent().v.set(0)
			handle.getParent().v.set(0)
			
			curveInfo = pm.arclen(curve , ch = 1)
			curveInfoName = curveInfo.rename(curve.name().replace('_cruve' , '_curveInfo'))
			
			MDName1 = pm.shadingNode("multiplyDivide",asUtility=True,n=jointList[0].name().replace('_'+swapName , '_MD1'))
			MDName1.operation.set(1)
			
			MDName2 = pm.shadingNode("multiplyDivide",asUtility=True,n=jointList[0].name().replace('_'+swapName , '_MD2'))
			MDName2.operation.set(2)
			
			
			self.globalScaleMD.input1X.set(1)
			
			MDName1.input1X.set(curveInfoName.arcLength.get())
			
			curveInfoName.arcLength.connect(MDName2.input1X)
			MDName1.outputX.connect(MDName2.input2X)
			self.globalScaleMD.outputX.connect(MDName1.input2X)
			
			
			for x in jointList:
				MDName2.outputX.connect(x.scaleX)
			
			ClusterList = self._createCurveCluster(curve)
			frontBackClusterList.append(ClusterList)
			
		
		OpenMaya.MGlobal_clearSelectionList()
		
		return frontBackClusterList



	def _createCurveCluster(self , curve = None):
		'''
		@curve : node , This is the curve is curve Node
		'''
		if curve is None:
			OpenMaya.MGlobal_displayError('@curve : This is the curve is None : curve = %s'%(curve))
			return
		CurveClusterList = []
		curveShape = curve.getShape()
		
		#num = curveShape.degree()+curveShape.spans.get()
		for CV in range(curveShape.degree()+curveShape.spans.get()):
			name = curve.name().replace('_cruve' , '_cluster_') + self.getTwoNnmber(CV + 1)
			CurveHandle , CurveCluster = pm.cluster(curve.cv[CV] , en = 1)
			
			CurveName = CurveCluster.rename(name)
			CurveName.setParent(self.featherClusterGroup)
			CurveClusterList.append(CurveName)

		return CurveClusterList


	def createCurves(self , object = None , type = 0 , attr = None ):
		'''
		@object : str , This is the object is object name
		@type : int , This is the type is sort
		@attr : list , This is the attr is add attr list
		'''
		if type > 1:
				OpenMaya.MGlobal_displayError('@type : The is great than 1 : type = %s'%(type))
				return 
		
		#name = self.getObjectName(object)
		
		name = object.replace('_1' , '')
		
		
		if type is 0:
			ctrName = pm.curve(n = name + '_ctrl' , d = 1 , p = [(0,0,0),(0,3,0),(0,4,1),(0,5,0),(0,4,-1),(0,3,0)] , k = [0,1,2,3,4,5])
			self.setAttrLock(ctrName,1,0)
			if attr != None:
				for att in attr :
					ctrName.addAttr(att , at = 'double' ,  k = 1)
			ctrNameGroup = self._objectGroup(ctrName)
			parentCon = pm.parentConstraint(object , ctrNameGroup , w = 1 )
			pm.delete(parentCon)
			OpenMaya.MGlobal_clearSelectionList()
			
			return ctrName
	
	
		if type is 1:
			ctrMName = pm.curve(n = name + '_M_ctrl' , d = 1 , p = [(0,0,0),(11,0,0),(13,0,-2),(15,0,0),(13,0,2),(11,0,0),(15,0,0),(13,0,-2),(13,0,2)] , k = [0,1,2,3,4,5,6,7,8])	
			ctrRightName = pm.curve(n = name + '_MRight_ctrl' , d = 1 , p = [(9,0,-2),(9,0,-1),(10,0,-1),(10,0,-2),(10.5,0,-2),(9.5,0,-3.2),(8.5,0,-2),(9,0,-2)] , k = [0,1,2,3,4,5,6,7])
			curLeftName = pm.curve(n = name + '_MLeft_ctrl' , d = 1 , p = [(9,0,2),(9,0,1),(10,0,1),(10,0,2),(10.5,0,2),(9.5,0,3.2),(8.5,0,2),(9,0,2)] , k = [0,1,2,3,4,5,6,7])	
			
			self.setAttrLock(ctrMName,1,0)
			self.setAttrLock(ctrRightName,1,0)	
			self.setAttrLock(curLeftName,1,0)
	
			ctrRightName.getShape().overrideEnabled.set(1)
			ctrRightName.getShape().overrideColor.set(18)
			curLeftName.getShape().overrideEnabled.set(1)
			curLeftName.getShape().overrideColor.set(18)
			ctrMName.getShape().overrideEnabled.set(1)
			ctrMName.getShape().overrideColor.set(6)	
			
			ctrNameGroup = self._objectGroup(ctrMName)
			ctrRightNameGroup = self._objectGroup(ctrRightName)
			curLeftNameGroup = self._objectGroup(curLeftName)
			
			ctrRightNameGroup.setParent(ctrMName)
			curLeftNameGroup.setParent(ctrMName)
			
			constr = pm.parentConstraint(object , ctrNameGroup ,w = 1)
			pm.delete(constr)
			
			ctrNameList = [ctrMName , curLeftName , ctrRightName] 
			
			OpenMaya.MGlobal_clearSelectionList()
			
			return ctrNameList
	
	
	
	def _createGroup(self):
		
#		if self.featherJointGroup is None:
			
		if pm.objExists('feather_joint_group') is False:
			self.featherJointGroup = pm.group(n = 'feather_joint_group' , em = 1)
	
		else :
			pm.select('feather_joint_group' , r = 1)
			self.featherJointGroup = pm.selected()[0] 
			
			
#		if self.featherIkHandGroup is None:
			
		if pm.objExists('feather_ikHand_group') is False:
			self.featherIkHandGroup = pm.group(n = 'feather_ikHand_group' , em = 1)
	
		else :
			pm.select('feather_ikHand_group' , r = 1)
			self.featherIkHandGroup = pm.selected()[0] 
		
		
		if pm.objExists('feather_ikCur_group') is False:
			self.featherIkCurGroup = pm.group(n = 'feather_ikCur_group' , em = 1)
	
		else :
			pm.select('feather_ikCur_group' , r = 1)
			self.featherIkCurGroup = pm.selected()[0] 
			
		
		if pm.objExists('globalScale_MD1') is False:
			self.globalScaleMD = pm.shadingNode('multiplyDivide' , asUtility=True , n = 'globalScale_MD1')
			
		else :
			pm.select('globalScale_MD1' , r = 1)
			self.globalScaleMD = pm.selected()[0]
			
			
		
		if pm.objExists('feather_cluster_group') is False:
			self.featherClusterGroup = pm.group(n = 'feather_cluster_group' , em = 1)
	
		else :
			pm.select('feather_cluster_group' , r = 1)
			self.featherClusterGroup = pm.selected()[0]
		
		
		if pm.objExists('featherCtrl_M_G') is False:
			self.featherCtrlGroup = pm.group(n = 'featherCtrl_M_G' , em = 1)
	
		else :
			pm.select('featherCtrl_M_G' , r = 1)
			self.featherCtrlGroup = pm.selected()[0]
		
		
		OpenMaya.MGlobal_clearSelectionList()
		
		
	
	def getObjectPoint(self , rootPoint = [0,0,0], endPoint = [0,0,0] , num = 3 , type = 0):
		'''
		@point1 : list , this is the point1 of the world Translate
		@point2 : list , this is the point1 of the world Translate
		@num : int , this is the num is number 
		@type : int , this is the type is sort
		'''
	
		if len(rootPoint) is not 3 or len(endPoint) is not 3:
			OpenMaya.MGlobal.displayError('@rootPoint and @endPoint is not list len is 3 : rootPoint = %s endPoint = %s'%(rootPoint ,endPoint))
			return
		if rootPoint ==  endPoint:
			OpenMaya.MGlobal.displayWarning('@rootPoint == @endPoint : rootPoint = %s endPoint = %s'%(rootPoint ,endPoint))
			return
		if type > 3:
			OpenMaya.MGlobal.displayError('@type : The is great than 3 : type = %s'%(type))
			return
		listPoint = []
		vec = [0,0,0]
		vec = [(v2-v1)/(num-1.0) for v2 ,v1 in zip(endPoint,rootPoint)]
		if type == 0:
			listPoint  = [[v3+n*v4 for v3 ,v4 in zip(rootPoint,vec)] for n in range(num-1) ]
			listPoint.append(list(endPoint))
			return listPoint
	
		if type == 1:
			endPointOne =  [vo1-(0.3*vo2) for vo1 , vo2 in zip(endPoint , vec)]
			listPoint = self.getObjectPoint(rootPoint,endPointOne,num)
			return listPoint 
			
		if type == 2:
			rootPointTwo =  [vo1+(0.3*vo2) for vo1 , vo2 in zip(rootPoint , vec)]
			endPointTwo =  [vo1-(0.3*vo2) for vo1 , vo2 in zip(endPoint , vec)]	
			listPoint = self.getObjectPoint(rootPointTwo,endPointTwo,num)
			return listPoint
			
		if type == 3:
			rootPointThree =  [vo1+(0.3*vo2) for vo1 , vo2 in zip(rootPoint, vec)]
			listPoint = self.getObjectPoint(rootPointThree,endPoint,num)
			return listPoint
			
			
			
				
	def ceratePlume(self , rootEndList = None):
		'''
		@rootEndList : list , This is the rootEndlist is number joint list
		'''
		if len(rootEndList[0]) is  not len(rootEndList[1]):
			OpenMaya.MGlobal.displayError('@rootEndList : Thes is @rootEndList[0] and @rootEndList[1] not even : len(rootEndList[0]) = %s != len(rootEndList[1]) = %s'%(len(rootEndList[0]) , len(rootEndList[1])))
			return
		addPlumeList = [] 
		for i in range(1 , len(rootEndList[0])-1):
			plumeRootName = rootEndList[0][i].name()
			rootName = plumeRootName.replace('front' , 'addFront')
			plumeEndName = rootEndList[1][i].name()
			endName = plumeEndName.replace('back' , 'addBack')
			OpenMaya.MGlobal_clearSelectionList()
			
			plumeRootJoint = pm.joint(n = rootName , p = rootEndList[0][i].getTranslation(space = 'world'))
			plumeEndJoint = pm.joint(n = endName , p = rootEndList[1][i].getTranslation(space = 'world'))
			
			pm.joint(plumeRootJoint , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)
			pm.joint(plumeEndJoint , e = True , zso = 1 , oj = "none" , ch = True)
			OpenMaya.MGlobal_clearSelectionList()
			
			addList = [plumeRootJoint , plumeEndJoint]
			addPlumeList.append(addList)
			
		return addPlumeList			
			
			
			
	def getObjectName(self , name = None):
		'''
		@name : str , This is the name is object name
		'''
		if name is None :
			OpenMaya.MGlobal_displayError('@name : thes is None : name = %s'%(name))
			return
		for i in range(10):
			if str(i) in name:
				objName = name.replace(str(i) , '')
		return objName
	
	
	
	def getTwoNnmber(self , int = 1):
		'''
		@int : int , This is the int of the number
		'''
		if len(str(int)) is 1:
			num = '0'+str(int)
		if len(str(int)) is 2:
			num = str(int)
		return num
	


	def _objectGroup(self , object = None):
		'''
		@object : str Node , This is the object of in is object 
		'''
		object_C = pm.group(n = object + '_C' ,em = 1)
		object_G = pm.group(object_C , n = object + '_G')
		self._getConstraint(object_G , object)
		pm.parent(object , object_C)
		OpenMaya.MGlobal_clearSelectionList()
		return  object_G
			
		
	def _getConstraint(self , sonObject = None , paterObject = None , pointConstra = True , orientConstra = True):
		'''
		@sonObject : str  node , This is the sonObject of is son Object 
		@parterObject : str Node , This is the parterObject is perter Object 
		@pointConstra : bool , This is the pointConstra is point Constraint
		@orientConstra : bool , This is the orientConstra is orient Constraint
		'''
		if sonObject is None or paterObject is None:
			 OpenMaya.MGlobal_displayError('@sonObject and @paterObject is None : sonObject = %s paterObject = %s'%(sonObject , paterObject))
			 return
		if pointConstra :
			constra = pm.pointConstraint(paterObject , sonObject , w = True)
			pm.delete(constra)
		if orientConstra :
			constra = pm.orientConstraint(paterObject , sonObject , w = True)
			pm.delete(constra)




	def setAttrLock(self , obj = None ,translate = True , rotate = True , scale = True , visibility = True ):
		'''
		@obj : str , This is the obj is tansform Node
		@translate : bool , This is the translate is object translate 
		@rotate : bool ,This is the rotate is object rotateilter
		@scale : bool , This is the scale is object scale 
		@visibility : bool , This is the visibility is object show
		'''
		attr = []
		if translate : attr += ['.tx','.ty','.tz']
		if rotate : attr += ['.rx','.ry','.rz']
		if scale : attr += ['.sx','.sy','.sz']
		if visibility : attr += ['.v']
		
		if obj is None:
			OpenMaya.MGlobal.displayError('@obj is None : obj = %s'%(obj))
			return 
		
		for a in attr:
			pm.setAttr(obj+a , l = True , k = False ,cb = False)

	

	def cerateFeatherJoint(self , rootPoint = None , endPoint = None , name = None , num = 1 , numRoot = 1):
		'''
		@rootPoint : list , This is the rootPoint of the root joint point
		@endPoint : list , This is the endPoint of the end joint point 
		@name : str , This is the name is joint name 
		@num : int , This is the num is number
		@numRoot : int , This is the numRoot is root joint number 
		'''
		number = self.getTwoNnmber(num)
		if not len(rootPoint) is len(endPoint):
			OpenMaya.MGlobal.displayError('@rootPoint and @endPoint not even : len(rootPoint) = %s len(endPoint) = %s'%(len(rootPoint),len(endPoint)))
			return 
		frontJointName = name+'_front'+number+'_'
		backJointName = name+'_back'+number+'_'
		tupleRootPoint = [(t1[0] , t1[1] , t1[2]) for t1 in rootPoint]
		tupleEndPoint = [(t2[0] , t2[1] , t2[2]) for t2 in endPoint]
		OpenMaya.MGlobal_clearSelectionList()
		frontJoint = [pm.joint(n = frontJointName + str(i1+numRoot) , p = point1 ) for i1 , point1 in enumerate(tupleRootPoint)]
		pm.joint(frontJoint[0] , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)
		pm.joint(frontJoint[-1] , e = True , zso = 1 , oj = "none" , ch = True)
		OpenMaya.MGlobal_clearSelectionList()
		backJoint = [pm.joint(n = backJointName + str(i2+numRoot) , p = point2 ) for i2 , point2 in enumerate(tupleEndPoint)]
		pm.joint(backJoint[0] , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)
		pm.joint(backJoint[-1] , e = True , zso = 1 , oj = "none" , ch = True)
		OpenMaya.MGlobal_clearSelectionList()
		
		frontBackList = [frontJoint,backJoint] 
		return frontBackList			
				
	
	def featherRootEndJoint(self , rootEndlist = None , frontRootNode = None , frontEndNode = None , backRootNode = None , backEndNode = None , type = 1 ):
		'''
		@rootEndlist : list , This is the rootEndlist is number joint list
		@frontRootNode : node , This is the frontRootNode is front root joint node
		@frontEndNode : node , This is the frontEndNode is front end joint node
		@backRootNode : node , This is the backRootNode is back root joint node
		@backEndNode : node , This is the backEndNode is back end joint node
		@type : int , this is the type is sort
		'''
		 
		frontAddList = []
		backAddList = []
		if type < 1 or type > 3 :
			OpenMaya.MGlobal_displayError('@type : The is great than 3 or less than 1 : type = %s'%(type))
			return 
		 
		numJoint = len(rootEndlist[0])
		if type == 1:
			frontEndName = rootEndlist[0][-1].replace(str(numJoint) , str(numJoint+1))
			backEndName = rootEndlist[1][-1].replace(str(numJoint) , str(numJoint+1))
			
			OpenMaya.MGlobal_clearSelectionList()
			frontEndJoint = pm.joint(n = frontEndName , a = True , p = backRootNode.getTranslation(space = 'world'))
			pm.parent(frontEndJoint ,  rootEndlist[0][-1])
			pm.joint(frontEndJoint , e = True , zso = 1 , oj = "none" , ch = True)
			OpenMaya.MGlobal_clearSelectionList()
			backEndJoint = pm.joint(n = backEndName , a = True ,  p = backEndNode.getTranslation(space = 'world') )
			pm.parent(backEndJoint ,  rootEndlist[1][-1])
			pm.joint(backEndJoint , e = True , zso = 1 , oj = "none" , ch = True)
			
			frontAddList += rootEndlist[0]
			frontAddList.append(frontEndJoint)
			
			backAddList += rootEndlist[1]
			backAddList.append(backEndJoint)
			
			frontBackAddList = [frontAddList , backAddList]
			return frontBackAddList
	
		if type == 3 :
			frontRootName = rootEndlist[0][-1].replace(str(numJoint+1) , str(1))
			backRootName = rootEndlist[1][-1].replace(str(numJoint+1) , str(1))
			
			OpenMaya.MGlobal_clearSelectionList()
			frontRootJoint = pm.joint(n = frontRootName , a = True , p = frontRootNode.getTranslation(space = 'world'))
			pm.parent(rootEndlist[0][0] ,frontRootJoint )
			pm.joint(frontRootJoint , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)
			OpenMaya.MGlobal_clearSelectionList()
			backRootJoint = pm.joint(n = backRootName , a = True ,  p = frontEndNode.getTranslation(space = 'world'))
			pm.parent(rootEndlist[1][0] , backRootJoint ) 
			pm.joint(backRootJoint , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)
			
			frontAddList.append(frontRootJoint)
			frontAddList += rootEndlist[0]
			
			backAddList.append(backRootJoint)
			backAddList += rootEndlist[1]
			
			frontBackAddList = [frontAddList , backAddList]
			return frontBackAddList
	
		if type == 2:
			frontRootName = rootEndlist[0][-1].replace(str(numJoint+1) , str(1))
			backRootName = rootEndlist[1][-1].replace(str(numJoint+1) , str(1))
			frontEndName = rootEndlist[0][-1].replace(str(numJoint+1) , str(numJoint+2))
			backEndName = rootEndlist[1][-1].replace(str(numJoint+1) , str(numJoint+2))
			
			OpenMaya.MGlobal_clearSelectionList()
			frontEndJoint = pm.joint(n = frontEndName , a = True , p = backRootNode.getTranslation(space = 'world'))
			pm.parent(frontEndJoint ,  rootEndlist[0][-1])
			pm.joint(frontEndJoint , e = True , zso = 1 , oj = "none" , ch = True)
			OpenMaya.MGlobal_clearSelectionList()
			backEndJoint = pm.joint(n = backEndName , a = True ,  p = backEndNode.getTranslation(space = 'world') )
			pm.parent(backEndJoint ,  rootEndlist[1][-1])
			pm.joint(backEndJoint , e = True , zso = 1 , oj = "none" , ch = True)		
			OpenMaya.MGlobal_clearSelectionList()
			frontRootJoint = pm.joint(n = frontRootName , a = True , p = frontRootNode.getTranslation(space = 'world'))
			pm.parent(rootEndlist[0][0] ,frontRootJoint )
			pm.joint(frontRootJoint , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)
			OpenMaya.MGlobal_clearSelectionList()
			backRootJoint = pm.joint(n = backRootName , a = True ,  p = frontEndNode.getTranslation(space = 'world'))
			pm.parent(rootEndlist[1][0] , backRootJoint ) 
			pm.joint(backRootJoint , e = True , zso = 1 , oj = "xyz" , sao = "yup" , ch = True)		
			
			
			frontAddList.append(frontRootJoint)
			frontAddList += rootEndlist[0]
			frontAddList.append(frontEndJoint)
			
			backAddList.append(backRootJoint)
			backAddList += rootEndlist[1]
			backAddList.append(backEndJoint)
			
			frontBackAddList = [frontAddList , backAddList]
			return frontBackAddList			





class AvesPlumePitchJiont(object):
	'''
	cerate go to joint  and  cerate mirror joint 
	'''
	pointlist = [[(2.472 , 1 , -0.394) , (2.585 , 1 , -5.022)] , 
				 [(4.635 , 1 , -0.762) , (5.338 , 1 , -5.064)] ,
				 [(7.131 , 1 , -0.359) , (8.206 , 1 , -5.002)] ,
				 [(9.471 , 1 , -0.606) , (11.12 , 1 , -5.002)] ,
				 [(11.33 , 1 , -0.010) , (13.63 , 1 , -2.969)]	
				]
	
	
	
	def __init__(self , num = 6):
		
		self.int = 1
		
		self.num = num
		
		self.nameLsit = ['wingBottom' ,'wingElbow' , 'wingsTail' , 'wings' , 'wingTips']
		
		self.leftList = []
		self.rightList = []
		
		
		self.plume = None
		self.mirrorPlume = None
		
		self.addPlume = []
		self.addMirrorPlume = []
		self.addJoint = []
		
	def biud(self , num = None):
		'''
		********buid*********
		'''
		if num:
			self.num = num
		self.plume = AvesPlumeJiont(self.num)
		

		
		if self.leftList == []:
			if self.rightList == []:
				OpenMaya.MGlobal_displayError('This is self.rightList is [] : %s'%self.rightList)
				return
			try :
				pm.select(self.rightList)
		
			except:
				logger.error("obj not nonentity : %s"%(self.leftList))	
				return	
				
			OpenMaya.MGlobal_clearSelectionList()	
			self.leftList =self._mirrorJoint(self.rightList)
			self.plume.featherJoint(self.rightList)
			self.mirrorPlume = AvesPlumeJiont(self.num)
			self.mirrorPlume.featherJoint(self.leftList)
			
		if self.rightList == []:
			if self.leftList == []:
				OpenMaya.MGlobal_displayError('This is self.leftList is [] : %s'%self.leftList)
				return
			try :
				pm.select(self.leftList)
		
			except:
				logger.error("obj not nonentity : %s"%(self.leftList))
				return 
			
			OpenMaya.MGlobal_clearSelectionList()		
			self.rightList = self._mirrorJoint(self.leftList)
			self.plume.featherJoint(self.leftList)
			self.mirrorPlume = AvesPlumeJiont(self.num)
			self.mirrorPlume.featherJoint(self.rightList)
	
	
	def _addBiudPitchJoint(self):
		
		addJoint = AvesPlumePitchJiont()
	
		addJoint._biudPitchJoint('add' + str(self.int))
		
		self.addJoint.append(addJoint)
			
	def addBuid(self , num =None):
		if num :
			self.num = num
		
		addPlume = AvesPlumeJiont(self.num)
		
		self.addPlume.append(addPlume)
		
		if self.leftList == []:
			OpenMaya.MGlobal_displayError('This is self.leftList is [] : %s'%self.leftList)
			return
				
		self.addJoint[self.int-1].rightList = self._mirrorJoint(self.addJoint[self.int-1].leftList)
		self.addPlume[self.int-1].featherJoint(self.addJoint[self.int-1].leftList)
		MirrorAddPlume = AvesPlumeJiont(self.num)
		self.addMirrorPlume.append(MirrorAddPlume)
		self.addMirrorPlume[self.int-1].featherJoint(self.addJoint[self.int-1].rightList)
				
		for l in range(len(self.leftList)):
			l_addjointGroup = self.addPlume[-1].featherDir[self.addJoint[-1].leftList[l].name()][0].getParent().getParent()
			l_jointCtrl = self.plume.featherDir[self.leftList[l].name()][0]
			
			l_addjointGroup.setParent(l_jointCtrl)	
				
		
		for r in range(len(self.rightList)):
			
			r_addjointGroup = self.addMirrorPlume[-1].featherDir[self.addJoint[-1].rightList[r].name()][0].getParent().getParent()
			
			r_jointCtrl = self.mirrorPlume.featherDir[self.rightList[r].name()][0]
			
			
			r_addjointGroup.setParent(r_jointCtrl)


			
		self.int += 1			
		
		OpenMaya.MGlobal_clearSelectionList()
		
	
	def _mirrorJoint(self , list = None):
		'''
		cerate mirror joint 
		@list : list , is list
		'''
		if list[0].name().find('R') is -1 :
			
			mirrorName =  [pm.mirrorJoint(a , mirrorYZ = 1 ,mirrorBehavior =1 ,searchReplace =('L' , 'R'))[0] for a in list]
			pm.select(mirrorName)
			mirrorNameList = pm.selected()
			OpenMaya.MGlobal_clearSelectionList()
			return mirrorNameList
		if list[0].name().find('L') is -1 :
			mirrorName =  [pm.mirrorJoint(a , mirrorYZ = 1 ,mirrorBehavior =1 ,searchReplace =('R' , 'L'))[0] for a in list]
			pm.select(mirrorName)
			mirrorNameList = pm.selected()
			OpenMaya.MGlobal_clearSelectionList()
			return mirrorNameList	
	

	def readinJoint(self):
		'''
		'''
		sel = pm.selected()
		if sel ==[]:
			logger.error('not select onj')
			return
		if sel[0].name().find('L') is -1 :
			self.rightList = [a for a in sel]

		if sel[0].name().find('R') is -1 :
			self.leftList = [a for a in sel]

			
		
	def _biudPitchJoint(self , addName = None):
		'''
		@cerate go to joint 
		'''
		jointList = []
		for jint in self.pointlist:
			jnt1 = [pm.joint(p = po) for po in jint]
			jnt1[0].orientJoint('xyz' , sao = 'yup')
			jnt1[-1].orientJoint('none')
			OpenMaya.MGlobal_clearSelectionList()
			jointList.append(jnt1)
		jointRenameList = self._PitchJointName(jointList , addName)
		
		self.rightList = []
		self.leftList = []
		
		if jointRenameList[0][0].name().find('L') is -1 :
			self.rightList = [a[0] for a in jointRenameList]
		if jointRenameList[0][0].name().find('R') is -1 :
			self.leftList = [a[0] for a in jointRenameList]			
			
	def _PitchJointName(self , jointList = None , add = None):
		'''
		@jointList : lisr , This is the jointList is joint list  
		'''
		renameList = [] 		
		if len(jointList) is len(self.nameLsit):
			for index , joint in enumerate(jointList):
				bor = self.getBorder(joint[0])
				if add is None:
					name1 = joint[0].rename(bor + '_' + self.nameLsit[index]+'1')
					name2 = joint[1].rename(bor + '_' + self.nameLsit[index]+'2')
				else:
					name1 = joint[0].rename(bor + '_' + add + self.nameLsit[index]+'1')
					name2 = joint[1].rename(bor + '_' + add + self.nameLsit[index]+'2')
				name3= [name1 , name2]
				renameList.append(name3)
		return renameList	
			
	def getBorder(self , object = None):
		'''
		@object : Node , This is the object is transform node
		'''
		border = ['L' , 'R']
		objectX = object.getTranslation(space = 'world')[0]
		if objectX > 0 :
			return border[0]
		if objectX < 0 :
			return border[1]		 








class Control(object):
	def __init__(self , side = 'C' , baseName = 'control' , size = 1 , objColor = 'yellow' , aimAxis = 'x') :
		'''
		This is the constructor
		
		[in] baseName : this is ths name that will be used as a base for all the names
		[in] side : this is ths side that will be used as a base for all the names
		[in] size : this is ths size that will be used for the control
		objColor : string , specify the color of the chain 
		[in] aimAxis : this is ths aim axis used to orient the control , use only vector dor x , y , z and their negatives
		'''
		
		self.baseName    = baseName
		
		self.side        = side
		
		self.objColor    = objColor
		
		self.size        = size
		
		self.aimAxis     = aimAxis
		
		
		
		self.control = None
		self.controlGrp_C = None
		self.controlGrp_G = None
		self.controlName = None
		
	
	def circleCnt(self):
		'''
		This procedure creates a circle control
		'''
		
		self.__buildName()
		if self.controlName:
			self.control = pm.circle( name = self.controlName , ch = 0 , o = 1 , nr = [ 1 , 0 , 0 ] ) [ 0 ]
		
		
		self.__finalizeCnt()	
		
	def sphereCnt(self):
		'''
		This procedure creates a sphere control
		'''
		
		self.__buildName()
		if not self.controlName:
				return
		circle1 = pm.circle( ch = 0 , o = True , nr = ( 1 , 0 , 0 ) , n = self.controlName) [0]
		circle2 = pm.circle( ch = 0 , o = True , nr = ( 0 , 1 , 0 ) ) [0]
		circle3 = pm.circle( ch = 0 , o = True , nr = ( 0 , 0 , 1 ) ) [0]
		
		pm.parent(circle2.getShape() , circle1 , shape = 1, add = 1)
		pm.parent(circle3.getShape() , circle1 , shape = 1, add = 1)
		
		pm.delete(circle2 , circle3)
		self.control = circle1
		
		self.__finalizeCnt()

	def pinCnt(self):
		'''
		This procedure creates a pin control
		'''
		
		self.__buildName()
		if not self.controlName:
			return
		line = pm.curve( d = 1 , p = [ ( 0 , 0 , 0 ) , ( 0.8 , 0 , 0 ) ] , k = [ 0 , 1 ] , n = self.controlName)
		circle = pm.circle( ch = 1 , o = True , nr = ( 0 , 1 , 0 ) , r = 0.1 ) [ 0 ]
		
		pm.move( 0.9 , 0 , 0 ,circle.getShape().cv , r = 1 )
		pm.parent( circle.getShape() , line , shape = 1 , add = 1 )
		
		pm.delete(circle)
		pm.select(cl = 1 )
		self.control = line
		
		self.__finalizeCnt()
		
		
	def __buildName(self):
		'''
		This fucntion creates the name of the control
		'''		
		
		self.controlName = self.side + '_' + self.baseName + '_crtl' 
		
		
	def __finalizeCnt(self):
		'''
		This funtion is in charge for orienting , scaling and zeroing the control
		'''		
		
		self.__aimCnt()
		
		if self.size != 1 :
			
			for s in self.control.getShapes():
				pm.scale(s.cv , self.size , self.size , self.size , r = 1 )
		
		
			pm.delete(self.control , ch = 1 )
		
		
		self.__group(self.control)
		
		
	def __aimCnt(self):
		'''
		This procedure let s you correctly aim thr control based on the provide aimAxis
		'''
		
		y = 0
		z = 0
		
		if self.aimAxis == 'y':
			z = 90
			
		elif self.aimAxis == 'z':
			y = -90
		
		
		for s in self.control.getShapes():
			pm.rotate(s.cv , 0 , y , z , r = 1 )


	def __group(self , obj = None):
		'''
		obj : PyNode , the object to zeroOut
		PyNode , the offset group
		'''
		
		par = obj.getParent()
		
		name = obj.name()
		
		groupName1 = name + '_C'
		
		groupName2 = name + '_G'
		
		if not groupName1:
			return
		
		if not groupName2:
			return	
				
		self.controlGrp_C = pm.createNode( 'transform', n = groupName1 )
		
		self.controlGrp_G = pm.createNode( 'transform', n = groupName2 )
		
		self.controlGrp_C.setMatrix(obj.wm.get())
		
		self.controlGrp_G.setMatrix(obj.wm.get())
		
		obj.setParent(self.controlGrp_C)
		
		self.controlGrp_C.setParent(self.controlGrp_G)
		if par :
			self.controlGrp_G.setParent(par)
		
		









