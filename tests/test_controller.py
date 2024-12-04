import pathlib
import shutil
import pytest
from src.controller import Controller
from .utils.check_dir import check_dir_for_filetypes
from .utils.testing_http_server import TestingHTTPServer


def test_set_url_file():
    controller = Controller()

    TEST_NAME = "test"
    controller.set_url_file(TEST_NAME)

    assert controller.url_file_name == TEST_NAME


def test_set_report_file():
    controller = Controller()

    TEST_NAME = "test"
    controller.set_report_file(TEST_NAME)

    assert controller.report_file_name == TEST_NAME


def test_set_destination():
    controller = Controller()

    TEST_NAME = "test"
    controller.set_destination(TEST_NAME)

    assert controller.destination == TEST_NAME


def test_run():
    controller = Controller()
    with pytest.MonkeyPatch().context() as mp:
        dest_dir = pathlib.Path("temp/test_controller/")

        # Delete these things if they already exist so it actually downloads stuff
        shutil.rmtree(dest_dir, True)

        mp.setattr(
            controller, "url_file_name", "resources/testing/testing_dataset.xlsx"
        )
        mp.setattr(
            controller, "report_file_name", "temp/test_controller/test_metadata.xlsx"
        )
        mp.setattr(controller, "destination", dest_dir)

        with TestingHTTPServer():
            controller.run()

        # Just do a basic test to see if at least 1 pdf file is present.
        pdf_count = check_dir_for_filetypes(dest_dir, ".pdf")
        assert pdf_count > 0
