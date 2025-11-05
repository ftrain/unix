#!/usr/bin/env python3
"""
tr - translate or delete characters
Classic Unix tr implementation in Python
"""

import sys


def print_usage():
    print("Usage: tr [OPTION]... SET1 [SET2]")
    print("Translate, squeeze, and/or delete characters from standard input,")
    print("writing to standard output.")
    print()
    print("Options:")
    print("  -d    delete characters in SET1")
    print("  -s    squeeze multiple occurrences of characters in SET1")


def expand_set(char_set):
    """Expand character set notation like 'a-z' to actual characters."""
    result = []
    i = 0

    while i < len(char_set):
        if i + 2 < len(char_set) and char_set[i + 1] == '-':
            # Range notation
            start = ord(char_set[i])
            end = ord(char_set[i + 2])
            for code in range(start, end + 1):
                result.append(chr(code))
            i += 3
        else:
            result.append(char_set[i])
            i += 1

    return ''.join(result)


def translate_text(set1, set2=None, delete=False, squeeze=False):
    """Translate or delete characters from stdin."""
    set1_expanded = expand_set(set1)
    set2_expanded = expand_set(set2) if set2 else ''

    # Build translation table
    if set2_expanded:
        # Pad set2 if shorter than set1
        if len(set2_expanded) < len(set1_expanded):
            set2_expanded += set2_expanded[-1] * (len(set1_expanded) - len(set2_expanded))

        trans_table = str.maketrans(set1_expanded, set2_expanded[:len(set1_expanded)])
    else:
        trans_table = None

    try:
        text = sys.stdin.read()

        if delete:
            # Delete characters in set1
            for char in set1_expanded:
                text = text.replace(char, '')

        elif trans_table:
            # Translate characters
            text = text.translate(trans_table)

        if squeeze:
            # Squeeze repeated characters in set1 (or set2 if translating)
            squeeze_set = set2_expanded if set2_expanded else set1_expanded
            result = []
            prev_char = None

            for char in text:
                if char in squeeze_set and char == prev_char:
                    continue
                result.append(char)
                prev_char = char

            text = ''.join(result)

        print(text, end='')

    except Exception as e:
        print(f"tr: {e}", file=sys.stderr)
        return 1

    return 0


def main():
    if '--help' in sys.argv or len(sys.argv) < 2:
        print_usage()
        return 0 if '--help' in sys.argv else 1

    # Parse options
    delete = False
    squeeze = False

    args = sys.argv[1:]
    sets = []

    for arg in args:
        if arg.startswith('-') and len(arg) > 1:
            for char in arg[1:]:
                if char == 'd':
                    delete = True
                elif char == 's':
                    squeeze = True
                else:
                    print(f"tr: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'tr --help' for more information.", file=sys.stderr)
                    return 1
        else:
            sets.append(arg)

    if len(sets) < 1:
        print("tr: missing operand", file=sys.stderr)
        return 1

    set1 = sets[0]
    set2 = sets[1] if len(sets) > 1 else None

    if delete and set2:
        print("tr: cannot translate and delete at the same time", file=sys.stderr)
        return 1

    return translate_text(set1, set2, delete, squeeze)


if __name__ == '__main__':
    sys.exit(main())
