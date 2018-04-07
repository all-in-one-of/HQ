#coding:utf-8
__author__ = 'dengtao'
import json
import os

k_presets={
            "btndict":{0:"技术（相机）",1:"预演",2:"角色",3:"模型(设置)",4:"模型(道具)",5:"设置(动画)",
            6:"设置(群集)",7:"设置(动捕)",8:"动画",9:"特效",10:"特效(动画)",11:"渲染"},

            "common":
            {
            "SJ_repeatName":["检查重名", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%E6%A3%80%E6%9F%A5%E9%87%8D%E5%90%8D.htm",
            "fantabox.common.SJ_repeatNameToolUI"],
            "check_catchName":["检查动捕提交文件名字规范", [(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E5%258A%25A8%25E6%258D%2595%25E6%258F%2590%25E4%25BA%25A4%25E6%2596%2587%25E4%25BB%25B6%25E5%2590%258D%25E5%25AD%2597%25E8%25A7%2584%25E8%258C%2583.htm"],
            "check_display_wireframe":["检查提交文件的视窗是否为线框模式", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%258F%2590%25E4%25BA%25A4%25E6%2596%2587%25E4%25BB%25B6%25E7%259A%2584%25E8%25A7%2586%25E7%25AA%2597%25E6%2598%25AF%25E5%2590%25A6%25E4%25B8%25BA%25E7%25BA%25BF%25E6%25A1%2586%25E6%25A8%25A1%25E5%25BC%258F.htm"],
            "check_invalid_displayLayer":["检查多余显示层", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E5%25A4%259A%25E4%25BD%2599%25E6%2598%25BE%25E7%25A4%25BA%25E5%25B1%2582.htm",
            "fantabox.common.SJ_cleanLayerTool"],
            "k005_check_wkHeadsUp":["检查wkHeadsUp",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5wkHeadsUp.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k007_check_UNKNOWNREF":["检查UNKNOWNREF节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5UNKNOWNREF%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k008_check_unknown":["检查未知节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%259C%25AA%25E7%259F%25A5%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k009_check_sharedRef":["检查sharedReferenceNode节点", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5sharedReferenceNode%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k011_check_Opathref":["检查不在O盘的参考路径", [(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584%25E5%258F%2582%25E8%2580%2583%25E8%25B7%25AF%25E5%25BE%2584.htm",
            "fantabox.common.SJ_pathbatTool"],
            "k016_check_uuoig":["检查检查多余的oig节点", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%25A3%2580%25E6%259F%25A5%25E5%25A4%259A%25E4%25BD%2599%25E7%259A%2584oig%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k004_check_vshapeNode":["检查不正确的shape命名",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E6%25AD%25A3%25E7%25A1%25AE%25E7%259A%2584shape%25E5%2591%25BD%25E5%2590%258D.htm",
            "fantabox.common.SJ_repeatNameToolUI"],
            "SJ_check_TSM_cleanup":["检查TSM残留script节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5TSM%25E6%25AE%258B%25E7%2595%2599script%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "check_listJoint_ExGroup":["检查群集文件是否存在空组",[(6,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E7%25BE%25A4%25E9%259B%2586%25E6%2596%2587%25E4%25BB%25B6%25E6%2598%25AF%25E5%2590%25A6%25E5%25AD%2598%25E5%259C%25A8%25E7%25A9%25BA%25E7%25BB%2584.htm"],
            "k003_check_History":["检查绑定后不干净的shape",[(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E7%25BB%2591%25E5%25AE%259A%25E5%2590%258E%25E4%25B8%258D%25E5%25B9%25B2%25E5%2587%2580%25E7%259A%2584shape.htm"],
            "k014_check_Opathabc":["检查不在O盘的abc代理路径",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584abc%25E4%25BB%25A3%25E7%2590%2586%25E8%25B7%25AF%25E5%25BE%2584.htm",
            "fantabox.common.SJ_pathbatTool"]

            },
            "modeling":
            {
            "check_cluster_meshOnly":["检查群集文件模型组是否干净",[(6,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E7%25BE%25A4%25E9%259B%2586%25E6%2596%2587%25E4%25BB%25B6%25E6%25A8%25A1%25E5%259E%258B%25E7%25BB%2584%25E6%2598%25AF%25E5%2590%25A6%25E5%25B9%25B2%25E5%2587%2580.htm"],
            "k002_check_novertPolo":["检查无点的Plolygons",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%2597%25A0%25E7%2582%25B9%25E7%259A%2584Plolygons.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k_checkTrouble_CVs":["检查模型CV点位移信息是否清零",[(2,0),(3,0),(5,0),(6,0),(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%25A8%25A1%25E5%259E%258BCV%25E7%2582%25B9%25E4%25BD%258D%25E7%25A7%25BB%25E4%25BF%25A1%25E6%2581%25AF%25E6%2598%25AF%25E5%2590%25A6%25E6%25B8%2585%25E9%259B%25B6.htm"],
            "SJ_check_missshader":["检查丢失材质模型",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%25A2%25E5%25A4%25B1%25E6%259D%2590%25E8%25B4%25A8%25E6%25A8%25A1%25E5%259E%258B.htm",
            "fantabox.common.SJ_fixedShadermodToolUI"],
            "SJ_check_faceshader":["检查按面赋材质模型",[(2,0),(3,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%E6%A3%80%E6%9F%A5%E6%8C%89%E9%9D%A2%E8%B5%8B%E4%BA%88%E6%9D%90%E8%B4%A8%E6%A8%A1%E5%9E%8B.htm",
            "fantabox.common.SJ_fixedShadermodToolUI"],
            
            },
            "rigging":
            {
            "check_keyobj":["检查是否有Key帧物体",[(2,0),(3,0),(5,0),(6,0),(7,0)]
            ]
            },
            "animation":
            {
            "check_feetMask":["检查脚底板",[(8,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E8%2584%259A%25E5%25BA%2595%25E6%259D%25BF.htm"],
            "check_defaultTransform":["检查位移旋转缩放是否初始化",[(2,0),(3,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25BD%258D%25E7%25A7%25BB%25E6%2597%258B%25E8%25BD%25AC%25E7%25BC%25A9%25E6%2594%25BE%25E6%2598%25AF%25E5%2590%25A6%25E5%2588%259D%25E5%25A7%258B%25E5%258C%2596.htm"],
            "check_invalid_animLayer":["检查多余动画层",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25BD%258D%25E7%25A7%25BB%25E6%2597%258B%25E8%25BD%25AC%25E7%25BC%25A9%25E6%2594%25BE%25E6%2598%25AF%25E5%2590%25A6%25E5%2588%259D%25E5%25A7%258B%25E5%258C%2596.htm",
            "fantabox.common.SJ_cleanLayerTool"]
            
            },
            "fx":
            {           
            },
            "rendering":
            {
            "check_render_Options":["检查Arnold与yeti渲染设置是否正确",[(8,1),(9,1),(10,1),(11,1)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5Options%25E8%25AE%25BE%25E7%25BD%25AE%25E6%2598%25AF%25E5%2590%25A6%25E6%25AD%25A3%25E7%25A1%25AE.htm",
            "fantabox.rendering.SJ_resetAiYetiRender"],
            "SJ_check_lambert_resetting":["检查lambert是否为默认参数",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5lambert%25E6%2598%25AF%25E5%2590%25A6%25E4%25B8%25BA%25E9%25BB%2598%25E8%25AE%25A4%25E5%258F%2582%25E6%2595%25B0.htm",
            "fantabox.rendering.SJ_doIt_lambert_resetting"],
            "SJ_miss_texpathlists":["检查丢失贴图节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%25A2%25E5%25A4%25B1%25E8%25B4%25B4%25E5%259B%25BE%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.modeling.SJ_texToolswdUI"],
            "SJ_texNo2ODisk":["检查不在O盘贴图节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E8%25B4%25B4%25E5%259B%25BE%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.modeling.SJ_texToolswdUI"],
            "check_aiSubdiv":["检查Arnold渲染细分大于3的物体",[(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5Arnold%25E6%25B8%25B2%25E6%259F%2593%25E7%25BB%2586%25E5%2588%2586%25E5%25A4%25A7%25E4%25BA%258E3%25E7%259A%2584%25E7%2589%25A9%25E4%25BD%2593.htm",
            "fantabox.common.SJ_fixedShadermodToolUI"],
            "k001_check_hairlinkarnold":["检查没有连接arnold的毛发节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%25B2%25A1%25E6%259C%2589%25E8%25BF%259E%25E6%258E%25A5arnold%25E7%259A%2584%25E6%25AF%259B%25E5%258F%2591%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_fixedShadermodToolUI"],
            "check_renderLayer":["检查多余渲染层",[(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E5%25A4%259A%25E4%25BD%2599%25E6%25B8%25B2%25E6%259F%2593%25E5%25B1%2582.htm",
            "fantabox.common.SJ_cleanLayerTool"],
            "k010_check_Opathvray":["检查不在O盘的Vray代理路径",[(2,0),(3,0),(4,0),(5,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584Vray%25E4%25BB%25A3%25E7%2590%2586%25E8%25B7%25AF%25E5%25BE%2584.htm"],
            "k012_check_OpathCache":["检查不在O盘的布料及几何体缓存路径",[(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584%25E5%25B8%2583%25E6%2596%2599%25E5%258F%258A%25E5%2587%25A0%25E4%25BD%2595%25E4%25BD%2593%25E7%25BC%2593%25E5%25AD%2598%25E8%25B7%25AF%25E5%25BE%2584.htm"],
            "k013_check_Opathaisin":["检查不在O盘的arnold代理路径",[(2,0),(3,0),(4,0),(5,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584arnold%25E4%25BB%25A3%25E7%2590%2586%25E8%25B7%25AF%25E5%25BE%2584.htm"],
            "k015_check_displink":["检查连接断了的置换节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E8%25BF%259E%25E6%258E%25A5%25E6%2596%25AD%25E4%25BA%2586%25E7%259A%2584%25E7%25BD%25AE%25E6%258D%25A2%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"]

            }
}

k_ftpresets={
            "btndict":{0:"技术（相机）",1:"预演",2:"角色",3:"模型(设置)",4:"模型(道具)",5:"设置(动画)",
            6:"设置(群集)",7:"设置(动捕)",8:"动画",9:"特效",10:"特效(动画)",11:"渲染"},

            "common":
            {
            "SJ_repeatName":["检查重名", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%E6%A3%80%E6%9F%A5%E9%87%8D%E5%90%8D.htm",
            "fantabox.common.SJ_repeatNameToolUI"],
            "check_catchName":["检查动捕提交文件名字规范", [(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E5%258A%25A8%25E6%258D%2595%25E6%258F%2590%25E4%25BA%25A4%25E6%2596%2587%25E4%25BB%25B6%25E5%2590%258D%25E5%25AD%2597%25E8%25A7%2584%25E8%258C%2583.htm"],
            "check_invalid_displayLayer":["检查多余显示层", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E5%25A4%259A%25E4%25BD%2599%25E6%2598%25BE%25E7%25A4%25BA%25E5%25B1%2582.htm",
            "fantabox.common.SJ_cleanLayerTool"],
            "k005_check_wkHeadsUp":["检查wkHeadsUp",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5wkHeadsUp.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k007_check_UNKNOWNREF":["检查UNKNOWNREF节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5UNKNOWNREF%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k008_check_unknown":["检查未知节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%259C%25AA%25E7%259F%25A5%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k009_check_sharedRef":["检查sharedReferenceNode节点", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5sharedReferenceNode%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k011_check_Opathref":["检查不在O盘的参考路径", [(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584%25E5%258F%2582%25E8%2580%2583%25E8%25B7%25AF%25E5%25BE%2584.htm",
            "fantabox.common.SJ_pathbatTool"],
            "k016_check_uuoig":["检查检查多余的oig节点", [(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%25A3%2580%25E6%259F%25A5%25E5%25A4%259A%25E4%25BD%2599%25E7%259A%2584oig%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k004_check_vshapeNode":["检查不正确的shape命名",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E6%25AD%25A3%25E7%25A1%25AE%25E7%259A%2584shape%25E5%2591%25BD%25E5%2590%258D.htm",
            "fantabox.common.SJ_repeatNameToolUI"],
            "SJ_check_TSM_cleanup":["检查TSM残留script节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5TSM%25E6%25AE%258B%25E7%2595%2599script%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "check_listJoint_ExGroup":["检查群集文件是否存在空组",[(6,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E7%25BE%25A4%25E9%259B%2586%25E6%2596%2587%25E4%25BB%25B6%25E6%2598%25AF%25E5%2590%25A6%25E5%25AD%2598%25E5%259C%25A8%25E7%25A9%25BA%25E7%25BB%2584.htm"],
            "k003_check_History":["检查绑定后不干净的shape",[(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E7%25BB%2591%25E5%25AE%259A%25E5%2590%258E%25E4%25B8%258D%25E5%25B9%25B2%25E5%2587%2580%25E7%259A%2584shape.htm"],
            "k014_check_Opathabc":["检查不在O盘的abc代理路径",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584abc%25E4%25BB%25A3%25E7%2590%2586%25E8%25B7%25AF%25E5%25BE%2584.htm",
            "fantabox.common.SJ_pathbatTool"]

            },
            "modeling":
            {
            "check_cluster_meshOnly":["检查群集文件模型组是否干净",[(6,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E7%25BE%25A4%25E9%259B%2586%25E6%2596%2587%25E4%25BB%25B6%25E6%25A8%25A1%25E5%259E%258B%25E7%25BB%2584%25E6%2598%25AF%25E5%2590%25A6%25E5%25B9%25B2%25E5%2587%2580.htm"],
            "k002_check_novertPolo":["检查无点的Plolygons",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%2597%25A0%25E7%2582%25B9%25E7%259A%2584Plolygons.htm",
            "fantabox.common.SJ_cleanUpTool"],
            "k_checkTrouble_CVs":["检查模型CV点位移信息是否清零",[(2,0),(3,0),(5,0),(6,0),(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%25A8%25A1%25E5%259E%258BCV%25E7%2582%25B9%25E4%25BD%258D%25E7%25A7%25BB%25E4%25BF%25A1%25E6%2581%25AF%25E6%2598%25AF%25E5%2590%25A6%25E6%25B8%2585%25E9%259B%25B6.htm"],
            },
            "rigging":
            {
            "check_keyobj":["检查是否有Key帧物体",[(2,0),(3,0),(5,0),(6,0),(7,0)]
            ]
            },
            "animation":
            {
            "check_feetMask":["检查脚底板",[(8,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E8%2584%259A%25E5%25BA%2595%25E6%259D%25BF.htm"],
            "check_defaultTransform":["检查位移旋转缩放是否初始化",[(2,0),(3,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25BD%258D%25E7%25A7%25BB%25E6%2597%258B%25E8%25BD%25AC%25E7%25BC%25A9%25E6%2594%25BE%25E6%2598%25AF%25E5%2590%25A6%25E5%2588%259D%25E5%25A7%258B%25E5%258C%2596.htm"],
            "check_invalid_animLayer":["检查多余动画层",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25BD%258D%25E7%25A7%25BB%25E6%2597%258B%25E8%25BD%25AC%25E7%25BC%25A9%25E6%2594%25BE%25E6%2598%25AF%25E5%2590%25A6%25E5%2588%259D%25E5%25A7%258B%25E5%258C%2596.htm",
            "fantabox.common.SJ_cleanLayerTool"]
            
            },
            "fx":
            {           
            },
            "rendering":
            {
            "check_render_Options":["检查Arnold与yeti渲染设置是否正确",[(8,1),(9,1),(10,1),(11,1)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5Options%25E8%25AE%25BE%25E7%25BD%25AE%25E6%2598%25AF%25E5%2590%25A6%25E6%25AD%25A3%25E7%25A1%25AE.htm",
            "fantabox.rendering.SJ_resetAiYetiRender"],
            "SJ_check_lambert_resetting":["检查lambert是否为默认参数",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5lambert%25E6%2598%25AF%25E5%2590%25A6%25E4%25B8%25BA%25E9%25BB%2598%25E8%25AE%25A4%25E5%258F%2582%25E6%2595%25B0.htm",
            "fantabox.rendering.SJ_doIt_lambert_resetting"],
            "SJ_miss_texpathlists":["检查丢失贴图节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%25A2%25E5%25A4%25B1%25E8%25B4%25B4%25E5%259B%25BE%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.modeling.SJ_texToolswdUI"],
            "SJ_texNo2ODisk":["检查不在O盘贴图节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E8%25B4%25B4%25E5%259B%25BE%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.modeling.SJ_texToolswdUI"],
            "check_aiSubdiv":["检查Arnold渲染细分大于3的物体",[(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5Arnold%25E6%25B8%25B2%25E6%259F%2593%25E7%25BB%2586%25E5%2588%2586%25E5%25A4%25A7%25E4%25BA%258E3%25E7%259A%2584%25E7%2589%25A9%25E4%25BD%2593.htm",
            "fantabox.common.SJ_fixedShadermodToolUI"],
            "k001_check_hairlinkarnold":["检查没有连接arnold的毛发节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E6%25B2%25A1%25E6%259C%2589%25E8%25BF%259E%25E6%258E%25A5arnold%25E7%259A%2584%25E6%25AF%259B%25E5%258F%2591%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_fixedShadermodToolUI"],
            "check_renderLayer":["检查多余渲染层",[(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E5%25A4%259A%25E4%25BD%2599%25E6%25B8%25B2%25E6%259F%2593%25E5%25B1%2582.htm",
            "fantabox.common.SJ_cleanLayerTool"],
            "k010_check_Opathvray":["检查不在O盘的Vray代理路径",[(2,0),(3,0),(4,0),(5,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584Vray%25E4%25BB%25A3%25E7%2590%2586%25E8%25B7%25AF%25E5%25BE%2584.htm"],
            "k012_check_OpathCache":["检查不在O盘的布料及几何体缓存路径",[(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584%25E5%25B8%2583%25E6%2596%2599%25E5%258F%258A%25E5%2587%25A0%25E4%25BD%2595%25E4%25BD%2593%25E7%25BC%2593%25E5%25AD%2598%25E8%25B7%25AF%25E5%25BE%2584.htm"],
            "k013_check_Opathaisin":["检查不在O盘的arnold代理路径",[(2,0),(3,0),(4,0),(5,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E4%25B8%258D%25E5%259C%25A8O%25E7%259B%2598%25E7%259A%2584arnold%25E4%25BB%25A3%25E7%2590%2586%25E8%25B7%25AF%25E5%25BE%2584.htm"],
            "k015_check_displink":["检查连接断了的置换节点",[(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0)],
            r"http://10.99.40.112/website/help/share_help_document/%E7%94%B5%E5%BD%B1%E5%88%B6%E4%BD%9C%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3--publish%E6%96%87%E6%A1%A3/index.htm#t=%25E6%25A3%2580%25E6%259F%25A5%25E8%25BF%259E%25E6%258E%25A5%25E6%2596%25AD%25E4%25BA%2586%25E7%259A%2584%25E7%25BD%25AE%25E6%258D%25A2%25E8%258A%2582%25E7%2582%25B9.htm",
            "fantabox.common.SJ_cleanUpTool"]

            }
}


def menuJson():
    k_presetjson = json.dumps( k_presets, indent=4)
    k_jsonfile = open('D:/fantaBox/Maya/hq_maya/scripts/fantabox/FantaBox_mayacheck.json', 'w')
    k_jsonfile.write(k_presetjson)
    k_jsonfile.close()

    k_ftpresetjson = json.dumps( k_ftpresets, indent=4)
    k_jsonftpfile = open('D:/fantaBox/Maya/hq_maya/scripts/fantabox/FantaBox_mayacheck_ftp.json', 'w')
    k_jsonftpfile.write(k_ftpresetjson)
    k_jsonftpfile.close()
    
if __name__=="__main__":
    menuJson()