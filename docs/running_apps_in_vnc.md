# Running Applications using a VNC Server

This is a quick few steps needed to run applications in the display which is running VNC. 
Make the following changes in the ~/.vnc/xstartup

```bash
cd  ~/.vnc/
nano xstartup 
```
The updated file should look like the following:

```bash
#!/bin/sh

xrdb "$HOME/.Xresources"
xsetroot -solid grey
#x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
#x-window-manager &
# Fix to make GNOME work
export XKL_XMODMAP_DISABLE=1
/etc/X11/Xsession
X11Forwarding yes
```

When you launch and connect with the VNC screen you will need to run the following command on the terminal for running programs through cli.
```bash
xhost +
```
Now you can run your applications like firefox with simple command: 
```bash
firefox 
```
Alternatively you can run the browser directly through your cli. you need to have a VNC display connected in your viewer. 
```bash
export DISPLAY=:1
```