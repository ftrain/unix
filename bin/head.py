#!/usr/bin/env python3
"""
head - output the first part of files
Classic Unix head implementation in Python
"""

import sys
import argparse


def head_file(filename, num_lines=10, show_header=False):
    """Print the first num_lines of a file."""
    try:
        if filename == '-':
            f = sys.stdin
            display_name = ''
        else:
            f = open(filename, 'r')
            display_name = filename

        if show_header:
            print(f"==> {display_name} <==")

        count = 0
        for line in f:
            if count >= num_lines:
                break
            print(line, end='')
            count += 1

        if filename != '-':
            f.close()

    except FileNotFoundError:
        print(f"head: cannot open '{filename}' for reading: No such file or directory",
              file=sys.stderr)
    except PermissionError:
        print(f"head: cannot open '{filename}' for reading: Permission denied",
              file=sys.stderr)
    except Exception as e:
        print(f"head: {filename}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Print the first 10 lines of each FILE to standard output.'
    )

    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to read (default: stdin)')
    parser.add_argument('-n', '--lines', type=int, default=10, metavar='NUM',
                        help='print the first NUM lines instead of the first 10')

    args = parser.parse_args()

    # If no files specified, read from stdin
    files = args.files if args.files else ['-']

    # Show headers if multiple files
    show_headers = len(files) > 1

    # Process files
    for i, filename in enumerate(files):
        if i > 0 and show_headers:
            print()
        head_file(filename, args.lines, show_headers)

    return 0


if __name__ == '__main__':
    sys.exit(main())
