__author__ = 'Kenneth Buchanan'
import sqlite3
import os
import re

main_directory = r'\some\directory'
# template locations
template_path_legacy = main_directory + r'IDF_Base_Templates\3750X-IDF-BaseTemplate.txt' #3750X Template
template_path = main_directory + r'IDF_Base_Templates\3850-IDF-BaseTemplate.txt' #3850 template

sqlite_file = main_directory + 'SQL_Database\Switches.db'
conn = sqlite3.connect(sqlite_file, check_same_thread=False) #allows different threads to access database. Needed for GUI
c = conn.cursor()



def hostnameSearchAutomatic():
    '''search entire hostname column in sql database then run configureHostname function against all hostnames found'''
    hostname_column_search = c.execute("SELECT HOSTNAME FROM SWITCHES")
    fetch_hostnames = c.fetchall() #variable needs to come after the sql query has been performed
    for hostname in fetch_hostnames: #for each hostname found, apply and create configuration
        configureHostname(hostname[0]) #index 0 used because fetchall returns tuple per hostname. so 0 is only available. Function is down below

    print(len(fetch_hostnames), 'configuration files have been created!', '\n')


#def hostnameSearchDistrict(district):
#    '''search for particular district'''
#    hostname_column_search = c.execute("SELECT HOSTNAME FROM SWITCHES WHERE DISTRICT=?", (district,))
#    fetch_hostnames = c.fetchall() #variable needs to come after the sql query has been performed
#    for hostname in fetch_hostnames: #for each hostname found, apply and create configuration
#        configureHostname(hostname[0]) #index 0 used because fetchall returns tuple per hostname. so 0 is only available. Function is down below
#    print(len(fetch_hostnames), 'configuration files have been created!', '\n')


def convertToStringLower(s):
    '''function to convert None type to string, also apply .lower()for consistency'''
    return '' if s is None else str(s).lower()

def convertToStringUpper(s):
    '''function to convert None type to string, also apply .upper()for consistency'''
    return '' if s is None else str(s).upper()

def convertToZeroIfEmpty(s):
    '''function to convert empty to 0 for consistency. This won't be needed in future because SQL data validation'''
    return 0 if s == '' else s

def convertToNoneLowerStringIfEmpty(s): # used for powerstack
    return 'none' if s is None else str(s).lower()

reserved_data_port = \
''' switchport mode access
 switchport access vlan 25
 no switchport voice vlan
 spanning-tree portfast
 snmp trap mac-notification change added
 snmp trap mac-notification change removed
 no logging event link-status
 nmsp attachment suppress
'''

reserved_voice_port = \
''' switchport mode access
 switchport access vlan 15
 no switchport voice vlan
 spanning-tree portfast
 snmp trap mac-notification change added
 snmp trap mac-notification change removed
 no logging event link-status
 nmsp attachment suppress
'''

#IDFX000 only - branch site's IDFX000 only to have TTD UPS
branchSTTDUpsIDFX000Cmd = \
'''
int gi1/0/5
 desc TTD-WAN UPS
''' + reserved_data_port
#IDFX000 only - branch site's IDFX000 only to have server virt
branchServerVirtUpsIDFX000Cmd = \
'''
int gi1/0/6
 desc Server Virt;UPS Mgmt
''' + reserved_data_port
#IDFX000 only - branch site's IDFX000 only to have data domain ipmi
branchDatadomainIpmiIDFX000Cmd = \
'''
int gi1/0/7
 desc DataDomain 2200 IPMI
''' + reserved_data_port
#IDFX000 only - branch site's IDFX000 only to have svmh21 ilo
branchSvmh21Green1ILOIDFX000Cmd = \
'''
int gi1/0/8
 desc SVMH21;Green Cable 1;ILO
''' + reserved_data_port
#IDFX000 only - branch site's IDFX000 only to have panzura ilo
branchPanzuraILOIDFX000Cmd = \
'''
int gi1/0/9
desc Panzura iDRAC (ILO)
''' + reserved_data_port

#---------------------------start analog fax gateway---------------------------------#
hqEvoipFaxGateway2IDF1000Cmd = \
'''
int gi1/0/5
 desc E-VOIP FXS ANALOG GATEWAY #2
''' + reserved_voice_port

hqEvoipFaxGateway2IDFX0XXCmd = \
'''
int gi1/0/4
 desc E-VOIP FXS ANALOG GATEWAY #2
''' + reserved_voice_port

branchEvoipFaxGateway2IDFX000Cmd = \
'''
int gi1/0/10
 desc E-VOIP FXS ANALOG GATEWAY #2
''' + reserved_voice_port

branchEvoipFaxGateway2IDFX0XXCmd = \
'''
int gi1/0/4
 desc E-VOIP FXS ANALOG GATEWAY #2
''' + reserved_voice_port

#---------------------------start evoip ups mgmt---------------------------------#
hqEvoipUpsMgmt2IDF1000Cmd = \
'''
int gi1/0/6
 desc E-VOIP UPS Mgmt #2
''' + reserved_data_port

hqEvoipUpsMgmt2IDF10XXCmd = \
'''
int gi1/0/5
 desc E-VOIP UPS Mgmt #2
''' + reserved_data_port

branchEvoipUpsMgmt2IDFX000Cmd = \
'''
int gi1/0/11
 desc E-VOIP UPS Mgmt #2
''' + reserved_data_port

branchEvoipUpsMgmt2IDFX0XXCmd = \
'''
int gi1/0/5
 desc E-VOIP UPS Mgmt #2
''' + reserved_data_port

#---------------------------start tape library---------------------------------#
branchOconusMgmtCmdIDFX000 = \
'''
int gi1/0/12
 desc OCONUS Tape Library Mgmt
''' + reserved_data_port

#---------------------------start taclanes-------------------------------------#
hqTaclane1IDF1000Cmd = \
'''
int gi1/0/7
 desc TACLANE #1
 speed 100
 duplex full
''' + reserved_data_port

hqTaclane1IDF10XXCmd = \
'''
int gi1/0/6
 desc TACLANE #1
 speed 100
 duplex full
''' + reserved_data_port

hqTaclane2IDF1000Cmd = \
'''
int gi1/0/8
 desc TACLANE #2
 speed 100
 duplex full
''' + reserved_data_port

hqTaclane1IDF10XXCmd = \
'''
int gi1/0/6
 desc TACLANE #1
 speed 100
 duplex full
''' + reserved_data_port

hqTaclane2IDF10XXCmd = \
'''
int gi1/0/7
 desc TACLANE #2
 speed 100
 duplex full
''' + reserved_data_port

branchTaclane1IDFX000Cmd = \
'''
int gi1/0/13
 desc TACLANE #1
 speed 100
 duplex full
''' + reserved_data_port

branchTaclane2IDFX000Cmd = \
'''
int gi1/0/14
 desc TACLANE #2
 speed 100
 duplex full
''' + reserved_data_port

branchTaclane1IDFX0XXCmd = \
'''
int gi1/0/6
 desc TACLANE #1
 speed 100
 duplex full
''' + reserved_data_port

branchTaclane2IDFX0XXCmd = \
'''
int gi1/0/7
 desc TACLANE #2
 speed 100
 duplex full
''' + reserved_data_port
#------------------------packet smart---------------------------------------#
hqPktSmtIDF1000Cmd = \
'''
int gi1/0/4
 desc E-VOIP PacketSmart MGMT
''' + reserved_voice_port

branchPktSmtIDFX000Cmd = \
'''
int gi1/0/4
 desc E-VOIP PacketSmart MGMT
''' + reserved_voice_port



#---------------------------start tacacs-------------------------------------#
tacacsEastCmd = \
'''aaa group server tacacs+ TACSERVERS
  server name ACS_NOC
  server name ACS_NOC_2
  ip tacacs source-interface vlan 25

tacacs-server directed-request
tacacs server ACS_NOC
 address ipv4 192.168.1.2
 key somekey
 timeout 10

tacacs-server directed-request
tacacs server ACS_SPTC
 address ipv4 192.168.1.2
 key somekey
 timeout 10 '''
tacacsWestCmd = \
'''aaa group server tacacs+ TACSERVERS
  server name ACS_SPTC
  server name ACS_NOC
  ip tacacs source-interface vlan 25

tacacs-server directed-request
tacacs server ACS_SPTC
 address ipv4 192.168.1.1
 key somekey
 timeout 10

tacacs-server directed-request
tacacs server ACS_NOC
 address ipv4 192.168.1.1
 key somkey
 timeout 10 '''

tacacsEast3750XCmd = \
'''
aaa group server tacacs+ TACSERVERS
  server 192.168.1.1
  server 192.168.1.12
  ip tacacs source-interface vlan 25

tacacs-server host 192.168.1.1 timeout 10 key somekey
tacacs-server host 192.168.1.2 timeout 10 key somekey
tacacs-server directed-request '''

tacacsWest3750XCmd = \
'''
aaa group server tacacs+ TACSERVERS
  server 10.200.33.36
  server 192.168.1.1
  ip tacacs source-interface vlan 25

tacacs-server host 192.168.1.1 timeout 10 key somekey
tacacs-server host 192.168.1.2 timeout 10 key somekey
tacacs-server directed-request '''

#---------------------------start ntp-------------------------------------#
ntpEastCmd = \
'''ntp server 192.168.1.5 prefer
ntp server 192.168.1.6
ntp source vlan 25 '''


ntpWestCmd = \
'''ntp server 192.168.1.5 prefer
ntp server 192.168.1.6
ntp source vlan 25 '''

#---------------------------start other port config-----------------------#
rapCfgCmd = \
'''
 description ARUBA RAP
 no switchport voice vlan
 switchport trunk native vlan 25
 switchport mode trunk
 snmp trap mac-notification change added
 snmp trap mac-notification change removed
 no logging event link-status
 spanning-tree portfast
 service-policy input INGRESS-QOS-POLICY
 nmsp attachment suppress
 no shutdown '''

portCfg = \
'''
 desc STANDARD ACCESS PORT
 switchport access vlan 25
 switchport mode access
 switchport voice vlan 15
 service-policy input INGRESS-QOS-POLICY
 snmp trap mac-notification change added
 snmp trap mac-notification change removed
 no logging event link-status
 nmsp attachment suppress
 spanning-tree portfast
 no shutdown
'''

splitStackCmd = \
'''
int gi1/1/2
 desc TO LEGACY 3750X IDF
'''

#start user port configuration
switch1PortCfg24 = 'int range gi1/0/4-24' + portCfg
switch1PortCfg48 = 'int range gi1/0/4-48' + portCfg
switch13750XPortCfg24 = 'int range gi1/0/2-24' + portCfg #3750X only
switch13750XPortCfg48 = 'int range gi1/0/2-48' + portCfg #3750X only
switch2PortCfg24 = 'int range gi2/0/1-24' + portCfg
switch2PortCfg48 = 'int range gi2/0/1-48' + portCfg
switch3PortCfg24 = 'int range gi3/0/1-24' + portCfg
switch3PortCfg48 = 'int range gi3/0/1-48' + portCfg
switch4PortCfg24 = 'int range gi4/0/1-24' + portCfg
switch4PortCfg48 = 'int range gi4/0/1-48' + portCfg
switch5PortCfg24 = 'int range gi5/0/1-24' + portCfg
switch5PortCfg48 = 'int range gi5/0/1-48' + portCfg
switch6PortCfg24 = 'int range gi6/0/1-24' + portCfg
switch6PortCfg48 = 'int range gi6/0/1-48' + portCfg
switch7PortCfg24 = 'int range gi7/0/1-24' + portCfg
switch7PortCfg48 = 'int range gi7/0/1-48' + portCfg
switch8PortCfg24 = 'int range gi8/0/1-24' + portCfg
switch8PortCfg48 = 'int range gi8/0/1-48' + portCfg
switch9PortCfg24 = 'int range gi9/0/1-24' + portCfg
switch9PortCfg48 = 'int range gi9/0/1-48' + portCfg
#end user port configuration

##end setting some variables##

def configureHostname(hostname):
    '''Make an SQL query that selects the entire Switches table and returns all values.
       first, you must use the execute statement to execute an SQL command
       next, you can treat the cursor as an iterator to get a list of matching rows from the execute statement'''
    hostname_row_search = c.execute("SELECT * FROM SWITCHES WHERE Hostname=? COLLATE NOCASE", (hostname,))
    fetch_data = c.fetchall() #variable needs to come after the sql query has been performed

    if fetch_data != []: # by defualt c.fetchall() will returnan empty list if nothing is found in the database.
        for i in fetch_data: #if hostname is not found in the database, run elif and exit program
            rowResult = i

## -----------------------------------start Set command variables----------------------------------###
#
        site = rowResult[1]
        district = rowResult[0].upper()
        ipAddress = rowResult[3]
        ntpTacacs = convertToStringUpper(rowResult[7])
        subnetmask = rowResult[5]
        defaultGateway = rowResult[6]
        hostname = rowResult[2].upper()
        timezone = rowResult[4].upper()
        switch1 = convertToStringLower(rowResult[8])
        switch2 = convertToStringLower(rowResult[9])
        switch3 = convertToStringLower(rowResult[10])
        switch4 = convertToStringLower(rowResult[11])
        switch5 = convertToStringLower(rowResult[12])
        switch6 = convertToStringLower(rowResult[13])
        switch7 = convertToStringLower(rowResult[14])
        switch8 = convertToStringLower(rowResult[15])
        switch9 = convertToStringLower(rowResult[16])
        splitStack = convertToZeroIfEmpty(rowResult[20]) #if switch is a split stack then add uplink port desc
        branchServerVirtSite = rowResult[18]
        panzura_iDRAC_ILO = rowResult[19]
        oconusTapeLibrary = rowResult[17]
        evoipFaxAnalogGateways = convertToZeroIfEmpty(rowResult[21])
        evoipUPS = convertToZeroIfEmpty(rowResult[22])
        taclanes = convertToZeroIfEmpty(rowResult[23])
        remoteArubaDevices = convertToZeroIfEmpty(rowResult[24])
        physicalLocation = convertToStringUpper(rowResult[25])
        physicalLocationCmd = 'snmp-server location ' + physicalLocation
        physicalLocationCmd2 = 'snmp-server location ' + district + '-' + site
        hostnameCmd = 'hostname ' + hostname
        domainNameCmd = 'ip domain-name ' + district.lower() + '.usa.doj.gov'
        ipAddressCmd = 'ip address ' + ipAddress + ' ' + subnetmask
        defaultGatewayCmd = 'ip default-gateway ' + defaultGateway
        # time variables below - syntax - timezone clock timezone <usa timezone> <utc offset in hours>
        timezoneASTCmd = 'clock timezone AST -4'
        timezoneESTCmd = 'clock timezone EST -5'
        timezoneCSTCmd = 'clock timezone CST -6'
        timezoneMSTCmd = 'clock timezone MST -7'
        timezoneAZSTCmd = 'clock timezone AZST -7'
        timezonePSTCmd = 'clock timezone PST -8'
        timezoneAKSTCmd = 'clock timezone AKST -9'
        timezoneHSTCmd = 'clock timezone HST -10'
        timezoneCHSTCmd = 'clock timezone CHST +10'
        timezoneCDT = 'clock summer-time CDT recurring 2 Sun Mar 2:00 1 Sun Nov 2:00'
        timezoneEDT = 'clock summer-time EDT recurring 2 Sun Mar 2:00 1 Sun Nov 2:00'
        timezoneMDT = 'clock summer-time MDT recurring 2 Sun Mar 2:00 1 Sun Nov 2:00'
        timezonePDT = 'clock summer-time PDT recurring 2 Sun Mar 2:00 1 Sun Nov 2:00'


    ### ------------------------------------end set command variables ---------------------------------###

        # depending on the hostname pattern match, aeither a 3750X config file or a 3850 one
        # use regex to determine if switch is hq IDF100, branch IDFX00, hq IDFX0X, or branch IDFXXX for 3750X
        # use regex to determine if switch is hq IDF1000, branch IDFX000, hq IDFX0XX, or branch IDFX0XX for 3850

        #3750X naming scheme
        hqIDF100Pattern = re.compile(r"^.*\D100$") #\D = has to be a non digit character
        hqIDF1XXPattern = re.compile(r"^.*\D1..$")
        branchIDFX00Pattern = re.compile(r"^.*\D.00$")
        branchIDFXXXPattern = re.compile(r"^.*\D...$")
        #3850 naming scheme
        hqIDF1000Pattern = re.compile(r"^.*\D1000$")
        hqIDF10XXPattern = re.compile(r"^.*\D10..$")
        branchIDFX000Pattern = re.compile(r"^.*\D.000$")
        branchIDFX0XXPattern = re.compile(r"^.*\D.0..$")

        #global BaseTemplateFile # python by default will try to search for variable locally in this function
                                # when you write BaseTemplateFile =  BaseTemplateFileLegacy, so need to make it look global


        # search name to find HQ, branch and IDF type for port reservations
        #3750X
        if re.findall(hqIDF100Pattern, hostname):
            BaseTemplateFile =  template_path_legacy# use 3750X base template instead
            site_switch_Type = 'HQ_IDF_100'
        elif re.findall(hqIDF1XXPattern, hostname):
            BaseTemplateFile = template_path_legacy
            site_switch_Type = 'HQ_IDF_1XX'
        elif re.findall(branchIDFX00Pattern, hostname):
            BaseTemplateFile = template_path_legacy
            site_switch_Type = 'BRANCH_IDF_X00'
        elif re.findall(branchIDFXXXPattern, hostname):
            BaseTemplateFile = template_path_legacy
            site_switch_Type = 'BRANCH_IDF_XXX'
        #3850
        elif re.findall(hqIDF1000Pattern, hostname):
            BaseTemplateFile = template_path
            site_switch_Type = 'HQ_IDF_1000'
        elif re.findall(hqIDF10XXPattern, hostname):
            BaseTemplateFile = template_path
            site_switch_Type = 'HQ_IDF_10XX'
        elif re.findall(branchIDFX000Pattern, hostname):
            BaseTemplateFile = template_path
            site_switch_Type = 'BRANCH_IDF_X000'
        elif re.findall(branchIDFX0XXPattern, hostname):
            BaseTemplateFile = template_path
            site_switch_Type = 'BRANCH_IDF_X0XX'
        else: # catch any other non-standard name.
            BaseTemplateFile = template_path
            site_switch_Type = 'CANNOT DETERMINE'

    ### ------------------------------------create config file and folder---------------------------------###
    #create path based on district if it doesn't exist
    #the r before the string means (raw string literal) so backslashes will not be treated as escape characters
    #which mitigates issues with things like regex but this is rarely needed anyway
        newpath = main_directory + r'All_District_Configuration_Files\%s\%s' %(district, site)
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    #create config file
        ConfigFile = main_directory + r'All_District_Configuration_Files\%s\%s\%s-CONFIG.txt' %(district, site, hostname)

    # try to remove the configuration file - if it doesn't exist, create it
        try:
            os.remove(ConfigFile)

        except FileNotFoundError:
            pass
        #print(" Old Configuration file does not exist. Will now create a new one. Location: " + ConfigFile)

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

        with open(BaseTemplateFile, 'r') as BaseTemplate:
            lines = BaseTemplate.readlines()
            with open(ConfigFile, 'w') as f:
                f.writelines(lines)

        # start domain name configuration #
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$domainNameCmd', domainNameCmd)
            f.write(filedata)
        # end start domain name configuration #

        # start hostname configuration #
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$hostnameCmd', hostnameCmd)
            f.write(filedata)
        # end start hostname configuration #

        # start ip address configuration #
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$ipAddressCmd', ipAddressCmd)
            f.write(filedata)
        # end ip address configuration #

        # start default gateway configuration #
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
        with open(ConfigFile, 'r+') as f:
            filedata = filedata.replace('$defaultGatewayCmd', defaultGatewayCmd)
            f.write(filedata)
        # end default gateway configuration #

        # start timezone configuration
        # timezones without summer time = AKST, AST, HST, AZST, CHST
        # timezones with summertime = CST, EST, MST, PST
        with open(ConfigFile, 'r') as f:
            filedata = f.read()
            if timezone == 'AST': # atlantic time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneASTCmd)
                    f.write(filedata)
            elif timezone == 'EST': # eastern time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneESTCmd)
                    f.write(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneSummerCmd', timezoneEDT)
                    f.write(filedata)
            elif timezone == 'CST': # central time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneCSTCmd)
                    f.write(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneSummerCmd', timezoneCDT)
                    f.write(filedata)
            elif timezone == 'MST': # mountain time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneMSTCmd)
                    f.write(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneSummerCmd', timezoneMDT)
                    f.write(filedata)
            elif timezone == 'PST': # pacific time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezonePSTCmd)
                    f.write(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneSummerCmd', timezonePDT)
                    f.write(filedata)
            elif timezone == 'AKST': # alaska time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneAKSTCmd)
                    f.write(filedata)
            elif timezone == 'HST': # hawaii time
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneHSTCmd)
                    f.write(filedata)
            elif timezone == 'CHST': # chamorro standard time (guam)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneCHSTCmd)
                    f.write(filedata)
            elif timezone == 'AZST': #arizona
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$timezoneCmd', timezoneAZSTCmd)
                    f.write(filedata)
            # end timezone configuration

        #start snmp location configuration

        if physicalLocation != '':
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$physicalLocationCmd', physicalLocationCmd)
                f.write(filedata)
        elif physicalLocation == '': #if there's no location, put [District] <Site>
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$physicalLocationCmd', physicalLocationCmd2)
                f.write(filedata)
        #end snmp location configuration

        #start ntp/tacacs configuration

        if ntpTacacs == 'EAST':
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$ntpCmd', ntpEastCmd)
                f.write(filedata)
            if BaseTemplateFile == template_path: # for 3850
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$tacacsCmd', tacacsEastCmd)
                    f.write(filedata)
            elif BaseTemplateFile == template_path_legacy: # for 3750X
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$tacacsCmd', tacacsEast3750XCmd)
                    f.write(filedata)

        elif ntpTacacs == 'WEST':
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$ntpCmd', ntpWestCmd)
                f.write(filedata)
            if BaseTemplateFile == template_path: # for 3850
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$tacacsCmd', tacacsEastCmd)
                    f.write(filedata)
            elif BaseTemplateFile == template_path_legacy: # for 3750X
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$tacacsCmd', tacacsWest3750XCmd)
                    f.write(filedata)
        #end ntp/tacacs configuraiton

        ###------------------start Switch1-----------------------###

        if switch1 != '':
            switch1ProvisionCmd = 'switch 1 provision ' + switch1
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch1ProvisionCmd', switch1ProvisionCmd)
                f.write(filedata)

            if switch1 == 'ws-c3850-24t' or switch1 == 'ws-c3850-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch1PortCfg24', switch1PortCfg24)
                    f.write(filedata)

            elif switch1 == 'ws-c3750x-24p': # for 3750X
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch13750XPortCfg24', switch13750XPortCfg24)
                    f.write(filedata)

            elif switch1 == 'ws-c3850-48t' or switch1 == 'ws-c3850-48p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch1PortCfg48', switch1PortCfg48)
                    f.write(filedata)

            elif switch1 == 'ws-c3750x-48p': # for 3750X
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch13750XPortCfg48', switch13750XPortCfg48)
                    f.write(filedata)

        ###------------------end Switch1-----------------------###

        ###------------------start Switch2-----------------------###

        if switch2 != '':
            switch2ProvisionCmd = 'switch 2 provision ' + switch2
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch2ProvisionCmd', switch2ProvisionCmd)
                f.write(filedata)

            if switch2 == 'ws-c3850-24t' or switch2 == 'ws-c3850-24p' or switch2 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch2PortCfg24', switch2PortCfg24)
                    f.write(filedata)

            elif switch2 == 'ws-c3850-48t' or switch2 == 'ws-c3850-48p' or switch2 == 'ws-c3750x-48p' :
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch3ProvisionCmd', switch3ProvisionCmd)
                f.write(filedata)

            if switch3 == 'ws-c3850-24t' or switch3 == 'ws-c3850-24p' or switch3 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch3PortCfg24', switch3PortCfg24)
                    f.write(filedata)

            elif switch3 == 'ws-c3850-48t' or switch3 == 'ws-c3850-48p' or switch3 == 'ws-c3750x-48p':
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch4ProvisionCmd', switch4ProvisionCmd)
                f.write(filedata)

            if switch4 == 'ws-c3850-24t' or switch4 == 'ws-c3850-24p' or switch4 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch4PortCfg24', switch4PortCfg24)
                    f.write(filedata)

            elif switch4 == 'ws-c3850-48t' or switch4 == 'ws-c3850-48p' or switch4 == 'ws-c3750x-48p':
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch5ProvisionCmd', switch5ProvisionCmd)
                f.write(filedata)

            if switch5 == 'ws-c3850-24t' or switch5 == 'ws-c3850-24p' or switch5 == 'ws-c3750x-24p' :
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch5PortCfg24', switch5PortCfg24)
                    f.write(filedata)

            elif switch5 == 'ws-c3850-48t' or switch5 == 'ws-c3850-48p' or switch5 == 'ws-c3750x-48p' :
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch6ProvisionCmd', switch6ProvisionCmd)
                f.write(filedata)

            if switch6 == 'ws-c3850-24t' or switch6.lower() == 'ws-c3850-24p' or switch6 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch6PortCfg24', switch6PortCfg24)
                    f.write(filedata)

            elif switch6 == 'ws-c3850-48t' or switch6.lower() == 'ws-c3850-48p' or switch6 == 'ws-c3750x-48p':
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch7ProvisionCmd', switch7ProvisionCmd)
                f.write(filedata)

            if switch7 == 'ws-c3850-24t' or switch7 == 'ws-c3850-24p' or switch7 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch7PortCfg24', switch7PortCfg24)
                    f.write(filedata)

            elif switch7 == 'ws-c3850-48t' or switch7 == 'ws-c3850-48p' or switch7 == 'ws-c3750x-48p':
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch8ProvisionCmd', switch8ProvisionCmd)
                f.write(filedata)

            if switch8 == 'ws-c3850-24t' or switch8 == 'ws-c3850-24p'  or switch8 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch8PortCfg24', switch8PortCfg24)
                    f.write(filedata)

            elif switch8 == 'ws-c3850-48t' or switch8 == 'ws-c3850-48p'  or switch8 == 'ws-c3750x-48p':
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
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$switch9ProvisionCmd', switch9ProvisionCmd)
                f.write(filedata)

            if switch9 == 'ws-c3850-24t' or switch9 == 'ws-c3850-24p'  or switch9 == 'ws-c3750x-24p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch9PortCfg24', switch9PortCfg24)
                    f.write(filedata)

            elif switch9 == 'ws-c3850-48t' or switch9 == 'ws-c3850-48p' or switch9 == 'ws-c3750x-48p':
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$switch9PortCfg48', switch9PortCfg48)
                    f.write(filedata)
        ###------------------end Switch9-----------------------###

        #specific port reservations for sites, hq/branch

        if site_switch_Type == 'HQ_IDF_1000': # run this code only if switch is HQ IDF1000
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$hqPktSmtIDF1000Cmd', hqPktSmtIDF1000Cmd)
                f.writelines(filedata)
            if evoipFaxAnalogGateways == 2: #provision evoip port if needed
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$hqEvoipFaxGateway2IDF1000Cmd', hqEvoipFaxGateway2IDF1000Cmd)
                    f.writelines(filedata)
            if evoipUPS == 2: # provision another UPS mgmt port if needed
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$hqEvoipUpsMgmt2IDF1000Cmd', hqEvoipUpsMgmt2IDF1000Cmd)
                    f.writelines(filedata)
            if taclanes == 1: # provision 1 taclane device
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$hqTaclane1IDF1000Cmd', hqTaclane1IDF1000Cmd)
                    f.writelines(filedata)
            elif taclanes == 2: # provision 2 taclane devices
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$hqTaclane1IDF1000Cmd', hqTaclane1IDF1000Cmd)
                    f.writelines(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$hqTaclane2IDF1000Cmd', hqTaclane2IDF1000Cmd)
                    f.writelines(filedata)

        elif site_switch_Type == 'HQ_IDF_10XX': # run this code only if switch is located at an Branch Site
            if evoipUPS == 2: # evoip ups mgmt for branch IDF10XX
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$hqEvoipUpsMgmt2IDF10XXCmd', hqEvoipUpsMgmt2IDF10XXCmd)
                    f.writelines(filedata)
            if taclanes == 1: # provision server virt UPS port, IPMI port, and ILO port
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f: #provision server virt UPS port
                    filedata = filedata.replace('$hqTaclane1IDF10XXCmd', hqTaclane1IDF10XXCmd)
                    f.writelines(filedata)
            elif taclanes == 2: # provision server virt UPS port, IPMI port, and ILO port
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f: #provision server virt UPS port
                    filedata = filedata.replace('$hqTaclane1IDF10XXCmd', hqTaclane1IDF10XXCmd)
                    f.writelines(filedata)
                with open(ConfigFile, 'r+') as f: #provision server virt UPS port
                    filedata = filedata.replace('$hqTaclane2IDF10XXCmd', hqTaclane2IDF10XXCmd)
                    f.writelines(filedata)

        elif site_switch_Type == 'BRANCH_IDF_X000': # run this code only if switch is located at an Branch Site
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$branchPktSmtIDFX000Cmd', branchPktSmtIDFX000Cmd)
                f.writelines(filedata)
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f: #always run this code if it's a branch site
                filedata = filedata.replace('$branchSTTDUpsIDFX000Cmd', branchSTTDUpsIDFX000Cmd)
                f.writelines(filedata)
            if branchServerVirtSite == 1: # if server virt exists, provision 3 ports, server virt ups, data domain ilo, scmh21 ilo
                with open(ConfigFile, 'r+') as f: # provision a data domain IPMI port
                    filedata = filedata.replace('$branchServerVirtUpsIDFX000Cmd', branchServerVirtUpsIDFX000Cmd)
                    f.writelines(filedata)
                with open(ConfigFile, 'r+') as f: # provision SVMH ILO port
                    filedata = filedata.replace('$branchDatadomainIpmiIDFX000Cmd', branchDatadomainIpmiIDFX000Cmd)
                    f.writelines(filedata)
                with open(ConfigFile, 'r+') as f: #provision svmh ilo port
                    filedata = filedata.replace('$branchSvmh21Green1ILOIDFX000Cmd', branchSvmh21Green1ILOIDFX000Cmd)
                    f.writelines(filedata)
            if panzura_iDRAC_ILO == 1: # panzura for branch IDFX000
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchPanzuraILOIDFX000Cmd', branchPanzuraILOIDFX000Cmd)
                    f.writelines(filedata)
            if evoipFaxAnalogGateways == 2: # # analog fax gateway for branch IDFX000
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchEvoipFaxGateway2IDFX000Cmd', branchEvoipFaxGateway2IDFX000Cmd)
                    f.writelines(filedata)
            if evoipUPS == 2: # evoip ups mgmt #2 for branch IDFX000
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchEvoipUpsMgmt2IDFX000Cmd', branchEvoipUpsMgmt2IDFX000Cmd)
                    f.writelines(filedata)
            if oconusTapeLibrary == 1: # ocunus tape library for branch IDFX000
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchOconusMgmtCmdIDFX000', branchOconusMgmtCmdIDFX000)
                    f.writelines(filedata)
            if taclanes == 1: # taclane 1 for branch IDFX000
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchTaclane1IDFX000Cmd', branchTaclane1IDFX000Cmd)
                    f.writelines(filedata)
            elif taclanes == 2: # taclane 1 and 2 for branch IDFX000
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchTaclane1IDFX000Cmd', branchTaclane1IDFX000Cmd)
                    f.writelines(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchTaclane2IDFX000Cmd', branchTaclane2IDFX000Cmd)
                    f.writelines(filedata)

        elif site_switch_Type == 'BRANCH_IDF_X0XX': # run this code only if switch is located at an Branch Site
            if evoipUPS == 2: # evoip ups mgmt # 2  for IDFX0XX
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchEvoipUpsMgmt2IDFX0XXCmd', branchEvoipUpsMgmt2IDFX0XXCmd)
                    f.writelines(filedata)
            if taclanes == 1: # 1 taclane port for branch IDFX0XX
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchTaclane1IDFX0XXCmd', branchTaclane1IDFX0XXCmd)
                    f.writelines(filedata)
            elif taclanes == 2: # 2 taclane ports for branch IDFX0XX
                with open(ConfigFile, 'r') as f:
                    filedata = f.read()
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchTaclane1IDFX0XXCmd', branchTaclane1IDFX0XXCmd)
                    f.writelines(filedata)
                with open(ConfigFile, 'r+') as f:
                    filedata = filedata.replace('$branchTaclane2IDFX0XXCmd', branchTaclane2IDFX0XXCmd)
                    f.writelines(filedata)

        # Configure gi1/1/2 uplink desc if split stack switch #
        if splitStack == 1:
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$splitStackCmd', splitStackCmd)
                f.write(filedata)

        # start aruba rap function
        # this allows user to enter the switch number of the switch to have the RAPs provisoned, the program will figure out
        #how many ports the switch has by looking at the data in the switch1,2,3,etc fields

        def provisionRAPPortsSwitch1():
            '''Provision RAP ports for a one switch stack. If there's only one PoE switch, and it's a RAP site, provision last ports on switch'''
            rapPortCnt = str(portCount - remoteArubaDevices + 1)
            rapPortRangeCmd = ('int range gi' + '1' + '/' + '0/' + rapPortCnt + '-' + str(portCount))
            rapPortCfgCmd = rapPortRangeCmd + rapCfgCmd
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$arubaRapCmd', rapPortCfgCmd)
                f.write(filedata)

        def provisionRAPPorts(switchNumber):
            '''provision rap ports for a multiple switch stack (poe)'''
            rapPortCfgCmd = 'int range gi' + switchNumber + '/' + '0/' + '1' + '-'+ str(remoteArubaDevices) + rapCfgCmd
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$arubaRapCmd', rapPortCfgCmd)
                f.write(filedata)

        #Start Aruba RAP configuration to cfg file
        #aruba raps are optional so try/catch cause is used
        try: #check each switch for PoE model. Start from last switch first, provision on first switch to be PoE.
             # stops at switch 2 because switch 1 will have reserved ports. In that case it will provision from 48 down
            remoteArubaDevices = convertToZeroIfEmpty(remoteArubaDevices) #create variable if number of aruba rap devices is entered
            if switch2 and remoteArubaDevices != 0: #only execute if there's more than 1 switch in the stack and if it is a RAP site
                if switch9 == 'ws-c3850-24p' or switch9 == 'ws-c3850-48p':
                    provisionRAPPorts('9')
                elif switch8 == 'ws-c3850-24p' or switch8 == 'ws-c3850-48p':
                    provisionRAPPorts('8')
                elif switch7 == 'ws-c3850-24p' or switch7 == 'ws-c3850-48p':
                    provisionRAPPorts('7')
                elif switch6 == 'ws-c3850-24p' or switch6 == 'ws-c3850-48p':
                    provisionRAPPorts('6')
                elif switch5 == 'ws-c3850-24p' or switch5 == 'ws-c3850-48p':
                    provisionRAPPorts('5')
                elif switch4 == 'ws-c3850-24p' or switch4 == 'ws-c3850-48p':
                    provisionRAPPorts('4')
                elif switch3 == 'ws-c3850-24p' or switch3 == 'ws-c3850-48p':
                    provisionRAPPorts('3')
                elif switch2 == 'ws-c3850-24p' or switch2 == 'ws-c3850-48p':
                    provisionRAPPorts('2')
            elif switch2 == None or switch2 == '' and remoteArubaDevices !=0: #if there is only one switch in stack, execute following code
                if switch1 == 'ws-c3850-24t' or switch1 == 'ws-c3850-24p':
                    portCount = 24
                    provisionRAPPortsSwitch1()
                elif switch1 == 'ws-c3850-48t' or switch1 == 'ws-c3850-48p':
                    portCount = 48
                    provisionRAPPortsSwitch1()
        except NameError:
            pass
        except TypeError:
            pass

        ##End Aruba RAP configuration to cfg file##

         # if there are 2 switches in power stack, switch 1 and switch 2 in same power stack domain
        # if there are 3 switches in power stack, switch 1, switch 2, and switch 3 are in same power stack domain
        # if there are 4 switches in power stack, switch 1,2,3,4 are in same power stack domain
        # if there are 5 switches in power stack, switch 1,2,3 are in same domain and switch 4 and 5 in same domain
        # if there are 6 switches in power stack, switch 1,2,3 in same domain, switch 4,5,6 in same domain
        # if there are 7 switches in power stack, switch 1,2,3,4 in same domain, switch 1,2 in same domain
        # if there are 9 switches in power stack, switch 1,2,3 in same domain. switch 4,5,6 in same, switch 7,8,9 in same
        switch_count = 0 #start counter at 0
        switch1 = 'switch1' # need this in powerstack code below so switch1 is always true
        switch_list_1_two = [switch1, switch2]
        switch_list_2_two = [switch4, switch5]
        switch_list_1_three = [switch1, switch2, switch3]
        switch_list_2_three = [switch4, switch5, switch6]
        switch_list_3_three = [switch7, switch8, switch9]
        switch_list_4_three = [switch5, switch6, switch7]
        switch_list_1_four = [switch1, switch2, switch3, switch4]
        switch_list_2_four = [switch5, switch6, switch7, switch8]
        switch_list_all = [switch1, switch2, switch3, switch4, switch5, switch6, switch7, switch8, switch9]
        switch_num = 1


        def powerstackConfig(x,y,z):
            '''power stack config: x = switch #, y = index 0 of power stack group list, z = power stack group list to use'''
            powerStackCmd = \
            'stack-power switch %s \n' %(str(x)) + \
            ' power-priority switch %s \n' %(str(y))+ \
            ' stack POWERSTACK'
            with open(ConfigFile, 'r') as f:
                filedata = f.read()
            with open(ConfigFile, 'r+') as f:
                filedata = filedata.replace('$powerstack%sswitchesCmd' %(cnt), powerStackCmd)
                f.writelines(filedata)
            z.remove(z[0])

        # count switches in stack
        for switch in switch_list_all:
            if switch != '':
                switch_count += 1

        #based on the number of switches in the stack - run code. Each block has different pwr stack groups to count from
        if switch_count == 1:
            cnt = 1
            ps1_one = [1]
            for switch in switch_list_1_two:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_one[0],ps1_one)
        elif switch_count == 2:
            cnt = 1
            ps1_two = [1,2]
            for switch in switch_list_1_two:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_two[0],ps1_two)
                    cnt += 1
                    switch_num += 1
                elif switch == switch2:
                    powerstackConfig(switch_num,ps1_two[0],ps1_two)
        elif switch_count == 3:
            cnt = 1
            ps1_three = [1,2,3]
            # if all switches are non-poe, don't reverse first non-poe you see after switch 1
            if all( switch is switch != 'ws-c3850-24p' or switch != 'ws-c3850-48p' for switch in switch_list_all):
                for switch in switch_list_1_three:
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt += 1
                    switch_num += 1
            else:
                for switch in switch_list_1_three:
                    if switch == 'switch1': #always assign switch 1 power priority 1
                        powerstackConfig(switch_num,ps1_three[0],ps1_three)
                        cnt += 1
                        switch_num += 1
                    elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                        ps1_three.reverse()
                        powerstackConfig(switch_num,ps1_three[0],ps1_three)
                        ps1_three.reverse()
                        cnt += 1
                        switch_num += 1
                    elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                        powerstackConfig(switch_num,ps1_three[0],ps1_three)
                        cnt += 1
                        switch_num += 1
        elif switch_count == 4:
            cnt = 1
            ps1_four = [1,2,3,4]
            for switch in switch_list_1_four:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps1_four.reverse()
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    ps1_four.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    cnt +=1
                    switch_num += 1
        elif switch_count == 5:
            cnt = 1
            ps1_three = [1,2,3]
            ps1_two = [1,2]
            for switch in switch_list_1_three:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t': # assign highest number in list to non poe
                    ps1_three.reverse()
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    ps1_three.reverse()
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p': # from left to right, assign lowest num in list to poe
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt +=1
                    switch_num += 1
            for switch in switch_list_2_two: # apply the same logic to the second set of switches in power stack
                if switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps1_two.reverse()
                    powerstackConfig(switch_num,ps1_two[0],ps1_two)
                    ps1_two.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps1_two[0],ps1_two)
                    cnt +=1
                    switch_num += 1
        elif switch_count == 6:
            cnt = 1
            ps1_three = [1,2,3]
            ps2_three = [1,2,3]
            '''
            # if all switches are non-poe, don't reverse first non-poe you see after switch 1, this is mainly for LTSC
            if all( switch is switch != 'ws-c3850-24p' or switch != 'ws-c3850-48p' for switch in switch_list_all):
                for switch in switch_list_1_three:
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt += 1
                    switch_num += 1
                for switch in switch_list_2_three:
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    cnt += 1
                    switch_num += 1
            '''
            for switch in switch_list_1_three:
                if switch == 'switch1':
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps1_three.reverse()
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    ps1_three.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt +=1
                    switch_num += 1
            for switch in switch_list_2_three:
                if switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps2_three.reverse()
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    ps2_three.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    cnt +=1
                    switch_num += 1
        elif switch_count == 7:
            cnt = 1
            ps1_four = [1,2,3,4]
            ps2_three = [1,2,3]
            for switch in switch_list_1_four:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps1_four.reverse()
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    ps1_four.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    cnt +=1
                    switch_num += 1
            for switch in switch_list_4_three:
                if switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps2_three.reverse()
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    ps2_three.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    cnt +=1
                    switch_num += 1
        elif switch_count == 8:
            cnt = 1
            ps1_four = [1,2,3,4]
            ps2_four = [1,2,3,4]
            for switch in switch_list_1_four:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps1_four.reverse()
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    ps1_four.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps1_four[0],ps1_four)
                    cnt +=1
                    switch_num += 1
            for switch in switch_list_2_four:
                if switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps2_four.reverse()
                    powerstackConfig(switch_num,ps2_four[0],ps2_four)
                    ps2_four.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps2_four[0],ps2_four)
                    cnt +=1
                    switch_num += 1
        elif switch_count == 9:
            cnt = 1
            ps1_three = [1,2,3]
            ps2_three = [1,2,3]
            ps3_three = [1,2,3]
            for switch in switch_list_1_three:
                if switch == 'switch1': #always assign switch 1 power priority 1
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt += 1
                    switch_num += 1
                elif switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps1_three.reverse()
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    ps1_three.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps1_three[0],ps1_three)
                    cnt +=1
                    switch_num += 1
            for switch in switch_list_2_three:
                if switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps2_three.reverse()
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    ps2_three.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps2_three[0],ps2_three)
                    cnt +=1
                    switch_num += 1
            for switch in switch_list_3_three:
                if switch == 'ws-c3850-24t' or switch == 'ws-c3850-48t':
                    ps3_three.reverse()
                    powerstackConfig(switch_num,ps3_three[0],ps3_three)
                    ps3_three.reverse()
                    cnt +=1
                    switch_num += 1
                elif switch == 'ws-c3850-24p' or switch == 'ws-c3850-48p':
                    powerstackConfig(switch_num,ps3_three[0],ps3_three)
                    cnt +=1
                    switch_num += 1

        # additional 3750X specific config goes here

        #start cleanup
        pattern = re.compile(r"^\$.*") #search for using regex. the parenthesis is for a 'group' and the \$ is so
        # special characters can be read 'as is'. the . says look for any character, and the * says look at the preceding
        # character, and allow that character to repeat itself. ^ carrot says from start of a string since the character is
        # a . (essentially a wildcard), then all characters can be allowed. The variables in the text file
        # are $<variable_name>

        with open(ConfigFile) as f:
            filedata = f.read()
        with open(ConfigFile, 'r') as f:
            for i, line in enumerate(f): #same as a for i in range command, and it's going to iterate each line in config file.
                for match in re.finditer(pattern, line): # python regex has a built in iterater that takes multiple input
                    with open(ConfigFile, 'r+') as f:
                        filedata = filedata.replace(match.group(), '%--------------------------------------%')
                        # match.group() needs to
                        # be used  because this displays what the search found for matches. Then it's replaced with a bunch
                        # of blank spaces
                        f.write(filedata)


        with open(ConfigFile) as f: #remove extra exclamation points with whitespace after regex removal
            all_lines = f.readlines()
        with open(ConfigFile, 'w') as f:
            for line in all_lines:
                if line != '%--------------------------------------%' + '\n':
                    f.write(line)
        #end cleanup

        # print information for user here
        print('Hostname: %s [%s]' %(hostname, site_switch_Type))
        print('District: %s' %(district))
        print('Site: %s' %(site))
        print('Number of Switches in this Stack: %s' %(switch_count))

        # piggy back off regex code and check to see what template file it's using to determine model type
        if BaseTemplateFile == template_path_legacy: #if this template is being used it must be 3750X
            print('Model Type: 3750X')
        elif BaseTemplateFile == template_path: # if this template is being used it must be 3850
            print('Model Type: 3850')

        if splitStack == 1:
            print('This is a Split Stack')

        if remoteArubaDevices != 0:
            print('Number of Aruba RAP Devices: %s' %(remoteArubaDevices))

        print('Configuration has been successfully generated!')
        print('--------------------------------------------------------------------------------')


    elif fetch_data == []: # by defualt c.fetchall() will return an empty list if nothing is found in the database.
                           # if nothing is found in the database, run elif and exit program
        print('Hostname %s can\'t be found in database.' %(hostname))

#hostnameSearch()
#hostnameSearchDistrict('')