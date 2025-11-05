#!/usr/bin/env python3
"""
cp - copy files and directories
Classic Unix cp implementation in Python
"""

import sys
import argparse
import os
import shutil



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
    parser = argparse.ArgumentParser(
        description='Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.'
    )

    parser.add_argument('sources', nargs='+', metavar='SOURCE',
                        help='source file(s) to copy')
    parser.add_argument('-r', '-R', '--recursive', action='store_true',
                        help='copy directories recursively')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force overwrite')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='explain what is being done')

    args = parser.parse_args()

    files = args.sources
    if len(files) < 2:
        parser.error("missing destination file operand")

    # If multiple sources, dest must be a directory
    if len(files) > 2:
        dest = files[-1]
        if not os.path.isdir(dest):
            print(f"cp: target '{dest}' is not a directory", file=sys.stderr)
            return 1
        for source in files[:-1]:
            copy_file(source, dest, args.recursive, args.force, args.verbose)
    else:
        copy_file(files[0], files[1], args.recursive, args.force, args.verbose)

    return 0


if __name__ == '__main__':
    sys.exit(main())
