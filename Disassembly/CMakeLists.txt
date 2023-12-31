cmake_minimum_required(VERSION 3.24)

project(disassembly ASM)

set(BASEROM ${CMAKE_CURRENT_SOURCE_DIR}/baserom.3ds)
set(BASEROM_DIR ${CMAKE_CURRENT_SOURCE_DIR}/baserom)
make_directory(${BASEROM_DIR})

set(TOOLS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/tools)

set(DISASM_CONFIG ${CMAKE_CURRENT_SOURCE_DIR}/oot3d.cfg)

if (CMAKE_SYSTEM_NAME STREQUAL "Windows")
    set(CTRTOOL ${TOOLS_DIR}/ctrtool.exe)
    set(N3DSDISASM ${TOOLS_DIR}/n3dsdisasm.exe)
else()
    set(CTRTOOL ${TOOLS_DIR}/ctrtool)
    set(N3DSDISASM ${TOOLS_DIR}/n3dsdisasm)
endif()

add_custom_command(
    DEPENDS ${BASEROM}
    COMMAND ${CTRTOOL} --exefsdir=${BASEROM_DIR}/exefs ${BASEROM}
    COMMAND ${CTRTOOL} --exheader=${BASEROM_DIR}/exheader.bin ${BASEROM}
    COMMAND ${CTRTOOL} --romfsdir=${BASEROM_DIR}/romfs ${BASEROM}
    COMMAND ${CTRTOOL} --plainrgn=${BASEROM_DIR}/plainrgn.bin ${BASEROM}
    OUTPUT ${BASEROM_DIR}/exefs/code.bin ${BASEROM_DIR}/exheader.bin
    COMMENT "Extracting files from baserom.3ds..."
)

add_custom_target(
    extract_baserom
    DEPENDS ${BASEROM_DIR}/exefs/code.bin ${BASEROM_DIR}/exheader.bin
)

add_custom_command(
    DEPENDS extract_baserom
    COMMAND cd ${CMAKE_CURRENT_SOURCE_DIR} && py ${TOOLS_DIR}/exefs2elf.py
    OUTPUT ${BASEROM_DIR}/baserom.elf
    COMMENT "Creating baserom.elf..."
)

add_custom_target(
    create_elf
    DEPENDS extract_baserom ${BASEROM_DIR}/baserom.elf
)

add_custom_command(
    DEPENDS extract_baserom
    COMMAND ${N3DSDISASM} -c ${DISASM_CONFIG} ${BASEROM_DIR}/exefs/code.bin > ${BASEROM_DIR}/baserom.s
    OUTPUT ${BASEROM_DIR}/baserom.s
    COMMENT "Disassembling code.bin into baserom.s..."
)

add_custom_target(
    n3dsdisasm
    DEPENDS ${BASEROM_DIR}/baserom.s
)

add_custom_command(
    DEPENDS n3dsdisasm
    COMMAND cd ${CMAKE_CURRENT_SOURCE_DIR} && py ./tools/split_n3dsdisasm.py ${BASEROM_DIR}/baserom.s asm
    COMMAND cd ${CMAKE_CURRENT_SOURCE_DIR} && py ./tools/split_data_chunks.py
    COMMAND cd ${CMAKE_CURRENT_SOURCE_DIR} && touch split_asm.txt
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/split_asm.txt
    COMMENT "Splitting baserom.s and data chunks..."
)

add_custom_target(
    split_asm
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/split_asm.txt
)

add_custom_target(
    disasm
    DEPENDS split_asm
)
