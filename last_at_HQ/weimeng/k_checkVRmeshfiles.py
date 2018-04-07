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
	kassmeshfiles=[]
	kassdsofiles=[]
	kassfilepath={}
	kassmeshs=cc.ls(type='aiStandIn')
	for kassmesh in kassmeshs:
		krassmesh=cc.listConnections(kassmesh,s=0,d=1)
		#kcassmesh=cc.listConnections((kassmesh+'.transOp'),s=0,d=1)
		if krassmesh:
			assmesh=cc.getAttr(kassmesh+'.dso')
			print 'assmesh  '+str(assmesh)
			if not assmesh in kassdsofiles:
				assmeshpath=os.path.dirname(assmesh)
				print 'assmeshpath  '+str(assmeshpath)
				if assmeshpath in kassfilepath:
					pass
				else:
					asspathfiles=os.listdir(assmeshpath)
					print 'asspathfiles  '+str(asspathfiles)
					for asspathfile in asspathfiles:
						#找出井号
						kexpo = r'(.*?)([\._])([#]*)([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$'						
						pattern = re.search(kexpo, assmesh)
						if pattern:
							# 找出####
							kwellnum=pattern.group(3)
							print 'kwellnum  '+str(kwellnum)
							k_NO=len(kwellnum)
							kexpc = r'(.*?)([\._])([0-9]{%d})([\.]?)([#]*)(\.ass\.gz|\.ass|\.obj|\.ply)$' %k_NO
							pattern = re.search(kexpc, asspathfile)
							if pattern:
								kseq=pattern.group()
								print kseq

							k_update={assmeshpath:asspathfiles}
							kassfilepath.update(k_update)
							
							#print 'kseq  '+str(kseq)

	#print kassfilepath


	#print kassmeshfiles
	#print len(kassmeshfiles)


if __name__ == "__main__":
    k_checkVRmeshfiles()
    k_checkabcfiles()
    k_checkassfiles()