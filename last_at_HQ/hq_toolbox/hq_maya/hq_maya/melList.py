# -*- coding: utf-8 -*-
mels = [
{
   'del_path':'Dynamics/Fluid Effects/geo_to_fluid()',
   'usage':"""
//网上下的
geo_to_fluid();
""",
},
{
    'del_path':'Dynamics/Fluid Effects/blackbodyUI()',
    'usage':"""
blackbodyUI();
""",
},
{
    'del_path':'Dynamics/Particles/Instance/source tkBakeParticleInstancer_v1_4_2_modify_by_qs.mel',
    'usage':"""
source tkBakeParticleInstancer_v1_4_2_modify_by_qs.mel;
""",
},
{
    'del_path':'Dynamics/Particles/Emitter/pointEmitterVel(string $pointEmitter, int $vertexCount)ONLYSE',
    'usage':"""
string $emitList[] = `ls -sl -type "pointEmitter"`;
string $emitList[] = `listRelatives -ad -type "pointEmitter"`;
for ($poem in $emitList){
    setAttr ($poem + ".rate")   (pointEmitterVel($poem, 3));
""",
},

{
    'del_path':'Dynamics/Particles/Emitter/setEmitterRateExpStr( )ONLYSE',
    'usage':"""
//Open and close mel scripts
/////declare variable for point emitters under shellPoly objects/////
global string $emitLi[];
$emitLi = `listRelatives -ad -type "pointEmitter" "bridge"`;"

//Time Changed mel scripts
/////reset point emitters rate////
int $current = `currentTime -q`;
int $start = `playbackOptions -q -min`;
if ($current == $start){
    int $end = `playbackOptions -q -max`;
    $emitLi = `listRelatives -ad -type "pointEmitter" "bridge"`;
    for ($poem in $emitLi){
        //keyframe  -o "over" -vc 0 ($poem + ".rate");
        keyframe  -index 0 -vc 0     -tc ($start-1)     ($poem + ".rate");
        keyframe  -index 2 -vc 0     -tc ($end+1)     ($poem + ".rate");
        keyframe  -index 1 -vc 0     -tc ($end)         ($poem + ".rate"); 
    }
}

//particle creation expression
string $poEm = $emitLi[int(particleId)];
goalV = `getAttr ($poEm+".atV")`;
goalU = `getAttr ($poEm+".atU")`;
cus_emited = 0;"

//particle Runtime expression
if (opacityPP < .8 && cus_emited==0){
    cus_emited = 1;
    keyframe  -index 0 -vc 0                 -tc (frame-1)     ($emitLi[int(particleId)] + ".rate");
    keyframe  -index 1 -vc (rand(50,200))     -tc (frame)     ($emitLi[int(particleId)] + ".rate");
    keyframe  -index 2 -vc 0                 -tc (frame+4)     ($emitLi[int(particleId)] + ".rate");
}
""",
},

{
    'path':'Rendering/zz01( )',
'usage':"""
zz01();
""",
},
{
    'del_path':'Dynamics/Particles/parColorForm3DTextureStr( )ONLYSE',
    'usage':"""
vector $pos = position;
setAttr stucco1.rpc -type "float3" ($pos.x) ($pos.y) ($pos.z);
float $color[] = `getAttr stucco1.outColor`;
rgbPP = <<$color[0], $color[1], $color[2]>>;
""",
},

]