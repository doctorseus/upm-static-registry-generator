import sys
import urllib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class UMPRegistryRequestHandler(SimpleHTTPRequestHandler):

    def send_header(self, keyword: str, value: str) -> None:
        # We need to serve the files with a different content-type
        if keyword == 'Content-type':
            url_parts = urllib.parse.urlsplit(self.path)
            request_path = str(url_parts.path)
            if 'tgz' not in request_path:
                value = 'application/json'
        super().send_header(keyword, value)


if __name__ == '__main__':
    handler_class = UMPRegistryRequestHandler

    server_address = ('0.0.0.0', 8000)
    httpd = ThreadingHTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
