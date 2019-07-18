#!/usr/bin/env python3
"""usage: gendiff [-h] [-f FORMAT] first_file second_file

Generate diff

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        set format of output"""

# from docopt import docopt
import argparse
from gendiff.comparison import comparator

def main():
  parser = argparse.ArgumentParser(description="Generate diff")
  parser.add_argument("first_file")
  parser.add_argument("second_file")
  parser.add_argument("-f", "--format", help="set format of output")
  parser.parse_args()
  args = parser.parse_args()
  comparator.get_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    # arguments = docopt(__doc__)
    # print(arguments)
    main()
