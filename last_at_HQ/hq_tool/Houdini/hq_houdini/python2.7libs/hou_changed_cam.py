# -*- coding: utf-8 -*-
#选中全部相机。或相机组，在Python Source Editor 中运行此脚本


import hou

def change_cam_attr(attr,value):
    '''
    change_cam_attr(attr,value)
    '''
    camlist=[]
    cam_nodes_f=[]
    geonodelist = hou.selectedNodes()

    
    for xs in geonodelist:
    
        camlist += xs.allSubChildren()
        
    camlist+=geonodelist
    cam_nodes_f+= [node for node in camlist if 'cam'==node.type().name()]
    if len(cam_nodes_f)<1:
		print 'please select least one camera'
    for caml in cam_nodes_f:

        caml.parm(str(attr)).set(str(value))

        print caml.path(),'  ',attr,'=====',caml.parm(str(attr)).eval()
def show_ui():
	inp=hou.ui.readMultiInput('输入分辨率', ('cam_resx','cam_resy','shutter Time(0.5)'),  buttons=('OK',), title='set_cam_res' )
	inp2=inp[1]

	if inp2[0]!='' and inp2[0]!='':
		change_cam_attr('resx',inp2[0])
		change_cam_attr('resy',inp2[1])
	else:
		print 'no input cam_res'
	if inp2[2]!='':
		change_cam_attr('shutter',inp2[2])
	else:
		print 'no input cam_res'