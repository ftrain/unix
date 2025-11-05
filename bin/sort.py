#!/usr/bin/env python3
"""
sort - sort lines of text files
Classic Unix sort implementation in Python
"""

import sys
import argparse


def sort_files(files, reverse=False, numeric=False, unique=False):
    """Read all files and sort their lines."""
    lines = []

    for filename in files:
        try:
            if filename == '-':
                f = sys.stdin
            else:
                f = open(filename, 'r')

            for line in f:
                lines.append(line.rstrip('\n'))

            if filename != '-':
                f.close()

        except FileNotFoundError:
            print(f"sort: cannot read: {filename}: No such file or directory",
                  file=sys.stderr)
            return 2
        except PermissionError:
            print(f"sort: cannot read: {filename}: Permission denied",
                  file=sys.stderr)
            return 2
        except Exception as e:
            print(f"sort: {filename}: {e}", file=sys.stderr)
            return 2

    # Sort the lines
    if numeric:
        # Numeric sort - try to convert to number, fallback to 0
        def numeric_key(line):
            try:
                return float(line.split()[0] if line.split() else '0')
            except (ValueError, IndexError):
                return 0
        lines.sort(key=numeric_key, reverse=reverse)
    else:
        lines.sort(reverse=reverse)

    # Remove duplicates if unique flag is set
    if unique:
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        lines = unique_lines

    # Print sorted lines
    for line in lines:
        print(line)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Sort lines of text FILE(s) and write to standard output.'
    )

    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to sort (default: stdin)')
    parser.add_argument('-r', '--reverse', action='store_true',
                        help='reverse the result of comparisons')
    parser.add_argument('-n', '--numeric-sort', action='store_true',
                        help='compare according to string numerical value')
    parser.add_argument('-u', '--unique', action='store_true',
                        help='output only unique lines')

    args = parser.parse_args()

    # If no files specified, read from stdin
    files = args.files if args.files else ['-']

    return sort_files(files, args.reverse, args.numeric_sort, args.unique)


if __name__ == '__main__':
    sys.exit(main())
