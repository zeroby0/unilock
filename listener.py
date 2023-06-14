import http.server
import socketserver
import subprocess
import netifaces


cmd_lock = [
    'dbus-send',
    '--session',
    '--dest=org.gnome.ScreenSaver',
    '--type=method_call',
    '--print-reply',
    '--reply-timeout=20000',
    '/org/gnome/ScreenSaver',
    'org.gnome.ScreenSaver.SetActive',
    'boolean:true'
]

cmd_unlock = [
    'dbus-send',
    '--session',
    '--dest=org.gnome.ScreenSaver',
    '--type=method_call',
    '--print-reply',
    '--reply-timeout=20000',
    '/org/gnome/ScreenSaver',
    'org.gnome.ScreenSaver.SetActive',
    'boolean:false'
]


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/unlock':
            subprocess.run(cmd_unlock, shell=True)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Unlock command executed')

        elif self.path == '/lock':
            subprocess.run(cmd_lock, shell=True)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Lock command executed')
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Invalid path')


# Get the IP address associated with the 'tailscale0' interface
interfaces = netifaces.interfaces()
tailscale0_ip = None
for interface in interfaces:
    if interface == 'tailscale0':
        addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if addresses:
            tailscale0_ip = addresses[0]['addr']
            break

if tailscale0_ip:
    # Set the server address and port
    server_address = (tailscale0_ip, 16384)

    # Create the HTTP server with custom request handler
    httpd = socketserver.TCPServer(server_address, MyRequestHandler)

    # Start the server
    print('Server listening on {}:{}'.format(*server_address))
    httpd.serve_forever()
else:
    print("Unable to find the IP address for 'tailscale0' interface.")