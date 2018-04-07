# -*- coding: utf-8 -*-
from PySide import QtCore,QtGui
import os
import hou
from os.path import join,getsize 
import sys,time,datetime
import glob
reload(sys)
sys.setdefaultencoding( "utf-8" ) 
path='//l_linzhenkun/E/l_houdini/python2.7lib/'
if not path in sys.path:
        sys.path.append(path)
def show_win():
	import Cache_Manager_ui
	reload(Cache_Manager_ui)
	class myWindowClass(Cache_Manager_ui.Ui_MainWindow):
		def __init__(self):
				super(Cache_Manager_ui.Ui_MainWindow, self).__init__()
				self.item_c=[]
				self.item_node=[]
				self.item_path=[]
				self.exist_s=0

		def setupUi(self,MainWindow):
				Cache_Manager_ui.Ui_MainWindow.setupUi(self, MainWindow)
				self.pushButton2.clicked.connect(self.set_replace)
				self.pushButton_rf.clicked.connect(self.search_file)
				self.pushButton.clicked.connect(self.set_path)
				self.lineEdit1_3.textChanged.connect(self.set_hidden)
				self.comboBox.currentIndexChanged.connect(self.set_hidden)
				self.pushButton_m2.clicked.connect(self.set_mis_report)
				self.pushButton_m3.clicked.connect(self.set_mis_no_geo)
				self.pushButton_setcolor.clicked.connect(self.set_all_color)
				self.pushButton_help.clicked.connect(self.dis_help)
				self.pushButton_jump.clicked.connect(self.jump_to)
				self.pushButton_set_hip.clicked.connect(self.set_hip_path)
				self.pb_countsize.clicked.connect(self.count_cache_size)
		def jump_to(self):
			if  str(hou.updateModeSetting())=='updateMode.Manual':
				pass
			else:
				hou.ui.displayMessage('设置 updateMode 为 Manual', buttons=('确认',),  title='')
				hou.setUpdateMode(hou.updateMode.Manual)
			sl=self.tableWidget.selectedIndexes()

			try:
				rs=sl[0].row()
				node_path=self.tableWidget.item(rs, 2).text()
				hou.node(node_path).setCurrent(1,1)
			except:
				pass
		def set_hip_path(self):
			rownum=self.tableWidget.rowCount()
			h_path=hou.houdiniPath()


			for r in range(0,rownum):
				ep=self.tableWidget.item(r, 3).text()
				try:
					if ep.find('$HIP')==-1:
						k=ep.replace(str(h_path[0]),'$HIP')
						if k!=ep:
							print 'set',self.tableWidget.item(r, 2).text(),'             ',k
							self.tableWidget.item(r, 4).setText(QtGui.QApplication.translate("MainWindow", str(k), None, 
	QtGui.QApplication.UnicodeUTF8))

				except:
					print 'Error:',self.tableWidget.item(r, 2).text()
				
			
			
		def dis_help(self):
			hou.ui.displayMessage("1、<刷新>                 可以获取当前所有缓存节点的最新信息\n2、<替换>                 可以替换所选择的（多选）<当前路径里>的字符串，并在<修改预览>里预览结果\n3、<过滤显示>           显示可以过滤显示匹配所输入的字符的行，匹配模式可以按照不同规则匹配字符\n4、                           点击列表栏上方的类型可以改变各类型排列方式,双击可复制\n5、<应用修改>           会按照列表里的修改预览修改缓存路径\n6、<set Missing file>  可以更改全部节点的模式\n7、<设置节点颜色>      会按照特效规范修改 缓存、动力学节点，编辑k帧的节点、输入输出节点的颜色。", buttons=('OK',),title='help') 
		def set_path(self):
			rownum=self.tableWidget.rowCount()

			for r in range(0,rownum):
				
				if self.tableWidget.item(r, 3).text()!=self.tableWidget.item(r, 4).text() and self.tableWidget.item(r, 4).text()!='' and self.tableWidget.item(r, 0).text().find('exist')==-1:
					if self.tableWidget.item(r, 1).text()=='alembic' or  self.tableWidget.item(r, 1).text()=='alembicarchive':
						ll=hou.parm(self.tableWidget.item(r, 2).text()+'/fileName')
					else:
						ll=hou.parm(self.tableWidget.item(r, 2).text()+'/file')
					
					try:
						ll.set(self.tableWidget.item(r, 4).text())
					except:
						print 'Error:'+str(ll)+'possible  locked '
					print 'set  '+str(ll) +' =  '+self.tableWidget.item(r, 4).text()
				else:
					pass
					
  

			
		def set_replace(self):

			input1=self.lineEdit1.text()
			input2=self.lineEdit1_2.text()
			sl=self.tableWidget.selectedIndexes()
			t=[]
			for s in sl :
				t.append(s.row())
			sln=list(set(t))

			for sx in sln:
				if self.tableWidget.isRowHidden(sx)!=1:
					if input1 in self.tableWidget.item(sx, 3).text():
						ll=self.tableWidget.item(sx, 3).text().replace(input1,input2)
					
						self.tableWidget.item(sx, 4).setText(QtGui.QApplication.translate("MainWindow", str(ll), None, 
	QtGui.QApplication.UnicodeUTF8))


		def set_hidden(self):
			input3=self.lineEdit1_3.text()
			input4=self.comboBox.currentIndex()
			zd={0:1,1:0,2:5,3:2,4:3}
			cs=self.tableWidget.rowCount()       
			
			sisel=self.tableWidget.findItems(input3,zd[input4])

			if len(input3):

				for cl in range(cs):
					self.tableWidget.setRowHidden(cl,1)
				
				for sl in sisel:
					self.tableWidget.setRowHidden((sl.row()),0)
			else:
				for cl in range(cs):
					self.tableWidget.setRowHidden(cl,0)
   
		def get_files_size(self,path_z):


			pa2=(path_z.split('/'))
			pa3=pa2[len(pa2)-1].split('.')
			pa3[1]='*'
			size=0L
			ll=glob.glob(os.path.dirname(path_z)+'/'+'.'.join(pa3))
			if ll!=[]:
				for l in ll:
					size+= getsize(l)
					final_size= float(size)/1024/1024
			else:
					final_size=0L
			return final_size
			

		def count_cache_size(self):
		
			start=time.time()
			print 'counting caches.....................'
			rownum=self.tableWidget.rowCount()
			pb=0.0
			z_size=0
			qs=0
			for r in range(0,rownum):
				if self.tableWidget.item(r, 0).text()=='True':
					pat=self.tableWidget.item(r, 5).text()

					gsize=self.get_files_size(pat)
					if len(str(int(gsize)))>3:
						str_size=str ('%-7.2f'%(gsize/1024))+' GB'
					else:
						str_size=str ('%-7.2f'% gsize)+' MB'

					self.tableWidget.item(r, 6).setText(QtGui.QApplication.translate("MainWindow", str_size, None, QtGui.QApplication.UnicodeUTF8))
					pb+=100.0/float(rownum-self.exist_s-1)
					if int(float(pb)%10)==0:
						if abs(pb-qs)>3:
							print 'counting caches : ',int(pb),'%'
						qs=pb


					z_size+=gsize
				else:
					continue
			if len(str(int(z_size)))>3:
				str_z_size=str ('%7.2f'%(z_size/1024))+' GB'
			else:
				str_z_size=str ('%6.2f'% z_size)+' MB'
			for r in range(0,rownum):
				if self.tableWidget.item(r, 0).text().find('exist')>-1:
					self.creat_item(r,6,str_z_size)
					break
			print 'cost time:','%.3f'%(time.time()-start),' s'

		def q_exist_file(self,path_e):
			try:
				pa2=(path_e.split('/'))
				pa3=pa2[len(pa2)-1].split('.')
				pa3[1]='*'
				
				jj=glob.iglob(os.path.dirname(path_e)+'/'+'.'.join(pa3))
				
				je=[]

				fe='None'
				for j in jj:
					je.append(j)
					if je!=[]:
						fe=je[0]
					break 
			except:
				fe='None'

			return fe

		def search_file(self):
			start=time.time()
			dialog.setupUi(myWindow)
			self.tableWidget.clearContents()


			  
			nodelist=hou.node('/obj').allSubChildren()


	  
			file_nodes_np = []
			file_nodes_all=[]



			file_nodes= [node for node in nodelist if 'file'==node.type().name()  and node.parm('file').unexpandedString().find('`chs')==-1 and node.parm('file').unexpandedString().find('pointlight.bgeo')==-1 and  node.name()!='file_mode' and node.name()!='read_back' and node.parent().name()!='instance1' and node.parent().type().name().find('cam') ]
			filecache_nodes= [node for node in nodelist if 'filecache'==node.type().name()] 
			dopio_nodes= [node for node in nodelist if 'dopio'==node.type().name()] 
			alembic_nodes= [node for node in nodelist if 'alembic'==node.type().name() and node.parent().type().name()!='ropnet'] 
			alembicarchive_nodes= [node for node in nodelist if 'alembicarchive'==node.type().name()] 
			file_nodes_all=file_nodes+filecache_nodes+dopio_nodes+alembic_nodes+alembicarchive_nodes

			index=1

			self.tableWidget.setRowCount(len(file_nodes_all)+1)
			zs=0
			self.exist_s=0
			path_w=0
			f_time=''
			for file in file_nodes_all:
				if  file.type().name()=='alembic' or  file.type().name()=='alembicarchive':
					filepar='fileName'
					misf='missingfile'
				else:
					filepar='file'
					misf='missingframe'
				try:
					fpn = file.parm(filepar).unexpandedString()

					fpjd = file.parm(filepar).eval()
					


				except:
					print 'erro',file.path()
					continue
				if fpjd.find('//')==-1:

					fee =os.path.exists(fpjd)
					if fee==True:
						fe=True
						e_path=fpjd
					elif self.q_exist_file(fpjd)!='None':

						
						e_path=self.q_exist_file(fpjd)


						fe=True			
					else:
						fe=''

				else:
					fe='no sure'
				if fe==True:
					try:
						st=datetime.datetime.fromtimestamp(os.path.getmtime(e_path))
						f_time=st.strftime('%Y/%m/%d %H:%M:%S')
					except:
						print file.path(),e_path
				else:
					s=''
					f_time=''

					self.exist_s+=1






				try:
					mis_str={0:'Report Error',1:'No Geometry'}

					mis_value = mis_str[file.parm(misf).eval()]
				except:
					mis_value=''
				if '$HIP' not in fpn :
					path_w+=1

				self.creat_item(index,0,str(fe))
				self.creat_item(index,1,file.type().name())
				self.creat_item(index,2,file.path())
				self.creat_item(index,3,fpn)
				self.creat_item(index,4,'')
				self.creat_item(index,5,fpjd)
				self.creat_item(index,6,'')
				self.creat_item(index,7,f_time)
				self.creat_item(index,8,mis_value)
				index+=1
			self.creat_item(0,0,str(self.exist_s)+' no exist')
			self.creat_item(0,1,'')
			self.creat_item(0,2,'')
			self.creat_item(0,3,str(path_w)+'个路径不是相对路径')
			self.creat_item(0,4,'')
			self.creat_item(0,5,'缓存总大小')
			self.creat_item(0,6,'')	
			self.creat_item(0,7,'')
			self.creat_item(0,8,'')
			print 'cost time:','%.3f'%(time.time()-start),' s'

		def creat_item(self,vi,hi,item_text):
			item = QtGui.QTableWidgetItem()
			self.tableWidget.setItem(vi, hi, item)
			self.tableWidget.item(vi, hi).setText(QtGui.QApplication.translate("MainWindow", item_text, None, QtGui.QApplication.UnicodeUTF8))

		def closeEvent(self, event):
			self.setParent(None)

		def set_misfile(self,k):
			nodelist=hou.node('/obj').allSubChildren()
			file_nodes= [node for node in nodelist if 'file'==node.type().name() and   node.name()!='file_mode' and 
		node.name()!='read_back' and node.parent().name()!='instance1' and node.parent().name()!='ipr_camera']
			filecache_nodes= [node for node in nodelist if 'filecache'==node.type().name()] 
			dopio_nodes= [node for node in nodelist if 'dopio'==node.type().name()] 
			alembic_nodes= [node for node in nodelist if 'alembic'==node.type().name()] 
			file_nodes_all=file_nodes+filecache_nodes+dopio_nodes+alembic_nodes   
			for node in file_nodes_all:
				if node.type().name()=='alembic':
					ll=node.parm('missingfile')
				else:
					ll=node.parm('missingframe')
				try:
					ll.set(k)
				except:
					print 'Error:'+str(node)+'possible inclode locked assets'
			
		def set_mis_report(self):
			self.set_misfile(0)
			print 'set all Missing file mode to Report Error'

			
		def set_mis_no_geo(self):
			self.set_misfile(1)
			print 'set all Missing file mode to No geometry' 
			

			
		def set_node_color(self,input_node,node_type):
			d={}
			nodes=input_node
			
			c1=hou.Color()
			c1.setRGB((1,0.4,0.4))
			d['cache']=c1
			
			c2=hou.Color()
			c2.setRGB((0,0.796,1))
			d['dop']=c2
			
			c3=hou.Color()
			c3.setRGB((1,0.796,0))
			d['out']=c3
			
			c4=hou.Color()
			c4.setRGB((0.867,0,0))
			d['edit']=c4
			
			c5=hou.Color()
			c5.setRGB((0.399,1,0.399))
			d['other']=5
			
			c6=hou.Color()
			c6.setRGB((0.796,0.796,1))
			d['render']=c6
			
			for node in nodes:
				try:
					node.setColor(d[node_type])
				except:
					print 'Error:'+str(node)+'possible inclode locked assets'
				
				
		def set_all_color(self):      
			nodelist=hou.node('/obj').allSubChildren()
			file_nodes= [node for node in nodelist if 'file'==node.type().name() and   node.name()!='file_mode' and 
		node.name()!='read_back' and node.parent().name()!='instance1' and node.parent().name()!='ipr_camera']
			filecache_nodes= [node for node in nodelist if 'filecache'==node.type().name()] 
			dopio_nodes= [node for node in nodelist if 'dopio'==node.type().name()] 
			alembic_nodes= [node for node in nodelist if 'alembic'==node.type().name()] 
			file_nodes_all=file_nodes+filecache_nodes+dopio_nodes+alembic_nodes    
			self.set_node_color(file_nodes_all,'cache')
			
			dop_nodes= [node for node in nodelist if node.type().name().find('dop')>-1 and 'dopio'!=node.type().name()  ]
			self.set_node_color(dop_nodes,'dop')
		
			
			out_nodes= [node for node in nodelist if 'object_merge'==node.type().name() or 'null'==node.type().name()  ]
			self.set_node_color(out_nodes,'out')
		
			
			edit_nodes= [node for node in nodelist if node.type().name().find('paint')>-1 or 'group'==node.type().name()  or 
		'drawcurve'==node.type().name()]
			xform_nodes= [node for node in nodelist if 'xform'==node.type().name()  and node.parent().name()!='ipr_camera']   
		 
			k_node=[]
			for n in xform_nodes:
				for p in n.parms():
					if p.keyframes()!=():
						k_node.append(n)    
			all_edit_nodes=edit_nodes+k_node
			self.set_node_color(all_edit_nodes,'edit')
			print "set nodes color succeed"
			

	myWindow=QtGui.QMainWindow()
	myWindow.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

	dialog = myWindowClass()


	dialog.setupUi(myWindow)


	myWindow.show()
