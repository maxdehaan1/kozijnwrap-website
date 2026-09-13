#!/usr/bin/env python3
"""Lokale preview die cleanUrls nabootst, net als Vercel doet.

    python3 serve.py      ->  http://localhost:4321
"""
import http.server, os, socketserver

PORT = 4321
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = super().translate_path(path)
        # /kozijnherstel -> kozijnherstel.html, /blog -> blog/index.html
        if not os.path.exists(p) and os.path.exists(p + ".html"):
            return p + ".html"
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "index.html")):
            return os.path.join(p, "index.html")
        return p

    def send_error(self, code, message=None, explain=None):
        page = os.path.join(ROOT, "404.html")
        if code == 404 and os.path.exists(page):
            body = open(page, "rb").read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def log_message(self, *a):
        pass


os.chdir(ROOT)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Preview op http://localhost:%d  (ctrl-c om te stoppen)" % PORT)
    httpd.serve_forever()
