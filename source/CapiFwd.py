#!/usr/bin/env python
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


import FileGenerator
from Helpers import NamespaceScope
from LifecycleTraits import CreateLifecycleTraits
from FileGenerator import WatchdogScope
from FileGenerator import IfDefScope
from FileGenerator import NewFileScope


def process_capi(capi_generator):
    if len(capi_generator.cur_namespace_path) == 1:
        capi_generator.output_header = capi_generator.file_traits.get_file_for_capi(capi_generator.cur_namespace_path)
        capi_generator.output_header.put_begin_cpp_comments(capi_generator.params_description)
        with WatchdogScope(
                capi_generator.output_header, '{0}_CAPI_INCLUDED'.format(capi_generator.get_namespace_id().upper())
        ):
            capi_generator.exception_traits.generate_exception_info()
            capi_generator.loader_traits.generate_c_functions_declarations()
    capi_generator.output_header = capi_generator.file_traits.get_file_for_namespace(capi_generator.cur_namespace_path)
    capi_generator.file_traits.include_capi_header(capi_generator.cur_namespace_path)


def process_fwd(capi_generator, namespace):
    if len(capi_generator.cur_namespace_path) == 1:
        capi_generator.output_header = capi_generator.file_traits.get_file_for_fwd(capi_generator.cur_namespace_path)
        capi_generator.output_header.put_begin_cpp_comments(capi_generator.params_description)
        with WatchdogScope(
                capi_generator.output_header, '{0}_FWD_INCLUDED'.format(capi_generator.get_namespace_id().upper())
        ):
            with IfDefScope(capi_generator.output_header, '__cplusplus'):
                capi_generator.output_header.put_line('#include <memory>')
                capi_generator.file_traits.include_forward_holder_header()
                capi_generator.output_header.put_line('')
                capi_generator.exception_traits.generate_check_and_throw_exception_forward_declaration()
                generate_forwards(capi_generator, namespace)
    capi_generator.output_header = capi_generator.file_traits.get_file_for_namespace(capi_generator.cur_namespace_path)
    capi_generator.file_traits.include_fwd_header(capi_generator.cur_namespace_path)


def generate_forwards(capi_generator, namespace):
    capi_generator.output_header.put_line('namespace {0}'.format(namespace.m_name))
    with FileGenerator.IndentScope(capi_generator.output_header):
        for cur_class in namespace.m_classes:
            with CreateLifecycleTraits(cur_class, capi_generator):
                capi_generator.output_header.put_line('class {0};'.format(
                    cur_class.m_name + capi_generator.lifecycle_traits.get_suffix()))
                capi_generator.output_header.put_line(
                    'typedef beautiful_capi::forward_pointer_holder<{0}> {1};'.format(
                        cur_class.m_name + capi_generator.lifecycle_traits.get_suffix(),
                        cur_class.m_name + capi_generator.params_description.m_forward_typedef_suffix))
        for nested_namespace in namespace.m_namespaces:
            with NamespaceScope(capi_generator.cur_namespace_path, nested_namespace):
                generate_forwards(capi_generator, nested_namespace)


def generate_forward_holder(capi_generator):
    with NewFileScope(capi_generator.file_traits.get_file_for_forward_holder(), capi_generator):
        capi_generator.output_header.put_begin_cpp_comments(capi_generator.params_description)
        with WatchdogScope(capi_generator.output_header, 'BEAUTIFUL_CAPI_FORWARD_HOLDER_INCLUDED'):
            with IfDefScope(capi_generator.output_header, '__cplusplus'):
                capi_generator.output_header.put_line('namespace beautiful_capi')
                with FileGenerator.IndentScope(capi_generator.output_header):
                    capi_generator.output_header.put_line('template<typename WrappedObjType>')
                    capi_generator.output_header.put_line('class forward_pointer_holder')
                    with FileGenerator.IndentScope(capi_generator.output_header, '};'):
                        capi_generator.output_header.put_line('void* m_pointer;')
                        capi_generator.output_header.put_line('bool m_object_was_created;')
                        capi_generator.output_header.put_line('const bool m_add_ref;')
                        with FileGenerator.Unindent(capi_generator.output_header):
                            capi_generator.output_header.put_line('public:')
                        capi_generator.output_header.put_line('forward_pointer_holder(void* pointer, bool add_ref)')
                        capi_generator.output_header.put_line(
                            ' : m_object_was_created(false), m_pointer(pointer), m_add_ref(add_ref)'
                        )
                        with FileGenerator.IndentScope(capi_generator.output_header):
                            pass
                        capi_generator.output_header.put_line('~forward_pointer_holder()')
                        with FileGenerator.IndentScope(capi_generator.output_header):
                            capi_generator.output_header.put_line('if (m_object_was_created)')
                            with FileGenerator.IndentScope(capi_generator.output_header):
                                capi_generator.output_header.put_line(
                                    'reinterpret_cast<WrappedObjType*>(this)->~WrappedObjType();'
                                )
                        capi_generator.output_header.put_line('operator WrappedObjType()')
                        with FileGenerator.IndentScope(capi_generator.output_header):
                            capi_generator.output_header.put_line('return WrappedObjType(m_pointer, m_add_ref);')
                        capi_generator.output_header.put_line('WrappedObjType* operator->()')
                        with FileGenerator.IndentScope(capi_generator.output_header):
                            capi_generator.output_header.put_line('m_object_was_created = true;')
                            capi_generator.output_header.put_line('return new(this) WrappedObjType(m_pointer, m_add_ref);')
                        capi_generator.output_header.put_line('void* get_raw_pointer() const')
                        with FileGenerator.IndentScope(capi_generator.output_header):
                            capi_generator.output_header.put_line('return m_pointer;')
