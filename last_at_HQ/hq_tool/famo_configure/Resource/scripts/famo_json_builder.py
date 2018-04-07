#coding:utf-8
__author__ = 'Administrator'
import json


trayIconData = {
    "defaultIcon":"O:/hq_tool/famo_configure/Resource/icons/famuma_pure.png",
    "title":u"温馨提示",
    "toolTip":U"花木马工具集",
    }


menuData = (
    {
        'menuName':u"Maya配置",
        "iconPath":"O:/hq_tool/famo_configure/Resource/icons/maya_2015.png",

        'children':(
            {
                'menuName': u"maya通用配置(本地化)",
                "iconPath": "O:/hq_tool/famo_configure/Resource/icons/famuma_pure.png",
                "execute": 'O:/hq_tool/famo_configure/bin/common_configure_local.exe',
                "dialogInfo": None
            },
            {
                'menuName': u"maya通用配置",
                "iconPath":"O:/hq_tool/famo_configure/Resource/icons/famuma_pure.png",
                "execute":'O:/hq_tool/famo_configure/bin/common_configure.exe',
                "dialogInfo":None
            },
            {
                'menuName': u"maya2015吴哥配置",
                "iconPath":"O:/hq_tool/famo_configure/Resource/icons/famuma_pure.png",
                "execute":'O:/hq_tool/famo_configure/bin/Wuge_configure.exe',
                "dialogInfo": None
            },
            {
                'menuName': u"maya2015林海雪原配置",
                "iconPath": "O:/hq_tool/famo_configure/Resource/icons/famuma_pure.png",
                "execute": 'O:/hq_tool/famo_configure/bin/linhaixueyuan_configure.exe',
                "dialogInfo": None
            }
        )
    },
    {
        'menuName':u"Houdini配置",
        "iconPath":"O:/hq_tool/famo_configure/Resource/icons/houdini_icon",
    }

)



allData ={
    "trayIconData": trayIconData,
    'menuData': menuData
}



dd = json.dumps( allData, indent=4 )

file = open(u'O:/hq_tool/famo_configure/Resource/json/menuData.json', 'w')
file.write(dd)
file.close()


class fanta_config():
    def __init__(self):
        self.menuRefresh()
        #pass

    def menuRefresh(self):

        def getMenu( meun, parent='' ):
            rootParent = parent
            for smenu in meun:
                parent = rootParent + '/'+smenu['menuName']
                print parent
                if smenu.has_key( 'children' ):
                    getMenu( smenu['children'], parent  )
        getMenu( menuData )

fanta_config()

'''
tt_suqing2.py
'''