import os
import pathlib
from src.downloader import Downloader
from .utils.testing_http_server import TestingHTTPServer

TEMP_DIR = "./temp/"


# Consider looking into monkey patching instead of the HTTP server
def test_downloader():
    downloader = Downloader()

    base_dir = pathlib.Path(TEMP_DIR)
    base_dir.mkdir(exist_ok=True)

    file_dest_path = base_dir.joinpath("test_downloader_file.pdf")
    if file_dest_path.exists():
        # Remove old if exists
        os.remove(file_dest_path)

    with TestingHTTPServer():
        success = downloader.download("http://localhost:8000/pdf", file_dest_path)
        assert success
        assert file_dest_path.exists()


def test_downloader_failure():
    downloader = Downloader()

    base_dir = pathlib.Path(TEMP_DIR)
    base_dir.mkdir(exist_ok=True)

    file_dest_path = base_dir.joinpath("test_downloader_file.pdf")
    if file_dest_path.exists():
        # Remove old if exists
        os.remove(file_dest_path)

    with TestingHTTPServer():
        success = downloader.download("http://localhost:8000/deny", file_dest_path)
        assert not success
        assert not file_dest_path.exists()
