# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from wifi_managers.wifi_manager_linux import WifiManagerLinux


class Priorizer(object):
    def __init__(self, wifi_manager, rules):
        self.wifi_manager = wifi_manager
        self.wifi_manager.check_conditions()
        self.rules = rules

    def connect_to_best(self):
        try:
            best = self._get_best_network(
                self.rules, self.wifi_manager.get_connectable_networks()
            )
        except IndexError:
            print("No wifi network discovered")
            return
        current = self.wifi_manager.get_current_network()

        if current.ssid != best.ssid:
            print("Got you NetworkManager ! Connecting to " + best.ssid)
            self.wifi_manager.connect_to(best.ssid)
        else:
            print("Already connected to best available")

    def _get_best_network(self, rules, available_networks):
        if rules == "best_strength":
            networks = sorted(available_networks, key=lambda x: x.strength, reverse=True)
            return networks[0]
        else:
            raise ValueError("Only rule for now is 'best_strength'")
