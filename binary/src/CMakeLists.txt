aux_source_directory (. SRC_LIST)

# find testFunc.h
include_directories (../binarylib)

link_directories (${PROJECT_SOURCE_DIR}/lib)

add_executable (main ${SRC_LIST})

target_link_libraries (main binary)

set (EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
