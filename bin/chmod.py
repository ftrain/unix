#!/usr/bin/env python3
"""
chmod - change file mode bits
Classic Unix chmod implementation in Python
"""

import sys
import argparse
import os
import stat



def parse_mode(mode_str):
    """Parse octal mode string to integer."""
    try:
        return int(mode_str, 8)
    except ValueError:
        return None


def change_mode(path, mode, recursive=False, verbose=False):
    """Change file mode."""
    try:
        os.chmod(path, mode)

        if verbose:
            print(f"mode of '{path}' changed to {oct(mode)[2:]}")

        # Recursive mode
        if recursive and os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for name in dirs + files:
                    full_path = os.path.join(root, name)
                    try:
                        os.chmod(full_path, mode)
                        if verbose:
                            print(f"mode of '{full_path}' changed to {oct(mode)[2:]}")
                    except Exception as e:
                        print(f"chmod: cannot access '{full_path}': {e}", file=sys.stderr)

        return True

    except FileNotFoundError:
        print(f"chmod: cannot access '{path}': No such file or directory", file=sys.stderr)
        return False
    except PermissionError:
        print(f"chmod: changing permissions of '{path}': Permission denied", file=sys.stderr)
        return False
    except Exception as e:
        print(f"chmod: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Change the mode of each FILE to MODE.'
    )

    parser.add_argument('mode', metavar='MODE',
                        help='octal mode (e.g., 755, 644)')
    parser.add_argument('files', nargs='+', metavar='FILE',
                        help='files to change mode')
    parser.add_argument('-R', '--recursive', action='store_true',
                        help='change files and directories recursively')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='output a diagnostic for every file processed')

    args = parser.parse_args()

    mode = parse_mode(args.mode)
    if mode is None:
        parser.error(f"invalid mode: '{args.mode}'")

    success = True
    for path in args.files:
        if not change_mode(path, mode, args.recursive, args.verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
