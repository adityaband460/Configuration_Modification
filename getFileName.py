# to get config file name from run_lte_enbsm

import re
import os

runlte_path = '/home/baditya/Downloads/PI_REL_V1.4.6-P2/cm/sw/bin/run_lte_enbsm'
with open(runlte_path, 'r') as file:

    print("Reading file:", runlte_path)
    config_file_name = None

    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        # skip empty lines and comments
        match = re.search(r'./enbSm.out\s+(\S+)', line)
        if match:
            config_file_path = match.group(1)
            print(f"Config file name found on line {line_number}: {config_file_path}")
            break
        

    config_file_name = os.path.basename(config_file_path)
    print("filename:", config_file_name)
        

    
