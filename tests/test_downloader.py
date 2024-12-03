import os
import pathlib
from src.downloader import Downloader
from .utils.http_file_server import TestingHTTPServer

TEMP_DIR = "./temp/"


# Consider looking into monkey patching instead of the HTTP server
def test_downloader():
    downloader = Downloader()
    with TestingHTTPServer():
        base_dir = pathlib.Path(TEMP_DIR)
        base_dir.mkdir(exist_ok=True)

        file_dest_path = base_dir.joinpath("test_downloader_file.pdf")
        if file_dest_path.exists():
            # Remove old if exists
            os.remove(file_dest_path)

        success = downloader.download("http://localhost:8000/pdf", file_dest_path)
        assert success

        assert file_dest_path.exists()
