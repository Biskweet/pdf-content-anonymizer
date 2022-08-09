import os
import sys

from scriptsrc import anonymizer


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Not enough arguments.")

    function = sys.argv[1]
    path = sys.argv[2]

    if not os.path.isdir(path) and not os.path.isfile(path):
        raise SystemExit("Not a valid path.")

    anonymizer.process_all_files(function, path)
