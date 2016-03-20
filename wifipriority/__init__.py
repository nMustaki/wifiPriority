# -*- coding: utf-8 -*-
# https://github.com/seveas/python-networkmanager/blob/master/examples/info.py
# http://dev.iachieved.it/iachievedit/exploring-networkmanager-d-bus-systemd-and-raspberry-pi/
# https://pythonhosted.org/python-networkmanager/
from __future__ import print_function, absolute_import
from wifi_managers.wifi_manager_linux import WifiManagerLinux
from priorizer import Priorizer


if __name__ == "__main__":
    Priorizer(wifi_manager=WifiManagerLinux(), rules="best_strength").connect_to_best()
