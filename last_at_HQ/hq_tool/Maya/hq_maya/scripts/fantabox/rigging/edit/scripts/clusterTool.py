# coding=gbk

import maya.OpenMaya as om
import maya.cmds as mc
from maya.cmds import *
import maya.mel as mm
import os,sys,re,math,random




def lz_sub_CtlToClu(subCtl):
	res = []
	tar_hide = subCtl+'_hide'
	tar_trans = listConnections('%s.t'%tar_hide)
	tar_item_split = subCtl.split('_ctl')
	tar_item = tar_item_split[0]+tar_item_split[1]

	if tar_trans:
		if tar_item in tar_trans:
			tar_trans = tar_item
		else:
			tar_trans = tar_trans[0]
		
		shape = listRelatives(tar_trans,s=1,pa=1)
		if shape:
			res = tar_trans
		else:
			
			constraint = listConnections('%s.rotatePivot'%tar_trans)
			if constraint:
				res = listConnections('%s.constraintRotatePivot'%constraint[0])[0]
	return res	




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



def lz_clu_findIndex(clu,poly):
	groupParts = listConnections('%s.outputGeometry'%clu)
	clu_index = -1
	for index,item in enumerate(groupParts):
		shp = listRelatives(item,s=1,pa=1)
		if shp:
			clu_index = index
			break
		all_his = listHistory(item,af=1,ag=1)
		for his in all_his:
			if his.find('tweak')!=-1:
				poly_tweak = listConnections('%s.vlist'%his)
				if not poly_tweak:
					poly_set = listConnections('%s.message'%his)
					poly_tweak = listConnections('%s.dagSetMembers'%poly_set[0])
				if poly == poly_tweak[0]:
					clu_index = index
					
					break
		if clu_index!=-1:
			break
			
	plug = listConnections('%s.outputGeometry'%clu,p=1)[index]
	clu_index_plug = listConnections(plug,p=1)[0]
	clu_index = int(clu_index_plug.split('[')[1].split(']')[0])	
	
	return clu_index



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
			temp_list.append(po_list)
		
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




def lz_cluToJo(trans=[],makeSkin = 0,otherPoly = 0,poly_dup = '' ):
	trans = lz_ls() if not trans else trans
	skin_new,base_jo = '',''
	joints_all = []
	poly_dup = poly_dup
	for tran in trans:
		po_index1,po_index2 = [],[]
		if not tran:
			continue
		clu = listConnections('%s.worldMatrix[0]'%tran)
		if not clu:
			continue
		if isinstance(clu,list):
			clu = clu[0]
		if objectType(clu) != 'cluster':
			continue
		count = getAttr('%s.weightList'%clu,s=1)
		set_clu = 	 listConnections('%s.message'%clu)[0]
		poly = listConnections('%s.dagSetMembers'%set_clu)[-1]

		select(tran)	
		EditMembershipTool()
		points = lz_ls()
		setToolTo('selectSuperContext')
		po_real = []
		for  po in points:
			if po.find(poly)!=-1:
				po_real.append(po)
		#print poly		
		lz_mirrorSelection_getIndex(po_index1,po_real)	
		clu_index = lz_clu_findIndex(clu,po_real[0].split('.')[0])	
		if not otherPoly:
			poly = po_real[0].split('.')[0]
		else:
			if not poly_dup:
				poly = duplicate(po_real[0].split('.')[0],n=poly+'_dupPoly')[0]
				poly_dup = poly
			else:
				poly = poly_dup
		sk = lz_findCluster(poly,type='skinCluster')
		if not makeSkin:
			if not sk:
				lz_warning(' 当前没有蒙皮 ！')
				return ['','']
		elif not sk:
			select(cl=1)
			base_jo = joint(n='tmp_baseJo#')
			sk = skinCluster(base_jo,poly)[0]

		skin_new = sk
		trans = xform(tran,q=1,rp=1,ws=1)	
		select(cl=1)
		jo = joint(p=trans,n=tran+'_jo')
		skinCluster(sk,ai= jo,lw = 1,e=1,wt=0) 
		setAttr('%s.liw'%jo,0)
		select (jo)
		for index,item in enumerate(po_index1):
			va = getAttr('%s.weightList[%d].weights[%s]'%(clu,clu_index,item))
			skinPercent(sk,'%s.vtx[%s]'%(poly,item),tv=(jo,va))
		setAttr('%s.liw'%jo,1)
		select (jo)
		joints_all.append(jo)
	return [skin_new,base_jo,joints_all,poly_dup]





def lz_pre_simpleMirror(jo,sameParent= 1):
	if not jo:
		return 
	if objectType(jo)!='joint':
		return
	select(cl=1)
	jo_temp = joint(p=[0,0,0])
	jo_parent = listRelatives(jo,pa=1,p=1)
	parent(jo,jo_temp)
	if jo.find('l_')!=-1:
		mir_jo = mirrorJoint(jo,mirrorYZ=1,mirrorBehavior=1,sr=['l_','r_'])[0]
	else:
		mir_jo = mirrorJoint(jo,mirrorYZ=1,mirrorBehavior=1,sr=['r_','l_'])[0]
	if jo_parent:
		if sameParent:
			parent(mir_jo,jo_parent[0])
		else:
			parent(mir_jo,w=1)
		parent(jo,jo_parent[0])
	else:
		parent(mir_jo,w=1)
		mir_jo = lz_ls()[0]
		parent(jo,w=1)

	delete(jo_temp)
	if attributeQuery('children',ex=1,node=mir_jo):
		children = listRelatives(mir_jo,ad=1,pa=1)
		for c in children:
			if attributeQuery('child',ex=1,node=c):
				lz_connectAttr('%s.children'%mir_jo,'%s.child'%c)
	return mir_jo




def lz_print(txt = ''):
	mm.eval('print "'+u(txt)+'"')



def u(txt=''):
	return unicode(txt,'gbk')




def lz_sub_CtlToClu(subCtl):
	res = []
	tar_hide = subCtl+'_hide'
	tar_trans = listConnections('%s.t'%tar_hide)
	tar_item_split = subCtl.split('_ctl')
	tar_item = tar_item_split[0]+tar_item_split[1]

	if tar_trans:
		if tar_item in tar_trans:
			tar_trans = tar_item
		else:
			tar_trans = tar_trans[0]
		
		shape = listRelatives(tar_trans,s=1,pa=1)
		if shape:
			res = tar_trans
		else:
			
			constraint = listConnections('%s.rotatePivot'%tar_trans)
			if constraint:
				res = listConnections('%s.constraintRotatePivot'%constraint[0])[0]
	return res




def lz_warning(txt = ''):
	mm.eval('warning "'+u(txt)+'"')




def lz_findCluster(obj,type=''):
	global lz_skin_skinSys
	lz_skin_skinSys = 0
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
		history = listHistory(obj,ag=1,gl=2,pdo=1)
	if not history:
		return sk

	for h in history:
		t = objectType(h)
		if t and t==type:
			sk=h
			break
	return sk




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





def lz_skin_getAverage():
	global lz_weight_jo
	global lz_weight_jo_sort
	global lz_weight_data_collection
	lz_weight_jo_sort = []
	lz_weight_jo = {}
	lz_weight_data_collection = {}
	points_st = []
	str_len = 36
	pre_return = lz_skin_prepare()
	if pre_return[0] == 0:
		return
	if pre_return[0]==800:
		window('lz_skin_window',e=1,title= u('权重辅助工具 (选择点数量超过600，不予显示)'))
		return
	window('lz_skin_window',e=1,title= u('权重辅助工具'))
	weight = floatSliderButtonGrp('skin_weight',q=True,v=True)
	jointName= textFieldButtonGrp('skin_jointName',q=True,tx=True)
	
	poly,shape_type,sk,componentV,sl = pre_return[0],pre_return[1],pre_return[2],pre_return[3],pre_return[4]
	lz_mirrorSelection_getIndex(points_st,sl)
	p_len = len(points_st)
	
	if objectType(sk) == "fmSkinCluster":
		infs = listConnections ("%s.lockWeights"%sk)
		for index,infName in enumerate(infs):
			for item in points_st:
				item_name = "[%s]"%item
				skin_value = getAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,item,str(index)))
				if item_name not in lz_weight_data_collection:
					lz_weight_data_collection[item_name] = {}
				if infName not in lz_weight_data_collection[item_name]:
					lz_weight_data_collection[item_name][infName] = skin_value
				if skin_value and infName not in lz_weight_jo_sort:
					lz_weight_jo_sort.append(infName)		
	
	if objectType(sk) == "skinCluster":	
		infs= listConnections('%s.matrix'%sk)
		for index,infName in enumerate(infs):
			for item in points_st:
				item_name = ''
				if shape_type==0 or  shape_type==2:
					item_name = "[%s]"%item
					skin_value = skinPercent(sk,componentV%(poly,int(item)),q=True,v=True,t=infName)
				elif shape_type== 1:
					item_name = "[%s][%s]"%(item[0],item[1])
					skin_value = skinPercent(sk,componentV%(poly,int(item[0]),int(item[1])),q=True,v=True,t=infName)
				elif  shape_type== 3:
					item_name = "[%s][%s][%s]"%(item[0],item[1],item[2])
					skin_value = skinPercent(sk,componentV%(poly,int(item[0]),int(item[1]),int(item[2])),q=True,v=True,t=infName)
				if item_name not in lz_weight_data_collection:
					lz_weight_data_collection[item_name] = {}
				if infName not in lz_weight_data_collection[item_name]:
					lz_weight_data_collection[item_name][infName] = skin_value
				if skin_value and infName not in lz_weight_jo_sort:
					lz_weight_jo_sort.append(infName)
	
	for index,infName in enumerate(lz_weight_jo_sort):
		sum = 0
		value_flag = 0
		for item in points_st:
			item_name = ''
			if shape_type==0 or  shape_type==2:
				item_name = "[%s]"%item
			elif shape_type==1:
				item_name = "[%s][%s]"%(item[0],item[1])
			elif shape_type==3:
				item_name = "[%s][%s][%s]"%(item[0],item[1],item[2])
			skin_value = lz_weight_data_collection[item_name][infName]
			loc_flag = getAttr('%s.liw'%infName)			
			sum += skin_value
			value_flag+=1

			if infName not in lz_weight_jo:
				name_all,name_len = infName,0.0
				for char in infName:
					if ord(char)>=65 and ord(char)<=90:
						name_len+=2
					elif ord(char)>=48 and ord(char)<=57:
						name_len+=1.6
					elif char =='|':
						name_len +=.75
					elif char == 'm' or char == 'w' or char =='_':
						name_len +=2.0
					else:
						name_len+=1.0
				#print int(name_len)
				if name_len<str_len:
					lenScale = (str_len-name_len)*1.25
					int_lenScale = int(lenScale)
					name_all = infName+" "*int_lenScale
					if lenScale - int_lenScale>0.5:
						name_all+= " "
					
					#print (infName+" "+str(str_len)+" "+str(name_len))
				elif name_len>str_len:
					name_all = "..."+infName[int(name_len)-str_len+2:]
				mid_str = " "*2+'(HOLD)'+" "*6 if loc_flag else " "*20
				lz_weight_jo[infName] = [name_all,'']
				#print name_all+mid_str+"AA"

		sum = sum/value_flag
		sum_str = str(round(sum,3))
		if sum_str>5:
			sum_str = sum_str[:5]
		lz_weight_jo[infName][1] = sum_str
		
	lz_weight_jo_sort.sort()










def lz_weight(points=[],infName ='',poly='',ap=0,value=0,copy = 0,prune = [],keep=0,tool_change = 0):
	global lz_weight_jo_sort
	global lz_skin_pointWeight
	global lz_weight_data_collection
	lz_skin_pointWeight = {}
	componentV,componentCV= '%s.vtx[%d]','%s.cv[%d][%d]'
	points_st,infs_real =[],[]
	sum=0.0
	sk = lz_findCluster(poly)
	if not sk:
		return []
	if objectType(sk) == "fmSkinCluster":
		infs = listConnections ("%s.lockWeights"%sk)

		if infName and points:
			if infName not in infs:
				return []
			index = infs.index(infName)
			lz_mirrorSelection_getIndex(points_st,points)
			p_len = len(points_st)
			if not ap:
				for item in points_st:
					sum += getAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,item,str(index)))
				sum = sum/p_len
			else:
				setAttr('%s.liw'%infName,0)
				for item in points_st:
					setAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,item,str(index)),value)
				#setToolTo('selectSuperContext')
				if tool_change:
					mm.eval('artAttrFmSkinToolScript(4)')
				#refresh()

		if not points and infName and poly:
			if infName not in infs:
				return []
			index = infs.index(infName)
			poly_shape = listRelatives(poly,s=1,pa=1)[0]
			vrt_len = getAttr('%s.vrts'%poly_shape,s=True)
			for item in range(vrt_len):
				value = getAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,item,str(index)))
				if value>=0.001:
					points.append(componentV%(poly,item))
			select(points+[poly])
			setToolTo("selectSuperContext")
			hilite(poly)
			#mm.eval('doMenuComponentSelection("'+poly+'", "vertex");')
			
		if copy ==1:
			lz_skin_pointWeight = {}
			lz_mirrorSelection_getIndex(points_st,points)
			for index,tar in enumerate(infs):
				value = getAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,points_st[0],str(index)))
				if value:
					lz_skin_pointWeight[tar] = value
		if copy ==2:
			lz_skin_toggleLock(0)
			lz_mirrorSelection_getIndex(points_st,points)
			targets = []
			for index,tar in enumerate(infs):
				value = getAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,points_st[0],str(index)))
				if tar not in lz_skin_pointWeight:
					targets.append(tar)
			for index,item in enumerate(lz_skin_pointWeight):
				inf_index = infs.index(item)
				for sub_item in points_st:
					setAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,sub_item,inf_index),lz_skin_pointWeight[item])
				setAttr('%s.liw'%item,1)
			for index,item in enumerate(targets):
				inf_index = infs.index(item)
				for sub_item in points_st:
					setAttr('%s.userWeightList[%s].userWeights[%s]'%(sk,sub_item,inf_index),0)
				setAttr('%s.liw'%item,1)
			lz_skin_toggleLock(0)

	if objectType(sk) == "skinCluster":
		targets= listConnections('%s.matrix'%sk)
		if infName and points:
			p_len = len(points)
			if infName not in targets:
				return []
			if not ap:
				for point in points:
					sum +=skinPercent(sk,point,q=True,v=True,t=infName)
				sum = sum/p_len
			else:
				setAttr('%s.liw'%infName,0)
				for p in points:
					skinPercent(sk,p,tv=(infName,value))
				if tool_change:	
					mm.eval('ArtPaintSkinWeightsTool;')
		if not points and infName and poly:
			poly_shape = listRelatives(poly,s=1,pa=1)[0]
			if infName not in targets:
				return []
			if objectType(poly_shape) =="mesh":
				vrt_len = getAttr('%s.vrts'%poly_shape,s=True)
				for point in range(vrt_len):
					value =skinPercent(sk,componentV%(poly,point),q=True,v=True,t=infName)
					if value>=0.001:
						points.append(componentV%(poly,point))
				select(points+[poly])
				setToolTo("selectSuperContext")
				hilite(poly)
			else:
				degreeU = getAttr('%s.degreeU'%poly_shape)
				degreeV = getAttr('%s.degreeV'%poly_shape)
				spanU = getAttr('%s.spansU'%poly_shape) + degreeU 
				spanV = getAttr('%s.spansV'%poly_shape) +degreeV 
				for item1 in range(spanU):
					for item2 in range(spanV):
						value =skinPercent(sk,componentCV%(poly,item1,item2),q=True,v=True,t=infName)
						if value>0:
							points.append(componentCV%(poly,item1,item2))
				select(points+[poly])
				setToolTo("selectSuperContext")
				mm.eval('doMenuComponentSelection("'+poly+'", "controlVertex");updateObjectSelectionMasks;updateComponentSelectionMasks;')
		if copy ==1:
			lz_skin_pointWeight ={}
			for tar in targets:
				value = skinPercent(sk,points,t=tar,q=True)
				if value:
					lz_skin_pointWeight[tar] = value
		if copy ==2:
			lz_skin_toggleLock(0)
			
			for index,item in enumerate(lz_skin_pointWeight):
				if index:
					skinPercent(sk,points,tv=[item,lz_skin_pointWeight[item]])
					setAttr('%s.liw'%item,1)
				else:
					if lz_skin_pointWeight[item] !=1:
						skinPercent(sk,points,tv=[item,.5])
						targets= skinCluster(sk,wi=1,q=1)
						for tar in targets:
							if tar !=item:
								skinPercent(sk,points,tv=[tar,0])
								setAttr('%s.liw'%tar,1)
						lz_skin_toggleLock(0)
					else:
						skinPercent(sk,points,tv=[item,1])
			lz_skin_toggleLock(0)
		if prune  and poly :
			poly_shape = listRelatives(poly,s=1,pa=1)[0]
			progressWindow(title='Prune Weights ...'
								,progress=0
								,status='percent: 0%'
								,isInterruptable=1)
			if objectType(poly_shape) =="mesh":
				vrt_len = getAttr('%s.vrts'%poly_shape,s=True)
				points_all = range(vrt_len) 
				points_st = []
				if points:
					lz_mirrorSelection_getIndex(points_st,points)
					if points_st[0] !='':
						points_all = points_st
				targets= lz_weight_jo_sort
				percent_v = 100.0/len(points_all)
				for index,point in enumerate(points_all):
					value_pair = []
					for tar in targets:
						value = lz_weight_data_collection['[%s]'%point][tar]#skinPercent(sk,componentV%(poly,point),q=True,v=True,t=tar)
						if value>0.0:
							setAttr('%s.liw'%tar,0)
						else:
							setAttr('%s.liw'%tar,1)
						if value<=0.01:
							value_pair.append(tar)
					for item in value_pair:
						skinPercent(sk,componentV%(poly,point),tv=[item,0])
						setAttr('%s.liw'%item,1)
					if progressWindow(q=1,ic=1):
						progressWindow(endProgress=1)
						break
					progressWindow(edit=1, progress=int(percent_v*index),status=('percent: '+str(percent_v*index)[:4]+'%'))

					#points.append(componentV%(poly,point))
			progressWindow(endProgress=1)
		if keep == 1 and poly :
			poly_shape = listRelatives(poly,s=1,pa=1)[0]
			if objectType(poly_shape) =="mesh":
				vrt_len = getAttr('%s.vrts'%poly_shape,s=True)
				points_all = range(vrt_len) 
				targets= lz_weight_jo_sort
				for index,point in enumerate(points_all):
					for tar in targets:
						value = lz_weight_data_collection[point][tar]#skinPercent(sk,componentV%(poly,point),q=True,v=True,t=tar)			
						if value>0.2:
							setAttr('%s.liw'%tar,0)
							skinPercent(sk,componentV%(poly,point),tv=[tar,value+0.001])
							#skinPercent(sk,componentV%(poly,point),tv=[tar,value])
							break

	if objectType(sk) == "cMuscleSystem":
		if copy ==1:
			lz_skin_pointWeight = {}
			lz_mirrorSelection_getIndex(points_st,points)
			targets = mm.eval('cMuscleQuery -system "'+sk+'" -mus;')
			for tar in targets:
				value = mm.eval('cMuscleWeight -system "'+sk+'" -mus "'+tar+'" -wt "sticky" -pi '+str(points_st[0])+' -q -v') 
				if value[0]>=0.001:
					lz_skin_pointWeight[tar] = value[0]
		if copy ==2:
			select(points)
			lz_skin_toggleLock(0)
			sk2 = lz_findCluster(poly,'skinCluster')
			env = 0 
			if sk2:
				env = getAttr('%s.envelope'%sk2)
			if not env:
				for index,item in enumerate(lz_skin_pointWeight):
					if index:
						mm.eval('cMuscleWeight -system "'+sk+'" -mus "'+item+'" -wt "sticky"  -v '+str(lz_skin_pointWeight[item])) 
						mm.eval('cMuscleWeight -system  "'+sk+'" -muscle "'+item+'" -wt "sticky" -lock 1');
					else:
						mm.eval('cMuscleWeight -system "'+sk+'" -mus "'+item+'" -wt "sticky"  -v 1')
			else:
				targets = mm.eval('cMuscleQuery -system "'+sk+'" -mus;')
				for tar in targets:
					mm.eval('cMuscleWeight -system "'+sk+'" -mus "'+tar+'" -wt "sticky"  -v 0') 
				for index,item in enumerate(lz_skin_pointWeight):
					mm.eval('cMuscleWeight -system "'+sk+'" -mus "'+item+'" -wt "sticky"  -v '+str(lz_skin_pointWeight[item])) 
					mm.eval('cMuscleWeight -system  "'+sk+'" -muscle "'+item+'" -wt "sticky" -lock 1');	
			lz_skin_toggleLock(0)
			#lz_skin_toggleLock(0)
	#setAttr fmSkinCluster1.userWeightList[1093].userWeights[10] 0.2;
	return [points,sum,lz_skin_pointWeight]




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













def lz_cluster():
	sl = lz_ls()
	obj_pair = {}
	clu_sl = ''
	sl_f ,sl_new = [],[]

	for item in sl:
		if item.find('.f[')!=-1 or item.find('.e[')!=-1:
			sl_f.append(item)
		else:
			sl_new.append(item)
	if sl_f:
		select(sl_f)
		sl1 = polyListComponentConversion(fe=1,tv=1)
		sl2 = polyListComponentConversion(ff=1,tv=1)
		sl3 = sl1+sl2
		if sl3:
			select(sl3)	
	if sl_new:
		select(sl_new,add=1)
	sl = ls(selection=True,fl=1)
	cur_obj = ''
	for item in sl:
		if item.find('.') !=-1:
			obj = item.split('.')[0]				
			if obj not in obj_pair:
				obj_pair[obj] = [item]
			else:
				obj_pair[obj].append(item)
		else:
			shape = listRelatives(item,s=1,pa=1)
			if shape:
				if objectType(shape[0]) == 'clusterHandle':
					clu_sl = listConnections('%s.worldMatrix[0]'%item)[0]
				if objectType(shape[0]) == 'nurbsCurve':
					clu_trans  =lz_sub_CtlToClu(item)
					if clu_trans:
						shape = listRelatives(clu_trans,s=1,pa=1)
						if shape:
							if objectType(shape[0]) == 'clusterHandle':
								clu_sl = listConnections('%s.worldMatrix[0]'%clu_trans)[0]
					cur_obj = item			
	if not obj_pair:
		clu_mirs = cluster(rel=1)
		return
	clu_mirs,clu_raw = [],''	

	if not clu_sl:	
		clu_raw = cluster(rel=1)[0]	
		trans_ex = xform('%sHandle'%clu_raw,q=1,ws=1,rp=1)
		select(cl=1)
		clu_mirs = cluster(rel=1)
		setAttr('%sHandleShape.origin'%clu_mirs[0],trans_ex[0],trans_ex[1],trans_ex[2])
		lz_xform('%sHandle'%clu_mirs[0],'%sHandle'%clu_raw,1)
	else:
		select(cl=1)
		clu_raw = cluster(rel=1)[0]	
		clu_mirs =	[clu_sl]	
	for index,obj in enumerate(obj_pair):
		weight_item,weight_item_index,weight_value = [],[],[]
		obj_dup = duplicate(obj,n=obj+'_dup')[0]
		select(obj_pair[obj])
		shape = listRelatives(obj_dup,s=1,pa=1)[0]
		if objectType(shape) == 'mesh':
			sl = ls(selection=True,fl=1)
			sl_new = []
			for v in sl:
				sl_new.append(v.replace(obj,obj_dup,1))
			select(sl_new)
			move(10,0,0,r=1)
			vrt_len = getAttr('%s.vrts'%shape,s=True)
			for number in range(vrt_len):
				va = getAttr('%s.pnts[%d]'%(obj_dup,number))[0][0]			
				if va>0:
					weight_item.append('%s.vtx[%d]'%(obj,number))
					weight_item_index.append(number)
					weight_value.append(va/10.0)
	
		if objectType(shape) == 'nurbsSurface':
			sl = ls(selection=True,fl=1)
			sl_new = []
			for v in sl:
				sl_new.append(v.replace(obj,obj_dup,1))
			select(sl_new)
			
			#makeIdentity(obj_dup,a=1,t=1,s=1,r=1)
			dU ,dV= getAttr('%s.degreeU'%shape),getAttr('%s.degreeV'%shape)
			sU,sV = getAttr('%s.spansU'%shape),getAttr('%s.spansV'%shape)
			formU,formV = getAttr('%s.formU'%shape),getAttr('%s.formV'%shape)
			nU = dU+sU if formU !=2 else dU+sU-1
			nV = dV+sV if formV !=2 else dV+sV-1
			maxU =  dU+sU if formU !=2 else sU
			maxV = dV+sV if formV !=2 else sV
			n_total = nU*nV
			uv_form = []
	
			all_uv = []		
			for u in range(maxU):
				all_uv.append([])
				for v in range(maxV):
					all_uv[u].append(xform('%s.cv[%d][%d]'%(obj,u,v),q=1,ws=1,t=1)[0])
					if not u:
						uv_form.append(v)
					elif formV ==2:
						uv_form.append(u*(nV+1)+v)
					else:
						uv_form.append(u*maxV+v)	
			move(10,0,0,r=1)
			for u in range(maxU):
				for v in range(maxV):
					va = xform('%s.cv[%d][%d]'%(obj_dup,u,v),q=1,ws=1,t=1)[0]
					va_minus = va - all_uv[u][v]
					if va_minus>0.1:
						weight_item.append('%s.cv[%d][%d]'%(obj,u,v))
						weight_item_index.append(uv_form[maxV*u+v])
						weight_value.append(va_minus/10.0)
		if objectType(shape) == 'nurbsCurve':
			sl = ls(selection=True,fl=1)
			sl_new = []
			for v in sl:
				sl_new.append(v.replace(obj,obj_dup,1))
			select(sl_new)
			dU,sU,formU= getAttr('%s.degree'%shape),getAttr('%s.spans'%shape),getAttr('%s.form'%shape)
			nU = dU+sU if formU !=2 else dU+sU-1
			maxU =  dU+sU if formU !=2 else sU
			all_u = []		
			for u in range(maxU):
				all_u.append(xform('%s.cv[%d]'%(obj,u),q=1,ws=1,t=1)[0])
			move(10,0,0,r=1)
			for u in range(maxU):
				va = xform('%s.cv[%d]'%(obj_dup,u),q=1,ws=1,t=1)[0]
				va_minus = va - all_u[u]
				if va_minus>0.1:
					weight_item.append('%s.cv[%d]'%(obj,u))
					weight_item_index.append(u)
					weight_value.append(va_minus/10.0)
		if objectType(shape) == 'lattice':
			sl = ls(selection=True,fl=1)
			sl_new = []
			for v in sl:
				sl_new.append(v.replace(obj,obj_dup,1))
			select(sl_new)
			uDiv = getAttr('%s.uDivisions'%shape)
			tDiv = getAttr('%s.tDivisions'%shape)
			sDiv = getAttr('%s.sDivisions'%shape)
			item_form = []
			all_pt = []
			for u in range(uDiv):
				all_pt.append([])
				for t in range(tDiv):
					all_pt[u].append([])
					for s in range(sDiv):
						all_pt[u][t].append(xform('%s.pt[%d][%d][%d]'%(obj_dup,s,t,u),q=1,ws=1,t=1)[0])
						item_form.append(u*tDiv*sDiv+t*sDiv+s)
			move(10,0,0,r=1)			
			for u in range(uDiv):
				for t in range(tDiv):
					for s in range(sDiv):
						va = xform('%s.pt[%d][%d][%d]'%(obj_dup,s,t,u),q=1,ws=1,t=1)[0]
						va_minus = va - all_pt[u][t][s]
						if va_minus>0.1:
							weight_item.append('%s.pt[%d][%d][%d]'%(obj,s,t,u))
							weight_item_index.append(item_form[u*tDiv*sDiv+t*sDiv+s])
							weight_value.append(va_minus/10.0)
		if weight_item:			
			set_clu = 	 listConnections('%s.message'%clu_mirs[0])[0]
			select(weight_item)	
			sets(fe= set_clu)
		
			obj_index = '%d'%index 
			objs_plugs = listConnections('%s.dagSetMembers'%set_clu,p=1)
			obj_shape = listRelatives(obj,s=1,pa=1)[0]
			#obj_index = objs.index(obj)
			obj_index = lz_clu_findIndex(clu_mirs[0],obj)
			for sub_index ,sub_item in enumerate(weight_item_index):
				try:
					setAttr('%s.weightList[%s].weights[%s]'%(clu_mirs[0],obj_index,sub_item),weight_value[sub_index])
				except:
					pass
		lz_delete([obj_dup])
	lz_delete(['%sHandle'%clu_raw])	
	if not cur_obj:
		select(listConnections('%s.matrix'%clu_mirs[0])[0])		
	else:
		select(cur_obj)

















def lz_selfMirror_cluster(trans=[],doPrint = 1,mirrorType = 1):
	trans = lz_ls() if not trans else trans
	value_pair = {}
	trans_mir_all,trans_all,clu_mirs =[],[],['','']
	for tran in trans:
		po_index1,po_index2 = [],[]
		if not tran:
			continue
		if attributeQuery('worldMatrix',node = tran,ex=1):
			clu = listConnections('%s.worldMatrix[0]'%tran)
		elif attributeQuery('relative',node = tran,ex=1):	
				continue
		else:
			continue
		if not clu:
			if objExists('%s_hide'%tran):
				tran = listConnections('%s_hide.t'%tran)[0]
				clu = listConnections('%s.worldMatrix[0]'%tran)
			else:
				continue
		if isinstance(clu,list):
			clu = clu[0]
		if objectType(clu) != 'cluster':
			continue
		count = getAttr('%s.weightList'%clu,s=1)

		select(tran)	
		EditMembershipTool()
		points = lz_ls()
		setToolTo('selectSuperContext')

		set_clu = 	 listConnections('%s.message'%clu)[0]
		obj_index = '0' 
		objs_plugs = listConnections('%s.dagSetMembers'%set_clu,p=1)
		poly = listConnections('%s.dagSetMembers'%set_clu)[-1]
		obj_shape = listRelatives(poly,s=1,pa=1)[0]
		obj_index =  lz_clu_findIndex(clu,poly)
		points_new = []
		if count==1:	
			lz_mirrorSelection_getIndex(po_index1,points)
		else:
			for s in points:
				if s.find(poly) !=-1:
					points_new.append(s)
			lz_mirrorSelection_getIndex(po_index1,points_new)	
			points = points_new

		select(points)
		#mir_points = lz_mirrorSelection(type=0,prec=4)
		#lz_mirrorSelection_getIndex(po_index2,mir_points)
		
		#if not mir_points:
		#	continue

		name_mir = tran

		po_neg_index,po_neg = [],[]
		po_pos_index,po_pos = [],[]
		po_mid_index,po_mid = [],[]
		for index,item in enumerate(po_index1):
			vtx = xform('%s.vtx[%d]'%(poly,item),q=1,ws=1,t=1)
			if vtx[0]<0:
				po_neg_index.append(item)
				po_neg.append('%s.vtx[%d]'%(poly,item))
			if vtx[0]>0:
				po_pos_index.append(item)
				po_pos.append('%s.vtx[%d]'%(poly,item))
			if abs(vtx[0])<0.0001:
				po_mid_index.append(item)
				po_mid.append('%s.vtx[%d]'%(poly,item))		

		trans,clu_pos, clu_neg =[],'',''
		mir_points,mir_points_index,mir_points_value = [],[],[]
		if po_mid:
			for index,item in enumerate(po_mid_index):
				va = getAttr('%s.weightList[%s].weights[%s]'%(clu,obj_index,item))
				mir_points.append('%s.vtx[%d]'%(poly,item))
				mir_points_value.append(va)
				mir_points_index.append(item)			
		if po_pos and mirrorType == 1:
			select(po_pos)
			clu_pos = 	cluster(rel=1)[0]

			for index,item in enumerate(po_pos_index):
				va = getAttr('%s.weightList[%s].weights[%s]'%(clu,obj_index,item))
				mir_points.append('%s.vtx[%d]'%(poly,item))
				mir_points_value.append(va)
				mir_points_index.append(item)
				try:
					setAttr('%s.weightList[0].weights[%s]'%(clu_pos,item),va)
				except:
					pass
			poly_dup = duplicate(poly,n=poly+'_dupCluPoly')[0]	
			poly_dup_shape = listRelatives(poly,s=1,pa=1)[0]
			vrt_len = getAttr('%s.vrts'%poly_dup_shape,s=True)
			cluJo_return = lz_cluToJo(trans=['%sHandle'%clu_pos],makeSkin = 1,otherPoly = 1,poly_dup = poly_dup )
			#[skin_new,base_jo,joints_all,poly_dup]
			joints_all= cluJo_return[2]
			jo_mir = lz_pre_simpleMirror(joints_all[0],sameParent= 1)
		
			skinCluster(cluJo_return[0],ai= jo_mir,lw = 1,e=1,wt=0) 
			setAttr('%s.liw'%jo_mir,0)
			#mirrorInverse = 1 if  po_neg else 0
			copySkinWeights( ss=cluJo_return[0], ds=cluJo_return[0], noMirror=0 ,mirrorMode='YZ',mirrorInverse= 0)
			for item in range(vrt_len):
				va = skinPercent(cluJo_return[0],'%s.vtx[%d]'%(poly_dup,item),q=1,v=1,t=jo_mir) 
				if va>0.02:
					mir_points.append('%s.vtx[%d]'%(poly,item))
					mir_points_value.append(va)
					mir_points_index.append(item)
			lz_delete([poly_dup,cluJo_return[1],jo_mir,clu_pos,joints_all[0]])
			
		if po_neg and mirrorType == 2:
			select(po_neg)
			clu_neg = 	cluster(rel=1)[0]		
	
			for index,item in enumerate(po_neg_index):
				va = getAttr('%s.weightList[%s].weights[%s]'%(clu,obj_index,item))
				mir_points.append('%s.vtx[%d]'%(poly,item))
				mir_points_value.append(va)
				mir_points_index.append(item)
				try:
					setAttr('%s.weightList[0].weights[%s]'%(clu_neg,item),va)
				except:
					pass		
			poly_dup = duplicate(poly,n=poly+'_dupCluPoly')[0]	
			poly_dup_shape = listRelatives(poly,s=1,pa=1)[0]	
			vrt_len = getAttr('%s.vrts'%poly_dup_shape,s=True)		
			cluJo_return = lz_cluToJo(trans=['%sHandle'%clu_neg],makeSkin = 1,otherPoly = 1,poly_dup = poly_dup )	
			joints_all= cluJo_return[2]
			jo_mir = lz_pre_simpleMirror(joints_all[0],sameParent= 1)
		
			skinCluster(cluJo_return[0],ai= jo_mir,lw = 1,e=1,wt=0) 
			setAttr('%s.liw'%jo_mir,0)
			#mirrorInverse = 1 if  po_neg else 0
			copySkinWeights( ss=cluJo_return[0], ds=cluJo_return[0], noMirror=0 ,mirrorMode='YZ',mirrorInverse= 1)
			for item in range(vrt_len):
				va = skinPercent(cluJo_return[0],'%s.vtx[%d]'%(poly_dup,item),q=1,v=1,t=jo_mir) 
				if va>0.02:
					mir_points.append('%s.vtx[%d]'%(poly,item))
					mir_points_value.append(va)
					mir_points_index.append(item)
			lz_delete([poly_dup,cluJo_return[1],jo_mir,joints_all[0],clu_neg])
			
		mir_index = '0'	


				

		
		clu_mirs[0] =  listConnections('%s.worldMatrix[0]'%name_mir)
		if not clu_mirs[0]:
			return 
		clu_mirs[0] = clu_mirs[0][0]
		
		clu_mir = clu_mirs[0]
		mir_set_clu = 	 listConnections('%s.message'%clu_mir)[0]
		points_new = []
		for s in mir_points:
			if s.find(poly) !=-1:
				points_new.append(s)
		current_points = []		
		mir_set_clu = 	 listConnections('%s.message'%clu_mir)[0]	
		objs_plugs_mir = listConnections('%s.dagSetMembers'%mir_set_clu,p=1)
		obj_shape_mir = listRelatives(poly,s=1,pa=1)[0]
		mir_index = lz_clu_findIndex(clu_mir,poly)
		select(name_mir)
		EditMembershipTool()					
		cu = lz_ls()
		for c in cu:
			if c.find(poly) !=-1:
				current_points.append(c)
		current_index = []		
		lz_mirrorSelection_getIndex(current_index,current_points)			
		if current_points:
			for index,item in enumerate(current_index):
				#va = getAttr('%s.weightList[0].weights[%s]'%(clu,item))
				try:
					setAttr('%s.weightList[%s].weights[%s]'%(clu_mir,mir_index,item),0)
				except:
					pass

		select(points_new)
		sets(fe=mir_set_clu)
			
		mir_set_clu = 	 listConnections('%s.message'%clu_mir)[0]	
		objs_plugs_mir = listConnections('%s.dagSetMembers'%mir_set_clu,p=1)
		mir_index = lz_clu_findIndex(clu_mir,poly)

		
		trans_mir_all.append(name_mir)
		trans_all.append(tran)
		
		for index,item in enumerate(mir_points_index):
			#va = getAttr('%s.weightList[0].weights[%s]'%(clu,item))
			try:
				setAttr('%s.weightList[%s].weights[%s]'%(clu_mir,mir_index,item),mir_points_value[index])
			except:
				pass
		
		
		if doPrint:
			lz_print('对称完成！\\n')
		
	setToolTo('selectSuperContext')		
	if(trans_all+trans_mir_all):		
		select(trans_all+trans_mir_all)	


























def lz_dupCluster(trans=[],doPrint = 1):
	trans = lz_ls() if not trans else trans
	value_pair = {}
	trans_mir_all,trans_all,clu_mirs =[],[],['','']
	for tran in trans:
		po_index1,po_index2 = [],[]
		if not tran:
			continue
		if attributeQuery('worldMatrix',node = tran,ex=1):
			clu = listConnections('%s.worldMatrix[0]'%tran)
		elif attributeQuery('relative',node = tran,ex=1):	
				continue
		else:
			continue
		if not clu:
			if objExists('%s_hide'%tran):
				#lz_sub_CtlToClu
				tran = lz_sub_CtlToClu(tran)
				#tran = listConnections('%s_hide.t'%tran)[0]
				clu = listConnections('%s.worldMatrix[0]'%tran)
			else:
				continue
		if isinstance(clu,list):
			clu = clu[0]
		if objectType(clu) != 'cluster':
			continue
		count = getAttr('%s.weightList'%clu,s=1)

		select(tran)	
		EditMembershipTool()
		points = lz_ls()
		setToolTo('selectSuperContext')

		set_clu = 	 listConnections('%s.message'%clu)[0]
		obj_index = '0' 
		objs_plugs = listConnections('%s.dagSetMembers'%set_clu,p=1)
		poly = listConnections('%s.dagSetMembers'%set_clu)[-1]
		obj_shape = listRelatives(poly,s=1,pa=1)[0]
		obj_index =  lz_clu_findIndex(clu,poly)
		points_new = []
		if count==1:	
			lz_mirrorSelection_getIndex(po_index1,points)
		else:
			for s in points:
				if s.find(poly) !=-1:
					points_new.append(s)
			lz_mirrorSelection_getIndex(po_index1,points_new)	
			points = points_new

		select(points)
		#mir_points = lz_mirrorSelection(type=0,prec=4)
		#lz_mirrorSelection_getIndex(po_index2,mir_points)
		
		name_mir = tran.replace('l_','r_',1)
		if name_mir == tran:
			name_mir.replace('r_','l_',1)
		if name_mir == tran:
			name_mir = tran+'_mir'
		#if not mir_points:
		#	continue

		po_neg_index,po_neg = [],[]
		po_pos_index,po_pos = [],[]
		po_mid_index,po_mid = [],[]
		for index,item in enumerate(po_index1):
			vtx = xform('%s.vtx[%d]'%(poly,item),q=1,ws=1,t=1)
			if vtx[0]<0:
				po_neg_index.append(item)
				po_neg.append('%s.vtx[%d]'%(poly,item))
			if vtx[0]>0:
				po_pos_index.append(item)
				po_pos.append('%s.vtx[%d]'%(poly,item))
			if abs(vtx[0])<0.001:
				po_mid_index.append(item)
				po_mid.append('%s.vtx[%d]'%(poly,item))		

		trans,clu_pos, clu_neg =[],'',''
		mir_points,mir_points_index,mir_points_value = [],[],[]
		if po_mid:
			for index,item in enumerate(po_mid_index):
				va = getAttr('%s.weightList[%s].weights[%s]'%(clu,obj_index,item))
				mir_points.append('%s.vtx[%d]'%(poly,item))
				mir_points_value.append(va)
				mir_points_index.append(item)			
		if po_pos:
			select(po_pos)
			clu_pos = 	cluster(rel=1)[0]
	
			for index,item in enumerate(po_pos_index):
				va = getAttr('%s.weightList[%s].weights[%s]'%(clu,obj_index,item))
				try:
					setAttr('%s.weightList[0].weights[%s]'%(clu_pos,item),va)
				except:
					pass
			poly_dup = duplicate(poly,n=poly+'_dupCluPoly')[0]	
			poly_dup_shape = listRelatives(poly,s=1,pa=1)[0]
			vrt_len = getAttr('%s.vrts'%poly_dup_shape,s=True)
			cluJo_return = lz_cluToJo(trans=['%sHandle'%clu_pos],makeSkin = 1,otherPoly = 1,poly_dup = poly_dup )
			#[skin_new,base_jo,joints_all,poly_dup]
			joints_all= cluJo_return[2]
			jo_mir = lz_pre_simpleMirror(joints_all[0],sameParent= 1)
	
			skinCluster(cluJo_return[0],ai= jo_mir,lw = 1,e=1,wt=0) 
			setAttr('%s.liw'%jo_mir,0)
			#mirrorInverse = 1 if  po_neg else 0
			copySkinWeights( ss=cluJo_return[0], ds=cluJo_return[0], noMirror=0 ,mirrorMode='YZ',mirrorInverse= 0)
			for item in range(vrt_len):
				va = skinPercent(cluJo_return[0],'%s.vtx[%d]'%(poly_dup,item),q=1,v=1,t=jo_mir) 
				if va>0.02:
					mir_points.append('%s.vtx[%d]'%(poly,item))
					mir_points_value.append(va)
					mir_points_index.append(item)
			lz_delete([poly_dup,cluJo_return[1],jo_mir,clu_pos,joints_all[0]])
			
		if po_neg:
			select(po_neg)
			clu_neg = 	cluster(rel=1)[0]		
	
			for index,item in enumerate(po_neg_index):
				va = getAttr('%s.weightList[%s].weights[%s]'%(clu,obj_index,item))
				try:
					setAttr('%s.weightList[0].weights[%s]'%(clu_neg,item),va)
				except:
					pass		
			poly_dup = duplicate(poly,n=poly+'_dupCluPoly')[0]	
			poly_dup_shape = listRelatives(poly,s=1,pa=1)[0]	
			vrt_len = getAttr('%s.vrts'%poly_dup_shape,s=True)		
			cluJo_return = lz_cluToJo(trans=['%sHandle'%clu_neg],makeSkin = 1,otherPoly = 1,poly_dup = poly_dup )	
			joints_all= cluJo_return[2]
			jo_mir = lz_pre_simpleMirror(joints_all[0],sameParent= 1)
		
			skinCluster(cluJo_return[0],ai= jo_mir,lw = 1,e=1,wt=0) 
			setAttr('%s.liw'%jo_mir,0)
			#mirrorInverse = 1 if  po_neg else 0
			copySkinWeights( ss=cluJo_return[0], ds=cluJo_return[0], noMirror=0 ,mirrorMode='YZ',mirrorInverse= 1)
			for item in range(vrt_len):
				va = skinPercent(cluJo_return[0],'%s.vtx[%d]'%(poly_dup,item),q=1,v=1,t=jo_mir) 
				if va>0.02:
					mir_points.append('%s.vtx[%d]'%(poly,item))
					mir_points_value.append(va)
					mir_points_index.append(item)
			lz_delete([poly_dup,cluJo_return[1],jo_mir,joints_all[0],clu_neg])
		mir_index = '0'	
		clu_created = 0 
		if not objExists(name_mir):	
			trans_ex = xform(tran,q=1,ws=1,rp=1)
			trans_mir = [-trans_ex[0],trans_ex[1],trans_ex[2]]
			select(cl=1)
			clu_mirs = cluster(rel=1)
			setAttr('%sHandleShape.origin'%clu_mirs[0],trans_mir[0],trans_mir[1],trans_mir[2])
			lz_xform('%sHandle'%clu_mirs[0],trans_mir,1)
			select(mir_points)
			sets(fe='%sSet'%clu_mirs[0])
			clu_mir = rename(clu_mirs[0],name_mir+'Clu')
			
			clu_mirs[1] = rename(clu_mirs[1],name_mir)
			clu_created = 1
				
		if not clu_created:		
		
			clu_mirs[0] =  listConnections('%s.worldMatrix[0]'%name_mir)
			if not clu_mirs[0]:
				return 
			clu_mirs[0] = clu_mirs[0][0]
			
			clu_mir = clu_mirs[0]
			mir_set_clu = 	 listConnections('%s.message'%clu_mir)[0]
			points_new = []
			for s in mir_points:
				if s.find(poly) !=-1:
					points_new.append(s)
			current_points = []		
			mir_set_clu = 	 listConnections('%s.message'%clu_mir)[0]	
			objs_plugs_mir = listConnections('%s.dagSetMembers'%mir_set_clu,p=1)
			obj_shape_mir = listRelatives(poly,s=1,pa=1)[0]
			mir_index = lz_clu_findIndex(clu_mir,poly)
			select(name_mir)
			EditMembershipTool()					
			cu = lz_ls()
			for c in cu:
				if c.find(poly) !=-1:
					current_points.append(c)
			current_index = []		
			lz_mirrorSelection_getIndex(current_index,current_points)			
			if current_points:
				for index,item in enumerate(current_index):
					#va = getAttr('%s.weightList[0].weights[%s]'%(clu,item))
					try:
						setAttr('%s.weightList[%s].weights[%s]'%(clu_mir,mir_index,item),0)
					except:
						pass
			select(mir_points)

			select(points_new)
			sets(fe=mir_set_clu)
		mir_set_clu = 	 listConnections('%s.message'%clu_mir)[0]	
		objs_plugs_mir = listConnections('%s.dagSetMembers'%mir_set_clu,p=1)
		mir_index = lz_clu_findIndex(clu_mir,poly)

		
		trans_mir_all.append(name_mir)
		trans_all.append(tran)
		
		for index,item in enumerate(mir_points_index):
			#va = getAttr('%s.weightList[0].weights[%s]'%(clu,item))
			try:
				setAttr('%s.weightList[%s].weights[%s]'%(clu_mir,mir_index,item),mir_points_value[index])
			except:
				pass
		
		
		if doPrint:
			lz_print('对称完成！\\n')
		
	setToolTo('selectSuperContext')		
	if(trans_all+trans_mir_all):		
		select(trans_all+trans_mir_all)	
		





def lz_cluToclu(trans=[],poly_tar='',onlyNew = 0 ,doPrint = 1):
	sl = lz_ls()
	trans = sl[:-1] if not trans else trans
	poly_tar = sl[-1] if not poly_tar else poly_tar
	warn1 = [] 
	need_rename = 1
	tar_trans_all,new_tar = [],0
	if len(trans+[poly_tar])<2:
		lz_warning('先选择各种簇 最后加选模型！')
		return
	poly_shape = listRelatives(poly_tar,s=1,pa=1)[0]
	if objectType(poly_shape ) =='nurbsCurve' or objectType(poly_shape ) =='clusterHandle':
		need_rename = 0
		if len(sl)>2:
			lz_warning('一对一的簇复制: 请选择新簇 加选 原始簇。或者新簇 加选 原始次控。多簇+模型 形成多对多复制\\n')
			return			
		last_item = sl[-1] 
		clu_handle = last_item
		po_index1,points = [],[]
		if objectType(poly_shape ) =='nurbsCurve':
			clu_handle = lz_sub_CtlToClu(last_item)
		clu_obj = listConnections('%s.worldMatrix[0]'%clu_handle)[0]
		clu_set = listConnections('%s.message'%clu_obj)[0]
		poly_tar = listConnections('%s.dagSetMembers'%clu_set)[0]
		clu_dups=[clu_obj,clu_handle]
 
		select(clu_handle)	
		EditMembershipTool()
		points = lz_ls()
		setToolTo('selectSuperContext')
		lz_mirrorSelection_getIndex(po_index1,points)
		for index,item in enumerate(po_index1):
			setAttr('%s.weightList[0].weights[%s]'%(clu_obj,item),0)
		tar_trans_all = [last_item]	
	poly_shape = listRelatives(poly_tar,s=1,pa=1)[0]
	if objectType(poly_shape ) !='mesh':
		return
	
	sk_tar = lz_findCluster(poly_tar,type='skinCluster')
	jo_base,joints_all,jo_raw ='',[],''
	if not sk_tar:
		select(cl=1)
		new_tar  = 1
		jo_base = joint(n='tmp_base')
		sk_tar = skinCluster(jo_base,poly_tar)[0]
	poly_dup = ''
	for index,tran in enumerate(trans):
		if objectType(tran)!='transform':
			continue

		tran_shape = listRelatives(tran,s=1,pa=1)
		tran_raw = tran
		if objectType(tran_shape[0]) =='nurbsCurve':
			tran = lz_sub_CtlToClu(tran)
		clu_dups,clu = [],[]	
		vtx_all = []
		joint_return = lz_cluToJo([tran],makeSkin = 1,otherPoly=1,poly_dup= poly_dup)
		if not joint_return[0]:
			warn1.append(tran)
			tar_trans_all.append(tran)
			continue
		jo_new =  joint_return[2][0]
		joints_all.append(jo_new)
		poly_dup = joint_return[3]
		#if not index:
		#	jo_raw = 
		sk_from = joint_return[0]
		skinCluster(sk_tar,e=1,dr=4,ps=0,ns=10,lw=1,wt=0,ai=jo_new)	
		setAttr('%s.liw'%jo_new,0)
		copySkinWeights( ss=sk_from, ds=sk_tar, noMirror=True ,surfaceAssociation='closestPoint',influenceAssociation='closestJoint')
		lz_weight(points=[],infName =jo_new,poly=poly_tar,ap=0,value=0)
		po_dups = []
		new_points = lz_ls()
		lz_mirrorSelection_getIndex(po_dups,new_points)

		trans_ex = xform(tran,q=1,ws=1,rp=1)
		trans_dup = [trans_ex[0],trans_ex[1],trans_ex[2]]
		if not clu_dups:
			select(cl=1)
			clu_dups = cluster(rel=1)
			setAttr('%sHandleShape.origin'%clu_dups[0],trans_dup[0],trans_dup[1],trans_dup[2])
			lz_xform('%sHandle'%clu_dups[0],trans_dup,1)
		clu = listConnections('%s.worldMatrix[0]'%tran)
		if new_points!=['']:
			set_clu =listConnections('%s.message'%clu_dups[0])[0]
			select(new_points)
			sets(fe=set_clu)
			#clu_mir = rename(clu_dups[0],name_mir+'Clu')
	
			obj_index = '0'
			objs_plugs = listConnections('%s.dagSetMembers'%set_clu,p=1)
			#obj_shape = poly_shape
			for p in objs_plugs:
				if p.find(poly_shape+'.') == 0:
					p_index_str = listConnections(p,p=1)[0]
					
					p_split = p_index_str.split('[')[1]
					obj_index = p_split.split(']')[0]
			for index,item in enumerate(po_dups):
				va = skinPercent(sk_tar,'%s.vtx[%d]'%(poly_tar,item),q=1,v=1,t=jo_new)
				vtx_all.append('%s.vtx[%d]'%(poly_tar,item))
				setAttr('%s.weightList[%s].weights[%s]'%(clu_dups[0],obj_index,item),va)
			select(clu_dups[1])
			
			if joint_return[1]:
				skinPercent(sk_tar,vtx_all,tv=(jo_new,0))
				
		if joint_return[1]:		
			delete(sk_from,joint_return[1],jo_new)
		clu_new,clu_dup,tran_new,tran_dup = '','','',''
		if need_rename and not onlyNew:
			if clu[0].find(':') == -1:
				if clu[0].find('old')==-1:
					clu_new = rename(clu[0],clu[0]+'_old')
					tran_new = rename(tran,tran+'_old')
					clu_dup = rename(clu_dups[0],clu[0])
					tran_dup = rename(clu_dups[1],tran)
				else:
					name_clu = clu[0].split('_old')[0]
					name_tran = tran.split('_old')[0]
					clu_new,tran_new = clu[0],tran
					clu_dup =  rename(clu_dups[0],name_clu)
					tran_dup =  rename(clu_dups[1],name_tran)
					
			else:
				clu_new = clu[0]
				tran_new = tran
				clu_noPre = clu[0].split(':')[1]
				tran_noPre = tran.split(':')[1]
				if objExists(tran_noPre):
					if objExists(tran_noPre+'_old'):
						lz_delete([tran_noPre+'_old'])
					clu_new = rename(clu_noPre,clu_noPre+'_old')
					tran_new = rename(tran_noPre,tran_noPre+'_old')
					clu_dup = rename(clu_dups[0],clu_noPre)
					tran_dup =  rename(clu_dups[1],tran_noPre)
				else:
					clu_dup = rename(clu_dups[0],clu_noPre)
					tran_dup =  rename(clu_dups[1],tran_noPre)
			if objectType(tran_shape[0]) =='nurbsCurve':
				tar_trans_all.append(tran_raw)
			else:
				tar_trans_all.append(tran_dup)	

				
			tar = ''
			tar_temp = listConnections('%s.t'%tran_new)
			tar_const = listConnections('%s.rotateOrder'%tran_new)
			if tar_temp:
				tar = tar_temp[0]
			name_pa = listRelatives(tran_new,p=1,pa=1)
			if name_pa:
				parent(tran_dup,name_pa)
			if tar:
				lz_connectAttr('%s.t'%tar,'%s.t'%tran_dup)
				lz_connectAttr('%s.r'%tar,'%s.r'%tran_dup)
				lz_connectAttr('%s.s'%tar,'%s.s'%tran_dup)
			if tar_const and not tar_temp:
				tar_ctl = listConnections('%s.target[0].targetScale'%tar_const[0])[0]
				parentConstraint(tar_ctl,tran_dup,mo=1)
				scaleConstraint(tar_ctl,tran_dup,mo=1)	
		if need_rename and onlyNew:

			clu_dup = rename(clu_dups[0],clu[0]+'#')
			tran_dup = rename(clu_dups[1],tran+'#')			
			if objectType(tran_shape[0]) =='nurbsCurve':
				tar_trans_all.append(tran_raw)
			else:
				tar_trans_all.append(tran_dup)	
			tar = ''
			tar_temp = listConnections('%s.t'%tran)
			tar_const = listConnections('%s.rotateOrder'%tran)
			if tar_temp:
				tar = tar_temp[0]
			name_pa = listRelatives(tran,p=1,pa=1)
			if name_pa:
				parent(tran_dup,name_pa)
			if tar:
				lz_connectAttr('%s.t'%tar,'%s.t'%tran_dup)
				lz_connectAttr('%s.r'%tar,'%s.r'%tran_dup)
				lz_connectAttr('%s.s'%tar,'%s.s'%tran_dup)
			if tar_const:
				tar_ctl = listConnections('%s.target[0].targetScale'%tar_const[0])[0]
				parentConstraint(tar_ctl,tran_dup,mo=1)
				scaleConstraint(tar_ctl,tran_dup,mo=1)				
		
	if new_tar:
		delete(sk_tar,jo_base)	
	lz_delete(poly_dup)
	select(tar_trans_all)
	if doPrint:
		lz_print('簇克隆完成\\n')
		if warn1:
			lz_warning('存在簇影响了多个模型 %s 该簇不能复制！\\n'%(str(warn1)))
			select(sl)
			select(sl)



global lz_cluster_datas
lz_cluster_datas = {}

def lz_setCluster_cmd(name,cmd):
	global lz_cluster_datas
	lz_cluster_datas[name] = cmd
def lz_execCluster_cmd():
	global lz_cluster_datas
	name = textScrollList('clusterInflList',q=1,si=1)
	if name:
		mm.eval("artSetToolAndSelectAttr artAttrCtx %s"%lz_cluster_datas[name[0]])
