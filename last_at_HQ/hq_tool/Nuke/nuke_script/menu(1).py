# -*- coding: UTF-8 -*- 
import os
import toolbars
import xufei
import DeadlineNukeClient
import AutoClear
import FootageCopy
import nuke
import os.path
import time,user_presets
import FootageCopy_v01
import shutil,math,threading

nuke.menu("Nuke").addCommand("Render/Render", "nuke.tcl('set nodes [nodes]; catch {set nodes [selected_nodes]}; render $nodes')", "alt+F5", index=2)

tb = menubar.addMenu("&Thinkbox") 
tb.addCommand("DeadlineNukeClient", DeadlineNukeClient.main, "")


# Define the tool menus. This file is loaded by menu.py.



# This is not currently used but when we support a text-only mode we'll need it.

#size = nuke.numvalue("preferences.toolbarTextSize")



# Get the top-level toolbar

toolbar = nuke.menu("Nodes")



n = nuke.toolbar("Nodes")

m = toolbar.addMenu("X_Click", icon="X_Click.png")

m.addCommand("X_checkFrames", "X_checkFrames()", "x")

m.addCommand("X_expandChannels", "X_expandChannels()", "E")

m.addCommand("@;X_expandChannels_v", "X_expandChannels_v()", "Shift+E",)

m.addCommand("batchReads","nuke.batchReads()")

m.addCommand("PRVBatchWaterMarks","batchRenderForPRV.batchWaterMarks()")

m.addCommand("MatchPlatform","matchPlatform()")

m.addCommand("OpenFileDirectory","OpenFileDirectory()","Alt+D")

m.addCommand("@;X_shuffle_R", "X_shuffle_R()", "Alt+R",)

m.addCommand("@;X_shuffle_G", "X_shuffle_G()", "Alt+G",)

m.addCommand("@;X_shuffle_B", "X_shuffle_B()", "Alt+B",)

m.addCommand("@;X_shuffle_A", "X_shuffle_A()", "Alt+A",)

m.addCommand("AutoSplit", "AutoSplit()", "Alt+v",)

m.addCommand("AutoClearNodes", "AutoClearNodes()", "Alt+c",)

m.addCommand("AutoSixViews_v2", "AutoSixViews_v2()", "Alt+h",)

m.addCommand("AutoSingleView", "AutoSingleView()", "Alt+q",)

m.addCommand("AutoSixViews", "AutoSixViews()", "Alt+w",)

m.addCommand("FootageClear", "FootageCopyClear()")

m.addCommand("FootageClear_v01", "FootageCopyClear_v01()")

m.addCommand("renamefile", "renamefile()")

m.addCommand("AutoWrite", "AutoWrite()")

m.addCommand("Autofile", "Autofile()")

m.addCommand("Collect", "Collect()")

m.addCommand("thesameformat", "thesameformat()")

m.addCommand("thesameframe", "thesameframe()")

m.addCommand("Relative_Path", "Relative_Path()")

m.addCommand("Relative_Path_rename", "Relative_Path_rename()")

m.addCommand("AutoCreatproject", "AutoCreatproject()", "u",)

m.addCommand("copyplates", "copyplates()")

m.addCommand("jumusingleview", "jumusingleview()","shift+a")

m.addCommand("huanmusingleview", "huanmusingleview()","shift+q")

m.addCommand("FootageCopyClear_move", "FootageCopyClear_move()")

m.addCommand("Autofindfile", "Autofindfile()","Alt+F")



# X_plugins by Felix 

m = toolbar.addMenu("X_plugin", icon="X_plugins.png")



# Filter

n = m.addMenu("Filter")

n.addCommand("X_FilmGrain","nuke.createNode(\"X_FilmGrain\")",icon="X_plugins.png")



# Channel

n = m.addMenu("Channel")

n.addCommand("He_RGBlayer","nuke.createNode(\"He_RGBlayer\")",icon="X_plugins.png")

n.addCommand("X_LgtPassRGB","nuke.createNode(\"X_LgtPassRGB\")",icon="X_plugins.png")

m.addCommand("RGB_to_alpha","nuke.createNode(\"RGB_to_alpha\")")



# 2D-image

n = m.addMenu("2D-image")

n.addCommand("X_nanPixels","nuke.createNode(\"X_nanPixels\")",icon="X_plugins.png")

n.addCommand("X_Slate","nuke.createNode(\"X_Slate\")",icon="X_plugins.png")

n.addCommand("X_SlateCAR","nuke.createNode(\"X_Slate_CAR-4\")",icon="X_plugins.png")

n.addCommand("X_WaterMarks","nuke.createNode(\"X_WaterMarks2\")",icon="X_plugins.png")

n.addCommand("X_WaterMarksCAR_Tga","nuke.createNode(\"X_WaterMarksCAR-2\")",icon="X_plugins.png")

n.addCommand("X_WaterMarksCAR_Dpx","nuke.createNode(\"X_WaterMarksCAR-3_Dpx\")",icon="X_plugins.png")

n.addCommand("X_WaterMarks_PRV","nuke.createNode(\"X_WaterMarks_prv2\")",icon="X_plugins.png")



n.addCommand("X_AspectRatioMark","nuke.createNode(\"X_AspectRatioMark\")",icon="X_plugins.png")

n.addCommand("X_Cropping","nuke.createNode(\"X_Cropping_v02\")")



# 3D-Comp

n = m.addMenu("3D-Comp")

n.addCommand("X_IDmsk","nuke.createNode(\"X_IDmsk\")",icon="X_plugins.png")

n.addCommand("X_LgtComp","nuke.createNode(\"X_LgtComp\")",icon="X_plugins.png")

n.addCommand("X_RoundLgt","nuke.createNode(\"X_RoundLgt\")",icon="X_plugins.png")



# 3D-Stereo

n = m.addMenu("3D-Stereo")

n.addCommand("X_RelightX","nuke.createNode(\"X_RelightX\")",icon="X_plugins.png")

n.addCommand("X_Stereo3DcamRig","nuke.createNode(\"X_Stereo3DcamRig\")",icon="X_plugins.png")

n.addCommand("X_Stereo3Dglasses","nuke.createNode(\"X_Stereo3Dglasses\")",icon="X_plugins.png")

n.addCommand("X_stereo3DprojectorFanta","nuke.createNode(\"X_stereo3DprojectorFanta\")",icon="X_plugins.png")

n.addCommand("X_stereo_camera","nuke.createNode(\"X_stereo_camera\")",icon="X_plugins.png")

n.addCommand("X_stereo_camera_v02","nuke.createNode(\"X_stereo_camera_v02\")",icon="X_plugins.png")

m.addCommand("LRview","nuke.createNode(\"LRview\")",icon="JoinViews.png")


# VideoCopilot

m = toolbar.addMenu("VideoCopilot", icon="VideoCopilot.png")

m.addCommand( "VideoCopilot/OpticalFlares", "nuke.createNode('OpticalFlares')", icon="OpticalFlares.png")

m.addCommand("StarProNK","nuke.createNode(\"StarProNK\")")


# jianggx gizmo

m = toolbar.addMenu("jianggx", icon="jianggx.png")

m.addCommand("i_Slate","nuke.createNode(\"i_Slate\")")

m.addCommand("i_WaterMark","nuke.createNode(\"i_WaterMark\")")

m.addCommand("i_One","nuke.createNode(\"i_One\")")

m.addCommand("HeatHaze","nuke.createNode(\"HeatHaze\")")

m.addCommand("slate","nuke.createNode(\"slate\")")

m.addCommand("X_Sharpen","nuke.createNode(\"X_Sharpen\")")

m.addCommand("id","nuke.createNode(\"id\")")

m.addCommand("seven_viewer","nuke.createNode(\"seven_viewer\")")

m.addCommand("X_pingmuzhuanhuan","nuke.createNode(\"X_pingmuzhuanhuan\")")

m.addCommand("X_huanmu","nuke.createNode(\"X_huanmu\")")

m.addCommand("X_RenderBoth","nuke.createNode(\"X_RenderBoth\")")

m.addCommand("X_shadow3D","nuke.createNode(\"X_shadow3D\")")

m.addCommand("X_meter","nuke.createNode(\"X_meter\")")

m.addCommand("jumu_viewer_cg","nuke.createNode(\"jumu_viewer_cg\")")

m.addCommand("jumu_viewer_shipai","nuke.createNode(\"jumu_viewer_shipai\")")

m.addCommand("X_360zhuanping","nuke.createNode(\"X_360zhuanping\")")

m.addCommand("X_pingmu180","nuke.createNode(\"X_pingmu180\")")

m.addCommand("X_pingmu180_v01","nuke.createNode(\"X_pingmu180_v01\")")

m.addCommand("X_pingmu180_v02","nuke.createNode(\"X_pingmu180_v02\")")

m.addCommand("X_pingmu360","nuke.createNode(\"X_pingmu360\")")

m.addCommand("X_pingmu360_v01","nuke.createNode(\"X_pingmu360_v01\")")

m.addCommand("Huan_360_6P","nuke.createNode(\"Huan_360_6P\")")

m.addCommand("Huan_360_zhuan","nuke.createNode(\"Huan_360_zhuan\")")

m.addCommand("Huan_Cam_text","nuke.createNode(\"Huan_Cam_text\")")

m.addCommand("Randomizer","nuke.createNode(\"Randomizer\")")

m.addCommand("H_Normal_Light","nuke.createNode(\"H_Normal_Light\")")

m.addCommand("H_ScreensMerge","nuke.createNode(\"H_ScreensMerge\")")

m.addCommand("H_SixScreenMask","nuke.createNode(\"H_SixScreenMask\")")

m.addCommand("H_VectorBlur","nuke.createNode(\"H_VectorBlur\")")

m.addCommand("H_VectorBlur_FixVector","nuke.createNode(\"H_VectorBlur_FixVector\")")

m.addCommand("dk_hair_keyer","nuke.createNode(\"dk_hair_keyer\")")

m.addCommand("akromatism_stRub","nuke.createNode(\"akromatism_stRub\")")

m.addCommand("Bezier", "nuke.createNode(\"Bezier\")","p", icon="Bezier.png")

m.addCommand("H_EdgeFX","nuke.createNode(\"H_EdgeFX\")")

m.addCommand("H_IBlur","nuke.createNode(\"H_IBlur\")")

m.addCommand("H_Maskingwide","nuke.createNode(\"H_Maskingwide\")")

m.addCommand("Paint", "nuke.createNode(\"Paint\")", icon="Paint.png")

m.addCommand("X_ColorSpill","nuke.createNode(\"X_ColorSpill\")")

m.addCommand("X_ball_jiaozheng_v01","nuke.createNode(\"X_ball_jiaozheng_v01\")")

m.addCommand("VR","nuke.createNode(\"VR\")")

m.addCommand("X_AutoFlare","nuke.createNode(\"X_AutoFlare\")")

m.addCommand("Draw/FlareFactory Plus", "nuke.createNode(\"FlareFactory_Plus\")", icon="FlareFactoryPlus.png")

m.addCommand("RotateNomals", "nuke.createNode(\"RotateNomals\")")

m.addCommand("Track_move", "nuke.createNode(\"Track_move\")")

m.addCommand("watermasks", "nuke.createNode(\"watermasks\")")

m.addCommand("PFBarrel", "nuke.createNode(\"PFBarrel\")")







toolbar.addMenu("FXXF",icon="FF.png")

toolbar.addCommand("FXXF/JZ/FHCQ_Canon15mm_JZ","nuke.createNode('FHCQ_Canon15mm_JZ')")

toolbar.addCommand("FXXF/JZ/FHCQ_Noffset_JZ","nuke.createNode('FHCQ_Noffset_JZ')")

toolbar.addCommand("FXXF/JZ/FHCQ_Offset_JZ","nuke.createNode('FHCQ_Offset_JZ')")

toolbar.addCommand("FXXF/JZ/FHCQ_UV_jz","nuke.createNode('FHCQ_UV_jz')")

toolbar.addCommand("FXXF/JZ/FHCQ_six_to_one","nuke.createNode('FHCQ_six_to_one')")

#toolbar.addCommand("FXXF/JZ/Noffset_test","nuke.createNode('Noffset_test')")

m.addCommand("Voxel/V_Average",           "nuke.createNode('V_Average.gizmo')",   icon="V_Average.png")
m.addCommand("Voxel/V_Erode",             "nuke.createNode('V_Erode.gizmo')",     icon="V_Erode.png")
m.addCommand("Voxel/V_Grid",              "nuke.createNode('V_Grid.gizmo')",      icon="V_Grid.png")
m.addCommand("Voxel/V_Light Directional", "nuke.createNode('V_DirLight.gizmo')",  icon="V_DirLight.png")
m.addCommand("Voxel/V_Light Environment", "nuke.createNode('V_EnvLight.gizmo')",  icon="V_EnvLight.png")
m.addCommand("Voxel/V_Light Point",       "nuke.createNode('V_PtLight.gizmo')",   icon="V_PtLight.png")
m.addCommand("Voxel/V_Noise",             "nuke.createNode('V_Noise.gizmo')",     icon="V_Noise.png")
m.addCommand("Voxel/V_Preview",           "nuke.createNode('V_Preview.gizmo')",   icon="V_Preview.png")
m.addCommand("Voxel/V_Render",            "nuke.createNode('V_Render.gizmo')",    icon="V_Render.png")
m.addCommand("Voxel/V_Shape",             "nuke.createNode('V_Shape.gizmo')",     icon="V_Shape.png")
m.addCommand("Voxel/V_Transform",         "nuke.createNode('V_Transform.gizmo')", icon="V_Transform.png")


# Click plugins by Felix





# Change hotKey

def X_shuffle_R():

  sh = nuke.createNode("Shuffle")

  sh['label'].setValue("Red")

  sh['red'].setValue('red')

  sh['green'].setValue('red')

  sh['blue'].setValue('red')

  sh['alpha'].setValue('red')



def X_shuffle_G():

  sh = nuke.createNode("Shuffle")

  sh['label'].setValue("Green")

  sh['red'].setValue('green')

  sh['green'].setValue('green')

  sh['blue'].setValue('green')

  sh['alpha'].setValue('green')


def X_shuffle_B():

  sh = nuke.createNode("Shuffle")

  sh['label'].setValue("Blue")

  sh['red'].setValue('blue')

  sh['green'].setValue('blue')

  sh['blue'].setValue('blue')

  sh['alpha'].setValue('blue')



def X_shuffle_A():

  sh = nuke.createNode("Shuffle")

  sh['label'].setValue("Alpha")

  sh['red'].setValue('alpha')

  sh['green'].setValue('alpha')

  sh['blue'].setValue('alpha')

  sh['alpha'].setValue('alpha')



#_______________________________________#



# X_checkFrames



def X_checkFrames():

  node = nuke.selectedNodes()

  ln = len(node)

  ls = []

  for i in xrange(ln) :

    x = node[i]

    startF = x.firstFrame()

    endF = x.lastFrame()

    for m in xrange(int(startF), int(endF) + 1):

      nuke.frame(m)

      if x.error() == True :

        ls.append(m)

        tls = tuple(ls)

        x['label'].setValue("Missing frame :" + str(tls))

      elif len(ls) == 0 :

        x['label'].setValue("I'm OK")



#______________________________________#


# X_expandChannels



def X_expandChannels() :

  t = nuke.selectedNode()

  dot = nuke.createNode('Dot')

  dot['xpos'].setValue(t.xpos() + 35)

  dot['ypos'].setValue(t.ypos() + 100)

  l = nuke.layers(t)

  max = len(l)

  m = 0

  n = -400



  while m < max:

    m = m + 1

    n = n + 100

    if m == 2:

      continue

    if m == max:

      break

    a = nuke.createNode('Shuffle')

    a['label'].setValue(l[m])

    a['in'].setValue(l[m])

    a['in2'].setValue('alpha')

    a['alpha'].setValue('red2')

    a.setInput(0, dot)

    if max > 4:

      a['xpos'].setValue(dot.xpos() + n)

      a['ypos'].setValue(dot.ypos() + 80)



##########



def X_expandChannels_v() :

  t = nuke.selectedNode()

  l = nuke.layers(t)

  dot = nuke.createNode('Dot')

  dot['xpos'].setValue(t.xpos() + 100)

  dot['ypos'].setValue(t.ypos() + 32)

  max = len(l)

  m = 0

  n = -400



  while m < max:

    m = m + 1

    n = n + 100

    if m == 2:

      continue

    if m == max:

      break

    a = nuke.createNode('Shuffle')

    a['label'].setValue(l[m])

    a['in'].setValue(l[m])

    a['in2'].setValue('alpha')

    a['alpha'].setValue('red2')

    a.setInput(0, dot)

    if max > 4:

      a['xpos'].setValue(dot.xpos() + 120)

      a['ypos'].setValue(dot.ypos() + n)






#____________________________________________#





def matchPlatform():

  allNodes = nuke.allNodes()

  import platform

  if platform.system() == "Linux":

    for i in allNodes:

      if 'file' in i.knobs().keys():

        oldValue = i['file'].value()

        replaceName = oldValue.replace('\\','/')

        if 'X:/' in replaceName:

          newName = replaceName.replace('T:/','/All/')

          i['file'].setValue(newName)

        elif '192.168.100.100' in replaceName:

          newName = replaceName.split('10.99.24.44')[-1]

          i['file'].setValue(newName)

  elif platform.system() == "Windows":

    for i in allNodes:

      if 'file' in i.knobs().keys():

        oldValue = i['file'].value()

        replaceName = oldValue.replace('\\','/')

        if '192.168.100.100' in replaceName:

          newName = replaceName.split('10.99.24.44')[-1]

          newName = newName.replace('/All/','T:/')

          i['file'].setValue(newName)

        elif '/All/' in replaceName:

          newName = replaceName.replace('/All/','T:/')

          i['file'].setValue(newName)



#____________________________________________#

def AutoSplit():
    views = nuke.views()
    if len(views) < 2:
        nuke.message("Only one view, nothing to split and rejoin.")
        return
    
    sel = nuke.selectedNode()
    if sel == None:
        nuke.message("You need to select a node to split views from and rejoin.")
        return
    
    selx = sel.knob("xpos").getValue()
    sely = sel.knob("ypos").getValue()
    
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
    p=nuke.Panel('AutoSplit')
    p.addEnumerationPulldown('Screen','DanPing JuMu HuanMu')
    p.addEnumerationPulldown('file_type','jpeg exr png tiff' )
    p.addSingleLineInput('parkname','_')
    ss=p.show()
    screen = p.value('Screen')
    file_type = p.value('file_type')
    parkname = p.value('parkname')
    if ss == 1:
    
        format = nuke.root()['format'].value()
        width = format.width()
        height = format.height()
        
        a = nuke.root()['name'].value().split('/')
        b = a[-1].split('_')
        c = b[-1].split('.')
        d = b[0]+'_'+b[1]+parkname+'_'+b[4]+'_'+c[0]+'_'+date
        
        if screen == 'DanPing':
            sec = 1
        if screen == 'JuMu':
            sec = 3
        if screen == 'HuanMu':
            sec = 6
        if file_type == 'jpeg':
            g = 'jpeg'
        if file_type == 'exr':
            g = 'exr'
        if file_type == 'png':
            g = 'png'
        if file_type == 'tiff':
            g = 'tiff'
        
        else:
            pass
        cc = width/sec
        
        nodes = []
        for x in views:
            n = nuke.createNode("OneView", inpanel=False)
            n.knob("label").setValue(x)
            m=('%s' % x)
            nodes.append(n)
       
      
       
            for i in range(sec):
                k = '%d' % (i+1)
                if screen == 'DanPing':
                    t = ''
                    cam = '_'+'cam'+m[0].upper()
               
                else:
                    t = k
                    cam = '_'+'cam'+t+m[0].upper()
    
                crop = nuke.createNode("Crop",inpanel=False)
                crop.setInput(0,n)
                crop['box'].setValue([cc*i,0,cc*(i+1),height])
                crop['reformat'].setValue(1)
                crop['crop'].setValue(0)
                crop['label'].setValue(m[0].upper()+'cam'+t)
                crop['xpos'].setValue((selx+i*100-50*sec+(len(nodes)-1)*200*sec/2)-50*(sec-1))
                crop['ypos'].setValue(sely+150)
                write = nuke.createNode("Write",inpanel=False)
                write['views'].setValue(m)  
                write['file'].setValue(a[0]+'/'+a[1]+'/'+a[2]+'/'+a[3]+'/Stuff/cmp/img/filp/'+d+'/'+t+m[0].upper()+'/'+ b[0]+'_'+b[1]+parkname+'_'+b[4]+'_'+c[0]+cam+'.%05d.'+g)
                write['xpos'].setValue((selx+i*100-50*sec+(len(nodes)-1)*200*sec/2)-50*(sec-1))
                write['ypos'].setValue(sely+200)
                if g == 'jpeg':
                    write['file_type'].setValue(g)
                    write['_jpeg_quality'].setValue('1')
                if g == 'exr':
                    write['file_type'].setValue(g)
                if g == 'png':
                    write['file_type'].setValue(g)
                if g == 'tiff':
                    write['file_type'].setValue(g)
                    write['compression'].setValue('none')
        
        
        
    
        
        
        
        for idx in range(0, len(nodes)):
            nodes[idx].knob("view").setValue(idx+1)
            nodes[idx].setInput(0, sel)
            nodes[idx].knob("xpos").setValue(selx + idx * 200*sec/2 - (len(nodes)-1)*100*sec/2)
            nodes[idx].knob("ypos").setValue(sely + 100)
    
    else:
        pass





#____________________________________________#
def AutoSingleView():
    a=nuke.selectedNodes()
    dict={}
    nlist=[]
    z=0
    def Bi(str1,str2,node1,node2,num):
        def back():
            global x,y
            x=0
            for i in range(num):
           
                if str1[i] != str2[i]:
                    x+=1
                    y=i
                    return x
        print back(),y
        if back()==1:
            if str1[y].upper()=='L' and str2[y].upper()=='R' and str1[y] != str2[y]:
                return (node1,node2)
            else:
                return 0
            if str1[y].upper()=='R' and str2[y].upper()=='L' and str1[y] != str2[y]:
                return (node2,node1)
            else:
                return 0
        else:
            return 0
                     
    for i in a:
        filename=os.path.basename( i['file'].value())
        nodename=i.name()
        dict[filename]=nodename
        nlist.append(filename)
        nlist.sort()
    
    for v in nlist:
        count=len(nlist)
        vname=v.split('.')[0]
        for n in range(1,count):
            
            if len(v)==len(nlist[n]) and v!=nlist[n]:
                print v,len(v),nlist[n],len(nlist[n])
                value=Bi(v,nlist[n],dict[v],dict[nlist[n]],len(v))
                print value
                if value !=0:
                    L=nuke.toNode(value[0])
                    L.setXYpos(100,200+300*z)
                    R=nuke.toNode(value[1])
                    R.setXYpos(300,200+300*z)
                    njv=nuke.createNode("JoinViews",inpanel=False)
                    njv.setXYpos(200,300*z+300)
                    njv.setInput(0,L)
                    njv.setInput(1,R)
                    nlist.remove(nlist[n])
                    back=nuke.createNode('BackdropNode',inpanel=False)
                    back.setXYpos(90,120+300*z)
                    back['bdwidth'].setValue(300)
                    back['bdheight'].setValue(210)
                    back['label'].setValue(vname)
                    back['note_font'].setValue("Helvetica Bold")
                    back['note_font_size'].setValue(15)
                    z+=1
                    break


#____________________________________________#

def AutoSixViews():    
    p=nuke.Panel('Node')
    p.addEnumerationPulldown('Node :','X_pingmu360_v01')
    s=p.show()
    pv=p.value('Node :')
    if s==1:
        a=nuke.selectedNodes()
        c={}
        b=[]
        x=-1
        for i in a:
            i.setSelected(False)
        for i in a:
            dictname=i.name()
            basename=os.path.basename(i['file'].value())
            file=basename[:-4]
            if basename=='Thumbs.db':
                i.setSelected(True)
                nukescripts.node_delete(popupOnError=True)
            else:
                c[file]=dictname
                b.append(file)
                b.sort()
    
        for v in b:
            if '1L' in v:
                n='1L'            
            elif '2L' in v:
                n='2L'
            elif '3L' in v:
                n='3L'
            elif '4L' in v:
                n='4L'
            elif '5L' in v:
                n='5L'
            elif '6L' in v:
                n='6L'
            if '1L' in v or '2L' in v or '3L' in v or '4L' in v or '5L' in v or '6L' in v:
                v2=v.replace(n,'2L')
                v3=v.replace(n,'3L')
                v4=v.replace(n,'4L')
                v5=v.replace(n,'5L')
                v6=v.replace(n,'6L')
                v7=v.replace(n,'1R')
                v8=v.replace(n,'2R')
                v9=v.replace(n,'3R')
                v10=v.replace(n,'4R')
                v11=v.replace(n,'5R')
                v12=v.replace(n,'6R')
                if v in b:
                    x+=1
                    node1=nuke.toNode('%s' % c[v])
                    node1.setXYpos(100,100+x*400)
    
                    if v2 in b:
                        node2=nuke.toNode('%s' % c[v2])
                        node2.setXYpos(200,100+x*400)
                        
                    if v3 in b:
                        node3=nuke.toNode('%s' % c[v3])
                        node3.setXYpos(300,100+x*400)
                        
                    if v4 in b:
                        node4=nuke.toNode('%s' % c[v4])
                        node4.setXYpos(400,100+x*400)
                
                    if v5 in b:
                        node5=nuke.toNode('%s' % c[v5])
                        node5.setXYpos(500,100+x*400)
                
                    if v6 in b:
                        node6=nuke.toNode('%s' % c[v6])
                        node6.setXYpos(600,100+x*400)
    
                    if v7 in b:
                        node7=nuke.toNode('%s' % c[v7])
                        node7.setXYpos(700,100+x*400)
                        
                    if v8 in b:
                        node8=nuke.toNode('%s' % c[v8])
                        node8.setXYpos(800,100+x*400)
                        
                    if v9 in b:
                        node9=nuke.toNode('%s' % c[v9])
                        node9.setXYpos(900,100+x*400)
                
                    if v10 in b:
                        node10=nuke.toNode('%s' % c[v10])
                        node10.setXYpos(1000,100+x*400)
                
                    if v11 in b:
                        node11=nuke.toNode('%s' % c[v11])
                        node11.setXYpos(1100,100+x*400)
    
                    if v12 in b:
                        node12=nuke.toNode('%s' % c[v12])
                        node12.setXYpos(1200,100+x*400)
                
                    nodel=nuke.createNode("%s" % pv,inpanel=False)                
                    nodel.setXYpos(350,250+x*400)
                    nodel.setSelected(False)
                    noder=nuke.createNode("%s" % pv,inpanel=False)
                    noder.setXYpos(950,250+x*400)
                    noder.setSelected(False)
                    nodejv=nuke.createNode("JoinViews",inpanel=False)
                    nodejv.setXYpos(650,300+x*400)
                    nodejv.setSelected(False)
                    backnode=nuke.createNode("BackdropNode",inpanel=False)
                    backnode.setXYpos(2100,20+x*400)
                    backnode.setSelected(False)
                    nodel.setInput(0,node1)
                    if v2 in b:
                        nodel.setInput(1,node2)
                        b.remove(v2)
                    if v3 in b:
                        nodel.setInput(2,node3)
                        b.remove(v3)
                    if v4 in b:
                        nodel.setInput(3,node4)
                        b.remove(v4)
                    if v5 in b:
                        nodel.setInput(4,node5)
                        b.remove(v5)
                    if v6 in b:
                        nodel.setInput(5,node6)
                        b.remove(v6)
                    if v7 in b:
                        noder.setInput(0,node7)
                        b.remove(v7)
                    if v8 in b:
                        noder.setInput(1,node8)
                        b.remove(v8)
                    if v9 in b:
                        noder.setInput(2,node9)
                        b.remove(v9)
                    if v10 in b:
                        noder.setInput(3,node10)
                        b.remove(v10)
                    if v11 in b:
                        noder.setInput(4,node11)
                        b.remove(v11)
                    if v12 in b:
                        noder.setInput(5,node12)
                        b.remove(v12)
                    nodejv.setInput(0,nodel)
                    nodejv.setInput(1,noder)
                    backnode['bdwidth'].setValue(1200)
                    backnode['bdheight'].setValue(310)
                    backnode.setXYpos(90,20+x*400)
                    backnode['label'].setValue(file[:-6])
                    backnode['note_font'].setValue("Helvetica Bold")
                    backnode['note_font_size'].setValue(30)


#____________________________________________#



#____________________________________________#

def AutoWrite():
    sel = nuke.selectedNode()
    if sel == None:
        nuke.message("You need to select a node to split views from and rejoin.")
        return
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
    p=nuke.Panel('AutoWrite')
    p.addEnumerationPulldown('file_type','jpeg exr png tiff' )
    p.addSingleLineInput('parkname','_')
    ss=p.show()
    file_type = p.value('file_type')
    parkname = p.value('parkname')
    if ss == 1:
          
        date=time.strftime('%Y%m%d',time.localtime(time.time()))
        a = nuke.root()['name'].value().split('/')
        b = a[-1].split('_')
        c = b[-1].split('.')
        d = b[0]+'_'+b[1]+parkname+'_'+b[4]+'_'+c[0]+'_'+date
    
        if file_type == 'jpeg':
            g = 'jpeg'
        if file_type == 'exr':
            g = 'exr'
        if file_type == 'png':
            g = 'png'
        if file_type == 'tiff':
            g = 'tiff'       
        else:
            pass
        
        write = nuke.createNode("Write",inpanel=False)  
        write['file'].setValue(a[0]+'/'+a[1]+'/'+a[2]+'/'+a[3]+'/Stuff/cmp/img/filp/'+d+'/'+g+'/'+b[0]+'_'+b[1]+parkname+'_'+b[4]+'_'+c[0]+'.%05d.'+g)
        if g == 'jpeg':
            write['file_type'].setValue(g)
            write['_jpeg_quality'].setValue('1')
        if g == 'exr':
            write['file_type'].setValue(g)
        if g == 'png':
            write['file_type'].setValue(g)
        if g == 'tiff':
            write['file_type'].setValue(g)
            write['compression'].setValue('none')
    else:
        pass

#____________________________________________#

def OpenFileDirectory():
    read=nuke.selectedNode()
    a=os.path.dirname(read['file'].value())
    path=a.replace('/','\\')
    os.system('start %s' % path)

#____________________________________________#


def AutoClearNodes():
	AutoClear.main()

#____________________________________________#

def FootageCopyClear():
	FootageCopy.run()

#____________________________________________#

def FootageCopyClear_v01():
	FootageCopy_v01.run()
#____________________________________________#


def renamefile():

    mm = nuke.root()['name'].value().split('/')
    cc = mm[0]+'/'+mm[1]+'/'+mm[2]+'/'+mm[3]
    scrpath = cc+'/'+'Footage_Final'
    newpath = cc+'/'+'Footage'
    oldpath = cc+'/'+'Footage_old'
    os.rename(newpath,oldpath)
    os.rename(scrpath,newpath)


def Autofile():
    sel = nuke.selectedNodes()
    p=nuke.Panel('channel')
    p.addEnumerationPulldown('channels','rgb rgba all')
    ss=p.show()
    channel = p.value('channels')
    
    if ss == 1:
        for i in sel:
            read = i['file'].value()
            name = i.name()
            node=nuke.toNode(name)
            a=read.split('.')
            write = nuke.createNode("Write",inpanel=False)
            write['file'].setValue(read)
            write['file_type'].setValue(a[-1])
            if a[-1] == 'exr':
                write['compression'].setValue('Zip (16 scanlines)')   
            write['channels'].setValue(channel)
            write.setInput(0,node)
          
            
    
    else:
        pass



def thesameformat():
    col=nuke.getColor()
    all=nuke.root()['format'].value().width()
    a=nuke.selectedNodes()
    dict={}
    for i in a:
        sel=i.name()
        format = i['format'].value().width()
        dict[sel]=[format]
    for name,value in dict.items():
        for i in value:
            if i == all:
                b=nuke.toNode(name)
                b['label'].setValue('the same format')
                b['tile_color'].setValue(col)


def Relative_Path():
    nuke.root()['project_directory'].setValue("[python {''.join(['/'+i for i in nuke.script_directory().split('/')[0:-2]])[1:]}]")
    a=nuke.selectedNode()
    c=a['file'].value().split('/')
    b=nuke.root()['name'].value().split('/')
    list=[i for i in b if i in c]
    name=''.join(['/'+i for i in list])[1:]
    
    all = nuke.allNodes()
    for i in all:
        nodename = i.name()
        zimu=''.join(x for x in nodename if x.isalpha())
        if 'Camera' == zimu or 'Read' == zimu or 'ReadGeo' == zimu or 'Axis' == zimu:
            filename = i['file'].value()
            if filename != '':
                newname=filename.replace(name,'..')
                print newname
                i['file'].setValue(newname)
            else:
                pass
        else:
            pass


def Relative_Path_rename():
    rpname=''.join(['/'+i for i in nuke.script_directory().split('/')[0:-3]])[1:]
    all = nuke.allNodes()
    for i in all:
        nodename = i.name()
        zimu=''.join(x for x in nodename if x.isalpha())
        if 'Camera' == zimu or 'Read' == zimu or 'ReadGeo' == zimu or 'Axis' == zimu:
            filename = i['file'].value()
            newname=filename.replace('..',rpname)
            i['file'].setValue(newname)
        else:
            pass
 

def thesameframe():
    col=nuke.getColor()
    first_frame=int(nuke.root()['first_frame'].value())
    last_frame=int(nuke.root()['last_frame'].value())
    a=nuke.selectedNodes()
    dict={}
    for i in a:
        sel=i.name()
        first = i['first'].value()
        last = i['last'].value()
        dict[sel]=[first,last]
    for name,value in dict.items():
            if value[0] == first_frame and value[1] == last_frame:
                b=nuke.toNode(name)
                b['label'].setValue('the same frame')
                b['tile_color'].setValue(col)
            else:
                pass


def Collect():
    p=nuke.Panel('Collect')
    p.addEnumerationPulldown('choose','all single')
    p.addFilenameSearch('path','')
    k=p.show()
    a=nuke.allNodes('Read')
    outpath=p.value('path')
    list=[]

    if k==1:
        def sName(self,num):
            num='%04d' % num
            if '####' in self:  
                return self.replace('####',num)
            if '%04d' in self:
                return self.replace('%04d',num)
        
        rootName=os.path.basename(nuke.root()['name'].value())
        foot=rootName.split('.')[0]+'/'
        scriptpath=outpath+foot+rootName
        savepath=outpath+foot
#打包所有素材
        if p.value('choose')=='all':
            for i in a:
                rname=i.name()
                if not rname in list:
                    Fframe=i['first'].value()
                    Lframe=i['last'].value()
                    cc=i['file'].value()
                    rootpath=unicode(cc,'utf8')
                    name=rootpath.split('/')
                    copypath=savepath+name[-2]+'/'
                    finpath=copypath+name[-1]
                    if i.clones()!=0:
                        list.append(rname)
                    if not os.path.exists(copypath) :
                        os.makedirs(copypath)
                    for v in range(Fframe,Lframe+1):
                        if Fframe==Lframe:
                            copy(rootpath,finpath)
                            finpath=finpath.encode('utf8')
                            i['file'].setValue(finpath)
                        else:
                            input=sName(rootpath,v)
                            output=sName(finpath,v)
                            if os.path.exists(input):
                                copy(input,output)
                            i['file'].setValue(finpath)
                else:
                    pass
                
            nuke.scriptSaveAs(scriptpath)
#打包单帧素材            
        if p.value('choose')=='single':
            for i in a:
                rname=i.name()

                if not rname in list:
                    Fframe=i['first'].value()
                    Lframe=i['last'].value()                
                    frame=nuke.frame()
                    cc=i['file'].value()
                    rootpath=unicode(cc,'utf8')
                    name=rootpath.split('/')
                    copypath=savepath+name[-2]+'/'
                    finpath=copypath+name[-1]
                    if i.clones()!=0:
                        list.append(rname)
                    if not os.path.exists(copypath) :
                        os.makedirs(copypath)
                    
                    if Fframe==Lframe:
                        copy(rootpath,finpath)
                        finpath=finpath.encode('utf8')
                        i['file'].setValue(finpath)
                    else:
                        input=sName(rootpath,frame)
                        output=sName(finpath,frame)

                        if os.path.isfile(input):
                            
                            copy(input,output)
                            output=output.encode('utf8')
                            i['file'].setValue(output)
                else:
                    pass
            nuke.scriptSaveAs(scriptpath)
    else:
        pass



def AutoCreatproject():
    try: 
        a = nuke.Panel('password')
        a.addPasswordInput('password', '')
        sss = a.show()
        enter = a.value('password')
        if enter == 'cmp':
            p = nuke.Panel('Auto Creat project')
            p.addFilenameSearch('file path', 'T:/All/')
            p.addSingleLineInput('projectname','')
            p.addSingleLineInput('first_shotaucct','')
            p.addSingleLineInput('last_shotaucct','')
            p.addMultilineTextInput('first_name','')
            p.addMultilineTextInput('last_name','')
            ret = p.show()
            createinput = p.value('file path')
            projectname = p.value('projectname')
            first_shotaucct =int(p.value('first_shotaucct'))
            last_shotaucct =int(p.value('last_shotaucct'))
            first_name = p.value('first_name').split(',')
            last_name = p.value('last_name').split(',') 
        
            
            d=dict(zip([chr(i) for i in range(97,123)],[x for x in range(97,123)]))
            first_input='a'
            last_input='f'
            a=d[first_input]
            b=d[last_input]
            alpha=[chr(i) for i in range(a,b)]
        
        
            if ret == 1:
                project=['Doc','References','Work','Roto','工作汇报']
                shot=['Footage','Stuff','Work']
                footage=['efx','rolo','scene','Geo']
                cmp=['img','mov','roto']
                img=['elem','filp','ren']
                ioput=['Lnner','Onset']  
                list=['sc%02d' % i for i in range(first_shotaucct,last_shotaucct+1)]
                for i in list: 
                    for n in first_name:         
                        for m in last_name:
                            for b in shot:
                                if b == 'Footage':
                                    for c in footage:
                                        dirname=createinput+projectname+'/'+n+i+m+'/'+b+'/'+c
                                        dirname=unicode(dirname,'utf8')
                                        os.makedirs(dirname)
                                elif b == 'Stuff':
                                    for d in cmp:
                                        if d == 'img':
                                            for e in img:
                                                dirname1=createinput+projectname+'/'+n+i+m+'/'+b+'/cmp/'+d+'/'+e
                                                dirname1=unicode(dirname1,'utf8')
                                                os.makedirs(dirname1)
                                        else:
                                            dirname2=createinput+projectname+'/'+n+i+m+'/'+b+'/cmp/'+d
                                            dirname2=unicode(dirname2,'utf8')
                                            os.makedirs(dirname2)
                                else:
                                    dirname3=createinput+projectname+'/'+n+i+m+'/'+b
                                    dirname3=unicode(dirname3,'utf8')
                                    os.makedirs(dirname3)
                for x in project:
                    if x == 'References':
                        for a in ioput:
                            dirname4=createinput+projectname+'/'+x+'/'+a
                            dirname4=unicode(dirname4,'utf8')
                            os.makedirs(dirname4)
                    else:
                        dirname5=createinput+projectname+'/'+x
                        dirname5=unicode(dirname5,'utf8')
                        os.makedirs(dirname5)
            else:
                pass
        else:
           nuke.message( "Please enter right password!!!")
        
        

        return 
    except: 
        return  




import os,shutil,time,threading,nuke,math
def copyplates():
    p=nuke.Panel('Collect')
    p.addFilenameSearch('path','')
    k=p.show()
    outpath=p.value('path')
    try:
        if k==1:
            a=nuke.allNodes('Read')
            rootName=nuke.root()['name'].value().split('/')
            rotoover='/'.join(i for i in rootName[:3])+'/roto/over/'
            References='/'.join(i for i in rootName[:3])+'/References/Lnner/'
            c=rotoover.split('/')
            d=References.split('/')
            num=100.0/len(a)
            t=0
            readlist=[]
            task = nuke.ProgressTask("Moving")
            for i in a:
                if task.isCancelled():
                    break
                readname=i.name()
                name=i['file'].value()
                filename='/'.join(i for i in name.split('/')[:-1])
                if not readname in readlist:
                    if rotoover in filename or References in filename:
                        print filename
                        allfile='/'.join(x for x in filename.split('/') if x not in c  and x not in d) 
                        os.makedirs(outpath+allfile)
                        b=os.listdir(filename)            
                        for i in b:
                            copy(filename+'/'+i,outpath+allfile)
            
                t=t+num
                setT=int(math.floor(t))
                task.setMessage("%s" % name)
                task.setProgress(setT)      
                time.sleep(0.1)
                readlist.append(readname)
        else:
            pass
        return 
    except: 
        return  


def jumusingleview():
    p=nuke.Panel('views')
    p.addEnumerationPulldown('views :','L R')
    s=p.show()
    g=p.value('views :')
    g='%s' % g
    pv='X_pingmu180_v02'
    
    if s==1:
        a=nuke.selectedNodes()
        c={}
        b=[]
        x=-1
        for i in a:
            i.setSelected(False)
        for i in a:
            dictname=i.name()
            basename=os.path.basename(i['file'].value())
            file=basename[:-9]
            if basename=='Thumbs.db':
                i.setSelected(True)
                nukescripts.node_delete(popupOnError=True)
            else:
                c[file]=dictname
                b.append(file)
                b.sort()
        for v in b:
            if '1'+g in v:
                n='1'+g           
            if '2'+g in v:
                n='2'+g
            if '3'+g in v:
                n='3'+g
            if '1'+g in v or '2'+g in v or '3'+g in v:
                x+=1
                v1=v.replace(n,'1'+g)
                v2=v.replace(n,'2'+g)
                v3=v.replace(n,'3'+g)
                if v1 in b:
                    node1=nuke.toNode('%s' % c[v])
                    node1.setXYpos(100,100+x*400)
        
                if v2 in b:
                    node2=nuke.toNode('%s' % c[v2])
                    node2.setXYpos(200,100+x*400)
                    
                if v3 in b:
                    node3=nuke.toNode('%s' % c[v3])
                    node3.setXYpos(300,100+x*400)
        
                nodel=nuke.createNode("%s" % pv,inpanel=False)                
                nodel.setXYpos(200,250+x*400)
                nodel.setSelected(False)
                backnode=nuke.createNode("BackdropNode",inpanel=False)
                backnode.setXYpos(900,20+x*400)
                nodel.setSelected(False)
                if v1 in b:
                    nodel.setInput(2,node1)
                    if v1!=v:
                        b.remove(v1)
                if v2 in b:
                    nodel.setInput(1,node2)
                    if v2!=v:
                        b.remove(v2)
                if v3 in b:
                    nodel.setInput(0,node3)
                    if v3!=v:
                        b.remove(v3)
                b.sort()
                backnode['bdwidth'].setValue(300)
                backnode['bdheight'].setValue(310)
                backnode.setXYpos(90,20+x*400)
                backnode['label'].setValue(v)
                backnode['note_font'].setValue("Helvetica Bold")
                backnode['note_font_size'].setValue(30)
    else:
        pass



def huanmusingleview():
    p=nuke.Panel('views')
    p.addEnumerationPulldown('views :','L R')
    s=p.show()
    g=p.value('views :')
    g='%s' % g
    pv='X_pingmu360_v01'
    
    if s==1:
        a=nuke.selectedNodes()
        c={}
        b=[]
        x=-1
        for i in a:
            i.setSelected(False)
        for i in a:
            dictname=i.name()
            basename=os.path.basename(i['file'].value())
            file=basename[:-9]
            if basename=='Thumbs.db':
                i.setSelected(True)
                nukescripts.node_delete(popupOnError=True)
            else:
                c[file]=dictname
                b.append(file)
                b.sort()
        for v in b:
            if '1'+g in v:
                n='1'+g           
            if '2'+g in v:
                n='2'+g
            if '3'+g in v:
                n='3'+g
            if '4'+g in v:
                n='4'+g           
            if '5'+g in v:
                n='5'+g
            if '6'+g in v:
                n='6'+g
            if '1'+g in v or '2'+g in v or '3'+g in v or '4'+g in v or '5'+g in v or '6'+g in v:
                x+=1
                v1=v.replace(n,'1'+g)
                v2=v.replace(n,'2'+g)
                v3=v.replace(n,'3'+g)
                v4=v.replace(n,'4'+g)
                v5=v.replace(n,'5'+g)
                v6=v.replace(n,'6'+g)
                if v1 in b:
                    node1=nuke.toNode('%s' % c[v])
                    node1.setXYpos(100,100+x*400)
        
                if v2 in b:
                    node2=nuke.toNode('%s' % c[v2])
                    node2.setXYpos(200,100+x*400)
                    
                if v3 in b:
                    node3=nuke.toNode('%s' % c[v3])
                    node3.setXYpos(300,100+x*400)
                if v4 in b:
                    node4=nuke.toNode('%s' % c[v4])
                    node4.setXYpos(400,100+x*400)
        
                if v5 in b:
                    node5=nuke.toNode('%s' % c[v5])
                    node5.setXYpos(500,100+x*400)
                    
                if v6 in b:
                    node6=nuke.toNode('%s' % c[v6])
                    node6.setXYpos(600,100+x*400)
        
                nodel=nuke.createNode("%s" % pv,inpanel=False)                
                nodel.setXYpos(350,250+x*400)
                nodel.setSelected(False)
                backnode=nuke.createNode("BackdropNode",inpanel=False)
                backnode.setXYpos(900,20+x*400)
                nodel.setSelected(False)
                if v1 in b:
                    nodel.setInput(0,node1)
                    if v1!=v:
                        b.remove(v1)
                if v2 in b:
                    nodel.setInput(1,node2)
                    if v2!=v:
                        b.remove(v2)
                if v3 in b:
                    nodel.setInput(2,node3)
                    if v3!=v:
                        b.remove(v3)
                if v4 in b:
                    nodel.setInput(3,node4)
                    if v4!=v:
                        b.remove(v4)
                if v5 in b:
                    nodel.setInput(4,node5)
                    if v5!=v:
                        b.remove(v5)
                if v6 in b:
                    nodel.setInput(5,node6)
                    if v6!=v:
                        b.remove(v6)
                b.sort()
                backnode['bdwidth'].setValue(600)
                backnode['bdheight'].setValue(310)
                backnode.setXYpos(90,20+x*400)
                backnode['label'].setValue(v)
                backnode['note_font'].setValue("Helvetica Bold")
                backnode['note_font_size'].setValue(30)
    else:
        pass

def test_move(): 
    a=[i for i in nuke.allNodes() if ''.join(x for x in i.name() if x.isalpha()) == 'Camera' or ''.join(x for x in i.name() if x.isalpha()) == 'Read' or ''.join(x for x in i.name() if x.isalpha()) == 'ReadGeo' or ''.join(x for x in i.name() if x.isalpha()) == 'Axis']
    
    num=100.0/len(a)
    t=0
    readlist=[]
    task = nuke.ProgressTask("Moving")            
    mm = nuke.root()['name'].value().split('/')
    cc = mm[0]+'/'+mm[1]+'/'+mm[2]+'/'+mm[3]
    scrpath = cc+'/'+'Footage_Final'
    
    
    for i in a:
    
        if task.isCancelled():
            break
        file=i['file'].value()
        if file != '':
            readname=i.name()       
            filename=i['file'].value()
            dirname='/'.join(os.path.dirname(filename).split('/')[:8])
            pathlist=dirname.split('/')
            if not readname in readlist:
                if pathlist[0]=='T:'or pathlist[0]=='S:':
                
                    if 'footage' in dirname or 'Footage' in dirname:
    
        
                        if 'Footage' in dirname:
                            copypath=os.path.dirname(dirname.replace('Footage','Footage_Final'))                       
    
                        else:
                            copypath=os.path.dirname(dirname.replace('footage','Footage_Final'))
    
                        dirname=unicode(dirname,'utf8')
                        copypath=unicode(copypath,'utf8')
    
                        if not os.path.exists(copypath) :
                            os.makedirs(copypath)   
                        if os.path.exists(dirname):
                            try:
            
                                shutil.move(dirname,copypath)
        
                            except shutil.Error:
                                footpath=copypath+'/'+dirname.split('/')[-1]
                                newpath=copypath+'/'+'temp'
                                frompath=newpath+'/'+dirname.split('/')[-1]
                                shutil.move(footpath,newpath)
                                shutil.move(dirname,copypath)
                                newlist=os.listdir(frompath)
                                if not os.path.exists(newpath) :        
                                    os.makedirs(newpath)
    
                                for v in newlist:
                                    topath=frompath+'/'+v
                                    shutil.move(topath,footpath)    
    
        t=t+num
        setT=int(math.floor(t))
        task.setMessage("%s" % filename)
        task.setProgress(setT)      
        time.sleep(0.1)
        readlist.append(readname) 




def Autofindfile():
    sel = nuke.selectedNodes()
    if sel == None:
        nuke.message("You need to select a node to split views from and rejoin.")
        return
    for i in sel:    
        file=i['file'].value()
        firstframe=os.listdir(file)
        first = min(firstframe).split('.')[1]
        last = max(firstframe).split('.')[1]
        path=os.listdir(file)[0].split('.')
        list=len(path[1])
        if last == 'db':
            last = int(first) + int(len(firstframe))-2
            if list == 3:
                a= '###'
                newpath=file+'/'+path[0]+'.'+a+'.'+path[2]
                i['file'].setValue(newpath)
                i['first'].setValue(int(first))
                i['last'].setValue(int(last))
                i['origfirst'].setValue(int(first))
                i['origlast'].setValue(int(last))
            if list == 4:
                a= '####'
                newpath=file+'/'+path[0]+'.'+a+'.'+path[2]
                i['file'].setValue(newpath)
                i['first'].setValue(int(first))
                i['last'].setValue(int(last))
                i['origfirst'].setValue(int(first))
                i['origlast'].setValue(int(last))
            if list == 5:
                a= '#####'
                newpath=file+'/'+path[0]+'.'+a+'.'+path[2]
                i['file'].setValue(newpath)
                i['first'].setValue(int(first))
                i['last'].setValue(int(last))
                i['origfirst'].setValue(int(first))
                i['origlast'].setValue(int(last))
        else:
            if list == 3:
                a= '###'
                newpath=file+'/'+path[0]+'.'+a+'.'+path[2]
                i['file'].setValue(newpath)
                i['first'].setValue(int(first))
                i['last'].setValue(int(last))
                i['origfirst'].setValue(int(first))
                i['origlast'].setValue(int(last))
            if list == 4:
                a= '####'
                newpath=file+'/'+path[0]+'.'+a+'.'+path[2]
                i['file'].setValue(newpath)
                i['first'].setValue(int(first))
                i['last'].setValue(int(last))
                i['origfirst'].setValue(int(first))
                i['origlast'].setValue(int(last))
            if list == 5:
                a= '#####'
                newpath=file+'/'+path[0]+'.'+a+'.'+path[2]
                i['file'].setValue(newpath)
                i['first'].setValue(int(first))
                i['last'].setValue(int(last))
                i['origfirst'].setValue(int(first))
                i['origlast'].setValue(int(last))


#-----------------------------------------------------------------------------#


def AutoSixViews_v2():    
    p=nuke.Panel('Node')
    p.addEnumerationPulldown('Node :','Huan_360_6P')
    s=p.show()
    pv=p.value('Node :')
    if s==1:
        a=nuke.selectedNodes()
        c={}
        b=[]
        x=-1
        for i in a:
            i.setSelected(False)
        for i in a:
            dictname=i.name()
            basename=os.path.basename(i['file'].value())
            file=basename[:-4]
            if basename=='Thumbs.db':
                i.setSelected(True)
                nukescripts.node_delete(popupOnError=True)
            else:
                c[file]=dictname
                b.append(file)
                b.sort()
    
        for v in b:
            if '1L' in v:
                n='1L'            
            elif '2L' in v:
                n='2L'
            elif '3L' in v:
                n='3L'
            elif '4L' in v:
                n='4L'
            elif '5L' in v:
                n='5L'
            elif '6L' in v:
                n='6L'
            if '1L' in v or '2L' in v or '3L' in v or '4L' in v or '5L' in v or '6L' in v:
                v2=v.replace(n,'2L')
                v3=v.replace(n,'3L')
                v4=v.replace(n,'4L')
                v5=v.replace(n,'5L')
                v6=v.replace(n,'6L')
                v7=v.replace(n,'1R')
                v8=v.replace(n,'2R')
                v9=v.replace(n,'3R')
                v10=v.replace(n,'4R')
                v11=v.replace(n,'5R')
                v12=v.replace(n,'6R')
                if v in b:
                    x+=1
                    node1=nuke.toNode('%s' % c[v])
                    node1.setXYpos(100,100+x*400)
    
                    if v2 in b:
                        node2=nuke.toNode('%s' % c[v2])
                        node2.setXYpos(200,100+x*400)
                        
                    if v3 in b:
                        node3=nuke.toNode('%s' % c[v3])
                        node3.setXYpos(300,100+x*400)
                        
                    if v4 in b:
                        node4=nuke.toNode('%s' % c[v4])
                        node4.setXYpos(400,100+x*400)
                
                    if v5 in b:
                        node5=nuke.toNode('%s' % c[v5])
                        node5.setXYpos(500,100+x*400)
                
                    if v6 in b:
                        node6=nuke.toNode('%s' % c[v6])
                        node6.setXYpos(600,100+x*400)
    
                    if v7 in b:
                        node7=nuke.toNode('%s' % c[v7])
                        node7.setXYpos(700,100+x*400)
                        
                    if v8 in b:
                        node8=nuke.toNode('%s' % c[v8])
                        node8.setXYpos(800,100+x*400)
                        
                    if v9 in b:
                        node9=nuke.toNode('%s' % c[v9])
                        node9.setXYpos(900,100+x*400)
                
                    if v10 in b:
                        node10=nuke.toNode('%s' % c[v10])
                        node10.setXYpos(1000,100+x*400)
                
                    if v11 in b:
                        node11=nuke.toNode('%s' % c[v11])
                        node11.setXYpos(1100,100+x*400)
    
                    if v12 in b:
                        node12=nuke.toNode('%s' % c[v12])
                        node12.setXYpos(1200,100+x*400)
                
                    nodel=nuke.createNode("%s" % pv,inpanel=False)                
                    nodel.setXYpos(350,250+x*400)
                    nodel.setSelected(False)
                    noder=nuke.createNode("%s" % pv,inpanel=False)
                    noder.setXYpos(950,250+x*400)
                    noder.setSelected(False)
                    nodejv=nuke.createNode("JoinViews",inpanel=False)
                    nodejv.setXYpos(650,300+x*400)
                    nodejv.setSelected(False)
                    backnode=nuke.createNode("BackdropNode",inpanel=False)
                    backnode.setXYpos(2100,20+x*400)
                    backnode.setSelected(False)
                    nodel.setInput(0,node1)
                    if v2 in b:
                        nodel.setInput(1,node2)
                        b.remove(v2)
                    if v3 in b:
                        nodel.setInput(2,node3)
                        b.remove(v3)
                    if v4 in b:
                        nodel.setInput(3,node4)
                        b.remove(v4)
                    if v5 in b:
                        nodel.setInput(4,node5)
                        b.remove(v5)
                    if v6 in b:
                        nodel.setInput(5,node6)
                        b.remove(v6)
                    if v7 in b:
                        noder.setInput(0,node7)
                        b.remove(v7)
                    if v8 in b:
                        noder.setInput(1,node8)
                        b.remove(v8)
                    if v9 in b:
                        noder.setInput(2,node9)
                        b.remove(v9)
                    if v10 in b:
                        noder.setInput(3,node10)
                        b.remove(v10)
                    if v11 in b:
                        noder.setInput(4,node11)
                        b.remove(v11)
                    if v12 in b:
                        noder.setInput(5,node12)
                        b.remove(v12)
                    nodejv.setInput(0,nodel)
                    nodejv.setInput(1,noder)
                    backnode['bdwidth'].setValue(1200)
                    backnode['bdheight'].setValue(310)
                    backnode.setXYpos(90,20+x*400)
                    backnode['label'].setValue(file[:-6])
                    backnode['note_font'].setValue("Helvetica Bold")
                    backnode['note_font_size'].setValue(30)


