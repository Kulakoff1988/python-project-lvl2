#!/usr/bin/env python3

from gendiff import cli


def main():
    cli.run(cli.arg_parser.parse_args())


if __name__ == "__main__":
    main()
