#!/usr/bin/env python3
"""
echo - display a line of text
Classic Unix echo implementation in Python
"""

import sys


def main():
    # Simple echo - print all arguments separated by spaces
    args = sys.argv[1:]

    # Handle -n option (no trailing newline)
    newline = True
    if args and args[0] == '-n':
        newline = False
        args = args[1:]

    output = ' '.join(args)

    if newline:
        print(output)
    else:
        print(output, end='')

    return 0


if __name__ == '__main__':
    sys.exit(main())
