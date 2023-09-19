from utils.encryption import Encryption
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from utils import read_config

class StravaAuthHandler:
    client_id: str
    client_secret: str
    auth_code: str

    def __init__(self) -> None:
        config = read_config()
        self.client_id: str = Encryption().decrypt_string(config["strava_credentials"]["client_id"])
        self.client_secret: str = Encryption().decrypt_string(config["strava_credentials"]["client_secret"])
        self.server = HTTPServer(('localhost', 5000), self.RedirectHandler)


    class RedirectHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urlparse(self.path).query
            params = parse_qs(query)
            self.server.auth_code = params.get('code', [None])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Strava authorization code received. You can close this tab now.")

    def handle_request(self) -> None:
        self.server.handle_request()
        self.auth_code = self.server.auth_code



