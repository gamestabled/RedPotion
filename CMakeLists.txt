cmake_minimum_required(VERSION 3.24)
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/ARMCC.cmake)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT DEFINED ENV{ARMCC_PATH})
    message(FATAL_ERROR "please set ARMCC_PATH")
endif()

find_program(ARM_ASM NAMES armasm.exe PATHS $ENV{ARMCC_PATH}/bin REQUIRED NO_DEFAULT_PATH)
find_program(ARM_AR NAMES armar.exe PATHS $ENV{ARMCC_PATH}/bin REQUIRED NO_DEFAULT_PATH)
find_program(ARM_CC NAMES armcc.exe PATHS $ENV{ARMCC_PATH}/bin REQUIRED NO_DEFAULT_PATH)
find_program(ARM_LINK NAMES armlink.exe PATHS $ENV{ARMCC_PATH}/bin REQUIRED NO_DEFAULT_PATH)
find_program(ARM_FROMELF NAMES fromelf.exe PATHS $ENV{ARMCC_PATH}/bin REQUIRED NO_DEFAULT_PATH)

macro (set_compilers)
    set(CMAKE_CXX_COMPILER_ID ARMCC)

    set(CMAKE_AR ${ARM_AR})
    set(CMAKE_C_COMPILER ${ARM_CC})
    set(CMAKE_CXX_COMPILER ${ARM_CC})
    set(CMAKE_ASM_COMPILER ${ARM_ASM})
    set(CMAKE_LINKER ${ARM_LINK})
endmacro()

if (WIN32)
    set_compilers()
    set(CMAKE_C_COMPILER_WORKS TRUE)
    set(CMAKE_CXX_COMPILER_WORKS TRUE)
    set(CMAKE_ASM_COMPILER_WORKS TRUE)
endif()

project(RedPotion C CXX ASM)

if (NOT WIN32)
    set_compilers()
endif()

set(CMAKE_EXECUTABLE_SUFFIX ".axf")

__compiler_armcc(C)
__compiler_armcc(CXX)
__compiler_armcc(ASM)

add_subdirectory(Library)
add_subdirectory(Disassembly)

file(GLOB_RECURSE csourcefiles ${CMAKE_CURRENT_SOURCE_DIR}/Source/*.c)
file(GLOB_RECURSE cxxsourcefiles ${CMAKE_CURRENT_SOURCE_DIR}/Source/*.cpp)

SET(CXX_FLAGS "--apcs=//interwork --cpu=MPCore --fpmode=fast --cpp --arm --force_new_nothrow --signed_chars --multibyte-chars --locale=japanese --no_rtti_data --no_rtti --no_exceptions --data-reorder --split_sections --forceinline -O3 -Otime")

SET_SOURCE_FILES_PROPERTIES(
    ${cxxsourcefiles}
    PROPERTIES
    COMPILE_FLAGS "${CXX_FLAGS}"
    )

SET_SOURCE_FILES_PROPERTIES(
    ${CMAKE_SOURCE_DIR}/data/conststring.cpp
    PROPERTIES
    COMPILE_FLAGS
    "${CXX_FLAGS} --no_data_reorder"
    )

add_executable(RedPotion ${csourcefiles} ${cxxsourcefiles})

set(DEPS_DIR ${CMAKE_CURRENT_BINARY_DIR}/deps)
set(ASM_LIBS_DIR ${CMAKE_CURRENT_BINARY_DIR}/asm_libs)
set(DISASSEMBLY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/Disassembly)
file(MAKE_DIRECTORY ${DEPS_DIR} ${ASM_LIBS_DIR})

file(GLOB_RECURSE asm_libs "${ASM_LIBS_DIR}")

target_link_directories(RedPotion PUBLIC ${asm_libs})

find_program(DEVKITARM_GCC NAMES arm-none-eabi-gcc.exe PATHS $ENV{DEVKITARM}/bin REQUIRED NO_DEFAULT_PATH)

foreach(CPP_FILE ${cxxsourcefiles})
    get_filename_component(FILE_NAME ${CPP_FILE} NAME_WE)
    add_custom_command(
        OUTPUT ${DEPS_DIR}/${FILE_NAME}.deps
        COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/tools/preproc.py ${CPP_FILE} ${DEPS_DIR}/${FILE_NAME}.deps "${DISASSEMBLY_DIR}/"
        DEPENDS ${CPP_FILE}
    )
    add_custom_target(${FILE_NAME}_deps DEPENDS ${DEPS_DIR}/${FILE_NAME}.deps)
endforeach()

foreach(CPP_FILE ${cxxsourcefiles})
    get_filename_component(FILE_NAME ${CPP_FILE} NAME_WE)
    set(DEPS_FILE ${DEPS_DIR}/${FILE_NAME}.deps)
    add_custom_command(
        OUTPUT ${ASM_LIBS_DIR}/${FILE_NAME}_asm.o
        COMMAND cd ${DISASSEMBLY_DIR} && python3 ${CMAKE_CURRENT_SOURCE_DIR}/tools/build_asm_deps.py "${DEVKITARM_GCC} -mfpu=vfpv2 -mcpu=MPCore -march=armv6k -marm -mno-thumb-interwork -r" "${DEPS_FILE}" "${ASM_LIBS_DIR}/${FILE_NAME}_asm.o"
        DEPENDS ${DEPS_DIR}/${FILE_NAME}.deps disasm
    )
    add_custom_target(${FILE_NAME}_asm DEPENDS ${ASM_LIBS_DIR}/${FILE_NAME}_asm.o)
    add_dependencies(RedPotion ${FILE_NAME}_asm)
    target_link_libraries(RedPotion PUBLIC ${ASM_LIBS_DIR}/${FILE_NAME}_asm.o)
endforeach()

target_link_libraries(RedPotion PUBLIC 
                                nnsdk
                                )

target_link_options(RedPotion PUBLIC
    --cpu=MPCore --entry=__ctr_start --startup=__ctr_start --library_type=standardlib
    --ref_cpp_init --scanlib --legacyalign
    --tailreorder --no_remove --datacompressor=off
    --inline 
    --verbose --mangled --symbols
    --scatter=${CMAKE_CURRENT_SOURCE_DIR}/Data/oot3d.ld
    )

target_include_directories(RedPotion PUBLIC ${CMAKE_SOURCE_DIR}/Include ${CMAKE_SOURCE_DIR}/Library/nnsdk/Include ${CMAKE_SOURCE_DIR}/Source/Game)

add_dependencies(RedPotion disasm)

