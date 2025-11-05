#!/usr/bin/env python3
"""
cut - remove sections from each line of files
Classic Unix cut implementation in Python
"""

import sys
import argparse


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
    parser = argparse.ArgumentParser(
        description='Print selected parts of lines from each FILE to standard output.'
    )

    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to process (default: stdin)')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--characters', metavar='LIST',
                       help='select only these characters')
    group.add_argument('-f', '--fields', metavar='LIST',
                       help='select only these fields')

    parser.add_argument('-d', '--delimiter', default='\t', metavar='DELIM',
                        help='use DELIM instead of TAB for field delimiter')

    args = parser.parse_args()

    # Parse the list
    char_list = None
    field_list = None

    if args.characters:
        char_list = parse_list(args.characters)
    elif args.fields:
        field_list = parse_list(args.fields)

    # If no files specified, read from stdin
    files = args.files if args.files else ['-']

    # Process files
    for filename in files:
        cut_file(filename, char_list, field_list, args.delimiter)

    return 0


if __name__ == '__main__':
    sys.exit(main())
