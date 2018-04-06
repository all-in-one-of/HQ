# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################

import maya.cmds as cmds
import os, re

#---------------w13_CachePathHelper
class w13_CachePathHelper(object):
    _menuStr = '''{'path':'Cache/w13_CachePathHelper()',
'icon':':/replaceCache.png',
'tip' : '检查设置缓存路径的工具',
'html':True,
'usage':'$fun()',
}
'''   
    def __init__(self):
        #[0:uiName, 1:pluginName, 2:get, 3:set]
        self.__nodeAttrs = { 
                            'cacheFile':        [None,               self.__get_cacheFile,   self.__set_cacheFile ],
                            'AlembicNode':      ["AbcImport.mll",    self.__get_AlembicNode, self.__set_AlembicNode ],
                            'miProxy':          ['Mayatomr.mll',     self.__get_miProxy,     self.__set_miProxy ],
                            'aiStandIn':        ['mtoa.mll',         self.__get_aiStadin,    self.__set_aiStadin ],
                            'VRayMesh':         ['vrayformaya.mll',  self.__get_VRayMesh,    self.__set_VRayMesh ]
                    }
        self.__typeForSort = ('cacheFile', 'AlembicNode', 'miProxy', 'VRayMesh', 'aiStandIn' )

        self.__loadedNodes = []
        for k, v in self.__nodeAttrs.iteritems():
            pluginName = v[0]
            if not pluginName or\
                    ( pluginName and cmds.pluginInfo( pluginName, query=True, registered=True) and cmds.pluginInfo( pluginName, query=True, loaded=True)  ):
               self.__loadedNodes.append( k )

        self.allCaches = {}


        windowName = 'w13_CachePathHelper'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
        sceneName = cmds.file(q=True,sn=True,shortName=True).split('.')[0] 
        cmds.window(windowName, title="w13_CachePathHelper", sizeable=1)
        cmds.columnLayout("w13_L01", p=windowName, adj=True)
        cmds.button( 'w13_uiReset', p="w13_L01", label="Get", h=40, c=self.__getAllCache  )
        cmds.textFieldButtonGrp( 'w13_uiFindWhat', p="w13_L01", label='Find what:', buttonLabel='Workspace', cw=([1,80]), h=30, adj=2, bc='cmds.textFieldButtonGrp("w13_uiFindWhat", e=True, tx=cmds.workspace(q =True, rootDirectory=True)  )'   )
        cmds.textFieldButtonGrp( 'w13_uiRepWith', p="w13_L01", label='Replace with:', buttonLabel='Workspace',cw=([1,80]), h=30, adj=2, bc='cmds.textFieldButtonGrp("w13_uiRepWith", e=True, tx=cmds.workspace(q =True, rootDirectory=True)  )'   )
        cmds.button( 'w13_uiReplace', p="w13_L01", label="Replace", h=40, c=self.w13_uiReplace_cmd  )
        cmds.separator( height=20, style='out' )

        cmds.rowLayout( 'w13_uiTypeLay', p='w13_L01', numberOfColumns=len(self.__loadedNodes)+2  )
        cmds.text( p='w13_uiTypeLay', l='Types:\t\t')
        cmds.radioCollection( 'w13_uiTypeList', p='w13_uiTypeLay'  )
        cmds.radioButton( 'w13_uiType_All',  p='w13_uiTypeLay', l='All'  )
        #print self.__loadedNodes
        for nt in self.__typeForSort:
            if nt in self.__loadedNodes:
                cmds.radioButton( 'w13_uiType_%s'%(nt),  p='w13_uiTypeLay', l=nt+'\t', cc=self.__uiFilter_cmd  )
        cmds.radioCollection( 'w13_uiTypeList', e=True, select='w13_uiType_All')

        #cmds.radioButtonGrp(  'w13_uiFilterType', p="w13_L01", label='Type:', numberOfRadioButtons=4, cw=[(1,50)], labelArray4=self.nodeTypeList, sl=1, cc=self.__uiFilter_cmd )
        cmds.separator( p='w13_L01', height=10, style='in' )
        cmds.rowLayout( 'w13_uiDisplayOption_Lay', p='w13_L01', numberOfColumns=2 )
        cmds.text( p='w13_uiDisplayOption_Lay', l='Display:\t\t')
        cmds.radioButtonGrp( 'w13_uiNoExists', p="w13_uiDisplayOption_Lay", numberOfRadioButtons=2,  labelArray2=['All', 'No exists'], sl=1, cc=self.__uiFilter_cmd )
        cmds.separator( p='w13_L01', height=20, style='in' )
        cmds.radioButtonGrp( 'w13_uiAbsRel', p="w13_L01", l='Path display', numberOfRadioButtons=2,  labelArray2=['Absolute', 'Relative'], sl=1, cc=self.__uiFilter_cmd )
        
        
        cmds.textScrollList( 'w13_uiCaches', p="w13_L01", numberOfRows=8, allowMultiSelection=True, bgc=[.2,.2,.2], showIndexedItem=4, h=500,dcc=self.__itemDoubleClick )
        cmds.button( 'self.w13_uiSetChange', p="w13_L01", label="Set All Change", h=40, c=self.w13_uiSetChange  )
        cmds.showWindow(windowName)
        
        #global allCaches
        self.__getAllCache()
        self.__uiFilter_cmd()

    def __uiFilter_cmd(self, *args ):

        wksp = cmds.workspace(q =True, rootDirectory=True)
        showAll = True if cmds.radioButtonGrp( 'w13_uiNoExists', q=True, sl=True)==1 else False
        abs = True if cmds.radioButtonGrp( 'w13_uiAbsRel', q=True, sl=True)==1 else False
        cmds.textScrollList( 'w13_uiCaches', e=True, removeAll=True)


        tye = cmds.radioCollection( 'w13_uiTypeList', q=True, select=True ).replace( 'w13_uiType_', '')

        if tye=='All':
            for nodeTyp, cacheData in self.allCaches.items():
                #if cacheData!=None:
                for node, path in cacheData.items():
                    if showAll:
                        strPath = '%s\t%s\t\t%s'%(nodeTyp, node, path if abs else path.replace(wksp, '') )
                        strPath = strPath.replace('/', '\\')
                        cmds.textScrollList( 'w13_uiCaches', e=True, append=strPath )
                    else:
                        if not os.path.exists( path ):
                            strPath = '%s\t%s\t\t%s'%(nodeTyp, node, path if abs else path.replace(wksp, '') )
                            strPath = strPath.replace('/', '\\')
                            cmds.textScrollList( 'w13_uiCaches', e=True, append=strPath )
        else:
            cacheData = self.allCaches[tye]
            for node, path in cacheData.items():
                if showAll:
                    strPath = '%s\t\t%s'%(node, path if abs else path.replace(wksp, ''))
                    strPath = strPath.replace('/', '\\')
                    cmds.textScrollList( 'w13_uiCaches', e=True, append=strPath )
                else:
                    if os.path.exists( path )==False:
                        strPath = '%s\t\t%s'%(node, path if abs else path.replace(wksp, '') )
                        strPath = strPath.replace('/', '\\')
                        cmds.textScrollList( 'w13_uiCaches', e=True, append=strPath )




    def __get_cacheFile(self, *args):
            cacheDir = cmds.getAttr( args[0]+'.cachePath', x=True)
            xmlFile = cmds.getAttr( args[0]+'.cacheName')+'.xml'
            cacheDir, xmlFile = str(cacheDir), str(xmlFile)
            xmlPath = os.path.join( cacheDir, xmlFile).replace('\\', '/')
            return xmlPath
    

    def __get_AlembicNode(self, *args):
        cacheDir = cmds.getAttr( args[0]+'.abc_File', x=True)        
        return cacheDir
    
    def __get_miProxy(self, *args):
        miProxyFile = cmds.getAttr( args[0]+'.miProxyFile', x=True)
        return miProxyFile
    
    def __get_aiStadin(self, *args):
        assFilePath = cmds.getAttr( args[0]+'.dso', x=True )

        dirName = os.path.dirname(assFilePath)
        baseName = os.path.basename( assFilePath )
        pattern = re.match( r'[^#]+(\#+).+', assFilePath)
        if not pattern:
            
            return assFilePath
        else:
            baseName = baseName.replace( pattern.groups()[0],
                              str(
                                  int( cmds.currentTime(q=True) + cmds.getAttr(args[0]+'.frameNumber') + cmds.getAttr(args[0]+'.frameOffset')  )
                                  ).zfill( len(pattern.groups()[0])   )
                              )
            finalName = os.path.join( dirName, baseName ).replace( '\\', '/' )
            
            return finalName
    
    
    def __get_VRayMesh(self, *args):
        vrmeshCache = cmds.getAttr( args[0]+'.fileName', x=True)
        return vrmeshCache

    def __get_AllMiProxyNodes(self,*args):        
        nodes = [node for node in cmds.ls( exactType=['mesh','nurbsSurface'] ) 
                 if not cmds.getAttr( node+'.intermediateObject') and cmds.getAttr( node+'.miProxyFile', x=True)
                 ]
        return nodes

    def __itemDoubleClick(self, *args):
        item = cmds.textScrollList( 'w13_uiCaches', q=True, selectItem=True)[-1]
        if cmds.radioCollection( 'w13_uiTypeList', q=True, select=True ).replace( 'w13_uiType_', '')=='All':
            cmds.select(item.split('\t')[1], r=True)
        else:
            cmds.select( item.split('\t')[0], r=True) 
            
    
    def w13_uiReplace_cmd(self, *args):
        typ = cmds.radioCollection( 'w13_uiTypeList', q=True, select=True ).replace( 'w13_uiType_', '')
        showAll = True if cmds.radioButtonGrp( 'w13_uiNoExists', q=True, sl=True)==1 else False
        #cmds.textScrollList( 'w13_uiCaches', e=True, removeAll=True)
        findStr = cmds.textFieldGrp( 'w13_uiFindWhat', q=True, tx=True).replace('\\', '/')
        repWithStr = cmds.textFieldGrp( 'w13_uiRepWith', q=True, tx=True).replace('\\', '/')
        if findStr=='':
            return False
            
        if typ=='All':
            for nodeTyp, cacheData in self.allCaches.items():
                if cacheData!=None:
                    for node, path in cacheData.items():
                        if showAll==False:
                            if os.path.exists( path )==False and findStr in path:
                                self.allCaches[nodeTyp][node] = path.replace( findStr, repWithStr )
                        else:
                            self.allCaches[nodeTyp][node] = path.replace( findStr, repWithStr )                       
        else:
            if self.allCaches[typ]!=None:
                cacheData=self.allCaches[typ]
                for node, path in cacheData.items():
                    if showAll==False:
                        if os.path.exists( path )==False and findStr in path:
                            self.allCaches[nodeTyp][node] = path.replace( findStr, repWithStr )
                    else:
                        self.allCaches[typ][node] = path.replace( findStr, repWithStr )
        self.__uiFilter_cmd()
        


    def __getAllCache( self, *args, **kwargs ):
        self.allCaches = {}
        for nt in self.__loadedNodes:
            self.allCaches[nt] = {}
            if nt=='miProxy':
                nodes = self.__get_AllMiProxyNodes()
            else:
                nodes = cmds.ls( exactType=nt )
            
            for node in nodes:
                #print self.__nodeAttrs[nt][1](node)
                self.allCaches[nt][node] = self.__nodeAttrs[nt][1](node)
        self.__uiFilter_cmd
    
    
    def __set_cacheFile(self, *args):
        node, oriPath, newPath = args
        if os.path.exists(newPath) and oriPath!=newPath and newPath.endswith('.xml'):
            tmp, tmp01 = os.path.split( newPath )
            tmp=tmp+'/'
            tmp01 = tmp01.replace( '.xml', '')
            
            cmds.setAttr( node+'.cachePath', tmp, type='string')
            cmds.setAttr( node+'.cacheName', tmp01, type='string')
    
    def __set_AlembicNode(self, *args):
        node, oriPath, newPath = args
        if os.path.exists(newPath) and oriPath!=newPath and newPath.endswith('.abc'):
            cmds.setAttr( node+'.abc_File', newPath, type='string')
    def __set_miProxy(self, *args):
        node, oriPath, newPath = args
        if os.path.exists(newPath) and oriPath!=newPath and newPath.endswith('.mi'):
            cmds.setAttr( node+'.miProxyFile', newPath, type='string')
      
    def __set_aiStadin(self, *args):
        node, oriPath, newPath = args
        if os.path.exists(newPath) and oriPath!=newPath and (newPath.endswith('.ass') or newPath.endswith('.ass.gz')):                    
            cmds.setAttr( node+'.dso', newPath, type='string' )
    
    def __set_VRayMesh(self, *args):
        node, oriPath, newPath = args
        print newPath, os.path.exists( newPath )
        if os.path.exists( newPath ) and oriPath!=newPath and newPath.endswith('.vrmesh' ):
            vrmeshCache = cmds.setAttr( node+'.fileName2', newPath, type='string' )
        
    
    
    def w13_uiSetChange(self, *args ):    
        
        for typ, cacheData in self.allCaches.iteritems():
            for node, newPath in cacheData.iteritems():
                oriPath = self.__nodeAttrs[typ][1]( node ) 
                oriPath, newPath = os.path.abspath( oriPath ), os.path.abspath( newPath )               
                self.__nodeAttrs[typ][2]( node, oriPath, newPath )
         
                        
        self.__getAllCache()    
        self.__uiFilter_cmd()
    
    
    #------------w13_End---------------------------------------------
    
#w13_CachePathHelper()