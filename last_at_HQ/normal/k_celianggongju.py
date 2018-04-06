#coding:utf-8
import maya.cmds as cc
import sys,shutil,math

if  cc.window('k_dengtao',exists=True):
    cc.deleteUI('k_dengtao',window=True)
cc.window('k_dengtao',title="拍摄相机流程辅助面板_k")

cc.columnLayout(adjustableColumn=1)
cc.text(label='')
cc.button(label='为人物修改颜色',h=40,command='matren()')
cc.button(label='为道具修改颜色',h=40,command='matdj()')
cc.button(label='为群众修改颜色',h=40,command='matqz()')
cc.text(label='')

cc.floatFieldGrp('k_gaodu',label='离地高度:',pre=5,extraLabel='',enable=True)

cc.button(label='选择相机_first',h=50,command='k_selcam()')

cc.button(label='选择测量物体_first',h=50,command='k_selwuti()')



cc.button(label='转移至坐标原点_first',h=50,command='k_move()')
cc.text(label='')
cc.button(label='选择相机_end',h=50,command='k_selcam2()')

cc.button(label='选择测量物体_end',h=50,command='k_selwuti2()')

cc.button(label='转移至坐标原点_end',h=50,command='k_move2()')

cc.text(label='')
cc.button(label='创建Locator的坐标',h=50,command='k_ann()')
cc.text(label='')
cc.button(label='创建相机显示窗口',h=50,command='k_camwin()')
cc.showWindow('k_dengtao')

def k_selcam():
    global kd_cam
    global k_ffs
    k_cam=cc.ls(sl=1)
    k_cams=cc.listRelatives(k_cam[0],f=1)
    k_type=cc.nodeType(k_cams)
    
    if not cc.objExists('first_frame_scenes'):
        k_ffs=cc.createNode('transform',n="first_frame_scenes")
    
    if k_type=="camera" and len(k_cam)==1:
        kd_cam=cc.duplicate(k_cam,rc=1,rr=1,n=("k_"+k_cam[0]))
        cc.setAttr (kd_cam[0]+".tx",l=0)
        cc.setAttr (kd_cam[0]+".ty",l=0) 
        cc.setAttr (kd_cam[0]+".tz",l=0) 
        cc.setAttr (kd_cam[0]+".rx",l=0) 
        cc.setAttr (kd_cam[0]+".ry",l=0) 
        cc.setAttr (kd_cam[0]+".rz",l=0) 
        cc.setAttr (kd_cam[0]+".sx",l=0)
        cc.setAttr (kd_cam[0]+".sy",l=0)
        cc.setAttr (kd_cam[0]+".sz",l=0) 
        for kd_camd in kd_cam:
            cc.parent(kd_camd,'first_frame_scenes')
            
def k_selcam2():
    global kd_cam2
    global k_ffs2
    k_cam=cc.ls(sl=1)
    k_cams=cc.listRelatives(k_cam[0],f=1)
    k_type=cc.nodeType(k_cams)
    
    if not cc.objExists('end_frame_scenes'):
        k_ffs2=cc.createNode('transform',n="end_frame_scenes")
    
    if k_type=="camera" and len(k_cam)==1:
        kd_cam2=cc.duplicate(k_cam,rc=1,rr=1,n=("k_"+k_cam[0]))
        cc.setAttr (kd_cam2[0]+".tx",l=0)
        cc.setAttr (kd_cam2[0]+".ty",l=0) 
        cc.setAttr (kd_cam2[0]+".tz",l=0) 
        cc.setAttr (kd_cam2[0]+".rx",l=0) 
        cc.setAttr (kd_cam2[0]+".ry",l=0) 
        cc.setAttr (kd_cam2[0]+".rz",l=0) 
        cc.setAttr (kd_cam2[0]+".sx",l=0)
        cc.setAttr (kd_cam2[0]+".sy",l=0)
        cc.setAttr (kd_cam2[0]+".sz",l=0) 
        for kd_camd in kd_cam2:
            cc.parent(kd_camd,'end_frame_scenes')
            
    
def k_selwuti():
    global k_dds
    global k_ffs
    k_meshs=cc.ls(sl=1)
    
    if not cc.objExists('first_frame_scenes'):
        k_ffs=cc.createNode('transform',n="first_frame_scenes")
    
    for k_mesh in k_meshs:
        k_dds=cc.duplicate(k_mesh,rc=1,rr=1,n=("k_"+k_mesh))
        for k_dd in k_dds:
            cc.parent(k_dd,'first_frame_scenes')

def k_selwuti2():
    global k_dds2
    global k_ffs2
    k_meshs=cc.ls(sl=1)
    
    if not cc.objExists('end_frame_scenes'):
        k_ffs2=cc.createNode('transform',n="end_frame_scenes")
    
    for k_mesh in k_meshs:
        k_dds2=cc.duplicate(k_mesh,rc=1,rr=1,n=("k_"+k_mesh))
        for k_dd in k_dds2:
            cc.parent(k_dd,'end_frame_scenes')
            

def k_move():
    global k_css
    global k_ffs
    if cc.objExists('cam_scenes_first'):
        cc.delete('cam_scenes_first')
        k_css=cc.createNode('transform',n="cam_scenes_first")
    else :
        k_css=cc.createNode('transform',n="cam_scenes_first")
    
    k_pointCon=cc.pointConstraint(kd_cam[0],k_css)
    cc.delete(k_pointCon)   
    
    cc.parent(k_ffs,k_css)
    
    if cc.objExists('cam_sceness_first'):
        cc.delete('cam_sceness_first')
        k_csc=cc.createNode('transform',n="cam_sceness_first")
    else :
        k_csc=cc.createNode('transform',n="cam_sceness_first")
         
    cc.parent(k_css,k_csc)
    
    k_pointCo=cc.pointConstraint(k_csc,k_css)
    cc.delete(k_pointCo)
    cc.parent("cam_scenes_first",w=1)
    cc.delete(k_csc)
    
    k_lidigaodu=cc.floatFieldGrp('k_gaodu',value1=True,q=True)
    
    k_rc=cc.getAttr(kd_cam[0]+".ry")
    cc.setAttr(k_css+".ry",-k_rc)
    
    cc.setAttr(k_css+".ty",k_lidigaodu)
    

def k_move2():
    global k_css2
    global k_ffs2
    if cc.objExists('cam_scenes_end'):
        cc.delete('cam_scenes_end')
        k_css2=cc.createNode('transform',n="cam_scenes_end")
    else :
        k_css2=cc.createNode('transform',n="cam_scenes_end")
    
    k_pointCon=cc.pointConstraint(kd_cam2[0],k_css2)
    cc.delete(k_pointCon)   
    
    cc.parent(k_ffs2,k_css2)
    print k_css2
    
    if cc.objExists('cam_sceness_end'):
        cc.delete('cam_sceness_end')
        k_csc=cc.createNode('transform',n="cam_sceness_end")
    else :
        k_csc=cc.createNode('transform',n="cam_sceness_end")
    
    print k_css2     
    cc.parent(k_css2,k_csc)
    k_pointCo=cc.pointConstraint(k_csc,k_css2)
    cc.delete(k_pointCo)
    cc.parent("cam_scenes_end",w=1)
    cc.delete(k_csc)
    
    k_lidigaodu=cc.floatFieldGrp('k_gaodu',value1=True,q=True)
    
    k_rc=cc.getAttr(kd_cam2[0]+".ry")
    cc.setAttr(k_css2+".ry",-k_rc)
    
    cc.setAttr(k_css2+".ty",k_lidigaodu)
   
    
    


def k_ann():
    k_locas=cc.ls(sl=1)
    
    for k_loca in k_locas:
        k_locass=cc.listRelatives(k_loca)
        if cc.nodeType(k_locass)=="locator":
            kl_tx=cc.getAttr(k_loca+".tx")
            kl_ty=cc.getAttr(k_loca+".ty")
            kl_tz=cc.getAttr(k_loca+".tz")        
            kl_tya=abs(kl_ty)
            kl_tza=abs(kl_tz)
            kl_txt=str(kl_tx)
            kl_tyt=str(kl_tya)
            kl_tzt=str(kl_tza)
            
            kt_zuobiao=cc.annotate (k_loca,tx='('+kl_txt[0:5]+','+kl_tzt[0:4]+','+kl_tyt[0:4]+')')
            kr_zuobiao=cc.listRelatives(kt_zuobiao,p=1)
            kpc_zuobaio=cc.pointConstraint(k_loca,kr_zuobiao)
            cc.delete(kpc_zuobaio)
        
        
        
def matren():
    k_sels=cc.ls(sl=1) 
    if not cc.objExists('kMskSG_r'):
        cc.sets(n='kMskSG_r',empty=1,renderable=1,noSurfaceShader=1)
        
    if not cc.objExists('kMskShader_r'):
        cc.shadingNode('surfaceShader',asShader=1,n='kMskShader_r')
        cc.setAttr('kMskShader_r.outColor',1,0,0,type='double3')
        
    if not cc.isConnected('kMskShader_r.outColor','kMskSG_r.surfaceShader'):
        cc.connectAttr('kMskShader_r.outColor','kMskSG_r.surfaceShader',f=1) 
        
    
    cc.sets(k_sels,e=1,fe='kMskSG_r')


def matdj():
    k_sels=cc.ls(sl=1) 
    if not cc.objExists('kMskSG_b'):
        cc.sets(n='kMskSG_b',empty=1,renderable=1,noSurfaceShader=1)
        
    if not cc.objExists('kMskShader_b'):
        cc.shadingNode('surfaceShader',asShader=1,n='kMskShader_b')
        cc.setAttr('kMskShader_b.outColor',0,0,1,type='double3')
        
    if not cc.isConnected('kMskShader_b.outColor','kMskSG_b.surfaceShader'):
        cc.connectAttr('kMskShader_b.outColor','kMskSG_b.surfaceShader',f=1) 
        
    
    cc.sets(k_sels,e=1,fe='kMskSG_b')

def matqz():
    k_sels=cc.ls(sl=1) 
    if not cc.objExists('kMskSG_p'):
        cc.sets(n='kMskSG_p',empty=1,renderable=1,noSurfaceShader=1)
        
    if not cc.objExists('kMskShader_p'):
        cc.shadingNode('surfaceShader',asShader=1,n='kMskShader_p')
        cc.setAttr('kMskShader_p.outColor',.2,0,.3,type='double3')
        
    if not cc.isConnected('kMskShader_p.outColor','kMskSG_p.surfaceShader'):
        cc.connectAttr('kMskShader_p.outColor','kMskSG_p.surfaceShader',f=1) 
        
    
    cc.sets(k_sels,e=1,fe='kMskSG_p')
    
    
def k_camwin():
    k_camt=cc.ls(sl=1,l=1)
    
    k_camtss=cc.ls(sl=1)
    
    k_camst=cc.listRelatives(k_camt[0],f=1)
    k_typec=cc.nodeType(k_camst)
    
    
    if k_typec=="camera" and len(k_camt)==1:
        k_camn=k_camt[0].replace('|','_')
        if  cc.window(k_camn,exists=True):
            cc.deleteUI(k_camn,window=True)
        cc.window(k_camn,title="dengtao的测试窗口")   
        cc.paneLayout()
        cc.modelPanel(cam=k_camt[0])
        print "ha"
        cc.window(k_camn,e=1,wh=(960,640))
        cc.showWindow(k_camn)
    
      
    
    
    
    
    
    
    