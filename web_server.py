from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        # query_params = parse_qs(self.path)
        query_params = parse_qs(parsed_url.query)

        discord_id = query_params.get('discord_id', [None])[0]

        if discord_id:
            print(f'Получили id: {discord_id}')

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # self.wfile.write(f"Discord ID received: {discord_id}".encode())

        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # self.wfile.write(f"Discord ID missing")

def run_server(address='', port=8000):
    server_address = (address, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Сервер запущен! Порт {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
