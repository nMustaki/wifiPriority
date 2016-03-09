# -*- coding: utf-8 -*-
import sys
import collections
import NetworkManager

# https://github.com/seveas/python-networkmanager/blob/master/examples/info.py
# http://dev.iachieved.it/iachievedit/exploring-networkmanager-d-bus-systemd-and-raspberry-pi/
# https://pythonhosted.org/python-networkmanager/


Wifi = collections.namedtuple('Wifi', 'name power')


def check_conditions():
    conditions = [
        NetworkManager.NetworkManager.NetworkingEnabled,
        NetworkManager.NetworkManager.WirelessEnabled,
        NetworkManager.Settings.CanModify
    ]
    if not all(conditions):
        raise ValueError("Basic conditions not ok")


def get_known_ssids():
    wifis = []
    for conn in NetworkManager.Settings.ListConnections():
        settings = conn.GetSettings()['connection']
        if settings["type"] != "802-11-wireless":
            continue
        ssid_name = settings["id"].split("Auto ")
        if len(ssid_name) == 1:
            continue  # auto connect not set up
        wifis.append(ssid_name[1])
    return wifis


def scan_ssids():
    ssids = {}
    for dev in NetworkManager.NetworkManager.GetDevices():
        if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
            continue
        for ap in dev.SpecificDevice().GetAccessPoints():
            ssids[ap.Ssid] = ap.Strength
    return ssids


def get_available_ssids(known_ssids, current_ssids):
    available = []
    for ssid in known_ssids:
        try:
            available.append(Wifi(name=ssid, power=current_ssids[ssid]))
            print ssid
        except KeyError:
            pass
    return sorted(available, key = lambda x: x.power, reverse=True)


def current_ssid():
    c = NetworkManager.const

    for conn in NetworkManager.NetworkManager.ActiveConnections:
        devices_types = [c('device_type', x.DeviceType) == "wifi" for x in conn.Devices]
        if not any(devices_types):
            continue

        settings = conn.Connection.GetSettings()
        return Wifi(name=settings["802-11-wireless"]["ssid"], power=-1)


def connectTo(name):
    """
    Activate a connection by name
    """

    # Find the connection
    connections = NetworkManager.Settings.ListConnections()
    connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
    conn = connections["Auto " + name]

    # Find a suitable device
    ctype = conn.GetSettings()['connection']['type']
    if ctype == 'vpn':
        for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED and dev.Managed:
                break
        else:
            print("No active, managed device found")
            sys.exit(1)
    else:
        dtype = {
            '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI,
            '802-3-ethernet': NetworkManager.NM_DEVICE_TYPE_ETHERNET,
            'gsm': NetworkManager.NM_DEVICE_TYPE_MODEM,
        }.get(ctype,ctype)
        devices = NetworkManager.NetworkManager.GetDevices()

        for dev in devices:
            if dev.DeviceType == dtype:
                break
        else:
            print("No suitable and available %s device found" % ctype)
            sys.exit(1)

    # And connect
    NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")


if __name__ == "__main__":
    check_conditions()
    available = get_available_ssids(get_known_ssids(), scan_ssids())
    print "available: " + str(available)
    current = current_ssid()
    print "current ssid " + str(current)
    if current.name != available[0].name:
        print "ahahah"
        connectTo(available[0].name)
    else:
        print "best available ok"
