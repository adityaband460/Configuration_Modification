	Able to connet to ems, able to change serial id, ems ip in both files
	Able to modify Managementmode,enodBip inside enbDeviceInfo.
	Modified so that code works for python version 2.7

 Keep this script inside the PI_REL package whose db file you want to modify.
 This code automatically finds current working db file path from run_lte file.


	1)To Create csv file 
		Run : python3 viewUpdateScript.py view
		
	2)To Update Sqlite file from csv
		make changes in generated csv file.
		Run : python3 viewUpdateScript.py update
		
		
