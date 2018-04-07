# coding=utf-8
import sys
k_python_sp = '//ftdyproject/digital/film_project/hq_tool/programs/python_site-packages'
if not k_python_sp in sys.path:
	sys.path.append(k_python_sp)
import json as ss
import maya.cmds as cc
import maya.mel as mm
import os    
import time
import datetime
import pymongo
import socket
import re
from bson.objectid import ObjectId


def k_check(p,j,o,n,r,s):
	k_fantabox  = '//10.99.1.13/hq_tool/Maya/hq_maya/scripts'
	k_json      = k_fantabox+'/fantabox'
	departments=['CAM','LAY','CHR','MOD','MOD_rig','ANI','RIG','RIG_clu','RIG_moc','FX','FX_ani','REN']
	n=int(n)
	if not o[-1]=='/':
		o = o+'/'

	client=pymongo.MongoClient('10.99.40.240',27017)
	db = client['hqft_film']
	kpost = db['check']
	checkIP=('127.0.0.1',998)
	ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ksocket.connect(checkIP)
	if not k_fantabox in sys.path:
		sys.path.append(k_fantabox)
	reload(sys)
	sys.setdefaultencoding('gbk')  
	import fantabox  

	k_enablefiles=ss.loads(open(r'%s/FantaBox_mayacheck_ftp.json' %k_json).read(),encoding='gbk')
	k_enables=ss.loads(s,encoding='gbk')   
	cc.file(p,f=1,op="v=0;",esn=0,ignoreVersion=1,typ="mayaBinary",o=1)


	kproj = j
	if kproj[-1]=='/':
		kproj = os.path.dirname(kproj)

	mm.eval('setProject "%s";'%kproj) 

	k_mayaname=os.path.basename(p)

	k_customname=[]

	for department in departments:
		if ('_'+department+'_') in k_mayaname:
			k_customname = k_mayaname.split('_'+department+'_')[-1]
			k_customname=os.path.splitext(k_customname)[0]


	oimage = o+'sourceimages/'+k_customname

	op = o+'ftbox_otherfile/'+k_customname

	k_Treturn={}

	k_enablesize=0
	for i in k_enables.keys():
		if k_enables[i][0]:
			k_enablesize+=1

	kpercent=100./k_enablesize

	kprogres=0

	for k_enable in k_enables:
		if k_enables[k_enable][0]:
			kType=1
			k_split = k_enable.split('.')
			k_mod=k_split[0]
			k_py =k_split[1]
			k_return='fantabox.%s()' %k_enable
			k_return2='fantabox.%s(%d)' %(k_enable,n)
			try:
				k_returna=eval(k_return2)
			except:
				k_returna=eval(k_return)
			if k_returna:
				kType=2
				modzw=k_enablefiles[k_mod][k_py][0]
				print '***  '+modzw.encode('utf-8')+'  *** 检查不通过'

			k_update={k_enablefiles[k_mod][k_py][0]:k_returna}
			k_Treturn.update(k_update)

			kprogres=kprogres+kpercent
			if kprogres >= 99.9:
				kprogres=100

			ksend={kprogres:kType}
			ksend=ss.dumps(ksend)
			ksocket.send(ksend)
			kreply=ksocket.recv(1024)


	import k_checkOutSideFile
	check_outsidefile=k_checkOutSideFile.k_cachefinder()
	outsidefile=check_outsidefile.k_checkit()
	kNodedate = check_outsidefile.kNodedate

	import k_editOutsidePath
	k_updata = k_editOutsidePath.k_editPath(j,o,op,oimage,outsidefile)
	k_updata.k_checkPath()
	k_pathUpdate = k_updata.kupdate

	mayaplugin_version=check_outsidefile.mayaplugin_version

	check_post={u"检查人":r,u"上传时间":datetime.datetime.now(),"maya_check":k_Treturn,"Nodedate":kNodedate,"outsidefile":outsidefile,"update":k_pathUpdate,u'插件版本':mayaplugin_version,'mayaPath':p,'mayaProject':j,'Opath':o,'customname':k_customname}
	kpost_id=kpost.insert(check_post)
	ksend={"_id":str(kpost_id)}
	ksend=ss.dumps(ksend)
	ksocket.send(ksend)
	ksocket.close()

def k_eMayaPath(k_id):
	checkIP=('127.0.0.1',998)
	ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ksocket.connect(checkIP)

	client=pymongo.MongoClient('10.99.40.240',27017)
	db = client['hqft_film']
	kpost = db['check']

	p= kpost.find({"_id":ObjectId(k_id)},{'mayaPath':1})
	for p in p:
		p=p['mayaPath']

	j= kpost.find({"_id":ObjectId(k_id)},{'mayaProject':1})
	for j in j:
		j=j['mayaProject']

	o= kpost.find({"_id":ObjectId(k_id)},{'Opath':1})
	for o in o:
		o=o['Opath']

	k_customname=kpost.find({"_id":ObjectId(k_id)},{'customname':1})
	for k_customname in k_customname:
		k_customname=k_customname['customname']

	op = o+'ftbox_otherfile/'+k_customname
	oimage = o+'sourceimages/'+k_customname

	data = kpost.find({"_id":ObjectId(k_id)},{'Nodedate':1})

	for data in data:
		data=data['Nodedate']

	p_dir =os.path.dirname(p)
	p_basename =os.path.basename(p)
	p_savedir = p_dir+'/ftp_updata'

	kexp =r'(^O:/|^o:/)(.*)'
	kexpb=r'(^%s)(.*)' %(j)

	for plug in data:
		if plug == 'kYetitex' and data['kYetitex']:
			for nodes in data['kYetitex']:
				for node in data['kYetitex'][nodes]:
					path = node['path']
					port = node['port']
					fileMode = node['fileMode']

					if not fileMode and not re.search(kexp,path):
						if re.search(kexpb,path):
							opath = path.replace(j,o)
							cc.pgYetiGraph(nodes,node=port,param='file_name',setParamValueString=opath)
						else:
							path_name =os.path.basename(path)
							oppath = oimage+'/'+path_name
							cc.pgYetiGraph(nodes,node=port,param='file_name',setParamValueString=oppath)

		elif plug == 'kmayaTex_userTex' and  data['kmayaTex_userTex']:
			for nodes in data['kmayaTex_userTex']:
				for node in data['kmayaTex_userTex'][nodes]:
					path = node['path']
					port = node['port']

					if not re.search(kexp,path):
						if re.search(kexpb,path):
							opath = path.replace(j,o)
							cc.setAttr(nodes+port,opath,type='string')
						else:
							path_name =os.path.basename(path)
							oppath = oimage+'/'+path_name
							cc.setAttr(nodes+port,oppath,type='string')


		elif plug=='kaiTex' or plug=='kmayaTex_default':
			for node in data[plug]:
				path = data[plug][node][0]['path']
				port = data[plug][node][0]['port']

				if not re.search(kexp,path):
					if re.search(kexpb,path):
						opath = path.replace(j,o)
						cc.setAttr(node+port,opath,type='string')
					else:
						path_name =os.path.basename(path)
						oppath = oimage+'/'+path_name
						cc.setAttr(node+port,oppath,type='string')



		else:
			if data[plug]:
				for node in data[plug]:
					path = data[plug][node][0]['path']
					port = data[plug][node][0]['port']

					if not re.search(kexp,path):
						if re.search(kexpb,path):
							opath = path.replace(j,o)
							cc.setAttr(node+port,opath,type='string')
						else:
							path_name =os.path.basename(path)
							oppath = op+'/'+path_name
							cc.setAttr(node+port,oppath,type='string')


	if not os.path.exists(p_savedir):
		os.makedirs(p_savedir)

	tempfile=p_savedir+'/'+p_basename

	cc.file(rename=tempfile)
	cc.file(f=1,op="v=0;",typ="mayaBinary",save=True)
	cc.file(f=1,new=1)

	ksocket.send('saved')





