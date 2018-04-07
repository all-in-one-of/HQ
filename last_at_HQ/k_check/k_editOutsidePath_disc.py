# coding=utf-8
import re
import sys
import os
import time
#python模块地址
path='//ftdyproject/digital/film_project/hq_tool/programs/python_site-packages'
if not path in sys.path:
	sys.path.append(path)
#链接数据库
from bson.objectid import ObjectId
import pymongo
client=pymongo.MongoClient('10.99.40.10',27017)
db = client['hqft_film']
kpost = db['check']


class k_editPath():
	def __init__(self,j,o,op,oimage,data):
		self.data = data
		self.j = j
		self.o = o
		self.op= op
		self.oimage= oimage
		self.kupdate={}

	def k_checkPath(self):
		#匹配数据  O盘路径开头的匹配  本地工程目录开头的匹配
		kexp =r'(^O:/|^o:/)(.*)'
		kexpb=r'(^%s)(.*)' %(self.j)

		outsidefile = self.data

		for plug in outsidefile:
			if outsidefile[plug] and plug!='Texture':
				for knode in outsidefile[plug]:
					#提取出文件的路径名字，大小，修改时间
					self.kname = knode[0]
					self.ksize = knode[1]
					self.ktime = knode[2]

					#如果匹配为 非o盘文件
					if not re.search(kexp,self.kname):
						#如果匹配为 本地工程目录内的文件，替换本地工程目录路径 为 o盘工程目录路径
						if re.search(kexpb,self.kname):
							oname = self.kname.replace(self.j,self.o)
							#匹配o盘有无 重复或相同的 文件
							self.kmatch(plug,oname,self.kname)
						#如果 非本地工程目录内，将文件上传至 op路径
						else:
							kname_name=os.path.basename(self.kname)

							oname = self.op+'/'+kname_name
							#匹配o盘有无 重复或相同的 文件
							self.kmatch(plug,oname,self.kname)

			elif outsidefile[plug] and plug=='Texture':
				for knode in outsidefile[plug]:
					#提取出文件的路径名字，大小，修改时间
					self.kname = knode[0]
					self.ksize = knode[1]
					self.ktime = knode[2]

					#如果匹配为 非o盘文件
					if not re.search(kexp,self.kname):
						#如果匹配为 本地工程目录内的文件，替换本地工程目录路径 为 o盘工程目录路径
						if re.search(kexpb,self.kname):
							oname = self.kname.replace(self.j,self.o)
							#匹配o盘有无 重复或相同的 文件
							self.kmatch(plug,oname,self.kname)
						#如果 非本地工程目录内，将文件上传至 op路径
						else:
							kname_name=os.path.basename(self.kname)

							oname = self.oimage+'/'+kname_name
							#匹配o盘有无 重复或相同的 文件
							self.kmatch(plug,oname,self.kname)


	def kmatch(self,plug,oname,kname):
		#获取o盘文件大小，修改时间
		if os.path.exists(oname):
			osize = os.path.getsize(oname)
			#otime  = time.localtime(os.stat(oname).st_mtime)
			#otimeg = time.strftime("%Y-%m-%d %H:%M:%S",otime)
			#print osize,otimeg
			#本地文件与o盘匹配
			if not self.ksize==osize:
				if self.kupdate.has_key(plug):
					self.kupdate[plug].append([kname,oname])
				else:self.kupdate.update({plug:[[kname,oname]]})

		else:	
			if self.kupdate.has_key(plug):
				self.kupdate[plug].append([kname,oname])
			else:self.kupdate.update({plug:[[kname,oname]]})


if __name__ == "__main__":
	k_editPath()
	a=k_editPath()
	a.k_checkPath()
	a.kupdate

