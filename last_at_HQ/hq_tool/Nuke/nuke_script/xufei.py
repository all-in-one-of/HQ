# -*- coding: UTF-8 -*- 
import nukescripts

import nuke

import os



def submitToFarm():

    RenderNodes=[

    'L0018',

    'L0019',

    'L0020',

    'L0031',

    'L0032',

    'L0033',

    ]

    

    def RenderOnNodes(renderNodes, prjFilePath, firstFrame, lastFrame, threads):

        renderStartIndex = 0

	allCmd = ""

        for renderNode in renderNodes:

            startFrame =  int(firstFrame) + renderStartIndex

            renderString = '/opt/TheFoundry/Nuke7.0v5/Nuke7.0 --nukex -i -F %s-%sx%s -m %s -x %s' % (startFrame, lastFrame, len(renderNodes), threads, prjFilePath)

            allCmd += " --tab --title='%s' -e 'ssh %s.jg.com \"%s\";echo \"\";echo \"\";echo \"\";echo \"\";echo \"\";echo \"Congratulations!\";echo \"\";echo \"Render Finished!\";read var;'" % (renderNode, renderNode, renderString)

            renderStartIndex = renderStartIndex + 1

        os.system("gnome-terminal %s" % allCmd)

    


    def OpenRenderWindow():

        p=nuke.Panel('Submit to renderfarm')

        p.addSingleLineInput('First Frame',nuke.root().firstFrame())

        p.addSingleLineInput('Last Frame',nuke.root().lastFrame())

        p.addEnumerationPulldown('Threads','8 16 32')

        for rserver in RenderNodes:

            p.addBooleanCheckBox(rserver,0)

    

    

        if p.show():

            selectedRenderNodes = []

            for rserver in RenderNodes:

                if (p.value(rserver)):

                    selectedRenderNodes.append(rserver)

            RenderOnNodes(selectedRenderNodes, nuke.root().name(), p.value("First Frame"), p.value("Last Frame"), p.value("Threads"))

    

    OpenRenderWindow()



nuke.menu('Nuke').addCommand('Render/Submit to renderfarm',submitToFarm,"+R")
