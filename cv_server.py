"""
Minimal CORS-enabled file server for CV uploads.
Run: python cv_server.py
Serves files from the cv/ directory on http://localhost:8765
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress logs

os.chdir(os.path.join(os.path.dirname(__file__), "cv"))
HTTPServer(("localhost", 8765), CORSHandler).serve_forever()
