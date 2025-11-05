#!/usr/bin/env python3
"""
diff - compare files line by line
Classic Unix diff implementation in Python
"""

import sys
import argparse


def print_usage():
    print("Usage: diff [OPTION]... FILE1 FILE2")
    print("Compare files line by line.")
    print()
    print("Options:")
    print("  -q    report only when files differ")
    print("  -s    report when files are identical")
    print("  -b    ignore changes in amount of white space")
    print("  -i    ignore case differences")


def normalize_line(line, ignore_space=False, ignore_case=False):
    """Normalize a line for comparison."""
    if ignore_case:
        line = line.lower()
    if ignore_space:
        line = ' '.join(line.split())
    return line


def simple_diff(file1, file2, brief=False, report_identical=False,
                ignore_space=False, ignore_case=False):
    """Perform a simple line-by-line diff."""
    try:
        with open(file1, 'r') as f1:
            lines1 = f1.readlines()

        with open(file2, 'r') as f2:
            lines2 = f2.readlines()

    except FileNotFoundError as e:
        print(f"diff: {e}", file=sys.stderr)
        return 2
    except PermissionError as e:
        print(f"diff: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"diff: {e}", file=sys.stderr)
        return 2

    # Normalize lines for comparison
    norm_lines1 = [normalize_line(line.rstrip('\n'), ignore_space, ignore_case)
                   for line in lines1]
    norm_lines2 = [normalize_line(line.rstrip('\n'), ignore_space, ignore_case)
                   for line in lines2]

    # Check if files are identical
    if norm_lines1 == norm_lines2:
        if report_identical:
            print(f"Files {file1} and {file2} are identical")
        return 0

    # Files differ
    if brief:
        print(f"Files {file1} and {file2} differ")
        return 1

    # Simple diff output (not the most sophisticated algorithm, but functional)
    i = 0
    j = 0

    while i < len(lines1) or j < len(lines2):
        # Find matching sections
        if i < len(lines1) and j < len(lines2) and norm_lines1[i] == norm_lines2[j]:
            i += 1
            j += 1
            continue

        # Find where they sync up again
        sync_i = i
        sync_j = j
        found_sync = False

        # Look ahead for matching lines
        for look_i in range(i, min(i + 10, len(lines1))):
            for look_j in range(j, min(j + 10, len(lines2))):
                if norm_lines1[look_i] == norm_lines2[look_j]:
                    sync_i = look_i
                    sync_j = look_j
                    found_sync = True
                    break
            if found_sync:
                break

        if not found_sync:
            sync_i = len(lines1)
            sync_j = len(lines2)

        # Output the difference
        if i < sync_i and j < sync_j:
            # Changed lines
            print(f"{i+1},{sync_i}c{j+1},{sync_j}")
            for k in range(i, sync_i):
                print(f"< {lines1[k]}", end='')
            print("---")
            for k in range(j, sync_j):
                print(f"> {lines2[k]}", end='')
        elif i < sync_i:
            # Deleted lines
            print(f"{i+1},{sync_i}d{j}")
            for k in range(i, sync_i):
                print(f"< {lines1[k]}", end='')
        elif j < sync_j:
            # Added lines
            print(f"{i}a{j+1},{sync_j}")
            for k in range(j, sync_j):
                print(f"> {lines2[k]}", end='')

        i = sync_i
        j = sync_j

    return 1


def main():
    if '--help' in sys.argv or len(sys.argv) < 3:
        print_usage()
        return 0 if '--help' in sys.argv else 1

    # Parse options
    brief = False
    report_identical = False
    ignore_space = False
    ignore_case = False

    args = sys.argv[1:]
    files = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'q':
                    brief = True
                elif char == 's':
                    report_identical = True
                elif char == 'b':
                    ignore_space = True
                elif char == 'i':
                    ignore_case = True
                else:
                    print(f"diff: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'diff --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

    if len(files) != 2:
        print("diff: missing operand", file=sys.stderr)
        print("Try 'diff --help' for more information.", file=sys.stderr)
        return 1

    return simple_diff(files[0], files[1], brief, report_identical,
                      ignore_space, ignore_case)


if __name__ == '__main__':
    sys.exit(main())
