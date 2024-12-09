"""
Automate benign FTP Traffic
Author: Kyri Lea

Requirements: ftplib
"""

import ftplib
import os
import random
import time
from datetime import datetime, timedelta

host = "192.168.105.52"
username = "student"
password = "student"

files = ["websites.txt", "ssh.py", "SVM.pdf", "fish.jpg"]

def do_ftp():
    ftp_server = ftplib.FTP(host, username, password)
    ftp_server.encoding = "utf-8"

    # Choose a random file from the list
    filename = files[random.randint(0, len(files)-1)]

    # Download that file from the server
    with open(filename, "wb") as file:
        ftp_server.retrbinary(f"RETR {filename}", file.write)

    # Close connection
    ftp_server.quit()

    # Delete the file so the script can be ran again
    try:
        os.remove(filename)
    except:
        pass


def run_12h():
    end_time = datetime.now() + timedelta(hours=12)

    while datetime.now() < end_time:
        do_ftp()
        wait_time = random.randint(5, 15) * 60  # Convert minutes to seconds
        time.sleep(wait_time)


run_12h()
    
