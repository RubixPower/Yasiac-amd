#!/usr/bin/env python3
import os
import subprocess
import glob


class Control():
    __slots__ = (
                "current_folder",
                "fan_speed_file",
                "fan_speed_file_status",
                "__weakref__"
                )

    def __init__(self):
        self.current_folder = (
            f'{os.path.dirname(os.path.abspath(__file__))}/'
            )
        self.fan_speed_file = glob.glob(
            '/sys/devices/pci*/*/*/hwmon/hwmon*/pwm1'
            )[0]
        self.fan_speed_file_status = subprocess.getoutput(
            'sudo find /sys -name pwm1_enable'
            )

    def amd_fan_speed_mode_current(self):
        with open(self.fan_speed_file_status) as data:
            status = data.read().strip()
        if status == '0':
            return 'max'
        elif status == '1':
            return 'manual'
        elif status == '2':
            return 'auto'
        else:
            return 'error'

    def amd_fan_speed_mode_change(self, choice):
        def file_write(number):
            with open(self.fan_speed_file_status, 'w') as f:
                f.write(number)
        if choice == 'max':
            file_write('0')
        elif choice == 'manual':
            file_write('1')
        elif choice == 'auto':
            file_write('2')
        elif choice == 'error':
            file_write('2')

    def amd_fan_speed_change(self, number):
        with open(f'{self.fan_speed_file}', 'w') as f:
            f.write(str(number))

    def amd_fan_speed_current(self):
        with open(self.fan_speed_file) as data:
            curr_speed = data.read().strip()
        return int(curr_speed)
