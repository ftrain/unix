#!/usr/bin/env python3
"""
tee - read from standard input and write to standard output and files
Classic Unix tee implementation in Python
"""

import sys
import argparse


def print_usage():
    print("Usage: tee [OPTION]... [FILE]...")
    print("Copy standard input to each FILE, and also to standard output.")
    print()
    print("Options:")
    print("  -a    append to the given FILEs, do not overwrite")


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    append = False
    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'a':
                    append = True
                else:
                    print(f"tee: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'tee --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    # Open output files
    file_handles = []
    mode = 'a' if append else 'w'

    try:
        for filename in files:
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
