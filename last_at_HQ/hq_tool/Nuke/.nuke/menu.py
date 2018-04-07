# -*- coding: UTF-8 -*- 

import os
import nuke
import re
import getpass
import time,render
from shutil import copy
from socket import *
import threading


SD = '1280 720 SD'
nuke.addFormat(SD)
DN = '2248 1264 DN'
nuke.addFormat(DN)

user=getpass.getuser()

if user=='D-018':

	def udpser():

		udpserver=socket(AF_INET,SOCK_DGRAM)

		try:
			udpserver.bind(('',8000))
			
			print 'udpserver start'
			udpserver.sendto('%s~~online' % user,('192.168.60.81',8000))
			while True :
				data,addr = udpserver.recvfrom(1024)
				print data,addr
				
				os.system('%s' %data.split('~~')[1])
				print 'render completed'
		except:
			pass
	threading.Thread(None,udpser).start()

def customBackgroundRender():
    class ShapePanel(nukescripts.PythonPanel):
            def __init__(self, node):
                    nukescripts.PythonPanel.__init__(self, 'CustomUI')
                    self.rpNode = node
                    self.paragraph = nuke.String_Knob('paragraph', 'Paragraph','%s' %5)
                    self.memory = nuke.String_Knob('memory', 'Memory','%s' %4096)
                    self.thread = nuke.String_Knob('thread', 'Thread','2')
                    for k in (self.paragraph, self.memory, self.thread):
                            self.addKnob(k)
    
    p = ShapePanel('CustomUI')
    if p.showModalDialog():
    
            x=int(p.paragraph.value())
            y=p.memory.value()
            z=int(p.thread.value())
            a=int(nuke.root()["first_frame"].value()-1)
            b=int(nuke.root()["last_frame"].value()+1)
            c=(b-a)//x
            d=range(a,b,c)            
            
            for e in range(0,x) :
                    write = nuke.selectedNode()
                    wviews=write['views'].value().split(' ')
                    
                    if  e==x-1 :
                            nuke.executeBackgroundNuke(nuke.EXE_PATH, [write], nuke.FrameRanges('%s-%s' %(d[e]+1,b-1)), wviews, {'maxThreads':z, 
'maxCache':'%sM' %y},continueOnError= True)    
                            
                    else :
                            nuke.executeBackgroundNuke(nuke.EXE_PATH, [write], nuke.FrameRanges('%s-%s' %(d[e]+1,d[e+1])), wviews, 
{'maxThreads':z, 'maxCache':'%sM' %y},continueOnError= True)
    else:
            pass

			



                



def customKillNukeProcess():
		if nuke.ask("该功能将会强制关闭所有nuke进程，请注意保存！\n\n'Yes' 继续，'No' 离开"):
				os.system('taskkill /f /im Nuke8.0.exe')
		else:
				pass
				
def Qrender():
	render.main()
	
def currentFrameCache():
	def huancun():
		readNodes=nuke.allNodes('Read')
		cframe=nuke.frame()
		cachepath='D:/NUKE_TEMP_DIR/'
		print '开始缓存......'
		for i in readNodes:
			i['cacheLocal'].setValue(0)
			filev=i['file'].value()
			files=filev.split('.')
			framestart=i['first'].value()
			if len(files)==2:
				filepath=files[0][:-4]+'%04d' % cframe+'.'+files[-1]
			if len(files)==3:
				filepath=files[0]+'.'+'%04d' % (cframe+framestart-100)+'.'+files[-1]
			copypath=cachepath+os.path.dirname(filepath.replace(':','_'))

			if not os.path.exists(copypath) :
				os.makedirs(copypath)
			try:
				copy('%s' % filepath ,'%s' % copypath )
				print '%s:缓存完成' % filepath
			except:
				pass
	threading.Thread(None,huancun).start()
	
def cacheLocal():
	a=nuke.allNodes('Read')
	for i in a:
		i['cacheLocal'].setValue(0)
		
def upload():
	node=nuke.allNodes('Read')
	pname=nuke.root().name()
	lenname=os.path.basename(pname)
	len=lenname.split('_')
	path='N:/Dragonnest/Sequence%s/%s_%s/Comp_Assets/Scene_Assets/upload/' %(len[0][3:],len[0],len[1])

	for i in node:
		file=i['file'].value()
		if  file.split(':')[0]!='N' and file.split(':')[0]!='B':
			spl=file.split('.')[-2][-4:]
			firstframe=int(i['first'].value())
			lastframe=int(i['last'].value())
			filename=os.path.basename(file)
			if not os.path.exists(path) :
				os.makedirs(path)
			if spl=='####' :
				for t in range(firstframe,lastframe+1):
					frame='%04d' % t
					filepath=file.replace('####',frame)
					copypath=path+filename.replace('####',frame)
					copy(filepath,copypath)
					i['proxy'].setValue(file)
					i['file'].setValue(path+filename)
			elif spl=='%04d':
				for t in range(firstframe,lastframe+1):
					frame='%04d' % t
					filepath=file.replace('%04d',frame)
					copypath=path+filename.replace('%04d',frame)
					copy(filepath,copypath)
					i['proxy'].setValue(file)
					i['file'].setValue(path+filename)
			else :
				
				copypath=path+filename
				copy(file,copypath)
				i['proxy'].setValue(file)
				i['file'].setValue(path+filename)
				
def roto_stereo():
	
	class RotoViewsPanel(nukescripts.PythonPanel):

		def __init__(self):

			import nuke.rotopaint

			super(RotoViewsPanel,self).__init__('Change views on RotoPaint Nodes...' )

			self.changeKnob = nuke.Enumeration_Knob('change', 'change', ['all RotoPaint nodes', 'selected RotoPaint nodes'])

			self.addKnob(self.changeKnob)

			self.viewsKnob = nuke.MultiView_Knob('views')

			self.addKnob(self.viewsKnob)

			self.viewsKnob.setValue((' ').join(nuke.views()))

			self.okButton = nuke.Script_Knob( "Change Views" )

			self.addKnob( self.okButton )

			self.okButton.setFlag( nuke.STARTLINE )

			self.cancelButton = nuke.Script_Knob( "Cancel" )

			self.addKnob( self.cancelButton )
	
		def knobChangedCallback(self, knob):

			self.knobChanged(knob)

			if knob == self.okButton:

				self.finishModalDialog( True )	 

				if self.changeKnob.value() == 'all RotoPaint nodes':

					self.__nodes = nuke.allNodes('RotoPaint')

					self.__nodes.extend(nuke.allNodes('Roto'))

				elif self.changeKnob.value() == 'selected RotoPaint nodes':

					self.__nodes = nuke.selectedNodes('RotoPaint')

					self.__nodes.extend(nuke.selectedNodes('Roto'))  

				self.__views =  self.viewsKnob.value().split(' ')
	 
				self.changeViews(self.__nodes, self.__views)
	 
			elif knob == self.cancelButton:

				self.finishModalDialog( False )
	 
		def getShapes(self, layer):

			shapes = []

			for element in layer:

				if isinstance(element, nuke.rotopaint.Layer):

					shapes.extend(self.getShapes(element))

				elif isinstance(element, nuke.rotopaint.Shape) or isinstance(element, nuke.rotopaint.Stroke):

					shapes.append(element)

			return shapes	 

		def changeViews(self, nodes, views):

			for n in nodes:

				print n.name()

				k = n['curves']

				shapes = self.getShapes(k.rootLayer)

				for s in shapes:

					attrs = s.getAttributes()
					# reset the number of views attribute

					if 'nv' in attrs:

					  attrs.remove('nv')

					  attrs.add('nv', len(views))

					# delete any previous view attributes

					count = 1

					while ('view%s' % count) in attrs:              

					  attrs.remove('view%s'% count)

					  count +=1

					# handle no selected views
					if views == [''] :
					  attrs.add('view1', 0.0)
					# handle any other number of views

					else:                    
						count = 1
					for view in views:
					   index = float(nuke.views().index(view)+1)
					   attrs.add('view%s'% count, index)
					   count +=1
				k.changed()
	p = RotoViewsPanel().showModalDialog()
	
def vb_disable():
	a=nuke.allNodes('VectorBlur')
	b=int(nuke.root()['last_frame'].value())
	for i in a:
		i['disable'].setExpression('t==%s' % b)


 


nuke.menu( 'Nuke' ).addCommand( 'CustomTools/BackgroundRender       ', customBackgroundRender )
nuke.menu( 'Nuke' ).addCommand( 'CustomTools/FrontgroundRender       ', Qrender )
nuke.menu( 'Nuke' ).addCommand( 'CustomTools/KillNukeProcess   ', customKillNukeProcess )
nuke.menu( 'Nuke' ).addCommand( 'CustomTools/cache  ', currentFrameCache )
nuke.menu( 'Nuke' ).addCommand( 'CustomTools/Footage Localise  ', cacheLocal,'ctrl+l' )
nuke.menu( 'Nuke' ).addCommand( 'CustomTools/upload  ', upload)
nuke.menu( 'Nuke' ).addCommand( 'CustomTools/roto_stereo  ', roto_stereo)













