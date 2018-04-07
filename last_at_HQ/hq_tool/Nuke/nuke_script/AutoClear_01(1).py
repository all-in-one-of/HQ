import os
import nuke,nukescripts

def main():
	p=nuke.Panel('Node')
	p.addEnumerationPulldown('Node :','jumu_viewer_cg jumu_viewer_shipai')
	s=p.show()
	pv=p.value('Node :')
	if s==1:
		a=nuke.selectedNodes()
		c={}
		b=[]
		x=-1
		for i in a:
			i.setSelected(False)
		for i in a:
			dictname=i.name()
			basename=os.path.basename(i['file'].value())
			file=basename[:-4]
			if basename=='Thumbs.db':
				i.setSelected(True)
				nukescripts.node_delete(popupOnError=True)
			else:
				c[file]=dictname
				b.append(file)
				b.sort()

		for v in b:
			t=v[:-5]
			if '1L' in v:
				n='1L'			
			elif '2L' in v:
				n='2L'
			elif '3L' in v:
				n='3L'
			if '1L' in v or '2L' in v or '3L' in v:
				v2=v.replace(n,'2L')
				v3=v.replace(n,'3L')
				v4=v.replace(n,'1R')
				v5=v.replace(n,'2R')
				v6=v.replace(n,'3R')
				if v4 in b:
					x+=1
					node1=nuke.toNode('%s' % c[v])
					node1.setXYpos(100,100+x*400)
					if v2 in b:
						node2=nuke.toNode('%s' % c[v2])
						node2.setXYpos(200,100+x*400)
						
					if v3 in b:
						node3=nuke.toNode('%s' % c[v3])
						node3.setXYpos(300,100+x*400)
						
					if v4 in b:
						node4=nuke.toNode('%s' % c[v4])
						node4.setXYpos(400,100+x*400)
				
					if v5 in b:
						node5=nuke.toNode('%s' % c[v5])
						node5.setXYpos(500,100+x*400)
				
					if v6 in b:
						node6=nuke.toNode('%s' % c[v6])
						node6.setXYpos(600,100+x*400)
				
					nodel=nuke.createNode("%s" % pv,inpanel=False)
					nodel.setXYpos(200,250+x*400)
					nodel.setSelected(False)
					noder=nuke.createNode("%s" % pv,inpanel=False)
					noder.setXYpos(500,250+x*400)
					nodel.setSelected(False)
					nodejv=nuke.createNode("JoinViews",inpanel=False)
					nodejv.setXYpos(350,300+x*400)
					nodel.setSelected(False)
					backnode=nuke.createNode("BackdropNode",inpanel=False)
					backnode.setXYpos(900,20+x*400)
					nodel.setSelected(False)
					nodel.setInput(2,node1)
					if v2 in b:
						nodel.setInput(1,node2)
						b.remove(v2)
					if v3 in b:
						nodel.setInput(0,node3)
						b.remove(v3)
					if v4 in b:
						noder.setInput(2,node4)
						b.remove(v4)
					if v5 in b:
						noder.setInput(1,node5)
						b.remove(v5)
					if v6 in b:
						noder.setInput(0,node6)
						b.remove(v6)
					nodejv.setInput(0,nodel)
					nodejv.setInput(1,noder)
					backnode['bdwidth'].setValue(600)
					backnode['bdheight'].setValue(310)
					backnode.setXYpos(90,20+x*400)
					backnode['label'].setValue(t)
					backnode['note_font'].setValue("Helvetica Bold")
					backnode['note_font_size'].setValue(30)