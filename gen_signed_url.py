from main import get_bucket, gen_signed_url
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate Signed Url')
    parser.add_argument('-f', '--file')
    parser.add_argument('-n', '--name')
    return parser, parser.parse_args()


def main():
    parser, arguments = parse_arguments()
    filepath = arguments.file
    objname = arguments.name
    if filepath:
        with open(filepath) as lines:
            key = lines.readlines()[0]
        bucket = get_bucket()
        gen_signed_url(bucket, key, filepath=filepath)
    elif objname:
        bucket = get_bucket()
        gen_signed_url(bucket, objname)
    else:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
