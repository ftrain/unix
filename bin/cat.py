#!/usr/bin/env python3
"""
cat - concatenate files and print on the standard output
Classic Unix cat implementation in Python
"""

import sys


def print_usage():
    print("Usage: cat [OPTION]... [FILE]...")
    print("Concatenate FILE(s) to standard output.")
    print()
    print("Options:")
    print("  -n    number all output lines")
    print("  -b    number nonempty output lines")
    print("  -s    squeeze multiple adjacent blank lines")
    print("  -E    display $ at end of each line")


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
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    number_lines = False
    number_nonblank = False
    squeeze_blank = False
    show_ends = False

    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'n':
                    number_lines = True
                elif char == 'b':
                    number_nonblank = True
                elif char == 's':
                    squeeze_blank = True
                elif char == 'E':
                    show_ends = True
                else:
                    print(f"cat: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'cat --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    # -b overrides -n
    if number_nonblank:
        number_lines = False

    # If no files specified, read from stdin
    if not files:
        files = ['-']

    # Process files
    line_number = 1
    for filename in files:
        line_number = cat_file(filename, number_lines, number_nonblank,
                              squeeze_blank, show_ends, line_number)

    return 0


if __name__ == '__main__':
    sys.exit(main())
