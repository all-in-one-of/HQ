# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################


import maya.cmds as cmds

#-------------w08 select by Normal
class w08_selectFacesByNormal(object):
    _menuStr = '''{'del_path':'Edit/w08_selectFacesByNormal()',
'icon':':/selectByComponent.png',
'tip' : '按面的法线选择面',
'usage':'$fun()',
}
'''
    def __init__(self):
        self.w08_oriSel=[]
        if cmds.window('w08', exists=True):
            cmds.deleteUI('w08')
        cmds.window('w08',title='w08_Select By Normal', tbm=False, w=400,sizeable=False)
        
        cmds.rowColumnLayout( 'w08_rcL', p='w08', numberOfColumns=1, width=400)
        cmds.button('w08_rcL02_01', p='w08_rcL', label='Get Objects From Selected', height=40, command=self.w08_getData  )
        cmds.radioButtonGrp( 'w08_01',  p='w08_rcL', label='Normal Value From', height=50, labelArray3=['X', 'Y', 'Z'], sl=2, numberOfRadioButtons=3, cc=self.w08_uiChange_cmd )
        cmds.floatSliderGrp( 'w08_normalValue', p='w08_rcL', field=True, label='Normal Value', height=30, minValue=-1, maxValue=1, step=.001, cw3=[80,50,170], cc=self.w08_uiChange_cmd  )
        
        cmds.rowColumnLayout(  'w08_rcL01', p='w08_rcL', numberOfColumns=3, columnAlign=[(1,'left'),(2,'right')] )
        cmds.checkBox( 'w08_checkMin', p='w08_rcL01', label='min', width=200, height=30, v=True, changeCommand=self.w08_uiChange_cmd )
        cmds.checkBox( 'w08_checkMax', p='w08_rcL01', label='max', width=200, height=30, v=True, changeCommand=self.w08_uiChange_cmd )
        cmds.checkBox( 'w08_absStyle', p='w08_rcL01', label='abs Style', width=200, height=30, v=True, changeCommand=self.w08_uiChange_cmd  )
        
        cmds.button(    'w08_06',   p='w08_rcL',label='Colse',bgc=[.4,.4,.4], h=50, rs=False, command='cmds.deleteUI("w08")')
        
        cmds.showWindow( 'w08')
    
    
    
    def w08_uiChange_cmd( self, normalDatas=[], *args ):
        normalDatas = self.w08_oriSel
        axis = cmds.radioButtonGrp( 'w08_01', q=True, sl=True)-1
        normalValue = cmds.floatSliderGrp( 'w08_normalValue', q=True, v=True)      
        checkMin = cmds.checkBox( 'w08_checkMin', q=True, v=True)
        checkMax = cmds.checkBox( 'w08_checkMax', q=True, v=True)
        absValue = cmds.checkBox( 'w08_absStyle', q=True, v=True)
        resultFaces = []
        if normalValue !=-1 and normalValue!=1 and checkMin != checkMax and normalDatas!=[]:
            #get single Axis normal
            if absValue:
                tempList = [ (   math.fabs( i[1][axis]),   i[0]   ) for i in normalDatas ]
            else:
                tempList = [ (i[1][axis], i[0] ) for i in normalDatas ]
            sep = (normalValue, 'fillter')
            tempList.append(  sep  )
            tempList.sort()
            sepIndex = tempList.index( sep )
            if checkMin:
                resultFaces = [ tempList[i][1] for i in range( sepIndex ) ]
                #for i in range( sepIndex ):                
                    #resultFaces.append( tempList[i][1] )
            else:
                resultFaces = [ tempList[i][1] for i in range( sepIndex+1, len(tempList) )  ]
                #for i in range( sepIndex+1, len(tempList) ):
                    #resultFaces.append( tempList[i][1] )
        
        if resultFaces!=[]:
            cmds.select( resultFaces, r=True)
        else:
            cmds.select( cl=True)
            
    
    def w08_getData(self, *args):        
        resultData = []
        polyObjs = cmds.filterExpand( sm=12)
        faces = cmds.filterExpand( sm=34)
        if polyObjs !=None:
            for poly in polyObjs:
                normalData = cmds.polyInfo(poly,fn=True)
                for f in normalData:
                    faceData = str(f).split()  
                    faceName =  '%s.f[%s]'%(poly,faceData[1][:-1])
                    nor = [  float(faceData[2]), float(faceData[3]), float(faceData[4]) ]
                    resultData.append(  (  faceName, nor   )       )
                        
        elif faces!=None:
            for f in faces:
                normalData = cmds.polyInfo(f, fn=True)[0] 
                faceData = str(normalData).split()  
                nor = [  float(faceData[2]), float(faceData[3]), float(faceData[4]) ]      
                resultData.append( ( f, nor ) )                
       
        self.w08_oriSel = resultData
    
    #----W08End