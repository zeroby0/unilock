# unilock

Lock/Unlock all my computers at once.  

run `gdbus monitor -y -d org.freedesktop.login1 | python3 controller.py` on your main computer.
run `python3 listener.py` on computers that should follow the main computer. Gnome/Linux only.


Edit the controller.py and add ip and port of your
listeners to the `listeners` list.

### Systemd

Systemd unit file for controller.
Put this at `~/.config/systemd/user/unilock-controller.service`
on your controller.
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

Systemd unit file for listener. 
Put this at `~/.config/systemd/user/unilock-listener.service`
on listeners.
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


