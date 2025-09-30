import csv
import sqlite3
import sys
import re
import os

# Get the database file path from the folder
def getDatabaseFilePath():

    package_path = os.path.dirname(os.path.abspath(__file__))
    package_sw_path = os.path.join(package_path, 'cm/sw')
    runlte_path = os.path.join(package_sw_path, 'bin/run_lte_enbsm')

    with open(runlte_path, 'r') as file:

        print("Reading file:", runlte_path)
        config_file_name = None

        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            
            match = re.search(r'./enbSm.out\s+(\S+)', line)
            if match:
                config_file_path = match.group(1)
                print("Config file name found on line {}: {}".format(line_number,config_file_path))
                break
            

        config_file_name = os.path.basename(config_file_path)
        print("filename:", config_file_name)

        db_path = os.path.join(package_sw_path,'cfg' ,config_file_name)
        print("Database file path:", db_path)
        return db_path

def createCsvFromDatabaseFile(db_path: str, output_path: str = "sqlite_db.csv"):
    
    ROW_TITLES = ['','PLMN', 'TAC', 'CELL_IDENTITY','PCI', 'DL_ARFCN_',
                'UL_ARFCN', 'BAND_INDICATOR','MME_IP_ADDRESS', 'BBU_IP_ADDRESS',
                'DL_BANDWIDTH','UL_BANDWIDTH','ReferenceSignalPower','RRH_MAX_TX_POWER',
                'GLOBAL_ENB_ID','MANAGEMENT_MODE','EMP_IP_ADDRESS','EMS_USERNAME']

    COL_TITLES = ['','System','Sector-0', 'Sector-1', 'Sector-2']

    # create a matrix to hold the data
    data_matrix = [['' for _ in range(len(COL_TITLES))] for _ in range(len(ROW_TITLES))]
      
    # Fill the first column with row titles
    for i, title in enumerate(ROW_TITLES):
        data_matrix[i][0] = title
    
    # Fill the first row with column titles
    for j, title in enumerate(COL_TITLES):
        data_matrix[0][j] = title

    try:    
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Get PLMN 
            get_plmn_PLMNTable = """ SELECT PLMNID FROM PLMNTable """
            cursor.execute(get_plmn_PLMNTable)

            PLMN = int(cursor.fetchone()[0])
            data_matrix[1][1] = PLMN

            # Get TAC
            # EpcTable --> TAC
            get_tac_EpcTable = """ SELECT TAC FROM EpcTable """
            cursor.execute(get_tac_EpcTable)

            TAC = int(cursor.fetchone()[0])
            data_matrix[2][1] = TAC

            # Get CELL_IDENTITY
            get_cell_idnetity_0 = """ SELECT CellIdentity FROM CellIdentityTable WHERE CellIndex = '0' """
            get_cell_identity_1 = """ SELECT CellIdentity FROM CellIdentityTable WHERE CellIndex = '1' """
            get_cell_identity_2 = """ SELECT CellIdentity FROM CellIdentityTable WHERE CellIndex = '2' """
            
            cursor.execute(get_cell_idnetity_0)
            CELL_IDENTITY_0 = int(cursor.fetchone()[0])
            data_matrix[3][2] = CELL_IDENTITY_0
            
            cursor.execute(get_cell_identity_1)
            CELL_IDENTITY_1 = int(cursor.fetchone()[0])
            data_matrix[3][3] = CELL_IDENTITY_1
            
            cursor.execute(get_cell_identity_2)
            CELL_IDENTITY_2 = int(cursor.fetchone()[0])
            data_matrix[3][4] = CELL_IDENTITY_2

            # Get PCI
            # UPDATE RFParamsTable SET PhyCellID = ? 
            # WHERE CellIndex = ? """
            get_pci_0 = """ SELECT PhyCellID FROM RFParamsTable WHERE CellIndex = '0' """
            get_pci_1 = """ SELECT PhyCellID FROM RFParamsTable WHERE CellIndex = '1' """
            get_pci_2 = """ SELECT PhyCellID FROM RFParamsTable WHERE CellIndex = '2' """

            cursor.execute(get_pci_0)
            PCI_0 = int(cursor.fetchone()[0])
            data_matrix[4][2] = PCI_0

            cursor.execute(get_pci_1)
            PCI_1 = int(cursor.fetchone()[0])
            data_matrix[4][3] = PCI_1
            
            cursor.execute(get_pci_2)
            PCI_2 = int(cursor.fetchone()[0])
            data_matrix[4][4] = PCI_2
            
            # Get DL_ARFCN
            # update_earfcn_dl_query_RFParamsTable = """ UPDATE RFParamsTable SET EARFCNDL = ? 
            # WHERE CellIndex = ? """

            get_dl_arfcn_0 = """ SELECT EARFCNDL FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_dl_arfcn_0)
            DL_ARFCN_0 = int(cursor.fetchone()[0])
            data_matrix[5][2] = DL_ARFCN_0

            get_dl_arfcn_1 = """ SELECT EARFCNDL FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_dl_arfcn_1)
            DL_ARFCN_1 = int(cursor.fetchone()[0])
            data_matrix[5][3] = DL_ARFCN_1

            get_dl_arfcn_2 = """ SELECT EARFCNDL FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_dl_arfcn_2)
            DL_ARFCN_2 = int(cursor.fetchone()[0])
            data_matrix[5][4] = DL_ARFCN_2

            # Get UL_ARFCN
            # update_earfcn_ul_query_RFParamsTable = """ UPDATE RFParamsTable SET EARFCNUL = ?
            # WHERE CellIndex = ? """

            get_ul_arfcn_0 = """ SELECT EARFCNUL FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_ul_arfcn_0)
            UL_ARFCN_0 = int(cursor.fetchone()[0])
            data_matrix[6][2] = UL_ARFCN_0

            get_ul_arfcn_1 = """ SELECT EARFCNUL FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_ul_arfcn_1)
            UL_ARFCN_1 = int(cursor.fetchone()[0])
            data_matrix[6][3] = UL_ARFCN_1

            get_ul_arfcn_2 = """ SELECT EARFCNUL FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_ul_arfcn_2)
            UL_ARFCN_2 = int(cursor.fetchone()[0])
            data_matrix[6][4] = UL_ARFCN_2

            # Get BAND_INDICATOR
            # update_band_indicator_query_RFParamsTable = """ UPDATE RFParamsTable SET FreqBandIndicator = ?
            # WHERE CellIndex = ? """

            get_band_indicator_0 = """ SELECT FreqBandIndicator FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_band_indicator_0)
            BAND_INDICATOR_0 = int(cursor.fetchone()[0])
            data_matrix[7][2] = BAND_INDICATOR_0

            get_band_indicator_1 = """ SELECT FreqBandIndicator FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_band_indicator_1)
            BAND_INDICATOR_1 = int(cursor.fetchone()[0])
            data_matrix[7][3] = BAND_INDICATOR_1

            get_band_indicator_2 = """ SELECT FreqBandIndicator FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_band_indicator_2)
            BAND_INDICATOR_2 = int(cursor.fetchone()[0])
            data_matrix[7][4] = BAND_INDICATOR_2

            # Get MME_IP_ADDRESS
            get_mme_ip_address = """ SELECT S1SigLinkServerList FROM MMECommInfoTable """
            cursor.execute(get_mme_ip_address)
            MME_IP_ADDRESS = cursor.fetchone()[0]
            data_matrix[8][1] = MME_IP_ADDRESS

            # Get BBU_IP_ADDRESS
            # UPDATE globalEnbIdInfoTable SET henb_self_address 
            get_bbu_ip_address = """ SELECT henb_self_address FROM globalEnbIdInfoTable """
            cursor.execute(get_bbu_ip_address)
            BBU_IP_ADDRESS = cursor.fetchone()[0]
            data_matrix[9][1] = BBU_IP_ADDRESS


            # Get DL_Bandwidth
            # RFParamsTable --> DLBandwidth

            get_dl_bandwidth_0 = """ SELECT DLBandwidth FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_dl_bandwidth_0)
            DL_BANDWIDTH_0 = cursor.fetchone()[0]
            data_matrix[10][2] = DL_BANDWIDTH_0

            get_dl_bandwidth_1 = """ SELECT DLBandwidth FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_dl_bandwidth_1)
            DL_BANDWIDTH_1 = cursor.fetchone()[0]
            data_matrix[10][3] = DL_BANDWIDTH_1

            get_dl_bandwidth_2 = """ SELECT DLBandwidth FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_dl_bandwidth_2)
            DL_BANDWIDTH_2 = cursor.fetchone()[0]
            data_matrix[10][4] = DL_BANDWIDTH_2
            
            # Get UL_Bandwidth
            # RFParamsTable --> ULBandwidth
            get_ul_bandwidth_0 = """ SELECT ULBandwidth FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_ul_bandwidth_0)
            UL_BANDWIDTH_0 = cursor.fetchone()[0]
            data_matrix[11][2] = UL_BANDWIDTH_0

            get_ul_bandwidth_1 = """ SELECT ULBandwidth FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_ul_bandwidth_1)
            UL_BANDWIDTH_1 = cursor.fetchone()[0]
            data_matrix[11][3] = UL_BANDWIDTH_1

            get_ul_bandwidth_2 = """ SELECT ULBandwidth FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_ul_bandwidth_2)
            UL_BANDWIDTH_2 = cursor.fetchone()[0]
            data_matrix[11][4] = UL_BANDWIDTH_2
            
            # Get RFParamsTable --> ReferenceSignalPower
            get_reference_signal_power_0 = """ SELECT ReferenceSignalPower FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_reference_signal_power_0)
            REFERENCE_SIGNAL_POWER_0 = int(cursor.fetchone()[0])
            data_matrix[12][2] = REFERENCE_SIGNAL_POWER_0

            get_reference_signal_power_1 = """ SELECT ReferenceSignalPower FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_reference_signal_power_1)
            REFERENCE_SIGNAL_POWER_1 = int(cursor.fetchone()[0])
            data_matrix[12][3] = REFERENCE_SIGNAL_POWER_1

            get_reference_signal_power_2 = """ SELECT ReferenceSignalPower FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_reference_signal_power_2)
            REFERENCE_SIGNAL_POWER_2 = int(cursor.fetchone()[0])
            data_matrix[12][4] = REFERENCE_SIGNAL_POWER_2

            # Get RFParamsTable --> RRHMaxTxPower
            get_rrh_max_tx_power_0 = """ SELECT RRHMaxTxPower FROM RFParamsTable WHERE CellIndex = '0' """
            cursor.execute(get_rrh_max_tx_power_0)
            RRH_MAX_TX_POWER_0 = int(cursor.fetchone()[0])
            data_matrix[13][2] = RRH_MAX_TX_POWER_0

            get_rrh_max_tx_power_1 = """ SELECT RRHMaxTxPower FROM RFParamsTable WHERE CellIndex = '1' """
            cursor.execute(get_rrh_max_tx_power_1)
            RRH_MAX_TX_POWER_1 = int(cursor.fetchone()[0])
            data_matrix[13][3] = RRH_MAX_TX_POWER_1
            
            get_rrh_max_tx_power_2 = """ SELECT RRHMaxTxPower FROM RFParamsTable WHERE CellIndex = '2' """
            cursor.execute(get_rrh_max_tx_power_2)
            RRH_MAX_TX_POWER_2 = int(cursor.fetchone()[0])
            data_matrix[13][4] = RRH_MAX_TX_POWER_2

            # Get globalEnbIdInfoTable --> GlobalEnbId
            get_global_enb_id = """ SELECT GlobalEnbId FROM globalEnbIdInfoTable """
            cursor.execute(get_global_enb_id)
            GLOBAL_ENB_ID = cursor.fetchone()[0]
            data_matrix[14][1] = GLOBAL_ENB_ID

            # Get ManagementMode
            # EnodebParamsTable --> ManagementMode
            get_management_mode = """ SELECT ManagementMode FROM EnodebParamsTable """
            cursor.execute(get_management_mode)
            MANAGEMENT_MODE = cursor.fetchone()[0]
            data_matrix[15][1] = MANAGEMENT_MODE

            # Get EMP_IP_ADDRESS
            get_emp_ip_address = """ SELECT EMSIpAddress FROM EnodeBEMSIpsecTable """
            cursor.execute(get_emp_ip_address)
            EMP_IP_ADDRESS = cursor.fetchone()[0]
            data_matrix[16][1] = EMP_IP_ADDRESS
            
            # Get EMS_USERNAME
            get_ems_username = """ SELECT Username FROM Tr69InitParamsTable """
            cursor.execute(get_ems_username)
            EMS_USERNAME = cursor.fetchone()[0]
            
            PRODUCT_CLASS, OUI, SERIAL_NUMBER = EMS_USERNAME.split('-')
            data_matrix[17][2] = PRODUCT_CLASS
            data_matrix[17][3] = OUI
            data_matrix[17][4] = SERIAL_NUMBER

    except sqlite3.Error as e:
        print("SQLite error: {}".format(e))
        exit(1)

    # Write in output csv file from data_matrix
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 0th row of data matrix contains column titles
        writer.writerows(data_matrix)  
        print("CSV file '{}' created successfully.".format(output_path))

def updateDatabaseFileFromCsv(db_path: str, input_path: str = "sqlite_db.csv"):
    
    data_matrix = []
    # Read the CSV file and populate the data_matrix
    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            data_matrix.append(row)

    # Extract values from data_matrix
    PLMN = data_matrix[1][1]
    TAC = data_matrix[2][1]

    CELL_IDENTITY_0 = data_matrix[3][2]
    CELL_IDENTITY_1 = data_matrix[3][3]
    CELL_IDENTITY_2 = data_matrix[3][4] 

    PCI_0 = data_matrix[4][2]
    PCI_1 = data_matrix[4][3]    
    PCI_2 = data_matrix[4][4]

    DL_ARFCN_0 = data_matrix[5][2]    
    DL_ARFCN_1 = data_matrix[5][3]    
    DL_ARFCN_2 = data_matrix[5][4]

    UL_ARFCN_0 = data_matrix[6][2]    
    UL_ARFCN_1 = data_matrix[6][3]    
    UL_ARFCN_2 = data_matrix[6][4]    
    
    BAND_INDICATOR_0 = data_matrix[7][2]    
    BAND_INDICATOR_1 = data_matrix[7][3]    
    BAND_INDICATOR_2 = data_matrix[7][4]

    MME_IP_ADDRESS = data_matrix[8][1]     
    BBU_IP_ADDRESS = data_matrix[9][1]
    CONNECTION_REQUEST_URL = "http://{}:15210".format(BBU_IP_ADDRESS)

    DL_BANDWIDTH_0 = data_matrix[10][2]
    DL_BANDWIDTH_1 = data_matrix[10][3]
    DL_BANDWIDTH_2 = data_matrix[10][4]

    UL_BANDWIDTH_0 = data_matrix[11][2]
    UL_BANDWIDTH_1 = data_matrix[11][3]
    UL_BANDWIDTH_2 = data_matrix[11][4]

    REFERENCE_SIGNAL_POWER_0 = data_matrix[12][2]
    REFERENCE_SIGNAL_POWER_1 = data_matrix[12][3]
    REFERENCE_SIGNAL_POWER_2 = data_matrix[12][4]

    RRH_MAX_TX_POWER_0 = data_matrix[13][2]
    RRH_MAX_TX_POWER_1 = data_matrix[13][3]
    RRH_MAX_TX_POWER_2 = data_matrix[13][4]

    GLOBAL_ENB_ID = data_matrix[14][1]

    MANAGEMENT_MODE = data_matrix[15][1]

    EMS_IP_ADDRESS = data_matrix[16][1]
    
    PRODUCT_CLASS = data_matrix[17][2]
    OUI = data_matrix[17][3]
    SERIAL_NUMBER = data_matrix[17][4]
    EMS_USERNAME = PRODUCT_CLASS + '-' + OUI + '-' + SERIAL_NUMBER

    # Connect to the SQLite database and update values
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Update PLMN
            # PLMNTable --> PLMNID
            # LTENeighbourCellInfoTable --> PLMNID
            # PeerEnbCommInfoTable --> PLMNID
            # OperatorInfoTable --> plmnId
            # UTRANNeighbourCellInfoTable --> PLMNID
            # GERANNeighbourCellInfoTable --> PLMNID

            update_plmn_query_PLMNTable = """ UPDATE PLMNTable SET PLMNID = ? """
            update_plmn_query_LTENeighbourCellInfoTable = """ UPDATE LTENeighbourCellInfoTable SET PLMNID = ? """ 
            update_plmn_query_PeerEnbCommInfoTable = """ UPDATE PeerEnbCommInfoTable SET PLMNID = ? """ 
            update_plmn_query_OperatorInfoTable = """ UPDATE OperatorInfoTable SET plmnId = ? """ 
            update_plmn_query_UTRANNeighbourCellInfoTable = """ UPDATE UTRANNeighbourCellInfoTable SET PLMNID = ? """ 
            update_plmn_query_GERANNeighbourCellInfoTable = """ UPDATE GERANNeighbourCellInfoTable SET PLMNID = ? """ 


            cursor.execute(update_plmn_query_PLMNTable, (PLMN,))
            cursor.execute(update_plmn_query_LTENeighbourCellInfoTable, (PLMN,))
            cursor.execute(update_plmn_query_PeerEnbCommInfoTable, (PLMN,))
            cursor.execute(update_plmn_query_OperatorInfoTable, (PLMN,))
            cursor.execute(update_plmn_query_UTRANNeighbourCellInfoTable, (PLMN,))
            cursor.execute(update_plmn_query_GERANNeighbourCellInfoTable, (PLMN,))


            # Update TAC
            # LTENeighbourCellInfoTable --> X_VENDOR_TAC
            # PeerEnbCommInfoTable --> TAC
            # EpcTable --> TAC

            update_tac_query_LTENeighbourCellInfoTable = """ UPDATE LTENeighbourCellInfoTable SET X_VENDOR_TAC = ? """
            update_tac_query_PeerEnbCommInfoTable = """ UPDATE PeerEnbCommInfoTable SET TAC = ? """
            update_tac_query_EpcTable = """ UPDATE EpcTable SET TAC = ? """

            cursor.execute(update_tac_query_LTENeighbourCellInfoTable, (TAC,))
            cursor.execute(update_tac_query_PeerEnbCommInfoTable, (TAC,))
            cursor.execute(update_tac_query_EpcTable, (TAC,))

            # Update Cell Identity
            # CellIdentityTable --> CellIdentity

            update_cell_identity_query_CellIdentityTable = """ UPDATE CellIdentityTable SET CellIdentity = ? 
            WHERE CellIndex = ? """

            cursor.execute(update_cell_identity_query_CellIdentityTable, (CELL_IDENTITY_0,'0'))
            cursor.execute(update_cell_identity_query_CellIdentityTable, (CELL_IDENTITY_1,'1'))
            cursor.execute(update_cell_identity_query_CellIdentityTable, (CELL_IDENTITY_2,'2'))

            # Update PCI
            # RFParamsTable --> PhyCellID 

            update_pci_query_RFParamsTable = """ UPDATE RFParamsTable SET PhyCellID = ? 
            WHERE CellIndex = ? """

            cursor.execute(update_pci_query_RFParamsTable, (PCI_0,'0'))
            cursor.execute(update_pci_query_RFParamsTable, (PCI_1,'1'))
            cursor.execute(update_pci_query_RFParamsTable, (PCI_2,'2'))

            # Update EARFCNDL
            # RFParamsTable    --> EARFCNDL

            update_earfcn_dl_query_RFParamsTable = """ UPDATE RFParamsTable SET EARFCNDL = ? 
            WHERE CellIndex = ? """

            cursor.execute(update_earfcn_dl_query_RFParamsTable, (DL_ARFCN_0,'0'))
            cursor.execute(update_earfcn_dl_query_RFParamsTable, (DL_ARFCN_1,'1'))
            cursor.execute(update_earfcn_dl_query_RFParamsTable, (DL_ARFCN_2,'2'))

            # Update EARFCNUL
            # RFParamsTable    --> EARFCNUL

            update_earfcn_ul_query_RFParamsTable = """ UPDATE RFParamsTable SET EARFCNUL = ?
            WHERE CellIndex = ? """

            cursor.execute(update_earfcn_ul_query_RFParamsTable, (UL_ARFCN_0,'0'))
            cursor.execute(update_earfcn_ul_query_RFParamsTable, (UL_ARFCN_1,'1'))
            cursor.execute(update_earfcn_ul_query_RFParamsTable, (UL_ARFCN_2,'2'))


            # Update Band Indicator
            # RFParamsTable --- > FreqBandIndicator

            update_band_indicator_query_RFParamsTable = """ UPDATE RFParamsTable SET FreqBandIndicator = ?
            WHERE CellIndex = ? """

            cursor.execute(update_band_indicator_query_RFParamsTable, (BAND_INDICATOR_0,'0'))
            cursor.execute(update_band_indicator_query_RFParamsTable, (BAND_INDICATOR_1,'1'))
            cursor.execute(update_band_indicator_query_RFParamsTable, (BAND_INDICATOR_2,'2'))

            # Update MME IP Address
            # MMECommInfoTable --> S1SigLinkServerList

            update_mme_ip_query_MMECommInfoTable = """ UPDATE MMECommInfoTable SET S1SigLinkServerList = ?"""

            cursor.execute(update_mme_ip_query_MMECommInfoTable, (MME_IP_ADDRESS,))


            # Update BBU IP Address

            # ipAddressTable 3 places : BBU_RRH_SFTP_IP, OAM_LCT_IP, CABACS_SNMP_AGENT
            # IpInterfaceTable 4 places : OAM_S1AP_INTERFACE, OAM_X2AP_INTERFACE, OAM_GTPU_INTERFACE, OAM_TR069_INTERFACE
            # Tr69InitParamsTable 1 place : ConnectionRequestURL
            # globalEnbIdInfoTable 1 place : henb_self_address
            # EnodeBEMSIpsecTable 1 place : ENBIpAddress
            # Modify in enbDenbDeviceInfo.txt 

            update_bbu_ip_query_ipAddressTable = """ UPDATE ipAddressTable 
            SET IPAddress = ? 
            WHERE ModuleName = 'BBU_RRH_SFTP_IP'
            or ModuleName = 'OAM_LCT_IP' 
            or ModuleName = 'CABACS_SNMP_AGENT' """

            update_bbu_ip_query_IpInterfaceTable = """ UPDATE IpInterfaceTable SET IPInterfaceIPAddress = ? 
            where Enable = '1' and (
                (X_VENDOR_INTERFACE_TYPE = 'OAM_S1AP_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = '36412') or 
                (X_VENDOR_INTERFACE_TYPE = 'OAM_X2AP_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = 36422) or
                (X_VENDOR_INTERFACE_TYPE = 'OAM_GTPU_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = 2152) or
                (X_VENDOR_INTERFACE_TYPE = 'OAM_TR069_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = '15210'))"""

            update_bbu_ip_query_Tr69InitParamsTable = """ UPDATE Tr69InitParamsTable SET ConnectionRequestURL = ? """

            update_bbu_ip_query_globalEnbIdInfoTable = """ UPDATE globalEnbIdInfoTable SET henb_self_address = ? """

            update_bbu_ip_query_EnodeBEMSIpsecTable = """ UPDATE EnodeBEMSIpsecTable SET ENBIpAddress = ? """


            
            cursor.execute(update_bbu_ip_query_ipAddressTable, (BBU_IP_ADDRESS,))
            cursor.execute(update_bbu_ip_query_IpInterfaceTable, (BBU_IP_ADDRESS,))
            cursor.execute(update_bbu_ip_query_Tr69InitParamsTable, (CONNECTION_REQUEST_URL,))
            cursor.execute(update_bbu_ip_query_globalEnbIdInfoTable, (BBU_IP_ADDRESS,))
            cursor.execute(update_bbu_ip_query_EnodeBEMSIpsecTable, (BBU_IP_ADDRESS,))

            # Update DL Bandwidth
            # RFParamsTable --> DLBandwidth

            update_dl_bandwidth_query_RFParamsTable = """ UPDATE RFParamsTable SET DLBandwidth = ?
            WHERE CellIndex = ? """
            cursor.execute(update_dl_bandwidth_query_RFParamsTable, (DL_BANDWIDTH_0,'0'))
            cursor.execute(update_dl_bandwidth_query_RFParamsTable, (DL_BANDWIDTH_1,'1'))
            cursor.execute(update_dl_bandwidth_query_RFParamsTable, (DL_BANDWIDTH_2,'2'))

            # Update UL Bandwidth
            # RFParamsTable --> ULBandwidth
            update_ul_bandwidth_query_RFParamsTable = """ UPDATE RFParamsTable SET ULBandwidth = ?
            WHERE CellIndex = ? """
            cursor.execute(update_ul_bandwidth_query_RFParamsTable, (UL_BANDWIDTH_0,'0'))
            cursor.execute(update_ul_bandwidth_query_RFParamsTable, (UL_BANDWIDTH_1,'1'))
            cursor.execute(update_ul_bandwidth_query_RFParamsTable, (UL_BANDWIDTH_2,'2'))

            # Update Referencesignal
            # RFParamsTable --> ReferenceSignalPower
            update_reference_signal_query_RFParamsTable = """ UPDATE RFParamsTable SET ReferenceSignalPower = ?
            WHERE CellIndex = ? """
            cursor.execute(update_reference_signal_query_RFParamsTable, (REFERENCE_SIGNAL_POWER_0,'0'))
            cursor.execute(update_reference_signal_query_RFParamsTable, (REFERENCE_SIGNAL_POWER_1,'1'))
            cursor.execute(update_reference_signal_query_RFParamsTable, (REFERENCE_SIGNAL_POWER_2,'2'))

            # Update RRH Max Tx Power
            # RFParamsTable --> RRHMaxTxPower
            update_rrh_max_tx_power_query_RFParamsTable = """ UPDATE RFParamsTable SET RRHMaxTxPower = ?
            WHERE CellIndex = ? """
            cursor.execute(update_rrh_max_tx_power_query_RFParamsTable, (RRH_MAX_TX_POWER_0,'0'))
            cursor.execute(update_rrh_max_tx_power_query_RFParamsTable, (RRH_MAX_TX_POWER_1,'1'))
            cursor.execute(update_rrh_max_tx_power_query_RFParamsTable, (RRH_MAX_TX_POWER_2,'2'))

            # Update globalEnbIdInfoTable --> GlobalEnbId
            update_global_enb_id_query = """ UPDATE globalEnbIdInfoTable SET GlobalEnbId = ? """
            cursor.execute(update_global_enb_id_query, (GLOBAL_ENB_ID,))
            
            # Update Management Mode
            # EnodebParamsTable --> ManagementMode
            update_management_mode_query = """ UPDATE EnodebParamsTable SET ManagementMode = ? """
            cursor.execute(update_management_mode_query, (MANAGEMENT_MODE,))
            
            ''' 
            Update EMS IP Address
            Tr69InitParamsTable --> serving_hems_address, initial_hems_address
            PerfMgmt --> URL
            EnodeBEMSIpsecTable --> EMSIpAddress            
            EnodeBLogBackUpTable --> URL, UplinkSpectrumURL
            '''

            tr_url = "http://{}:8080/acs/AcsServlet".format(EMS_IP_ADDRESS)
            perfMgmt_url = "sftp://{}/home/enbemsftp/PM/PMRCVD".format(EMS_IP_ADDRESS)
            enodeBLogBackUpTable_url = "sftp://{}/home/enbems/emsdata/devbkp/logbkp".format(EMS_IP_ADDRESS)
            uplinkSpectrum_url = "sftp://{}/home/enbems/emsdata/devbkp/ulbkp".format(EMS_IP_ADDRESS)

            update_ems_ip_query_Tr69InitParamsTable = """ UPDATE Tr69InitParamsTable SET serving_hems_address = ?,
            initial_hems_address = ? """
            update_ems_ip_query_PerfMgmt = """ UPDATE PerfMgmt SET URL = ? """
            update_ems_ip_query_EnodeBEMSIpsecTable = """ UPDATE EnodeBEMSIpsecTable SET EMSIpAddress = ? """
            update_ems_ip_query_EnodeBLogBackUpTable = """ UPDATE EnodeBLogBackUpTable SET URL = ?,
            UplinkSpectrumURL = ? """   

            cursor.execute(update_ems_ip_query_Tr69InitParamsTable, (tr_url, tr_url))
            cursor.execute(update_ems_ip_query_PerfMgmt, (perfMgmt_url,))
            cursor.execute(update_ems_ip_query_EnodeBEMSIpsecTable, (EMS_IP_ADDRESS,))
            cursor.execute(update_ems_ip_query_EnodeBLogBackUpTable, (enodeBLogBackUpTable_url, uplinkSpectrum_url))


            '''
            Update EMS Username
            Tr69InitParamsTable --> Username
            EnodebDeviceInfoTable --> ManufacturerOUI, ProductClass, SerialNumber, HardwareVersion
            RRHInfoTable --> RRHConnectionTopology
            CPRILinkTable --> CPRILinkName 'CHBBU300A-002488-1114B06611:CRU41284611-002488-1114B01111'
            '''
            update_ems_username_query_Tr69InitParamsTable = """ UPDATE Tr69InitParamsTable SET Username = ? """
            update_ems_username_query_EnodebDeviceInfoTable = """ UPDATE EnodebDeviceInfoTable SET
            ManufacturerOUI = ?, ProductClass = ?, SerialNumber = ? , HardwareVersion = ? """
            update_ems_username_query_RRHInfoTable = """ UPDATE RRHInfoTable SET RRHConnectionTopology = ? """
            update_ems_username_query_CPRILinkTable = """ UPDATE CPRILinkTable SET CPRILinkName = ? WHERE CPRILinkNumber = ? """


            # get values from CPRILinkTable by CPRILinkNumber (1,2,3)
            # split by ':' and take first part
            # insert EMS_USERNAME + ':' + second part of CPRILinkName
            get_CPRILinkName = """ SELECT CPRILinkName FROM CPRILinkTable """
            cursor.execute(get_CPRILinkName)

            CPRILinkName_array = cursor.fetchall()
            CPRILinkName_1 = CPRILinkName_array[0][0]
            CPRILinkName_2 = CPRILinkName_array[1][0]
            CPRILinkName_3 = CPRILinkName_array[2][0]

            cpriLinkName_1_parts = CPRILinkName_1.split(':')
            cpriLinkName_2_parts = CPRILinkName_2.split(':')
            cpriLinkName_3_parts = CPRILinkName_3.split(':')

            CPRILinkName_1_new = EMS_USERNAME + ':' + cpriLinkName_1_parts[1]
            CPRILinkName_2_new = EMS_USERNAME + ':' + cpriLinkName_2_parts[1]
            CPRILinkName_3_new = EMS_USERNAME + ':' + cpriLinkName_3_parts[1] 


            cursor.execute(update_ems_username_query_Tr69InitParamsTable, (EMS_USERNAME,))
            cursor.execute(update_ems_username_query_EnodebDeviceInfoTable, (OUI, PRODUCT_CLASS, SERIAL_NUMBER, PRODUCT_CLASS))
            cursor.execute(update_ems_username_query_RRHInfoTable, (EMS_USERNAME,))

            cursor.execute(update_ems_username_query_CPRILinkTable, (CPRILinkName_1_new,'1'))
            cursor.execute(update_ems_username_query_CPRILinkTable, (CPRILinkName_2_new,'2'))
            cursor.execute(update_ems_username_query_CPRILinkTable, (CPRILinkName_3_new,'3'))
            
            # commit the changes to the database
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite error: {}".format(e))
        exit(1)

    print("Database file '{}' updated successfully.".format(db_path))

def updateEnodebDeviceInfoFile(input_path: str = "sqlite_db.csv"):

    package_path = os.path.dirname(os.path.abspath(__file__))
    enbDeviceInfo_path = os.path.join(package_path, 'cm/sw/cfg/enbDeviceInfo.txt')
    data_matrix = []
    # Read the CSV file
    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data_matrix.append(row)

    BBU_IP_ADDRESS = data_matrix[9][1]
    MANAGEMENT_MODE = data_matrix[15][1]
    EMS_IP_ADDRESS = data_matrix[16][1]

    # Read the existing lines from enbDeviceInfo.txt and create a dictionary for all variables
    enbDeviceInfo_dict = {}
    with open(enbDeviceInfo_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                enbDeviceInfo_dict[key] = value

    # update in dictionary
    enbDeviceInfo_dict["henb_self_address"] = BBU_IP_ADDRESS
    enbDeviceInfo_dict["ManagementMode"] = MANAGEMENT_MODE
    enbDeviceInfo_dict["ems_ip_address"] = EMS_IP_ADDRESS

    # update enbDeviceInfo.txt file based on dictionary
    with open(enbDeviceInfo_path, 'w') as file:
        for key, value in enbDeviceInfo_dict.items():
            file.write("{}={}\n".format(key, value))

    print("enbDeviceInfo.txt file : '{}' updated successfully.".format(enbDeviceInfo_path))

def main():
   
    # Get the working Database file path from current
    db_path = getDatabaseFilePath()


    command = None
    if len(sys.argv) < 2:
        command = "view"
    else:
        command = sys.argv[1].lower()

    if command == "view":
        createCsvFromDatabaseFile(db_path)
    elif command == "update":
        updateDatabaseFileFromCsv(db_path)
        updateEnodebDeviceInfoFile()
    else:
        print("Invalid command. Use 'view' to create CSV from database or 'update' to update database from CSV.")
        sys.exit(1)

if __name__ == "__main__":
    main()