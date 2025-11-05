#!/usr/bin/env python3
"""
grep - search for patterns in files
Classic Unix grep implementation in Python
"""

import sys
import re


def print_usage():
    print("Usage: grep [OPTION]... PATTERN [FILE]...")
    print("Search for PATTERN in each FILE or standard input.")
    print()
    print("Options:")
    print("  -i    ignore case distinctions")
    print("  -v    invert match (select non-matching lines)")
    print("  -n    print line numbers with output")
    print("  -c    print only a count of matching lines")
    print("  -h    suppress file names on output")
    print("  -l    print only names of files with matches")


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
    if len(sys.argv) < 2:
        print_usage()
        return 2

    # Parse options
    ignore_case = False
    invert = False
    show_line_numbers = False
    count_only = False
    suppress_filename = False
    files_only = False

    args = sys.argv[1:]
    pattern = None
    files = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '--help':
            print_usage()
            return 0
        elif arg.startswith('-') and arg != '-':
            # Parse options
            for char in arg[1:]:
                if char == 'i':
                    ignore_case = True
                elif char == 'v':
                    invert = True
                elif char == 'n':
                    show_line_numbers = True
                elif char == 'c':
                    count_only = True
                elif char == 'h':
                    suppress_filename = True
                elif char == 'l':
                    files_only = True
                else:
                    print(f"grep: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'grep --help' for more information.", file=sys.stderr)
                    return 2
        else:
            # First non-option argument is the pattern
            if pattern is None:
                pattern = arg
            else:
                files.append(arg)

        i += 1

    if pattern is None:
        print("grep: missing pattern", file=sys.stderr)
        print("Try 'grep --help' for more information.", file=sys.stderr)
        return 2

    return grep(pattern, files, ignore_case, invert, show_line_numbers,
                count_only, suppress_filename, files_only)


if __name__ == '__main__':
    sys.exit(main())
