
#######################
##autor<<yanzhili>>----
##ToolName<<yzl_cam>>--
##buildTime<<2010.08>>-
##QQ<<342555216>>------
#######################

from maya.cmds import *
import string

#sel is joint.
window = window(title='yzl_Cam',w=620,h=500,mb=1,)
menu(l='help',tearOff=0)
menuItem(l='help')
columnLayout()

frameLayout(l='current_Cam',cll=1,cl=0,borderStyle='out')
columnLayout()
current_Cam=textFieldButtonGrp( label='current_Cam', text='select_Cam', buttonLabel='<<get In',bc='getInCam()' )
separator( height=10,w=390, style='in' )

rowColumnLayout(numberOfColumns=2,columnWidth=[(1, 410), (2, 25)] )
FSBG_cc1=floatSliderButtonGrp( label='Depth', field=True,min=0.100,max=10.0,fmn=0.1,fmx=35,v=1, buttonLabel='++', pre=3,symbolButtonDisplay=0, columnWidth=(5, 23) ,cc='cc1()',bc='jiajia("cc1")')                                            
button(l='--',c='jianjian("cc1")')
FSBG_cc2=floatSliderButtonGrp( label='left & Right', field=True,min=-5.00,max=5.0,fmn=-10.00,fmx=10.00, buttonLabel='++',pre=3, symbolButtonDisplay=0, columnWidth=(5, 23) ,cc='cc2()',bc='jiajia("cc2")')
button(l='--',c='jianjian("cc2")')
FSBG_cc3=floatSliderButtonGrp( label='up & Down',field=True,min=-5.00,max=5.0,fmn=-10.00,fmx=10.00,buttonLabel='++', pre=3,symbolButtonDisplay=0, columnWidth=(5, 23) ,cc='cc3()',bc='jiajia("cc3")')
button(l='--',c='jianjian("cc3")')
setParent('..')

thePre=floatSliderGrp( label='mins value', field=True,pre=3, minValue=0.001, maxValue=0.5, fieldMinValue=0.001, fieldMaxValue=1, value=0.02 )
textFieldButtonGrp( label='', text='reset Cam settings>>',ed=0, buttonLabel='resetting' ,bc='resetting()')


setParent( '..' )
setParent( '..' )
columnLayout()
frameLayout(l='all Cam resetting',cll=1,cl=1,borderStyle='etchedIn')
columnLayout()
button(l='all Cam resetting',h=25,w=250,c='allCamResetting()')
separator( height=10,w=390, style='in' )
setParent( '..' )
setParent( '..' )

setParent( '..' )
showWindow( window )

def jiajia(x):
	current_C=textFieldButtonGrp(current_Cam,q=1,text=1)
	cur_pre=floatSliderGrp(thePre,q=1,v=1)
	if x=='cc1':
		getCamPreScale=getAttr(current_C+'.postScale')
		floatSliderButtonGrp(FSBG_cc1,e=1,v=getCamPreScale+cur_pre)
		setAttr(current_C+'.postScale',getCamPreScale+cur_pre)
	if x=='cc2':
		getCamfilmTranslateH=getAttr(current_C+'.filmTranslateH')
		floatSliderButtonGrp(FSBG_cc2,e=1,v=getCamfilmTranslateH+cur_pre)
		setAttr(current_C+'.filmTranslateH',getCamfilmTranslateH+cur_pre)
	if x=='cc3':
		getCamfilmTranslateV=getAttr(current_C+'.filmTranslateV')
		floatSliderButtonGrp(FSBG_cc3,e=1,v=getCamfilmTranslateV+cur_pre)
		setAttr(current_C+'.filmTranslateV',getCamfilmTranslateV+cur_pre)

def jianjian(x):
	current_C=textFieldButtonGrp(current_Cam,q=1,text=1)
	cur_pre=floatSliderGrp(thePre,q=1,v=1)
	if x=='cc1':
		getCamPreScale=getAttr(current_C+'.postScale')
		floatSliderButtonGrp(FSBG_cc1,e=1,v=getCamPreScale-cur_pre)
		setAttr(current_C+'.postScale',getCamPreScale-cur_pre)
	if x=='cc2':
		getCamfilmTranslateH=getAttr(current_C+'.filmTranslateH')
		floatSliderButtonGrp(FSBG_cc2,e=1,v=getCamfilmTranslateH-cur_pre)
		setAttr(current_C+'.filmTranslateH',getCamfilmTranslateH-cur_pre)
	if x=='cc3':
		getCamfilmTranslateV=getAttr(current_C+'.filmTranslateV')
		floatSliderButtonGrp(FSBG_cc3,e=1,v=getCamfilmTranslateV-cur_pre)
		setAttr(current_C+'.filmTranslateV',getCamfilmTranslateV-cur_pre)

def getInCam():
	sels=ls(sl=1)
	current_C=getShape(sels[0])
	textFieldButtonGrp(current_Cam,e=1,text=getShape(sels[0]))
	getCamPreScale=getAttr(current_C+'.postScale')
	getCamfilmTranslateH=getAttr(current_C+'.filmTranslateH')
	getCamfilmTranslateV=getAttr(current_C+'.filmTranslateV')
	floatSliderButtonGrp(FSBG_cc1,e=1,v=getCamPreScale)
	floatSliderButtonGrp(FSBG_cc2,e=1,v=getCamfilmTranslateH)
	floatSliderButtonGrp(FSBG_cc3,e=1,v=getCamfilmTranslateV)

def cc1():
	current_C=textFieldButtonGrp(current_Cam,q=1,text=1)
	thecc1=floatSliderButtonGrp(FSBG_cc1,q=1,v=1)
	setAttr(current_C+'.postScale',thecc1)

def cc2():
	current_C=textFieldButtonGrp(current_Cam,q=1,text=1)
	thecc2=floatSliderButtonGrp(FSBG_cc2,q=1,v=1)
	setAttr(current_C+'.filmTranslateH',thecc2)

def cc3():
	current_C=textFieldButtonGrp(current_Cam,q=1,text=1)
	thecc3=floatSliderButtonGrp(FSBG_cc3,q=1,v=1)
	setAttr(current_C+'.filmTranslateV',thecc3)

def getShape(x):
    if("transform"==nodeType(x)):
        shape=listRelatives(x,fullPath=0,shapes=1)
        return shape[0]
    else:
        return None

def resetting():
	current_C=textFieldButtonGrp(current_Cam,q=1,text=1)
	floatSliderButtonGrp(FSBG_cc1,e=1,v=1)
	floatSliderButtonGrp(FSBG_cc2,e=1,v=0)
	floatSliderButtonGrp(FSBG_cc3,e=1,v=0)
	setAttr(current_C+'.postScale',1)
	setAttr(current_C+'.filmTranslateH',0)
	setAttr(current_C+'.filmTranslateV',0)

def allCamResetting():
	allCam=listCameras()
	for i in allCam:
		currCamShape=getShape(i)
		setAttr(currCamShape+'.postScale',1)
		setAttr(currCamShape+'.filmTranslateH',0)
		setAttr(currCamShape+'.filmTranslateV',0)
	
	floatSliderButtonGrp(FSBG_cc1,e=1,v=1)
	floatSliderButtonGrp(FSBG_cc2,e=1,v=0)
	floatSliderButtonGrp(FSBG_cc3,e=1,v=0)
########----end!----#############



