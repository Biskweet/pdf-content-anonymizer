import os
import sys

from src import anonymizer


if __name__ == "__main__":
    if len(sys.argv) > 2:
        path = sys.argv[2]

        if not os.path.isdir(path):
            raise SystemExit("Not a valid directoy.")

        if path[-1] != '/':
            path += '/'

    else:
        path = "sensitive-pdfs"

    anonymizer.process_all_files(path)

