from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn
import urlparse
import time
import cgi

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        self.wfile.write(parsed_path.path)
        return

    def do_POST(self):
        # Parse the form data posted
        parsed_path = urlparse.urlparse(self.path)
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        self.send_response(201)
        self.end_headers()
        for field in form.keys():
            field_item = form[field]
            self.wfile.write('%s=%s\n' % (field, form[field].value))
        return
    
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 9000), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
