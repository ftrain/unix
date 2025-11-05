#!/usr/bin/env python3
"""
edit - simple terminal text editor
A nano-like editor for basic text editing
"""

import sys
import curses
import argparse
from pathlib import Path


class TextEditor:
    def __init__(self, stdscr, filename=None):
        self.stdscr = stdscr
        self.filename = filename
        self.lines = []
        self.cursor_y = 0
        self.cursor_x = 0
        self.offset_y = 0
        self.modified = False

        # Load file if specified
        if filename and Path(filename).exists():
            with open(filename, 'r') as f:
                self.lines = [line.rstrip('\n') for line in f.readlines()]

        if not self.lines:
            self.lines = ['']

        # Setup curses
        curses.curs_set(1)
        self.stdscr.keypad(True)
        self.height, self.width = stdscr.getmaxyx()

    def draw_status_line(self):
        """Draw the status line at the bottom."""
        status_y = self.height - 2

        # File info
        filename = self.filename or "[New File]"
        modified = " [Modified]" if self.modified else ""
        pos = f"Ln {self.cursor_y + 1}, Col {self.cursor_x + 1}"

        status = f" {filename}{modified}"
        status = status[:self.width - len(pos) - 1]
        status = status.ljust(self.width - len(pos) - 1) + pos

        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(status_y, 0, status[:self.width - 1])
        self.stdscr.attroff(curses.A_REVERSE)

    def draw_help_line(self):
        """Draw the help line at the bottom."""
        help_y = self.height - 1
        help_text = "^X Exit  ^S Save  ^K Cut Line  ^U Paste  Arrow Keys Move"

        self.stdscr.addstr(help_y, 0, help_text[:self.width - 1])

    def draw_content(self):
        """Draw the file content."""
        for i in range(self.height - 2):
            line_num = self.offset_y + i
            if line_num < len(self.lines):
                line = self.lines[line_num]
                self.stdscr.addstr(i, 0, line[:self.width - 1])
            self.stdscr.clrtoeol()

    def refresh(self):
        """Refresh the entire screen."""
        self.stdscr.clear()
        self.draw_content()
        self.draw_status_line()
        self.draw_help_line()

        # Position cursor
        screen_y = self.cursor_y - self.offset_y
        self.stdscr.move(screen_y, self.cursor_x)
        self.stdscr.refresh()

    def move_cursor(self, dy, dx):
        """Move cursor by delta."""
        # Update y position
        new_y = max(0, min(len(self.lines) - 1, self.cursor_y + dy))
        self.cursor_y = new_y

        # Update x position
        max_x = len(self.lines[self.cursor_y])
        self.cursor_x = max(0, min(max_x, self.cursor_x + dx))

        # Adjust scroll offset
        if self.cursor_y < self.offset_y:
            self.offset_y = self.cursor_y
        elif self.cursor_y >= self.offset_y + (self.height - 2):
            self.offset_y = self.cursor_y - (self.height - 3)

    def insert_char(self, ch):
        """Insert a character at cursor position."""
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[:self.cursor_x] + ch + line[self.cursor_x:]
        self.cursor_x += 1
        self.modified = True

    def delete_char(self):
        """Delete character before cursor (backspace)."""
        if self.cursor_x > 0:
            line = self.lines[self.cursor_y]
            self.lines[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
            self.cursor_x -= 1
            self.modified = True
        elif self.cursor_y > 0:
            # Join with previous line
            prev_line = self.lines[self.cursor_y - 1]
            curr_line = self.lines[self.cursor_y]
            self.lines[self.cursor_y - 1] = prev_line + curr_line
            del self.lines[self.cursor_y]
            self.cursor_y -= 1
            self.cursor_x = len(prev_line)
            self.modified = True

    def delete_forward(self):
        """Delete character at cursor (delete key)."""
        line = self.lines[self.cursor_y]
        if self.cursor_x < len(line):
            self.lines[self.cursor_y] = line[:self.cursor_x] + line[self.cursor_x + 1:]
            self.modified = True
        elif self.cursor_y < len(self.lines) - 1:
            # Join with next line
            curr_line = self.lines[self.cursor_y]
            next_line = self.lines[self.cursor_y + 1]
            self.lines[self.cursor_y] = curr_line + next_line
            del self.lines[self.cursor_y + 1]
            self.modified = True

    def insert_newline(self):
        """Insert a newline at cursor position."""
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[:self.cursor_x]
        self.lines.insert(self.cursor_y + 1, line[self.cursor_x:])
        self.cursor_y += 1
        self.cursor_x = 0
        self.modified = True

    def cut_line(self):
        """Cut the current line."""
        if hasattr(self, 'clipboard'):
            self.clipboard = self.lines[self.cursor_y]
        else:
            self.clipboard = self.lines[self.cursor_y]

        if len(self.lines) > 1:
            del self.lines[self.cursor_y]
            if self.cursor_y >= len(self.lines):
                self.cursor_y = len(self.lines) - 1
        else:
            self.lines[0] = ''
        self.cursor_x = 0
        self.modified = True

    def paste_line(self):
        """Paste the cut line."""
        if hasattr(self, 'clipboard'):
            self.lines.insert(self.cursor_y + 1, self.clipboard)
            self.cursor_y += 1
            self.cursor_x = 0
            self.modified = True

    def save_file(self):
        """Save the file."""
        if not self.filename:
            # Prompt for filename
            self.stdscr.addstr(self.height - 1, 0, "File Name: ")
            self.stdscr.clrtoeol()
            self.stdscr.refresh()

            curses.echo()
            filename = self.stdscr.getstr(self.height - 1, 11, 60).decode('utf-8')
            curses.noecho()

            if filename:
                self.filename = filename
            else:
                return False

        try:
            with open(self.filename, 'w') as f:
                for line in self.lines:
                    f.write(line + '\n')
            self.modified = False

            # Show save message
            self.stdscr.addstr(self.height - 1, 0, f"[ Wrote {len(self.lines)} lines ]")
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            curses.napms(1000)
            return True
        except Exception as e:
            self.stdscr.addstr(self.height - 1, 0, f"[ Error: {str(e)} ]")
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            curses.napms(2000)
            return False

    def run(self):
        """Main editor loop."""
        self.refresh()

        while True:
            try:
                ch = self.stdscr.getch()

                # Exit (Ctrl+X)
                if ch == 24:  # Ctrl+X
                    if self.modified:
                        self.stdscr.addstr(self.height - 1, 0, "Save modified buffer? (y/n) ")
                        self.stdscr.clrtoeol()
                        self.stdscr.refresh()
                        response = self.stdscr.getch()
                        if response in (ord('y'), ord('Y')):
                            if not self.save_file():
                                continue
                    break

                # Save (Ctrl+S)
                elif ch == 19:  # Ctrl+S
                    self.save_file()

                # Cut line (Ctrl+K)
                elif ch == 11:  # Ctrl+K
                    self.cut_line()

                # Paste (Ctrl+U)
                elif ch == 21:  # Ctrl+U
                    self.paste_line()

                # Navigation
                elif ch == curses.KEY_UP:
                    self.move_cursor(-1, 0)
                elif ch == curses.KEY_DOWN:
                    self.move_cursor(1, 0)
                elif ch == curses.KEY_LEFT:
                    if self.cursor_x > 0:
                        self.move_cursor(0, -1)
                    elif self.cursor_y > 0:
                        self.cursor_y -= 1
                        self.cursor_x = len(self.lines[self.cursor_y])
                elif ch == curses.KEY_RIGHT:
                    if self.cursor_x < len(self.lines[self.cursor_y]):
                        self.move_cursor(0, 1)
                    elif self.cursor_y < len(self.lines) - 1:
                        self.cursor_y += 1
                        self.cursor_x = 0
                elif ch == curses.KEY_HOME:
                    self.cursor_x = 0
                elif ch == curses.KEY_END:
                    self.cursor_x = len(self.lines[self.cursor_y])

                # Editing
                elif ch == 10 or ch == 13:  # Enter
                    self.insert_newline()
                elif ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8:
                    self.delete_char()
                elif ch == curses.KEY_DC:  # Delete
                    self.delete_forward()
                elif ch == 9:  # Tab
                    self.insert_char('    ')
                elif 32 <= ch <= 126:  # Printable characters
                    self.insert_char(chr(ch))

                self.refresh()

            except KeyboardInterrupt:
                break


def main():
    parser = argparse.ArgumentParser(
        description='Simple terminal text editor (nano-like)'
    )

    parser.add_argument('filename', nargs='?', help='file to edit')

    args = parser.parse_args()

    def editor_wrapper(stdscr):
        editor = TextEditor(stdscr, args.filename)
        editor.run()

    try:
        curses.wrapper(editor_wrapper)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
