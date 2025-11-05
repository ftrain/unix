#!/usr/bin/env python3
"""
wc - word, line, character, and byte count
Classic Unix wc implementation in Python
"""

import sys


def print_usage():
    print("Usage: wc [OPTION]... [FILE]...")
    print("Print newline, word, and byte counts for each FILE.")
    print()
    print("Options:")
    print("  -l    print the newline counts")
    print("  -w    print the word counts")
    print("  -c    print the byte counts")
    print("  -m    print the character counts")


def count_file(filename, show_lines=True, show_words=True,
               show_chars=True, show_bytes=False):
    """
    Count lines, words, and characters in a file.
    Returns tuple: (lines, words, chars, bytes)
    """
    try:
        if filename == '-':
            f = sys.stdin
            content = f.read()
        else:
            with open(filename, 'rb') as f:
                content_bytes = f.read()
                byte_count = len(content_bytes)
                content = content_bytes.decode('utf-8', errors='replace')

        lines = content.count('\n')
        words = len(content.split())
        chars = len(content)

        if filename == '-':
            byte_count = len(content.encode('utf-8'))

        return (lines, words, chars, byte_count)

    except FileNotFoundError:
        print(f"wc: {filename}: No such file or directory", file=sys.stderr)
        return None
    except PermissionError:
        print(f"wc: {filename}: Permission denied", file=sys.stderr)
        return None
    except Exception as e:
        print(f"wc: {filename}: {e}", file=sys.stderr)
        return None


def format_output(lines, words, chars, bytes_count, filename,
                  show_lines, show_words, show_chars, show_bytes):
    """Format the output line for wc."""
    output = []

    if show_lines:
        output.append(f"{lines:8}")
    if show_words:
        output.append(f"{words:8}")
    if show_chars:
        output.append(f"{chars:8}")
    if show_bytes and not show_chars:  # Don't show both chars and bytes
        output.append(f"{bytes_count:8}")

    if filename and filename != '-':
        output.append(f" {filename}")

    return ''.join(output)


def main():
    # Parse options
    show_lines = False
    show_words = False
    show_chars = False
    show_bytes = False

    args = sys.argv[1:]
    files = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '--help':
            print_usage()
            return 0
        elif arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'l':
                    show_lines = True
                elif char == 'w':
                    show_words = True
                elif char == 'c':
                    show_bytes = True
                elif char == 'm':
                    show_chars = True
                else:
                    print(f"wc: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'wc --help' for more information.", file=sys.stderr)
                    return 1
        else:
            files.append(arg)

        i += 1

    # If no options specified, show all (default behavior)
    if not (show_lines or show_words or show_chars or show_bytes):
        show_lines = True
        show_words = True
        show_chars = True

    # If no files specified, read from stdin
    if not files:
        files = ['-']

    # Process files
    total_lines = 0
    total_words = 0
    total_chars = 0
    total_bytes = 0
    successful_files = 0

    for filename in files:
        result = count_file(filename, show_lines, show_words,
                          show_chars, show_bytes)

        if result is None:
            continue

        lines, words, chars, bytes_count = result
        successful_files += 1

        total_lines += lines
        total_words += words
        total_chars += chars
        total_bytes += bytes_count

        print(format_output(lines, words, chars, bytes_count,
                          filename, show_lines, show_words,
                          show_chars, show_bytes))

    # Print totals if multiple files
    if len(files) > 1 and successful_files > 1:
        print(format_output(total_lines, total_words, total_chars,
                          total_bytes, "total", show_lines,
                          show_words, show_chars, show_bytes))

    return 0


if __name__ == '__main__':
    sys.exit(main())
