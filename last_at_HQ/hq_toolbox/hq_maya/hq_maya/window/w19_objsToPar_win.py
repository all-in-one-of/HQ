# -*- coding: utf-8 -*-
import os
if os.path.exists( r'\\10.99.1.6\Digital\Library\hq_toolbox' )==False and os.path.exists(r'\\XMFTDYPROJECT\digital\film_project\Tool\hq_toolbox')==False :
    raise IOError()
#####################################################################################



import maya.cmds as cmds
import qsMaya as qm

class w19_objsToPar_win(object):
    
    _menuStr = '''{'path':'Dynamics/Particles/w19_objsToPar_win( )',
'icon':':/particle.svg',
'tip' : '每个物体中间放置一下粒子',
'usage':'$fun( )',
}
'''
    def __init__(self):
        windowName = 'objsToPar_win'
        if cmds.window( windowName, exists=True):
            cmds.deleteUI( windowName)
            
        cmds.window(windowName, title="w19_objsToPar_win", sizeable=0)
        cmds.columnLayout(adj=True)
        cmds.textFieldButtonGrp( 'w19_parName', label='nParticle Node', text='new', buttonLabel='Get from sel', h=40, ed=False, cw3=(80,150,80), bc=self.w19_parName  )
        cmds.checkBox('w19_initialState', l='Initial State', v=True, h=40)
        cmds.button( 'w19_do', label='Objects to particles', h=40, c=self.w19_do_cmd  )
        cmds.showWindow( windowName )

    def w19_parName(self, *args):
        par = cmds.ls(sl=True, exactType='nParticle')
        if par==[]:
            if cmds.ls(sl=True):
                par = cmds.listRelatives( cmds.ls(sl=True), ad=True, type='nParticle', f=True)
                if par!=[]:
                   cmds.textFieldButtonGrp( 'w19_parName', e=True, text=par[0] )
                else: cmds.textFieldButtonGrp( 'w19_parName', e=True, text='new' )
            else: cmds.textFieldButtonGrp( 'w19_parName', e=True, text='new' )           
        else:
           cmds.textFieldButtonGrp( 'w19_parName', e=True, text=par[0] )
    
    def w19_do_cmd(self, *args):
        parName = cmds.textFieldButtonGrp( 'w19_parName', q=True, text=True)
        initialState = cmds.checkBox('w19_initialState', q=True, v=True)
        qm.objsToPar(parName, initialState)
