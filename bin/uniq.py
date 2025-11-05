#!/usr/bin/env python3
"""
uniq - report or omit repeated lines
Classic Unix uniq implementation in Python
"""

import sys


def print_usage():
    print("Usage: uniq [OPTION]... [INPUT [OUTPUT]]")
    print("Filter adjacent matching lines from INPUT (or standard input),")
    print("writing to OUTPUT (or standard output).")
    print()
    print("Options:")
    print("  -c    prefix lines by the number of occurrences")
    print("  -d    only print duplicate lines, one for each group")
    print("  -u    only print unique lines")


def uniq_lines(input_file, output_file, count=False, duplicates_only=False,
               unique_only=False):
    """Process lines and output unique or duplicate lines."""
    try:
        if input_file == '-':
            f_in = sys.stdin
        else:
            f_in = open(input_file, 'r')

        if output_file == '-':
            f_out = sys.stdout
        else:
            f_out = open(output_file, 'w')

        prev_line = None
        line_count = 0

        def output_line(line, count_val):
            """Output a line with optional count."""
            if duplicates_only and count_val <= 1:
                return
            if unique_only and count_val > 1:
                return

            if count:
                f_out.write(f"{count_val:7} {line}\n")
            else:
                f_out.write(f"{line}\n")

        for line in f_in:
            line = line.rstrip('\n')

            if line == prev_line:
                line_count += 1
            else:
                # Output previous line if exists
                if prev_line is not None:
                    output_line(prev_line, line_count)

                prev_line = line
                line_count = 1

        # Output last line
        if prev_line is not None:
            output_line(prev_line, line_count)

        if input_file != '-':
            f_in.close()
        if output_file != '-':
            f_out.close()

    except FileNotFoundError as e:
        print(f"uniq: {e}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"uniq: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"uniq: {e}", file=sys.stderr)
        return 1

    return 0


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    count = False
    duplicates_only = False
    unique_only = False

    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'c':
                    count = True
                elif char == 'd':
                    duplicates_only = True
                elif char == 'u':
                    unique_only = True
                else:
                    print(f"uniq: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'uniq --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    # Determine input and output files
    input_file = files[0] if len(files) > 0 else '-'
    output_file = files[1] if len(files) > 1 else '-'

    return uniq_lines(input_file, output_file, count, duplicates_only, unique_only)


if __name__ == '__main__':
    sys.exit(main())
