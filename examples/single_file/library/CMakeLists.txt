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

project(single_file)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

add_custom_command(
  OUTPUT ${single_file_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${single_file_SOURCE_DIR}/../../../source/Main.py -i ${single_file_SOURCE_DIR}/single_file.xml -p ${single_file_SOURCE_DIR}/single_file_params.xml -o ${single_file_SOURCE_DIR}/include -w ${single_file_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${single_file_SOURCE_DIR}/single_file.xml
  DEPENDS ${single_file_SOURCE_DIR}/single_file_params.xml
  WORKING_DIRECTORY ${single_file_SOURCE_DIR}
)

include_directories(${single_file_SOURCE_DIR}/source/)

add_library(single_file SHARED
  ${single_file_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${single_file_SOURCE_DIR}/source/PrinterImpl.h
  ${single_file_SOURCE_DIR}/source/PrinterImpl.cpp
)
