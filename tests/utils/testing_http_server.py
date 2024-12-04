from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from typing import Self
import base64
from .embedded_pdf import EMBEDDED_PDF


class TestingRequestHandler(BaseHTTPRequestHandler):
    """
    Custom request handler for testing server.
    """

    def pdf(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", "attachment; filename=test.pdf")
        self.end_headers()

        pdf_content = base64.b64decode(EMBEDDED_PDF)
        self.wfile.write(pdf_content)

    def do_GET(self):
        match self.path:
            case "/pdf":
                self.pdf()
            case _:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")


class TestingHTTPServer:
    """
    An extremely simple HTTP server for testing.

    Meant to be used with the context manager in testing for quick listening and closing.

    Spawns a seperate thread in context manager.
    """

    def __init__(self):
        server_address = ("localhost", 8000)
        self.httpd = HTTPServer(server_address, TestingRequestHandler)

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
