import argparse
from wf_software_support import main_processing

def main():
    parser = argparse.ArgumentParser(description="Word-formation software support")
    parser.add_argument("in_file", type=str, help="Initial data")
    parser.add_argument("out_file", type=str,
                        help="File with word-formation nests")
    args = parser.parse_args()
    with open(args.in_file, "r") as in_file:
        with open(args.out_file, "w") as out_file:
            data = in_file.readlines()
            main_processing(data, out_file)

if __name__ == '__main__':
    main()
