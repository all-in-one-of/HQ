//Maya  2015

//通用项目配置


//Arnold version 1.2.7.3
+ MAYAVERSION:2015 mtoa any O:\hq_tool\Maya\Arnold\Arnold_1.2.7.3_Maya2015
PATH +:= bin
ARNOLD_PLUGIN_PATH =O:\hq_tool\Maya\Arnold\Arnold_1.2.7.3_Maya2015\shaders;O:\hq_tool\Maya\Arnold\Arnold_1.2.7.3_Maya2015\shaders\alShaders\bin
MTOA_TEMPLATES_PATH +:= shaders\alShaders\ae
MAYA_RENDER_DESC_PATH = O:\hq_tool\Maya\Arnold\Arnold_1.2.7.3_Maya2015
MTOA_PROCEDURAL_PATH =O:\hq_tool\Maya\Yeti\Yeti_2.0.24_maya2015\bin
MTOA_EXTENSIONS_PATH =O:\hq_tool\Maya\Yeti\Yeti_2.0.24_maya2015\plug-ins
LD_LIBRARY_PATH =O:\hq_tool\Maya\Yeti\Yeti_2.0.24_maya2015\bin


//Yeti version 2.0.24
+ MAYAVERSION:2015 pgYetiMaya 2.0.24 O:\hq_tool\Maya\Yeti\Yeti_2.0.24_maya2015
PATH +:= bin
PEREGRINEL_LICENSE = O:\hq_tool\Maya\Yeti\Yeti_2.0.24_maya2015\rlm\yeti.lic
YETI_HOME = O:\hq_tool\Maya\Yeti\Yeti_2.0.24_maya2015;

//VRay version 3.10.01
+ MAYAVERSION:2015 vrayformaya 3.10.01 O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015
PATH +:= bin
VRAY_FOR_MAYA2015_PLUGINS_x64 = O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\vrayplugins;
VRAY_FOR_MAYA2015_MAIN_x64 = O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015
VRAY_FOR_MAYA2015_PLUGINS_x64 = O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\vrayplugins
VRAY_OSL_PATH_MAYA2015_x64 = O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\Chaos Group\opensl
VRAY_TOOLS_MAYA2015_x64 = O:\hq_tool\Maya\Vray\vray_3.10.01_Maya2015\Chaos Group\bin

//shave Version 9.0v24
+ MAYAVERSION:2015 shaveHaircut 1.1 O:\hq_tool\Maya\Shave\shave_1.1_maya2015
RLM_LICENSE +:= rlm
PATH +:= bin



//fisheye for mentalray
+ MAYAVERSION:2015 Mayatomr any C:\Program Files\Autodesk\mentalrayForMaya2015
MAYA_MR_STARTUP_DIR = O:\hq_tool\Maya\Mentalray\mentalray_for_maya2015
MI_CUSTOM_SHADER_PATH = O:\hq_tool\Maya\Mentalray\mentalray_for_maya2015\shaders
MI_LIBRARY_PATH = O:\hq_tool\Maya\Mentalray\mentalray_for_maya2015\shaders\include

//anzobinRigNodes
+ MAYAVERSION:2015 anzobinRigNodes any O:\hq_tool\Maya\AnzobinRigNodes
[r] scripts: .\scripts

//realflow
+ MAYAVERSION:2015 realflow 2014.0.1 O:\hq_tool\Maya\Realflow


//hq_tool
+ MAYAVERSION:2015 hq_maya any O:\hq_tool\Maya\hq_maya
[r] icons: .\hq_icons
[r] scripts: .\scripts

//Maya 2017