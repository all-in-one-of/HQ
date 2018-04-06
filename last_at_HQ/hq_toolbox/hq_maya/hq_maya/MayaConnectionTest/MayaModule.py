from PySide import QtGui
from PySide import QtCore
import thread
import os
import rpyc

from maya import OpenMayaUI as mui
import maya.cmds as cmds
import time


class MayaConnectionUI(QtGui.QMainWindow):
    '''
        This is a example python code to show how to uses rpc python module
        to create a live connection between Maya and Houdini.
        
        It requires rpyc for python 2.7: http://rpyc.readthedocs.org/en/latest/
        
        This is just a test, it is not a final or optimized code.
        
        This script must be copied in the script folder of maya and
        launched as followed in a python tool shelf:
        
        import MayaModule
        ui = MayaModule.MayaConnectionUI()
        ui.show()
        
        On the Houdini side, you must have in your $HOME/houdini13.0/scripts a file
        names 123.py with this code in it:
        
        import hrpyc
        server = hrpyc.start_server(port=18812)
        
        You can copy the icons green_light.png and red_light.png 
        in a folder "icons" saved in the same place as the python file.
        
        Author: Guillaume Jobst
        Email: contact@guillaume-j.com
        Web: www.guillaume-j.com
    
    '''

    
    def __init__(self):
        QtGui.QMainWindow.__init__(self, parent=getMayaWindow())
        
        _DEFAULT_PORT = "18812"
        
        # This is where the tmp geo will be saved (as .obj)
        # and load in Houdini from.

        self.PATH = os.path.join( os.environ['temp'], "tmp.obj" ).replace( '\\', '/')
        
        
        self.setWindowTitle("Maya - Houdini bridge")
        cw = QtGui.QWidget()
        
        # Default connection variables
        self.houdini_connexion = None
        self.hou = None
        
        # Switch variables
        self.check_connection = True
        self.dynamicCameraON = False
        self.cancel = False
        
        cw_layout = QtGui.QVBoxLayout()
        cw_layout.setSpacing(10)
        
        # Houdini connection UI
        houConnectionLayout = QtGui.QHBoxLayout(spacing=20)
        self.houConnectionLabel  = QtGui.QLabel("Not connected to Houdini")
        
        self.houConnectionBtn = QtGui.QPushButton("")
        self.houConnectionBtn.setFlat(True)
        self.houConnectionBtn.setIcon(QtGui.QIcon(os.path.dirname(__file__)+"/icons/red_light.png"))
        self.houConnectionBtn.setFixedSize(32,32)
        self.houConnectionBtn.setIconSize(QtCore.QSize(32,32))
        self.houConnectionBtn.clicked.connect(self._connectTOHou)
        
        houConnectionLayout.addWidget(self.houConnectionBtn)
        houConnectionLayout.addWidget(self.houConnectionLabel)
        
        # Send geo button UI
        self.sendGeoToHouBtn = QtGui.QPushButton("Send selected mesh to houdini", self)
        self.sendGeoToHouBtn.clicked.connect(self.sendSelectionToHoudini)
        self.sendGeoToHouBtn.setDisabled(True)
        
        # Dynamic camera create / disable button
        self.dynCamBtn = QtGui.QPushButton("Create/Enable Dynamic Camera")
        self.dynCamBtn.clicked.connect(self.createDynamicCamera)
        self.dynCamBtn.setDisabled(True)
        
        cw_layout.addItem(houConnectionLayout)
        cw_layout.addWidget(self.sendGeoToHouBtn)
        cw_layout.addWidget(self.dynCamBtn)
        cw.setLayout(cw_layout)
        self.setCentralWidget(cw)
        
        # Check here if we can connect to houdini or not
        thread.start_new(self._connectionCheck, ())
    
    
    
    def closeEvent(self, event):
        ''' When we close the UI, set the check connection variable
            To false in order to stop the test.
        '''
        self.check_connection = False
        self.close()
          
     
        
    def _connectTOHou(self):
        ''' Try to connect to houdini => localhost and post 18812
            If connection works, the houdini python module hou is
            assigned to self.hou variable
            
            If not, it changes the UI accordingly ( buttons are disabled ).
        '''
        
        # Connection works
        try:
            
            self.houdini_connexion = rpyc.classic.connect("localhost", 18812)
            self.hou = self.houdini_connexion.modules.hou
            
            self.hou_connected = True
            self.houConnectionBtn.setIcon(QtGui.QIcon(os.path.dirname(__file__)+"/icons/green_light.png"))
            self.houConnectionLabel.setText("Connected to Houdini")
            
            self.dynCamBtn.setDisabled(False)
            self.sendGeoToHouBtn.setDisabled(False)
        
        
        # Connection doesn't work   
        except:
            
            self.cancel = True
            self.hou_connected = False
            
            self.houConnectionBtn.setIcon(QtGui.QIcon(os.path.dirname(__file__)+"/icons/red_light.png"))
            self.houConnectionLabel.setText("Not connected to Houdini")
            
            self.dynCamBtn.setDisabled(True)
            self.sendGeoToHouBtn.setDisabled(True)
    
    
    def sendSelectionToHoudini(self):
        ''' This method creates in houdini a geo node called "maya_geo"
            or uses any existing on.
            Then set the object file path to the obj exported by maya.
        '''
        
        print("Sending mesh to houdini...")
        
        
        # Export the selected mesh as obj
        cmds.file(self.PATH, force=True, typ="OBJexport",es=True)
        
        # Check if any node "maya_geo" already exist in Houdini
        # If not, create one.
        n=self.hou.node("/obj/maya_geo")
        
        if not n:
            n=self.hou.node("/obj").createNode("geo", node_name="maya_geo", run_init_scripts=False)
            f=n.createNode("file")
            
        else:
            f = self.hou.node("/obj/maya_geo/file1")
        
        # Set the Houdini geo's path parm to the obj just exported by Maya   
        f.parm("file").set(self.PATH)
        
        
    def createDynamicCamera(self):
        ''' Create or Enable / Disable the camera live connection
            It creates a camera in Maya ( if none is alread selected )
        '''
        
        # Create or enable live camera
        if not self.dynamicCameraON:
            
            
            # Create the maya camera
            # Or use the selected one if any
            mayaSel = cmds.ls(selection=True)
            
            if mayaSel:
                self.maya_cam = cmds.ls(selection=True)[0]
                
            else:
                self.maya_cam = cmds.camera()[0]
                cmds.rename(self.maya_cam, "dynamic_camera")
            
            
            # Create a houdini camera node if no camera found already
            self.dynHouCam = self.hou.node("/obj/dynamic_camera")
            
            if not self.dynHouCam:
                self.dynHouCam = self.hou.node("/obj").createNode("cam", node_name="dynamic_camera")
            
            
            # Change switch state
            self.cancel = False
            self.dynamicCameraON = True
            self.dynCamBtn.setText("Disable live connection")
            
            
            # Start live connection loop
            # Every 0.5 second it will set the houdini camera node transformation
            # parameters to the maya's camera transform.
            thread.start_new(self._loop, ())
        
        
        # Disable live camera connection   
        else:
            self.dynamicCameraON = False
            self.cancel = True
            self.dynCamBtn.setText("Create/Enable Dynamic Camera")

   
    def _loop(self):
        ''' As long as the dynamic connection is ON (self.cancel set to True)
            This will update the houdini camera transform parameters according to 
            the maya camera.
        '''
        while not self.cancel:
            
            # Fetch datas from Maya camera
            trans = [cmds.getAttr("dynamic_camera"+".translateX"),
                     cmds.getAttr("dynamic_camera"+".translateY"),
                     cmds.getAttr("dynamic_camera"+".translateZ")]
            
            rot = [cmds.getAttr("dynamic_camera"+".rotateX"),
                   cmds.getAttr("dynamic_camera"+".rotateY"),
                   cmds.getAttr("dynamic_camera"+".rotateZ")]
            
            # Apply datas to Houdini camera
            self.dynHouCam.setParms({"tx":trans[0],
                                    "ty":trans[1],
                                    "tz":trans[2],
                                    "rx":rot[0],
                                    "ry":rot[1],
                                    "rz":rot[2]})

            time.sleep(0.5)
        
    
    def _connectionCheck(self):
        ''' As long as the windows is opened, this will check if we can
            connect to Houdini, if we close the windows, the variable
            self.check_connection will be set to False and the test
            won't occur anymore.
        '''
        while self.check_connection:
            self._connectTOHou()
            time.sleep(1)



def getMayaWindow():
    '''
    Get the maya main window as a QMainWindow instance
    '''
    #from PySide.shiboken import wrapInstance
    from shiboken import wrapInstance
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QWidget)
