from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from typing import Self


class TestPDFFileRequest(BaseHTTPRequestHandler):
    """
    PDF file request for testing
    """

    def do_GET(self):
        if not self.path == "/pdf":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", "attachment; filename=test.pdf")
        self.end_headers()
        self.wfile.write(b"%PDF-1.7")


class TestHTTPServer:
    """
    An extremely simple HTTP server for testing.

    Meant to be used with the context manager in testing for quick listening and closing.

    Spawns a seperate thread in context manager.
    """

    def __init__(self):
        server_address = ("localhost", 8000)
        self.httpd = HTTPServer(server_address, TestPDFFileRequest)

    def serve(self):
        self.httpd.serve_forever()
        print("HTTP Server running at http://localhost:8000/file")

    def serve_thread(self):
        self.server_thread = threading.Thread(target=self.serve, daemon=True)
        self.server_thread.start()

    def __enter__(self) -> Self:
        self.serve_thread()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.httpd.shutdown()
        print("HTTP Server shutdown.")
