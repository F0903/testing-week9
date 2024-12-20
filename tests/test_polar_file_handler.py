import pathlib
from queue import Queue
import shutil
from src.polar_file_handler import PolarFileHandler
from .utils.fs_utils import check_dir_for_filetypes, TEMP_DIR
from .utils.testing_http_server import TestingHTTPServer


def test_download_thread():
    file_handler = PolarFileHandler()

    # "Creates a dictionary of downloads"
    finished_dict = {"BRnum": [], "pdf_downloaded": []}

    # It's a bit difficult to get items of out the queue when all tasks are done, so keep track of them here.
    original_queue_items = []
    queue = Queue()

    NUM_TEST_TASKS = 3

    # Queue up the items for download
    for i in range(0, NUM_TEST_TASKS):
        item = [i, "http://localhost:8000/pdf", TEMP_DIR, str(i), None, finished_dict]
        queue.put(item)
        original_queue_items.append(item)

    # Spin up the testing server and start the download
    with TestingHTTPServer():
        file_handler.download_thread(queue)

    # Assert download results
    for i in range(0, NUM_TEST_TASKS):
        id = finished_dict["BRnum"][i]
        is_downloaded = finished_dict["pdf_downloaded"][i] == "yes"

        queue_item = original_queue_items[i]

        # Not exactly elegant, but sort of required with this codebase
        ITEM_DIR_INDEX = 2
        ITEM_NAME_INDEX = 3

        dest_dir = pathlib.Path(queue_item[ITEM_DIR_INDEX])
        dest_name = queue_item[ITEM_NAME_INDEX]
        full_dest = dest_dir.joinpath(dest_name + ".pdf")

        # Since we are using a local mock server, the download needs to succeed
        assert is_downloaded
        assert full_dest.exists()


def test_start_download():
    file_handler = PolarFileHandler(timeout=5)

    # Setup destination directory and remove it if it already exists
    dest_dir = pathlib.Path(f"{TEMP_DIR}test_start_download/")
    shutil.rmtree(dest_dir, True)

    with TestingHTTPServer():
        file_handler.start_download(
            "resources/testing/testing_dataset.xlsx",
            f"{TEMP_DIR}test_start_download/test_metadata.xlsx",
            dest_dir,
        )

    # Just do a basic test to see if at least 1 pdf file is present.
    pdf_count = check_dir_for_filetypes(dest_dir, ".pdf")
    assert pdf_count > 0


def test_start_download_existing_metadata():
    file_handler = PolarFileHandler(timeout=5)

    # Setup destination directory and remove it if it already exists
    dest_dir = pathlib.Path(f"{TEMP_DIR}test_start_download/")
    shutil.rmtree(dest_dir, True)

    with TestingHTTPServer():
        file_handler.start_download(
            "resources/testing/testing_dataset.xlsx",
            "resources/testing/testing_metadata.xlsx",
            dest_dir,
            write_metadata=False,
        )

    # Just do a basic test to see if at least 1 pdf file is present.
    pdf_count = check_dir_for_filetypes(dest_dir, ".pdf")
    assert pdf_count > 0
