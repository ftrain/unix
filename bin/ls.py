#!/usr/bin/env python3
"""
ls - list directory contents
Classic Unix ls implementation in Python
"""

import sys
import os
import stat
import time
import pwd
import grp


def print_usage():
    print("Usage: ls [OPTION]... [FILE]...")
    print("List information about the FILEs (the current directory by default).")
    print()
    print("Options:")
    print("  -a    do not ignore entries starting with .")
    print("  -l    use a long listing format")
    print("  -t    sort by modification time, newest first")
    print("  -r    reverse order while sorting")
    print("  -R    list subdirectories recursively")
    print("  -d    list directories themselves, not their contents")


def format_permissions(mode):
    """Convert file mode to rwxrwxrwx format."""
    perms = []

    # File type
    if stat.S_ISDIR(mode):
        perms.append('d')
    elif stat.S_ISLNK(mode):
        perms.append('l')
    else:
        perms.append('-')

    # Owner permissions
    perms.append('r' if mode & stat.S_IRUSR else '-')
    perms.append('w' if mode & stat.S_IWUSR else '-')
    perms.append('x' if mode & stat.S_IXUSR else '-')

    # Group permissions
    perms.append('r' if mode & stat.S_IRGRP else '-')
    perms.append('w' if mode & stat.S_IWGRP else '-')
    perms.append('x' if mode & stat.S_IXGRP else '-')

    # Other permissions
    perms.append('r' if mode & stat.S_IROTH else '-')
    perms.append('w' if mode & stat.S_IWOTH else '-')
    perms.append('x' if mode & stat.S_IXOTH else '-')

    return ''.join(perms)


def format_long_listing(filepath, filename):
    """Format a file entry in long listing format."""
    try:
        file_stat = os.lstat(filepath)

        # Permissions
        perms = format_permissions(file_stat.st_mode)

        # Number of links
        nlinks = file_stat.st_nlink

        # Owner and group
        try:
            owner = pwd.getpwuid(file_stat.st_uid).pw_name
        except (KeyError, AttributeError):
            owner = str(file_stat.st_uid)

        try:
            group = grp.getgrgid(file_stat.st_gid).gr_name
        except (KeyError, AttributeError):
            group = str(file_stat.st_gid)

        # Size
        size = file_stat.st_size

        # Modification time
        mtime = time.strftime('%b %d %H:%M',
                             time.localtime(file_stat.st_mtime))

        return f"{perms} {nlinks:3} {owner:8} {group:8} {size:8} {mtime} {filename}"

    except Exception as e:
        return f"? ? ? ? ? ? {filename}"


def list_directory(path, show_all=False, long_format=False,
                  sort_time=False, reverse=False, recursive=False,
                  list_dir=False):
    """List contents of a directory."""
    try:
        if list_dir:
            # List the directory itself, not its contents
            if long_format:
                print(format_long_listing(path, path))
            else:
                print(path)
            return

        entries = os.listdir(path)

        # Filter hidden files
        if not show_all:
            entries = [e for e in entries if not e.startswith('.')]

        # Get full paths and stat info for sorting
        entry_info = []
        for entry in entries:
            full_path = os.path.join(path, entry)
            try:
                st = os.lstat(full_path)
                entry_info.append((entry, full_path, st))
            except:
                entry_info.append((entry, full_path, None))

        # Sort
        if sort_time:
            entry_info.sort(key=lambda x: x[2].st_mtime if x[2] else 0, reverse=True)
        else:
            entry_info.sort(key=lambda x: x[0])

        if reverse and not sort_time:
            entry_info.reverse()
        elif reverse and sort_time:
            entry_info.reverse()

        # Print entries
        if long_format:
            for entry, full_path, st in entry_info:
                print(format_long_listing(full_path, entry))
        else:
            for entry, full_path, st in entry_info:
                print(entry)

        # Recursive listing
        if recursive:
            for entry, full_path, st in entry_info:
                if st and stat.S_ISDIR(st.st_mode):
                    print(f"\n{full_path}:")
                    list_directory(full_path, show_all, long_format,
                                 sort_time, reverse, recursive, list_dir)

    except PermissionError:
        print(f"ls: cannot open directory '{path}': Permission denied", file=sys.stderr)
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory", file=sys.stderr)
    except Exception as e:
        print(f"ls: {path}: {e}", file=sys.stderr)


def main():
    if '--help' in sys.argv:
        print_usage()
        return 0

    # Parse options
    show_all = False
    long_format = False
    sort_time = False
    reverse = False
    recursive = False
    list_dir = False

    args = sys.argv[1:]
    paths = []

    for arg in args:
        if arg.startswith('-') and arg != '-':
            for char in arg[1:]:
                if char == 'a':
                    show_all = True
                elif char == 'l':
                    long_format = True
                elif char == 't':
                    sort_time = True
                elif char == 'r':
                    reverse = True
                elif char == 'R':
                    recursive = True
                elif char == 'd':
                    list_dir = True
                else:
                    print(f"ls: invalid option -- '{char}'", file=sys.stderr)
                    print("Try 'ls --help' for more information.", file=sys.stderr)
                    return 1
        else:
            paths.append(arg)

    # If no paths specified, use current directory
    if not paths:
        paths = ['.']

    # List each path
    for i, path in enumerate(paths):
        if len(paths) > 1 and not list_dir:
            if i > 0:
                print()
            print(f"{path}:")

        if os.path.isdir(path) and not list_dir:
            list_directory(path, show_all, long_format, sort_time,
                         reverse, recursive, list_dir)
        else:
            # It's a file or we want to list the directory itself
            if long_format:
                print(format_long_listing(path, os.path.basename(path) if not list_dir else path))
            else:
                print(path)

    return 0


if __name__ == '__main__':
    sys.exit(main())
