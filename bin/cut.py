#!/usr/bin/env python3
"""
cut - remove sections from each line of files
Classic Unix cut implementation in Python
"""

import sys
import argparse


def print_usage():
    print("Usage: cut OPTION... [FILE]...")
    print("Print selected parts of lines from each FILE to standard output.")
    print()
    print("Options:")
    print("  -c LIST   select only these characters")
    print("  -f LIST   select only these fields")
    print("  -d DELIM  use DELIM instead of TAB for field delimiter")


def parse_list(list_str):
    """Parse a list like '1,3,5-7' into a set of indices."""
    indices = set()

    for part in list_str.split(','):
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start) if start else 1
            end = int(end) if end else float('inf')
            # Convert to 0-indexed
            for i in range(start - 1, end if end == float('inf') else end):
                indices.add(i)
        else:
            # Convert to 0-indexed
            indices.add(int(part) - 1)

    return indices


def cut_file(filename, char_list=None, field_list=None, delimiter='\t'):
    """Cut characters or fields from a file."""
    try:
        if filename == '-':
            f = sys.stdin
        else:
            f = open(filename, 'r')

        for line in f:
            line = line.rstrip('\n')

            if char_list is not None:
                # Character mode
                output = []
                for i in sorted(char_list):
                    if i < len(line):
                        output.append(line[i])
                    elif i == float('inf'):
                        output.append(line[max(char_list) - 1:])
                        break
                print(''.join(output))

            elif field_list is not None:
                # Field mode
                fields = line.split(delimiter)
                output = []
                for i in sorted(field_list):
                    if i < len(fields):
                        output.append(fields[i])
                print(delimiter.join(output))

        if filename != '-':
            f.close()

    except FileNotFoundError:
        print(f"cut: {filename}: No such file or directory", file=sys.stderr)
    except PermissionError:
        print(f"cut: {filename}: Permission denied", file=sys.stderr)
    except Exception as e:
        print(f"cut: {filename}: {e}", file=sys.stderr)


def main():
    if '--help' in sys.argv or len(sys.argv) < 2:
        print_usage()
        return 0 if '--help' in sys.argv else 1

    # Parse options
    char_list = None
    field_list = None
    delimiter = '\t'

    args = sys.argv[1:]
    files = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '-c':
            if i + 1 < len(args):
                char_list = parse_list(args[i + 1])
                i += 1
            else:
                print("cut: option requires an argument -- 'c'", file=sys.stderr)
                return 1
        elif arg == '-f':
            if i + 1 < len(args):
                field_list = parse_list(args[i + 1])
                i += 1
            else:
                print("cut: option requires an argument -- 'f'", file=sys.stderr)
                return 1
        elif arg == '-d':
            if i + 1 < len(args):
                delimiter = args[i + 1]
                i += 1
            else:
                print("cut: option requires an argument -- 'd'", file=sys.stderr)
                return 1
        elif not arg.startswith('-'):
            files.append(arg)

        i += 1

    if char_list is None and field_list is None:
        print("cut: you must specify a list of characters or fields", file=sys.stderr)
        return 1

    # If no files specified, read from stdin
    if not files:
        files = ['-']

    # Process files
    for filename in files:
        cut_file(filename, char_list, field_list, delimiter)

    return 0


if __name__ == '__main__':
    sys.exit(main())
