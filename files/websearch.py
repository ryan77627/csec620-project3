"""
Automate benign DNS and HTTP traffic
Author: Kyri Lea

Requirements: dnspython 
"""

import dns.resolver
import requests
import random
import time
from datetime import datetime, timedelta

with open("websites.txt") as file:
    sites = [line.strip() for line in file]
    
    # Set script to run regularly for the first 12 hours
    end_time = datetime.now() + timedelta(hours=12)
    while datetime.now() < end_time:
        # Do a random DNS query
        try:
            site = sites[random.randint(0, len(sites))]
            result = dns.resolver.resolve(site, "A")
        except:
            pass

        # Wait 1-3 minutes before the next one
        wait_time = random.randint(1, 3) * 60  # Convert minutes to seconds
        time.sleep(wait_time)

        # Do two random HTTP Requests
        try:
            site = "http://" + sites[random.randint(0, len(sites))]
            result = requests.get(site)
            site = "http://" + sites[random.randint(0, len(sites))]
            result = requests.get(site)
        except:
            pass

        # Wait 1-3 minutes before the next one
        wait_time = random.randint(1, 3) * 60  # Convert minutes to seconds
        time.sleep(wait_time)

        # Connect to internal webserver
        try:
            site = "http://192.168.105.53"
            result = requests.get(site)
        except:
            pass

        # Wait 1-3 minutes before the next one
        wait_time = random.randint(1, 3) * 60  # Convert minutes to seconds
        time.sleep(wait_time)


    # Set script to run less frequently for the second 12 hours (overnight)
    end_time = datetime.now() + timedelta(hours=12)
    while datetime.now() < end_time:
        # Do a random DNS query
        try:
            site = sites[random.randint(0, len(sites))]
            result = dns.resolver.resolve(site, "A")
        except:
            pass

        # Wait 1-20 minutes before the next one
        wait_time = random.randint(1, 20) * 60  # Convert minutes to seconds
        time.sleep(wait_time)

        # Do a random HTTP Request
        try:
            site = "http://" + sites[random.randint(0, len(sites))]
            result = requests.get(site)
        except:
            pass

        # Wait 1-20 minutes before the next one
        wait_time = random.randint(1, 20) * 60  # Convert minutes to seconds
        time.sleep(wait_time)

        # Connect to internal webserver
        try:
            site = "http://192.168.105.53"
            result = requests.get(site)
        except:
            pass

        # Wait 1-20 minutes before the next one
        wait_time = random.randint(1, 20) * 60  # Convert minutes to seconds
        time.sleep(wait_time)
