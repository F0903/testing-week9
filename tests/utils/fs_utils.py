import errno
import os

TEMP_DIR = "./temp/"


def check_dir_for_filetypes(dest_dir: str, extension: str) -> int:
    """
    Counts how many files with the spcified extension is in the specified directory, and returns the result.
    """

    count = 0
    for entry in os.listdir(dest_dir):
        _, ext = os.path.splitext(entry)

        if ext == extension:
            count += 1

    return count


def remove_if_exists(filename: str):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
