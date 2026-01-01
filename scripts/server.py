#!/usr/bin/env python3
"""
Simple local HTTP server for the SaaS Directory Aggregator
Run this to start the server at http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

# Change to the script's directory
script_dir = Path(__file__).parent.absolute()
os.chdir(script_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

def start_server():
    Handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║          SaaS Directory Aggregator - Local Server             ║
╚════════════════════════════════════════════════════════════════╝

✓ Server running at: http://localhost:{PORT}
✓ Open your browser and navigate to: http://localhost:{PORT}

Press Ctrl+C to stop the server.
        """)
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped.")
            exit(0)

if __name__ == "__main__":
    start_server()
