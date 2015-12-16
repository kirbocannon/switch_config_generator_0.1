__author__ = 'KennyB'
import sqlite3
import fileinput
import os

sqlite_file = r'/Users/KennyB/DB/Database/Switches.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

BaseTemplateFile = r'/Users/KennyB/DB/BaseConfig/BaseTemplate.txt'
hostnameInput = input('Enter Hostname: ')


#Make an SQL query that selects the entire Switches table and returns all values. Also print values for user.
#first, you must use the execute statement to execute an SQL command
#next, you can treat the cursor as an iterator to get a list of matching rows from the execute statement

hostnameRowSearch = c.execute("SELECT * FROM Switches WHERE Hostname=? COLLATE NOCASE", (hostnameInput,))

for i in c.fetchall():
    rowResult = i
    print('Here are all the parameters that were applied to the configuration: for ' + hostnameInput.upper() + ":",
          '\n',
          '\n',
          'District:                        ', i[0].upper(),
          '\n',
          'Site:                            ', i[1],
          '\n',
          'Hostname:                        ', i[2].upper(),
          '\n',
          'Serial Number:                   ', i[3],
          '\n',
          'IP Address:                      ', i[4],
          '\n',
          'Data Subnet Mask:                ', i[5],
          '\n',
          'Data Default - Gateway:          ', i[6],
          '\n',
          'Split-stack?:                    ', i[7],
          '\n',
          'Aruba RAP Switch Number:         ', i[8],
          '\n',
          'Aruba RAP Switch Port Count:     ', i[9],
          '\n',
          'Number of Aruba Devices:         ', i[10],
          '\n',
          'Uplink Port Desc:                ', i[11],
          '\n',
          'TACACS & NTP:                    ', i[12].upper(),
          '\n',
          'Time Zone:                       ', i[13].upper(),
          '\n',
          'Physical Location:               ', i[14],
          '\n',
          'Switch Model Number 1:           ', i[15],
          '\n',
          'Switch Model Number 2:           ', i[16],
          '\n',
          'Switch Model Number 3:           ', i[17],
          '\n',
          'Switch Model Number 4:           ', i[18],
          '\n',
          'Switch Model Number 5:           ', i[19],
          '\n',
          'Switch Model Number 6:           ', i[20],
          '\n',
          'Switch Model Number 7:           ', i[21],
          '\n',
          'Switch Model Number 8:           ', i[22],
          '\n',
          'Switch Model Number 9:           ', i[23],
          '\n',
          'QoS:                             ', i[24],
          '\n'
          )

## -----------------------------------start Set command references----------------------------------###
##
#

#functions to convert None type to string, also apply .lower() and .upper() for consistency
def convertToStringStandardLower(s):
    return '' if s is None else str(s).lower()

def convertToStringStandardUpper(s):
    return '' if s is None else str(s).upper()

#start switch row return reference variables
site = rowResult[1]
district = rowResult[0].upper()
ipAddress = rowResult[4]
subnetmask = rowResult[5]
defaultGateway = rowResult[6]
uplinks = convertToStringStandardUpper(rowResult[11])
hostname = rowResult[2].upper()
snmpPhysicalLocation = convertToStringStandardUpper(rowResult[14])
timezone = rowResult[13].upper()
splitStack = i[7].upper()
rapCfgCmd = '''
description Aruba RAP
switchport trunk native vlan 25
switchport mode trunk
no snmp trap link-status
spanning-tree portfast
service-policy input LAN-QOS-POLICY
nmsp attachment suppress
no shutdown
'''

#set switch variables, put through string conversion method - if None, convert to string to vaoid problems in further code
#none types are a problem because you can't call out the variable in further code and treat it like a string... it will return attrib error
#none types form when user doesn't enter data into a field. You'll see in SQL that fields will be NULL

switch1 = convertToStringStandardLower(rowResult[15])
switch2 = convertToStringStandardLower(rowResult[16])
switch3 = convertToStringStandardLower(rowResult[17])
switch4 = convertToStringStandardLower(rowResult[18])
switch5 = convertToStringStandardLower(rowResult[19])
switch6 = convertToStringStandardLower(rowResult[20])
switch7 = convertToStringStandardLower(rowResult[21])
switch8 = convertToStringStandardLower(rowResult[22])
switch9 = convertToStringStandardLower(rowResult[23])


## ------------------------------------end Set command references----------------------------------###

#start basic user port configuration
portCfg = '''
desc USER PORT
switchport access vlan 25
switchport mode access
switchport voice vlan 15
service-policy input LAN-QOS-POLICY
snmp trap mac-notification change added
snmp trap mac-notification change removed
no logging event link-status
no snmp trap link-status
nmsp attachment suppress
spanning-tree portfast
no shutdown
'''
#end basic user port configuration

#start user port configuration
switch1PortCfg24 = 'int gi1/0/4-24' + portCfg
switch1PortCfg48 = 'int gi1/0/4-48' + portCfg
switch2PortCfg24 = 'int gi2/0/1-24' + portCfg
switch2PortCfg48 = 'int gi2/0/1-48' + portCfg
switch3PortCfg24 = 'int gi3/0/1-24' + portCfg
switch3PortCfg48 = 'int gi3/0/1-48' + portCfg
switch4PortCfg24 = 'int gi4/0/1-24' + portCfg
switch4PortCfg48 = 'int gi4/0/1-48' + portCfg
switch5PortCfg24 = 'int gi5/0/1-24' + portCfg
switch5PortCfg48 = 'int gi5/0/1-48' + portCfg
switch6PortCfg24 = 'int gi6/0/1-24' + portCfg
switch6PortCfg48 = 'int gi6/0/1-48' + portCfg
switch7PortCfg24 = 'int gi7/0/1-24' + portCfg
switch7PortCfg48 = 'int gi7/0/1-48' + portCfg
switch8PortCfg24 = 'int gi8/0/1-24' + portCfg
switch8PortCfg48 = 'int gi8/0/1-48' + portCfg
switch9PortCfg24 = 'int gi9/0/1-24' + portCfg
switch9PortCfg48 = 'int gi9/0/1-48' + portCfg
#end user port configuration

hostnameCmd = 'hostname ' + hostname
domainNameCmd = 'ip domain-name ' + district + '.usa.doj.gov'
ipAddressCmd = 'ip address ' + ipAddress + ' ' + subnetmask
switch2PriorityCmd = 'switch 2 priority 10'
timezoneASTCmd = 'clock timezone ' + timezone + ' ' + '-4'
timezoneESTCmd = 'clock timezone ' + timezone + ' ' + '-5'
timezoneCSTCmd = 'clock timezone ' + timezone + ' ' + '-6'
timezoneMSTCmd = 'clock timezone ' + timezone + ' ' + '-7'
timezonePSTCmd = 'clock timezone ' + timezone + ' ' + '-8'
timezoneAKSTCmd = 'clock timezone ' + timezone + ' ' + '-9'
timezoneHSTCmd = 'clock timezone ' + timezone + ' ' + '-10'
defaultGatewayCmd = 'ip default-gateway ' + defaultGateway
uplinkRowResult = uplinks.split(',')
tacacsEastCmd = ''
tacacsWestCmd = ''
ntpEastCmd = '''
ntp server <ntp1> prefer
ntp server <ntp2>
'''
ntpWestCmd = '''
ntp server <ntp1> prefer
ntp server <ntp2>
'''




### ------------------------------------end set command variables ---------------------------------###


### ------------------------------------start create config file and folder---------------------------------###
#create path based on district if it doesn't exist
#the r before the string means (raw string literal) so backslashes will not be treated as escape characters
#which mitigates issues with things like regex but this is rarely needed anyway
newpath = r'/Users/KennyB/DB/ConfigFiles/%s' %district
if not os.path.exists(newpath):
    os.makedirs(newpath)

#create config file
ConfigFile = r'/Users/KennyB/DB/ConfigFiles/%s/%s-CONFIG.txt' %(district, hostnameInput.upper())

# try to remove the configuration file - if it doesn't exist, create it
try:
    os.remove(ConfigFile)

except FileNotFoundError:
    print(" Old Configuration file does not exist. Will now create a new one. Location: " + ConfigFile)

try:
    file = open(ConfigFile, 'w')
    file.close()

except PermissionError:
    print("There seems to be a permissions issue. Ensure you have full permission to " + ConfigFile)

except OSError:
    print("Something went wrong when creating the config file!")

### ------------------------------------end create config file and folder---------------------------------###

#find all variables and replace with table data from CSV
#notice the end='', this is new in python 3.x and allows you to specify what you wanted appened to the end of a print
#line. By default it is \n so we use a blank space so it doesn't auto insert a new line

with open(BaseTemplateFile) as BaseTemplate:
    lines = BaseTemplate.readlines()
    with open(ConfigFile, 'w') as f:
        f.writelines(lines)

# start domain name configuration #
with open(ConfigFile, 'r') as f:
    filedata = None
    filedata = f.read()
with open(ConfigFile, 'r+') as f:
    filedata = filedata.replace('$domainNameCmd', domainNameCmd)
    f.write(filedata)
# end start domain name configuration #

# start hostname configuration #
with open(ConfigFile, 'r') as f:
    filedata = None
    filedata = f.read()
with open(ConfigFile, 'r+') as f:
    filedata = filedata.replace('$hostnameCmd', hostnameCmd)
    f.write(filedata)
# end start hostname configuration #

# start ip address configuration #
with open(ConfigFile, 'r') as f:
    filedata = None
    filedata = f.read()
with open(ConfigFile, 'r+') as f:
    filedata = filedata.replace('$ipAddressCmd', ipAddressCmd)
    f.write(filedata)
# end ip address configuration #

# start default gateway configuration #
with open(ConfigFile, 'r') as f:
    filedata = None
    filedata = f.read()
with open(ConfigFile, 'r+') as f:
    filedata = filedata.replace('$defaultGatewayCmd', defaultGatewayCmd)
    f.write(filedata)
# end default gateway configuration #

#start snmp location configuration

# start timezone configuration
with open(ConfigFile, 'r') as f:
    filedata = None
    filedata = f.read()
if timezone == 'AST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezoneASTCmd)
        f.write(filedata)
elif timezone == 'EST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezoneESTCmd)
        f.write(filedata)
elif timezone == 'CST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezoneCSTCmd)
        f.write(filedata)
elif timezone == 'MST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezoneMSTCmd)
        f.write(filedata)
elif timezone == 'PST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezonePSTCmd)
        f.write(filedata)
elif timezone == 'AKST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezoneAKSTCmd)
        f.write(filedata)
elif timezone == 'HST':
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$timezoneCmd', timezoneHSTCmd)
        f.write(filedata)
# end timezone configuration

#start snmp location configuration

if snmpPhysicalLocation != '':
    snmpPhysicalLocationCmd = 'snmp-server location ' + snmpPhysicalLocation
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$snmpPhysicalLocationCmd', snmpPhysicalLocationCmd)
        f.write(filedata)

elif snmpPhysicalLocation == '':
    snmpPhysicalLocationCmd2 = 'snmp-server location ' + site
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$snmpPhysicalLocationCmd', snmpPhysicalLocationCmd2)
        f.write(filedata)
#end snmp location configuration

###------------------start Switch1-----------------------###

if switch1 != '':
    switch1ProvisionCmd = 'switch 1 provision ' + switch1
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch1ProvisionCmd', switch1ProvisionCmd)
        f.write(filedata)

    if switch1 == 'ws-c3850-24t' or switch1 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch1PortCfg24', switch1PortCfg24)
            f.write(filedata)

    elif switch1 == 'ws-c3850-48t' or switch1 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch1PortCfg48', switch1PortCfg48)
            f.write(filedata)
###------------------end Switch1-----------------------###

###------------------start Switch2-----------------------###

if switch2 != '':
    switch2ProvisionCmd = 'switch 2 provision ' + switch2
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch2ProvisionCmd', switch2ProvisionCmd)
        f.write(filedata)
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch2PriorityCmd', switch2PriorityCmd)
        f.write(filedata)

    if switch2 == 'ws-c3850-24t' or switch2 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch2PortCfg24', switch2PortCfg24)
            f.write(filedata)

    elif switch2 == 'ws-c3850-48t' or switch2 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch2PortCfg48', switch2PortCfg48)
            f.write(filedata)
###------------------end Switch2-----------------------###

###------------------start Switch3-----------------------###

if switch3 != '':
    switch3ProvisionCmd = 'switch 3 provision ' + switch3
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch3ProvisionCmd', switch3ProvisionCmd)
        f.write(filedata)

    if switch3 == 'ws-c3850-24t' or switch3 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch3PortCfg24', switch3PortCfg24)
            f.write(filedata)

    elif switch3 == 'ws-c3850-48t' or switch3 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch3PortCfg48', switch3PortCfg48)
            f.write(filedata)
###------------------end Switch3-----------------------###

###------------------start Switch4-----------------------###

if switch4 != '':
    switch4ProvisionCmd = 'switch 4 provision ' + switch4
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch4ProvisionCmd', switch4ProvisionCmd)
        f.write(filedata)

    if switch4 == 'ws-c3850-24t' or switch4 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch4PortCfg24', switch4PortCfg24)
            f.write(filedata)

    elif switch4 == 'ws-c3850-48t' or switch4 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch4PortCfg48', switch4PortCfg48)
            f.write(filedata)
###------------------end Switch4-----------------------###

###------------------start Switch5-----------------------###

if switch5 != '':
    switch5ProvisionCmd = 'switch 5 provision ' + switch5               #start putting these in nested if statements?
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch5ProvisionCmd', switch5ProvisionCmd)
        f.write(filedata)

    if switch5 == 'ws-c3850-24t' or switch5 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch5PortCfg24', switch5PortCfg24)
            f.write(filedata)

    elif switch5 == 'ws-c3850-48t' or switch5 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch5PortCfg48', switch5PortCfg48)
            f.write(filedata)
###------------------end Switch5-----------------------###

###------------------start Switch6-----------------------###

if switch6 != '':
    switch6ProvisionCmd = 'switch 6 provision ' + switch6
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch6ProvisionCmd', switch6ProvisionCmd)
        f.write(filedata)

    if switch6.lower() == 'ws-c3850-24t' or switch6.lower() == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch6PortCfg24', switch6PortCfg24)
            f.write(filedata)

    elif switch6.lower() == 'ws-c3850-48t' or switch6.lower() == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch6PortCfg48', switch6PortCfg48)
            f.write(filedata)

###------------------end Switch6-----------------------###

###------------------start Switch7-----------------------###

if switch7 != '':
    switch7ProvisionCmd = 'switch 7 provision ' + switch7
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch7ProvisionCmd', switch7ProvisionCmd)
        f.write(filedata)

    if switch7.lower() == 'ws-c3850-24t' or switch7 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch7PortCfg24', switch7PortCfg24)
            f.write(filedata)

    elif switch7 == 'ws-c3850-48t' or switch7 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch7PortCfg48', switch7PortCfg48)
            f.write(filedata)
###------------------end Switch7-----------------------###

###------------------start Switch8-----------------------###

if switch8 != '':
    switch8ProvisionCmd = 'switch 8 provision ' + switch8
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch8ProvisionCmd', switch8ProvisionCmd)
        f.write(filedata)

    if switch8 == 'ws-c3850-24t' or switch8 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch8PortCfg24', switch8PortCfg24)
            f.write(filedata)

    elif switch8 == 'ws-c3850-48t' or switch8 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch8PortCfg48', switch8PortCfg48)
            f.write(filedata)
###------------------end Switch8-----------------------###

###------------------start Switch9-----------------------###

if switch9 != '':
    switch9ProvisionCmd = 'switch 9 provision ' + switch9
    with open(ConfigFile, 'r') as f:
        filedata = None
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$switch9ProvisionCmd', switch9ProvisionCmd)
        f.write(filedata)

    if switch9 == 'ws-c3850-24t' or switch9 == 'ws-c3850-24p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch9PortCfg24', switch9PortCfg24)
            f.write(filedata)

    elif switch9 == 'ws-c3850-48t' or switch9 == 'ws-c3850-48p':
        filedata = None
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$switch9PortCfg48', switch9PortCfg48)
            f.write(filedata)
###------------------end Switch9-----------------------###

###------------------start uplink port desc-----------------------###
#row result port descriptions are seperated by commas by the user. The commas are used to split into a list, then
#print seperate strings to replace the $ variables. THere is a while loop because there are only 4 uplink ports
#the try, exception is used for when the index is out of range (i.e. there aren't more than x amount of port desc)

def configUplinks():
    if uplinks != '' or uplinks != None:
        count = -1 #set count below 0 index (first item in split list)
        uplinkNum = 1
        while count < 3: #there are only 4 uplinks so from 0 to 3 is looped
            count += 1

            filedata = None
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$uplink%sDescCmd' %uplinkNum, uplinkRowResult[count])
                f.writelines(filedata)
                uplinkNum += 1

try:
    configUplinks()
except IndexError:
    pass
except NameError:
    pass

###------------------end uplink port desc-------------------------###

#Start Aruba RAP configuration to cfg file
#aruba raps are optional so try/catch cause is used
# this allows user to enter the switch number of the switch to have the RAPs provisoned, the program will figure out
#how many ports the switch has by looking at the data in the switch1,2,3,etc fields

def calcRapPorts():
    rapPortCnt = str(portCount - rapDeviceCount + 1)
    rapPortRangeCmd = ('int range gi' + str(rapSwitchNumber) + '/' + '0/' + rapPortCnt + '-' + str(portCount))
    rapPortCfgCmd = rapPortRangeCmd + rapCfgCmd
    filedata = None
    with open(ConfigFile, 'r') as f:
        filedata = f.read()
    with open(ConfigFile, 'r+') as f:
        filedata = filedata.replace('$arubaRapCmd', rapPortCfgCmd)
        f.write(filedata)

try:
    rapSwitchNumber = rowResult[8]
    rapDeviceCount = rowResult[10]
    if rapSwitchNumber != '' or rapSwitchNumber.upper() != 'NONE' or rapSwitchNumber != 0 or rapSwitchNumber != None:
#check for switch 1
        if rapSwitchNumber == 1:
            if switch1 == 'ws-c3850-24t' or switch1 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch1 == 'ws-c3850-48t' or switch1 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 2
        elif rapSwitchNumber == 2:
            if switch2 == 'ws-c3850-24t' or switch2 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch2 == 'ws-c3850-48t' or switch2 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 3
        elif rapSwitchNumber == 3:
            if switch3 == 'ws-c3850-24t' or switch3 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch3 == 'ws-c3850-48t' or switch3 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 4
        elif rapSwitchNumber == 4:
            if switch4 == 'ws-c3850-24t' or switch4 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch4 == 'ws-c3850-48t' or switch4 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 5
        elif rapSwitchNumber == 5:
            if switch5 == 'ws-c3850-24t' or switch5 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch5 == 'ws-c3850-48t' or switch5 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 6
        elif rapSwitchNumber == 6:
            if switch6 == 'ws-c3850-24t' or switch6 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch6 == 'ws-c3850-48t' or switch6 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 7
        elif rapSwitchNumber == 7:
            if switch7 == 'ws-c3850-24t' or switch7 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch7 == 'ws-c3850-48t' or switch7 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 8
        elif rapSwitchNumber == 8:
            if switch8 == 'ws-c3850-24t' or switch8 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch8 == 'ws-c3850-48t' or switch8 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()
#check for switch 9
        elif rapSwitchNumber == 9:
            if switch9 == 'ws-c3850-24t' or switch9 == 'ws-c3850-24p':
                portCount = 24
                calcRapPorts()
            elif switch9 == 'ws-c3850-48t' or switch9 == 'ws-c3850-48p':
                portCount = 48
                calcRapPorts()

except NameError:
    pass
except TypeError:
    pass
    print('This switch was not configured for any Aruba RAP Devices.')
#End Aruba RAP configuration to cfg file


