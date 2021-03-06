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


import os


class AtomicString(object):
    def __init__(self, string_value):
        self.value = string_value

    def get_lines(self):
        return [self.value]


class FileGenerator(object):
    def __init__(self, filename):
        self.filename = filename
        self.cur_indent = 0
        self.file_header = None
        self.copyright_header = None
        self.automatic_generation_warning = None
        self.lines = []

    def __del__(self):
        self.__write()

    def __write(self):
        if self.filename:
            dir_name = os.path.dirname(self.filename)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(self.filename, 'w') as output_file:
                if self.file_header:
                    output_file.write(self.file_header + '\n')
                if self.copyright_header:
                    output_file.write(self.copyright_header + '\n\n')
                if self.automatic_generation_warning:
                    output_file.write(self.automatic_generation_warning + '\n\n')
                for line in self.get_lines():
                    output_file.write(line)

    def get_lines(self):
        result = []
        for line in self.lines:
            for elementary_line in line.get_lines():
                result.append(elementary_line)
        return result

    def increase_indent(self):
        self.cur_indent += 4

    def decrease_indent(self):
        self.cur_indent -= 4
        if self.cur_indent < 0:
            raise IndentationError

    def get_indent_str(self):
        return ' ' * self.cur_indent

    def put_line(self, line, eol='\n'):
        self.lines.append(AtomicString(self.get_indent_str() + line + eol))

    def put_file(self, another_file):
        self.lines.append(another_file)

    def put_python_header(self):
        self.file_header = '#!/usr/bin/env python'

    def put_python_gnu_gpl_copyright_header(self):
        self.put_copyright_header(
            '#\n'
            '# Beautiful Capi generates beautiful C API wrappers for your C++ classes\n'
            '# Copyright (C) 2015 Petr Petrovich Petrov\n'
            '#\n'
            '# This file is part of Beautiful Capi.\n'
            '#\n'
            '# Beautiful Capi is free software: you can redistribute it and/or modify\n'
            '# it under the terms of the GNU General Public License as published by\n'
            '# the Free Software Foundation, either version 3 of the License, or\n'
            '# (at your option) any later version.\n'
            '#\n'
            '# Beautiful Capi is distributed in the hope that it will be useful,\n'
            '# but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
            '# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
            '# GNU General Public License for more details.\n'
            '#\n'
            '# You should have received a copy of the GNU General Public License\n'
            '# along with Beautiful Capi.  If not, see <http://www.gnu.org/licenses/>.\n'
            '#\n'
        )

    def put_copyright_header(self, copyright_header_text):
        self.copyright_header = copyright_header_text

    def put_python_automatic_generation_warning(self, empty_lines=True):
        self.put_automatic_generation_warning(
            '#\n'
            '# WARNING: This file was automatically generated by Xsd2Python3.py program!\n'
            '# Do not edit this file! Please edit the source XSD schema.\n'
            '#\n'
        )

    def put_automatic_generation_warning(self, warning_text):
        self.automatic_generation_warning = warning_text

    def put_begin_cpp_comments(self, params_description):
        self.put_copyright_header(params_description.m_copyright_header)
        self.put_automatic_generation_warning(params_description.m_automatic_generated_warning)


class Indent(object):
    def __init__(self, file_generator):
        self.file_generator = file_generator

    def __enter__(self):
        self.file_generator.increase_indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_generator.decrease_indent()


class Unindent(object):
    def __init__(self, file_generator):
        self.file_generator = file_generator

    def __enter__(self):
        self.file_generator.decrease_indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_generator.increase_indent()


class IndentScope(Indent):
    def __init__(self, file_generator, ending='}'):
        super().__init__(file_generator)
        self.ending = ending

    def __enter__(self):
        self.file_generator.put_line('{')
        super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.file_generator.put_line(self.ending)


class WatchdogScope(object):
    def __init__(self, file_generator, watchdog_string):
        self.file_generator = file_generator
        self.watchdog_string = watchdog_string

    def __enter__(self):
        self.file_generator.put_line('#ifndef {0}'.format(self.watchdog_string))
        self.file_generator.put_line('#define {0}'.format(self.watchdog_string))
        self.file_generator.put_line('')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_generator.put_line('')
        self.file_generator.put_line('#endif /* {0} */'.format(self.watchdog_string))
        self.file_generator.put_line('')


class IfDefScope(object):
    def __init__(self, file_generator, condition_string):
        self.file_generator = file_generator
        self.condition_string = condition_string

    def __enter__(self):
        self.file_generator.put_line('#ifdef {0}'.format(self.condition_string))
        self.file_generator.put_line('')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_generator.put_line('')
        self.file_generator.put_line('#endif /* {0} */'.format(self.condition_string))


class NewFileScope(object):
    def __init__(self, file_generator, capi_generator):
        self.file_generator = file_generator
        self.previous_file_generator = capi_generator.output_header
        self.capi_generator = capi_generator

    def __enter__(self):
        self.capi_generator.output_header = self.file_generator

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.capi_generator.output_header = self.previous_file_generator
