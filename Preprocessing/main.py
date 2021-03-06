import argparse
from preprocessing import main_processing

def main():
    parser = argparse.ArgumentParser(description=
                                     "Removing plural words and separating groups")
    parser.add_argument("in_file", type=str, help="Initial data")
    parser.add_argument("out_file", type=str,
                        help="File with groups")
    args = parser.parse_args()
    with open(args.in_file, "r") as in_file:
        with open(args.out_file, "w") as out_file:
            data = in_file.readlines()
            main_processing(data, out_file)

if __name__ == '__main__':
    main()
