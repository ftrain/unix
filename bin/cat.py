#!/usr/bin/env python3
"""
cat - concatenate files and print on the standard output
Classic Unix cat implementation in Python
"""

import sys
import argparse


def cat_file(filename, number_lines=False, number_nonblank=False,
             squeeze_blank=False, show_ends=False, line_number=1):
    """
    Concatenate a file to stdout with optional formatting.
    Returns the next line number to use.
    """
    try:
        if filename == '-':
            f = sys.stdin
        else:
            f = open(filename, 'r')

        prev_blank = False

        for line in f:
            # Check if line is blank (just whitespace)
            is_blank = line.strip() == ''

            # Squeeze multiple blank lines
            if squeeze_blank and is_blank and prev_blank:
                continue

            prev_blank = is_blank

            # Remove trailing newline for processing
            line_content = line.rstrip('\n')

            # Build output
            output = []

            # Line numbering
            if number_lines or (number_nonblank and not is_blank):
                output.append(f"{line_number:6}  ")
                line_number += 1

            output.append(line_content)

            # Show end of line marker
            if show_ends:
                output.append('$')

            print(''.join(output))

        if filename != '-':
            f.close()

        return line_number

    except FileNotFoundError:
        print(f"cat: {filename}: No such file or directory", file=sys.stderr)
        return line_number
    except PermissionError:
        print(f"cat: {filename}: Permission denied", file=sys.stderr)
        return line_number
    except Exception as e:
        print(f"cat: {filename}: {e}", file=sys.stderr)
        return line_number


def main():
    parser = argparse.ArgumentParser(
        description='Concatenate FILE(s) to standard output.'
    )

    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to concatenate (default: stdin)')
    parser.add_argument('-n', '--number', action='store_true',
                        help='number all output lines')
    parser.add_argument('-b', '--number-nonblank', action='store_true',
                        help='number nonempty output lines')
    parser.add_argument('-s', '--squeeze-blank', action='store_true',
                        help='squeeze multiple adjacent blank lines')
    parser.add_argument('-E', '--show-ends', action='store_true',
                        help='display $ at end of each line')

    args = parser.parse_args()

    # -b overrides -n
    number_lines = args.number and not args.number_nonblank

    # If no files specified, read from stdin
    files = args.files if args.files else ['-']

    # Process files
    line_number = 1
    for filename in files:
        line_number = cat_file(filename, number_lines, args.number_nonblank,
                              args.squeeze_blank, args.show_ends, line_number)

    return 0


if __name__ == '__main__':
    sys.exit(main())
