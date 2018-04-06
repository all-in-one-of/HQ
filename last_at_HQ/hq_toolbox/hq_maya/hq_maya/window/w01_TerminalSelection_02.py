# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import qsMaya as qm


import math


#------------------------------w01 Start-------------------------------------
#class w01_terminalSelection():
w01_objectsData= ()
def w01_TerminalSelection():
    '''{'path':'General/w01_TerminalSelection()',
'icon2':'menuIconWindow.png',
'icon':':/selectByObject.png',
'html':'',
'usage':'w01_TerminalSelection()',
}
'''
    if cmds.window('w01', exists=True):
        cmds.deleteUI('w01')
    cmds.window('w01',title='w01_Terminal Selection ', tbm=False, w=650,sizeable=False)
    #form = cmds.formLayout('form', p=QSWindow, w=550, numberOfDivisions=100)
    cmds.formLayout('w01_formL', p='w01', w=500, numberOfDivisions=100)
    
    cmds.rowColumnLayout( 'w01_rcL', p='w01_formL', numberOfColumns=3)
    cmds.radioButtonGrp( 'w01_01',  p='w01_rcL', label='first', numberOfRadioButtons=3, cw=([1,20],[2,20],[3,20]),select=1, rat=([1,'top', 25], [2,'both', 10]),  vertical=True, changeCommand='w01_01_cc()\nw01_changeUI_command(w01_objectsData)' )
    cmds.radioButtonGrp( 'w01_02',  p='w01_rcL', label='sec', numberOfRadioButtons=3, cw=([1,20],[2,20],[3,20]), select=2,  rat=([1,'top', 25], [2,'both', 10]),  vertical=True, changeCommand='w01_02_cc()\nw01_changeUI_command(w01_objectsData)' )
    cmds.radioButtonGrp( 'w01_03',  p='w01_rcL', label='third', numberOfRadioButtons=3, cw=([1,25],[2,25],[3,25]), select=3,rat=([1,'top', 25], [2,'both', 10]),  vertical=True, changeCommand='w01_03_cc()\nw01_changeUI_command(w01_objectsData)')
    
    
    
    cmds.rowColumnLayout( 'w01_rcL02', p='w01_formL', numberOfColumns=4, width=600, columnWidth=[(1, 300), (2, 40), (3, 40), (4,130)], cs=[1,10] )
    
    #row 1b
    cmds.button('w01_rcL02_01', p='w01_rcL02', label='Get Objects From Selected', command='w01_objectsData = w01_rcL02_01_c()\nw01_changeUI_command(w01_objectsData)')
    cmds.text(                  p='w01_rcL02', enable=False,visible=False)
    cmds.text(                  p='w01_rcL02', enable=False,visible=False)
    #cmds.text(                  p='w01_rcL02', enable=False,visible=False)
    cmds.intFieldGrp( 'w01_disCount', label='count', w=80, cl2=['right','center'], cw2=[60,50], value1=0, bgc=[.8,.5,0], en=False)
    
    
    
    #row 2
    cmds.floatSliderGrp( 'w01_rcL02_02', p='w01_rcL02', field=True, label='Size', minValue=0, maxValue=100, step=.1, cw3=[30,50,100], cc="w01_changeUI_command(w01_objectsData)")
    cmds.checkBox( 'w01_rcL02_03', p='w01_rcL02', label='min', bgc=[0,.8,0], changeCommand="w01_minMax_cc('w01_rcL02_03','w01_rcL02_04', w01_objectsData)" )
    cmds.checkBox( 'w01_rcL02_04', p='w01_rcL02', label='max', bgc=[0,.8,0], changeCommand="w01_minMax_cc('w01_rcL02_03','w01_rcL02_04', w01_objectsData)")
    cmds.radioButtonGrp( 'w01_12', p='w01_rcL02', label='By', numberOfRadioButtons=2, bgc=[.15,.15,.15], labelArray2=['value', 'percent'], cw=([1,15],[2,50],[2,50]), select=2, changeCommand="w01_By_cc( 'w01_12', 'w01_rcL02_02', w01_objectsData)" )   #cat=([2,'left',4] ),
    
    
    #row 3
    cmds.floatSliderGrp( 'w01_rcL02_05', p='w01_rcL02', field=True, label='Count', minValue=0, maxValue=100, step=.1, cw3=[30,50,100], changeCommand="w01_changeUI_command(w01_objectsData)")
    cmds.checkBox( 'w01_rcL02_06', p='w01_rcL02', label='min', bgc=[0,.8,0], changeCommand="w01_minMax_cc('w01_rcL02_06','w01_rcL02_07', w01_objectsData)"  )
    cmds.checkBox( 'w01_rcL02_07', p='w01_rcL02', label='max', bgc=[0,.8,0], changeCommand="w01_minMax_cc('w01_rcL02_06','w01_rcL02_07', w01_objectsData)"  )
    cmds.radioButtonGrp( 'w01_13', p='w01_rcL02', label='By', numberOfRadioButtons=2, bgc=[.15,.15,.15], labelArray2=['value', 'percent'], cw=([1,15],[2,50],[2,50]), select=2, changeCommand="w01_By_cc( 'w01_13', 'w01_rcL02_05', w01_objectsData)"  )
    
    
    #row 4
    cmds.floatSliderGrp( 'w01_rcL02_08', p='w01_rcL02', field=True, label='Area', minValue=0, maxValue=100, step=.005, cw3=[30,50,100], changeCommand="w01_changeUI_command(w01_objectsData)")
    cmds.checkBox( 'w01_rcL02_09', p='w01_rcL02', label='min', bgc=[0,.8,0], changeCommand="w01_minMax_cc('w01_rcL02_09','w01_rcL02_10', w01_objectsData)"  )
    cmds.checkBox( 'w01_rcL02_10', p='w01_rcL02', label='max', bgc=[0,.8,0], changeCommand="w01_minMax_cc('w01_rcL02_09','w01_rcL02_10', w01_objectsData)"  )
    cmds.radioButtonGrp( 'w01_14', p='w01_rcL02', label='By', numberOfRadioButtons=2, bgc=[.15,.15,.15], labelArray2=['value', 'percent'], cw=([1,15],[2,50],[2,50]), select=2, changeCommand="w01_By_cc( 'w01_14', 'w01_rcL02_08', w01_objectsData)" )
    
    
    #row 5
    cmds.checkBox( 'w01_rcL02_11', p='w01_rcL02', label='SELECT', bgc=[.5,0,0], h=30,rs=False, changeCommand="w01_select_cc(w01_objectsData)") 
    cmds.text(                  p='w01_rcL02', enable=False,visible=False)
    cmds.text(                  p='w01_rcL02', enable=False,visible=False)
    cmds.button(     'w01_15',   p='w01_rcL02',label='Colse',bgc=[.4,.4,.4], rs=False, command='w01_15_closeCommand()\nw01_objectsData=()')
    
    
    
    #select type
    #edit formLayout
    cmds.formLayout( 'w01_formL', edit=True, attachForm=[('w01_rcL', 'top', 5), ('w01_rcL', 'bottom', 5),('w01_rcL', 'left', 5),\
                                                         ('w01_rcL02', 'top', 5), ('w01_rcL02', 'bottom', 5),('w01_rcL02', 'right', 5)],\
                                      attachControl=[('w01_rcL', 'right', 5, 'w01_rcL02')],\
                                      attachPosition=[('w01_rcL', 'right', 5, 18), ('w01_rcL02', 'left', 5, 18)] )
    
 
    cmds.showWindow( 'w01')


def w01_select_cc(w01_objectsData):
    if w01_objectsData != ():
        if cmds.checkBox( 'w01_rcL02_11', q=True, v=True):
            cmds.checkBox( 'w01_rcL02_11', e=True, bgc=[0,.8,0] )
        else:
            cmds.checkBox( 'w01_rcL02_11', e=True, bgc=[.8,0,0] )
        w01_changeUI_command(w01_objectsData)
    


def w01_15_closeCommand():
    cmds.deleteUI('w01')




def w01_By_cc(radio, slider, w01_objectsData):
    #w01_By_cc( 'w01_12', 'w01_rcL02_02')
    #w01_By_cc( 'w01_13', 'w01_rcL02_05')
    #w01_By_cc( 'w01_14', 'w01_rcL02_08')
    radio_v = cmds.radioButtonGrp( radio, q=True, sl=True)
    if radio_v == 2:
        cmds.floatSliderGrp( slider, e=True, v=0)         
    else:# radio_v==1 and globals().has_key('w01_objectsData'): 
        cmds.floatSliderGrp( slider, e=True, v=.01)
    w01_changeUI_command(w01_objectsData)



def w01_minMax_cc(minName, maxName, w01_objectsData):
    min_v = cmds.checkBox( minName, q=True, v=True)
    max_v = cmds.checkBox( maxName, q=True, v=True)
    if min_v == max_v:
        cmds.checkBox( minName, e=True, bgc=[0,.8,0])
        cmds.checkBox( maxName, e=True, bgc=[0,.8,0])
    elif min_v: #min is True max is False
        cmds.checkBox( minName, e=True, bgc=[0,.8,0])
        cmds.checkBox( maxName, e=True, bgc=[.8,0,0])
    else:#min is False, max is True
        cmds.checkBox( minName, e=True, bgc=[.8,0,0])
        cmds.checkBox( maxName, e=True, bgc=[0,.8,0])
    if w01_objectsData != ():      
        w01_changeUI_command(w01_objectsData)

    
def w01_filterByFaceCount(objectList,minCount=2):
#    '''path:Selection/filterByFaceCount()ONLYSE
#icon:filtersOn.png
#usage:
#QM.filterByFaceCount(cmds.ls(sl=True),minCount=2)
#objectList = cmds.listRelatives(cmds.ls(sl=True), ad=True, f=True, type='mesh')
#resultList = QM.filterByFaceCount(objectList,minCount=2)
#cmds.select(resultList[0], r=True)
#'''
  
    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]

    objectList = qm.childCheck02(objectList, 'mesh')
    
    minObj, maxObj, faceCountList = [], [], []
    for object in objectList:
        objFaceCount = cmds.polyEvaluate(object,face=True)
        faceCountList.append([objFaceCount, object])  
        if objFaceCount<minCount:
            minObj.append(object)
        else:
            maxObj.append(object)
    print '%s objects in fist List. \n%s objects in secondary list'%( len(minObj), len(maxObj) )
    return minObj, maxObj, faceCountList



def w01_filterByPolyArea(objects,thresholdObject):
#    '''path:Selection/filterByPolyArea()ONLYSE
#icon:filtersOn.png
#usage:
#objectList = cmds.listRelatives(cmds.ls(sl=True)[:-1], ad=True, f=True, type='mesh')
#objectThreshold = cmds.ls(sl=True)[-1]
#resultList = QM.filterByPolyArea(objectList,objectThreshold)  
#cmds.select(resultList[0], r=True)
#'''    
    if str(type(objects)) == "<type 'str'>" or str(type(objects)) == "<type 'unicode'>":
        objects = [objects]
        
    objects = qm.childCheck02(objects, 'mesh')
    
    gThan, lThan, polyAreaList = [], [], []
    thrValue = cmds.polyEvaluate(thresholdObject, wa=True)
    for obj in objects:
        polyArea = cmds.polyEvaluate(obj,wa=True)
        polyAreaList.append([polyArea, obj])
        if  polyArea > thrValue:
            gThan.append(obj)
        else:
            lThan.append(obj)
    print '%s objects in fist List. \n%s objects in secondary list'%( len(lThan), len(gThan) )
    return lThan, gThan, polyAreaList



def w01_filterObjByBBoxSize(objectList, objectThreshold):
#    '''path:Selection/filterObjByBBoxSize()ONLYSE
#icon:filtersOn.png
#usage:
#resultList = QM.filterObjByBBoxSize(cmds.ls(sl=True)[:-1],cmds.ls(sl=True)[-1])
#cmds.select(resultList[0], r=True)
#objectList = cmds.listRelatives(cmds.ls(sl=True)[1], ad=True, f=True, type='transform')
#objectThreshold = cmds.ls(sl=True)[0]
#resultList = QM.filterObjByBBoxSize(objectList,objectThreshold)  
#cmds.select(resultList[0], r=True)
#'''
    
    if isinstance( objectList, str) or isinstance( objectList, unicode):
        objectList = [objectList]
        
    gThan, lThan, bbsiList = [],[],[]
    temp = cmds.getAttr(objectThreshold+'.bbsi')[0]
    sizeThreshold = round(math.sqrt(  math.pow(temp[0], 2) + math.pow(temp[1], 2) + math.pow(temp[2], 2) ), 5)
    #objectList = cmds.listRelatives(objGrp,ad=True,type='mesh')
    for object in objectList:
        temp = cmds.getAttr(object+'.bbsi')[0]
        bboxLen = math.sqrt(  math.pow(temp[0], 2) + math.pow(temp[1], 2) + math.pow(temp[2], 2) )
        bbsiList.append([bboxLen, object])
        if bboxLen > sizeThreshold:
            gThan.append(object)
        else:
            lThan.append(object)  
    print '%s objects in fist List. \n%s objects in secondary list'%( len(lThan), len(gThan) )
    return lThan, gThan, bbsiList



def w01_rcL02_01_c():
    objectList = qm.childCheck02( cmds.ls(sl=True, exactType='transform', l=True), 'mesh')
    
    bbsi = w01_filterObjByBBoxSize(objectList, cmds.ls(sl=True)[0])[2]
    bbsi.sort()  
    
    count = w01_filterByFaceCount(objectList,minCount=2)[2]
    count.sort()

    area = w01_filterByPolyArea(objectList,objectList[0])[2]
    area.sort()
    
    return bbsi, count, area, objectList




def w01_01_cc():
    rbNum=[1,2,3]
    w01_01_state = cmds.radioButtonGrp( 'w01_01',  q=True, sl=True )
    rbNum.remove(w01_01_state)
    w01_02_state = cmds.radioButtonGrp( 'w01_02',  q=True, sl=True )
    w01_03_state = cmds.radioButtonGrp( 'w01_03',  q=True, sl=True )
    if w01_02_state == w01_01_state and w01_03_state == w01_01_state:
        cmds.radioButtonGrp( 'w01_02',  e=True, sl=rbNum[0])
        cmds.radioButtonGrp( 'w01_03',  e=True, sl=rbNum[1])
        
    elif w01_02_state == w01_01_state and w01_03_state != w01_01_state:
        rbNum.remove(w01_03_state)
        cmds.radioButtonGrp( 'w01_02',  e=True, sl=rbNum[0])
    elif w01_02_state != w01_01_state and w01_03_state == w01_01_state:
        rbNum.remove(w01_02_state)
        cmds.radioButtonGrp( 'w01_03',  e=True, sl=rbNum[0])

    
def w01_02_cc():
    rbNum=[1,2,3]
    w01_02_state = cmds.radioButtonGrp( 'w01_02',  q=True, sl=True )
    rbNum.remove(w01_02_state)
    w01_01_state = cmds.radioButtonGrp( 'w01_01',  q=True, sl=True )
    w01_03_state = cmds.radioButtonGrp( 'w01_03',  q=True, sl=True )
    if w01_01_state == w01_02_state and w01_03_state == w01_02_state:
        cmds.radioButtonGrp( 'w01_01',  e=True, sl=rbNum[0])
        cmds.radioButtonGrp( 'w01_03',  e=True, sl=rbNum[1])
        
    elif w01_01_state == w01_02_state and w01_03_state != w01_02_state:
        rbNum.remove(w01_03_state)
        cmds.radioButtonGrp( 'w01_01',  e=True, sl=rbNum[0])
    elif w01_01_state != w01_02_state and w01_03_state == w01_02_state:
        rbNum.remove(w01_01_state)
        cmds.radioButtonGrp( 'w01_03',  e=True, sl=rbNum[0])

        
def w01_03_cc():
    rbNum=[1,2,3]
    w01_03_state = cmds.radioButtonGrp( 'w01_03',  q=True, sl=True )
    rbNum.remove(w01_03_state)
    w01_01_state = cmds.radioButtonGrp( 'w01_01',  q=True, sl=True )
    w01_02_state = cmds.radioButtonGrp( 'w01_02',  q=True, sl=True )
    if w01_01_state == w01_03_state and w01_02_state == w01_03_state:
        cmds.radioButtonGrp( 'w01_01',  e=True, sl=rbNum[0])
        cmds.radioButtonGrp( 'w01_02',  e=True, sl=rbNum[1])
        
    elif w01_01_state == w01_03_state and w01_02_state != w01_03_state:
        rbNum.remove(w01_02_state)
        cmds.radioButtonGrp( 'w01_01',  e=True, sl=rbNum[0])
    elif w01_01_state != w01_03_state and w01_02_state == w01_03_state:
        rbNum.remove(w01_01_state)
        cmds.radioButtonGrp( 'w01_02',  e=True, sl=rbNum[0])




def w01_separateObjects(w01_select_Mode, objectList, w01_objectsData):
    if cmds.checkBox( 'w01_rcL02_11', q=True, v=True):# and locals().has_key('w01_objectsData'):
        if w01_select_Mode == 'bbsiMode':
            objectsDataOri = w01_objectsData[0]            
            slider = 'w01_rcL02_02'
            slider_v = cmds.floatSliderGrp( 'w01_rcL02_02', q=True, v=True)   #bbsi slider_v 
            min_v = cmds.checkBox( 'w01_rcL02_03', q=True, v=True)     #bbsi min
            max_v = cmds.checkBox( 'w01_rcL02_04', q=True, v=True)     #bbsi max
            by_v = cmds.radioButtonGrp( 'w01_12', q=True, sl=True)          #bbsi by value/percent                           
        elif w01_select_Mode == 'countMode':
            objectsDataOri = w01_objectsData[1]
            slider = 'w01_rcL02_05'
            slider_v = cmds.floatSliderGrp( 'w01_rcL02_05', q=True, v=True)   #count slider_v 
            min_v = cmds.checkBox( 'w01_rcL02_06', q=True, v=True)     #count min
            max_v = cmds.checkBox( 'w01_rcL02_07', q=True, v=True)     #count max
            by_v = cmds.radioButtonGrp( 'w01_13', q=True, sl=True)          #count by value/percent
        elif w01_select_Mode == 'areaMode':
            objectsDataOri = w01_objectsData[2]
            slider = 'w01_rcL02_08'
            slider_v = cmds.floatSliderGrp( 'w01_rcL02_08', q=True, v=True)   #area slider_v 
            min_v = cmds.checkBox( 'w01_rcL02_09', q=True, v=True)     #area min
            max_v = cmds.checkBox( 'w01_rcL02_10', q=True, v=True)     #area max    
            by_v = cmds.radioButtonGrp( 'w01_14', q=True, sl=True)          #area by value/percent        
    
    
    #if select_v and globals().has_key('w01_objectsData'):#select or not
        #get objectList from objectsData
        objFromData = []           
        for obj in objectsDataOri:
            objFromData.append(obj[1])
        
        #filter objectsData
        keepDataIndexLi = []
        for obj in objectList:
            #if obj in objFromData:
            #index = objFromData.index(obj)
            keepDataIndexLi.append( objFromData.index(obj) )
        
                         
        #to get good objectsData
        if keepDataIndexLi != []:
            objectsData = []
            for index in keepDataIndexLi:
                objectsData.append( objectsDataOri[index] )
        
        
        objectsData.sort()
        objectList = []
        for obj in objectsData:
            objectList.append(obj[1]) 
        
        #set UI
        if by_v == 2:# by percent
            cmds.floatSliderGrp( slider, e=True, minValue=0, maxValue=100, step=.1)         
        else:# radio_v==1 #by value            
            minV = objectsData[0][0] + .0001
            maxV = objectsData[-1][0] + -.0001
            cmds.floatSliderGrp( slider, e=True, minValue=minV, maxValue=maxV, step=.001)
                    
        if min_v != max_v:
            #calculate#objects by bbsi            
            if by_v==1:#value mode
                for value in objectsData:
                    if value[0] >= slider_v:#slider value compare
                        sepIndex = objectsData.index(value)
                        break
                if locals().has_key('sepIndex') == False:
                    sepIndex = -2 
                        
            else:#percent mode
                sepIndex = int(  (len(objectsData)) * slider_v / 100  )
                            
            #separate objects
            if  min_v:#return min
                return objectList[:sepIndex+1]
                #print 'min'
            else:#return max
                return objectList[sepIndex:]
                #print 'max'
        else:
            return objectList
            #print 'all'




def w01_changeUI_command(w01_objectsData):
    if w01_objectsData != ():#locals().has_key('w01_objectsData'):
        methodOrder = (cmds.radioButtonGrp( 'w01_01',  q=True, sl=True ),\
                       cmds.radioButtonGrp( 'w01_02',  q=True, sl=True ),\
                       cmds.radioButtonGrp( 'w01_03',  q=True, sl=True ) )
        
        if   methodOrder == (1, 2, 3):#bbsi count area
            tempResult = w01_separateObjects('bbsiMode', w01_objectsData[3], w01_objectsData)
            tempResult = w01_separateObjects('countMode', tempResult, w01_objectsData)
            cmds.select(w01_separateObjects('areaMode', tempResult, w01_objectsData), r=True)
            
        elif methodOrder == (1, 3, 2):#bbsi area count
            tempResult = w01_separateObjects('bbsiMode', w01_objectsData[3], w01_objectsData)
            tempResult = w01_separateObjects('areaMode', tempResult, w01_objectsData)
            cmds.select(w01_separateObjects('countMode', tempResult, w01_objectsData), r=True)
            
        elif methodOrder == (2, 3, 1):#count area bbsi
            tempResult = w01_separateObjects('countMode', w01_objectsData[3], w01_objectsData)
            tempResult = w01_separateObjects('areaMode', tempResult, w01_objectsData)
            cmds.select(w01_separateObjects('bbsiMode', tempResult, w01_objectsData), r=True)
            
        elif methodOrder == (2, 1, 3):#count bbsi area
            tempResult = w01_separateObjects('countMode', w01_objectsData[3], w01_objectsData)
            tempResult = w01_separateObjects('areaMode', tempResult, w01_objectsData)
            cmds.select(w01_separateObjects('bbsiMode', tempResult, w01_objectsData), r=True)
            
        elif methodOrder == (3, 1, 2):#area bbsi count
            tempResult = w01_separateObjects('areaMode', w01_objectsData[3], w01_objectsData)
            tempResult = w01_separateObjects('bbsiMode', tempResult, w01_objectsData)
            cmds.select(w01_separateObjects('countMode', tempResult, w01_objectsData), r=True)
        elif methodOrder == (3, 2, 1):#area count bbsi
            tempResult = w01_separateObjects('areaMode', w01_objectsData[3], w01_objectsData)
            tempResult = w01_separateObjects('countMode', tempResult, w01_objectsData)
            cmds.select(w01_separateObjects('bbsiMode', tempResult, w01_objectsData), r=True)
            
        cmds.intFieldGrp( 'w01_disCount', e=True, value1=len( cmds.ls(sl=True) )  )


