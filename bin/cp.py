#!/usr/bin/env python3
"""
cp - copy files and directories
Classic Unix cp implementation in Python
"""

import sys
import argparse
import os
import shutil


def print_usage():
    print("Usage: cp [OPTION]... SOURCE DEST")
    print("  or:  cp [OPTION]... SOURCE... DIRECTORY")
    print("Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.")
    print()
    print("Options:")
    print("  -r, -R    copy directories recursively")
    print("  -f        force overwrite")
    print("  -v        verbose mode")


def copy_file(source, dest, recursive=False, force=False, verbose=False):
    """Copy a file or directory."""
    try:
        # Check if source exists
        if not os.path.exists(source):
            print(f"cp: cannot stat '{source}': No such file or directory", file=sys.stderr)
            return False

        # If dest is a directory, copy into it
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(source))

        # Check if dest exists and not forcing
        if os.path.exists(dest) and not force:
            # In interactive mode, we'd ask. For now, just warn
            pass

        # Copy
        if os.path.isdir(source):
            if not recursive:
                print(f"cp: -r not specified; omitting directory '{source}'", file=sys.stderr)
                return False
            shutil.copytree(source, dest)
        else:
            shutil.copy2(source, dest)

        if verbose:
            print(f"'{source}' -> '{dest}'")

        return True

    except PermissionError:
        print(f"cp: cannot copy '{source}' to '{dest}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        print(f"cp: {e}", file=sys.stderr)
        return False


def main():
    if '--help' in sys.argv or len(sys.argv) < 3:
        print_usage()
        return 0 if '--help' in sys.argv else 1

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
                    print(f"cp: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'cp --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    if len(files) < 2:
        print("cp: missing file operand", file=sys.stderr)
        return 1

    # If multiple sources, dest must be a directory
    if len(files) > 2:
        dest = files[-1]
        if not os.path.isdir(dest):
            print(f"cp: target '{dest}' is not a directory", file=sys.stderr)
            return 1

        for source in files[:-1]:
            copy_file(source, dest, recursive, force, verbose)
    else:
        # Single source to dest
        copy_file(files[0], files[1], recursive, force, verbose)

    return 0


if __name__ == '__main__':
    sys.exit(main())
