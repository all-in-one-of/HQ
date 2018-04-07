//Maya  2013
//通用项目配置
//Arnold version 1.0.0.1
+ MAYAVERSION:2013 mtoa any C:\hq_tool\Maya\Arnold\Arnold_1.0.0.1_Maya2013
PATH +:= bin
ARNOLD_PLUGIN_PATH =C:\hq_tool\Maya\Arnold\Arnold_1.0.0.1_Maya2013\shaders;C:\hq_tool\Maya\Arnold\Arnold_1.0.0.1_Maya2013\shaders\alShaders\bin
MTOA_TEMPLATES_PATH +:= shaders\alShaders\ae
MAYA_RENDER_DESC_PATH = C:\hq_tool\Maya\Arnold\Arnold_1.0.0.1_Maya2013


//VRay version 2.40.01
+ MAYAVERSION:2013 vrayformaya any C:\hq_tool\Maya\Vray\vray_2.40.01_Maya2013
PATH +:= bin
VRAY_FOR_MAYA2013_PLUGINS_x64 = C:\hq_tool\Maya\Vray\vray_2.40.01_Maya2013\vrayplugins;
VRAY_FOR_MAYA2013_MAIN_x64 = C:\hq_tool\Maya\Vray\vray_2.40.01_Maya2013
VRAY_FOR_MAYA2013_PLUGINS_x64 = C:\hq_tool\Maya\Vray\vray_2.40.01_Maya2013\vrayplugins
VRAY_TOOLS_MAYA2013_x64 = C:\hq_tool\Maya\Vray\vray_2.40.01_Maya2013\Chaos Group\bin
MAYA_RENDER_DESC_PATH = C:\hq_tool\Maya\Vray\vray_2.40.01_Maya2013\bin\rendererDesc

//shave Version 8.0
+ MAYAVERSION:2013 shaveHaircut 1.1 C:\hq_tool\Maya\Shave\shave_1.1_maya2013
RLM_LICENSE +:= rlm
PATH +:= bin


//fisheye for mentalray
+ MAYAVERSION:2013 Mayatomr any C:\Program Files\Autodesk\Maya2013\mentalray
MAYA_MR_STARTUP_DIR = C:\hq_tool\Maya\Mentalray\mentalray_for_maya2013
MI_CUSTOM_SHADER_PATH = C:\hq_tool\Maya\Mentalray\mentalray_for_maya2013\shaders
MI_LIBRARY_PATH = C:\hq_tool\Maya\Mentalray\mentalray_for_maya2013\shaders\include

//anzobinRigNodes
+ MAYAVERSION:2013 anzobinRigNodes any C:\hq_tool\Maya\AnzobinRigNodes\AnzobinRigNodes_1.0_Maya2013
[r] scripts: .\scripts

//realflow
+ MAYAVERSION:2013 realflow any C:\hq_tool\Maya\Realflow\Realflow_2014.0.1_Maya2013
path +:=bin



//Maya  2015

//吴哥项目等旧项目配置

//Arnold version 1.2.3.1
+ MAYAVERSION:2015 mtoa any C:\hq_tool\Maya\Arnold\Arnold_1.2.3.1_Maya2015
PATH +:= bin
ARNOLD_PLUGIN_PATH =C:\hq_tool\Maya\Arnold\Arnold_1.2.3.1_Maya2015\shaders;C:\hq_tool\Maya\Arnold\Arnold_1.2.3.1_Maya2015\shaders\alShaders\bin
MTOA_TEMPLATES_PATH +:= shaders\alShaders\ae
MAYA_RENDER_DESC_PATH = C:\hq_tool\Maya\Arnold\Arnold_1.2.3.1_Maya2015
MTOA_PROCEDURAL_PATH =C:\hq_tool\Maya\Yeti\Yeti_1.3.19_maya2015\bin
MTOA_EXTENSIONS_PATH =C:\hq_tool\Maya\Yeti\Yeti_1.3.19_maya2015\plug-ins
LD_LIBRARY_PATH =C:\hq_tool\Maya\Yeti\Yeti_1.3.19_maya2015\bin


//Yeti version 1.3.19
+ MAYAVERSION:2015 pgYetiMaya 1.3.19 C:\hq_tool\Maya\Yeti\Yeti_1.3.19_maya2015
PATH +:= bin
PEREGRINEL_LICENSE = C:\hq_tool\Maya\Yeti\Yeti_1.3.19_maya2015\rlm\yeti.lic
YETI_HOME = C:\Yeti_1.3.19_maya2015;


//VRay version 3.10.01
+ MAYAVERSION:2015 vrayformaya 3.10.01 C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015
PATH +:= bin
VRAY_FOR_MAYA2015_PLUGINS_x64 = C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\vrayplugins;
VRAY_FOR_MAYA2015_MAIN_x64 = C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015
VRAY_FOR_MAYA2015_PLUGINS_x64 = C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\vrayplugins
VRAY_OSL_PATH_MAYA2015_x64 = C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\Chaos Group\opensl
VRAY_TOOLS_MAYA2015_x64 = C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\Chaos Group\bin
MAYA_RENDER_DESC_PATH = C:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\bin\rendererDesc

//shave Version 9.0v24
+ MAYAVERSION:2015 shaveHaircut 1.1 C:\hq_tool\Maya\Shave\shave_1.1_maya2015
RLM_LICENSE +:= rlm
PATH +:= bin



//fisheye for mentalray
+ MAYAVERSION:2015 Mayatomr any C:\Program Files\Autodesk\mentalrayForMaya2015
MAYA_MR_STARTUP_DIR = C:\hq_tool\Maya\Mentalray\mentalray_for_maya2015
MI_CUSTOM_SHADER_PATH = C:\hq_tool\Maya\Mentalray\mentalray_for_maya2015\shaders
MI_LIBRARY_PATH = C:\hq_tool\Maya\Mentalray\mentalray_for_maya2015\shaders\include


//anzobinRigNodes
+ MAYAVERSION:2015 anzobinRigNodes any C:\hq_tool\Maya\AnzobinRigNodes
[r] scripts: .\scripts

//realflow
+ MAYAVERSION:2015 realflow 2014.0.1 C:\hq_tool\Maya\Realflow

//hq_tool
+ MAYAVERSION:2015 hq_maya any C:\hq_tool\Maya\hq_maya
[r] icons: .\icons
[r] scripts: .\scripts

//Miarmy
+ MAYAVERSION:2015 Miarmy Any C:\hq_tool\Maya\Miarmy\Miarmy_5.5.15RC_Maya2015
PATH +:= bin
[r] icons: .\maya\icons
[r] scripts: .\maya\scripts
[r] plug-ins: .\maya\plug-ins

//Maya 2017