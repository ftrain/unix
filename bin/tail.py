#!/usr/bin/env python3
"""
tail - output the last part of files
Classic Unix tail implementation in Python
"""

import sys
from collections import deque


def print_usage():
    print("Usage: tail [OPTION]... [FILE]...")
    print("Print the last 10 lines of each FILE to standard output.")
    print("With more than one FILE, precede each with a header giving the file name.")
    print()
    print("Options:")
    print("  -n NUM    print the last NUM lines instead of the last 10")
    print("  -NUM      same as -n NUM")


def tail_file(filename, num_lines=10, show_header=False):
    """Print the last num_lines of a file."""
    try:
        if filename == '-':
            f = sys.stdin
            display_name = ''
        else:
            f = open(filename, 'r')
            display_name = filename

        if show_header:
            print(f"==> {display_name} <==")

        # Use a deque to efficiently keep last N lines
        last_lines = deque(maxlen=num_lines)

        for line in f:
            last_lines.append(line)

        # Print the last lines
        for line in last_lines:
            print(line, end='')

        if filename != '-':
            f.close()

    except FileNotFoundError:
        print(f"tail: cannot open '{filename}' for reading: No such file or directory",
              file=sys.stderr)
    except PermissionError:
        print(f"tail: cannot open '{filename}' for reading: Permission denied",
              file=sys.stderr)
    except Exception as e:
        print(f"tail: {filename}: {e}", file=sys.stderr)


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    num_lines = 10
    args = sys.argv[1:]
    files = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '-n':
            # Next argument should be the number
            if i + 1 < len(args):
                try:
                    num_lines = int(args[i + 1])
                except ValueError:
                    print(f"tail: invalid number of lines: '{args[i + 1]}'",
                          file=sys.stderr)
                    return 1
                i += 1
            else:
                print("tail: option requires an argument -- 'n'", file=sys.stderr)
                return 1
        elif arg.startswith('-') and arg != '-':
            # Check if it's -NUM format
            try:
                num_lines = int(arg[1:])
            except ValueError:
                print(f"tail: invalid option -- '{arg[1:]}'", file=sys.stderr)
                print("Try 'tail --help' for more information.", file=sys.stderr)
                return 1
        else:
            files.append(arg)

        i += 1

    # If no files specified, read from stdin
    if not files:
        files = ['-']

    # Show headers if multiple files
    show_headers = len(files) > 1

    # Process files
    for i, filename in enumerate(files):
        if i > 0 and show_headers:
            print()
        tail_file(filename, num_lines, show_headers)

    return 0


if __name__ == '__main__':
    sys.exit(main())
