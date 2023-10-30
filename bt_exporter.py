"""Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) prom exporter"""

import os
import time
import requests
import binascii
import argparse
from time import sleep
from prometheus_client import start_http_server, Gauge, Enum
from bluepy import btle


class XiaoMiTemp(btle.DefaultDelegate):
    def __init__(self,mac,location, temp, humid, batt):
        btle.DefaultDelegate.__init__(self)
        self.mac=mac
        self.loc=location
        self.temp = temp
        self.humid = humid
        self.batt = batt

    def handleNotification(self, cHandle, data):
        databytes=bytearray(data)
        self.temp.labels(self.mac, self.loc).set(int.from_bytes(databytes[0:2],"little")/100)
        self.humid.labels(self.mac, self.loc).set(int.from_bytes(databytes[2:3],"little"))
        self.batt.labels(self.mac, self.loc).set(int.from_bytes(databytes[3:5],"little")/1000)


class AppMetrics:
    def __init__(self, devices, polling_interval_seconds=180):
        self.polling_interval_seconds = polling_interval_seconds
        self.devices = devices
        # Metrics scheme
        self.temperature = Gauge("lywsd03mmc_temp", "Current temperature", ['mac', 'location'])
        self.humidity = Gauge("lywsd03mmc_humid", "Current humidity", ['mac', 'location'])
        self.battery = Gauge("lywsd03mmc_batt", "Battery level", ['mac', 'location'])

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        for mac, location in self.devices:
            p = btle.Peripheral( )
            p.setDelegate( XiaoMiTemp(mac, location, self.temperature, self.humidity, self.battery) )

            # BLE performs very poorly, constant errors are not uncommon
            for attempt in range(10):
                try:
                    p.connect(mac)
                    p.waitForNotifications(15.0)
                    break
                except Exception as e:
                    pass
                finally:
                    p.disconnect()

def main():
    parser = argparse.ArgumentParser(
            description="Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) prom exporter")
    parser.add_argument(
            '--device',
            action='append',
            required=True,
            help="BLE Device in 'MAC;location' format")
    parser.add_argument(
            '--polling-interval',
            default=180,
            type=int,
            help='Polling interval in seconds')
    parser.add_argument(
            '--port',
            default=9877,
            type=int,
            help='Exporter port')

    args = parser.parse_args()

    devices = [tuple(device.split(';')) for device in args.device]
    polling_interval = args.polling_interval
    exporter_port = args.port

    app_metrics = AppMetrics(
        polling_interval_seconds=polling_interval,
        devices=devices
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
