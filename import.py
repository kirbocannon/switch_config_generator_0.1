__author__ = 'KennyB'
import csv, sqlite3
import os


databaseFileName = r'/Users/KennyB/DB/Database/Switches.db'
csvFileName = r'/Users/KennyB/DB/CSV_Import/newexport.csv'

# r+ = open a file for reading and writing. Pointer is placed at beginning of file
# w = opens a file for writing only. If the file does not exist, create a new file for writing
# w+ = oepns a file for reading and writing. Overwrites existing file if the file exists. Creates new file if it doesn't.
# a+ = opens file for appending and reading. file pointer is placed at end of file. if the file doesn't exist, create it'
def RemoveDatabaseFile():
    #Remove a database file if it exists
    try:
        os.remove(databaseFileName)
    except FileNotFoundError:
        pass
        print("Database File Not Found at: " + databaseFileName + ". Will now attempt to create new database file there...")
    except PermissionError:
        pass
        print("Permission error!")


def CreateDatabaseFile():
    #Create the database file if one doesn't exist
    try:
         f = open(databaseFileName, 'w')
         f.close
    except FileExistsError:
        pass
        print("file exists")
    except OSError:
        pass
        print("Creation of Database file failed")

def ImportDataFromCSV():
    conn = sqlite3.connect(databaseFileName)
    c = conn.cursor()
    with open(csvFileName, 'rt') as f:
        csvReader = csv.DictReader(f)
        to_db = [(i['District'], i['Site'], i['Hostname'], i['Serial Number'], i['IP Address'], i['Data Subnet Mask'], i['Data - Default Gateway'],
                         i['Split-stack?'], i['Aruba RAP Switch Number'], i['Aruba RAP Switch Port Count'], i['Number of Aruba Devices'],
                         i['Uplink Port Desc'], i['TACACS & NTP'], i['Time Zone'], i['Physical Location'], i['Switch 1 Model Number'],
                         i['Switch 2 Model Number'], i['Switch 3 Model Number'], i['Switch 4 Model Number'], i['Switch 5 Model Number'], i['Switch 6 Model Number'],
                         i['Switch 7 Model Number'], i['Switch 8 Model Number'], i['Switch 9 Model Number'], i['QoS']) for i in csvReader
                ]



#you need quotes.. double or single between columns with spaces or dashes or special characters etc.
#currently there are 26 values
    try:
        c.executemany("""INSERT INTO Switches(District, Site, Hostname, 'Serial Number', 'IP Address',
                        'Data Subnet Mask', 'Data - Default Gateway', 'Split-stack?', 'Aruba RAP Switch Number', 'Aruba RAP Switch Port Count',
                        'Number of Aruba Devices', 'Uplink Port Desc', 'TACACS & NTP', 'Time Zone', 'Physical Location', 'Switch 1 Model Number',
                        'Switch 2 Model Number', 'Switch 3 Model Number', 'Switch 4 Model Number', 'Switch 5 Model Number', 'Switch 6 Model Number', 'Switch 7 Model Number',
                        'Switch 8 Model Number', 'Switch 9 Model Number', 'QoS') VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", to_db)
    except sqlite3.IntegrityError:
        print("ERROR: There appears to be duplicate hostnames, serial numbers, or IP addresses in the CSV. Please remove duplicates and try again.")

    conn.commit()
    conn.close()
    print("Values Succesfully Imported!")

def CreateNewTable():

    RemoveDatabaseFile()
    CreateDatabaseFile()
    conn = sqlite3.connect(databaseFileName)
    c = conn.cursor()
    c.execute("CREATE TABLE SWITCHES (District TEXT, Site TEXT, Hostname TEXT UNIQUE, 'Serial Number' TEXT UNIQUE, 'IP Address' TEXT UNIQUE, PRIMARY KEY(Hostname))") #windows added unique fields
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Data Subnet Mask' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Data - Default Gateway' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Split-stack?' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Aruba RAP Switch Number' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Aruba RAP Switch Port Count' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Number of Aruba Devices' INTEGER ")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Uplink Port Desc' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'TACACS & NTP' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Time Zone' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Physical Location' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 1 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 2 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 3 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 4 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 5 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 6 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 7 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 8 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'Switch 9 Model Number' TEXT")
    c.execute("ALTER TABLE SWITCHES ADD COLUMN 'QoS' TEXT")
    conn.commit()
    conn.close()
    print("New Database Created!")

CreateNewTable()
ImportDataFromCSV()
