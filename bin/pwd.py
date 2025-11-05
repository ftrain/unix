#!/usr/bin/env python3
"""
pwd - print name of current/working directory
Classic Unix pwd implementation in Python
"""

import sys
import os


def main():
    print(os.getcwd())
    return 0


if __name__ == '__main__':
    sys.exit(main())
