# Unilock :unlock:

Lock / Unlock all your (Gnome/Linux) computers at once.  


You should use this with Tailscale (or any other VPN), or anyone
in your network will be able to lock/unlock your computers. 
See the [Tailscale](#tailscale) section.

### Usage

#### Controller

Download `controller.py` onto your main
computer (Controller), and add the IPs of
computers you'd like to control to it.


For example:
```py
listeners = [
    # Delete these lines and
    # add IPs of your listeners here.
    '100.110.23.50',
    '100.21.245.51',
    '100.180.23.50:62000',
]
```

Then run `gdbus monitor -y -d org.freedesktop.login1 | python3 controller.py`.


#### Listeners

Download `listener.py` onto the computers
you'd like to control (Listeners), and
set the interface you'd like them to listen on.

For example:
```py
interface = 'eth0'
interface_ip = None  # Optional. We'll detect the IP

port = 49050 # default: 49050
```

then run `python3 listener.py`.

And you're all set.

### Systemd

You can create systemd services so Unilock
starts when your computer starts.

#### Controller

Put this at `~/.config/systemd/user/unilock-controller.service`
on your controller and run 
`systemctl --user enable unilock-controller --now` to enable it.

```
[Unit]
Description=Unilock Controller: Lock all systems when this system is locked
After=graphical.target
Wants=gnome-session.target

[Service]
ExecStart=/bin/bash -c "gdbus monitor -y -d org.freedesktop.login1 | python3 /path/to/controller.py"
Restart=on-failure
RestartSec=3s

[Install]
WantedBy=default.target
```

#### Listener

Put this at `~/.config/systemd/user/unilock-listener.service`
on your listeners and run
`systemctl --user enable unilock-listener --now` to enable it.

```
[Unit]
Description=Unilock Listener: Lock/Unlock this system following controller
After=graphical.target
Wants=gnome-session.target

[Service]
ExecStart=/bin/bash -c "python3 /path/to/listener.py"
Restart=on-failure
RestartSec=3s

[Install]
WantedBy=default.target
```

### Tailscale


If you use [Tailscale](https://tailscale.com/), set 
interface to `tailscale0` on
your listeners.

And add the `tailscaled.service` as
dependency to the Controller and Listener
systemd service files.


```
After=graphical.target tailscaled.service
Wants=gnome-session.target tailscaled.service
```

