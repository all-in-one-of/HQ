import maya.cmds as cmds

class Createobj(object):
    def __init__(self,pathobj=[],objcount=[],pathcurve='',group='grp'):
       self.objcounts=objcount
       self.windows='DuplicatePath'
       self.slidername='sileder'
       self.buttonname='create'
       self.group=group
        
    def Window(self):
        cmds.window(self.windows)
        cmds.columnLayout(adj=1)
        cmds.intSliderGrp(self.slidername, field=True, label='count:  ',maxValue=100 )
        cmds.button(l=self.buttonname,c='Createobj().pathAnim()')
        cmds.setParent('..')
        cmds.showWindow()
        
    def pathAnim(self,**arg):
        start=0
        end=0
        arg['fractionMode']=1
        arg['follow']=1
        arg['followAxis']='x'
        arg['upAxis']='y'
        arg['worldUpType']='vector'
        arg['worldUpVector']=(0,1,0)
        arg['inverseUp']=False
        arg['inverseFront']=False
        arg['bank']=False
        
        countvalue=cmds.intSliderGrp(self.slidername,q=1, v=True)
        
        starts=1
        ends=countvalue
        cu=0
        cmds.currentTime(ends)
        sel=cmds.ls(sl=1)
        
        uo=len(sel)
        
        if uo is 2:
            shapes=cmds.listRelatives(sel[1],s=1)
            if cmds.nodeType(shapes[0]) != 'nurbsCurve':
                cmds.error('must selcet one object and select another nurbsCurve')
        else:    
            cmds.error('must select two object:first select object and select a nurbsCurve')
        
        if cmds.objExists(sel[1]+'_'+self.group):
            cmds.delete(sel[1]+'_'+self.group)
        self.pathcurves=sel[1]
        self.objcounts=[]    
        
        for i in range(countvalue):
            self.objcounts.append(cmds.duplicate(sel[0]))
            cmds.select(self.objcounts[cu],add=1)
            cu=cu+1
        cmds.group(n=sel[1]+'_'+self.group)
        for s in self.objcounts:
            cmds.pathAnimation(self.pathcurves,s,startTimeU=start,endTimeU=end,**arg)
            
            starts=starts+1
            ends=ends+1
            
            start=starts
            end=ends
            
        listmotion=cmds.ls('motionPath*')
        for i in listmotion:
            if 'Value' in i:
                cmds.delete(i)
        cmds.currentTime(1,e=True)
        
        cmds.select(sel[0])
        cmds.select(sel[1],add=1)
Createobj().Window()