import maya.cmds as cc
import os
import re
from xml.dom import minidom
import maya.app.general.fileTexturePathResolver as k

class k_cachefinder():
	#阿诺德缓存
	kassfiles=[]
	#有问题阿诺德节点
	kerror_arnold=[]

	#abc缓存
	kabcmeshfiles=[]

	#vray缓存
	kvrmeshfiles=[]
	#vrayIES
	kvrIESfiles=[]
	#VRaySettingsNode
	kvrsettfiles=[]
	#Vray全部的外部文件
	#Maya cache缓存
	kcacheFiles=[]
	#Maya cache xml数据
	kcacheFilesx=[]	

	#MR缓存
	kmrcacheFiles=[]

	#贴图
	kTexture=[]
	kmayaTex=[]
	kaiTex  =[]
	kVpTex  =[]


	#插件版本
	mayaplugin_version={}

	projectDir = cc.workspace(query=True,rootDirectory=True)    

	def __init__(self):
		#self.k_checkVRmeshfiles()
		#self.k_checkabcfiles()
		#self.k_checkassfiles()
		#self.k_checkabcfiles()
		#self.k_cachefiles()
		#self.k_checkMRmeshfiles()
		self.k_checkTexfiles()
		#for x in self.kmayaTex:
			#print x
		#for y in self.kcacheFiles:
			#print y
		#print self.mayaplugin_version

	def k_checkTexfiles(self):
		texfiles=cc.ls(type='file')
		for texfile in texfiles:
			#判断有无自定义属性
			userAttrs=cc.listAttr(texfile,ud=1)
			if userAttrs:
				#获取有无UDIM模式
				ktexmode=cc.getAttr(texfile+'.uvTilingMode')
				#如果无：
				if not ktexmode:
					for userAttr in userAttrs:
						#判断自定义内容是否 Tex 开头
						if userAttr[:3]=='Tex':
							#获取自定义属性的 内容
							userTex=cc.getAttr(texfile+"."+userAttr)
							#添加入总数组
							if userTex and not userTex in self.kmayaTex:
								if os.path.exists(userTex):
									#print texfile
									self.kmayaTex.append(userTex)
									#print userTex
									userTex_tx=os.path.splitext(userTex)[0]+'.tx'
									if os.path.exists(userTex_tx) and not userTex_tx in self.kmayaTex:
										self.kmayaTex.append(userTex_tx)
										#print userTex_tx


				#有UDIM模式
				else:
					for userAttr in userAttrs:
						#判断自定义内容是否 Tex 开头
						if userAttr[:3]=='Tex':
							userTex=cc.getAttr(texfile+"."+userAttr)
							#获取自定义内容 的UDIM贴图
							k_getUDIMp=k.getFilePatternString(userTex, False, ktexmode)    
							k_exudims=k.findAllFilesForPattern(k_getUDIMp,None)
							#添加贴图入总数组
							for k_exudim in k_exudims:
								if k_exudim and not k_exudim in self.kmayaTex:
									#print texfile
									self.kmayaTex.append(k_exudim)	
									#print k_exudim	

									k_exudim_tx=os.path.splitext(k_exudim)[0]+'.tx'
									if os.path.exists(k_exudim_tx) and not k_exudim_tx in self.kmayaTex:
										self.kmayaTex.append(k_exudim_tx)
										#print k_exudim_tx		


			else:
				ktexfile=cc.getAttr(texfile+'.fileTextureName')
				ktexmode=cc.getAttr(texfile+'.uvTilingMode')
				if not ktexmode:
					if ktexfile and not os.path.isabs(ktexfile):
						ktexfile=self.projectDir+ktexfile
					ktexfile=ktexfile.replace('\\','/')
					if ktexfile and not ktexfile in self.kmayaTex:
						if os.path.exists(ktexfile):
							#print texfile
							self.kmayaTex.append(ktexfile)
							#print ktexfile

							ktexfile_tx=os.path.splitext(ktexfile)[0]+'.tx'
							if os.path.exists(ktexfile_tx) and not ktexfile_tx in self.kmayaTex:
								self.kmayaTex.append(ktexfile_tx)
								#print ktexfile_tx	

				else:
					if ktexfile and not os.path.isabs(ktexfile):
						ktexfile=self.projectDir+ktexfile
					ktexfile=ktexfile.replace('\\','/')	
					k_getUDIMp=k.getFilePatternString(ktexfile, False, ktexmode) 
					k_exudim=k.findAllFilesForPattern(k_getUDIMp,None)
					for ktexfile in k_exudim:
						if ktexfile and not ktexfile in self.kmayaTex:
							#print texfile
							self.kmayaTex.append(ktexfile)
							#print ktexfile

							ktexfile_tx=os.path.splitext(ktexfile)[0]+'.tx'
							if os.path.exists(ktexfile_tx) and not ktexfile_tx in self.kmayaTex:
								self.kmayaTex.append(ktexfile_tx)
								#print ktexfile_tx

		#先判断插件有没开，防止找不到节点类型
		if cc.pluginInfo("mtoa",q=1,l=1):
			aiTexfiles=cc.ls(type='aiImage')
			if aiTexfiles:
				for aiTexfile in aiTexfiles:
					#返回文件路径
					aiTexfilesname = cc.getAttr(aiTexfile+'.filename')
					#判断是否为空 及 在总数组有无重复 及 文件是否存在
					if aiTexfilesname and not aiTexfilesname in self.kaiTex:
						if os.path.exists(aiTexfilesname):
							#print aiTexfilesname
							self.kaiTex.append(aiTexfilesname)

							#判断此文件有无tx版本的路径
							aiTexfilesname_tx=os.path.splitext(aiTexfilesname)[0]+'.tx'
							#判断文件是否存在 及 在总数组有无重复
							if os.path.exists(aiTexfilesname_tx) and not aiTexfilesname_tx in self.kaiTex:
								self.kaiTex.append(aiTexfilesname_tx)
								#print aiTexfilesname_tx

		#先判断插件有没开，防止找不到节点类型
		if cc.pluginInfo("vrayformaya",q=1,l=1):
			Vptexfiles=cc.ls(type='VRayPtex')
			if Vptexfiles:
				for Vptexfile in Vptexfiles:
					#返回文件路径
					Vptexfilename = cc.getAttr(Vptexfile+'.ptexFile')
					#判断是否为空 及 在总数组有无重复 及 文件是否存在
					if Vptexfilename and not Vptexfilename in self.kVpTex:
						if os.path.exists(Vptexfilename):
							#print Vptexfilename
							self.kaiTex.append(Vptexfilename)

							#判断此文件有无tx版本的路径
							Vptexfilename_tx=os.path.splitext(Vptexfilename)[0]+'.tx'
							#判断文件是否存在 及 在总数组有无重复
							if os.path.exists(Vptexfilename_tx) and not Vptexfilename_tx in self.kaiTex:
								self.kaiTex.append(Vptexfilename_tx)
								#print Vptexfilename_tx



			
		self.kTexture=list(set(self.kmayaTex+self.kaiTex+self.kVpTex))

		for a in self.kTexture:
			print a

	def k_checkMRmeshfiles(self):
		if cc.pluginInfo("Mayatomr",q=1,l=1):
			version = cc.pluginInfo("Mayatomr",q=1,v=1)
			self.mayaplugin_version.update({'mentalray':version})

			mrmeshs=cc.ls(type='mip_binaryproxy')
			for mrmesh in mrmeshs:
				kmrmesh=cc.getAttr(mrmesh+'.object_filename')
				if kmrmesh and not os.path.isabs(kmrmesh):
					kmrmesh=self.projectDir+kmrmesh
				kmrmesh=kmrmesh.replace('\\','/')
				if kmrmesh and not kmrmesh in self.kmrcacheFiles:
					if os.path.exists(kmrmesh):
						self.kmrcacheFiles.append(kmrmesh)		

			mrmeshs=cc.ls(type='mesh')
			for mrmesh in mrmeshs:
				kmrmesh=''
				try:
					kmrmesh=cc.getAttr(mrmesh+'.miProxyFile')
				except:pass
				if kmrmesh:
					if kmrmesh and not os.path.isabs(kmrmesh):
						kmrmesh=self.projectDir+kmrmesh
					kmrmesh=kmrmesh.replace('\\','/')
					if kmrmesh and not kmrmesh in self.kmrcacheFiles:
						if os.path.exists(kmrmesh):
							self.kmrcacheFiles.append(kmrmesh)	


	def k_checkVRmeshfiles(self):
		if cc.pluginInfo("vrayformaya",q=1,l=1):
			version = cc.pluginInfo("vrayformaya",q=1,v=1)
			self.mayaplugin_version.update({'Vray':version})
			#kwp = cc.workspace(q =True, rootDirectory=True)
			
			kvrmeshs=cc.ls(type='VRayMesh')
			for kvrmesh in kvrmeshs:
				krvrmesh=cc.listConnections((kvrmesh+'.output'),s=0,d=1)
				if krvrmesh:
					vrmesh=cc.getAttr(kvrmesh+'.fileName')
					if vrmesh and not os.path.isabs(vrmesh):
						vrmesh=self.projectDir+vrmesh
					vrmesh=vrmesh.replace('\\','/')
					if vrmesh and not vrmesh in self.kvrmeshfiles:
						if os.path.exists(vrmesh):
							self.kvrmeshfiles.append(vrmesh)

			kvrIESs=cc.ls(type="VRayLightIESShape")
			for kvrIES in kvrIESs:
				if cc.getAttr(kvrIES+'.enabled'):
					kIESfile = cc.getAttr(kvrIES+'.iesFile')
					if kIESfile and not os.path.isabs(kIESfile):
						kIESfile=self.projectDir+kIESfile
					kIESfile=kIESfile.replace('\\','/')
					if kIESfile and not kIESfile in self.kvrIESfiles:
						if os.path.exists(kIESfile):self.kvrIESfiles.append(kIESfile)

			vrsettfiles=cc.ls(type="VRaySettingsNode")
			for vrsettfile in vrsettfiles:
				for k_stype in ['causticsFile','fileName','pmap_file','imap_fileName']:
					kvrsettfile = cc.getAttr(vrsettfile+'.'+k_stype)
					if kvrsettfile and not kvrsettfile in self.kvrsettfiles:
						if os.path.exists(kvrsettfile):self.kvrsettfiles.append(kvrsettfile)

	def k_checkabcfiles(self):
		if cc.pluginInfo("AbcImport",q=1,l=1):
			version = cc.pluginInfo("AbcImport",q=1,v=1)
			self.mayaplugin_version.update({'Abc':version})

			kabcmeshs=cc.ls(type='AlembicNode')
			for kabcmesh in kabcmeshs:
				krabcmesh=cc.listConnections((kabcmesh+'.outPolyMesh'),s=0,d=1)
				kcabcmesh=cc.listConnections((kabcmesh+'.transOp'),s=0,d=1)
				if krabcmesh or kcabcmesh:
					abcfilepath=cc.getAttr(kabcmesh+'.abc_File')

					#判断是否为绝对路径
					if abcfilepath and not os.path.isabs(abcfilepath):
						abcfilepath=self.projectDir+abcfilepath
					abcfilepath=abcfilepath.replace('\\','/')

					if abcfilepath and not abcfilepath in self.kabcmeshfiles:
						if os.path.exists(abcfilepath):
							self.kabcmeshfiles.append(abcfilepath)	

	def k_cachefiles(self):
		kcachefiles=cc.ls(type='cacheFile')
		for kcachefile in kcachefiles:
			#检查是否无用节点
			krcfmesh=cc.listConnections((kcachefile+'.outCacheData'),s=0,d=1)
			cenable=cc.getAttr(kcachefile+'.enable')
			#print kcachefile,cenable
			if krcfmesh and cenable:
				#根据节点获取缓存路径 及 名称
				cfDir=cc.getAttr(kcachefile+'.cachePath')
				if cfDir and not os.path.isabs(cfDir):
					cfDir=self.projectDir+cfDir
				cfDir=cfDir.replace('\\','/')
				cfname=cc.getAttr(kcachefile+'.cacheName')
				#确保路径后面不加 /
				#print ('****'+cfDir)
				if cfDir[-1]=='/':
					cfDir=os.path.dirname(cfDir)
				cffile=cfDir+'/'+cfname+'.xml'
				#print ('----'+cffile)
				#判断有无重复检查
				if not cffile in self.kcacheFilesx:
					
					if os.path.exists(cffile):
						#print ('++++'+cffile)
						self.kcacheFilesx.append(cffile)
						#根据xml文件 获取 缓存的类型（合并还是每帧一个）及格式
						k_cacheFormat,k_cacheType=self.k_xml(cffile)
						#print k_cacheFormat
						#print k_cacheType
						#处理合并为一个文件的缓存
						if k_cacheType == 'OneFile':
							if k_cacheFormat == 'mcx' :
								#去除后缀 并且该为 mcx的后缀
								cffilef=os.path.splitext(cffile)[0]+'.mcx'
								if cffilef:
									self.kcacheFiles.append(cffilef)
									#print cffilef
							elif k_cacheFormat == 'mcc' :
								cffilef=os.path.splitext(cffile)[0]+'.mc'
								if cffilef:
									self.kcacheFiles.append(cffilef)
									#print cffilef

						#处理每帧一个文件
						elif k_cacheType == 'OneFilePerFrame':
							#print ('1-----'+cffile)
							cfDir = os.path.dirname(cffile)
							if cfDir:
								cachefs = os.listdir(cfDir)
								#print cachefs
								for cachef in cachefs:
									if k_cacheFormat == 'mcx':
										#去掉xml文件路径的 后缀
										cachefx = os.path.splitext(cffile)[0]
										#设定判断匹配公式 
										kexpc = r'%s(Frame)([0-9]+)(\.mcx)' %(cachefx)
										#将文件夹内的文件 加上文件夹路径
										cachef = cfDir+'/'+cachef
										#进行匹配
										match = re.search(kexpc,cachef)
										#print ('2++++'+cachefx)
										#print ('3++++'+cachef)
										#print ('4++++'+kexpc)
										if match:
											self.kcacheFiles.append(cachef)
											#print cachef
									elif k_cacheFormat == 'mcc':
										cachefx = os.path.splitext(cffile)[0]
										kexpc = r'%s(Frame)([0-9]+)(\.mc)' %(cachefx)
										cachef = cfDir+'/'+cachef
										match = re.search(kexpc,cachef)
										if match:
											self.kcacheFiles.append(cachef)
											#print cachef



	def k_xml(self,cffile):
		dom = minidom.parse(cffile)
		root = dom.documentElement
		f_cacheType = root.getElementsByTagName("cacheType")

		k_cacheFormat = f_cacheType[0].getAttribute('Format')
		k_cacheType   = f_cacheType[0].getAttribute('Type')							

		return k_cacheFormat,k_cacheType

	def k_checkassfiles(self):
		#maya节点返回的路径
		kassdso=[]
		#记录文件夹内里的文件，避免重复对网络进行获取
		kassfilepath={}

		self.kexpo  = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply|\.asstoc)$'
		self.kexpo2 = r'(.*?)([\._])([0-9#]*)([\.]?)([0-9#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'

		if cc.pluginInfo("mtoa",q=1,l=1):

			version = cc.pluginInfo("mtoa",q=1,v=1)
			self.mayaplugin_version.update({'Arnold':version})
			kassmeshs=cc.ls(type='aiStandIn')

			for kassmesh in kassmeshs:
				#先判断是否无下游输出的节点
				krassmesh=cc.listConnections(kassmesh,s=0,d=1)
				#kcassmesh=cc.listConnections((kassmesh+'.transOp'),s=0,d=1)
				if krassmesh:
					#print 'kassmesh  '+str(kassmesh)
					assdsom=cc.getAttr(kassmesh+'.dso')

					#判断是否为绝对路径
					if assdsom and not os.path.isabs(assdsom):
						assdso=self.projectDir+assdsom

					assdso=assdsom.replace('\\','/')

					#获取 缓存名 与 路径
					assmesh_getpath=os.path.basename(assdso)
					#print 'assdso  '+str(assdso)
					assmeshpath=os.path.dirname(assdso)
					#print 'assmeshpath  '+str(assmeshpath)

					#先判断有无重复检查
					if assdsom and not assdsom in kassdso:
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
				kexpc = r'%s%s([0-9]{%d})([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply|\.asstoc)$' %(pattern.group(1),pattern.group(2),k_NO)
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