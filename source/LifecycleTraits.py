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

import Parser
from Constants import Constants
from TraitsBase import TraitsBase
from ExceptionTraits import create_exception_traits


class LifecycleTraitsBase(TraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)
        delete_method = Parser.TMethod()
        delete_method.m_name = Constants.delete_suffix
        delete_method.m_noexcept = True
        if cur_class.m_delete_or_release_noexcept_filled:
            delete_method.m_noexcept = cur_class.m_delete_or_release_noexcept
        self.delete_exception_traits = create_exception_traits(delete_method, cur_class, capi_generator)
        self.copy_method = Parser.TMethod()
        self.copy_method.m_name = Constants.copy_suffix
        other_arg = Parser.TArgument()
        other_arg.m_type = 'void*'
        other_arg.m_name = 'other.{0}'.format(Constants.object_var)
        self.copy_method.m_arguments.append(other_arg)
        self.copy_method.m_noexcept = False
        if cur_class.m_copy_or_add_ref_noexcept_filled:
            self.copy_method.m_noexcept = cur_class.m_copy_or_add_ref_noexcept
        self.copy_exception_traits = create_exception_traits(self.copy_method, cur_class, capi_generator)

    def get_base_init(self):
        if self.cur_class.m_base:
            return ' : {base_class_name}(0, false)'.format(base_class_name=self.cur_class.m_base + self.get_suffix())
        else:
            return ''

    def get_destructor_declaration(self):
        return '~' + self.cur_class.m_name + self.get_suffix() + '()'

    def get_delete_c_function_name(self):
        return self.capi_generator.get_namespace_id().lower() + Constants.delete_suffix

    def generate_delete_c_function(self):
        delete_c_function_name = self.get_delete_c_function_name()
        c_function_declaration = 'void {delete_c_function}({arguments_list})'.format(
            delete_c_function=delete_c_function_name,
            arguments_list=', '.join(self.delete_exception_traits.get_c_argument_pairs())
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            method_call = 'delete static_cast<{0}*>(object_pointer);'.format(
                self.cur_class.m_implementation_class_name
            )
            self.delete_exception_traits.generate_implementation_call(method_call, '')
        self.put_source_line('')

    def generate_std_methods(self):
        self.put_line('bool {0}() const'.format(self.capi_generator.params_description.m_is_null_method))
        with self.indent_scope():
            self.put_line('return !{0};'.format(Constants.object_var))
        self.put_line('bool {0}() const'.format(self.capi_generator.params_description.m_is_not_null_method))
        with self.indent_scope():
            self.put_line('return {0} != 0;'.format(Constants.object_var))
        self.put_line('bool operator!() const')
        with self.indent_scope():
            self.put_line('return !{0};'.format(Constants.object_var))
        self.put_line('{class_name}* operator->()'.format(
            class_name=self.cur_class.m_name + self.get_suffix()))
        with self.indent_scope():
            self.put_line('return this;')
        self.put_line('const {class_name}* operator->() const'.format(
            class_name=self.cur_class.m_name + self.get_suffix()))
        with self.indent_scope():
            self.put_line('return this;')

    def generate_delete_method(self):
        pass

    def generate_copy_or_add_ref_for_constructor(self):
        self.copy_method.m_arguments[0].m_name = Constants.object_var
        self.put_line('if ({object_var})'.format(object_var=Constants.object_var))
        with self.indent_scope():
            self.copy_exception_traits.generate_c_call(
                '_'.join(self.capi_generator.cur_namespace_path[:-1]).lower() + Constants.copy_suffix,
                'SetObject({c_function}({arguments}))',
                True
            )


class CopySemantic(LifecycleTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def get_suffix(self):
        return self.capi_generator.params_description.m_wrapper_class_suffix_copy_semantic

    def generate_destructor(self):
        self.capi_generator.inheritance_traits.generate_destructor(
            self.get_destructor_declaration(), self.get_delete_c_function_name()
        )
        self.generate_delete_c_function()

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other){base_init}'.format(
            class_name=self.cur_class.m_name + self.get_suffix(), base_init=self.get_base_init())
        )
        with self.indent_scope():
            self.put_line('if (other.{object_var})'.format(object_var=Constants.object_var))
            with self.indent_scope():
                self.copy_exception_traits.generate_c_call(
                    self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix,
                    'SetObject({c_function}({arguments}))',
                    True
                )
            self.put_line('else')
            with self.indent_scope():
                self.put_line('SetObject(0);')
        self.put_line('{class_name}(void *object_pointer, bool copy_object){base_init}'.format(
            class_name=self.cur_class.m_name + self.get_suffix(), base_init=self.get_base_init())
        )
        with self.indent_scope():
            self.copy_method.m_arguments[0].m_name = 'object_pointer'
            self.put_line('if (object_pointer && copy_object)')
            with self.indent_scope():
                self.copy_exception_traits.generate_c_call(
                    self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix,
                    'SetObject({c_function}({arguments}))',
                    True
                )
            self.put_line('else')
            with self.indent_scope():
                self.put_line('SetObject(object_pointer);')
        c_function_declaration = 'void* {copy_c_function}({arguments_list})'.format(
            copy_c_function=self.capi_generator.get_namespace_id().lower() + Constants.copy_suffix,
            arguments_list=', '.join(self.copy_exception_traits.get_c_argument_pairs_for_function())
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            method_call = 'return new {0}(*static_cast<{0}*>(object_pointer));'.format(
                self.cur_class.m_implementation_class_name
            )
            self.copy_exception_traits.generate_implementation_call(method_call, 'void*')
        self.put_source_line('')


class RawPointerSemantic(LifecycleTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)

    def get_suffix(self):
        return self.capi_generator.params_description.m_wrapper_class_suffix_raw_pointer

    def generate_destructor(self):
        pass

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other){base_init}'.format(
            class_name=self.cur_class.m_name + self.get_suffix(), base_init=self.get_base_init()))
        with self.indent_scope():
            self.put_line('SetObject(other.{object_var});'.format(object_var=Constants.object_var))
        self.put_line('{class_name}(void *object_pointer, bool /*add_ref*/){base_init}'.format(
            class_name=self.cur_class.m_name + self.get_suffix(), base_init=self.get_base_init()))
        with self.indent_scope():
            self.put_line('SetObject(object_pointer);')

    def generate_delete_method(self):
        self.capi_generator.inheritance_traits.generate_destructor(
            'void ' + self.capi_generator.params_description.m_delete_method + '()',
            self.get_delete_c_function_name()
        )
        self.generate_delete_c_function()


class RefCountedSemantic(LifecycleTraitsBase):
    def __init__(self, cur_class, capi_generator):
        super().__init__(cur_class, capi_generator)
        release_method = Parser.TMethod()
        release_method.m_name = Constants.release_suffix
        release_method.m_noexcept = True
        if cur_class.m_delete_or_release_noexcept_filled:
            release_method.m_noexcept = cur_class.m_delete_or_release_noexcept
        self.release_exception_traits = create_exception_traits(release_method, cur_class, capi_generator)
        add_ref_method = Parser.TMethod()
        add_ref_method.m_name = Constants.add_ref_suffix
        add_ref_method.m_noexcept = True
        if cur_class.m_copy_or_add_ref_noexcept_filled:
            add_ref_method.m_noexcept = cur_class.m_copy_or_add_ref_noexcept
        self.add_ref_exception_traits = create_exception_traits(add_ref_method, cur_class, capi_generator)

    def get_suffix(self):
        return self.capi_generator.params_description.m_wrapper_class_suffix_reference_counted

    def generate_destructor(self):
        release_c_function_name = self.capi_generator.get_namespace_id().lower() + Constants.release_suffix
        self.capi_generator.inheritance_traits.generate_destructor(
            self.get_destructor_declaration(),
            release_c_function_name
        )
        c_function_declaration = 'void {release_c_function}({arguments_list})'.format(
            release_c_function=release_c_function_name,
            arguments_list=', '.join(self.release_exception_traits.get_c_argument_pairs())
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            method_call = 'intrusive_ptr_release(static_cast<{0}*>(object_pointer));'.format(
                self.cur_class.m_implementation_class_name
            )
            self.release_exception_traits.generate_implementation_call(method_call, '')
        self.put_source_line('')

    def generate_copy_constructor(self):
        self.put_line('{class_name}(const {class_name}& other){base_init}'.format(
            class_name=self.cur_class.m_name + self.get_suffix(), base_init=self.get_base_init()))
        with self.indent_scope():
            self.put_line('SetObject(other.{object_var});'.format(object_var=Constants.object_var))
            self.add_ref_exception_traits.generate_c_call(
                self.capi_generator.get_namespace_id().lower() + Constants.add_ref_suffix,
                '{c_function}({arguments})',
                False
            )
        self.put_line('{class_name}(void *object_pointer, bool add_ref){base_init}'.format(
            class_name=self.cur_class.m_name + self.get_suffix(), base_init=self.get_base_init()))
        with self.indent_scope():
            self.put_line('SetObject(object_pointer);'.format(object_var=Constants.object_var))
            self.put_line('if (add_ref && object_pointer)')
            with self.indent_scope():
                self.add_ref_exception_traits.generate_c_call(
                    self.capi_generator.get_namespace_id().lower() + Constants.add_ref_suffix,
                    '{c_function}({arguments})',
                    False
                )
        c_function_declaration = 'void {addref_c_function}({arguments_list})'.format(
            addref_c_function=self.capi_generator.get_namespace_id().lower() + Constants.add_ref_suffix,
            arguments_list=', '.join(self.add_ref_exception_traits.get_c_argument_pairs())
        )
        self.capi_generator.loader_traits.add_c_function_declaration(c_function_declaration)
        with self.indent_scope_source():
            method_call = 'intrusive_ptr_add_ref(static_cast<{0}*>(object_pointer));'.format(
                self.cur_class.m_implementation_class_name
            )
            self.add_ref_exception_traits.generate_implementation_call(method_call, '')
        self.put_source_line('')

    def generate_copy_or_add_ref_for_constructor(self):
        self.copy_method.m_arguments[0].m_name = Constants.object_var
        self.put_line('if ({object_var})'.format(object_var=Constants.object_var))
        with self.indent_scope():
            self.add_ref_exception_traits.generate_c_call(
                '_'.join(self.capi_generator.cur_namespace_path[:-1]).lower() + Constants.add_ref_suffix,
                '{c_function}({arguments})',
                False
            )


str_to_lifecycle = {
    Parser.TLifecycle.copy_semantic: CopySemantic,
    Parser.TLifecycle.raw_pointer_semantic: RawPointerSemantic,
    Parser.TLifecycle.reference_counted: RefCountedSemantic
}


def create_lifecycle_traits(cur_class, capi_generator):
    if cur_class.m_lifecycle in str_to_lifecycle:
        return str_to_lifecycle[cur_class.m_lifecycle](cur_class, capi_generator)
    raise ValueError


class CreateLifecycleTraits(object):
    def __init__(self, cur_class, capi_generator):
        self.cur_class = cur_class
        self.capi_generator = capi_generator
        self.previous_lifecycle_traits = capi_generator.lifecycle_traits

    def __enter__(self):
        self.capi_generator.lifecycle_traits = create_lifecycle_traits(self.cur_class, self.capi_generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.capi_generator.lifecycle_traits = self.previous_lifecycle_traits
