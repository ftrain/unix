#!/usr/bin/env python3
"""
mkdir - make directories
Classic Unix mkdir implementation in Python
"""

import sys
import argparse
import os


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
    parser = argparse.ArgumentParser(
        description='Create the DIRECTORY(ies), if they do not already exist.'
    )

    parser.add_argument('directories', nargs='+', metavar='DIRECTORY',
                        help='directories to create')
    parser.add_argument('-p', '--parents', action='store_true',
                        help='make parent directories as needed')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print a message for each created directory')

    args = parser.parse_args()

    # Create each directory
    success = True
    for path in args.directories:
        if not make_directory(path, args.parents, args.verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
