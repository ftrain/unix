#!/usr/bin/env python3
"""
tee - read from standard input and write to standard output and files
Classic Unix tee implementation in Python
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Copy standard input to each FILE, and also to standard output.'
    )

    parser.add_argument('files', nargs='*', metavar='FILE',
                        help='files to write to')
    parser.add_argument('-a', '--append', action='store_true',
                        help='append to the given FILEs, do not overwrite')

    args = parser.parse_args()

    # Open output files
    file_handles = []
    mode = 'a' if args.append else 'w'

    try:
        for filename in args.files:
            try:
                file_handles.append(open(filename, mode))
            except Exception as e:
                print(f"tee: {filename}: {e}", file=sys.stderr)

        # Read from stdin and write to stdout and all files
        for line in sys.stdin:
            # Write to stdout
            print(line, end='')

            # Write to all files
            for f in file_handles:
                try:
                    f.write(line)
                except Exception as e:
                    print(f"tee: write error: {e}", file=sys.stderr)

    finally:
        # Close all files
        for f in file_handles:
            try:
                f.close()
            except:
                pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
