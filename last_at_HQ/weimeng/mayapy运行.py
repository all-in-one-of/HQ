##�������
import sys
sys.path.append("O:\hq_tool\Maya\Arnold\Arnold_1.2.7.3_Maya2015\scripts")
##maya��������
import maya.standalone
maya.standalone.initialize(name = "python")
##��maya����ȡ����
import maya.cmds as cmds
filepath  = "D:/test.mb"
cmds.file(filepath ,o=1)