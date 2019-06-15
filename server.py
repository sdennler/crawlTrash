#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from crawl import crawlThunstetten, makeJson

hostName = '0.0.0.0'
serverPort = 8081


class crawlServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server_version = 'Server: crawlServer/1.1'
        if(self.path.endswith('/trash/thunstetten')):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(makeJson(crawlThunstetten()), 'utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), crawlServer)
    print('Server started http://%s:%s' % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print('Server stopped.')
