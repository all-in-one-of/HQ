# coding=utf-8
import re
import sys
import os
import time

path='//ftdyproject/digital/film_project/hq_tool/programs/python_site-packages'
if not path in sys.path:
	sys.path.append(path)
from bson.objectid import ObjectId
import pymongo
client=pymongo.MongoClient('10.99.40.10',27017)
db = client['hqft_film']
kpost = db['check']


class k_editPath():
	def __init__(self,j,o,op,data):
		self.data = data
		self.j = j
		self.o = o
		self.op= op
		self.kupdate={}

	def k_checkPath(self):
		kexp =r'(^O:/|^o:/)(.*)'
		kexpb=r'(^%s)(.*)' %(self.j)

		outsidefile = self.data

		for plug in outsidefile:
			if outsidefile[plug]:
				for knode in outsidefile[plug]:
					self.kname = knode[0]
					self.ksize = knode[1]
					self.ktime = knode[2]

					if not re.search(kexp,self.kname):
						if re.search(kexpb,self.kname):
							oname = self.kname.replace(self.j,self.o)
							self.kmatch(plug,oname,self.kname)
						else:
							kname_name=os.path.basename(self.kname)
							oname = self.op+'/'+kname_name
							self.kmatch(plug,oname,self.kname)

	def kmatch(self,plug,oname,kname):
		if os.path.exists(oname):
			osize = os.path.getsize(oname)
			otime  = time.localtime(os.stat(oname).st_mtime)
			otimeg = time.strftime("%Y-%m-%d %H:%M:%S",otime)
			if not self.ksize==osize or not self.ktime==otime:
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

