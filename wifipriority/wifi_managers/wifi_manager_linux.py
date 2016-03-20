# -*- coding: utf-8 -*-
# pylint: disable=E1101
from __future__ import print_function, absolute_import
import NetworkManager
from datastructures import WifiNetwork
from .wifi_manager_base import WifiManagerBase


class WifiManagerLinux(WifiManagerBase):
    def check_conditions(self):
        """Checks network manager state

            Raises:
                ValueError : if something is not ok
        """
        conditions = [
            NetworkManager.NetworkManager.NetworkingEnabled,
            NetworkManager.NetworkManager.WirelessEnabled,
            NetworkManager.Settings.CanModify
        ]
        if not all(conditions):
            raise ValueError("Basic conditions not ok")

    def get_connectable_networks(self):
        """Returns a list of discovered wifi networks for which we have connection info

            Return:
                list of WifiNetwork objects
        """
        available = []
        configured_connections = self.get_configured_networks()
        detected_networks = self.scan_wifi_networks()
        for ssid in configured_connections.keys():
            try:
                available.append(
                    WifiNetwork(ssid=ssid, strength=detected_networks[ssid])
                )
            except KeyError:
                pass
        return available

    def get_configured_networks(self):
        wifis = {}
        for conn in NetworkManager.Settings.ListConnections():
            settings = conn.GetSettings()['connection']
            if settings["type"] != "802-11-wireless":
                continue
            ssid_name = settings["id"].split("Auto ")
            if len(ssid_name) == 1:
                continue  # auto connect not set up
            wifis[ssid_name[1]] = {
                "strength": -1
            }
        return wifis

    def scan_wifi_networks(self):
        ssids = {}
        for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
                continue
            for access_point in dev.SpecificDevice().GetAccessPoints():
                ssids[access_point.Ssid] = {
                    "strength": access_point.Strength
                }
        return ssids

    def get_current_network(self):
        """Returns current wifi network

            Return:
                WifiNetwork
        """
        constants = NetworkManager.const

        for conn in NetworkManager.NetworkManager.ActiveConnections:
            devices_types = [constants('device_type', x.DeviceType) == "wifi" for x in conn.Devices]
            if not any(devices_types):
                continue

            settings = conn.Connection.GetSettings()
            return WifiNetwork(ssid=settings["802-11-wireless"]["ssid"], strength=-1)

    def connect_to(self, ssid):
        """Activate a connection by name

            Args:
                ssid (string) : the ssid to connect to

            Raises:
                ValueError : if no valid adaptater found
        """

        # Find the connection
        connections = NetworkManager.Settings.ListConnections()
        connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
        conn = connections[u"Auto {}".format(ssid)]

        # Find a suitable device
        ctype = conn.GetSettings()['connection']['type']
        if ctype == 'vpn':
            for dev in NetworkManager.NetworkManager.GetDevices():
                if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED and dev.Managed:
                    break
            else:
                raise ValueError("No active, managed device found")
        else:
            dtype = {
                '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI
            }.get(ctype, ctype)
            devices = NetworkManager.NetworkManager.GetDevices()

            for dev in devices:
                if dev.DeviceType == dtype:
                    break
            else:
                raise ValueError("No suitable and available %s device found" % ctype)

        # And connect
        NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
