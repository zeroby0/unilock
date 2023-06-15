import http.server
import socketserver
import subprocess
import netifaces


interface = 'tailscale0'
interface_ip = None  # Optional. We'll detect the IP

port = 49050  # default: 49050

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
            subprocess.run(cmd_unlock)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Unlock command executed')

        elif self.path == '/lock':
            subprocess.run(cmd_lock)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Lock command executed')

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Invalid path')


def get_interface_ip(interface_p):
    # Get the IP address associated with the interface

    interfaces = netifaces.interfaces()
    interface_ip = None

    for interface in interfaces:
        if interface == interface_p:
            addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if addresses:
                interface_ip = addresses[0]['addr']
                break

    if interface_ip is None:
        raise RuntimeError(
            f"Unable to find the IP address for interface {interface_ip}")

    return interface_ip


if interface_ip is None:
    interface_ip = get_interface_ip(interface)


try:
    httpd = socketserver.TCPServer((interface_ip, port), MyRequestHandler)

    print(f'Server listening on {interface_ip}:{port}')

    httpd.serve_forever()

except KeyboardInterrupt:
    print('Shutting down')
    httpd.shutdown()
