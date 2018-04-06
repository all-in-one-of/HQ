project (support_icons)

include (svg_file_list.cmake)

set (index_file SVGIcons.index)
set (resource_files
    IconMapping
    LICENSE.txt
)

add_subdirectory (archivemaker)

add_custom_command (
    OUTPUT ${H_CONFIG_ICONS_INSTALL_PATH}/${index_file}
    COMMAND ${H_BIN_PATH}/svgarchivemaker
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND ${CMAKE_COMMAND} -E copy
        ${index_file}
        ${H_CONFIG_ICONS_INSTALL_PATH}/${index_file}
    DEPENDS
        # Has to depend on the cmake file because otherwise new files
        # don't trigger a rebuild of the index file.
        svg_file_list.cmake

        # We also need to depend on the archivemaker.C itself.
        # The add_dependencies command doesn't seem to do the trick.
        archivemaker/archivemaker.C

        # The list of all svg files.
        ${support_icons_svg_files}
)

h_copy_command (
    DESTINATION ${H_SUPPORT_CONFIG_INSTALL_PATH}
    SOURCE ${CMAKE_CURRENT_SOURCE_DIR}
    FILES ${resource_files}
    OUTPUT output_resource_files
)

add_custom_target (
    ${PROJECT_NAME}
    ALL
    DEPENDS
        ${H_CONFIG_ICONS_INSTALL_PATH}/${index_file}
        ${output_resource_files}
)

add_dependencies (${PROJECT_NAME} svgarchivemaker)
