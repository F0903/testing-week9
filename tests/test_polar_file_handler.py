import pathlib
from queue import Queue
from src.polar_file_handler import PolarFileHandler
from .utils.http_file_server import TestHTTPServer


def test_download_thread():
    file_handler = PolarFileHandler()

    # Creates a dictionary of downloads
    finished_dict = {"BRnum": [], "pdf_downloaded": []}

    original_queue_items = []
    queue = Queue()

    NUM_TEST_TASKS = 3

    for i in range(0, NUM_TEST_TASKS):
        item = [i, "http://localhost:8000/pdf", f"temp/", str(i), None, finished_dict]
        queue.put(item)
        original_queue_items.append(item)

    with TestHTTPServer():
        file_handler.download_thread(queue)

    for i in range(0, NUM_TEST_TASKS):
        id = finished_dict["BRnum"][i]
        is_downloaded = finished_dict["pdf_downloaded"][i] == "yes"

        queue_item = original_queue_items[i]

        # Not exactly elegant, but sort of required with this codebase.
        ITEM_DIR_INDEX = 2
        ITEM_NAME_INDEX = 3

        dest_dir = pathlib.Path(queue_item[ITEM_DIR_INDEX])
        dest_name = queue_item[ITEM_NAME_INDEX]
        full_dest = dest_dir.joinpath(dest_name + ".pdf")

        assert is_downloaded and full_dest.exists()


def test_start_download():
    file_handler = PolarFileHandler(timeout=5)

    # Just run the downloader. The most essential parts are tested in test_download_thread.
    file_handler.start_download(
        "customer_data/GRI_2017_2020.xlsx",
        "customer_data/Metadata2017_2020.xlsx",
        "temp/",
    )
