#Author: yanzhili
#email: piqyzl@163.com
#QQ:342555216
#LastUpdate:2010.09.20
from maya.cmds import *
import maya.mel
import string

mywindow='footStep'
if window(mywindow,exists=True):
	 deleteUI(mywindow)
mywindow=window(title="yzl-footStep", iconName='footStep', widthHeight=(100, 55),mb=1 )
menu(l='help',tearOff=0)
menuItem(l='help')
columnLayout( adjustableColumn=True )
frameLayout(l='footStep',cll=1,cl=0,borderStyle='out')
columnLayout()
parentObject=textFieldButtonGrp( label='get Frame', buttonLabel='<<get',columnAlign3 = ["right","right","right"],cw3 = [80,100,100],bc='getFrame()' )
button(w=180,l="do>>footStep",c="doFootStep()")
separator( height=10,w=390, style='in' )
setParent( '..' )
setParent( '..' )
setParent( '..' )
showWindow(mywindow)

def getFrame():
	currFrame=currentTime( query=True )
	textFieldButtonGrp(parentObject,e=1,text=currFrame)

def doFootStep():
	sels=ls(sl=1)[0]
	aPlayBackSlider= maya.mel.eval('$tmpVar=$gPlayBackSlider')
	rangeArr=timeControl(aPlayBackSlider, q=True, ra=1)
	pinFrame=textFieldButtonGrp(parentObject,q=1,text=1)
	if "transform"==nodeType(sels):
		currentTime(pinFrame)
		thePiv=xform(sels,q=1,ws=1,piv=1)
		theRo=xform(sels,q=1,ws=1,ro=1)
		tempLocator=group(em=1)
		xform(tempLocator,ws=1,t=(thePiv[0],thePiv[1],thePiv[2]))
		xform(tempLocator,ws=1,ro=(theRo[0],theRo[1],theRo[2]))
		parentConstraint(tempLocator,sels,mo=1,weight=1,)
		bakeResults(sels, simulation=1,t=(rangeArr[0],rangeArr[1]),sb=1,preserveOutsideKeys=1)
		delete(tempLocator)
		select(sels)

###---------------end!---------####



