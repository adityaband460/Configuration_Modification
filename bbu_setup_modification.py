'''
This script modifies the radio profiles on BBM cards based on the configuration
specified in a CSV file. It reads the CSV file to determine the downlink bandwidth
for each BBM card, maps the bandwidth to the corresponding radio profile, and updates
the radio profile on each BBM card via SSH. Finally, it restarts the smInit
service to apply the changes.

'''


import csv
import sqlite3
import sys
import re
import os
import subprocess
import time


global package_path
global bbm0_ip
global bbm1_ip
global bbm2_ip
bbm0_ip = "152.10.1.1"
bbm1_ip = "172.15.1.1"
bbm2_ip = "142.5.1.1"
# Function return array of radio profiles based on csv input
def get_radioProfiles(input_path: str = "sqlite_db.csv"):
    
    data_matrix = []
    # Read the CSV file and populate the data_matrix
    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            data_matrix.append(row)

    # Extract values from data_matrix
    DL_BANDWIDTH_0 = data_matrix[10][2]
    DL_BANDWIDTH_1 = data_matrix[10][3]
    DL_BANDWIDTH_2 = data_matrix[10][4]

    BAND_INDICATOR_0 = data_matrix[7][2]    
    BAND_INDICATOR_1 = data_matrix[7][3]    
    BAND_INDICATOR_2 = data_matrix[7][4]

    print("DL_BANDWIDTH_0: {}".format(DL_BANDWIDTH_0))
    print("DL_BANDWIDTH_1: {}".format(DL_BANDWIDTH_1))
    print("DL_BANDWIDTH_2: {}".format(DL_BANDWIDTH_2))
    print("BAND_INDICATOR_0: {}".format(BAND_INDICATOR_0))
    print("BAND_INDICATOR_1: {}".format(BAND_INDICATOR_1))
    print("BAND_INDICATOR_2: {}".format(BAND_INDICATOR_2))

    # create mapping Bandwidth to MHz
    band_mapping = {
        "n25": "5",
        "n50": "10",
        "n100": "20"
    }
 
    radio_profile0_path = "default.json.{}MHz".format(band_mapping.get(DL_BANDWIDTH_0))
    radio_profile1_path = "default.json.{}MHz".format(band_mapping.get(DL_BANDWIDTH_1))
    radio_profile2_path = "default.json.{}MHz".format(band_mapping.get(DL_BANDWIDTH_2))

    print("Radio Profile 0 Path: {}".format(radio_profile0_path))
    print("Radio Profile 1 Path: {}".format(radio_profile1_path))
    print("Radio Profile 2 Path: {}".format(radio_profile2_path))

    # create array of radio profiles
    radio_profiles = [radio_profile0_path, radio_profile1_path, radio_profile2_path]
    return radio_profiles

# Function to input radio profiles array and update the database file
def updateRadioProfiles():

    waitForBBMToBeReachable()

    radio_profiles = get_radioProfiles()

    username = "root"
    password = "root"
    
    # Assuming the script is in package folder
    global package_path
    package_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(package_path)
    # scp bbm folder from package to bbm card 0
    bbm0_put = """sshpass -p '{0}' scp -o StrictHostKeyChecking=no -r bbm {1}@{2}:/home/root 
    """.format(password, username, bbm0_ip)

    # scp bbm folder from package to bbm card 1
    bbm1_put = """sshpass -p '{0}' scp -o StrictHostKeyChecking=no -r bbm {1}@{2}:/home/root 
    """.format(password, username, bbm1_ip)

    # scp bbm folder from package to bbm card 2
    bbm2_put = """sshpass -p '{0}' scp -o StrictHostKeyChecking=no -r bbm {1}@{2}:/home/root 
    """.format(password, username, bbm2_ip)

    subprocess.call(bbm0_put, shell=True)
    print("copied bbm to bbm0")
    subprocess.call(bbm1_put, shell=True)
    print("copied bbm to bbm1")
    subprocess.call(bbm2_put, shell=True)
    print("copied bbm to bbm2")

    # ssh to BBM card 0 and change permission of bbm folder
    # change radio profiles according to bandwidth

    bbm0_cmd = "chmod 777 -R bbm && " \
    "cd bbm/sw/ca_radio/radio_profiles && " \
    "cp {3} default.json && " \
    "exit".format(password, username, bbm0_ip, radio_profiles[0])

    change_bbm0_radio_profile = """sshpass -p '{0}' ssh -o StrictHostKeyChecking=no {1}@{2} "{4}"
    """.format(password, username, bbm0_ip, radio_profiles[0], bbm0_cmd)

    print("logging into bbm0 to change radio profile")
    subprocess.call(change_bbm0_radio_profile, shell=True)
    print("changed radio profile on bbm0")

    # ssh to BBM card 1 and change permission of bbm folder
    # change radio profiles according to bandwidth

    bbm1_cmd = "chmod 777 -R bbm && " \
    "cd bbm/sw/ca_radio/radio_profiles && " \
    "cp {3} default.json && " \
    "exit".format(password, username, bbm1_ip, radio_profiles[1])
    change_bbm1_radio_profile = """sshpass -p '{0}' ssh -o StrictHostKeyChecking=no {1}@{2} "{4}"
    """.format(password, username, bbm1_ip, radio_profiles[1], bbm1_cmd)

    print("logging into bbm1 to change radio profile")
    subprocess.call(change_bbm1_radio_profile, shell=True)
    print("changed radio profile on bbm1")

    # ssh to BBM card 2 and change permission of bbm folder
    # change radio profiles according to bandwidth

    bbm2_cmd = "chmod 777 -R bbm && " \
    "cd bbm/sw/ca_radio/radio_profiles && " \
    "cp {3} default.json && " \
    "exit".format(password, username, bbm2_ip, radio_profiles[2])

    change_bbm2_radio_profile = """sshpass -p '{0}' ssh -o StrictHostKeyChecking=no {1}@{2} "{4}"
    """.format(password, username, bbm2_ip, radio_profiles[2], bbm2_cmd)
    print("logging into bbm2 to change radio profile")
    subprocess.call(change_bbm2_radio_profile, shell=True)
    print("changed radio profile on bbm2")
def stopAllenbsm():
    # move to package path
    os.chdir("{}/cm/sw/bin".format(package_path))
    print("Stopping smInit service and killing all enbsm processes")
    # stop smInit and ftm service and execute killall_enbsm command to stop
    cmd = "systemctl stop smInit.service && systemctl stop ftm.service && ./killall_enbsm"            
    subprocess.call(cmd,shell=True)
    os.chdir(package_path)
    
def waitForBBMToBeReachable():
    # wait for ping to be successful for all bbm cards
    ping_bbm0 = "ping -c 1 {} > /dev/null 2>&1".format(bbm0_ip)
    ping_bbm1 = "ping -c 1 {} > /dev/null 2>&1".format(bbm1_ip)
    ping_bbm2 = "ping -c 1 {} > /dev/null 2>&1".format(bbm2_ip)

    while True:
        if subprocess.call(ping_bbm0, shell=True) == 0 and subprocess.call(ping_bbm1, shell=True) == 0 and subprocess.call(ping_bbm2, shell=True) == 0:
            print("All BBM cards are reachable")
            break
        else:
            print("Waiting for BBM cards to be reachable...")
            time.sleep(1)

def startSmInitService():
    stopAllenbsm()
    # move to home path
    os.chdir("/root")
    subprocess.call("chmod 777 -R {}".format(package_path), shell=True)


    
    # read /etc/systemd/system/smInit.service file and replace ExecStart path with package_path
    print("Updating smInit.service with correct package path")
    lines = []
    with open('/etc/systemd/system/smInit.service', 'r') as file:
        for line in file:

            if re.match(r'^\s*ExecStart=',line):
                line = "ExecStart=/bin/bash -c \"sleep 5; cd {}/cm/sw/bin; ./run_lte_enbsm > smInit.log\"".format(package_path)
                
            lines.append(line)

    with open('/etc/systemd/system/smInit.service', 'w') as file:
        file.writelines(lines)


    time.sleep(2)
    waitForBBMToBeReachable()


    print("Starting smInit service")
    # enable smInit service
    subprocess.call("systemctl enable smInit.service", shell=True)
    
    # reload systemd daemon
    subprocess.call("systemctl daemon-reload", shell=True)

    # start smInit service
    subprocess.call("systemctl start smInit.service", shell=True)

    print("smInit service started")

def main():
    updateRadioProfiles()
    startSmInitService()

if __name__ == "__main__":
    main()


