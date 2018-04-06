#!usr/bin/env python
#coding:utf-8

#//--------------------------------------------------------------
#//	Script:     lz_subCtl_doIt.py
#//	Descr:		给角色添加次级控制器
#//--------------------------------------------------------------

global lz_subCtls
global lz_subCtl_ornObj
from maya.cmds import *
import random,sys, webbrowser, re
import maya.mel as mm

lz_subCtls =[]
lz_subCtl_ornObj=''
global lz_face_sub
global lz_face_main
global lz_face_all
global lz_master_sub
lz_face_sub = 'Face_Sub'
lz_face_all= 'Face_All'
lz_face_main= 'Face_Main'
lz_master_sub= 'MASTER_SUB'

global lz_rename_level
lz_selection,lz_rename_level=[],0
global lz_skin_skinSys
lz_skin_skinSys = 0

def lz_rand_rename(objects=[],rand = ['','New'],rep = ['','']):
	if not objects:
		objects = ls(sl=1,fl=1)
	objects_new = ['']*len(objects)
	objects_len = {}
	#rand_number = []
	for index,obj in enumerate(objects):
		res = obj.split('|')
		t_l = len(res)
		if t_l not in objects_len:
			objects_len[t_l] = [[obj,index]]
		else :
			objects_len[t_l].append([obj,index])
	sort_key = objects_len.keys()
	sort_key.sort(None,None,1)
	for key in sort_key:
		for sub_item in objects_len[key]:
			res = sub_item[0].split('|')
			
			if res[0] == sub_item[0]:
				if not rep[0]:
					finnaly_name = sub_item[0] 
				else:
					finnaly_name = sub_item[0].replace(rep[0],rep[1],1)
			else: 
				if not rep[0]:
					finnaly_name = rand[0]+res[-1]+rand[1]+"#"	
				else:
					finnaly_name = res[0].replace(rep[0],rep[1],1)
			
			objects_new[sub_item[1]] = rename(sub_item[0],finnaly_name)

	return objects_new

def lz_connectAttr(attr1,attr2):
	attr_split = ''
	if attr1 and attr2:
		attr_split = attr2.split('.')
		if objExists(attr_split[0]):
			conn = listConnections(attr2,p=1)
			if conn and conn[0] == attr1:
				return
	try:
		locked = getAttr(attr2,l=1)
		if locked:
			lz_hideAttr(attr_split[0],[attr_split[1]],1)
		connectAttr(attr1,attr2,f=1)
		if locked:
			lz_hideAttr(attr_split[0],[attr_split[1]])
	except:
		pass

def lz_subCtl_rename():
	sled = ls(sl=1,fl=1)
	res = []
	if not sled:
		return []
	res_split = sled[0].split('.')
	res.append(res_split[0])
	if res[0] == sled[0]:
		res = lz_rand_rename(res,rand = ['',''])
	else:
		res = lz_rand_rename(res,rand = ['',''])
		res.append(res[0]+'.'+res_split[1])
	return res

def lz_hideAttr(obj,attr,reverse=0,v=0):
	objects = []
	temp = ['x','y','z']
	if isinstance(obj,list):
		objects = obj
	else:
		objects =[obj]
	for o in objects:
		if not o:
			continue
			
		for i in attr:
			if i == 't' or i == 'r' or i == 's':
				try:
					for t in temp:
						if not reverse:
							setAttr('%s.%s'%(o,i+t),k=False,channelBox=v,lock=True)
						else:
							setAttr('%s.%s'%(o,i+t),channelBox=True,lock=False)
							setAttr('%s.%s'%(o,i+t),k=True)
				except:
					pass
			else:
				try:
					if not reverse:
						setAttr('%s.%s'%(o,i),k=False,channelBox=v,lock=True)
					else:
						setAttr('%s.%s'%(o,i),channelBox=True,lock=False)
						setAttr('%s.%s'%(o,i),k=True)
				except:
					pass
	
def lz_rigTool_delBld(res = [],attr=''):
	res = lz_ls() if not res else res
	if not res[0] or not objExists(res[0]):
		return 0
	for r in res:
		if objectType(r) == 'blendShape':
			res = r
			break
	if not attr :
		attr = channelBox('mainChannelBox',q=1,sha=1)
		if not attr:
			attr = channelBox('mainChannelBox',q=1,sma=1)
			if not attr:
				lz_print('请在通道栏上选择要删除的blendShape名！\\n')
				return 0
		attr = attr[0]
	if not attr or not objExists(attr):
		select(res)
		return 0

	if not attributeQuery(attr,node=res,ex=1):
		select(res)
		return 0
	cout = blendShape(res,q=1,wc=1)
	for i in range(cout):
		setAttr('%s.weight[%d]'%(res,i),0)
	
	setAttr('%s.%s'%(res,attr),1)
	weight = getAttr('%s.weight'%res)[0]
	obj_index = -1
	for index,w in enumerate(weight):
		if w >0:
			obj_index = index
			break
	obj = listConnections('%s.inputTarget[0].inputTargetGroup[%d].inputTargetItem[6000].inputGeomTarget'%(res,obj_index))
	if obj and objExists(obj[0]):
		blendShape(res,e=1,rm=1,t=[obj[0],cout,obj[0],1])
	else:
		#设置组合比较多，要找正确的shape就要翻历史
		fu = listHistory(res,f=1,gl=2)
		for f in fu:
			if f.find('Shape') !=-1 :
				shape = f
				break
		outObj = listRelatives(shape,p=1,pa=1)[0]
		attr_geo = duplicate(outObj,n=attr)[0]
		shape = listRelatives(attr_geo,s=1,pa=1)[0]
		lz_connectAttr('%s.worldMesh[0]'%shape,'%s.inputTarget[0].inputTargetGroup[%d].inputTargetItem[6000].inputGeomTarget'%(res,obj_index))
		lz_connectAttr('%s.worldMesh[0]'%shape,'%s.input[%d].inputGeometry'%(res,obj_index))
		blendShape(res,e=1,rm=1,t=[attr,cout,attr,1])
		delete(attr)
	select(res)

def lz_addBlend(obj,obj_dup='',surffix = '_dup',blend_name = 'blendShape#',weight = 1):
	shape,blend_now= '',''
	shapes = listRelatives(obj,pa=1)
	his = listHistory(obj,ag=1,gl=2,pdo=1)
	len_his = 0
	if his:
		len_his = len(his)
		if not shapes:
			return []
		for s in shapes:
			temp_his = listHistory(s,ag=1,gl=2,pdo=1)
			if temp_his and len(temp_his) == len_his:
				shape = s
		#找到现有的blendShape
		for h in his:
			if(objectType(h) == 'blendShape'):
				if getAttr('%s.envelope'%h):
					blend_now = h
	else:
		shape = shapes[0]
		

	if not blend_now:
		obj_dup = duplicate(obj,n=obj+surffix)[0] if not obj_dup else obj_dup
		blend_now = blendShape(obj_dup,obj,weight=[0,weight],n=blend_name)[0]
		if len_his >=2:
			his_tar = his[-2]
			if his_tar!=blend_now:
				reorderDeformers(his_tar,blend_now,obj)
				
	else:		
		values = blendShape(blend_now,q=1,weight=1)		
		count = blendShape(blend_now,q=1,wc=1)
		setAttr('%s.envelope'%blend_now,0)
		'''
		if values:
			for index,c in enumerate(values):#blend归0
				try:
					blendShape(blend_now,e=1,weight=[index,0])
				except:
					pass	
		'''			
		obj_dup = duplicate(obj,n=obj+surffix)[0] if not obj_dup else obj_dup
		'''
		if values:
			for index,v in enumerate(values):#blend恢复
				try:
					blendShape(blend_now,e=1,weight=[index,v])	
				except:
					pass
		'''			
		setAttr('%s.envelope'%blend_now,1)			
		objs = listConnections('%s.inputTarget'%(blend_now))
		if not objs or obj_dup not in objs:
			blendShape(blend_now,e=True,t=[obj,count,obj_dup,1],weight=[count,weight])

	return (obj_dup,blend_now)	

def lz_addAttr(obj,targets=[],sources=[],ln='fk_ik_snapMode',h= 0,at='enum',en='',k=1,cb=1,value=0):
	flag = 0
	if not attributeQuery(ln,node=obj,ex=1):
		if at!='string' and at!='stringArray':
			addAttr(obj,ln=ln,at=at,en=en)
		else:
			addAttr(obj,ln=ln,dt=at,en=en)
		flag = 1
	if not h:
		try:		
			#type = at if at=='string' else ''		
			setAttr('%s.%s'%(obj,ln),value,cb=cb)
			setAttr('%s.%s'%(obj,ln),keyable=k)
		except:
			pass
	for tar in targets:
		lz_connectAttr('%s.%s'%(obj,ln),tar)
	for sou in sources:
		lz_connectAttr(sou,'%s.%s'%(obj,ln))
	return flag

def lz_findCluster(obj,type=''):
	global lz_skin_skinSys
	sk = ''
	history ='' 
	if not type:
		if lz_skin_skinSys ==0:
			type = 'skinCluster'
		if lz_skin_skinSys ==1:
			type = 'fmSkinCluster'
		if lz_skin_skinSys ==2:
			type = 'cMuscleSystem'	
	if obj:
		history = listHistory(obj,ag=1,gl=2,pdo=1)#避免dg节点影响
	if not history:
		return sk
	#找到需要的skinCluster
	for h in history:
		t = objectType(h)
		if t and t==type:
			sk=h
			break
	return sk

def lz_subCtl_veToFace(poly,selectionRaw):
	res,raw_res,componentF = [],[],'%s.f[%s]'
	componentV = '%s.vtx[%s]'
	res_inf = []
	for item in selectionRaw:
		vtx_index,edge_vtx,face_vtx = [],[],[]
		if item.find('.vtx[')!=-1:
			temp_info = polyInfo(item,vf=1)[0]
			res.append(componentF%(poly,lz_polyPin_getInfo(temp_info)[0]))
			raw_res.append(item)
			lz_mirrorSelection_getIndex(vtx_index,[item])
			res_inf.append(vtx_index)
		elif item.find('.e[')!=-1:
			temp_info = polyInfo(item,ef=1)[0]
			res.append(componentF%(poly,lz_polyPin_getInfo(temp_info)[0]))
			raw_res.append(item)
			edge_vtx = polyListComponentConversion(item,fe=1,tv=1)
			lz_mirrorSelection_getIndex(vtx_index,edge_vtx)
			res_inf.append(vtx_index)
		elif item.find('.f[')!=-1:
			res.append(item)
			raw_res.append(item)
			face_vtx = polyListComponentConversion(item,ff=1,tv=1)
			lz_mirrorSelection_getIndex(vtx_index,face_vtx)
			res_inf.append(vtx_index)
	return [res,raw_res,res_inf]

def lz_polyPin_getInfo(rawInput):
	res = []
	temp_input = rawInput.split(" ")
	for item in temp_input:
		if item:
			res.append(item) 
	return res[2:-1]

def lz_mirrorSelection_getIndex(points,sl):
	if not sl:
		return 0 
	if not isinstance(sl,list):
		sl = [sl]
	po_splits = []
	for point in sl:
		if point.find('.')!=-1:
			if sl[0].find('][')!=-1:
				po_splits = point.split('.')[1].split('][')
			else:
				po_splits = [point.split('.')[1]]
		else:
			po_splits = [point]
		po_splits_len = len(po_splits)
		temp_list = []
		po_list = []
		for item in po_splits:
			po_all = item.split(':')
			po_len = len(po_all)
			if po_len!=1:
				point_match01,point_match02= re.search('(\d+)',po_all[0]),re.search('(\d+)',po_all[1])
				point_start,point_end = int(point_match01.groups()[0]),int(point_match02.groups()[0])
				po_list = range(point_start,point_end+1)
			else:
				point_match01 = re.search('(\d+)',po_all[0])
				if point_match01:
					po_list = [int(point_match01.groups()[0])]
			temp_list.append(po_list)#存放数据格式为[[1,2,3,4],[3,4,5],[3]]
		
		for i1 in temp_list[0]:
			if po_splits_len == 1:
				points.append(i1)
			else:
				for i2 in temp_list[1]:
					if po_splits_len == 2:
						points.append([i1,i2])
					else:
						for i3 in temp_list[2]:
							points.append([i1,i2,i3])

def lz_subCtl(initObj,poly ='',ctls=[],noJoint= 1,color='lr',ctl_style =2,controler_scale=2,ctl_name=0,addInf = 1,components=[],uvAuto=[],sled_obj=[],inf_vtx=[],parentGrp=[]):
	global lz_subCtl_ornObj
	global lz_face_sub
	global lz_face_all

	attach_grps,attach_locs,skin_object = [],[],[]
	joints_return,subCtlsGrps,subCtls,subHideCtlsGrps = [],[],[],[]
	subCtl_grp,subCtl='',''
	init		= Lz_Init(joints=[initObj])
	scale_grp,joint_parent= 'lz_scale',init.joint_parent
	rand,prefix,joints,length,joint_parent,joint_realParent = init.rand,init.prefix,init.joints,init.length,init.joint_parent,init.joint_realParent
	setup_parent = init.setup_parent
	setup_grp,ctls_grp,surfaces_grp,joints_grp,com_grp,local_grp,rawJoints,rawJntGrp= init.setup_grp,init.ctls_grp,init.surfaces_grp,init.joints_grp,init.com_grp,init.local_grp,init.rawJoints,init.rawJntGrp
	parent(initObj,joints_grp)

	#if noJoint:
	delete(rawJntGrp)
	pa_face = ''
	for item in listConnections('%s.message'%poly):
		if item == lz_face_sub:
			pa_face= lz_face_sub
	if not pa_face:
		if parentGrp:
			parentGrp = group(em=True,n=parentGrp) if not objExists(parentGrp) else parentGrp
			parent(setup_parent,parentGrp)
		if objExists('FUNC') and parentGrp == 'MASTER_SUB':
			if not listRelatives(parentGrp,p=1,pa=1) :
				parent('MASTER_SUB','FUNC')
	else:
		parent(setup_parent,pa_face)
	sub_attachGrp	= group(em=1,n=prefix+'attachGrp')
	parent([sub_attachGrp],com_grp)
	setAttr('%s.v'%sub_attachGrp,0)
	lz_delete([prefix+'stdAxis',prefix+'localAxis'])
	#处理一下components
	attach_upperGrp =sub_attachGrp if not pa_face else 'MASTER_SUB'
	res_return = lz_pin(components,object = poly,attach_upperGrp =sub_attachGrp,scale_grp =scale_grp,addJoint=0,addCtl=0,simple=1,objParent = 0)
	attach_grps = res_return[1]
	attach_locs = res_return[2]
	normals		= res_return[4]
	inf_vtx		= res_return[5]
	
	#找sk的级别关系
	sk = lz_findCluster(poly,type='skinCluster')
	
	if not ctls:
		for index,item in enumerate(attach_locs):
			select(cl=1)
			trans = xform(item,q=1,ws=1,rp=1)
			joints_return.append(joint(p=trans,radius=.5,n=prefix+"joint_"+str(index)))
		joints_grps = lz_group(joints_return,'_grp')
		parent(joints_grps,joints_grp)
		lz_hideAttr(joints_grps,['s','v'])
		ctl = lz_ctl_factory(ctl_style)
		aim_grp = group(em=1)	
	else:
		joints_return = ctls#joints_return被换成了现有的ctls
	skin_object = 	joints_return
	for index,item in enumerate(joints_return):
		if not ctls:
			subCtl = duplicate(ctl,n=  prefix+'ctl_'+str(index))[0]			
			subCtl_grp,subCtl_drivenMove,subCtl_drivenGrp,subCtl_move = group(subCtl,n=subCtl+'_grp'),group(subCtl,n=subCtl+'_drivenMove'),group(subCtl,n=subCtl+'_drivenGrp'),group(subCtl,n=subCtl+'_move')
			lz_xform([subCtl_grp,subCtl_drivenMove,subCtl_move,subCtl_drivenGrp],subCtl)
			scale(controler_scale*0.4,controler_scale*0.4,controler_scale*0.4,subCtl_grp)
			makeIdentity(subCtl_grp,a=1,s=1)
			if ctl_style ==3 or ctl_style==4:
				normalInfo = normals[index]
				setAttr('%s.t'%aim_grp,normalInfo[0],normalInfo[1],normalInfo[2])
				aimConstraint(aim_grp,subCtl_grp,aimVector=[0,1,0],upVector=[0,1,0],worldUpType="vector",worldUpVector=[0,1,0])
				aimConstraint(aim_grp,subCtl_grp,rm=1)
				if ctl_style ==3:
					lz_rotateCV([subCtl],rt = [0,0,90])
				ro = getAttr('%s.r'%subCtl_grp)[0]
				setAttr('%s.r'%subCtl_grp,0,0,0)
				lz_rotateCV([subCtl],rt = ro)		
			lz_xform(subCtl_grp,attach_locs[index],0)

		else:	
			if ctl_name:
				joints_return[index] = rename(item,item+'_raw')
			
			subCtl = lz_duplicateObj(joints_return[index],item)[0]
			
			delete(listRelatives(joints_return[index],s=1,pa=1,type='nurbsCurve'))
			newitem = item 
			joints_return[index] = rename(item,item+'#')
			subCtl  = rename(subCtl,newitem)
			subCtl_grp = duplicate(subCtl,po=1,n= subCtl+'_grp')[0]
			parent(subCtl,subCtl_grp)
			subCtl_drivenMove,subCtl_drivenGrp,subCtl_move =group(subCtl,n=subCtl+'_drivenMove'),group(subCtl,n=subCtl+'_drivenGrp'),group(subCtl,n=subCtl+'_move')
			
			lz_xform([subCtl_grp],attach_locs[index])
			lz_xform([subCtl_move,subCtl_drivenGrp,subCtl_drivenMove],item)	

			
		subCtl_hide = duplicate(subCtl_drivenGrp,po=1,n=subCtl+'_hide')[0]
		subCtl_hideGrp = group(subCtl_hide,n=subCtl_hide+'Grp')
		subCtl_hideCo = duplicate(subCtl_hide,po=1,n=subCtl+'_hideCo')[0]
		subCtl_hideCoGrp = group(subCtl_hideCo,n=subCtl_hideCo+'Grp')	
		subCtl_hide_pa = group(subCtl_hideCoGrp,n=subCtl+'_paGrp')		
		lz_xform([subCtl_hideCoGrp,subCtl_hideGrp,subCtl_hideCo,subCtl_hide,subCtl_hide_pa],item)
		connectAttr('%s.t'%subCtl_drivenGrp,'%s.t'%subCtl_hideCoGrp)
		connectAttr('%s.r'%subCtl_drivenGrp,'%s.r'%subCtl_hideCoGrp)
		connectAttr('%s.s'%subCtl_drivenGrp,'%s.s'%subCtl_hideCoGrp)
		connectAttr('%s.t'%subCtl,'%s.t'%subCtl_hideCo)
		connectAttr('%s.r'%subCtl,'%s.r'%subCtl_hideCo)
		connectAttr('%s.s'%subCtl,'%s.s'%subCtl_hideCo)
		parentConstraint(subCtl_hideCo,subCtl_hide,mo=1)
		scaleConstraint(subCtl_hideCo,subCtl_hide,mo=1)
		#lz_xform(joint_realParent,attach_locs[index])
		if lz_subCtl_ornObj and objExists(lz_subCtl_ornObj):
			inf_obj = lz_subCtl_ornObj
		else:
			if sk :			
				inf_obj = lz_subCtl_infObject(poly,sk,inf_vtx[index])
			else:
				inf_obj = poly
		lz_addAttr(subCtl,sources=['%s.message'%subCtl_grp],ln='upperGrp',h=1,at='message',en='')
		lz_addAttr(subCtl,sources=['%s.message'%inf_obj],ln='ornObj',h=1,at='message',en='')
		#orientConstraint(attach_locs[index],subCtl_grp,mo=1)
		#subCtlGrp_antiCon = lz_subCtl_link2(subCtl_drivenGrp,subCtl_drivenMove)
		
		link_return = lz_subCtl_link(subCtl_hide,subCtl,subCtl_drivenGrp,subCtl_move
			,subCtl_drivenMove,subCtl_hideCo,subCtl_hideCoGrp,joints_return[index])
		subCtl_antiCon,subCtlGrp_antiCon = 	link_return[1],link_return[0]
		inf_obj_dup = group(em=1,p=local_grp,n = prefix+'infObj_'+str(index))
		lz_xform(inf_obj_dup,subCtl_grp)
		parentConstraint(inf_obj,inf_obj_dup,sr=['x','y','z'],mo=1)
		lz_addAttr(subCtl_move,ln='surfaceFollow',at='double',targets=['%s.ft'%subCtl_antiCon,'%s.ft'%subCtlGrp_antiCon],k=0,cb=1,value=1)
		lz_addAttr(subCtl,sources=['%s.message'%inf_obj_dup],ln='ponObj',h=1,at='message',en='')
		#制作约束切换
		po = pointConstraint([inf_obj_dup,attach_locs[index]],subCtl_grp,mo=True,weight=0.0)[0]
		po_1 = orientConstraint(attach_locs[index],subCtl_grp,mo=True,weight=1)[0]
		list = pointConstraint(po,q=True,wal=True)
		for index,item in enumerate(list):
			condition = createNode('condition',n=subCtl_grp+'_cond#')
			connectAttr('%s.surfaceFollow'%subCtl_move,'%s.ft'%condition)
			setAttr('%s.st'%condition,index)
			setAttr('%s.ctr'%condition,1)
			setAttr('%s.cfr'%condition,0)
			connectAttr('%s.ocr'%condition,'%s.%s'%(po,item))
		
		lz_attrMaxMin('%s.surfaceFollow'%subCtl_move,max=1,min=0)
		lz_hideAttr(subCtl,['v'])
		lz_hideAttr([subCtl_move,subCtl_drivenMove],['t','s','r','v'])
		#额外的组，用来做旋转目标体。
		subCtl_aimOrn = group(em=1,p=subCtl_grp,n=subCtl+'_aimOrn')
		connectAttr('%s.r'%subCtl_hide,'%s.r'%subCtl_aimOrn)
		subCtlsGrps.append(subCtl_grp)
		subCtls.append(subCtl)		
		subHideCtlsGrps.append(subCtl_hideGrp)
	if not ctls:
		delete([ctl,aim_grp])
		#lz_hideAttr(joints_return,['v','t','r','s'])
	else:
		for item in ctls:
			pass#setAttr('%s.v'%item,0)
	parent(subCtlsGrps,ctls_grp)
	parent(subHideCtlsGrps,ctls_grp)
	setAttr('%s.v'%joints_grp,0)
	lz_setColor(subCtls,color)
	lz_hideAttr(subCtlsGrps,['s','v'])
	lz_hideAttr(attach_locs+attach_grps,['v','t','r','s'])
	connectAttr('%s.s'%scale_grp,'%s.s'%ctls_grp)
	connectAttr('%s.r'%scale_grp,'%s.r'%ctls_grp)
	if ctl_name:
		delete(joints_grp)
	return  [skin_object,subCtls,setup_parent]

class Lz_Init(object):
	def __init__(self,auto_setup=[],joints=[],scale_grp ='',joint_parent ='',rootFirst = 0,anti_axis = 0,prefix = '',empty=0,world = 0,xformReal =0):
		self.lz_all	= group(em=True,n='lz_all') if not objExists('lz_all') else 'lz_all'
		self.lz_setup	= group(em=True,p='lz_all',n='lz_setup') if not objExists('lz_setup') else 'lz_setup'
		
		self.lz_world	= group(em=True,p='lz_all',n='lz_world') if not objExists('lz_world') else 'lz_world'
		self.lz_extra	= group(em=True,p='lz_all',n='lz_extra') if not objExists('lz_extra') else 'lz_extra'
		self.lz_pins	= group(em=True,p='lz_all',n='lz_pin')	 if not objExists('lz_pin') else 'lz_pin'
		#self.lz_surfaces=group(em=True,p='lz_all',n='lz_surfaces') if  not objExists('lz_surfaces') else 'lz_surfaces'
		self.rand	= str(random.randint(0,100))	
		self.joints,self.dupJoints,self.dupJntGrp	= [],[],''
		if not objExists('lz_scale'):
			self.lz_scale	= group(em=True,p='lz_all',n='lz_scale') 
			setAttr('%s.inheritsTransform'%self.lz_scale,0)
			lz_hideAttr([self.lz_scale],['inheritsTransform'])
			orientConstraint(self.lz_all,self.lz_scale,mo=1)
			scaleConstraint(self.lz_all,self.lz_scale)
		else:
			self.lz_scale	= 'lz_scale'		
		if not objExists('lz_extra'):
			self.lz_extra	= group(em=True,p='lz_all',n='lz_extra') 
			setAttr('%s.inheritsTransform'%self.lz_extra,0)
			lz_hideAttr([self.lz_extra],['inheritsTransform'])
		else:
			self.lz_extra	= 'lz_extra'				
		lz_subGrpInit()
		lz_hideAttr(self.lz_extra,['t','r','s','v'])
		#11.9.27添加一个lz_exp的expression节点
		#self.lz_exp = expression(s="",n='lz_exp') if not objExists('lz_exp') else 'lz_exp'
		lz_hideAttr(self.lz_scale,['t','r','s','v'])
		if empty:
			return
		if not joints:
			if auto_setup:
				autoSelect_return = lz_ikfk_autoSelect(auto_setup[:-2],auto_setup[-2],auto_setup[-1])
				self.joints = autoSelect_return if autoSelect_return else ls(sl=True)
		else:
			self.joints 	= joints
		self.exist			= 0 
		self.joint_parent	= joint_parent
		self.length			= len(self.joints)#length放在前面，作为是否有joints的判断。
		self.joints			= lz_rand_rename(self.joints,['','']) if self.joints else [group(em=1,p=self.lz_extra,n='lz_O#')]
		#如果没有joints，那么就造一个lz_O#
		lz_removeJointScale(self.joints)#把joints的scale链接去除掉
		self.prefix		= self.joints[0]+'_' if not prefix else prefix
		self.setup_parent,self.setup_grp,self.local_grp,self.scale_grp,self.world_grp = self.prefix+'setupParent',self.prefix+'setupGrp',self.prefix+'localGrp',self.prefix+'scaleGrp',self.prefix+'worldGrp'
		self.std_axis,self.local_axis,self.ctls_grp,self.surfaces_grp,self.joints_grp,self.com_grp = self.prefix+'stdAxis',self.prefix+'localAxis',self.prefix+'ctlsGrp',self.prefix+'surfacesGrp',self.prefix+'jointsGrp',self.prefix+'componentGrp'
		
		#11.7.22 修改，通用架构
		if objExists(self.setup_parent):
			self.rawJntGrp,self.rawJoints,self.joint_realParent= '','',''
			self.exist = 1
			return 
		self.setup_parent	= group(em=1,p=self.lz_setup,n=self.setup_parent) 
		self.setup_grp		= group(em=1,p=self.setup_parent,n=self.setup_grp) 
		self.surfaces_grp	= group(em=1,p=self.setup_parent,n=self.surfaces_grp) 
		self.local_grp		= group(em=1,p=self.setup_parent,n=self.local_grp)
		self.world_grp		= group(em=1,p=self.setup_parent,n=self.world_grp)
		self.local_axis		= group(em=1,p=self.local_grp,n=self.local_axis)
		self.std_axis		= group(em=1,p=self.local_grp,n=self.std_axis) 
		self.ctls_grp		= group(em=1,p=self.setup_grp,n=self.ctls_grp) 		
		self.joints_grp		= group(em=1,p=self.setup_grp,n=self.joints_grp) 
		self.com_grp		= group(em=1,p=self.setup_grp,n=self.com_grp) 
		
		setAttr('%s.inheritsTransform'%self.ctls_grp,0)
		setAttr('%s.inheritsTransform'%self.surfaces_grp,0)
		setAttr('%s.inheritsTransform'%self.joints_grp,0)
		setAttr('%s.inheritsTransform'%self.com_grp,0)
		setAttr('%s.inheritsTransform'%self.local_grp,0)
		setAttr('%s.v'%self.surfaces_grp,0)
		setAttr('%s.v'%self.com_grp,0)
		#parentConstraint(self.setup_parent,self.local_grp,mo=1)
		#setAttr('%s.v'%self.joints_grp,0)
		#localGrp配合zero骨骼的方向
		self.scale_grp		= self.scale_grp if not scale_grp else scale_grp
		if not objExists(self.scale_grp):
			group(em=True,p=self.setup_grp,n = self.scale_grp)	
			#缩放增强，做一个额外乘法
			self.scale_world = group(em=1,p=self.local_grp,n=self.prefix+'scaleWorld')
			self.scale_local = group(em=1,p=self.local_grp,n=self.prefix+'scaleLocal')
			scaleConstraint(self.setup_grp,self.scale_world,mo=1)
			mult = createNode('multDoubleLinear',n=self.scale_grp+'_mult')
			connectAttr('%s.sx'%self.scale_world,'%s.i1'%mult)
			connectAttr('%s.sx'%self.scale_local,'%s.i2'%mult)
			connectAttr('%s.output'%mult,'%s.sx'%self.scale_grp)
			connectAttr('%s.output'%mult,'%s.sy'%self.scale_grp)
			connectAttr('%s.output'%mult,'%s.sz'%self.scale_grp)
			
		setAttr('%s.inheritsTransform'%self.scale_grp,0)	
		
		#把self.setup_parent组作为parentGrp
		if not self.joint_parent:
			joint_search	= self.joints[0] if rootFirst else self.joints[-1]
			self.joint_parent	= listRelatives(joint_search,pa=True,p=True)
			if self.joint_parent:
				self.joint_parent =  self.joint_parent[0]
				self.joint_realParent = group(em=1,p=self.local_grp,n=self.prefix+'realParent')
				lz_xform([self.setup_parent,self.setup_grp],joint_search)
				lz_xform([self.joint_realParent],joint_search)
				if xformReal:
					lz_xform([self.joint_realParent],self.joint_parent)
				makeIdentity(self.joint_realParent,a=1,t=1,r=1)
				parentConstraint(self.joint_parent,self.joint_realParent,mo=1)
				scaleConstraint(self.joint_parent,self.joint_realParent,mo=1)
				connectAttr('%s.t'%self.joint_realParent,'%s.t'%self.setup_grp)
				connectAttr('%s.r'%self.joint_realParent,'%s.r'%self.setup_grp)
				group(em=1,p=self.joint_realParent,n=self.prefix+'rp_notEmpty')
			else:
				self.joint_realParent,self.joint_parent = self.setup_parent,self.setup_parent
		else:#特别简单的情况
			self.joint_realParent = group(em=1,p=self.local_grp,n=self.prefix+'realParent')
			lz_xform([self.joint_realParent],self.joint_parent)
			lz_xform([self.setup_parent,self.setup_grp],self.joint_parent)
			makeIdentity(self.joint_realParent,a=1,t=1,r=1)
			parentConstraint(self.joint_parent,self.joint_realParent,mo=1)
			scaleConstraint(self.joint_parent,self.joint_realParent,mo=1)
			connectAttr('%s.t'%self.joint_realParent,'%s.t'%self.setup_grp)
			connectAttr('%s.r'%self.joint_realParent,'%s.r'%self.setup_grp)
			group(em=1,p=self.joint_realParent,n=self.prefix+'rp_notEmpty')
		lz_xform([self.joints_grp,self.ctls_grp],self.joint_realParent)
		#为了保持骨骼结构，进行克隆处理
		if self.length >0:
			self.rawJoints = lz_duplicate(self.joints,'_raw',isHierachy = 0,rootFirst = 0)
			joint_zero	= self.rawJoints[0] if rootFirst else self.rawJoints[-1]
			joint_zero_dup = duplicate(joint_zero,po=1,n=joint_zero+'_tarJoints')[0]
			setAttr('%s.r'%joint_zero_dup,0,0,0)
			lz_pre_createFitJoint(joint_zero_dup,anti_axis = anti_axis)
			if not world:
				#lz_xform(self.local_axis,joint_zero_dup,1,1)
				parent(self.local_axis,joint_zero_dup,r=1)
				parent(self.local_axis,self.local_grp)
				setAttr('%s.t'%self.local_axis,0,0,0)
			lz_xform(self.std_axis,joint_zero_dup,1,1)
			self.rawJntGrp = group(em=1,p=self.joints_grp,n=self.prefix+'rawJointsGrp')
			parent(self.rawJoints,self.rawJntGrp)
			for index,item in enumerate(self.joints):
				parentConstraint(self.rawJoints[index],item,mo=1)
				scaleConstraint(self.rawJoints[index],item,mo=1)
				setAttr('%s.overrideEnabled'%self.rawJoints[index],1)
				setAttr('%s.overrideLevelOfDetail'%self.rawJoints[index],1)
				setAttr('%s.overrideEnabled'%item,1)
			delete(joint_zero_dup)

def lz_subGrpInit():
	global lz_face_sub
	global lz_face_all
	global lz_face_main
	global lz_master_sub
	if not objExists(lz_face_sub):
		group(n=lz_face_sub,em=1)
	if not objExists(lz_face_main):
		group(n=lz_face_main,em=1)
	if not objExists(lz_master_sub):
		group(n= lz_master_sub,em=1)
	if not objExists(lz_face_all):
		group(n=lz_face_all,em=1)
		try:
			parent(lz_face_main,lz_face_sub,lz_face_all)
		except:
			pass
	if not 	objExists('FUNC'):
		group(n='FUNC',em=1)
		setAttr('FUNC.inheritsTransform',0)
		lz_hideAttr(['FUNC'],['inheritsTransform'])
		try:
			parent(lz_face_all,lz_master_sub,'FUNC')
		except:
			pass
	return 'FUNC'	

def lz_removeJointScale(items):
	if not items:
		return 
	message = '%s.inverseScale'
	for item in items:
		if attributeQuery('inverseScale',node=item,ex=1):
			conn = listConnections(message%item,p=1,d=0)
			if conn:
				disconnectAttr(conn[0],message%item)	

def lz_xform(obj,target,isXform=1,ro=0):
	objects = []
	roos = ['xyz','yzx','zxy','xzy','yxz','zyx']
	if isinstance(obj,list) or isinstance(obj,tuple):
		objects = obj
	else:
		objects =[obj]
	if isinstance(target,list) or isinstance(target,tuple):
		target_ro = target_r = target_piv = target
		target_roo = xform(obj,q=True,ws=True,roo=1)
	else:
		target_ro = xform(target,q=True,ws=True,ro=True)
		target_roo = xform(target,q=True,ws=True,roo=1)
		target_r  = getAttr('%s.r'%target)[0]
		target_piv = xform(target,q=True,ws=True,rp=True)
	for o in objects:
		if not ro:
			if not isXform:
				move(target_piv[0],target_piv[1],target_piv[2],o,rpr=True)
			else:
				xform(o,ws=True,piv=target_piv)
		else:
			if not isXform:
				setAttr('%s.rotateOrder'%o,roos.index(target_roo))
				setAttr('%s.r'%o,target_r[0],target_r[1],target_r[2])
			else:
				setAttr('%s.rotateOrder'%o,roos.index(target_roo))
				xform(o,ro=target_ro,ws=True)
	return objects				

def lz_duplicate(joints,surffix='',parentGrp = '',nameObjs=[],isHierachy = 1,rootFirst = 0):
	joints_new = []
	if nameObjs and len(nameObjs) != len(joints):
		return []
	if isinstance(joints,str):
		joints = [joints]
	for i,jo in enumerate(joints):
		if not jo:
			continue
		name = nameObjs[i]+surffix if nameObjs else jo+surffix
		select(cl=1)
		joint_new = joint(p=[0,0,0],n=name)
		grp = group(joint_new)
		lz_xform(grp,jo,0)
		r_order = getAttr('%s.rotateOrder'%jo)
		setAttr('%s.rotateOrder'%joint_new,r_order)
		lz_xform(grp,jo,1,1)
		parent(joint_new,w=1)
		delete(grp)

		joints_new.append(joint_new)
		if isHierachy:
			if i>0:
				if not rootFirst:
					parent(joints_new[i-1],joint_new)
				else:
					parent(joint_new,joints_new[i-1])
	#if len(joints) == 1:
	#	jo = getAttr('%s.jo'%joints[0])[0]
	#	setAttr('%s.jo'%joints_new[0],jo[0],jo[1],jo[2])
	return joints_new			

def lz_pre_createFitJoint(new_start,anti_axis = 0):
	tar_obj = ''
	if anti_axis:
		tar_obj = lz_pre_simpleMirror(new_start,sameParent= 0)
		lz_delete(new_start)
	else:
		tar_obj = new_start
	start_jo = duplicate(tar_obj,n=new_start+'_dup',po=1)[0]
	parent(start_jo,tar_obj)
	setAttr('%s.tx'%start_jo,1)
	parent(start_jo,w=1)
	setAttr('%s.jo'%start_jo,0,0,0)
	trans_tar = xform(tar_obj,q=1,ws=1,rp=1)
	trans_start = xform(start_jo,q=1,ws=1,rp=1)
	#new_start_tx = getAttr('%s.tx'%tar_obj)
	setAttr('%s.tz'%start_jo,trans_tar[2])
	
	if abs(trans_start[1] - trans_tar[1])>.01:
		setAttr('%s.tx'%start_jo,trans_tar[0])
	parent(start_jo,tar_obj)
	
	joint(tar_obj,e=1,ch=1,oj='xyz',sao='yup')
	
	delete(start_jo)
	
	if anti_axis:
		lz_pre_simpleMirror(tar_obj,sameParent= 0)
		delete(tar_obj)

def lz_delete(objs,setState=1):
	if not objs:
		return
	if not isinstance(objs,list):
		objs = [objs]	
	for item in objs:
		if item and objExists(item):
			if setState:
				setAttr('%s.nodeState'%item,2)
			delete(item)

def lz_pin(sled=[],object=''
	,attach_upperGrp ='',scale_grp ='',all_grp =''
	,addJoint=1,addCtl=1,simple=1,objParent=1,trans = [],u_aim = ''):
	global lz_u_allGrp
	global lz_u_upperGrp
	global lz_u_scaleGrp	
	global lz_master_sub
	res_return,geo_grps,attach_grps,attaches,ctls,normals,v_all = [],[],[],[],[],[],[]
	componentE,componentF = '%s.e[%s]','%s.f[%s]'
	if not sled:
		sled = ls(sl=1,fl=1)
	if not sled:
		return 0
	init = Lz_Init(empty = 1)
	all_grp = 'lz_pin' if not all_grp else all_grp
	setup_grp,scale_grp = 'lz_setup','lz_scale'
	if not listRelatives(setup_grp) and not objExists('FUNC'):
		attach_upperGrp = 'lz_attaches_gps'
		if not objExists(attach_upperGrp):
			group(em=1,n=attach_upperGrp)
			setAttr('%s.inheritsTransform'%attach_upperGrp,0)
			parent(attach_upperGrp,all_grp)
			lz_hideAttr([attach_upperGrp],['inheritsTransform'])
		for item in lz_ls('*lz_attaches_gps'):
			try:
				setAttr('%s.t'%item,0,0,0)
				setAttr('%s.r'%item,0,0,0)
			except:
				pass
	else:
		lz_subGrpInit()	
		if not attach_upperGrp:
			attach_upperGrp= lz_master_sub
		
	'''
	if not scale_grp:
		scale_grp = 'lz_attach_scale'
		if not objExists(scale_grp):
			group(em=1,n=scale_grp)
			setAttr('%s.inheritsTransform'%scale_grp,0)
			lz_hideAttr([scale_grp],['inheritsTransform'])
			parent(scale_grp,all_grp)
			scaleConstraint('lz_all',scale_grp)
		select(sled)
	'''
	object = object if object else sled[-1].split('.')[0]
	comp_return = lz_subCtl_getComponents(object,sled)
	all_sled,sled_vtx,sled_edge,sled_face = comp_return[0],comp_return[1],comp_return[2],comp_return[3]
	sled_uv,sled_u,sled_objs = comp_return[4],comp_return[5],comp_return[6]
	
	lz_u_allGrp,lz_u_upperGrp,lz_u_scaleGrp = all_grp,attach_upperGrp,scale_grp
	if all_sled ==[[]]*6:#单独的anti smooth
		lz_polyPin_antiSmooth(object)
	for index,item in enumerate(all_sled):
		res_return = lz_polyPin_interface(object,item
				,addJoint = addJoint,addCtl = addCtl
				,type=index,simple=simple,trans = trans,objParent = objParent,u_aim = u_aim)
		
		geo_grps += res_return[0]
		attach_grps+= res_return[1]
		attaches+= res_return[2]
		ctls+= res_return[3]
		normals+=res_return[5]
		v_all +=res_return[6]
		if res_return[3]:
			lz_addAttr(res_return[3][0],sources=['%s.message'%object],ln='poly_tar',h=1,at='message',en='')
	if geo_grps:
		for index,item in enumerate(geo_grps):
			setAttr('%s.v'%item,0)
			parent(item,attach_grps[index])
	if attach_grps:
		for item in attach_grps:
			parent(item,attach_upperGrp)
	if attaches:
		for item in attaches:
			connectAttr('%s.s'%scale_grp,'%s.s'%item)
		if ctls:
			select(ctls)
		else:
			select(attaches)
	lz_polyPin_antiSmooth(object)
	
	return [geo_grps,attach_grps,attaches,ctls,normals,v_all]

def lz_pre_createFitJoint(new_start,anti_axis = 0):
	tar_obj = ''
	if anti_axis:
		tar_obj = lz_pre_simpleMirror(new_start,sameParent= 0)
		lz_delete(new_start)
	else:
		tar_obj = new_start
	start_jo = duplicate(tar_obj,n=new_start+'_dup',po=1)[0]
	parent(start_jo,tar_obj)
	setAttr('%s.tx'%start_jo,1)
	parent(start_jo,w=1)
	setAttr('%s.jo'%start_jo,0,0,0)
	trans_tar = xform(tar_obj,q=1,ws=1,rp=1)
	trans_start = xform(start_jo,q=1,ws=1,rp=1)
	#new_start_tx = getAttr('%s.tx'%tar_obj)
	setAttr('%s.tz'%start_jo,trans_tar[2])
	
	if abs(trans_start[1] - trans_tar[1])>.01:
		setAttr('%s.tx'%start_jo,trans_tar[0])
	parent(start_jo,tar_obj)
	
	joint(tar_obj,e=1,ch=1,oj='xyz',sao='yup')
	
	delete(start_jo)
	
	if anti_axis:
		lz_pre_simpleMirror(tar_obj,sameParent= 0)
		delete(tar_obj)

def lz_subCtl_getComponents(object,selectionRaw,justIndex = 0 ):
	componentV,componentE,componentF = '%s.vtx[%s]','%s.e[%s]','%s.f[%s]'
	vtx_index,edge_index,face_index,vtx_sl,edge_sl,face_sl = [],[],[],[],[],[]
	uv_all,u_all,else_objs,obj_types = [],[],[],['mesh','nurbsSurface','nurbsCurve']
	if not selectionRaw:
		return [[[]]*6,[],[],[],[],[],[]]
	for item in selectionRaw:
		if item.find('.uv[')!=-1:
			if not justIndex:
				uv_all.append(item)
			else:
				type_match = re.search('\[(-?\d+(\.\d+)?)\]\[',item)
				uLoc = '' if not type_match else type_match.groups()[0]
				type_match = re.search('\]\[(-?\d+(\.\d+)?)\]',item)
				vLoc = '' if not type_match else type_match.groups()[0]
				if not uLoc or not vLoc:
					continue
				uv_all.append([float(uLoc),float(vLoc)])
		if item.find('.u[')!=-1:
			u_all.append(item)
		if objectType(item) not in obj_types and item !=object:
			else_objs.append(item)
	
	sled_vtx = polyListComponentConversion(selectionRaw,fv=1,tv=1)
	sled_edge = polyListComponentConversion(selectionRaw,fe=1,te=1)
	sled_face = polyListComponentConversion(selectionRaw,ff=1,tf=1)
	if sled_vtx and sled_vtx[0].find('*') !=-1:
		sled_vtx =[]
	if sled_edge and sled_edge[0].find('*') !=-1:
		sled_edge =[]
	if sled_face and sled_face[0].find('*') !=-1:
		sled_face =[]	
	lz_mirrorSelection_getIndex(vtx_index,sled_vtx)
	lz_mirrorSelection_getIndex(edge_index,sled_edge)
	lz_mirrorSelection_getIndex(face_index,sled_face)
	for item in vtx_index:
		if item=='':
			continue
		vtx_sl.append(componentV%(object,item))
	for item in edge_index:
		if item=='':
			continue
		edge_sl.append(componentE%(object,item))
	for item in face_index:
		if item=='':
			continue
		face_sl.append(componentF%(object,item))
	if not justIndex:
		selectionRaw = [vtx_sl,edge_sl,face_sl,uv_all,u_all,else_objs]
	else:
		selectionRaw = [vtx_index,edge_index,face_index,uv_all,u_all,else_objs]
		vtx_sl,edge_sl,face_sl = vtx_index,edge_index,face_index
	return [selectionRaw,vtx_sl,edge_sl,face_sl,uv_all,u_all,else_objs]

def lz_polyPin_interface(object,item,addJoint = 1,addCtl = 1,type =1,simple =0,trans =[],objParent = 1,u_aim = ''):
	global lz_u_object
	global lz_u_item
	res_return,joints_all = [[]]*7,[]
	if not item:
		return res_return
	if type ==3:
		res_return = lz_polyPin_uv(object,item)	
	elif type ==4:
		if not u_aim:
			lz_u_object = object
			lz_u_item = item
			lz_polyPin_u_UI()
		else:
			res_return = lz_polyPin_u(object,item,u_aim,u_aim)
	elif type ==5:
		res_return = lz_polyPin_hair(object,item,trans = trans)
		addJoint,addCtl = 0,0
	elif not simple:
		if type ==0:
			res_return = lz_polyPin_vtx(object,item)
		if type ==1:
			res_return = lz_polyPin_edge(object,item)
		if type ==2:
			res_return = lz_polyPin_face(object,item)
	else:
		res_return = lz_polyPin_hair(object,item)
	attaches,ctls,normalInfos = res_return[2],res_return[3],res_return[5]
	if type == 5 and objParent:
		for index,o in enumerate(item):
			parent(o,attaches[index])
	if addJoint:
		for attach in attaches:
			select(cl=1)
			joint_new = joint(radius=.5,n=object+'_atJo#')
			parent(joint_new,attach,r=1)
			joints_all.append(joint_new)
	if addCtl:
		if normalInfos:
			for index,normalInfo in enumerate(normalInfos):
				ctls.append(lz_pin_normalCtl(normalInfo,attaches[index],joints_all[index])[0])			
	return res_return

def lz_polyPin_hair(object,sled,trans = []):
	name = object.split('|')[-1]+'_hair_'
	shape_type = 0
	geo_grps,attach_grps,attaches,ctls,hair_slIndex,v_indexAll,normalInfos =[],[],[],[],[],[],[]
	obj_shape = listRelatives(object,s=1,pa=1)
	if obj_shape and objectType(obj_shape[0]) != 'nurbsSurface':
		lz_mirrorSelection_getIndex(hair_slIndex,sled)
	if objectType(obj_shape[0]) == 'nurbsSurface':
		shape_type = 1
	for index,item in enumerate(sled):
		if not shape_type:
			trans_one = trans[index] if trans else ''

			attach_return = lz_ikfk_surfaceAttatch3( object,item,name= name,trans = trans_one)
			v_indexAll.append(attach_return[3])
			normalInfo = polyInfo(attach_return[4],fn=1)[0]	
			normalInfos.append(lz_polyPin_getInfo2(normalInfo))
		else:
			trans_one = trans[index] if trans else item
			attach_return = lz_ikfk_surfaceAttatch2( '',object,trans_one,name= name)
		attaches.append(attach_return[0])
		attach_grps.append(attach_return[1])

	return [geo_grps,attach_grps,attaches,ctls,hair_slIndex,normalInfos,v_indexAll] 

def lz_ikfk_surfaceAttatch3( poly,obj,name = '',trans = [],toCreate = 0):
	trans = lz_attach_trans(obj) if not trans else trans
	onMesh_return = lz_subCtl_closestOnMesh([trans],poly,asTrans = 0 )
	 
	res_face,res_faceIndex,vIndex,uLoc,vLoc = onMesh_return[0][0],onMesh_return[1][0],onMesh_return[2][0],onMesh_return[3][0],onMesh_return[4][0]
	vIndex,uLoc,vLoc = onMesh_return[2][0],onMesh_return[3][0],onMesh_return[4][0]
	name = poly.split('|')[-1]+'_uv_' if not name else name
	attach_return = lz_ikfk_surfaceAttatch(obj)
	seg_loc,seg_loc_grp = attach_return[0],attach_return[1]
	return [seg_loc,seg_loc_grp,[uLoc,vLoc],vIndex,res_face,res_faceIndex]

def lz_attach_trans(object):
	translate = [0.0,0.0,0.0]
	number =0.0
	if isinstance(object,list) or isinstance(object,tuple):
		translate = object
	else:
		if objectType(object) == "transform":
			translate = xform(object,q=True,ws=True,rp=True)
		else:
			translate_old = xform(object,q=True,ws=True,t=True)
			for index,item in enumerate(translate_old):
				if (index+1)%3 == 0:
					translate[0] += translate_old[index-2]
					translate[1] += translate_old[index-1]
					translate[2] += translate_old[index]
					number+=1.0
			translate[0] = translate[0]/number
			translate[1] = translate[1]/number
			translate[2] = translate[2]/number
	return translate

def lz_subCtl_closestOnMesh(ctls,mainPoly,asTrans = 0 ,shape = ''):
	componentF = '%s.f[%s]'
	trans = getAttr('%s.t'%mainPoly)[0]+getAttr('%s.r'%mainPoly)[0]
	res_face,res_faceIndex,res_vIndex,ulocs,vlocs,outPos = [],[],[],[],[],[]
	poly_shape = listRelatives(mainPoly,s=True,type='mesh')[0]
	vrt_len = getAttr('%s.vrts'%poly_shape,s=True)
	
	trans_t = getAttr('%s.t'%mainPoly)[0]
	trans_r = getAttr('%s.r'%mainPoly)[0]
	trans_s = getAttr('%s.s'%mainPoly)[0]
	main_pa = listRelatives(mainPoly,pa=1,p=1)
	#使用closest point on mesh
	shape = listRelatives(mainPoly,s=1,pa=1,type="mesh")[0] if not shape else shape
	pointOnMesh = createNode('closestPointOnMesh',n=mainPoly+'clo#')
	connectAttr('%s.outMesh'%shape,'%s.inMesh'%pointOnMesh)
	for item in ctls:
		grp = group(em=1)
		grp_mid = group(grp)
		if main_pa:
			grp_pa = group(grp_mid)
			parent(grp_pa,main_pa[0],r=1)
		setAttr('%s.s'%grp_mid,trans_s[0],trans_s[1],trans_s[2])
		setAttr('%s.t'%grp_mid,trans_t[0],trans_t[1],trans_t[2])
		lz_xform(grp_mid,mainPoly,1)
		setAttr('%s.r'%grp_mid,trans_r[0],trans_r[1],trans_r[2])
		if not asTrans:
			lz_xform(grp,item,0)
		else:
			setAttr('%s.t'%grp,item[0],item[1],item[2])
		trans_grp = getAttr('%s.t'%grp)[0]
		setAttr('%s.inPosition'%pointOnMesh,trans_grp[0],trans_grp[1],trans_grp[2])
		fIndex = getAttr('%s.closestFaceIndex'%pointOnMesh)
		res_faceIndex.append(fIndex)
		res_vIndex.append(getAttr('%s.closestVertexIndex'%pointOnMesh))
		res_face.append(componentF%(mainPoly,fIndex))	
		ulocs.append(getAttr('%s.parameterU'%pointOnMesh))
		vlocs.append(getAttr('%s.parameterV'%pointOnMesh))
		outPos.append(getAttr('%s.position'%pointOnMesh)[0])
		delete(grp,grp_mid)
		if main_pa:
			delete(grp_pa)
	delete(pointOnMesh)
	return [res_face,res_faceIndex,res_vIndex,ulocs,vlocs,outPos]

def lz_ikfk_surfaceAttatch(polyVertex):
	seg_loc = shuai_polyAttach(polyVertex)
	seg_loc_grp = group(seg_loc,n=seg_loc+"_grp")
	lz_xform(seg_loc_grp,seg_loc)
	setAttr('%s.inheritsTransform'%seg_loc_grp,0)
	
	return [seg_loc,seg_loc_grp]

def shuai_polyAttach(sel):
    if sel.find('.vtx[')!=-1:
        edgeInfo=polyInfo(sel,ve=1)[0]
        edge=sel.split('.')[0]+'.e[%s]'%(edgeInfo.split()[2])
        parameter=2
        if sel.find(polyInfo(edge,ev=1)[0].split()[2])!=-1:
            parameter=1
        curveInfo=pointOnCurve(edge,ch=1,pr=parameter,p=1)
        attachLoc=spaceLocator(n='attachLoc#')[0]
        connectAttr(curveInfo+'.position',attachLoc+'.t')
        normalCstrt=normalConstraint(sel.split('.')[0],attachLoc,weight=1,aimVector=[0,0,1],upVector=[1,0,0],worldUpType='vector',worldUpVector=[1,0,0])[0]
        connectAttr(curveInfo+'.tangent',normalCstrt+'.worldUpVector')
        return attachLoc
    else:
        warning('Please select a single vertex ！！')

def lz_polyPin_getInfo(rawInput):
	res = []
	temp_input = rawInput.split(" ")
	for item in temp_input:
		if item:
			res.append(item) 
	return res[2:-1]

def lz_polyPin_getInfo2(rawInput):
	res = []
	temp_input = rawInput.split(" ")
	for item in temp_input:
		if item:
			res.append(item)
	res[-1] = res[-1].replace('\n','')
	for index,item in enumerate(res):
		if index>1:
			res[index] = float(item)
	return res[2:]

def lz_polyPin_antiSmooth(object):
	preST_attr = ''
	polyCurveNodes,attachNodes = [],[]
	shape = listRelatives(object,s=1,pa=1)
	if not shape or objectType(shape[0])!='mesh':
		return 0
	for item in shape:
		if item.find('Orig')==-1:
			shape = item
			break
	
	history = listHistory(shape,ag=1,gl=2)
	polyST,polyIndex,skIndex,type ='',-1,-1,"polySmoothFace"
	typeSk= 'skinCluster'

	#找到需要的polySmoothFace
	for index,h in enumerate(history):
		try:
			t = objectType(h)
		except:
			pass
			continue
		if t and t== typeSk:
			skIndex = index
		if t and t==type:
			polyST=h
			polyIndex = index
			break
	
	#我要在这里做一个还原的过程
	lz_polyPin_recoverSmooth(shape)
	
	#找到所有shape连接的polyEdgeToCurve
	conn1 = listConnections("%s.worldMatrix[0]"%shape)

	if conn1:
		for index,item in enumerate(conn1):
			try:
				if objectType(item) == 'polyEdgeToCurve' :
					polyCurveNodes.append(item)		
			except:
				pass
	if not polyST:
		return 0
	preST_attr = listConnections('%s.inputPolymesh'%polyST,p=1)
	if not preST_attr:
		return 0
	preST_attr = preST_attr[0]
	preAt_attr = preST_attr.replace('outMesh','worldMesh')
	for item in polyCurveNodes:
		temp_attr = connectionInfo('%s.inputPolymesh'%item,sfd=1)
		if temp_attr!=preST_attr:
			lz_connectAttr(preST_attr,'%s.inputPolymesh'%item)
	return 1

def lz_polyPin_recoverSmooth(shape):
	polyCurveNodes,attachNodes = [],[]
	#找到所有shape连接的polyEdgeToCurve
	conn1 = listConnections("%s.worldMatrix[0]"%shape,sh=1)
	if conn1:
		for index,item in enumerate(conn1):
			try:
				if objectType(item) == 'polyEdgeToCurve' :
					polyCurveNodes.append(item)		
			except:
				pass
			
	shape_attr  = '%s.outMesh'%shape
	shape_inAttr = '%s.inMesh'%shape
	upper_attr = connectionInfo(shape_inAttr,sfd=1)
	for item in polyCurveNodes:
		temp_attr = connectionInfo('%s.inputPolymesh'%item,sfd=1)
		if temp_attr!=shape_attr:
			connectAttr(shape_attr,'%s.inputPolymesh'%item,f=1)
		else:
			if upper_attr:
				connectAttr( upper_attr,'%s.inputPolymesh'%item,f=1)

def lz_polyPin_edgeInOneFace(edge01,edge02):
	poly = edge01.split('.')[0]
	face_info = polyInfo(edge01,ef=1)[0]
	face_info = lz_polyPin_getInfo(face_info)
	flag =0 
	for item in face_info:
		edge_info = polyInfo('%s.f[%s]'%(poly,item),fe=1)[0]
		edge_info = lz_polyPin_getInfo(edge_info)
		for edge in edge_info:
			if edge02 == edge:
				flag =1
				break
	return flag

def	lz_group(objects_raw,suffix='_new',toWorld=0,axis='',nameObjs=[],setOrder = 0):
	objects = []
	if not objects_raw:
		objects_raw = ls(sl=1)
	if isinstance(objects_raw,list):
		objects = objects_raw
	else:
		objects.append(objects_raw)
	obj_grps,nameObjs = [],nameObjs if nameObjs and len(objects)==len(nameObjs) else objects
	for index,obj in enumerate(objects):
		if not obj:
			continue
		obj_grp = group(em = True, n= (nameObjs[index]+suffix))
		parent(obj_grp,obj,r=1)
		parent(obj_grp,w=1)
		lz_xform(obj_grp,obj)
		if axis:
			lz_xform(obj_grp,axis,1,1)
		else:
			lz_xform(obj_grp,obj,1,1)
		obj_parent = listRelatives(obj, pa=True,p=True,type='transform')
		if obj_parent and not toWorld:
			parent( obj_grp, obj_parent )
		parent(obj,obj_grp)
		obj_grps.append(obj_grp)
		if setOrder:
			setAttr('%s.rotateOrder'%obj_grp,getAttr('%s.rotateOrder'%obj))
	return obj_grps
	
def lz_ctl_factory(subCtlShape=''):
	if subCtlShape in range(1,10):
		ctl_style	= subCtlShape
		if ctl_style == 1:
			subCtlShape = 'joint'
		elif ctl_style == 2:
			subCtlShape = 'box'
		elif ctl_style == 3:
			subCtlShape = 'circle'
		elif ctl_style == 4:
			subCtlShape = 'lahuan'
		elif ctl_style == 5:
			subCtlShape = 'doubleCone'	
		
	shapes = {'circle':'circle(r=1.4,nr=(1,0,0),ch=0)[0]','box':'create_box()'
			,'direction':'create_direction()','joint':'create_joint()'
			,'lahuan':'create_lahuan()','doubleCone':'create_doubleCone()'}
	if subCtlShape in shapes:
		exec('ctl = '+shapes[subCtlShape])
	return ctl

def create_joint():
	import maya.mel as mm
	return mm.eval("curve -d 1 -p 0 1 0 -p 0 0.92388 0.382683 -p 0 0.707107 0.707107 -p 0 0.382683 0.92388 -p 0 0 1 -p 0 -0.382683 0.92388 -p 0 -0.707107 0.707107 -p 0 -0.92388 0.382683 -p 0 -1 0 -p 0 -0.92388 -0.382683 -p 0 -0.707107 -0.707107 -p 0 -0.382683 -0.92388 -p 0 0 -1 -p 0 0.382683 -0.92388 -p 0 0.707107 -0.707107 -p 0 0.92388 -0.382683 -p 0 1 0 -p 0.382683 0.92388 0 -p 0.707107 0.707107 0 -p 0.92388 0.382683 0 -p 1 0 0 -p 0.92388 -0.382683 0 -p 0.707107 -0.707107 0 -p 0.382683 -0.92388 0 -p 0 -1 0 -p -0.382683 -0.92388 0 -p -0.707107 -0.707107 0 -p -0.92388 -0.382683 0 -p -1 0 0 -p -0.92388 0.382683 0 -p -0.707107 0.707107 0 -p -0.382683 0.92388 0 -p 0 1 0 -p 0 0.92388 -0.382683 -p 0 0.707107 -0.707107 -p 0 0.382683 -0.92388 -p 0 0 -1 -p -0.382683 0 -0.92388 -p -0.707107 0 -0.707107 -p -0.92388 0 -0.382683 -p -1 0 0 -p -0.92388 0 0.382683 -p -0.707107 0 0.707107 -p -0.382683 0 0.92388 -p 0 0 1 -p 0.382683 0 0.92388 -p 0.707107 0 0.707107 -p 0.92388 0 0.382683 -p 1 0 0 -p 0.92388 0 -0.382683 -p 0.707107 0 -0.707107 -p 0.382683 0 -0.92388 -p 0 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 ;")

def create_box():
	import maya.mel as mm
	return mm.eval("curve -d 1 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5    -0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5       -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p 0.5    0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p   0.5     -0.5 0.5 -k   0  -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 ;")

def lz_setColor(objs,color = 'r'):
	dic = {'r':13,'g':14,'b':6,'w':16,'y':17,'p':9,'c':12,'lc':21
			,'lr':20,'lg':19,'lb':18,'ldb':15,'dr':4,'db':5,'dp':30,'gb':29,'gg':28}
	for obj in objs:
		shape = listRelatives(obj,s=1,pa=1)
		if shape:
			obj = shape[0]
		setAttr('%s.ove'%obj,1)
		new_color = 13 if not color in dic else dic[color]
		setAttr('%s.ovc'%obj,new_color)
		
def lz_skin_toggleLock(flag):
	global lz_weight_jo_sort
	indexes = textScrollList("skin_showList",q=1,sii=1) if textScrollList("skin_showList",q=1,ex=1) else []
	obscured,tool_exist = 1,textScrollList('skinClusterInflList',q=True,ex=True)
	if tool_exist:
		obscured = textScrollList('skinClusterInflList',q=True,io=True)
	else:
		obscured = 1
	selection = ls(sl=True)
	suffix ='' if not flag else ' (Hold)'
	
	if not selection:
		return 0	
	poly = selection[0].split('.')[0]
	if objectType(poly) != 'transform':
		poly = listRelatives(poly,ni=1,p=1)[0]
	if not obscured:
		tool_allItem = textScrollList('skinClusterInflList',q=True,ai=True)
		tool_selects = textScrollList('skinClusterInflList',q=True,si=True)
		tool_res = []
		for index,item in enumerate(tool_allItem):
				item_raw = item
				if item.find(' (Hold)'):
					item = item.split(' (Hold)')[0]
				if tool_selects and (item  in tool_selects or item_raw in tool_selects):
					setAttr('%s.liw'%item,0)
					textScrollList('skinClusterInflList',e=True,rii=index+1)
					textScrollList('skinClusterInflList',e=True,ap=[index+1,item])
					tool_res.append(item)
				else:
					setAttr('%s.liw'%item,flag)
					textScrollList('skinClusterInflList',e=True,rii=index+1)
					textScrollList('skinClusterInflList',e=True,ap=[index+1,item+suffix])
		if tool_res:		
			textScrollList('skinClusterInflList',e=True,si=tool_res)
	else:
		shape 	= listRelatives(poly,pa=True,s=True)
		if not shape:
			return  0
		cluster = lz_findCluster(poly)
		if not cluster:
			return 0
		if objectType(cluster) == "fmSkinCluster":
			objects = listConnections ("%s.lockWeights"%cluster)
			for obj in objects:
				setAttr('%s.liw'%obj,flag)
		if objectType(cluster) == "skinCluster":	
			objects = skinCluster(cluster,q=True,inf=True)
			for obj in objects:
				skinCluster(cluster,e=True,inf = obj,lw=flag)
		if objectType(cluster) == "fmSkinCluster" or objectType(cluster) == "skinCluster" and flag == 1 and indexes:
			if indexes:
				for index in indexes:
					if index == 1:
						continue
					setAttr('%s.liw'%lz_weight_jo_sort[index-2],0)
		if objectType(cluster) == "cMuscleSystem":
			objects = mm.eval('cMuscleQuery -system "'+cluster+'" -mus;')
			for obj in objects:
				mm.eval('cMuscleWeight -system  "'+cluster+'" -muscle "'+obj+'" -wt "sticky" -lock '+str(flag));
			if window('cMusclePaintWin',q=True,ex=True):
				sled = mm.eval('cMusclePaint_getSelItemsFromList("tslMusclePaint")')
				for item in sled:
					mus = listRelatives(item,ni=1,s=1,type='cMuscleObject')[0]
					mm.eval('cMuscleWeight -system  "'+cluster+'" -muscle "'+mus+'" -wt "sticky" -lock 0');
				mm.eval('cMusclePaint_refreshList "'+cluster+'" "tslMusclePaint" ;')
		
	lz_skin_UI_update(cal = 0)

def lz_subCtl_link(subCtl_hide,subCtl,subCtl_drivenGrp,subCtl_move,subCtl_drivenMove,subCtl_hideCo,subCtl_hideCoGrp,target):
	#判断类型，骨骼链接target，其他cluster链接其本身
	target_c = listRelatives(target,c=1,pa=1)
	if target_c and objectType(target_c[0])=='transform':
		target = target_c[0]
	#处理subCtl的链接
	connectAttr('%s.r'%subCtl_hide,'%s.r'%target)
	connectAttr('%s.s'%subCtl_hide,'%s.s'%target)
	connectAttr('%s.t'%subCtl_hide,'%s.t'%target)
	#处理subCtl_drivenGrp的anti
	condition = createNode('condition',n=subCtl_drivenGrp+'_cond#')
	setAttr('%s.st'%condition,0)
	setAttr('%s.ct'%condition,0,0,0)
	setAttr('%s.cf'%condition,-1,-1,-1)
		
	temp_multi = createNode('multiplyDivide',n=subCtl_drivenGrp+'_multiT')
	connectAttr('%s.t'%subCtl_drivenGrp,'%s.input1'%temp_multi)
	#setAttr('%s.input2'%temp_multi,-1,-1,-1)
	connectAttr('%s.oc'%condition,'%s.input2'%temp_multi)
	connectAttr('%s.output'%temp_multi,'%s.t'%subCtl_drivenMove,f=1)	
	#处理subCtl的anti
	condition1 = createNode('condition',n=subCtl+'_cond#')
	setAttr('%s.st'%condition1,0)
	setAttr('%s.ct'%condition1,0,0,0)
	setAttr('%s.cf'%condition1,-1,-1,-1)
		
	temp_multi = createNode('multiplyDivide',n=subCtl+'_multiT')
	connectAttr('%s.t'%subCtl,'%s.input1'%temp_multi)
	setAttr('%s.input2'%temp_multi,-1,-1,-1)
	connectAttr('%s.oc'%condition1,'%s.input2'%temp_multi)	
	connectAttr('%s.output'%temp_multi,'%s.t'%subCtl_move,f=1)
	return [condition,condition1]

def lz_attrMaxMin(attrName,max=0,min=0,hxv = 1,hnv=1):
	if isinstance(attrName,list):
		for item in attrName:
			addAttr(item,e=1,hxv=1)
			addAttr(item,e=1,max=max)
			addAttr(item,e=1,hnv=1)
			addAttr(item,e=1,min=min)
	else:
		addAttr(attrName,e=1,hxv=1)
		addAttr(attrName,e=1,max=max)
		addAttr(attrName,e=1,hnv=1)
		addAttr(attrName,e=1,min=min)
		
def lz_subCtl_afterLoft(infomations):
	

	import string
	
	ssd=softSelect(query=1,ssd=1)
	sel=ls(selection=1,flatten=1)
	cvpoint_n=sel[0]
	
	split_n1=string.split(cvpoint_n,".")
	name_n1=split_n1[0]+"_sub"
	name_n2=split_n1[0]+"_facesub"
	if objExists(name_n1):
		cvpoint=name_n1+"."+split_n1[1]
	elif objExists(name_n2):
		cvpoint=name_n2+"."+split_n1[1]


	split_n=string.split(cvpoint,"[")
	
	size_n=len(split_n)
	if size_n ==2:
		match_n="["+split_n[1]
		AllCV=string.replace(cvpoint,match_n,"[*]")
		
	else:
	    match_n=[("["+split_n[1]),("["+split_n[2])]
	    AllCV_n=string.replace(cvpoint,match_n[0],"[*]")
	    AllCV=string.replace(AllCV_n,match_n[1],"[*]")
	    
	select(AllCV)
	AllCVPoint=ls(selection=1,flatten=1)
	select(clear=1)
	
	#-----------------------------------------------------------
	#
	#上面代码是软选择的
	#------------------------------------------------------------
	
	
	subText,skin_object,inf_vtx,subCtls= infomations[0],infomations[1],infomations[2],infomations[3]
	componentF,componentE,componentV = '%s.f[%s]','%s.e[%s]','%s.vtx[%s]'
	baseJoint,skin_node,ctl_selection,ctls_piv ='','',[],[]
	skin_node = lz_findCluster(subText,type='skinCluster')
	#---------------------------------------------------------------------------
	#
	#	控制器合并
	#
	#---------------------------------------------------------------------------
	try:
		select("*_subCtl_*")
		select("*_subCtl*grp*",toggle=1)
		select("*_subCtl*parent",toggle=1)
		select("*_subCtl*link",toggle=1)
		select("*_subCtl*move",toggle=1)
		select("*_subCtl*driven*",toggle=1)
		select("*_subCtl*hide*",toggle=1)
		select("*_subCtl*aimOrn*",toggle=1)
		ctl_selection =ls(sl=1,tr=1,v=1)
	except:
		pass

	for item in subCtls:
		ctl_pv = xform(item,q=True,ws=True,rp=True)
		ctls_piv.append([round(ctl_pv[0],3),round(ctl_pv[1],3),round(ctl_pv[2],3)])
	if ctl_selection:
		for index,item in enumerate(ctl_selection):
			item_pv = xform(item,q=True,ws=True,rp=True)
			item_pv = [round(item_pv[0],3),round(item_pv[1],3),round(item_pv[2],3)]
			for subIndex,subItem in enumerate(ctls_piv):
				if item_pv == subItem and subCtls[subIndex]!=ctl_selection[index]:
					connectAttr('%s.t'%subCtls[subIndex],'%s.t'%ctl_selection[index])
					setAttr('%s_parent.v'%ctl_selection[index],0)
	
	baseJoint = subText+'_baseJoint'
	baseJoint_parent = listRelatives(baseJoint,p=1)
	if not baseJoint_parent:
		parent(baseJoint,'lz_extra')
	#---------------------------------------------------------------------------
	#
	#	简单权重过程
	#
	#---------------------------------------------------------------------------
	
	
	
	if skin_node:
		for item in skin_object:
			skinCluster(skin_node,e=1,ai=item,ug=1,ps=0,ns=10,lw=1,wt=0)
		select(subText)
		lz_skin_toggleLock(0)
        for index,item in enumerate(inf_vtx):
            if softSelect(query=1,sse=1):
                for sub_item in item:
                    for point_n in AllCVPoint:
                        cv1=xform(cvpoint,q=1,ws=1,t=1)
                        cv2=xform(point_n,q=1,ws=1,t=1)
                        distance=mm.eval("mag<<%f,%f,%f>>"%(cv2[0]-cv1[0],cv2[1]-cv1[1],cv2[2]-cv1[2]))
                        x=distance/ssd
                        if x<=1:
                            falloff=gradientControlNoAttr("softSelectFalloffRamp",q=1,valueAtPoint=x)
                            skinPercent(skin_node, point_n,r=0,tv=(skin_object[index],falloff))
                            str_falloff=str(falloff)
                            print("skinPercent -tv " +skin_object[index]+" "+ str_falloff +" " + point_n +"\n")
            else:
                for index,item in enumerate(inf_vtx):
                    skinPercent(skin_node, AllCVPoint[item[0]],r=0,tv=(skin_object[index],1))

		select(subCtls)
	
	return subCtls

def lz_skin_UI_update(cal = 1):
	global lz_weight_jo
	global lz_weight_jo_sort
	global lz_weight_jo_sl
	if not textScrollList('skin_showList',q=1,ex=1):
		return
	if cal:
		lz_skin_getAverage()
	textScrollList('skin_showList',e=1,ra=1)
	textScrollList('skin_showList',e=1,append=(u("影响物名")+" "*28+u("是否锁住        ")+u("平均权重值"))) 
	for jo in lz_weight_jo_sort:
		loc_flag = getAttr('%s.liw'%jo)
		mid_str = " "*2+'(HOLD)'+" "*6 if loc_flag else " "*20
		textScrollList('skin_showList',e=1,append=str(lz_weight_jo[jo][0]+mid_str+lz_weight_jo[jo][1])) 
	if lz_weight_jo_sl:
		exist_list = []
		last_item = ''
		times = 0
		for item in lz_weight_jo_sl:
			if item in lz_weight_jo_sort:
				index_item = lz_weight_jo_sort.index(item)+2
				textScrollList('skin_showList',e=1,sii=index_item)
				last_item = item
				times +=1
		if last_item:
			textFieldButtonGrp('skin_jointName',e=1,tx = last_item)
			floatSliderButtonGrp('skin_weight',e=1,value = float(lz_weight_jo[last_item][1]))
		if times <= 1:
			button('skin_set1',e=1,enable =1)
		else:
			button('skin_set1',e=1,enable =0)
		button('skin_set0',e=1,enable =1)	

def lz_print(txt = ''):
	import maya.mel as mm
	mm.eval('print "'+u(txt)+'"')

def u(txt=''):
	return unicode(txt,'gbk')
def utf(txt = ''):
	return unicode(txt,'utf-8')

def lz_subCtl_infObject(object,sk,inf_vtx = []):
	if isinstance(inf_vtx,int):
		inf_vtx = [inf_vtx]
	values_all,componentV = {},'%s.vtx[%s]'
	targets= skinCluster(sk,wi=1,q=1)
	p_len = len(inf_vtx)
	for tar in targets:
		sum = 0.0
		for point in inf_vtx:
			temp_s = skinPercent(sk,componentV%(object,point),q=True,v=True,t=tar)
			if temp_s >0.01:
				sum +=temp_s
		sum = sum/p_len
		if sum:
			values_all[tar] = sum
	max_value = 0
	max_item =''
	
	for item in values_all:
		if values_all[item]>max_value:
			max_value = values_all[item]
			max_item = item
	return max_item

def lz_subCtl_doIt(sled=[],ctlText ='',ctl_color = 'lr',ctl_scale=0.0,ctl_style=0,ctl_name ='',addInf = 0,clu = 0):
	
	ctlText		= textField('subCtlField',q=1,tx=1 ) if not ctlText else ctlText
	ctl_scale	= floatField('subCtlStyleField',q=1,v=1) if not ctl_scale else ctl_scale
	ctl_style	= optionMenuGrp('subCtlStyle',q=1,sl=1) if not ctl_style else ctl_style
	#利用sled来判断mirror与否
	ctl_mirror	= checkBox('subCtl_mirrorCB',q=1,v=1) if not sled else 0
	
	mainText,subText,ctlMirror,str1,str2,mirCtls,inf_vtx	= '','','','','',[],[]

	selectionRaw =ls(sl=1,fl=1) if not sled else sled
	
	#散骨点的情况比较简单
	if not selectionRaw:
		return 5
	sl_poly = selectionRaw[0].split('.')[0]
 
	#点，线，面，就是最普通的物体固定
	if objectType(selectionRaw[0])=='mesh':
		if sl_poly == selectionRaw[0]:
			return 0
		if not attributeQuery("subPoly",ex=1,node=sl_poly) and not attributeQuery("mainPoly",ex=1,node=sl_poly):
			return 1
		if attributeQuery("subPoly",ex=1,node=sl_poly):
			mainText = sl_poly
			conn = listConnections("%s.subPoly"%mainText)
			if conn:
				subText = conn[0]
			else:
				return 4
		if attributeQuery("mainPoly",ex=1,node=sl_poly):
			subText = sl_poly
			conn = listConnections("%s.mainPoly"%subText)
			if conn:
				mainText = conn[0]
			else:
				return 4
	#选择骨骼就是做主控了


    ##生成了次级骨骼


	if ctl_mirror:
		str1 = textField("subCtl_mirrorField01",q=1,tx=1)
		str2 = textField("subCtl_mirrorField02",q=1,tx=1)
		ctlMirror = ctlText.replace(str1,str2,1)
		if ctlMirror == ctlText:
			return 2
	select(cl=1)
	initObj = joint(p=[0,0,0],n=ctlText+'pin')
	if objExists(initObj):
		initObj = rename(initObj,initObj+"#")
	raw_len,raw_mesh = len(selectionRaw)- 1,[]
	for index,sl in enumerate(selectionRaw):
		if objectType(sl)=='mesh':
			raw_mesh.append([sl,index])
	sub_loc = 1 if raw_len>1 and (len(raw_mesh) == 1 and raw_mesh[0][1] == raw_len) else 0
	
	
	
	
	
	
	#-------------------------------------------
	#
	#	不选择 component时，先执行这里
	#
	#-------------------------------------------
	if objectType(selectionRaw[-1])!='mesh' or sub_loc:
		#最后选择poly，这样才会固定
		
		sl_poly = selectionRaw[-1].split('.')[0]

		sl_len = len(selectionRaw)
		sl_shape = listRelatives(sl_poly,s=1,type='mesh')
		#单独做mesh添加控制器
		sl_mesh = []
		for item in selectionRaw:
			if not attributeQuery("subPoly",ex=1,node=item) and not attributeQuery("mainPoly",ex=1,node=item):
				shape = listRelatives(item,s=1,type='mesh')
				if shape:
					sl_mesh.append(item)
		if len(selectionRaw) == len(sl_mesh):
			#ctlMirror = ''
			lz_subCtl_simpleCtl(selectionRaw,ctlText,ctl_scale,lz_ctl_factory(ctl_style),ctlMirror,[str1,str2],ctl_name = ctl_name,clu= clu)
			delete(initObj)
			lz_print("简单控制器已添加 \\n")
			return 100	
		
		#对组和joint，cluster类添加控制器
		if not attributeQuery("subPoly",ex=1,node=sl_poly) and not attributeQuery("mainPoly",ex=1,node=sl_poly) and not sl_shape:	
			flag = 1
			#排除重复添加
			for item in selectionRaw:
				shape_i = listRelatives(item,s=1,type='nurbsCurve')
				if shape_i:
					flag = 0
					break

			if flag:
				lz_subCtl_simpleCtl(selectionRaw,ctlText,ctl_scale,lz_ctl_factory(ctl_style),ctlMirror,[str1,str2],ctl_name = ctl_name,clu= clu)
				delete(initObj)
				lz_print("简单控制器已添加 \\n")
				return 100
		
		#---------------------------------------------------------------------------
		#
		#	下面就是主控转次控过程
		#
		#---------------------------------------------------------------------------
		if sl_len<2 or not sl_shape:
			select(selectionRaw)
			delete(initObj)
			return 8
		ctls =  []
		ctls_mir = []
		ctls_now = []
		#可能会选择到一些poly和未添加控制器的物体
		
		sled_mod = []

		for item in selectionRaw[:-1] :
			shape_i = listRelatives(item,s=1,type='nurbsCurve')
			shapeMesh = listRelatives(item,s=1,type='mesh')
			if not shape_i:
				sled_mod.append(item)
			if shape_i and not shapeMesh:
				ctls.append(item)
		if sled_mod:
			ctls += lz_subCtl_simpleCtl(sled_mod,ctlText,ctl_scale,lz_ctl_factory(ctl_style),ctlMirror,[str1,str2],ctl_name = ctl_name,clu= clu)
		
		#确定mainText，有无次控都可以添加
		mainText = sl_poly
		if attributeQuery("subPoly",ex=1,node=sl_poly):
			mainText = sl_poly
		if attributeQuery("mainPoly",ex=1,node=sl_poly):
			subText = sl_poly
			conn = listConnections("%s.mainPoly"%subText)
			if conn:
				mainText = conn[0]
			else:
				mainText = sl_poly	
					
		#找到可以对称的控制器
		if ctl_mirror:
			for ctl in ctls:
				if ctl.find(str1)!=-1:
					ctl_mir = ctl.replace(str1,str2,1)
					if objExists(ctl_mir):
						ctls_mir.append(ctl_mir)
				if ctl.find(str2)==-1: 
					ctls_now.append(ctl)
		else:
			ctls_now = ctls
		#排除重复添加
		for ctl in ctls_now:
			if attributeQuery('upperGrp',ex=1,node=ctl):
				delete(initObj)
				select(selectionRaw)
				return 8
	
		subClt_return = lz_subCtl(initObj,poly =mainText,color=ctl_color,ctl_name = ctl_name,addInf= addInf,noJoint = 1,ctls=ctls_now,components=ctls,parentGrp='MASTER_SUB')
		
		skin_object,subCtls = subClt_return[0],subClt_return[1]
		
		global lz_subCtls
		lz_subCtls += subCtls
		if ctl_mirror:
			sled = ctls_mir+[mainText]
			lz_subCtl_doIt(sled,ctlText =ctlMirror,ctl_color = 'lb',ctl_scale=ctl_scale,ctl_style=ctl_style)
		select(lz_subCtls)
		lz_print("次级控制器添加完成！\\n")
		return 100

	sled_return = lz_subCtl_veToFace(mainText,selectionRaw)
	inf_vtx=sled_return[2]
	
	subClt_return = lz_subCtl(initObj,poly =mainText,color=ctl_color,components=selectionRaw,inf_vtx = inf_vtx,ctl_style = ctl_style,parentGrp='MASTER_SUB',controler_scale=ctl_scale,addInf = addInf)
	skin_object,subCtls = subClt_return[0],subClt_return[1]
	informations = [subText,skin_object,inf_vtx,subCtls]
	#骨骼模型蒙皮
	
	select(selectionRaw)
	lz_subCtl_afterLoft(informations)
	if ctl_mirror:
		shape = listRelatives(mainText,s=1,pa=1)[0]
		sled = lz_mirrorSelection_closestComponent(mainText,shape,inf_vtx)
		lz_subCtl_doIt(sled,ctlText =ctlMirror,ctl_color = 'lb',ctl_scale=ctl_scale,ctl_style=ctl_style)
	lz_print("次级控制器添加完成！\\n")
	return 100
"""
def lz_subCtl_recover(doPrint = 1):
	sl = lz_ls()
	last_item = sl[-1]
	last_shape = listRelatives(last_item,s=1,pa=1)
	inf_vtx,attach_locs,tar_attachGrps,new_poly = [],[],[],''
	tar_attachGrps = lz_subCtl_tarAttach(last_item)
	if last_shape:
		if objectType(last_shape[0]) == 'mesh':
			new_poly = last_item

	poly_tar = new_poly if new_poly else ''
	ctls_all = sl if not new_poly else sl[:-1]
	res_return = ''
	
	if tar_attachGrps[0]:
		new_poly = ''
		ctls_all = sl[:-1]
		sl = sl[:-1]
	for index,item in enumerate(ctls_all):
		subCtl_grp = listConnections('%s.upperGrp'%item)[0]
		subCtl_parent = item+'_parent'
		subCtl_move = item+'_move'
		prefix = item.split('ctl')[0]
		setupParent = listRelatives(listRelatives(listRelatives(subCtl_grp,p=1,pa=1)[0],p=1,pa=1)[0],p=1,pa=1)
		setupPa_children = listRelatives(setupParent,c=1,pa=1)
		localGrp = ''
		if setupPa_children:
			for sc in setupPa_children:
				if sc.find('localGrp')!=-1:
					localGrp = sc
					break
		try:
			setAttr(subCtl_parent+'.surfaceFollow',0)
		except:
			subCtl_parent = subCtl_move
			setAttr(subCtl_move+'.surfaceFollow',0)
			pass
		ctl_dup = duplicate(item,po=1,rc=1,n='sub_tmp#')[0]

		up_grp = listRelatives(subCtl_grp,p=1,pa=1)[0]
		pre = up_grp.split('ctls')[0]
		pre_raw = pre.split('pin')[0]
		scale_grp = ''#listConnections('%s.s'%up_grp)[0]
		sub_attachGrp  = pre+'attachGrp'
		lz_connectAttr('lz_scale.s','%s.s'%up_grp)
		infObj,at_old_grp ='',''
		
		paConst = listConnections('%s.rotatePivot'%subCtl_grp)
		fond_at,fond_inf = 0,0
	
		if paConst:
			for n_item in listConnections(paConst[0]):
				if n_item.find(pre_raw)==-1 and not fond_at and listRelatives(n_item,s=1):
					at = n_item
					at_old_grp = listRelatives(at,p=1,pa=1)[0]
					if at.find('_rawPo')!=-1:
						at = at_old_grp
						at_old_grp = listRelatives(at_old_grp,p=1,pa=1)[0]
					
					at_shape = listConnections('%s.t'%at)[0]
					if not poly_tar:
						poly_tar = listConnections('%s.inputMesh'%at_shape)
						if  poly_tar:	
							poly_tar = poly_tar[0]
						else:
							for k_item in listHistory(at_shape,af=1):
								if objectType(k_item) == 'mesh':
									poly_tar = k_item
							
					fond_at =1
				if n_item.find('infObj')!=-1 and not fond_inf:
					infObj = n_item
					fond_inf =1
		if objExists(item+'_infObj'):
			infObj = item+'_infObj'
		if not infObj:
			infObj =  group(em=1,n=item+'_infObj')
			if localGrp:
				parent(infObj,localGrp)
			pointConstraint(localGrp,infObj,mo=1)
		if not  poly_tar and tar_attachGrps[0] :
			at_shape = listRelatives(tar_attachGrps[0],s=1,pa=1)[0]
			if objectType(at_shape) == 'follicle':
				poly_tar = listConnections('%s.inputMesh'%at_shape)[0]
			elif attributeQuery('poly_tar',ex=1,node= tar_attachGrps[0]):
				poly_tar = listConnections('%s.poly_tar'%tar_attachGrps[0])[0]
		if not tar_attachGrps[0]:			
			res_return = lz_pin([ctl_dup],object = poly_tar,attach_upperGrp =sub_attachGrp,scale_grp =scale_grp,addJoint=0,addCtl=0,simple=1,objParent = 0)
			attach_locs = res_return[2]
			inf_vtx		= res_return[5]
		else:
			attach_locs.append(tar_attachGrps[0])
			parent(tar_attachGrps[1],sub_attachGrp)
			lz_connectAttr('%s.s'%scale_grp,'%s.s'%tar_attachGrps[0])
			res_return = lz_pin([ctl_dup],object = poly_tar,attach_upperGrp =sub_attachGrp,scale_grp =scale_grp,addJoint=0,addCtl=0,simple=1,objParent = 0)
			inf_vtx		= res_return[5]		
			lz_delete(res_return[1])
		attach_po_grp = duplicate(attach_locs[0],rc=1,po=1,n=attach_locs[0]+'_rawPo')[0]
		parent(attach_po_grp,attach_locs[0])

		lz_delete([subCtl_grp+"_pointConstraint1",at_old_grp,ctl_dup])

		#lz_xform(subCtl_grp,item,1)
		#lz_xform(attach_po_grp,subCtl_grp,1)
		#处理下所有组的轴心
		
		lz_delete(["%s_hide_parentConstraint1"%item,"%s_hide_scaleConstraint1"%item])
		#lz_xform(item,attach_locs[0],1)
		lz_xform(subCtl_grp,subCtl_parent,1)
		lz_xform(subCtl_grp,attach_locs[0],0)
		lz_xform(subCtl_grp,attach_locs[0],1)
		for sub_item in ['_move','_drivenGrp','_drivenMove','_hideCoGrp','_hideCo','_hide']:
			lz_xform('%s%s'%(item,sub_item),attach_locs[0],1)
		parentConstraint('%s_hideCo'%item,'%s_hide'%item,mo=1)
		scaleConstraint('%s_hideCo'%item,'%s_hide'%item,mo=1)		
		#处理一下 infObj

		po_inf  = listConnections('%s.rotatePivot'%infObj)[0]

		tar_inf =  listConnections('%s.constraintRotatePivot'%po_inf)[0]
		delete(po_inf)
		lz_xform(infObj,subCtl_grp,1)

		#重建点约束
		po = pointConstraint([infObj,attach_po_grp,subCtl_grp],mo=1)[0]
		list = pointConstraint(po,q=True,wal=True)
		for index,m_item in enumerate(list):
			condition = createNode('condition',n=subCtl_grp+'_cond#')
			connectAttr('%s.surfaceFollow'%subCtl_parent,'%s.ft'%condition)
			setAttr('%s.st'%condition,index)
			setAttr('%s.ctr'%condition,1)
			setAttr('%s.cfr'%condition,0)
			connectAttr('%s.ocr'%condition,'%s.%s'%(po,m_item))	

		poly_find = new_poly if new_poly else poly_tar
		sk = lz_findCluster(poly_find,type='skinCluster')
		inf_item = poly_find

		if sk and inf_vtx:		
			inf_item = lz_subCtl_infObject(poly_find,sk,inf_vtx[0])

		if not inf_item:
			ornObj = listConnections('%s.ornObj'%item)
			if ornObj:
				inf_item = ornObj[0]
		lz_delete([subCtl_grp+"_orientConstraint1"])
		orientConstraint(inf_item,subCtl_grp,mo=1)
		parentConstraint(inf_item,infObj,sr=['x','y','z'],mo=1)
		lz_connectAttr('%s.message'%inf_item,'%s.ornObj'%item)
		
		setAttr(subCtl_parent+'.surfaceFollow',1)	
	select(sl)
	
	if doPrint:
		lz_print('次控已恢复！\\n')
	return {'inf_vtx':inf_vtx}

def lz_ls(sl=''):
	if sl:
		try:
			select(sl)
		except:
			pass
	res = ls(sl=1,fl=1)
	if not res:
		res = ['']
	return res

def lz_subCtl_tarAttach(item):
	tar_shape,tar_attach,tar_attachGrp = '','',''
	i = 1
	while(i <5):
		shape  = listRelatives(item,s=1,pa=1)
		if shape:
			shape = shape[0]
			if objectType(shape) == 'follicle':
				tar_shape = shape
			else:
				item = listRelatives(item,p=1,pa=1)
				if item:
					item = item[0]
				else:
					i = 5
		else:
			item = listRelatives(item,p=1,pa=1)
			if item:
				item = item[0]
			else:
				i = 5
			
		i+=1
	if tar_shape:
		tar_attach = listRelatives(tar_shape,p=1,pa=1)[0]
		tar_attachGrp = listRelatives(tar_attach,p=1,pa=1)[0]	
	return [tar_attach,tar_attachGrp]
"""
def lz_mirrorSelection_closestComponent(poly,poly_shape,inf_vtx):
	res = []
	for points in inf_vtx:
		
		if len(points) == 1:
			res.append(lz_mirrorSelection_closestPoint(poly,poly_shape,points,0,2)[0])
		if len(points) == 2:
			temp_points = lz_mirrorSelection_closestPoint(poly,poly_shape,points,0,2)
			if len(temp_points)!=2:
				res.append(temp_points[0])
			else:
				temp_edge = polyListComponentConversion(temp_points,fv=1,te=1,internal=1)
				if temp_edge:
					res.append(temp_edge[0])
				else:
					res.append(temp_points[0])
		if len(points) == 4:
			temp_points = lz_mirrorSelection_closestPoint(poly,poly_shape,points,0,2,resFace=1)
			#res.append(temp_points)
			
			if len(temp_points)!=4:
				res.append(temp_points[0])
			else:
				temp_face = polyListComponentConversion(temp_points,fv=1,tf=1,internal=1)
				if temp_face:
					res.append(temp_face[0])
				else:
					res.append(temp_points[0])
			
	return res

def lz_mirrorSelection_closestPoint(poly,poly_shape,points,type,prec = 2,resFace=0):
	res,resIndex,points_trans,all_points,prec,type =[],[],[],{},int(prec),int(type)
	points_ac,all_ac,prefix,res_prefix=[],[],'%s.vrts[%s]','%s.vtx[%s]'
	vrt_len = getAttr('%s.vrts'%poly_shape,s=True)
	componentF = '%s.f[%d]'
	multi,exp,type_else = [0,0,0],[[-1,1,1],[1,-1,1],[1,1,-1]],[0,1,2]
	del type_else[type]
	multi[type],multi[type_else[0]],multi[type_else[1]] = .5,.25,.25
	#得到所有选择的点的位置


	for vertex in points:
		if vertex == "":
			continue
		trans = getAttr(prefix%(poly_shape,vertex))[0]
		temp = lz_listMulti(trans,exp[type])
		tempX,tempY,tempZ = round(temp[0],prec),round(temp[1],prec),round(temp[2],prec)
		points_trans.append([tempX,tempY,tempZ,temp[0],temp[1],temp[2]])
	#if prec == 3:
	sub_parent = listRelatives(poly,p=1,pa=1)
	poly_dup = duplicate(poly)[0]
	lz_hideAttr(poly_dup,['t','r','s'],1)
	if sub_parent:
		parent(poly_dup,w=1)
	makeIdentity(poly_dup,a=1,s=1,r=1,t=1)
	shape = listRelatives(poly_dup,s=1,type='mesh')[0]
	pointOnMesh = createNode('closestPointOnMesh',n=poly_dup+'clo#')
	connectAttr('%s.outMesh'%shape,'%s.inMesh'%pointOnMesh)
	#得到所有shape上的点的位置
	for i in range(vrt_len):
		trans = getAttr(prefix%(poly_shape,i))[0]
		tempX,tempY,tempZ = round(trans[0],prec),round(trans[1],prec),round(trans[2],prec)
		temp = [tempX,tempY,tempZ]
		if temp[type] in all_points:
			all_points[temp[type]].append(temp+[i,trans[0],trans[1],trans[2]])
		else:
			all_points[temp[type]] = [temp+[i,trans[0],trans[1],trans[2]]]
	#把对称的点选出来
	for tran_index,tran in enumerate(points_trans):
		if tran[type] in all_points:
			for item in all_points[tran[type]]:		
				all_ac.append([item[3],item[4],item[5],item[6]])
			if all_ac:
				min_vtx		= all_ac[0][0]
				min_index	= 0 
				min_value	= 1
				for index,item in enumerate(all_ac):
					#最短距离还需要一个权重，对称X以X权重最大
					temp_value = abs(multi[0]*(item[1]-tran[3]))+abs(multi[1]*(item[2]-tran[4]))+abs(multi[2]*(item[3]-tran[5]))
					if temp_value<min_value:
						min_value	= temp_value
						min_vtx		= item[0]
						min_index	= index
				res.append(res_prefix%(poly,min_vtx))
				del all_ac[min_index]
		else:
			setAttr('%s.inPosition'%pointOnMesh,tran[3],tran[4],tran[5])
			vIndex = getAttr('%s.closestVertexIndex'%pointOnMesh)
			res.append(res_prefix%(poly,vIndex))
	delete(poly_dup)
	return res

def lz_listMulti(listObj1,number,divide=0):
	list_res = []
	if isinstance(number,list):
		if len(listObj1) != len(number):
			return -1
		else:
			for index,obj in enumerate(listObj1):
				if not divide:
					list_res.append(obj*number[index])
				else:
					list_res.append(obj/number[index])	
			return list_res
		
	for index,obj in enumerate(listObj1):
		if not divide:
			list_res.append(obj*number)
		else:
			if obj!=0:
				list_res.append(obj/number)
			else:
				list_res.append(obj)
	return list_res
	
def lz_selectComTargets(plug,preValue=1,attrName='messageArray',removeShape=1):
	allObjs	= ls(sl=True)
	single	= plug.split('.')[0]
	list	= allObjs if about(v=1) =='2011' else [single]
	selection = []
	for obj in list:
		if not objExists(obj):
			continue
		if attributeQuery(attrName,node=obj,ex=True):
			children = attributeQuery(attrName,node=obj,lc=True)
			for index,item in enumerate(children):
				tar = listConnections('%s.%s.%s'%(obj,attrName,item),p=1)
				if tar:
					res_temp = tar[0].split('.')[0]
					if removeShape and objectType(res_temp) == 'nurbsCurve':
						continue
					selection.append(res_temp)
	selection.append(single)
	try:
		select(selection)
	except:
		pass
	return selection
	
def lz_rotateCV(objects,rt = [0,0,90]):
	for obj in objects:
		shape = listRelatives(obj,s=True)[0]
		if objectType(shape) == 'nurbsCurve':
			number = getAttr('%s.spans'%shape)
			degree = getAttr('%s.degree'%shape)
			cv = '%s.cv[0:%d]'%(shape,number+degree-1)
		elif objectType(shape) == 'nurbsSurface':
			number = getAttr('%s.controlPoints'%shape,s=True)
			cv = '%s.cv[0:%d]'%(shape,number-1)
		piv = xform(obj,q=True,ws=True,rp=True)
		rotate(rt[0],rt[1],rt[2],cv,p=piv,r=True)
		
def create_lahuan():
	import maya.mel as mm
	return mm.eval("curve -d 3 -p 0 -0.00398928 -0.00120638 -p 0 1.747161 -0.00080425 -p 0 3.221762 -0.000402125 -p 0 4.982262 0 -p 0 4.982262 0 -p 0 4.982262 0 -p 0 5.021229 -0.265841 -p 0 5.19865 -0.783612 -p 0 5.982262 -1.108194 -p 0 6.765874 -0.783612 -p 0 7.090456 0 -p 0 6.765874 0.783612 -p 0 5.982262 1.108194 -p 0 5.19865 0.783612 -p 0 5.009554 0.244509 -p 0 4.982262 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 13 -k 13 ;")

