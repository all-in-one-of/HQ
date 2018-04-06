##插件加载
import sys
sys.path.append("O:\hq_tool\Maya\Arnold\Arnold_1.2.7.3_Maya2015\scripts")
##maya独立运行
import maya.standalone
maya.standalone.initialize(name = "python")
##打开maya，获取数据
import maya.cmds as cmds
filepath  = "D:/test.mb"
cmds.file(filepath ,o=1)