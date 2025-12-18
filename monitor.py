#!/usr/bin/env python3
# monitor.py - Monitor proxy and IPS logs

import json
import time
from datetime import datetime
import docker
import requests

class ProxyMonitor:
    def __init__(self):
        self.client = docker.from_api()
        
    def check_containers(self):
        """Check container status"""
        containers = ['squid-proxy', 'snort-ids', 'suricata-ids']
        for container_name in containers:
            try:
                container = self.client.containers.get(container_name)
                print(f"[{datetime.now()}] {container_name}: {container.status}")
            except:
                print(f"[{datetime.now()}] {container_name}: Not running")
    
    def check_logs(self):
        """Check recent alerts"""
        try:
            with open('./snort/logs/alert', 'r') as f:
                alerts = f.readlines()[-10:]  # Last 10 alerts
                if alerts:
                    print(f"\nRecent Snort Alerts:")
                    for alert in alerts:
                        print(f"  {alert.strip()}")
        except:
            pass
    
    def proxy_health(self):
        """Check proxy health"""
        try:
            response = requests.get('http://google.com', 
                                  proxies={'http': 'http://localhost:3128'},
                                  timeout=5)
            print(f"Proxy connectivity: OK - Status {response.status_code}")
        except:
            print("Proxy connectivity: FAILED")

if __name__ == "__main__":
    monitor = ProxyMonitor()
    while True:
        print("\n" + "="*50)
        monitor.check_containers()
        monitor.check_logs()
        monitor.proxy_health()
        time.sleep(60)