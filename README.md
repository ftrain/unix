# Classic Unix Tools in Python

A learning exercise: reimplementing classic Unix command-line tools (circa 1981) in Python.

## Philosophy

Following the Unix philosophy:
- Each tool does one thing well
- Tools work together via standard input/output
- Text streams are the universal interface

## Tools Implemented

### Text Processing
- **grep** - Search for patterns in files using regular expressions
- **wc** - Count lines, words, and characters
- **cat** - Concatenate and display files
- **head** - Display first lines of files
- **tail** - Display last lines of files
- **sort** - Sort lines of text
- **uniq** - Report or filter out repeated lines
- **cut** - Extract columns from text
- **tr** - Translate or delete characters

### File Operations
- **ls** - List directory contents
- **cp** - Copy files and directories
- **mv** - Move or rename files
- **rm** - Remove files and directories
- **mkdir** - Create directories
- **rmdir** - Remove empty directories
- **chmod** - Change file permissions
- **find** - Search for files in directory trees

### Utilities
- **echo** - Display text
- **pwd** - Print working directory
- **tee** - Read from stdin and write to stdout and files
- **diff** - Compare files line by line

### Text Editor (Bonus!)
- **edit** - Simple nano-like terminal text editor with:
  - Arrow key navigation
  - Insert/delete characters and lines
  - Cut and paste lines (Ctrl+K, Ctrl+U)
  - Save file (Ctrl+S)
  - Status line showing filename, position, and modifications
  - Help line with key bindings

## Usage

Each tool is a standalone Python script in the `bin/` directory:

```bash
# Basic usage examples
python3 bin/grep.py "pattern" file.txt
python3 bin/wc.py file.txt
python3 bin/cat.py file1.txt file2.txt
python3 bin/ls.py -la /path/to/dir

# Tools work with pipes
python3 bin/cat.py file.txt | python3 bin/grep.py "search" | python3 bin/wc.py -l

# Get help for any tool
python3 bin/grep.py --help
```

## Making Tools Executable (Optional)

You can make the scripts executable and add them to your PATH:

```bash
chmod +x bin/*.py

# Add to PATH (in ~/.bashrc or ~/.zshrc)
export PATH="/path/to/unix/bin:$PATH"

# Then use without python3 prefix
grep.py "pattern" file.txt
```

## Testing

Sample test files are in the `tests/` directory:

```bash
# Test grep
python3 bin/grep.py "line" tests/sample.txt
python3 bin/grep.py -i "unix" tests/sample.txt
python3 bin/grep.py -n "quick" tests/sample.txt

# Test wc
python3 bin/wc.py tests/sample.txt
python3 bin/wc.py -l tests/sample.txt

# Test sort and uniq
python3 bin/cat.py tests/sample.txt | python3 bin/sort.py | python3 bin/uniq.py

# Test head and tail
python3 bin/head.py -5 tests/sample.txt
python3 bin/tail.py -3 tests/sample.txt

# Test cut
python3 bin/echo.py "one:two:three:four" | python3 bin/cut.py -d : -f 2

# Test tr
python3 bin/echo.py "hello world" | python3 bin/tr.py 'a-z' 'A-Z'
```

## Implementation Notes

- Written in Python 3 for clarity and educational value
- Each tool is self-contained with minimal dependencies
- Standard library only (no external packages, except curses for editor)
- **Professional CLI using argparse** - automatic help, validation, long options
- Basic error handling and edge cases covered
- Simplified versions - not all features of the original Unix tools
- Text editor uses Python's curses library for terminal UI

## What's Not Included

This is a learning exercise focusing on 1981-era Unix tools:
- No shell implementation
- No system administration tools
- No network tools (they came later)
- No advanced features from modern versions

Note: We added a simple text editor as a bonus!

## Learning Value

Building these tools teaches:
- File I/O and text processing
- Regular expressions
- Command-line argument parsing
- Unix philosophy and design patterns
- Working with standard input/output/error
- File system operations
- Process exit codes

## License

Educational/learning purposes. Feel free to study, modify, and learn from this code.
