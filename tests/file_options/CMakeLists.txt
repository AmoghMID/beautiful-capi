#
# Beautiful Capi generates beautiful C API wrappers for your C++ classes
# Copyright (C) 2015 Petr Petrovich Petrov
#
# This file is part of Beautiful Capi.
#
# Beautiful Capi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Beautiful Capi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.
#

project(file_option)

cmake_minimum_required(VERSION 2.8)

include_directories(${file_option_SOURCE_DIR}/source/)

find_package(PythonInterp 3.4 REQUIRED)

function(bcapi_add_test test_name)
  add_custom_command(
    OUTPUT ${file_option_SOURCE_DIR}/library/source/AutoGenWrap_${test_name}.cpp
    COMMAND ${PYTHON_EXECUTABLE} ${file_option_SOURCE_DIR}/../../source/Main.py -i ${file_option_SOURCE_DIR}/library/file_options.xml -p ${file_option_SOURCE_DIR}/library/${test_name}_params.xml -o ${file_option_SOURCE_DIR}/library/include/${test_name} -w ${file_option_SOURCE_DIR}/library/source/AutoGenWrap_${test_name}.cpp
    MAIN_DEPENDENCY ${file_option_SOURCE_DIR}/library/file_options.xml
    DEPENDS ${file_option_SOURCE_DIR}/library/${test_name}_params.xml
    WORKING_DIRECTORY ${file_option_SOURCE_DIR}
  )
  add_library(file_options_${test_name} SHARED
    ${file_option_SOURCE_DIR}/library/source/AutoGenWrap_${test_name}.cpp
    ${file_option_SOURCE_DIR}/library/source/PrinterImpl.h
    ${file_option_SOURCE_DIR}/library/source/PrinterImpl.cpp
    ${file_option_SOURCE_DIR}/library/source/SphereImpl.h
    ${file_option_SOURCE_DIR}/library/source/SphereImpl.cpp
    ${file_option_SOURCE_DIR}/library/source/BodyImpl.h
    ${file_option_SOURCE_DIR}/library/source/BodyImpl.cpp
    ${file_option_SOURCE_DIR}/library/source/NodeImpl.h
    ${file_option_SOURCE_DIR}/library/source/NodeImpl.cpp
    ${file_option_SOURCE_DIR}/library/source/DataImpl.h
    ${file_option_SOURCE_DIR}/library/source/DataImpl.cpp
  )
  add_executable(file_options_${test_name}_client
    ${file_option_SOURCE_DIR}/clients/Main.cpp
  )
  add_dependencies(file_options_${test_name}_client file_options_${test_name})
  target_include_directories(file_options_${test_name}_client PRIVATE ${file_option_SOURCE_DIR}/library/include/${test_name})
  target_link_libraries(file_options_${test_name}_client file_options_${test_name})
  target_compile_definitions(file_options_${test_name}_client PRIVATE  -D${test_name})
endfunction()

bcapi_add_test(test00)
bcapi_add_test(test01)
bcapi_add_test(test02)
bcapi_add_test(test03)
bcapi_add_test(test04)
bcapi_add_test(test05)
bcapi_add_test(test06)
bcapi_add_test(test07)
bcapi_add_test(test08)
bcapi_add_test(test09)
