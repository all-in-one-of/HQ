#功能：1.python和php通信，传输数据；2.调用浏览器打开maya检查结果信息页

#coding=utf-8
import urllib
import urllib2
import json
import webbrowser

#数据转换为json格式，要求：1.post_json；2.check_json；3.ip（唯一标识）
ip = "127.0.0.1"
values = {
            'data':{
               'ip':ip,
               'check_json':{
                    "k005_check_wkHeadsUp": [1, "true", u"检查wkHeadsUp", "commom", "通用"],
            			"k008_check_unknown": [1, "true", u"检查未知节点", "commom", u"通用"], 
            			"k011_check_Opathref": [1, "true", u"检查不在O盘的参考路径", "commom", u"通用"], 
            			"k009_check_sharedRef": [1, "true", u"检查sharedReferenceNode节点", "commom", u"通用"], 
            			"k013_check_Opathaisin": [1, "true", u"检查不在O盘的arnold代理路径", "commom", u"通用"], 
            			"k001_check_hairlinkarnold": [1, "false", u"检查没有连接arnold的毛发节点", "model", u"模型"], 
            			"k010_check_Opathvray": [1, "true", u"检查不在O盘的Vray代理路径", "commom", u"通用"], 
            			"k003_check_History": [1, "false", u"检查绑定后不干净的shape", "model", u"模型"], 
            			"k012_check_OpathCache": [1, "true", u"检查不在O盘的布料及几何体缓存路径", "commom", u"通用"], 
            			"k007_check_UNKNOWNREF": [1, "true", u"检查UNKNOWNREF节点", "commom", u"通用"], 
            			"k006_check_voronoi": [1, "true", u"检查voronoi破碎节点", "commom", u"通用"], 
            			"k002_check_novertPolo": [1, "true", u"检查无点的Plolygons", "model", u"模型"], 
            			"k015_check_displink": [1, "true", u"检查连接断了的置换节点", "commom", u"通用"], 
            			"k016_check_uuoig": [1, "true", u"检查检查多余的oig节点", "commom", u"通用"], 
            			"k014_check_Opathabc": [1, "true", u"检查不在O盘的abc代理路径", "commom", u"通用"], 
            			"k004_check_vshapeNode": [1, "false", u"检查不正确的shape命名", "commom", u"通用"]
            			},
        			'post_json':{
        			    "efe": "avi", 
        			    "fefe": "fef", 
        			    "fef": "fe", 
        			    "fef": "fe", 
        			    "outside_file": {
        			        "ass": ["C:/wwwww.ass","C:/wwwww.ass.gz","C:/adfa001.obj"], 
        			        "abc": ["C:/wwwww1.abc","C:/wwwww2.abc","C:/wwwww3.abc","C:/wwwww4.abc"], 
        			        "Texture": ["C:/wwwww.jpg","C:/wwwww.jpg","C:/wwwww.jpg","C:/wwwww.jpg"]
        			    }, 
        			    "_id": "ObjectId(595b45b675c97715e0495607)", 
        			    "fef": "45654544", 
        			    "efef": "45454121", 
        			    "maya_check": {
        			        "k009_check_sharedRef": [], 
        			        "k013_check_Opathaisin": [
        			            "ArnoldStandInShape"
        			        ], 
        			        "k004_check_vshapeNode": [
        			            "pSphere2|asdf", 
        			            "awdsfefShape", 
        			            "fd", 
        			            "fewf", 
        			            "gfrwe", 
        			            "pSphereShape2"
        			        ]
        			    }
        			}
    	    }
    }

#和php通信的
jsonValues = urllib.urlencode(values)

url = "http://10.99.40.240/FTManager/index.php/Home/MayaCheck/index"
request = urllib2.Request(url=url, data=jsonValues)
request = urllib2.Request(url=url, data=jsonValues)
response = urllib2.urlopen(request)
the_page = response.read()
the_page = the_page + "?ip=" + ip;
#print the_page

#浏览器打开网址，查看检查详细信息
webbrowser.open(the_page, new=0, autoraise=True)
