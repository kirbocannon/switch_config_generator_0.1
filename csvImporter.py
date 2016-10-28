__author__ = 'Kenneth Buchanan'
import csv
import sqlite3
import os

#This program is used to import data about switches from a CSV into an SQLite database
# First, it creates an SQL database table called switches.db. Then, place the captured data into the database
#switchConfigGenerator.py will make SQL queries based on the info that was imported from the CSV

main_directory = r'\some\directory'
databaseFileName = main_directory + r'SQL_Database\Switches.db'
csvFileName = main_directory + r'Put_CSV_Here\2016-SSR-Configuration-Input.csv'

def RemoveDatabaseFile():
    '''Remove a database file if it exists'''
    try:
        os.remove(databaseFileName)
    except FileNotFoundError:
        print("Database File Not Found at: " + databaseFileName + ". Will now attempt to create new database file there...")
    except PermissionError:
        print('Updating %s' %(databaseFileName))

def CreateDatabaseFile():
    '''Create the database file if one doesn't exist'''
    try:
         f = open(databaseFileName, 'w')
         f.close
    except FileExistsError:
        print("file exists")
    except OSError:
        print("Creation of Database file failed")

def ImportDataFromCSV():
    '''Read data in CSV'''
    conn = sqlite3.connect(databaseFileName)
    c = conn.cursor()
    try:
        with open(csvFileName, 'rt') as f:
            csvReader = csv.DictReader(f)
            to_db = [(i['district'], i['site'], i['hostname'], i['ipAddress'], i['timeZone'], i['dataSubnetMask'], i['dataDefaultGateway'],
                             i['tacacsNtp'], i['switch1'], i['switch2'], i['switch3'], i['switch4'], i['switch5'], i['switch6'],
                             i['switch7'], i['switch8'], i['switch9'], i['oconusTapeLibrary'], i['branchServerVirtSite'],
                             i['panzura_iDRAC_ILO'], i['splitStack'], i['evoipFaxAnalogGateways'], i['evoipUPS'], i['taclanes'], i['remoteArubaDevices'],
                             i['physicalLocation']) for i in csvReader
                    ]
    except FileNotFoundError:
        print('\n' + "CSV File not found. CSV file should be named '2016-SSR-Configuration-Input.csv',and placed at this location: " + '\n' + csvFileName )


    try: #Insert data from CSV into SQL table
        c.executemany("""INSERT INTO Switches('district', 'site', 'hostname', 'ipAddress', 'timezone', 'dataSubnetMask', 'dataDefaultGateway',
                         'tacacsNtp', 'switch1', 'switch2', 'switch3', 'switch4', 'switch5', 'switch6',
                         'switch7', 'switch8', 'switch9', 'oconusTapeLibrary', 'branchServerVirtSite',
                         'panzura_iDRAC_ILO', 'splitStack', 'evoipFaxAnalogGateways', 'evoipUPS', 'taclanes', 'remoteArubaDevices',
                         'physicalLocation') VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", to_db
                      )
        print("All Values Successfully Imported!")

    except sqlite3.IntegrityError:
        print("ERROR: There appears to be duplicate hostnames, or IP addresses in the CSV. Not "
              "all values were imported. Please remove duplicates and try again.")

    conn.commit()
    conn.close()


def CreateNewTable():
    '''Create new SQL table for data to be imported into to. Set data validation/rules/etc'''
    RemoveDatabaseFile()
    CreateDatabaseFile()
    conn = sqlite3.connect(databaseFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE SWITCHES (district TEXT, site TEXT, hostname TEXT UNIQUE, 'ipAddress' TEXT UNIQUE, PRIMARY KEY(hostname))")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'timeZone' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'dataSubnetMask' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'dataDefaultGateway' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'tacacsNTP' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch1' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch2' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch3' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch4' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch5' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch6' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch7' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch8' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'switch9' TEXT ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'oconusTapeLibrary' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'branchServerVirtSite' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'panzura_iDRAC_ILO' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'splitStack' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'evoipFaxAnalogGateways' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'evoipUPS' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'taclanes' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'remoteArubaDevices' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'physicalLocation' TEXT ")
    conn.commit()
    conn.close()


#CreateNewTable()
#ImportDataFromCSV()
