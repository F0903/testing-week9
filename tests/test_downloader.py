import pathlib
from src.downloader import Downloader
from .utils.fs_utils import remove_if_exists
from .utils.testing_http_server import TestingHTTPServer

TEMP_DIR = "./temp/"


# Consider looking into monkey patching instead of the HTTP server
def test_downloader():
    downloader = Downloader()

    # Setup base dir and make sure it exists
    base_dir = pathlib.Path(TEMP_DIR)
    base_dir.mkdir(exist_ok=True)

    # Create full destination path and remove the file if it already exists
    file_dest_path = base_dir.joinpath("test_downloader_file.pdf")
    remove_if_exists(file_dest_path)

    with TestingHTTPServer():
        success = downloader.download("http://localhost:8000/pdf", file_dest_path)
        assert success
        assert file_dest_path.exists()


def test_downloader_denied():
    downloader = Downloader()

    # Setup base dir and make sure it exists
    base_dir = pathlib.Path(TEMP_DIR)
    base_dir.mkdir(exist_ok=True)

    # Create full destination path and remove the file if it already exists
    file_dest_path = base_dir.joinpath("test_downloader_file.pdf")
    remove_if_exists(file_dest_path)

    with TestingHTTPServer():
        success = downloader.download("http://localhost:8000/deny", file_dest_path)

        # Make sure we did not succeed and the file doesn't exist, since the web resource rejected
        assert not success
        assert not file_dest_path.exists()
