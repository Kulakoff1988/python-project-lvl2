import argparse
from gendiff import engine


arg_parser = argparse.ArgumentParser(description="Generate diff")
arg_parser.add_argument("old_file")
arg_parser.add_argument("new_file")
arg_parser.add_argument("-f", "--format", help="set format of output")


def run(args):
    engine.get_diff(args.old_file, args.new_file, args.format)
