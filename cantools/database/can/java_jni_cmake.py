import os
import os.path
import time
import traceback

from .java_model_source import camel_case
from ...version import __version__

SOURCE_FMT = '''\
# The MIT License (MIT)
#
# Copyright (c) 2018-2019 Erik Moqvist
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This file was generated by cantools version {version} {date}.

# For more information about using CMake with Android Studio, read the
# documentation: https://d.android.com/studio/projects/add-native-code.html

# Sets the minimum version of CMake required to build the native library.
cmake_minimum_required(VERSION 3.18.1)

project("{database_name}")

add_library({database_name} SHARED {jni_file_name}.cpp {database_name}.c)

find_library(log-lib log)

target_link_libraries({database_name} ${{log-lib}})
'''


def generate_cmake(output_directory,
                   database_name):
    try:
        date = time.ctime()
        jni_file_name = camel_case(database_name)
        source = SOURCE_FMT.format(version=__version__,
                                   date=date,
                                   database_name=database_name,
                                   jni_file_name=jni_file_name)
        filename_cmake = "CMakeLists.txt"
        os.makedirs(output_directory, exist_ok=True)
        path_cmake = os.path.join(output_directory, filename_cmake)
        with open(path_cmake, 'w') as fout:
            fout.write(source)
    except Exception as e:
        print(e.args)
        print(traceback.format_exc())
