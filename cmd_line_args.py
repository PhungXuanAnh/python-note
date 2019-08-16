import argparse


def parse_cmdline():
    parser = argparse.ArgumentParser(
        description="Sample parser command line argument in python")

    parser.add_argument('-d', '--directory',
                        metavar='DIRECTORY',
                        dest='dir',
                        help='Enter a directory path',
                        required=True)

    parser.add_argument('-f', '--file',
                        metavar='FILE',
                        dest='file',
                        help='Enter a file path',
                        required=True,
                        type=str)

    parser.add_argument('-n', '--number',
                        metavar='NUMBER',
                        dest='number',
                        help='Enter a number',
                        required=True,
                        type=int)

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_cmdline()

    print(args.dir)

    print(args.file)

    print(args.number)
