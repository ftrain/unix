#!/usr/bin/env python3
"""
mkdir - make directories
Classic Unix mkdir implementation in Python
"""

import sys
import argparse
import os


def print_usage():
    print("Usage: mkdir [OPTION]... DIRECTORY...")
    print("Create the DIRECTORY(ies), if they do not already exist.")
    print()
    print("Options:")
    print("  -p    make parent directories as needed")
    print("  -v    verbose mode")


def make_directory(path, parents=False, verbose=False):
    """Create a directory."""
    try:
        if parents:
            os.makedirs(path, exist_ok=True)
        else:
            os.mkdir(path)

        if verbose:
            print(f"mkdir: created directory '{path}'")

        return True

    except FileExistsError:
        print(f"mkdir: cannot create directory '{path}': File exists", file=sys.stderr)
        return False
    except PermissionError:
        print(f"mkdir: cannot create directory '{path}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        print(f"mkdir: {e}", file=sys.stderr)
        return False


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    parents = False
    verbose = False

    args = sys.argv[1:]
    directories = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'p':
                    parents = True
                elif char == 'v':
                    verbose = True
                else:
                    print(f"mkdir: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'mkdir --help' for more information.", file=sys.stderr)
                    return 1
        else:
            directories.append(arg)

    if len(directories) < 1:
        print("mkdir: missing operand", file=sys.stderr)
        print("Try 'mkdir --help' for more information.", file=sys.stderr)
        return 1

    # Create each directory
    success = True
    for path in directories:
        if not make_directory(path, parents, verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
