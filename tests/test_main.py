import shutil
import pathlib
import sys
from src.main import main
from pytest import MonkeyPatch
from .utils.testing_http_server import TestingHTTPServer
from .utils.fs_utils import check_dir_for_filetypes


def test_main():
    with MonkeyPatch().context() as mp:
        dest_dir = pathlib.Path("temp/test_main/")

        # Delete these things if they already exist so it actually downloads stuff
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
    with MonkeyPatch().context() as mp:
        threw = False
        try:
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
                    "temp/test_main/",
                    "-t",
                    "this aint a number",
                ],
            )

            main()

        except Exception:
            threw = True

        assert threw
