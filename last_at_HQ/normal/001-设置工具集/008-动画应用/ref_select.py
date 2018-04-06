from maya.cmds import *
import string
import maya.mel 

def doo():
   sel=ls(sl=1)
   okRN=[]
   if sel!=[]:
     for i in sel:
        if referenceQuery(i,inr=1)==1:
           okRN.append(referenceQuery(i,rfn=1))

   gReferenceEditorPanel = maya.mel.eval("$temp=$gReferenceEditorPanel") 
   allRef=ls(type="reference")
   [allRef.remove(i) for i in allRef if "RN" not in i]
   rangeRef=len(allRef)
   tempzidian={}
   for i in range(rangeRef):
       sceneEditor(gReferenceEditorPanel,e=1,selectItem=i)
       currRN=sceneEditor(gReferenceEditorPanel,q=1,selectReference=1)
       tempzidian[i]=currRN
   for k in tempzidian.keys():
       if okRN!=[] and  tempzidian[k][0]==okRN[0]:
          sceneEditor(gReferenceEditorPanel,e=1,selectItem=k)