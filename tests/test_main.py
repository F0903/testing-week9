import shutil
import pathlib
import sys
from src.main import main
import pytest
from .utils.testing_http_server import TestingHTTPServer
from .utils.fs_utils import check_dir_for_filetypes


def test_main():
    with pytest.MonkeyPatch().context() as mp:
        # Setup destination directory and remove it if it already exists
        dest_dir = pathlib.Path("temp/test_main/")
        shutil.rmtree(dest_dir, True)

        # Set command line arguments to test with.
        mp.setattr(
            sys,
            "argv",
            [
                sys.argv[0],
                "-uf",
                "resources/testing/testing_dataset.xlsx",
                "-rf",
                "temp/test_main/test_metadata.xlsx",
                "-d",
                str(dest_dir),
                "-t",
                "4",
            ],
        )

        with TestingHTTPServer():
            main()

        # Just do a basic test to see if at least 1 pdf file is present.
        pdf_count = check_dir_for_filetypes(dest_dir, ".pdf")
        assert pdf_count > 0


def test_main_invalid_thread_arg():
    with pytest.MonkeyPatch().context() as mp:
        # Make sure main raises ValueError on the invalid thread arg.
        with pytest.raises(ValueError):
            # Set command line arguments to test with.
            mp.setattr(
                sys,
                "argv",
                [
                    sys.argv[0],
                    "-t",
                    "this aint a number",
                ],
            )

            main()
