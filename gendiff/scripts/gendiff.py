#!/usr/bin/env python3

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
  main()