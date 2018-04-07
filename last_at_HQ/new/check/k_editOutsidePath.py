# coding=utf-8
import re
import sys
import os
import time
path='D:/ziliao/201707/python_site-packages'
if not path in sys.path:
	sys.path.append(path)

from bson.objectid import ObjectId
import pymongo
client=pymongo.MongoClient('10.99.40.10',27017)
db = client['k_text']
kpost = db['check']


class k_editPath():
	def __init__(self):
		self.kupdate={}

	def k_checkPath(self):
		_id = "599653a7ebb2dd5da8a4f4d6"
		j = 'E:/work/7_0314_wenti'
		o = 'D:/work/7_0314_wenti'
		op = 'D:/work/7_0314_wenti/other'

		kexp =r'(^O:/|^o:/)(.*)'
		kexpb=r'(^%s)(.*)' %(j)

		

		#根据数据库 找到outsidefile的内容
		getfile = kpost.find({"_id":ObjectId(_id)},{"outsidefile":1})
		outsidefile = getfile[0]['outsidefile']



		for plug in outsidefile:

			if outsidefile[plug]:
				for knode in outsidefile[plug]:
					#print knode
					self.kname = knode[0]
					self.ksize = knode[1]
					self.ktime = knode[2]

					if not re.search(kexp,self.kname):
						if re.search(kexpb,self.kname):
							oname = self.kname.replace(j,o)

							self.kmatch(plug,oname,self.kname)

						else:
							kname_name=os.path.basename(self.kname)

							oname = op+'/'+kname_name

							self.kmatch(plug,oname,self.kname)

	def kmatch(self,plug,oname,kname):

		if os.path.exists(oname):
			osize = os.path.getsize(oname)
			otime  = time.localtime(os.stat(oname).st_mtime)
			otimeg = time.strftime("%Y-%m-%d %H:%M:%S",otime)
			#print osize,otimeg
			if not self.ksize==osize or not self.ktime==otime:

				if self.kupdate.has_key(plug):
					self.kupdate[plug].append([oname,kname])
				else:self.kupdate.update({plug:[[oname,kname]]})


		else:	
			if self.kupdate.has_key(plug):
				self.kupdate[plug].append([oname,kname])
			else:self.kupdate.update({plug:[[oname,kname]]})


if __name__ == "__main__":
	k_editPath()
	a=k_editPath()
	a.k_checkPath()
	a.kupdate

