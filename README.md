# wifiPriority
Auto connect to wireless network according to priority rules

# What is it
So I have two wifi networks at home, and I want my computer to connect to the strongest of the two.
NetworkManager will do it one day (backend seems to be there, but there's no UI for it),but in the meantime I'm growing grumpy.
So this project aims to check wifi reception and connect to the best network.

# Current state
For now it's only a proof of concept but extra dirty copy-pasted code... It can only gets better, right ?
For the moment, it scans for all available wifi networks, and connects to the strongest one for which you have checked autoconnect.

# Usage
```python
python wifipriority.py
```

# Roadmap
- clean code, (re)factor...
- force wifi rescan (what about battery life ?)
- daemonize
- handles custom priorities based on a conf file
- refactor again

# Under the hood
- Python 2.7
- python-networkmanager and code stolen from theirs examples
- system packages for python dbus bindings
