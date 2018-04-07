# coding=utf-8


# p=mb文件路径，j=工程目录，o=o盘工程路径，op=本地文件不在工程目录的，指定o盘特定文件夹 ,id是数据库的id
def k_eMayaPath(k_id):

	import re
	k_python_sp = '//ftdyproject/digital/film_project/hq_tool/programs/python_site-packages'

	if not k_python_sp in sys.path:
	    sys.path.append(k_python_sp)
	import datetime
	from bson.objectid import ObjectId
	import pymongo

    import socket
    checkIP=('127.0.0.1',998)
    ksocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ksocket.connect(checkIP)


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
	op = o+'/ftbox_otherfile'

	#数据内容
	data = kpost.find({"_id":ObjectId(k_id)},{'Nodedate':1})

	#创建临时文件夹路径
	p_dir =os.path.dirname(p)
	p_basename =os.path.basename(p)
	p_savedir = p_dir+'/temp'



	kexp =r'(^O:/|^o:/)(.*)'
	kexpb=r'(^%s)(.*)' %(j)

	#k_eNodedate2=['kYeticache','kabcmeshfiles','kassfiles','kaiTex','kassfiles','kcacheFiles','kmayaTex_default','kmrcacheFiles','kshave_cache',]
	k_except2 = ['kmayaTex_userTex','kYetitex']

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

		elif plug == 'kcacheFiles':
			pass		
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
							print node+port,opath
						else:
							cc.setAttr(node+port,op,type='string')

			print 'out'
	print 'ok'

	#创建临时文件夹
	if not os.path.exists(p_savedir):
		os.makedirs(p_savedir)

	tempfile=p_savedir+'/'p_basename

	#修改文件名 并 保存
	cc.file(rename=tempfile)
	cc.file(f=1,op="v=0;",typ="mayaBinary",save=True)

	ksocket.send('saved')
