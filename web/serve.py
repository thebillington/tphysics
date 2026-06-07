#!/usr/bin/env python3
import http.server
import webbrowser
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

readme_link = os.path.join(WEB_DIR, 'README.md')
examples_link = os.path.join(WEB_DIR, 'examples')
readme_src = os.path.join(REPO_ROOT, 'README.md')
examples_src = os.path.join(REPO_ROOT, 'examples')

if not os.path.exists(readme_link):
    os.symlink(readme_src, readme_link)
if not os.path.exists(examples_link):
    os.symlink(examples_src, examples_link)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_ROOT, **kwargs)

    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
        super().end_headers()

    def log_message(self, format, *args):
        if args and isinstance(args[0], str) and 'favicon' in args[0]:
            return
        super().log_message(format, *args)


if __name__ == '__main__':
    url = f'http://localhost:{PORT}/web/'
    print(f'Serving tphysics REPL at {url}')
    webbrowser.open(url)

    httpd = http.server.HTTPServer(('', PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
