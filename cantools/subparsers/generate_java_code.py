import argparse
import copy
import os
import os.path
import re

from .. import database
from ..database.can.java_model_source import generate_model_class
from ..database.can.java_native_source import generate_native_class
from ..database.can.java_jni_source import generate_jni
from ..database.can.java_jni_cmake import generate_cmake
from ..database.can.java_jni_log_header import generate_log_header
from .generate_c_source import _do_generate_c_source


def _canonical(value):
    """Replace anything but 'a-z', 'A-Z' and '0-9' with '_'.

    """
    return re.sub(r'[^a-zA-Z0-9]', '_', value)


def camel_to_snake_case(value):
    value = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', value)
    value = re.sub(r'(_+)', '_', value)
    value = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', value).lower()
    value = _canonical(value)
    return value


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components[0:])


def _do_generate_java_code(args):
    copy_args = copy.copy(args)
    dbase = database.load_file(args.infile,
                               encoding=args.encoding,
                               prune_choices=args.prune,
                               strict=not args.no_strict)

    if args.database_name is None:
        basename = os.path.basename(args.infile)
        database_name = os.path.splitext(basename)[0]
        database_name = camel_to_snake_case(database_name)
    else:
        database_name = args.database_name

    _do_generate_c_source(copy_args)

    generate_model_class(args.output_directory,
                         dbase,
                         database_name,
                         args.package,
                         args.bit_fields,
                         args.node)

    generate_native_class(args.output_directory,
                          dbase,
                          database_name,
                          args.package,
                          args.android,
                          args.node)

    generate_jni(args.output_directory,
                 dbase,
                 database_name,
                 args.package,
                 args.android,
                 args.node)

    generate_cmake(args.output_directory,
                   database_name)

    generate_log_header(args.output_directory)

    print('Successfully generated')


def add_subparser(subparsers):
    generate_java_code_parser = subparsers.add_parser(
        'generate_java_code',
        description='Generate Java source code from given database file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    generate_java_code_parser.add_argument(
        '--database-name',
        help=('The database name.  Uses the stem of the input file name if not'
              ' specified.'))
    generate_java_code_parser.add_argument(
        '--no-floating-point-numbers',
        action='store_true',
        default=False,
        help='No floating point numbers in the generated code.')
    generate_java_code_parser.add_argument(
        '--bit-fields',
        action='store_true',
        help='Use bit fields to minimize struct sizes.')
    generate_java_code_parser.add_argument(
        '-e', '--encoding',
        help='File encoding.')
    generate_java_code_parser.add_argument(
        '--prune',
        action='store_true',
        help='Try to shorten the names of named signal choices.')
    generate_java_code_parser.add_argument(
        '--no-strict',
        action='store_true',
        help='Skip database consistency checks.')
    generate_java_code_parser.add_argument(
        '-f', '--generate-fuzzer',
        action='store_true',
        help='Also generate fuzzer source code.')
    generate_java_code_parser.add_argument(
        '-o', '--output-directory',
        default='.',
        help='Directory in which to write output files.')
    generate_java_code_parser.add_argument(
        '--use-float',
        action='store_true',
        default=False,
        help='Use float instead of double for floating point generation.')
    generate_java_code_parser.add_argument(
        'infile',
        help='Input database file.')
    generate_java_code_parser.add_argument(
        '--node',
        help='Generate pack/unpack functions only for messages sent/received by the node.')
    generate_java_code_parser.add_argument(
        '--package',
        default="can.tools",
        help='class package')
    generate_java_code_parser.add_argument(
        '--android',
        default=False,
        help='Used in android platform')
    generate_java_code_parser.set_defaults(func=_do_generate_java_code)
