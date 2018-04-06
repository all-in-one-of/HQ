project (svgarchivemaker)

# When changing this list, make you also update the
# SHS/icons CMakeLists.txt custom command depends.
set (sources
    archivemaker.C
)

h_executable (DEV_ONLY ${sources})
h_library_deps (FS)
