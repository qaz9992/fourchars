"""
python . [arguments]
"""

from main import *
from sys import exit, argv

if __name__ == "__main__":
    exit(main(argv, len(argv)))