# -*- coding: UTF-8 -*- 
# by Xuefeng   2011.10.20

# BatchReads   v2.0



import nukescripts

import glob

import nuke



class BatchReads( nukescripts.PythonPanel ):



    def __init__( self ):

        nukescripts.PythonPanel.__init__( self, "batchReads v2.0" )



        # Find Project Folders in /All/*

        allFolder = glob.glob('/All/*')

        projFolder = []

        for i in allFolder:

            t=i.split('/').pop()

            if len(t)==3:

                projFolder.append(t)

        

        # Define Departments

        deptList = ['ani','cmp','dmt','efx','lgt','mod','prd','pvz','tex','trk']

        

        # Define Knobs

        self.root = nuke.Enumeration_Knob( "root", "ROOT :  /" ,('All',))

        self.project = nuke.Enumeration_Knob( "project", "Project :  /" ,projFolder)

        self.scene = nuke.String_Knob( "scene", "Scene :  /" )

        self.camera = nuke.String_Knob( "camera", "Camera :  /" )

        self.stuff = nuke.Enumeration_Knob( "stuff", "Stuff :  /",('STUFF',) )

        self.department = nuke.Enumeration_Knob( "department", "Department :  /",deptList )

        self.folder = nuke.String_Knob( "folder", "Folder :  /" )

        self.divline1 = nuke.Text_Knob("")

        self.key = nuke.String_Knob( "key", "Key : " )

        self.divline2 = nuke.Text_Knob( "advanced ","Advanced    " )

        self.frmplus = nuke.Int_Knob( "frmplus","First Frame +" )

        self.frmminus = nuke.Int_Knob( "frmminus","Last Frame -" )

        self.lastversion =nuke.Boolean_Knob( "lastversion","Only Last Version" ) 

        self.appendclip = nuke.Boolean_Knob( "appendclip","AppendClip" )

       

        # Add Knob in the Panel

        self.addKnob( self.root )

        self.addKnob( self.project )

        self.addKnob( self.scene )

        self.addKnob( self.camera )

        self.addKnob( self.stuff )

        self.addKnob( self.department )

        self.addKnob( self.folder )

        self.addKnob( self.divline1 )

        self.addKnob( self.key )

        self.addKnob( self.divline2 )

        self.addKnob( self.frmplus )

        self.addKnob( self.frmminus )

        self.addKnob( self.lastversion )

        self.addKnob( self.appendclip )

        

        # Initialize the Knobs Value

        self.root.setValue(0)

        #self.project.setValue('MGC')

        self.scene.setValue('0')

        self.camera.setValue('*')

        self.stuff.setValue(0)

        self.department.setValue(1)

        self.folder.setValue('publish')

        self.key.setValue('final')

        self.frmplus.setValue(1)

        self.frmminus.setValue(1)

        self.lastversion.setValue(1)

        self.appendclip.setValue(0)





    def showDialog( self ):

        result = nukescripts.PythonPanel.showModalDialog( self )



        if result:

            # User Input Value

            inputPath = "/All/"+self.project.value()+'/'+self.scene.value()+'/'+ \

                        self.camera.value()+'/STUFF/'+self.department.value()+'/'+ \

                        self.folder.value()+'/*'+self.key.value()+'*/'

            

            # Via InputPath search All Correct Path

            searchPath = glob.glob(inputPath)

            searchPath.sort()

            

            # Remove Void Folder

            for i in searchPath:

                if glob.glob(i+'*') == []:

                    searchPath.remove(i)

            

            # Folder Last Version

            if self.lastversion.value():

                

                folderPath = []

                lastFolderPath = []

                

                for i in searchPath:

                    t = i.split('_'+self.department.value()).pop(0)

                    folderPath.append(t)

                folderPath = list(set(folderPath))

                folderPath.sort()

                

                for i in folderPath:

                    lastFolderPath.append(max(glob.glob(i+'*'+self.key.value()+'*')))

                searchPath = lastFolderPath



            # Define xPos is ReadNode x position in the NodeGraph

            # Define clip is each ReadNode number of AppendclipNode

            xPos = 0

            clip = 0

            

            # Need AppendClipNode

            if self.appendclip.value():

                # Create AppendclipNode

                appendClip = nuke.createNode('AppendClip',inpanel=False)

                appendClip.setXYpos(len(searchPath)*50,500)

                

                # Create ReadNodes in the loop

                for i in searchPath:

                    # fileList is each Folder's Files

                    fileList = glob.glob(i+'/*')

                    fileList.sort()

                    
                    # Remove the Error file

                    for i in fileList:

                        if len(i.split('.'))!=3 or len(i.split('.').pop(1)) != 4  or i.split('.').pop(1).isdigit() is False :

                            fileList.remove(i)

                    

                    # Calculate First Frame and Last Frame

                    frontNum = str(int(min(fileList).split('.').pop(1)) + self.frmplus.value())

                    backNum = str(int(max(fileList).split('.').pop(1)) - self.frmminus.value())

                    # fileName is fullname of the ReadNode

                    fileName = fileList[0].split('.').pop(0)+'.%04d.'+fileList[0].split('.').pop()

                    

                    # Create ReadNode

                    creatRead=nuke.createNode("Read","file {"+fileName+" "+frontNum+"-"+backNum+"}", inpanel = False)

                    creatRead.setXYpos(xPos,1)

                    xPos=xPos+100

                    

                    # link to AppendclipNode

                    sc=nuke.selectedNode()

                    appendClip.setInput(clip,sc)

                    clip=clip+1



            # Needn't AppendClipNode

            else:

                # Create ReadNodes in the loop

                for i in searchPath:

                    # fileList is each Folder's Files

                    fileList = glob.glob(i+'/*')

                    fileList.sort()

                    

                    # Remove the Error file

                    for i in fileList:

                        if len(i.split('.'))!=3 or len(i.split('.').pop(1)) != 4  or i.split('.').pop(1).isdigit() is False :

                            fileList.remove(i)

                    

                    # Calculate First Frame and Last Frame

                    frontNum = str(int(min(fileList).split('.').pop(1)) + self.frmplus.value())

                    backNum = str(int(max(fileList).split('.').pop(1)) - self.frmminus.value())
                    # fileName is fullname of the ReadNode

                    fileName = fileList[0].split('.').pop(0)+'.%04d.'+fileList[0].split('.').pop()

                    

                    # Create ReadNode

                    creatRead=nuke.createNode("Read","file {"+fileName+" "+frontNum+"-"+backNum+"}", inpanel = False)

                    creatRead.setXYpos(xPos,1)

                    xPos=xPos+100



            # Show the message

            length=len(searchPath)

            nuke.message(str(length)+'Reads')









def batchReads():

    return BatchReads().showDialog()
