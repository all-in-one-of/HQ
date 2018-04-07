fluidShape = cmds.ls(sl=True, type="fluidShape")[0]
cmds.setAttr(fluidShape+".densityMethod", 2)
cmds.setAttr(fluidShape+".velocityMethod", 1)
cmds.setAttr(fluidShape+".transparency", 0.449999988079, 0.449999988079, 0.449999988079, type="float3")
cmds.setAttr(fluidShape+".edgeDropoff", 0.0)
cmds.setAttr(fluidShape+".colorInput", 5)
cmds.setAttr(fluidShape+".colorInputBias", 0.0)
cmds.setAttr(fluidShape+".opacityInput", 5)
cmds.setAttr(fluidShape+".opacityInputBias", 0.0)
cmds.setAttr(fluidShape+".quality", 4.0)
cmds.setAttr(fluidShape+".contrastTolerance", 0.0500000007451)
cmds.setAttr(fluidShape+".renderInterpolator", 3)
cmds.setAttr(fluidShape+".colorTexture", False)
cmds.setAttr(fluidShape+".opacityTexture", True)
cmds.setAttr(fluidShape+".textureType", 0)
cmds.setAttr(fluidShape+".colorTexGain", 1.0)
cmds.setAttr(fluidShape+".opacityTexGain", 2.0)
cmds.setAttr(fluidShape+".amplitude", 1.0)
cmds.setAttr(fluidShape+".ratio ", 0.600000023842)
cmds.setAttr(fluidShape+".frequencyRatio", 3.0)
cmds.setAttr(fluidShape+".depthMax", 4)
cmds.setAttr(fluidShape+".invertTexture", False)
cmds.setAttr(fluidShape+".inflection", True)
cmds.setAttr(fluidShape+".textureTime", 0.800000011921)
cmds.setAttr(fluidShape+".frequency", 2.0)
cmds.setAttr(fluidShape+".textureScaleX", 1.0)
cmds.setAttr(fluidShape+".textureScaleY", 1.0)
cmds.setAttr(fluidShape+".textureScaleZ", 1.0)
cmds.setAttr(fluidShape+".selfShadowing", True)
cmds.setAttr(fluidShape+".shadowOpacity", 0.209999993443)
cmds.setAttr(fluidShape+".lightType", 1)
cmds.setAttr(fluidShape+".lightBrightness", 1.0)
cmds.setAttr(fluidShape+".fluidLightColor", 1.0, 1.0, 1.0, type="float3")
cmds.setAttr(fluidShape+".ambientBrightness", 1.0)
cmds.setAttr(fluidShape+".ambientDiffusion", 2.5)
cmds.setAttr(fluidShape+".ambientColor", 0.10000000149, 0.10000000149, 0.10000000149, type="float3")
cmds.setAttr(fluidShape+".directionalLightX", 0.5)
cmds.setAttr(fluidShape+".directionalLightY", 0.800000011921)
cmds.setAttr(fluidShape+".directionalLightZ", 0.5)
cmds.setAttr(fluidShape+".pointLightX", 0.0)
cmds.setAttr(fluidShape+".pointLightY", 0.0)
cmds.setAttr(fluidShape+".pointLightZ", 0.0)
cmds.setAttr(fluidShape+".pointLightDecay", 1)
cmds.setAttr(fluidShape+".opacity[0].opacity_Position", 0.0)
cmds.setAttr(fluidShape+".opacity[0].opacity_FloatValue", 0.0)
cmds.setAttr(fluidShape+".opacity[0].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[1].opacity_Position", 0.479999989271)
cmds.setAttr(fluidShape+".opacity[1].opacity_FloatValue", 0.0)
cmds.setAttr(fluidShape+".opacity[1].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[2].opacity_Position", 0.637000024319)
cmds.setAttr(fluidShape+".opacity[2].opacity_FloatValue", 0.0189999993891)
cmds.setAttr(fluidShape+".opacity[2].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[3].opacity_Position", 0.680000007153)
cmds.setAttr(fluidShape+".opacity[3].opacity_FloatValue", 0.129600003362)
cmds.setAttr(fluidShape+".opacity[3].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[4].opacity_Position", 0.69470000267)
cmds.setAttr(fluidShape+".opacity[4].opacity_FloatValue", 0.325800001621)
cmds.setAttr(fluidShape+".opacity[4].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[5].opacity_Position", 0.75)
cmds.setAttr(fluidShape+".opacity[5].opacity_FloatValue", 0.5)
cmds.setAttr(fluidShape+".opacity[5].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[6].opacity_Position", 0.84500002861)
cmds.setAttr(fluidShape+".opacity[6].opacity_FloatValue", 0.634599983692)
cmds.setAttr(fluidShape+".opacity[6].opacity_Interp", 1)
cmds.setAttr(fluidShape+".opacity[7].opacity_Position", 1.0)
cmds.setAttr(fluidShape+".opacity[7].opacity_FloatValue", 0.689999997616)
cmds.setAttr(fluidShape+".opacity[7].opacity_Interp", 1)
cmds.setAttr(fluidShape+".color[0].color_Position", 0.0)
cmds.setAttr(fluidShape+".color[0].color_Color", 1.0, 1.0, 1.0, type="float3")
cmds.setAttr(fluidShape+".color[0].color_Interp", 1)
cmds.setAttr(fluidShape+".incandescence[0].incandescence_Position", 0.0)
cmds.setAttr(fluidShape+".incandescence[0].incandescence_Color", 0.0, 0.0, 0.0, type="float3")
cmds.setAttr(fluidShape+".incandescence[0].incandescence_Interp", 1)