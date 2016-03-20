# -*- coding: utf-8 -*-
"""Base class to be subclassed by various implementations"""

class WifiManagerBase(object):
    def check_conditions(self):
        raise NotImplementedError

    def get_connectable_networks(self):
        raise NotImplementedError

    def get_configured_networks(self):
        raise NotImplementedError

    def scan_wifi_networks(self):
        raise NotImplementedError

    def get_current_network(self):
        raise NotImplementedError

    def connect_to(self, ssid):
        """Activate a connection by name

            Args:
                ssid (string) : the ssid to connect to

            Raises:
                ValueError : if no valid adaptater found
        """
        raise NotImplementedError
