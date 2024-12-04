import os


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
