#!/usr/bin/env python3
"""
mv - move (rename) files
Classic Unix mv implementation in Python
"""

import sys
import argparse
import os
import shutil



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
    parser = argparse.ArgumentParser(
        description='Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.'
    )

    parser.add_argument('sources', nargs='+', metavar='SOURCE',
                        help='source file(s) or directory(ies)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force overwrite')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='explain what is being done')

    args = parser.parse_args()

    files = args.sources
    if len(files) < 2:
        parser.error("missing destination file operand after '%s'" % files[0] if files else "")

    # If multiple sources, dest must be a directory
    if len(files) > 2:
        dest = files[-1]
        if not os.path.isdir(dest):
            print(f"mv: target '{dest}' is not a directory", file=sys.stderr)
            return 1
        for source in files[:-1]:
            move_file(source, dest, args.force, args.verbose)
    else:
        move_file(files[0], files[1], args.force, args.verbose)

    return 0


if __name__ == '__main__':
    sys.exit(main())
