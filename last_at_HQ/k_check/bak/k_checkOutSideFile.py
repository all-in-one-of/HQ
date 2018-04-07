# -*- coding: utf-8 -*-

import maya.cmds as cc
import os
import re
from xml.dom import minidom
import maya.app.general.fileTexturePathResolver as k
import time

class k_cachefinder():

	def __init__(self):

		self.kassfiles=[]
		self.kerror_arnold=[]
		self.kabcmeshfiles=[]
		self.kvrayfiles=[]
		self.kvrmeshfiles=[]
		self.kvrsettfiles=[]
		self.kcacheFiles=[]
		self.kcacheFilesx=[]	
		self.kmrcacheFiles=[]
		self.kTexture=[]
		self.kmayaTex=[]
		self.kaiTex  =[]
		self.kVpTex  =[]
		self.kparcache=[]
		self.kYeti=[]
		self.kYeticache=[]
		self.kYetitex  =[]
		self.kshave_cache=[]
		self.mayaplugin_version={}
		self.kNodedate={}
		self.klocal={}
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

	def k_Nodedate(self,plugin,node,port,path):
		ktemp={'path':path,'port':port}
		if self.kNodedate.has_key(plugin):
			self.kNodedate[plugin].update({node:[ktemp]})
		else:self.kNodedate[plugin]={node:[ktemp]}
		####################################################

	def k_Nodedate2(self,plugin,node,port,path,**kwargs):
		ktemp={'path':path,'port':port}
		ktemp.update(kwargs)
		if self.kNodedate.has_key(plugin):
			if self.kNodedate[plugin].has_key(node):
				self.kNodedate[plugin][node].append(ktemp)
			else:
				self.kNodedate[plugin].update({node:[ktemp]})
		else:self.kNodedate[plugin]={node:[ktemp]}
		####################################################	




	def k_checkYeticache(self):
		self.kexpo3  = r'(.*?)([\.]?)([%][0-9]*d)(\.fur)$'
		self.kexpo4  = r'(.*?)([\.]?)([%][0-9]*d)(\.png|\.tif|\.exr)$'
		self.kexpu4  = r'(.*)(\.png|\.tif|\.exr)$'

		if cc.pluginInfo("pgYetiMaya",q=1,l=1):
			yetis=cc.ls(type='pgYetiMaya')
			version = cc.pluginInfo("pgYetiMaya",q=1,v=1)
			self.mayaplugin_version.update({'Yeti':version})

			for yeti in yetis:
				yeticache=cc.getAttr(yeti+'.cacheFileName')
				if yeticache and not os.path.isabs(yeticache):
					yeticache=self.projectDir+yeticache
				if yeticache:
					self.k_Nodedate('kYeticache',yeti,'.cacheFileName',yeticache)
					yeticache_name=os.path.basename(yeticache)
					yeticache_dir =os.path.dirname (yeticache)
					pattern = re.search(self.kexpo3,yeticache)
					if pattern:
						try:
							yeticachefiles=os.listdir(yeticache_dir)
							for yeticachefile in yeticachefiles:
								kexpc = r'%s%s([0-9]*)(\.fur)$' %(pattern.group(1),pattern.group(2))
								if yeticache_dir[-2:]==':/':
									yeticachefilef=yeticache_dir+yeticachefile
								else:yeticachefilef=yeticache_dir+'/'+yeticachefile

								pattern2 = re.search(kexpc,yeticachefilef)
								if pattern2 and not yeticachefilef in self.kYeticache:
									self.kYeticache.append(yeticachefilef)
						except:
							pass

					else:
						if os.path.exists(yeticache) and not yeticache in self.kYeticache:
							self.kYeticache.append(yeticache)
						
				try:
					yetiTexs=cc.pgYetiGraph(yeti,listNodes=True,type='texture')
					enablecache = cc.getAttr(yeti+'.fileMode')

					if yetiTexs:
						for yetiTex in yetiTexs:
							yetiTexfile=cc.pgYetiGraph(yeti,node=yetiTex,param='file_name',getParamValue=True)
							if yetiTexfile and not os.path.isabs(yetiTexfile):
								yetiTexfile=self.projectDir+yetiTexfile
							yetiTexfile=yetiTexfile.replace('\\','/')

							if yetiTexfile:
								self.k_Nodedate2('kYetitex',yeti,yetiTex,yetiTexfile,fileMode=enablecache)
								yetiTex_name=os.path.basename(yetiTexfile)
								yetiTex_dir =os.path.dirname (yetiTexfile)
								patternt = re.search(self.kexpo4,yetiTexfile)
								if patternt:
									try:
										YetiTexfiles=os.listdir(yetiTex_dir)
										for YetiTexfile in YetiTexfiles:
											kexpt = r'%s%s([0-9]*)(\.png|\.tif|\.exr)$' %(patternt.group(1),patternt.group(2))
											if yetiTex_dir[-2:]==':/':
												YetiTexfilef=yetiTex_dir+YetiTexfile
											else:YetiTexfilef=yetiTex_dir+'/'+YetiTexfile
											pattern = re.search(kexpt,YetiTexfilef)
											if pattern and not YetiTexfilef in self.kYetitex:
												self.kYetitex.append(YetiTexfilef)
									except:
										pass
								else:
									if os.path.exists(yetiTexfile) and not yetiTexfile in self.kYeticache:
										patternt = re.search(self.kexpu4,yetiTexfile)
										if patternt and not yetiTexfile in self.kYetitex:
											self.kYetitex.append(yetiTexfile)
				except:
					pass

			self.kYeti=list(set(self.kYeticache+self.kYetitex))

	def k_checkShaveCache(self):
		if cc.pluginInfo("shaveNode",q=1,l=1):
			version = cc.pluginInfo("shaveNode",q=1,v=1)
			self.mayaplugin_version.update({'shave':version})
			kshaveHairs=cc.ls(type='shaveHair')
			shaveStat=''
			try:
				shaveStat=cc.getAttr('shaveGlobals.tmpDir')
			except:
				pass
			if shaveStat and not os.path.isabs(shaveStat):
				shaveStat=self.projectDir+shaveStat

			if shaveStat:
				shaveStat=shaveStat.replace('\\','/')
				self.k_Nodedate('kshave_cache','shaveGlobals','.tmpDir',shaveStat)
				try:
					shaveStatfiles=os.listdir(shaveStat)

					for shaveStatfile in shaveStatfiles:
						for kshaveHair in kshaveHairs:
							kshaveHair = kshaveHair.replace(':','_');
							kexpo  = r'(shaveStatFile_)(%s)(\.?)([0-9]*)(.stat)$' %(kshaveHair)
							pattern = re.search(kexpo,shaveStatfile)
							if pattern :
								if shaveStat[-1]=='/':
									shaveStatfile=shaveStat+shaveStatfile
								else:shaveStatfile=shaveStat+'/'+shaveStatfile
								if not shaveStatfile in self.kshave_cache:
									self.kshave_cache.append(shaveStatfile)


						kexpo2 = r'(shaveObjFile_)(.*?)(.obj)$'
						kexpo3 = r'(shaveInstance_)(.*?)(.obj)$'
						pattern2 = re.search(kexpo2,shaveStatfile)
						pattern3 = re.search(kexpo3,shaveStatfile)
						if pattern2 or pattern3 and not shaveStatfile in self.kshave_cache:
							self.kshave_cache.append(shaveStatfile)
				except:
					pass

	def k_checkDiskPcache(self):
		dyns = cc.ls(type='dynGlobals')
		for dyn in dyns:
			if cc.getAttr(dyn+'.useParticleDiskCache'):
				parpath = cc.workspace(fre='particles')
				fparpath = self.projectDir+parpath
				pcacheDir=cc.getAttr(dyn+'.cd')
				if pcacheDir:
					cachepath=fparpath+'/'+pcacheDir
					try:
						cachepathfiles=os.listdir(cachepath)
						for cachepathfile in cachepathfiles:

							cachepath=cachepath.replace('\\','/')
							if cachepath[-1]=='/':
								cachepathfile=cachepath+cachepathfile
							else:cachepathfile=cachepath+'/'+cachepathfile

							if os.path.splitext(cachepathfile)[-1]=='.pdc' and not cachepathfile in self.kparcache:
								self.kparcache.append(cachepathfile)
					except:
						pass


		
	def k_checkTexfiles(self):
		texfiles=cc.ls(type='file')
		for texfile in texfiles:
			userAttrs=cc.listAttr(texfile,ud=1)
			if userAttrs:
				ktexmode=cc.getAttr(texfile+'.uvTilingMode')
				if not ktexmode:
					for userAttr in userAttrs:
						if userAttr[:3]=='Tex':
							userTex=cc.getAttr(texfile+"."+userAttr)
							self.k_Nodedate2('kmayaTex_userTex',texfile,('.'+userAttr),userTex)
							#####################################################

							if userTex and not userTex in self.kmayaTex:
								if os.path.exists(userTex):
									self.kmayaTex.append(userTex)
									userTex_tx=os.path.splitext(userTex)[0]+'.tx'
									if os.path.exists(userTex_tx) and not userTex_tx in self.kmayaTex:
										self.kmayaTex.append(userTex_tx)

				else:
					for userAttr in userAttrs:
						if userAttr[:3]=='Tex':
							userTex=cc.getAttr(texfile+"."+userAttr)
							self.k_Nodedate2('kmayaTex_userTex',texfile,('.'+userAttr),userTex)
							#####################################################
							k_getUDIMp=k.getFilePatternString(userTex, False, ktexmode)    
							k_exudims=k.findAllFilesForPattern(k_getUDIMp,None)
							for k_exudim in k_exudims:
								if k_exudim and not k_exudim in self.kmayaTex:
									self.kmayaTex.append(k_exudim)	

									k_exudim_tx=os.path.splitext(k_exudim)[0]+'.tx'
									if os.path.exists(k_exudim_tx) and not k_exudim_tx in self.kmayaTex:
										self.kmayaTex.append(k_exudim_tx)	


			else:
				ktexfile=cc.getAttr(texfile+'.fileTextureName')
				ktexmode=cc.getAttr(texfile+'.uvTilingMode')


				if not ktexmode:
					if ktexfile and not os.path.isabs(ktexfile):
						ktexfile=self.projectDir+ktexfile
					ktexfile=ktexfile.replace('\\','/')

					if ktexfile:
						self.k_Nodedate('kmayaTex_default',texfile,'.fileTextureName',ktexfile)
						#####################################################			
									
						if not ktexfile in self.kmayaTex and os.path.exists(ktexfile):
							self.kmayaTex.append(ktexfile)
							ktexfile_tx=os.path.splitext(ktexfile)[0]+'.tx'
							if os.path.exists(ktexfile_tx) and not ktexfile_tx in self.kmayaTex:
								self.kmayaTex.append(ktexfile_tx)


				else:
					if ktexfile and not os.path.isabs(ktexfile):
						ktexfile=self.projectDir+ktexfile
					ktexfile=ktexfile.replace('\\','/')	

					if ktexfile:
						self.k_Nodedate('kmayaTex_default',texfile,'.fileTextureName',ktexfile)
						#####################################################	

						k_getUDIMp=k.getFilePatternString(ktexfile, False, ktexmode) 
						k_exudim=k.findAllFilesForPattern(k_getUDIMp,None)
						for ktexfile in k_exudim:
							if not ktexfile in self.kmayaTex:
								self.kmayaTex.append(ktexfile)
								ktexfile_tx=os.path.splitext(ktexfile)[0]+'.tx'
								if os.path.exists(ktexfile_tx) and not ktexfile_tx in self.kmayaTex:
									self.kmayaTex.append(ktexfile_tx)


		if cc.pluginInfo("mtoa",q=1,l=1):
			aiTexfiles=cc.ls(type='aiImage')
			if aiTexfiles:
				for aiTexfile in aiTexfiles:
					aiTexfilesname = cc.getAttr(aiTexfile+'.filename')
					if aiTexfilesname :
						self.k_Nodedate('kaiTex',aiTexfile,'.filename',aiTexfilesname)
						#####################################################

						if not aiTexfilesname in self.kaiTex and os.path.exists(aiTexfilesname):
							self.kaiTex.append(aiTexfilesname)

							aiTexfilesname_tx=os.path.splitext(aiTexfilesname)[0]+'.tx'
							if os.path.exists(aiTexfilesname_tx) and not aiTexfilesname_tx in self.kaiTex:
								self.kaiTex.append(aiTexfilesname_tx)


		if cc.pluginInfo("vrayformaya",q=1,l=1):
			Vptexfiles=cc.ls(type='VRayPtex')
			if Vptexfiles:
				for Vptexfile in Vptexfiles:
					Vptexfilename = cc.getAttr(Vptexfile+'.ptexFile')
					if Vptexfilename :
						self.k_Nodedate('kVpTex',Vptexfile,'.ptexFile',Vptexfilename)
						#####################################################
						
						if not Vptexfilename in self.kVpTex and os.path.exists(Vptexfilename):
							self.kaiTex.append(Vptexfilename)
							Vptexfilename_tx=os.path.splitext(Vptexfilename)[0]+'.tx'
							if os.path.exists(Vptexfilename_tx) and not Vptexfilename_tx in self.kaiTex:
								self.kaiTex.append(Vptexfilename_tx)


			
		self.kTexture=list(set(self.kmayaTex+self.kaiTex+self.kVpTex))

		

	def k_checkMRmeshfiles(self):
		if cc.pluginInfo("Mayatomr",q=1,l=1):
			version = cc.pluginInfo("Mayatomr",q=1,v=1)
			self.mayaplugin_version.update({'mentalray':version})

			mrmeshs=cc.ls(type='mesh')
			for mrmesh in mrmeshs:
				kmrmesh=cc.getAttr(mrmesh+'.miProxyFile')
				if kmrmesh:
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

			kvrmeshs=cc.ls(type='VRayMesh')
			for kvrmesh in kvrmeshs:
				krvrmesh=cc.listConnections((kvrmesh+'.output'),s=0,d=1)
				if krvrmesh:
					vrmesh=cc.getAttr(kvrmesh+'.fileName')
					if vrmesh and not os.path.isabs(vrmesh):
						vrmesh=self.projectDir+vrmesh
					vrmesh=vrmesh.replace('\\','/')

					self.k_Nodedate('kvrmeshfiles',kvrmesh,'.fileName',vrmesh)
					#####################################################

					if vrmesh and not vrmesh in self.kvrmeshfiles:
						if os.path.exists(vrmesh):
							self.kvrmeshfiles.append(vrmesh)


			vrsettfiles=cc.ls(type="VRaySettingsNode")
			for vrsettfile in vrsettfiles:
				for k_stype in ['causticsFile','fileName','pmap_file','imap_fileName']:
					kvrsettfile = cc.getAttr(vrsettfile+'.'+k_stype)
					if kvrsettfile and not kvrsettfile in self.kvrsettfiles:
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
				krabcmesh=cc.listConnections((kabcmesh+'.outPolyMesh'),s=0,d=1)
				kcabcmesh=cc.listConnections((kabcmesh+'.transOp'),s=0,d=1)
				if krabcmesh or kcabcmesh:
					abcfilepath=cc.getAttr(kabcmesh+'.abc_File')

					if abcfilepath and not os.path.isabs(abcfilepath):
						abcfilepath=self.projectDir+abcfilepath
					abcfilepath=abcfilepath.replace('\\','/')

					if abcfilepath:
						self.k_Nodedate('kabcmeshfiles',kabcmesh,'.abc_File',abcfilepath)
						#####################################################

						if not abcfilepath in self.kabcmeshfiles and os.path.exists(abcfilepath):
							self.kabcmeshfiles.append(abcfilepath)	

			

	def k_cachefiles(self):
		kcachefiles=cc.ls(type='cacheFile')
		for kcachefile in kcachefiles:
			krcfmesh=cc.listConnections((kcachefile+'.outCacheData'),s=0,d=1)
			cenable=cc.getAttr(kcachefile+'.enable')

			if krcfmesh and cenable:
				cfDir=cc.getAttr(kcachefile+'.cachePath')
				if cfDir and not os.path.isabs(cfDir):
					cfDir=self.projectDir+cfDir
				cfDir=cfDir.replace('\\','/')
				cfname=cc.getAttr(kcachefile+'.cacheName')
				if cfDir[-1]=='/':
					cfDir=os.path.dirname(cfDir)
				cffile=cfDir+'/'+cfname+'.xml'


				if os.path.exists(cffile):
					self.kcacheFiles.append(cffile)
					self.k_Nodedate('kcacheFiles',kcachefile,'.cachePath',cfDir)
					#####################################################
					k_cacheFormat,k_cacheType=self.k_xml(cffile)

					if k_cacheType == 'OneFile':
						if k_cacheFormat == 'mcx' :
							cffilef=os.path.splitext(cffile)[0]+'.mcx'
							if cffilef:
								self.kcacheFiles.append(cffilef)

						elif k_cacheFormat == 'mcc' :
							cffilef=os.path.splitext(cffile)[0]+'.mc'
							if cffilef:
								self.kcacheFiles.append(cffilef)


					elif k_cacheType == 'OneFilePerFrame':
						cachefs = os.listdir(cfDir)
						for cachef in cachefs:
							if k_cacheFormat == 'mcx':
								cachefx = os.path.splitext(cffile)[0]
								kexpc = r'%s(Frame)([0-9]+)(\.mcx)' %(cachefx)
								cachef = cfDir+'/'+cachef
								match = re.search(kexpc,cachef)
								if match:
									self.kcacheFiles.append(cachef)

							elif k_cacheFormat == 'mcc':
								cachefx = os.path.splitext(cffile)[0]
								kexpc = r'%s(Frame)([0-9]+)(\.mc)' %(cachefx)
								cachef = cfDir+'/'+cachef
								match = re.search(kexpc,cachef)
								if match:
									self.kcacheFiles.append(cachef)



	def k_xml(self,cffile):
		dom = minidom.parse(cffile)
		root = dom.documentElement
		f_cacheType = root.getElementsByTagName("cacheType")

		k_cacheFormat = f_cacheType[0].getAttribute('Format')
		k_cacheType   = f_cacheType[0].getAttribute('Type')							

		return k_cacheFormat,k_cacheType		

	def k_checkassfiles(self):

		kassdso=[]
		kassfilepath={}
		self.kexpo  = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply|\.asstoc)$'
		if cc.pluginInfo("mtoa",q=1,l=1):

			version = cc.pluginInfo("mtoa",q=1,v=1)
			self.mayaplugin_version.update({'Arnold':version})
			kassmeshs=cc.ls(type='aiStandIn')

			for kassmesh in kassmeshs:
				krassmesh=cc.listConnections(kassmesh,s=0,d=1)
				if krassmesh:
					assdsom=cc.getAttr(kassmesh+'.dso')

					if assdsom and not os.path.isabs(assdsom):
						assdsom=self.projectDir+assdsom

					assdsom=assdsom.replace('\\','/')

					assmesh_getpath=os.path.basename(assdsom)
					assmeshpath=os.path.dirname(assdsom)

					if assdsom :
						self.k_Nodedate('kassfiles',kassmesh,'.dso',assdsom)
						#####################################################

						if not assdsom in kassdso:
							kassdso.append(assdsom)
							if assmeshpath in kassfilepath:
								asspathfiles=kassfilepath[assmeshpath]
								krseqfile=self.k_filterassfile(assdsom,asspathfiles,kassmesh)
							else:
								asspathfiles=[]
								try:
									asspathfiles=os.listdir(assmeshpath)
								except WindowsError:
									pass

								krseqfile=self.k_filterassfile(assdsom,asspathfiles,kassmesh)
								k_update={assmeshpath:asspathfiles}
								kassfilepath.update(k_update)


	def k_filterassfile(self,assdsom,asspathfiles,kassmesh):

		assmesh_getpath=os.path.basename(assdsom)
		assmeshpath=os.path.dirname(assdsom)

		for asspathfile in asspathfiles:	
			pattern = re.search(self.kexpo, assmesh_getpath)

			if pattern:
				kwellnum=pattern.group(3)
				k_NO=len(kwellnum)
				kexpc = r'%s%s([0-9]{%d})([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply|\.asstoc)$' %(pattern.group(1),pattern.group(2),k_NO)
				kpattern = re.search(kexpc, asspathfile)
				if kpattern:
					kseq=kpattern.group()
					if assmeshpath[-2:]==':/':
						kseqfile=assmeshpath+kseq
					else:kseqfile=assmeshpath+'/'+kseq


					if not kseqfile in self.kassfiles:
						if os.path.exists(kseqfile):
							self.kassfiles.append(kseqfile)


			else:
				kseqfile=assdsom
				if not kseqfile in self.kassfiles:
					if os.path.exists(kseqfile):
						self.kassfiles.append(kseqfile)
					else:
						self.kerror_arnold.append(kassmesh)



if __name__ == "__main__":
	a=k_cachefinder()
	a.k_checkit()