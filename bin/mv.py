#!/usr/bin/env python3
"""
mv - move (rename) files
Classic Unix mv implementation in Python
"""

import sys
import argparse
import os
import shutil


def print_usage():
    print("Usage: mv [OPTION]... SOURCE DEST")
    print("  or:  mv [OPTION]... SOURCE... DIRECTORY")
    print("Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.")
    print()
    print("Options:")
    print("  -f    force overwrite")
    print("  -v    verbose mode")


def move_file(source, dest, force=False, verbose=False):
    """Move a file or directory."""
    try:
        # Check if source exists
        if not os.path.exists(source):
            print(f"mv: cannot stat '{source}': No such file or directory", file=sys.stderr)
            return False

        # If dest is a directory, move into it
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(source))

        # Check if dest exists and not forcing
        if os.path.exists(dest) and not force:
            # In interactive mode, we'd ask. For now, just proceed
            pass

        # Move/rename
        shutil.move(source, dest)

        if verbose:
            print(f"'{source}' -> '{dest}'")

        return True

    except PermissionError:
        print(f"mv: cannot move '{source}' to '{dest}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        print(f"mv: {e}", file=sys.stderr)
        return False


def main():
    if '--help' in sys.argv or len(sys.argv) < 3:
        print_usage()
        return 0 if '--help' in sys.argv else 1

    # Parse options
    force = False
    verbose = False

    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'f':
                    force = True
                elif char == 'v':
                    verbose = True
                else:
                    print(f"mv: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'mv --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    if len(files) < 2:
        print("mv: missing file operand", file=sys.stderr)
        return 1

    # If multiple sources, dest must be a directory
    if len(files) > 2:
        dest = files[-1]
        if not os.path.isdir(dest):
            print(f"mv: target '{dest}' is not a directory", file=sys.stderr)
            return 1

        for source in files[:-1]:
            move_file(source, dest, force, verbose)
    else:
        # Single source to dest
        move_file(files[0], files[1], force, verbose)

    return 0


if __name__ == '__main__':
    sys.exit(main())
