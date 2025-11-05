#!/usr/bin/env python3
"""
rmdir - remove empty directories
Classic Unix rmdir implementation in Python
"""

import sys
import argparse
import os


def print_usage():
    print("Usage: rmdir [OPTION]... DIRECTORY...")
    print("Remove the DIRECTORY(ies), if they are empty.")
    print()
    print("Options:")
    print("  -p    remove DIRECTORY and its ancestors")
    print("  -v    verbose mode")


def remove_directory(path, parents=False, verbose=False):
    """Remove an empty directory."""
    try:
        os.rmdir(path)

        if verbose:
            print(f"rmdir: removing directory, '{path}'")

        # Remove parents if requested
        if parents:
            parent = os.path.dirname(path)
            while parent and parent != '/':
                try:
                    os.rmdir(parent)
                    if verbose:
                        print(f"rmdir: removing directory, '{parent}'")
                    parent = os.path.dirname(parent)
                except:
                    break

        return True

    except FileNotFoundError:
        print(f"rmdir: failed to remove '{path}': No such file or directory", file=sys.stderr)
        return False
    except OSError:
        print(f"rmdir: failed to remove '{path}': Directory not empty", file=sys.stderr)
        return False
    except PermissionError:
        print(f"rmdir: failed to remove '{path}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        print(f"rmdir: {e}", file=sys.stderr)
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
                    print(f"rmdir: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'rmdir --help' for more information.", file=sys.stderr)
                    return 1
        else:
            directories.append(arg)

    if len(directories) < 1:
        print("rmdir: missing operand", file=sys.stderr)
        print("Try 'rmdir --help' for more information.", file=sys.stderr)
        return 1

    # Remove each directory
    success = True
    for path in directories:
        if not remove_directory(path, parents, verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
