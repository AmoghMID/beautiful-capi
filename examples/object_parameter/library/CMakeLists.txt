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

project(object_parameter)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

add_custom_command(
  OUTPUT ${object_parameter_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${object_parameter_SOURCE_DIR}/../../../source/Main.py -i ${object_parameter_SOURCE_DIR}/object_parameter.xml -p ${object_parameter_SOURCE_DIR}/object_parameter_params.xml -o ${object_parameter_SOURCE_DIR}/include -w ${object_parameter_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${object_parameter_SOURCE_DIR}/object_parameter.xml
  DEPENDS ${object_parameter_SOURCE_DIR}/object_parameter_params.xml
  WORKING_DIRECTORY ${object_parameter_SOURCE_DIR}
)

include_directories(${object_parameter_SOURCE_DIR}/source/)

add_library(object_parameter SHARED
  ${object_parameter_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${object_parameter_SOURCE_DIR}/source/PageImpl.h
  ${object_parameter_SOURCE_DIR}/source/PageImpl.cpp
  ${object_parameter_SOURCE_DIR}/source/DocumentImpl.h
  ${object_parameter_SOURCE_DIR}/source/DocumentImpl.cpp
)
