from http.server import BaseHTTPRequestHandler, HTTPServer


def run_http_server(port, process_command, cleanup):
    class HttpHandler(BaseHTTPRequestHandler):
        def _set_response(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            process_command(post_data)
            self._set_response()
            self.wfile.write("OK".encode('utf-8'))

    server_address = ('', port)
    httpd = HTTPServer(server_address, HttpHandler)
    print('Starting http server.\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        cleanup()
    httpd.server_close()
    print('Stopping http server.\n')