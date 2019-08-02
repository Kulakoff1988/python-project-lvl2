import argparse
from gendiff import engine


def run():
    parser = argparse.ArgumentParser(description="Generate diff")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")
    parser.parse_args()
    args = parser.parse_args()
    engine.get_diff(args.first_file, args.second_file, args.format)
