# -*- coding: utf-8 -*-

import maya.cmds as cc
import os
import re
from xml.dom import minidom
import maya.app.general.fileTexturePathResolver as k
import time

class k_cachefinder():

	def __init__(self):
		#阿诺德缓存
		self.kassfiles=[]
		#有问题阿诺德节点
		self.kerror_arnold=[]

		#abc缓存
		self.kabcmeshfiles=[]

		#Vray全部的外部文件
		self.kvrayfiles=[]
		#vray缓存
		self.kvrmeshfiles=[]
		#vrayIES
		#kvrIESfiles=[]
		#VRaySettingsNode
		self.kvrsettfiles=[]
		
		#Maya cache缓存
		self.kcacheFiles=[]
		#Maya cache xml数据
		self.kcacheFilesx=[]	

		#MR缓存
		self.kmrcacheFiles=[]

		#贴图
		self.kTexture=[]
		self.kmayaTex=[]
		self.kaiTex  =[]
		self.kVpTex  =[]
		#经典粒子缓存-+
		self.kparcache=[]

		#Yeti文件
		self.kYeti=[]
		#Yeti毛发缓存
		self.kYeticache=[]
		#Yeti毛发贴图
		self.kYetitex  =[]

		#shave毛发缓存
		self.kshave_cache=[]
		#插件版本
		self.mayaplugin_version={}

		#节点数据
		self.kNodedate={}

		#使用本地路径的节点
		self.klocal={}

		#外部文件总集合
		self.outside_file={}

		self.projectDir = cc.workspace(query=True,rootDirectory=True)  



	def k_checkit(self):
		self.k_checkassfiles()
		self.k_checkabcfiles()
		self.k_checkVRmeshfiles()
		self.k_cachefiles()
		self.k_checkTexfiles()
		self.k_checkYeticache()
		self.k_checkShaveCache()
		self.k_checkMRmeshfiles()
		self.k_checkDiskPcache()


		self.k_dirt(self.kassfiles,'Arnold')
		self.k_dirt(self.kabcmeshfiles,'Abc')
		self.k_dirt(self.kvrayfiles,'Vray')
		self.k_dirt(self.kcacheFiles,'nCache')
		self.k_dirt(self.kTexture,'Texture')	
		self.k_dirt(self.kYeti,'Yeti')
		self.k_dirt(self.kshave_cache,'Shave')		
		self.k_dirt(self.kmrcacheFiles,'mentalray')
		self.k_dirt(self.kparcache,'Particle')

		#print self.outside_file

		return self.outside_file



	def k_dirt(self,ksets,name):
		temp=[]
		for kset in ksets:
			temp.append(self.k_findes(kset))
		self.outside_file.update({name:temp})

	def k_findes(self,kfile):
		filesize = os.path.getsize(kfile)
		filedit  = time.localtime(os.stat(kfile).st_mtime)
		fileditg = time.strftime("%Y-%m-%d %H:%M:%S",filedit)
		return [kfile,filesize,fileditg]

	#获取maya节点数据  node=节点名字  port=需要获取的节点属性名字   path=属性内容
	def k_Nodedate(self,plugin,node,port,path):
		##########设置节点内容 及 加入到节点数据#############
		ktemp={'path':path,'port':port}
		if self.kNodedate.has_key(plugin):
			self.kNodedate[plugin].update({node:[ktemp]})
		else:self.kNodedate[plugin]={node:[ktemp]}
		####################################################

	def k_Nodedate2(self,plugin,node,port,path,**kwargs):
		##########设置节点内容 及 加入到节点数据#############
		ktemp={'path':path,'port':port}
		ktemp.update(kwargs)
		if self.kNodedate.has_key(plugin):
			#一个maya节点内 如果有多个需要返回的属性路径  用数组添加法
			if self.kNodedate[plugin].has_key(node):
				self.kNodedate[plugin][node].append(ktemp)
			else:
				self.kNodedate[plugin].update({node:[ktemp]})
		else:self.kNodedate[plugin]={node:[ktemp]}
		####################################################	




	def k_checkYeticache(self):
		#缓存匹配公式
		self.kexpo3  = r'(.*?)([\.]?)([%][0-9]*d)(\.fur)$'
		#贴图匹配公式
		self.kexpo4  = r'(.*?)([\.]?)([%][0-9]*d)(\.png|\.tif|\.exr)$'
		self.kexpu4  = r'(.*)(\.png|\.tif|\.exr)$'
		#节点返回的路径存放地  为了不重复检查

		if cc.pluginInfo("pgYetiMaya",q=1,l=1):
			yetis=cc.ls(type='pgYetiMaya')

			version = cc.pluginInfo("pgYetiMaya",q=1,v=1)
			self.mayaplugin_version.update({'Yeti':version})

			for yeti in yetis:
				yeticache=cc.getAttr(yeti+'.cacheFileName')


				#判断是否绝对路径
				if yeticache and not os.path.isabs(yeticache):
					yeticache=self.projectDir+yeticache

				if yeticache:

					##########设置节点内容 及 加入到节点数据#############
					self.k_Nodedate('kYeticache',yeti,'.cacheFileName',yeticache)
					####################################################
					


					#获取 缓存名 与 路径
					yeticache_name=os.path.basename(yeticache)
					yeticache_dir =os.path.dirname (yeticache)

					pattern = re.search(self.kexpo3,yeticache)

					if pattern:
						try:
							#返回路径下的所谓文件
							yeticachefiles=os.listdir(yeticache_dir)
							for yeticachefile in yeticachefiles:
								#print yeticachefile
								#匹配
								kexpc = r'%s%s([0-9]*)(\.fur)$' %(pattern.group(1),pattern.group(2))
								
								#判断是否在盘的根目录   防止出现E：//xxxxx 这种情况
								if yeticache_dir[-2:]==':/':
									yeticachefilef=yeticache_dir+yeticachefile
								else:yeticachefilef=yeticache_dir+'/'+yeticachefile

								pattern2 = re.search(kexpc,yeticachefilef)
								if pattern2 and not yeticachefilef in self.kYeticache:
									self.kYeticache.append(yeticachefilef)
									#print yeticachefilef

						except:
							#print e.message
							pass

					else:
						#非序列的文件
						if os.path.exists(yeticache) and not yeticache in self.kYeticache:
							self.kYeticache.append(yeticache)
							#print yeticache
						


				#pgYetiGraph为 yeti提供的mel
				try:
					yetiTexs=cc.pgYetiGraph(yeti,listNodes=True,type='texture')
					enablecache = cc.getAttr(yeti+'.fileMode')

					if yetiTexs:
						for yetiTex in yetiTexs:
							#获取yeti Graph里面的节点 及 参数
							yetiTexfile=cc.pgYetiGraph(yeti,node=yetiTex,param='file_name',getParamValue=True)
							if yetiTexfile and not os.path.isabs(yetiTexfile):
								yetiTexfile=self.projectDir+yetiTexfile
							yetiTexfile=yetiTexfile.replace('\\','/')

							if yetiTexfile:


								##########设置节点内容 及 加入到节点数据#############
								self.k_Nodedate2('kYetitex',yeti,yetiTex,yetiTexfile,fileMode=enablecache)
								#####################################################

								yetiTex_name=os.path.basename(yetiTexfile)
								yetiTex_dir =os.path.dirname (yetiTexfile)

								patternt = re.search(self.kexpo4,yetiTexfile)
								#匹配是否为序列格式
								if patternt:
									try:
										YetiTexfiles=os.listdir(yetiTex_dir)
										for YetiTexfile in YetiTexfiles:
											#print yeticachefile
											kexpt = r'%s%s([0-9]*)(\.png|\.tif|\.exr)$' %(patternt.group(1),patternt.group(2))
											#判断是否在盘的根目录   防止出现E：//xxxxx 这种情况
											if yetiTex_dir[-2:]==':/':
												YetiTexfilef=yetiTex_dir+YetiTexfile
											else:YetiTexfilef=yetiTex_dir+'/'+YetiTexfile
											#匹配完整路径格式
											pattern = re.search(kexpt,YetiTexfilef)
											if pattern and not YetiTexfilef in self.kYetitex:
												self.kYetitex.append(YetiTexfilef)
												#print YetiTexfilef
									except:
										#print e.message
										pass
								else:
									if os.path.exists(yetiTexfile) and not yetiTexfile in self.kYeticache:
										#匹配yeti支持的图片格式
										patternt = re.search(self.kexpu4,yetiTexfile)
										if patternt and not yetiTexfile in self.kYetitex:
											self.kYetitex.append(yetiTexfile)
											#print yetiTexfile

				except:
					pass

			self.kYeti=list(set(self.kYeticache+self.kYetitex))



	def k_checkShaveCache(self):
		if cc.pluginInfo("shaveNode",q=1,l=1):

			version = cc.pluginInfo("shaveNode",q=1,v=1)
			self.mayaplugin_version.update({'shave':version})

			#shaveGlobals=cc.ls(type='shaveGlobals')
			kshaveHairs=cc.ls(type='shaveHair')

			#if 'shaveGlobals' in shaveGlobals:
			#只返回指定的shaveGlobal节点内容
			shaveStat=''
			try:
				shaveStat=cc.getAttr('shaveGlobals.tmpDir')
			except:
				pass
			if shaveStat and not os.path.isabs(shaveStat):
				shaveStat=self.projectDir+shaveStat
			

			if shaveStat:
				shaveStat=shaveStat.replace('\\','/')

				##########设置节点内容 及 加入到节点数据#############
				self.k_Nodedate('kshave_cache','shaveGlobals','.tmpDir',shaveStat)
				#####################################################

				try:
					shaveStatfiles=os.listdir(shaveStat)

					for shaveStatfile in shaveStatfiles:

						# 针对文件内有多个shave节点 返回shave节点的名字匹配缓存名字
						for kshaveHair in kshaveHairs:
							#将shave节点的：号改成_ （针对参考类型的shave节点）
							kshaveHair = kshaveHair.replace(':','_');
							#匹配每个shave节点对应的缓存
							kexpo  = r'(shaveStatFile_)(%s)(\.?)([0-9]*)(.stat)$' %(kshaveHair)

							pattern = re.search(kexpo,shaveStatfile)
							if pattern :
								#
								if shaveStat[-1]=='/':
									shaveStatfile=shaveStat+shaveStatfile
								else:shaveStatfile=shaveStat+'/'+shaveStatfile

								if not shaveStatfile in self.kshave_cache:
									self.kshave_cache.append(shaveStatfile)
									#print shaveStatfile

						

						#匹配shave特定OBJ文件
						kexpo2 = r'(shaveObjFile_)(.*?)(.obj)$'
						kexpo3 = r'(shaveInstance_)(.*?)(.obj)$'

						pattern2 = re.search(kexpo2,shaveStatfile)
						pattern3 = re.search(kexpo3,shaveStatfile)
						if pattern2 or pattern3 and not shaveStatfile in self.kshave_cache:
							self.kshave_cache.append(shaveStatfile)
							#print shaveStatfile

				except:
					pass



	def k_checkDiskPcache(self):
		#获取缓存控制节点
		dyns = cc.ls(type='dynGlobals')
		#它可能有多个
		for dyn in dyns:
			if cc.getAttr(dyn+'.useParticleDiskCache'):
				#找出工程目录定义的粒子缓存 存放地址
				parpath = cc.workspace(fre='particles')
				fparpath = self.projectDir+parpath
				#获取粒子缓存具体子目录
				pcacheDir=cc.getAttr(dyn+'.cd')
				if pcacheDir:
					#获取最终目录位置
					cachepath=fparpath+'/'+pcacheDir

					try:
						#列出目录里的的所有文件
						cachepathfiles=os.listdir(cachepath)
						for cachepathfile in cachepathfiles:

							cachepath=cachepath.replace('\\','/')
							if cachepath[-1]=='/':
								cachepathfile=cachepath+cachepathfile
							else:cachepathfile=cachepath+'/'+cachepathfile

							#分离后缀 查询后缀 是否为pdc格式
							if os.path.splitext(cachepathfile)[-1]=='.pdc' and not cachepathfile in self.kparcache:
								self.kparcache.append(cachepathfile)
								#print cachepathfile
					except:
						pass


		
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


							##########设置节点内容 及 加入到节点数据#############
							self.k_Nodedate2('kmayaTex_userTex',texfile,('.'+userAttr),userTex)
							#####################################################

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
							
							##########设置节点内容 及 加入到节点数据#############
							self.k_Nodedate2('kmayaTex_userTex',texfile,('.'+userAttr),userTex)
							#####################################################

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

					if ktexfile:
						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kmayaTex_default',texfile,'.fileTextureName',ktexfile)
						#####################################################			
									
						if not ktexfile in self.kmayaTex and os.path.exists(ktexfile):
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

					if ktexfile:
						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kmayaTex_default',texfile,'.fileTextureName',ktexfile)
						#####################################################	

						#maya内部UDIM命令
						k_getUDIMp=k.getFilePatternString(ktexfile, False, ktexmode) 
						k_exudim=k.findAllFilesForPattern(k_getUDIMp,None)
						for ktexfile in k_exudim:
							if not ktexfile in self.kmayaTex:
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
					if aiTexfilesname :

						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kaiTex',aiTexfile,'.filename',aiTexfilesname)
						#####################################################

						if not aiTexfilesname in self.kaiTex and os.path.exists(aiTexfilesname):
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
					if Vptexfilename :

						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kVpTex',Vptexfile,'.ptexFile',Vptexfilename)
						#####################################################
						
						if not Vptexfilename in self.kVpTex and os.path.exists(Vptexfilename):
							#print Vptexfilename
							self.kaiTex.append(Vptexfilename)

							#判断此文件有无tx版本的路径
							Vptexfilename_tx=os.path.splitext(Vptexfilename)[0]+'.tx'
							#判断文件是否存在 及 在总数组有无重复
							if os.path.exists(Vptexfilename_tx) and not Vptexfilename_tx in self.kaiTex:
								self.kaiTex.append(Vptexfilename_tx)
								#print Vptexfilename_tx



			
		self.kTexture=list(set(self.kmayaTex+self.kaiTex+self.kVpTex))

		

	def k_checkMRmeshfiles(self):
		if cc.pluginInfo("Mayatomr",q=1,l=1):
			version = cc.pluginInfo("Mayatomr",q=1,v=1)
			self.mayaplugin_version.update({'mentalray':version})


			#检查mesh节点 mentalray栏内的缓存路径
			mrmeshs=cc.ls(type='mesh')
			for mrmesh in mrmeshs:
				kmrmesh=cc.getAttr(mrmesh+'.miProxyFile')
				if kmrmesh:
					##########设置节点内容 及 加入到节点数据#############
					self.k_Nodedate('kmrcacheFiles',mrmesh,'.miProxyFile',kmrmesh)
					#####################################################

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
			
			#查询vray代理
			kvrmeshs=cc.ls(type='VRayMesh')
			for kvrmesh in kvrmeshs:
				krvrmesh=cc.listConnections((kvrmesh+'.output'),s=0,d=1)
				if krvrmesh:
					vrmesh=cc.getAttr(kvrmesh+'.fileName')
					if vrmesh and not os.path.isabs(vrmesh):
						vrmesh=self.projectDir+vrmesh
					vrmesh=vrmesh.replace('\\','/')

					##########设置节点内容 及 加入到节点数据#############
					self.k_Nodedate('kvrmeshfiles',kvrmesh,'.fileName',vrmesh)
					#####################################################

					if vrmesh and not vrmesh in self.kvrmeshfiles:
						if os.path.exists(vrmesh):
							self.kvrmeshfiles.append(vrmesh)


			#查询vray光子图
			vrsettfiles=cc.ls(type="VRaySettingsNode")
			for vrsettfile in vrsettfiles:
				#causticsFile----散射图，fileName ----lightcache图  pmap_file ---photon map imap_fileName --- Irradiance map
				for k_stype in ['causticsFile','fileName','pmap_file','imap_fileName']:
					kvrsettfile = cc.getAttr(vrsettfile+'.'+k_stype)
					if kvrsettfile and not kvrsettfile in self.kvrsettfiles:
						
						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kvrsettfiles',vrsettfile,('.'+k_stype),kvrsettfile)
						#####################################################

						if os.path.exists(kvrsettfile):self.kvrsettfiles.append(kvrsettfile)


			self.kvrayfiles=list(set(self.kvrmeshfiles+self.kvrsettfiles))

			

	def k_checkabcfiles(self):
		if cc.pluginInfo("AbcImport",q=1,l=1):
			version = cc.pluginInfo("AbcImport",q=1,v=1)
			self.mayaplugin_version.update({'Abc':version})

			kabcmeshs=cc.ls(type='AlembicNode')
			for kabcmesh in kabcmeshs:
				#确认abc节点有无输出，
				krabcmesh=cc.listConnections((kabcmesh+'.outPolyMesh'),s=0,d=1)
				kcabcmesh=cc.listConnections((kabcmesh+'.transOp'),s=0,d=1)
				if krabcmesh or kcabcmesh:
					abcfilepath=cc.getAttr(kabcmesh+'.abc_File')

					#判断是否为绝对路径
					if abcfilepath and not os.path.isabs(abcfilepath):
						abcfilepath=self.projectDir+abcfilepath
					abcfilepath=abcfilepath.replace('\\','/')

					if abcfilepath:
						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kabcmeshfiles',kabcmesh,'.abc_File',abcfilepath)
						#####################################################

						if not abcfilepath in self.kabcmeshfiles and os.path.exists(abcfilepath):
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

				if os.path.exists(cffile):
					#print ('++++'+cffile)
					
					##########设置节点内容 及 加入到节点数据#############
					self.k_Nodedate('kcacheFiles',kcachefile,'.cachePath',cfDir)
					#####################################################


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
						#cfDir = os.path.dirname(cffile)

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
		#self.kexpo2 = r'(.*?)([\._])([0-9#]*)([\.]?)([0-9#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'

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
						assdsom=self.projectDir+assdsom

					assdsom=assdsom.replace('\\','/')

					#获取 缓存名 与 路径
					assmesh_getpath=os.path.basename(assdsom)
					#print 'assdso  '+str(assdso)
					assmeshpath=os.path.dirname(assdsom)
					#print 'assmeshpath  '+str(assmeshpath)

					#先判断有无重复检查
					if assdsom :
						##########设置节点内容 及 加入到节点数据#############
						self.k_Nodedate('kassfiles',kassmesh,'.dso',assdsom)
						#####################################################

						if not assdsom in kassdso:
							kassdso.append(assdsom)
							#如果路径出现过
							if assmeshpath in kassfilepath:
								#k_filterseq=[]
								#asspathfiles=os.listdir(assmeshpath)
								asspathfiles=kassfilepath[assmeshpath]
								#print 'asspathfiles  '+str(asspathfiles)
								krseqfile=self.k_filterassfile(assdsom,asspathfiles,kassmesh)
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
								krseqfile=self.k_filterassfile(assdsom,asspathfiles,kassmesh)
								#self.kassfiles.append(krseqfile)

								k_update={assmeshpath:asspathfiles}
								kassfilepath.update(k_update)
								
										#print 'kseq  '+str(kseq)
										#



			#print kassfilepath


	#执行过滤判断    assdso=节点返回的数据   asspathfiles=文件夹下的所有文件  kassmesh=maya节点名字
	def k_filterassfile(self,assdsom,asspathfiles,kassmesh):
		#根据节点返回的数据 获取文件名字 与 路径
		assmesh_getpath=os.path.basename(assdsom)
		assmeshpath=os.path.dirname(assdsom)

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
					
					#判断是否在盘的根目录   防止出现E：//xxxxx 这种情况
					if assmeshpath[-2:]==':/':
						kseqfile=assmeshpath+kseq
					else:kseqfile=assmeshpath+'/'+kseq


					if not kseqfile in self.kassfiles:
						if os.path.exists(kseqfile):
							self.kassfiles.append(kseqfile)
							#return kseqfile
							#print kseqfile



			else:
				#判断节点返回的数据 是否在 总的缓存数组里存在
				kseqfile=assdsom
				if not kseqfile in self.kassfiles:
					#print kseqfile
					#判断文件是否存在
					#测试节点返回的路径是否存在
					if os.path.exists(kseqfile):
						self.kassfiles.append(kseqfile)
					else:
						self.kerror_arnold.append(kassmesh)



if __name__ == "__main__":
	a=k_cachefinder()
	a.k_checkit()