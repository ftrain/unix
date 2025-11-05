#!/usr/bin/env python3
"""
chmod - change file mode bits
Classic Unix chmod implementation in Python
"""

import sys
import argparse
import os
import stat


def print_usage():
    print("Usage: chmod [OPTION]... MODE FILE...")
    print("Change the mode of each FILE to MODE.")
    print()
    print("Options:")
    print("  -v    verbose mode")
    print("  -R    change files and directories recursively")
    print()
    print("MODE is an octal number (e.g., 755, 644)")


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
    if '--help' in sys.argv or len(sys.argv) < 3:
        print_usage()
        return 0 if '--help' in sys.argv else 1

    # Parse options
    recursive = False
    verbose = False

    args = sys.argv[1:]
    mode_str = None
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'R':
                    recursive = True
                elif char == 'v':
                    verbose = True
                else:
                    print(f"chmod: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'chmod --help' for more information.", file=sys.stderr)
                    return 1
        elif mode_str is None:
            mode_str = arg
        else:
            files.append(arg)

    if mode_str is None:
        print("chmod: missing mode operand", file=sys.stderr)
        return 1

    mode = parse_mode(mode_str)
    if mode is None:
        print(f"chmod: invalid mode: '{mode_str}'", file=sys.stderr)
        return 1

    if len(files) < 1:
        print("chmod: missing operand after mode", file=sys.stderr)
        return 1

    # Change mode for each file
    success = True
    for path in files:
        if not change_mode(path, mode, recursive, verbose):
            success = False

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
