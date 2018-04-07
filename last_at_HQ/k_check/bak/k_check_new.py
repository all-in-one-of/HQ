# coding=utf-8
import sys
#python模块路径
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

#p=maya文件路径，j=maya工程文件路径，o=网络工程地址，s=maya脚本内容
def k_check(p,j,o,s):
	#maya脚本地址
	k_fantabox  = '//10.99.1.13/hq_tool/Maya/hq_maya/scripts'
	k_json      = k_fantabox+'/fantabox'

	o = o+'/'
	#特殊文件夹路径
	op = o+'ftbox_otherfile'
	#联接mongoDB
	client=pymongo.MongoClient('10.99.40.10',27017)
	db = client['hqft_film']
	kpost = db['check']
	#联接TCP
	checkIP=('127.0.0.1',998)
	ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ksocket.connect(checkIP)
	#插件模块地址
	if not k_fantabox in sys.path:
		sys.path.append(k_fantabox)
	#不reload不行
	reload(sys)
	sys.setdefaultencoding('gbk')  
	#import maya脚本模块
	import fantabox  

	#解析json文件
	k_enablefiles=ss.loads(open(r'%s/FantaBox_mayacheck.json' %k_json).read(),encoding='gbk')
	k_enables=ss.loads(s,encoding='gbk') 
	#maya后台打开文件      
	cc.file(p,f=1,op="v=0;",esn=0,ignoreVersion=1,typ="mayaBinary",o=1)
	#maya设置工程目录
	mm.eval('setProject "%s";'%j) 

	#定义威猛先生检查出来的内容
	k_Treturn={}

	#设置 进度条
	k_enablesize=0
	for i in k_enables.keys():
		if k_enables[i][0]:
			k_enablesize+=1

	kpercent=100./k_enablesize

	kprogres=0

	#执行具体脚本
	for k_enable in k_enables:
		if k_enables[k_enable][0]:
			kType=1
			k_split = k_enable.split('.')
			k_mod=k_split[0]
			k_py =k_split[1]
			k_return='fantabox.%s()' %k_enable
			#特殊模块需要给参数 参数为模块的数字代码
			k_return2='fantabox.%s(%d)' %(k_enable,-1)
			try:
			    k_returna=eval(k_return)
			except:
			    k_returna=eval(k_return2)
			#如果检查出有问题 type改变为不通过状态
			if k_returna:
			    kType=2
			#k_update={k_enable:k_returna}


			k_update={k_enablefiles[k_mod][k_py][0]:k_returna}
			k_Treturn.update(k_update)

			kprogres=kprogres+kpercent
			if kprogres >= 99.9:
			    kprogres=100
		    #发送进度条数值 及 检查通过状态
			ksend={kprogres:kType}
			#包装成json
			ksend=ss.dumps(ksend)
			#TCP发送
			ksocket.send(ksend)
			#接收回应
			kreply=ksocket.recv(1024)
			#time.sleep(.1)


	#k_outputs=ss.dumps(k_Treturn)
	#执行 检查maya外部文件 脚本
	import k_checkOutSideFile
	check_outsidefile=k_checkOutSideFile.k_cachefinder()
	outsidefile=check_outsidefile.k_checkit()
	kNodedate = check_outsidefile.kNodedate

	#执行 修改外部文件路径 脚本 （本地匹配o盘）
	import k_editOutsidePath
	k_updata = k_editOutsidePath.k_editPath(j,o,op,outsidefile)
	k_updata.k_checkPath()
	k_pathUpdate = k_updata.kupdate

	#调取maya文件内用到的插件版本
	mayaplugin_version=check_outsidefile.mayaplugin_version

	#上传数据到数据库
	check_post={u"检查人":"k",u"上传时间":datetime.datetime.now(),"maya_check":k_Treturn,"Nodedate":kNodedate,"outsidefile":outsidefile,"update":k_pathUpdate,u'插件版本':mayaplugin_version,'mayaPath':p,'mayaProject':j,'Opath':o}
	kpost_id=kpost.insert(check_post)
	#print kpost_id
	#发送数据库 新增表格的id
	ksend={"_id":str(kpost_id)}
	ksend=ss.dumps(ksend)
	ksocket.send(ksend)
	ksocket.close()

# p=mb文件路径，j=工程目录，o=o盘工程路径，op=本地文件不在工程目录的，指定o盘特定文件夹 ,id是数据库的id
def k_eMayaPath(k_id):
	#k_python_sp = '//ftdyproject/digital/film_project/hq_tool/programs/python_site-packages'

	#if not k_python_sp in sys.path:
		#sys.path.append(k_python_sp)
	#import datetime
	#from bson.objectid import ObjectId
	#import pymongo
	#联接TCP
	checkIP=('127.0.0.1',998)
	ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ksocket.connect(checkIP)

	#联接数据库
	client=pymongo.MongoClient('10.99.40.10',27017)
	db = client['hqft_film']
	kpost = db['check']

	#文件路径
	p= kpost.find({"_id":ObjectId(k_id)},{'mayaPath':1})
	for p in p:
		p=p['mayaPath']

	#工程路径
	j= kpost.find({"_id":ObjectId(k_id)},{'mayaProject':1})
	for j in j:
		j=j['mayaProject']

	#目标路径
	o= kpost.find({"_id":ObjectId(k_id)},{'Opath':1})
	for o in o:
		o=o['Opath']

	#目标特殊文件夹路径
	op = o+'ftbox_otherfile'

	#数据内容
	data = kpost.find({"_id":ObjectId(k_id)},{'Nodedate':1})

	for data in data:
		data=data['Nodedate']


	#创建临时上传文件夹路径
	p_dir =os.path.dirname(p)
	p_basename =os.path.basename(p)
	p_savedir = p_dir+'/ft_update'


	#匹配数据  O盘路径开头的匹配  本地工程目录开头的匹配
	kexp =r'(^O:/|^o:/)(.*)'
	kexpb=r'(^%s)(.*)' %(j)

	#k_eNodedate2=['kYeticache','kabcmeshfiles','kassfiles','kaiTex','kassfiles','kcacheFiles','kmayaTex_default','kmrcacheFiles','kshave_cache',]
	
	#k_except2 = ['kmayaTex_userTex','kYetitex']

	#执行 修改maya节点路径内容
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
							cc.pgYetiGraph(nodes,node=port,param='file_name',setParamValueString=op)

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
							cc.setAttr(nodes+port,op,type='string')

		#elif plug == 'kcacheFiles':
			#pass	

		else:
			if data[plug]:
				print plug
				for node in data[plug]:
					path = data[plug][node][0]['path']
					port = data[plug][node][0]['port']

					if not re.search(kexp,path):
						if re.search(kexpb,path):
							#print path
							opath = path.replace(j,o)
							cc.setAttr(node+port,opath,type='string')
							#print node+port,opath
						else:
							cc.setAttr(node+port,op,type='string')

			#print 'out'
	#print 'ok'

	#创建临时文件夹
	if not os.path.exists(p_savedir):
		os.makedirs(p_savedir)

	tempfile=p_savedir+'/'+p_basename

	#修改文件名 并 保存
	cc.file(rename=tempfile)
	cc.file(f=1,op="v=0;",typ="mayaBinary",save=True)

	#保存maya文件后 发送TCP信号 
	ksocket.send('saved')

'''    for k_Treturns in k_Treturn:
        if k_Treturn[k_Treturns]:
            print ('---------'+k_enablefiles[k_Treturns][2]+'--------------')
            for k_Treturnss in k_Treturn[k_Treturns]:
                print (k_Treturnss) '''





