from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from ArgoCD! ArgoCD hello From!")

server = HTTPServer(('0.0.0.0', 8080), Handler)
print("Listening on 8080")
server.serve_forever()

