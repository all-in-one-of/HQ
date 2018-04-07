# coding=utf-8
import re


# p=mb文件路径，j=工程目录，o=o盘工程路径，op=本地文件不在工程目录的，指定o盘特定文件夹
def k_editOutsidefiles(j,o,op,data):

	kexp =r'(^O:/|^o:/)(.*)'
	kexpb=r'(^%s)(.*)' %(j)

	if data['kYeticache']:
		for node in data['kYeticache']:
			path = data['kYeticache'][node][0]['path']
			port = data['kYeticache'][node][0]['port']

			if not re.search(kexp,path):
				if re.search(kexpb,path):
					print path
					opath = path.replace(j,o)
					cc.setAttr(node+port,opath,type='string')
				else:
					cc.setAttr(node+port,op,type='string')


	if data['kYetitex']:
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
