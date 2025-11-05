#!/usr/bin/env python3
"""
sort - sort lines of text files
Classic Unix sort implementation in Python
"""

import sys


def print_usage():
    print("Usage: sort [OPTION]... [FILE]...")
    print("Sort lines of text FILE(s) and write to standard output.")
    print()
    print("Options:")
    print("  -r    reverse the result of comparisons")
    print("  -n    compare according to string numerical value")
    print("  -u    output only unique lines")


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
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    reverse = False
    numeric = False
    unique = False

    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'r':
                    reverse = True
                elif char == 'n':
                    numeric = True
                elif char == 'u':
                    unique = True
                else:
                    print(f"sort: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'sort --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    # If no files specified, read from stdin
    if not files:
        files = ['-']

    return sort_files(files, reverse, numeric, unique)


if __name__ == '__main__':
    sys.exit(main())
