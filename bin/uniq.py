#!/usr/bin/env python3
"""
uniq - report or omit repeated lines
Classic Unix uniq implementation in Python
"""

import sys
import argparse


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
    parser = argparse.ArgumentParser(
        description='Filter adjacent matching lines from INPUT, writing to OUTPUT.'
    )

    parser.add_argument('input', nargs='?', default='-', metavar='INPUT',
                        help='input file (default: stdin)')
    parser.add_argument('output', nargs='?', default='-', metavar='OUTPUT',
                        help='output file (default: stdout)')
    parser.add_argument('-c', '--count', action='store_true',
                        help='prefix lines by the number of occurrences')
    parser.add_argument('-d', '--repeated', action='store_true',
                        help='only print duplicate lines, one for each group')
    parser.add_argument('-u', '--unique', action='store_true',
                        help='only print unique lines')

    args = parser.parse_args()

    return uniq_lines(args.input, args.output, args.count,
                     args.repeated, args.unique)


if __name__ == '__main__':
    sys.exit(main())
