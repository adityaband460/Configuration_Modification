from openpyxl import load_workbook
import sqlite3


file_path = "./config-changes.xlsx"

workbook = load_workbook(filename = file_path)

sheet = workbook['Sheet1']

PLMN = sheet['B2'].value
TAC = sheet['B3'].value

CELL_IDENTITY_0 = sheet['C4'].value
CELL_IDENTITY_1 = sheet['D4'].value
CELL_IDENTITY_2 = sheet['E4'].value

PCI_0 = sheet['C5'].value
PCI_1 = sheet['D5'].value
PCI_2 = sheet['E5'].value

DL_ARFCN_0 = sheet['C6'].value
DL_ARFCN_1 = sheet['D6'].value
DL_ARFCN_2 = sheet['E6'].value

UL_ARFCN_0 = sheet['C7'].value
UL_ARFCN_1 = sheet['D7'].value
UL_ARFCN_2 = sheet['E7'].value

BAND_INDICATOR_0 = sheet['C8'].value
BAND_INDICATOR_1 = sheet['D8'].value
BAND_INDICATOR_2 = sheet['E8'].value

MME_IP_ADDRESS = sheet['B9'].value
BBU_IP_ADDRESS = sheet['B10'].value



# print(PLMN, TAC)

db_path = "./20250314_amannagar_b1_zte6-RelocTimers-alarm2.sqlite"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Update PLMN
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
    # IpInterfaceTable     ---> IPInterfaceIPAddress where X_VENDOR_INTERFACE_TYPE ,X_VENDOR_SOURCE_PORT_NUMBER
    # 'OAM_S1AP_INTERFACE','36412'
    # 'OAM_X2AP_INTERFACE',36422
    # 'OAM_GTPU_INTERFACE',2152, 
    # globalEnbIdInfoTable  --> henb_self_address



    # Tr69InitParamsTable  --> ConnectionRequestURL --> 'http://10.131.183.31:15210'
    # EnodeBEMSIpsecTable   --> ENBIpAddress
    # ipAddressTable        --> ?

    update_bbu_ip_query_IpInterfaceTable = """ UPDATE IpInterfaceTable SET IPInterfaceIPAddress = ? 
    where Enable = '1' and (
        (X_VENDOR_INTERFACE_TYPE = 'OAM_S1AP_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = '36412') or 
        (X_VENDOR_INTERFACE_TYPE = 'OAM_X2AP_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = 36422) or
        (X_VENDOR_INTERFACE_TYPE = 'OAM_GTPU_INTERFACE' and X_VENDOR_SOURCE_PORT_NUMBER = 2152)) """
    
    update_bbu_ip_query_globalEnbIdInfoTable = """ UPDATE globalEnbIdInfoTable SET henb_self_address = ? """
    

    cursor.execute(update_bbu_ip_query_IpInterfaceTable, (BBU_IP_ADDRESS,))
    cursor.execute(update_bbu_ip_query_globalEnbIdInfoTable, (BBU_IP_ADDRESS,))
    # cursor.execute("UPDATE IpInterfaceTable SET IPInterfaceIPAddress = ? WHERE Alias = 'cpe-s1ap-1'", (BBU_IP_ADDRESS,))

    
    # commit the changes to the database
    conn.commit()

    if cursor.rowcount == 0:
        print("No rows were updated.")
    else:
        print(f"{cursor.rowcount} row(s) updated.")
    # print("PLMN updated successfully.")
    # print("TAC updated successfully.")
