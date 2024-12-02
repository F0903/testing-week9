from typing import Optional
import os
from .polar_file_handler import PolarFileHandler


# Class for instantiating a download from a file into a given path.
class Controller:

    # Initiates the controller class with default values
    def __init__(self) -> None:
        self.url_file_name = os.path.join("customer_data", "GRI_2017_2020.xlsx")
        self.report_file_name = os.path.join("customer_data", "Metadata2017_2020.xlsx")
        self.destination = "files"

    # Overwrites the file containing the url's
    def set_url_file(self, url_file_name: str) -> None:
        self.url_file_name = url_file_name

    # Overwrites the file to report succesfull downloads
    def set_repor_file(self, report_file_name: str) -> None:
        self.report_file_name = report_file_name

    # Overwrites download destination
    def set_destination(self, destination: str) -> None:
        self.destination = destination

    # Runs the filehandler
    def run(self, number_of_threads: Optional[int] = None) -> None:
        if number_of_threads:
            file_handler = PolarFileHandler(number_of_threads)
        else:
            file_handler = PolarFileHandler()
        file_handler.start_download(
            self.url_file_name, self.report_file_name, self.destination
        )
