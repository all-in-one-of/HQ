#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
python "$S/cmake/UtilityScripts/GenerateCMakeFileList.py" support_icons_svg_files svg_file_list.cmake *.svg $DIR
