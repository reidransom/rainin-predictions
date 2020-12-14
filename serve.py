import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


os.chdir('./dist')
server_object = HTTPServer(server_address=('', 9000), RequestHandlerClass=SimpleHTTPRequestHandler)
server_object.serve_forever()
