import os
import nukescripts
import nuke
def main():
	class ShapePanel(nukescripts.PythonPanel):
			def __init__(self, node):
					nukescripts.PythonPanel.__init__(self, 'CustomUI')
					self.rpNode = node
					self.paragraph = nuke.String_Knob('paragraph', 'Paragraph','4' )
					self.write = nuke.String_Knob('write', 'Write','1')
					self.thread = nuke.String_Knob('thread', 'Thread','2')
					for k in (self.paragraph, self.write, self.thread):
							self.addKnob(k)

	p = ShapePanel('CustomUI')
	if p.showModalDialog():

			x=int(p.paragraph.value())
			y=p.write.value()
			z=int(p.thread.value())
			a=int(nuke.root()["first_frame"].value()-1)
			b=int(nuke.root()["last_frame"].value()+1)
			c=(b-a)//x
			d=range(a,b,c)
			pname=nuke.root().name()
			for e in range(0,x) :
					name=os.path.basename(nuke.root().name()).split('.')[0]
					name=name+'_'+str(e)
					Ropen=open('D:/Bat/%s.bat' % name,'w')
					print name
					if  e==x-1 :
							Ropen.write('\"C:/Program Files/Nuke9.0v1/Nuke9.0.exe\" --nukex -i -F %s-%sx%s -m %s -x %s&&exit' %(d[e]+1,b-1,y,z,pname))
							  
					else :
							Ropen.write('\"C:/Program Files/Nuke9.0v1/Nuke9.0.exe\" --nukex -i -F %s-%sx%s -m %s -x %s&&exit' %(d[e]+1,d[e+1],y,z,pname))

					Ropen.close()
			Bopen=open('D:/Bat/Batch.bat','w')
			for i in range(0,x) :
					name=os.path.basename(nuke.root().name()).split('.')[0]
					name=name+'_'+str(i)
					Bopen.write('start D:/Bat/%s\n' % name)
			Bopen.close()
			path='D:/Bat/Batch.bat'
			os.system(path)
	else:
			pass