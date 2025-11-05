#!/usr/bin/env python3
"""
tail - output the last part of files
Classic Unix tail implementation in Python
"""

import sys
import argparse
from collections import deque


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
    parser = argparse.ArgumentParser(
        description='Print the last 10 lines of each FILE to standard output.'
    )

    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to read (default: stdin)')
    parser.add_argument('-n', '--lines', type=int, default=10, metavar='NUM',
                        help='print the last NUM lines instead of the last 10')

    args = parser.parse_args()

    # If no files specified, read from stdin
    files = args.files if args.files else ['-']

    # Show headers if multiple files
    show_headers = len(files) > 1

    # Process files
    for i, filename in enumerate(files):
        if i > 0 and show_headers:
            print()
        tail_file(filename, args.lines, show_headers)

    return 0


if __name__ == '__main__':
    sys.exit(main())
