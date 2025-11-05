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
    parser = argparse.ArgumentParser(
        description='Remove the DIRECTORY(ies), if they are empty.'
    )

    parser.add_argument('directories', nargs='+', metavar='DIRECTORY',
                        help='directories to remove')
    parser.add_argument('-p', '--parents', action='store_true',
                        help='remove DIRECTORY and its ancestors')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='output a diagnostic for every directory processed')

    args = parser.parse_args()

    # Remove each directory
    success = True
    for path in args.directories:
        if not remove_directory(path, args.parents, args.verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
