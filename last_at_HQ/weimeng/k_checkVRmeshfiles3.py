import maya.cmds as cc
import os
import re

class k_cachefinder():
	#阿诺德缓存的数组
	kassfiles=[]
	#有问题阿诺德节点
	kerror_arnold=[]
	projectDir = cc.workspace(query=True,rootDirectory=True)    

	def __init__(self):
	    #self.k_checkVRmeshfiles()
	    #self.k_checkabcfiles()
	    self.k_checkassfiles()

	def k_checkVRmeshfiles(self):
		#kwp = cc.workspace(q =True, rootDirectory=True)
		kvrmeshfiles=[]
		kvrmeshs=cc.ls(type='VRayMesh')
		for kvrmesh in kvrmeshs:
			krvrmesh=cc.listConnections((kvrmesh+'.output'),s=0,d=1)
			if krvrmesh:
				vrmesh=cc.getAttr(kvrmesh+'.fileName')
				if not vrmesh in kvrmeshfiles:
					if os.path.exists(vrmesh):
						kvrmeshfiles.append(vrmesh)


	def k_checkabcfiles(self):
		kabcmeshfiles=[]
		kabcmeshs=cc.ls(type='AlembicNode')
		for kabcmesh in kabcmeshs:
			krabcmesh=cc.listConnections((kabcmesh+'.outPolyMesh'),s=0,d=1)
			kcabcmesh=cc.listConnections((kabcmesh+'.transOp'),s=0,d=1)
			if krabcmesh or kcabcmesh:
				abcmesh=cc.getAttr(kabcmesh+'.abc_File')
				if not abcmesh in kabcmeshfiles:
					if os.path.exists(abcmesh):
						kabcmeshfiles.append(abcmesh)	



	def k_checkassfiles(self):
		#总缓存文件
		#maya节点返回的路径
		kassdso=[]
		#记录文件夹内里的文件，避免重复对网络进行获取
		kassfilepath={}

		self.kexpo  = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'
		self.kexpo2 = r'(.*?)([\._])([0-9#]*)([\.]?)([0-9#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'

		kassmeshs=cc.ls(type='aiStandIn')
		for kassmesh in kassmeshs:
			krassmesh=cc.listConnections(kassmesh,s=0,d=1)
			#kcassmesh=cc.listConnections((kassmesh+'.transOp'),s=0,d=1)
			if krassmesh:
				#print 'kassmesh  '+str(kassmesh)
				assdso=cc.getAttr(kassmesh+'.dso')
				#获取 缓存名 与 路径
				assmesh_getpath=os.path.basename(assdso)
				#print 'assdso  '+str(assdso)
				assmeshpath=os.path.dirname(assdso)
				#print 'assmeshpath  '+str(assmeshpath)

				if not assdso in kassdso:
					kassdso.append(assdso)

					if assmeshpath in kassfilepath:
						#k_filterseq=[]
						#asspathfiles=os.listdir(assmeshpath)
						asspathfiles=kassfilepath[assmeshpath]
						#print 'asspathfiles  '+str(asspathfiles)
						krseqfile=self.k_filterassfile(assdso,asspathfiles,kassmesh)
						#self.kassfiles.append(krseqfile)
					else:
						#k_filterseq=[]
						#判断是否能根据文件夹 返回 文件夹里面的所有文件
						try:
							asspathfiles=os.listdir(assmeshpath)
						except WindowsError:
							try:
								asspathfiles=os.listdir(self.projectDir+assmeshpath)
							except WindowsError,e:
								#print e.message
								pass

						#print 'asspathfiles  '+str(asspathfiles)
						krseqfile=self.k_filterassfile(assdso,asspathfiles,kassmesh)
						#self.kassfiles.append(krseqfile)

						k_update={assmeshpath:asspathfiles}
						kassfilepath.update(k_update)
						
								#print 'kseq  '+str(kseq)
								#

		for x in self.kassfiles:
			print x

		print self.kassfiles
		#print kassfilepath


	#执行过滤判断    assdso=节点返回的数据   asspathfiles=文件夹下的所有文件  kassmesh=maya节点名字
	def k_filterassfile(self,assdso,asspathfiles,kassmesh):
		#根据节点返回的数据 获取文件名字 与 路径
		assmesh_getpath=os.path.basename(assdso)
		assmeshpath=os.path.dirname(assdso)

		#print assdso
		for asspathfile in asspathfiles:
			#找出井号
			#print 'asspathfile____  '+str(asspathfile)			
			pattern = re.search(self.kexpo, assmesh_getpath)
			#pattern2 = re.search(self.kexpo2, assmesh_getpath)

			if pattern:
				# 找出####
				#print pattern.groups()
				kwellnum=pattern.group(3)
				#print 'kwellnum  '+str(kwellnum)
				k_NO=len(kwellnum)
				kexpc = r'%s%s([0-9]{%d})([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$' %(pattern.group(1),pattern.group(2),k_NO)
				pattern = re.search(kexpc, asspathfile)
				if pattern:
					kseq=pattern.group()
					#k_filterseq.append(kseq)
					kseqfile=assmeshpath+'/'+kseq
					if not kseqfile in self.kassfiles:
						if os.path.exists(kseqfile):
							self.kassfiles.append(kseqfile)
							#return kseqfile
							#print kseqfile
							print '1'


			else:
				#判断节点返回的数据 是否在 总的缓存数组里存在
				kseqfile=assdso.replace('\\','/')
				if not kseqfile in self.kassfiles:
					#print kseqfile
					#判断文件是否存在
					#测试节点返回的路径是否存在
					if os.path.exists(kseqfile):
						self.kassfiles.append(kseqfile)
					#如果不存在加上工程路径
					elif os.path.exists(self.projectDir+kseqfile):
						self.kassfiles.append(kseqfile)
					else:
						kerror_arnold.append(kassmesh)



if __name__ == "__main__":
	k_cachefinder()