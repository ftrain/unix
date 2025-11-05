#!/usr/bin/env python3
"""
rm - remove files or directories
Classic Unix rm implementation in Python
"""

import sys
import argparse
import os
import shutil



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
    parser = argparse.ArgumentParser(
        description='Remove (unlink) the FILE(s).'
    )

    parser.add_argument('files', nargs='+', metavar='FILE',
                        help='files to remove')
    parser.add_argument('-r', '-R', '--recursive', action='store_true',
                        help='remove directories and their contents recursively')
    parser.add_argument('-f', '--force', action='store_true',
                        help='ignore nonexistent files and arguments, never prompt')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='explain what is being done')

    args = parser.parse_args()

    success = True
    for path in args.files:
        if not remove_file(path, args.recursive, args.force, args.verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
