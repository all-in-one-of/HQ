import maya.cmds as cmds
import math

from qsMaya.utility import checkArg


def wt02(objectList,searchPattern):
    '''{"del_path":"Modeling/wt02(cmds.ls(sl=True,exactType='transform'),'forEm')",
"icon":"uvChooser.svg",
"usage":"deleteUVSet(cmds.ls(sl=True,exactType='transform'),'forEm')",
}
'''

    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]

    for tfNode in objectList:
        if cmds.listRelatives(tfNode,shapes=True, type='mesh', f=True ) is not None:
            for uvSet in cmds.polyUVSet(tfNode, q=True, allUVSets=True):
                if re.search(searchPattern, uvSet):
                    cmds.polyUVSet(tfNode, delete=True, uvSet=uvSet)



def wt01(objectList, matchPattern):
    '''{"del_path":"Modeling/wt01(cmds.ls(sl=True),'forEm')ONLYSE",
"icon":"uvChooser.svg",
"usage":"QM.setCurrentUVSet(cmds.ls(sl=True),'forEm')"
}
'''

    if str(type(objectList)) == "<type 'str'>" or str(type(objectList)) == "<type 'unicode'>":
        objectList = [objectList]

    for tfNode in objectList:
        if cmds.listRelatives(tfNode,shapes=True, type='mesh', f=True ) is not None:
            for uvSet in cmds.polyUVSet(tfNode, q=True, allUVSets=True):
                if re.search(matchPattern, uvSet):
                    cmds.polyUVSet(tfNode, currentUVSet=True, uvSet=uvSet)
                    break