import maya.cmds as cc
import os
import re

class k_cachefinder():
	#阿诺德缓存的数组
	kassfiles=[]
	#abc缓存的数组
	kabcmeshfiles=[]
	#vray缓存的数组
	kvrmeshfiles=[]
	#Maya cache缓存的数组
	kcacheFiles=[]
	#有问题阿诺德节点
	kerror_arnold=[]
	projectDir = cc.workspace(query=True,rootDirectory=True)    

	def __init__(self):
		#self.k_checkVRmeshfiles()
		#self.k_checkabcfiles()
		#self.k_checkassfiles()
		self.k_checkabcfiles()
		for x in self.kcacheFiles:
			print x


	def k_checkVRmeshfiles(self):
		#kwp = cc.workspace(q =True, rootDirectory=True)
		
		kvrmeshs=cc.ls(type='VRayMesh')
		for kvrmesh in kvrmeshs:
			krvrmesh=cc.listConnections((kvrmesh+'.output'),s=0,d=1)
			if krvrmesh:
				vrmesh=cc.getAttr(kvrmesh+'.fileName')
				if not os.path.isabs(vrmesh):
					vrmesh=self.projectDir+vrmesh
				vrmesh=vrmesh.replace('\\','/')
				if not vrmesh in self.kvrmeshfiles:
					if os.path.exists(vrmesh):
						self.kvrmeshfiles.append(vrmesh)


	def k_checkabcfiles(self):
		kabcmeshs=cc.ls(type='AlembicNode')
		for kabcmesh in kabcmeshs:
			krabcmesh=cc.listConnections((kabcmesh+'.outPolyMesh'),s=0,d=1)
			kcabcmesh=cc.listConnections((kabcmesh+'.transOp'),s=0,d=1)
			if krabcmesh or kcabcmesh:
				abcfilepath=cc.getAttr(kabcmesh+'.abc_File')

				#判断是否为绝对路径
				if not os.path.isabs(abcfilepath):
					abcfilepath=self.projectDir+abcfilepath
				abcfilepath=abcfilepath.replace('\\','/')

				if not abcfilepath in self.kabcmeshfiles:
					if os.path.exists(abcfilepath):
						self.kabcmeshfiles.append(abcfilepath)	

	def k_cachefiles(self):
		kcachefiles=cc.ls(type='cacheFile')
		for kcachefile in kcachefiles:
			krcfmesh=cc.listConnections((kcachefile+'.outCacheData'),s=0,d=1)
			if krcfmesh:
				cfDir=cc.getAttr(kcachefile+'.cachePath')
				if not os.path.isabs(cfDir):
					cfDir=self.projectDir+cfDir
				cfDir=cfDir.replace('\\','/')
				cfname=cc.getAttr(kcachefile+'.cacheName')
				cffile=cfDir+cfname+'.xml'
				if not cffile in self.kcacheFiles:
					print cffile
					if os.path.exists(cffile):
						self.kvrmeshfiles.append(cffile)

	def k_checkassfiles(self):
		#maya节点返回的路径
		kassdso=[]
		#记录文件夹内里的文件，避免重复对网络进行获取
		kassfilepath={}

		self.kexpo  = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'
		self.kexpo2 = r'(.*?)([\._])([0-9#]*)([\.]?)([0-9#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'

		kassmeshs=cc.ls(type='aiStandIn')
		for kassmesh in kassmeshs:
			#先判断是否无下游输出的节点
			krassmesh=cc.listConnections(kassmesh,s=0,d=1)
			#kcassmesh=cc.listConnections((kassmesh+'.transOp'),s=0,d=1)
			if krassmesh:
				#print 'kassmesh  '+str(kassmesh)
				assdsom=cc.getAttr(kassmesh+'.dso')

				#判断是否为绝对路径
				if not os.path.isabs(assdsom):
					assdso=self.projectDir+assdsom

				assdso=assdsom.replace('\\','/')

				#获取 缓存名 与 路径
				assmesh_getpath=os.path.basename(assdso)
				#print 'assdso  '+str(assdso)
				assmeshpath=os.path.dirname(assdso)
				#print 'assmeshpath  '+str(assmeshpath)

				#先判断有无重复检查
				if not assdsom in kassdso:
					kassdso.append(assdsom)
					#如果路径出现过
					if assmeshpath in kassfilepath:
						#k_filterseq=[]
						#asspathfiles=os.listdir(assmeshpath)
						asspathfiles=kassfilepath[assmeshpath]
						#print 'asspathfiles  '+str(asspathfiles)
						krseqfile=self.k_filterassfile(assdso,asspathfiles,kassmesh)
						#self.kassfiles.append(krseqfile)
					else:
						asspathfiles=[]
						#判断是否能根据文件夹 返回 文件夹里面的所有文件
						try:
							asspathfiles=os.listdir(assmeshpath)
						except WindowsError:
							#print e.message
							pass

						#print 'asspathfiles  '+str(asspathfiles)
						krseqfile=self.k_filterassfile(assdso,asspathfiles,kassmesh)
						#self.kassfiles.append(krseqfile)

						k_update={assmeshpath:asspathfiles}
						kassfilepath.update(k_update)
						
								#print 'kseq  '+str(kseq)
								#



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
				kpattern = re.search(kexpc, asspathfile)
				if kpattern:
					kseq=kpattern.group()
					#k_filterseq.append(kseq)
					kseqfile=assmeshpath+'/'+kseq
					if not kseqfile in self.kassfiles:
						if os.path.exists(kseqfile):
							self.kassfiles.append(kseqfile)
							#return kseqfile
							#print kseqfile



			else:
				#判断节点返回的数据 是否在 总的缓存数组里存在
				kseqfile=assdso
				if not kseqfile in self.kassfiles:
					#print kseqfile
					#判断文件是否存在
					#测试节点返回的路径是否存在
					if os.path.exists(kseqfile):
						self.kassfiles.append(kseqfile)
					else:
						self.kerror_arnold.append(kassmesh)



if __name__ == "__main__":
	k_cachefinder()