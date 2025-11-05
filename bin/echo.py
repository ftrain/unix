#!/usr/bin/env python3
"""
echo - display a line of text
Classic Unix echo implementation in Python
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Display a line of text.'
    )

    parser.add_argument('text', nargs='*', help='text to display')
    parser.add_argument('-n', '--no-newline', action='store_true',
                        help='do not output the trailing newline')

    args = parser.parse_args()

    output = ' '.join(args.text)

    if args.no_newline:
        print(output, end='')
    else:
        print(output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
