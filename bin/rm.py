#!/usr/bin/env python3
"""
rm - remove files or directories
Classic Unix rm implementation in Python
"""

import sys
import argparse
import os
import shutil


def print_usage():
    print("Usage: rm [OPTION]... FILE...")
    print("Remove (unlink) the FILE(s).")
    print()
    print("Options:")
    print("  -r, -R    remove directories and their contents recursively")
    print("  -f        force removal, ignore nonexistent files")
    print("  -v        verbose mode")


def remove_file(path, recursive=False, force=False, verbose=False):
    """Remove a file or directory."""
    try:
        # Check if path exists
        if not os.path.exists(path):
            if not force:
                print(f"rm: cannot remove '{path}': No such file or directory", file=sys.stderr)
            return not force

        # Remove
        if os.path.isdir(path):
            if not recursive:
                print(f"rm: cannot remove '{path}': Is a directory", file=sys.stderr)
                return False
            shutil.rmtree(path)
        else:
            os.remove(path)

        if verbose:
            print(f"removed '{path}'")

        return True

    except PermissionError:
        if not force:
            print(f"rm: cannot remove '{path}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        if not force:
            print(f"rm: {e}", file=sys.stderr)
        return False


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    recursive = False
    force = False
    verbose = False

    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char in ['r', 'R']:
                    recursive = True
                elif char == 'f':
                    force = True
                elif char == 'v':
                    verbose = True
                else:
                    print(f"rm: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'rm --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    if len(files) < 1:
        print("rm: missing operand", file=sys.stderr)
        print("Try 'rm --help' for more information.", file=sys.stderr)
        return 1

    # Remove each file
    success = True
    for path in files:
        if not remove_file(path, recursive, force, verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
