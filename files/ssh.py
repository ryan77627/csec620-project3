"""
Automate benign SSH Traffic
Author: Kyri Lea

Requirements: paramiko
"""

import paramiko as pm
import random
import time
from datetime import datetime, timedelta

host1 = "192.168.105.50" # lin-client-1
host2 = "192.168.105.52" # lin-client-3
port = 22
username = "student"
password = "student"

def run_ssh(host):
    # A couple of commands that can be run
    commands = ["ls", "whoami", "pwd", "date", "cat /etc/passwd"]

    # Set up connection with host1
    ssh_client = pm.SSHClient()
    ssh_client.set_missing_host_key_policy(pm.AutoAddPolicy())
    ssh_client.connect(hostname=host, port=port, username=username, password=password)

    # Run a random command
    cmd = commands[random.randint(0, len(commands)-1)]
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    # We don't actually care what it returns

    # Close the connection
    ssh_client.close()

def run_24h():
    end_time = datetime.now() + timedelta(hours=24)

    while datetime.now() < end_time:
        # Run the function
        num = random.choice([1,2])
        host = host1 if num == 1 else host2
        run_ssh(host)
        
        # Wait for a random time between 5 to 30 minutes
        wait_time = random.randint(5, 20) * 60  # Convert minutes to seconds
        time.sleep(wait_time)

run_24h()
