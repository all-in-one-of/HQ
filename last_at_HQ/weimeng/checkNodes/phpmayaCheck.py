#���ܣ�1.python��phpͨ�ţ��������ݣ�2.�����������maya�������Ϣҳ

#coding=utf-8
import urllib
import urllib2
import json
import webbrowser

#����ת��Ϊjson��ʽ��Ҫ��1.post_json��2.check_json��3.ip��Ψһ��ʶ��
ip = "127.0.0.1"
values = {
            'data':{
               'ip':ip,
               'check_json':{
                    "k005_check_wkHeadsUp": [1, "true", u"���wkHeadsUp", "commom", "ͨ��"],
            			"k008_check_unknown": [1, "true", u"���δ֪�ڵ�", "commom", u"ͨ��"], 
            			"k011_check_Opathref": [1, "true", u"��鲻��O�̵Ĳο�·��", "commom", u"ͨ��"], 
            			"k009_check_sharedRef": [1, "true", u"���sharedReferenceNode�ڵ�", "commom", u"ͨ��"], 
            			"k013_check_Opathaisin": [1, "true", u"��鲻��O�̵�arnold����·��", "commom", u"ͨ��"], 
            			"k001_check_hairlinkarnold": [1, "false", u"���û������arnold��ë���ڵ�", "model", u"ģ��"], 
            			"k010_check_Opathvray": [1, "true", u"��鲻��O�̵�Vray����·��", "commom", u"ͨ��"], 
            			"k003_check_History": [1, "false", u"���󶨺󲻸ɾ���shape", "model", u"ģ��"], 
            			"k012_check_OpathCache": [1, "true", u"��鲻��O�̵Ĳ��ϼ������建��·��", "commom", u"ͨ��"], 
            			"k007_check_UNKNOWNREF": [1, "true", u"���UNKNOWNREF�ڵ�", "commom", u"ͨ��"], 
            			"k006_check_voronoi": [1, "true", u"���voronoi����ڵ�", "commom", u"ͨ��"], 
            			"k002_check_novertPolo": [1, "true", u"����޵��Plolygons", "model", u"ģ��"], 
            			"k015_check_displink": [1, "true", u"������Ӷ��˵��û��ڵ�", "commom", u"ͨ��"], 
            			"k016_check_uuoig": [1, "true", u"���������oig�ڵ�", "commom", u"ͨ��"], 
            			"k014_check_Opathabc": [1, "true", u"��鲻��O�̵�abc����·��", "commom", u"ͨ��"], 
            			"k004_check_vshapeNode": [1, "false", u"��鲻��ȷ��shape����", "commom", u"ͨ��"]
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

#��phpͨ�ŵ�
jsonValues = urllib.urlencode(values)

url = "http://10.99.40.240/FTManager/index.php/Home/MayaCheck/index"
request = urllib2.Request(url=url, data=jsonValues)
request = urllib2.Request(url=url, data=jsonValues)
response = urllib2.urlopen(request)
the_page = response.read()
the_page = the_page + "?ip=" + ip;
#print the_page

#���������ַ���鿴�����ϸ��Ϣ
webbrowser.open(the_page, new=0, autoraise=True)
