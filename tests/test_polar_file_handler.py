import pathlib
from queue import Queue
from src.polar_file_handler import PolarFileHandler
from .utils.http_file_server import TestHTTPServer


def test_download_thread():
    file_handler = PolarFileHandler()

    # Creates a dictionary of downloads
    finished_dict = {"BRnum": [], "pdf_downloaded": []}

    queue = Queue()

    NUM_TEST_TASKS = 3

    for i in range(0, NUM_TEST_TASKS):
        queue.put(["http://localhost:8000/pdf", f"temp/", str(i), None, finished_dict])

    with TestHTTPServer():
        for i in range(0, NUM_TEST_TASKS):
            file_handler.download_thread(i, queue)

    for i in range(0, NUM_TEST_TASKS):
        id = finished_dict["BRnum"][i]
        is_downloaded = finished_dict["pdf_downloaded"][i]

        queue_item = queue[i]
        dest_dir = queue_item[1]
        dest_name = queue_item[2]

        file_path = pathlib.Path(queue_item)

        assert is_downloaded and file_path.exists()


def test_start_download():
    pass
