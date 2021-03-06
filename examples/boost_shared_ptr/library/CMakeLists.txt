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

project(boost_shared_ptr)

cmake_minimum_required(VERSION 2.8)

find_package(PythonInterp 3.4 REQUIRED)

add_custom_command(
  OUTPUT ${boost_shared_ptr_SOURCE_DIR}/source/AutoGenWrap.cpp
  COMMAND ${PYTHON_EXECUTABLE} ${boost_shared_ptr_SOURCE_DIR}/../../../source/Main.py -i ${boost_shared_ptr_SOURCE_DIR}/boost_shared_ptr.xml -p ${boost_shared_ptr_SOURCE_DIR}/boost_shared_ptr_params.xml -o ${boost_shared_ptr_SOURCE_DIR}/include -w ${boost_shared_ptr_SOURCE_DIR}/source/AutoGenWrap.cpp
  MAIN_DEPENDENCY ${boost_shared_ptr_SOURCE_DIR}/boost_shared_ptr.xml
  DEPENDS ${boost_shared_ptr_SOURCE_DIR}/boost_shared_ptr_params.xml
  WORKING_DIRECTORY ${boost_shared_ptr_SOURCE_DIR}
)

include_directories(
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/core/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/config/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/assert/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/throw_exception/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/predef/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/smart_ptr/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/type_traits/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/static_assert/include/
  ${boost_shared_ptr_SOURCE_DIR}/../../../3rdparty/boost/align/include/
  ${boost_shared_ptr_SOURCE_DIR}/source/
)

add_library(boost_shared_ptr SHARED
  ${boost_shared_ptr_SOURCE_DIR}/source/AutoGenWrap.cpp
  ${boost_shared_ptr_SOURCE_DIR}/source/PrinterImpl.h
  ${boost_shared_ptr_SOURCE_DIR}/source/PrinterImpl.cpp
)
