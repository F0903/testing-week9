import logging
import os
from pathlib import Path
import threading
from typing import Optional
from queue import Queue
import polars as pl
from xlsxwriter import Workbook
from .downloader import Downloader

LOG = logging.getLogger(__name__)


def assign_with_resize(lst, index, value):
    """
    Utility function that resizes a list to the specified index range if it is smaller than it.
    """

    if index >= len(lst):
        # Extend the list with None to the required size
        lst.extend([None] * (index + 1 - len(lst)))
    lst[index] = value


# Class for handling a file with download links
class PolarFileHandler:

    # Creates an instance of the filehandler with a dictionary of successfull downloads
    def __init__(self, number_of_threads: Optional[int] = 10, timeout=30) -> None:
        LOG.info("Initializing PolarFileHandler with % threads...", number_of_threads)

        self.number_of_threads = number_of_threads
        self.timeout = timeout

    # Function that starts a download instance using the downloader class. Used in threads
    def download_thread(self, queue: Queue) -> None:
        LOG.debug("Running download thread with queue = %", queue)

        while not queue.empty():
            index, link, destination, name, alt_link, finished_dict = queue.get()

            LOG.debug("Setting up download of %", name)

            downloader = Downloader()
            Path(destination).mkdir(exist_ok=True)

            # Dictionaries are not necesarily thread safe but appending to it is so this is fine. If more complicated tasks where needed you would use a mutex lock etc
            assign_with_resize(finished_dict["BRnum"], index, name)

            downloaded = downloader.download(
                url=link,
                destination_path=os.path.join(destination, name + ".pdf"),
                alt_url=alt_link,
                timeout=self.timeout,
            )

            assign_with_resize(
                finished_dict["pdf_downloaded"],
                index,
                "yes" if downloaded else "no",
            )
            queue.task_done()

    def start_download(self, url_file: str, meta_file: str, destination: str) -> None:
        """
        Starts downlaoding files from urls listed in url_file which will be placed in the destination, and reported in the meta file.
        """

        LOG.debug("Starting download of % to %", url_file, destination)

        file_data = pl.read_excel(
            source=url_file, columns=["BRnum", "Pdf_URL", "Report Html Address"]
        )

        # We index after the BRnums for now
        ID = "BRnum"

        # Initiates empty dataframe
        report_data = pl.DataFrame()
        # Tries reading the files listed as not downloaded if it fails it will make a new meta file that fullfills the structure
        try:
            report_data = pl.read_excel(meta_file, columns=[ID, "pdf_downloaded"])
            report_data = report_data.filter(pl.col("pdf_downloaded") == "yes")
            # Sort out files that are downloaded
            file_data = file_data.join(report_data, on=ID, how="anti")
        except:
            print("New meta data file will be created")

        # Return if empty, all files have been successfully downloaded
        if not file_data.rows():
            return

        queue = Queue()

        # Creates a dictionary of downloads
        finished_dict = {ID: [], "pdf_downloaded": []}

        # counter to only download 10 files
        j = 0
        # We thru each br number and starts a download
        for index, row in enumerate(file_data.rows(named=True)):
            if j == 20:
                break
            alt_link = row["Report Html Address"]
            link = row["Pdf_URL"]
            id = row[ID]
            # Creates a new thread and adds them to the list so that we can make sure all downloads are done before exiting
            queue.put([index, link, destination, id, alt_link, finished_dict])
            j += 1

        # Makes sure each thread is done
        for _ in range(self.number_of_threads):
            thread = threading.Thread(target=self.download_thread, args=(queue,))
            thread.start()

        queue.join()
        # Creates a dataframe from the dictionary of downloads
        finished_data_frame = pl.from_dict(finished_dict)

        if not report_data.is_empty():
            finished_data_frame = pl.concat(
                [finished_data_frame, report_data], rechunk=True
            )

        with Workbook(meta_file) as file:
            finished_data_frame.write_excel(workbook=file)
