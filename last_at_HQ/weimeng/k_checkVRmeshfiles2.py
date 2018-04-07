import maya.cmds as cc
import os

def k_checkVRmeshfiles():
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


def k_checkabcfiles():
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

def k_checkassfiles():
	#总缓存文件
	kassfiles=[]
	#maya节点返回的路径
	kassdso=[]
	#记录文件夹内里的文件，避免重复对网络进行获取
	kassfilepath={}

	kexpo  = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'
	kexpo2 = r'(.*?)([\._])([0-9#]*)([\.]?)([0-9#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'

	kassmeshs=cc.ls(type='aiStandIn')
	for kassmesh in kassmeshs:
		krassmesh=cc.listConnections(kassmesh,s=0,d=1)
		#kcassmesh=cc.listConnections((kassmesh+'.transOp'),s=0,d=1)
		if krassmesh:
			print 'kassmesh  '+str(kassmesh)
			assdso=cc.getAttr(kassmesh+'.dso')
			assmesh_getpath=os.path.basename(assdso)
			print 'assdso  '+str(assdso)
			assmeshpath=os.path.dirname(assdso)
			#print 'assmeshpath  '+str(assmeshpath)

			if not assdso in kassdso:
				kassdso.append(assdso)

				if assmeshpath in kassfilepath:
					#k_filterseq=[]
					#asspathfiles=os.listdir(assmeshpath)
					asspathfiles=kassfilepath[assmeshpath]
					#print 'asspathfiles  '+str(asspathfiles)
					for asspathfile in asspathfiles:
						#找出井号
						#print 'asspathfile____  '+str(asspathfile)			
						pattern = re.search(kexpo, assmesh_getpath)
						pattern2 = re.search(kexpo2, assmesh_getpath)

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
								if not kseqfile in kassfiles:
									if os.path.exists(kseqfile):
										kassfiles.append(kseqfile)
										print kseqfile

						elif pattern2:
							kseqfile=assdso
							if not kseqfile in kassfiles:
								if os.path.exists(kseqfile):
									kassfiles.append(kseqfile)
									print kseqfile

						else:
							kseqfile=assdso
							if not kseqfile in kassfiles:
								if os.path.exists(kseqfile):
									kassfiles.append(kseqfile)
									print kseqfile
				else:
					#k_filterseq=[]
					asspathfiles=os.listdir(assmeshpath)
					#print 'asspathfiles  '+str(asspathfiles)
					for asspathfile in asspathfiles:
						#找出井号
						#kexpo = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'						
						pattern = re.search(kexpo, assmesh_getpath)
						pattern2 = re.search(kexpo2, assmesh_getpath)
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
								if not kseqfile in kassfiles:
									if os.path.exists(kseqfile):
										kassfiles.append(kseqfile)
										print kseqfile

						elif pattern2:
							kseqfile=assdso
							if not kseqfile in kassfiles:
								if os.path.exists(kseqfile):
									kassfiles.append(kseqfile)
									print kseqfile


						else:
							kseqfile=assdso
							if not kseqfile in kassfiles:
								if os.path.exists(kseqfile):
									kassfiles.append(kseqfile)
									print kseqfile
									
					k_update={assmeshpath:asspathfiles}
					kassfilepath.update(k_update)
							
							#print 'kseq  '+str(kseq)

	for x in kassfiles:
		print x

	#print kassdso
	#print kassfilepath


if __name__ == "__main__":
    k_checkVRmeshfiles()
    k_checkabcfiles()
    k_checkassfiles()