#!/usr/bin/env python3
"""
find - search for files in a directory hierarchy
Classic Unix find implementation in Python
"""

import sys
import argparse
import os
import stat
import fnmatch


def print_usage():
    print("Usage: find [PATH...] [EXPRESSION]")
    print("Search for files in a directory hierarchy.")
    print()
    print("Expressions:")
    print("  -name PATTERN    base of file name matches PATTERN")
    print("  -type TYPE       file is of type TYPE (f=file, d=directory)")
    print("  -print           print the full file name")


def find_files(paths, name_pattern=None, file_type=None, do_print=True):
    """Recursively find files matching criteria."""
    for start_path in paths:
        try:
            # Handle the starting path itself
            if not os.path.exists(start_path):
                print(f"find: '{start_path}': No such file or directory", file=sys.stderr)
                continue

            # Walk the directory tree
            for root, dirs, files in os.walk(start_path):
                # Check directories
                for dirname in dirs:
                    full_path = os.path.join(root, dirname)
                    if check_match(full_path, dirname, name_pattern, 'd', file_type):
                        if do_print:
                            print(full_path)

                # Check files
                for filename in files:
                    full_path = os.path.join(root, filename)
                    if check_match(full_path, filename, name_pattern, 'f', file_type):
                        if do_print:
                            print(full_path)

        except PermissionError as e:
            print(f"find: '{start_path}': Permission denied", file=sys.stderr)
        except Exception as e:
            print(f"find: {e}", file=sys.stderr)

    return 0


def check_match(full_path, name, name_pattern, actual_type, desired_type):
    """Check if a file matches the search criteria."""
    # Check name pattern
    if name_pattern and not fnmatch.fnmatch(name, name_pattern):
        return False

    # Check file type
    if desired_type:
        if desired_type == 'f' and actual_type != 'f':
            return False
        if desired_type == 'd' and actual_type != 'd':
            return False

    return True


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    args = sys.argv[1:]

    if not args:
        # Default: find current directory
        args = ['.']

    # Parse arguments
    paths = []
    name_pattern = None
    file_type = None
    do_print = True

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '-name':
            if i + 1 < len(args):
                name_pattern = args[i + 1]
                i += 1
            else:
                print("find: -name requires an argument", file=sys.stderr)
                return 1

        elif arg == '-type':
            if i + 1 < len(args):
                file_type = args[i + 1]
                if file_type not in ['f', 'd']:
                    print(f"find: invalid type '{file_type}'", file=sys.stderr)
                    return 1
                i += 1
            else:
                print("find: -type requires an argument", file=sys.stderr)
                return 1

        elif arg == '-print':
            do_print = True

        elif not arg.startswith('-'):
            paths.append(arg)

        else:
            print(f"find: unknown option: {arg}", file=sys.stderr)
            return 1

        i += 1

    # Default path is current directory
    if not paths:
        paths = ['.']

    return find_files(paths, name_pattern, file_type, do_print)


if __name__ == '__main__':
    sys.exit(main())
