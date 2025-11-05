#!/usr/bin/env python3
"""
grep - search for patterns in files
Classic Unix grep implementation in Python
"""

import sys
import re
import argparse


def grep(pattern, files, ignore_case=False, invert=False,
         show_line_numbers=False, count_only=False,
         suppress_filename=False, files_only=False):

    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        print(f"grep: invalid pattern: {e}", file=sys.stderr)
        return 2

    # If no files specified, read from stdin
    if not files:
        files = ['-']

    # Determine if we should show filenames
    show_filename = len(files) > 1 and not suppress_filename

    exit_status = 1  # Default: no matches found

    for filename in files:
        try:
            if filename == '-':
                f = sys.stdin
                display_name = '(standard input)'
            else:
                f = open(filename, 'r')
                display_name = filename

            match_count = 0
            line_number = 0

            for line in f:
                line_number += 1
                # Remove trailing newline for matching
                line_stripped = line.rstrip('\n')

                matches = regex.search(line_stripped) is not None
                if invert:
                    matches = not matches

                if matches:
                    match_count += 1
                    exit_status = 0  # Found at least one match

                    if count_only or files_only:
                        continue

                    # Build output line
                    output = []
                    if show_filename:
                        output.append(f"{display_name}:")
                    if show_line_numbers:
                        output.append(f"{line_number}:")
                    output.append(line_stripped)

                    print(''.join(output))

            if count_only:
                if show_filename:
                    print(f"{display_name}:{match_count}")
                else:
                    print(match_count)

            if files_only and match_count > 0:
                print(display_name)

            if filename != '-':
                f.close()

        except FileNotFoundError:
            print(f"grep: {filename}: No such file or directory", file=sys.stderr)
            return 2
        except PermissionError:
            print(f"grep: {filename}: Permission denied", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"grep: {filename}: {e}", file=sys.stderr)
            return 2

    return exit_status


def main():
    parser = argparse.ArgumentParser(
        description='Search for PATTERN in each FILE or standard input.',
        add_help=False
    )
    parser.add_argument('--help', action='help',
                        help='show this help message and exit')

    parser.add_argument('pattern', help='pattern to search for')
    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to search (default: stdin)')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='ignore case distinctions')
    parser.add_argument('-v', '--invert-match', action='store_true',
                        help='select non-matching lines')
    parser.add_argument('-n', '--line-number', action='store_true',
                        help='print line numbers with output')
    parser.add_argument('-c', '--count', action='store_true',
                        help='print only a count of matching lines')
    parser.add_argument('-h', '--no-filename', action='store_true',
                        help='suppress file names on output')
    parser.add_argument('-l', '--files-with-matches', action='store_true',
                        help='print only names of files with matches')

    args = parser.parse_args()

    return grep(args.pattern, args.files, args.ignore_case, args.invert_match,
                args.line_number, args.count, args.no_filename,
                args.files_with_matches)


if __name__ == '__main__':
    sys.exit(main())
