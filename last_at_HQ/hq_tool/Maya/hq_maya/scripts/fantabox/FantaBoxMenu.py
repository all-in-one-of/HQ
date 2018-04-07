# -*- coding:gbk -*-
import maya.cmds as cmds
import maya.mel as mel
import mtoa
import json
import os
from functools import partial

class FantaBoxMenu():
    def __init__(self):
        
        self.projectPath = r"O:/hq_tool/Maya/hq_maya/scripts/fantabox"
        self.rigpath = "O:/hq_tool/Maya/hq_maya/scripts/fantabox/rigging"
        
        ##通用
        self.commenus = (
        {"拍屏工具":'mel.eval("playblastTool")' },
        {"拼屏工具":'mel.eval("comscreenTool")' },
        {"参考工具":'mel.eval("editRefPathBat")'},
        {"代理工具":'mel.eval("proxyTool")'},
        {},
        {"检查重名工具": 'fb.com.SJ_repeatNameToolUI()'},
        {"清理无用节点工具": 'fb.com.SJ_cleanUpTool()'},
        {"清理无用层工具": 'fb.com.SJ_cleanLayerTool()'},
        {"修复模型材质工具": 'fb.com.SJ_fixedShadermodToolUI()'},
        {},
        {"去空间命名工具": 'mel.eval("removeNameSpace")'},
        {"节点锁定解锁工具":'mel.eval("unlockNodeTool")'},
        {"随机选取物体工具":'mel.eval("ramdonsel")' },
        {"批量修改参数工具":'fb.com.SJ_attrEditedToolwdUI()'},
        {"路径动画复制模型工具":'mel.eval("dulpathgeoTool")'  },
        {"模型钉点工具":'fb.com.shuai_polyAttach()'},
        {"加载摄影机平面工具":'mel.eval("loadcameraplanelTool")'},
        {"绝对路径转相对路径":'mel.eval("absolutepathbat")' },
        {},
        {"批量处理路径工具":'fb.com.SJ_pathbatTool()'},
        {"批处理渲染工具":'mel.eval("batrenderTool")' },
        {},
        {"MayaSublime链接切换":'fb.com.MayaSublime_UI()'},
        )
        # 模型
        self.modmenus = (
        {"SJ角色工具集":'fb.mod.SJ_charToolwdUI()'},
        {},
        {"角色模型库":'fb.mod.Char_ModelLibWin()'},
        {"道具模型库":'fb.mod.YY_ModelLibWin()'},
        {},
        {"uv工具":'fb.mod.UVToolwdUI()'},
        {"贴图工具":'fb.mod.SJ_texToolswdUI()'},
        {"材质工具":'fb.mod.comshderwdUI()'},
        {"灯光通道栏工具":'mel.eval("lightechbox")'},
        {},
        {"摆放物体到面工具":'mel.eval("putonface")' },
        {"物体表面吸附工具":'mel.eval("snaponface")'},
        {},
        {"距离测量工具":'mel.eval("measuredistance")'},
        {"选择隐藏物体工具":'mel.eval("selhidden")'},
        {"目标群体约束工具":'mel.eval("objconstrain")' },
        {},
        {"创建物体笔刷工具":'mel.eval("crobjbrush")'},
        {"石头生成工具":'mel.eval("stonemaker")'}
        )
        
        # 动画
        self.animenus = (
        {"Adv5工具集":'import shuai_AdvancedSkeleton5;reload(shuai_AdvancedSkeleton5)'},
        {"线框模式切换（轻显）":'fb.ani.SJ_animateDisplaywdUI()'},
        {"显示着色工具":'fb.ani.SJ_hardwareDisplaySwitcherwdUI()'},
        {},
        {"动画常用工具面板":'mel.eval("AnimateusefulTool")'},
        {"动画综合工具":'mel.eval("AnimateeCom")'},
        {},
        {"Arnoldのocc材质赋予工具":'mel.eval("Arnoldocc")' },
        {"材质网络丢失修复工具":'mel.eval("fixmissingshader")'},
        {"选择曲面给材质的模型":'mel.eval("faceToShader")'},
        {},
        {"动画对称工具(adv)":'fb.ani.SJ_animateSybwdUI()'},
        {"逐帧FKIK互转(adv)":'mel.eval("IKFKAnimSwitchWin")'},
        {"缩放动画曲线工具":'fb.ani.SJ_scaleAnimationwdUI()'},
        {"可编辑动画轨迹":'mel.eval("editableMotionTrail")'},
        {"优化动画曲线工具":'mel.eval("opAnimateCurve")'},
        {},
        {"选择子骨骼工具":'mel.eval("seljoint")'},
        {"捕捉添加控制器工具":'mel.eval("mopctrlTool")' },
        {},
        {"缓存路径检查工具":'mel.eval("cacheFileCheckWindow")'},
        {"yeti（解算毛发）缓存输出工具":'fb.ani.SJ_yetiCachewdUI()'},
        {"断开变体节点":'fb.ren.SJ_choicebreak()'},
        {"abc及毛发（单帧）缓存工具集":'fb.ani.SJ_abcFurCache_ToolwdUI()'}

        )
        
        # 特效
        
        self.fxmenus = (
        {"vfx_maya":'w00_window_QSTools(ICONDIRS)' },
        {"特效重命名工具":'mel.eval("fxrenametool")' },
        {"特效abc模型规范输出":'fb.fx.fx_prefixNameUI()' },
        {"相机流程工具":'fb.fx.camerapipwdUI()'},
        {"动画模型序列工具":r'mel.eval("geoAnimateseq")' },
        {"转化粒子替代工具":'mel.eval("nParticlesTranslater")' },
        {"特效渲染设置工具":'mel.eval("TX_RenderSettingUI")' }
        )
        # 组装
        self.renmenus = (
        {"重置默认lambert属性":'fb.ren.lambert_defaultSet().reset_lambertAttr();fb.ren.lambert_defaultSet().reset_lambertDisplayment()'},
        {"Arnold及Yeti渲染面板优化":'fb.ren.SJ_resetAiYetiRender()'},
        {"渲三屏工具":'mel.eval("GYF_winUI")'},
        {"Arnold前台渲染":"import mtoa.cmds.arnoldRender;mtoa.cmds.arnoldRender.arnoldBatchRender('')"},
        {},
        {"自动设置工程目录":'mel.eval("autosetproj")'},
        {},
        {"随机变体切换":'fb.ren.SJ_randomChoice()'},
        {"毛发显影工具":'fb.ren.SJ_furDisplaySwitchwdUI()'}
        )



    #设置脚本目录自动化
    def automenu(self, famenu, autopath, menunamedict, maindict, subdict):
        rigdirs = maindict[autopath]
        for r in range(len(rigdirs)):
            if rigdirs[r] != None:
                paths = autopath + "/" + rigdirs[r]
                try:
                    cmds.menuItem(str(rigdirs[r]), label=str(r + 1) + "." + menunamedict[rigdirs[r]], p=famenu, to=1,
                                  sm=1)
                except:
                    cmds.menuItem(str(rigdirs[r]), label=str(r + 1) + "." + rigdirs[r], p=famenu, to=1, sm=1)
                cmds.setParent("..", menu=True)
                submenufile = subdict[paths]
                for u in range(len(submenufile)):
                    scriptpath = paths + "/" + submenufile[u]
                    submenuname = os.path.splitext(submenufile[u])[0]
                    if os.path.splitext(scriptpath)[-1] == ".mel":
                        melname = r'''mel.eval('source "%s"')''' % (scriptpath)
                        try:
                            cmds.menuItem(label=str(u + 1) + "." + menunamedict[submenuname], p=str(rigdirs[r]), to=1,
                                          c=melname)
                        except:
                            cmds.menuItem(label=str(u + 1) + "." + str(submenuname), p=str(rigdirs[r]), to=1, c=melname)
                    else:
                        pyname = r'execfile("%s")' % (scriptpath)
                        try:
                            cmds.menuItem(label=str(u + 1) + "." + menunamedict[submenuname], p=str(rigdirs[r]), to=1,
                                          c=pyname)
                        except:
                            cmds.menuItem(label=str(u + 1) + "." + str(submenuname), p=str(rigdirs[r]), to=1, c=pyname)
    #子菜单目录：
    def menubuild(self,menuchild,menufather):
        modmenuChild = self.modmenus
        mc=0
        for m in range(len(menuchild)):
            if menuchild[m]!={}:
                if menuchild[m].values()[0]!=None:
                    cmds.menuItem(l=str(m+1-mc)+"."+menuchild[m].keys()[0], to=1, p=menufather, c=menuchild[m].values()[0])
                else:
                    mc = mc+1
                    
            else:
                mc = mc+1
                cmds.menuItem(d=1, p=menufather)
    #主菜单目录
    def main(self, *args):
        #global gMainWindow
        #gMainWindow = mel.eval('global string $gMainWindow;global string $tempMelVar;$tempMelVar=$gMainWindow')
        gMainWindow = mel.eval('$tempMelVar=$gMainWindow')
        if cmds.menu("fantaboxwd", q=1, ex=1):
            cmds.deleteUI("fantaboxwd")
        cmds.menu("fantaboxwd", p=gMainWindow, to=1, label=r"FantaBox")
        commonmn = cmds.menuItem(label='通用', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        modelmn = cmds.menuItem(label='模型', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        rigmn = cmds.menuItem(label='设置',c = "fb.rig.AR_optionwindow().creat()")
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        animatmn = cmds.menuItem(label='动画', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        fxmn = cmds.menuItem(label='特效', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        rendermn = cmds.menuItem(label='组装', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        checkmn = cmds.menuItem(label='提交规范检查工具',c='fb.loadcheckNode()' )
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        refreshmn = cmds.menuItem(label='刷新',c='import FantaBoxMenu;reload(fb.FantaBoxMenu);fb.FantaBoxMenu.FantaBoxMenu().main()' )

        cmds.setParent("..", menu=True)

        ##通用子面板:
        self.menubuild(self.commenus,commonmn)
           
        ##模型子面板：
        self.menubuild(self.modmenus,modelmn)
        '''
        ##设置子面板：
        rigFile = open(u'%s/rigpath.json'%(self.rigpath), 'r').read()
        rigData = json.loads(rigFile)
        self.automenu(rigmn, self.rigpath, rigData["name"], rigData["path"][0], rigData["path"][1])
        '''
        ##动画子面板：
        self.menubuild(self.animenus,animatmn)
            
        ##特效子面板：
        self.menubuild(self.fxmenus,fxmn)

        ##组装子面板：
        self.menubuild(self.renmenus,rendermn)