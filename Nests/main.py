import argparse
from wf_nests import main_processing

def main():
    parser = argparse.ArgumentParser(description="Working with word-formation nests")
    parser.add_argument("in_file", type=str, help="Initial data with nests")
    args = parser.parse_args()
    with open(args.in_file, "r") as in_file:
        data = in_file.readlines()
        main_processing(data)

if __name__ == '__main__':
    main()
