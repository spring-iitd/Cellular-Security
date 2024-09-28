# Dummy HTTP Sever to check if NAT Port Forwarding is set up correctly or, not.

from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'CONNECTED')
        else:
            self.send_error(404)

def run(server_class=HTTPServer, handler_class=MyHandler, port=9999):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

