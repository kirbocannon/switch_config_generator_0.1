__author__ = 'Kenneth Buchanan'
from tkinter import *
import tkinter.messagebox as tkmsg
from switchConfigGenerator import hostnameSearchAutomatic #hostnameSearchDistrict #import all function/variables from main config generator py file
from csvImporter import CreateNewTable, ImportDataFromCSV
from datetime import datetime
from threading import Thread
import sys

main_directory = r'\some\directory'
version = '1.7'

welcome = \
r'''
------------------ Welcome to the Configuration Generator ----------------------

Please click 'Import CSV file into Database' to import new values.

Next, click 'Generate All Switch Configrations Now' to start generating all switch configurations. For more detailed instructions, please take a look at the following file:


--------------------------------------------------------------------------------
'''


def date_and_time():
    '''grabs and formats current date & time'''
    time = datetime.now()
    date_now = '%s:%s:%s %s/%s/%s' %(time.hour, time.minute, time.second, time.month, time.day, time.year)
    return str((date_now))


class MainWindow: # Create gui and all buttons

    def __init__(self, master): #gets called automatically when you create an object "master" means root/main window. init__ will say, whenever you create object from this class, create master window
        '''formatting for a windows platform'''
        frame = Frame(master, width=100, height=100, pady=20)
        frame.grid()
        master.minsize(width=830, height=650)
        master.maxsize(width=830, height=650)
        self.cv = Canvas(width=200, height=200)
        #create menu navigation
        self.menubar = Menu(master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        #self.filemenu.add_command(label="Generate Config By Specific District", command=configByDistrictWindow.runGenerateDistrictConfig)
        self.filemenu.add_command(label="Exit", command=self.quitApp)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About..", command=self.runAboutMessageBox1)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        #create logo
        self.photo = PhotoImage(file= main_directory + r"Graphics\sealRe1.gif")
        self.cv.create_image(120, 120, image=self.photo)
        self.cv.place(bordermode=OUTSIDE, x=555, y = -30)
        #create main buttons
        self.importCSVButton1 = Button(frame, fg='green', text = "Step 1 --> Import CSV file into Database", \
                                       command=self.runImportCSV, activebackground='yellow', height = 3)
        self.importCSVButton1.grid()

        self.generateAllButton2 = Button(frame, fg='red', text = "Step 2 --> Generate All Switch Configurations Now \n "
                                                                 "(This may take several minutes!)",
                                         command=self.runSwitch, activebackground='yellow', height = 3)
        self.generateAllButton2.grid()

        self.quitButton3 = Button(frame, text = "      Exit      ", command=self.quitApp, activebackground='yellow', height = 3)
        self.quitButton3.grid()
        #Create status text
        self.label1 = Label(master, text='Details:')
        self.label1.grid()
        #create textbox for logging
        self.textbox=Text(root, height=20, width=80, relief='ridge', state = 'normal') #groove #flat #raised #soild #sunken
        self.textbox.grid(padx=(80, 100), row=4, column=0)
        self.textboxScrollbar = Scrollbar(master, command=self.textbox.yview, orient='vertical')
        self.textboxScrollbar.place(bordermode =OUTSIDE, height=330, width=300, x=440, y=225)
        self.textboxScrollbar.configure(command = self.textbox.yview)
        self.textbox.configure(yscrollcommand=self.textboxScrollbar.set)
        self.cnt = 0 #counter used for auto scrolling in textbox


    def redirector(self, inputStr): #redirector method
        '''redirect stdout (output messages) to the details box in the GUI'''
        self.textbox.insert(INSERT, inputStr)
        if self.cnt > 1: #only scroll after first text input is placed in textbox
            self.textbox.yview(END) #scroll to end each time output is displayed
        self.cnt += 1


    def runSwitchConfigurator(self):
        '''run the switch generator function - from the switchConfigGenerator file'''
        self.textbox['state'] = NORMAL
        self.label1.config(text='The Configuration Generator is now running. Creating all IDF configurations. @ ' + date_and_time())
        hostnameSearchAutomatic()
        self.label1.config(text='All Switch Configurations have been created @ ' + date_and_time())
        print('Finished task at ' + date_and_time())
        self.textbox.yview(END) #set scrollbar to end
        self.textbox['state'] = DISABLED

    def runImportCSV(self):
        '''This function uses csvImporter.py to remove/update/add table elements from a csv file'''
        self.textbox['state'] = NORMAL
        print('--------------------------------------------------------------------------------')
        CreateNewTable()
        ImportDataFromCSV()


        self.label1.config(text='CSV values have been uploaded into Database @ ' + date_and_time())
        print('Finished task at ' + date_and_time())
        self.textbox.yview(END) #set scrollbar to end
        self.textbox['state'] = DISABLED

    def quitApp(self):
        '''quit application'''
        exit()

    def runAboutMessageBox1(self):
        '''about message box'''
        about ='''
        Switch Configuration Generator %s
        Project: Switch Stack Replacement 2016
        Developer: Kenneth Buchanan ''' %(version)

        tkmsg.showinfo('About', about)

    def printTextVariable(self, x):
        print(x)

    def donothing(self):
        '''for testing button functionality'''
        pass

    def runSwitch(self):
        '''run configuration generator with multiple another thread for user responsiveness'''
        t = Thread(target=self.runSwitchConfigurator) #separate thread for database reading
        t.start()

'''
class configByDistrictWindow:
    def __init__(self,master):
        #window for config by district
        district_entry = StringVar()
        self.districtWindow = Toplevel(master=root)
        self.label1 = Label(self.districtWindow, text = 'Enter District: ')
        self.entry1 = Entry(self.districtWindow, width = 15, textvariable = district_entry)
        self.button1 = Button(self.districtWindow, text = "Generate Config", command=self.printTextVariable(district_entry), activebackground='yellow', height = 1)


    def runGenerateDistrictConfig(self):
        self.label1.pack(side='left')
        self.entry1.pack(side='left')
        self.button1.pack()

    def printTextVariable(self,x):
        pass
'''

if __name__ == '__main__':
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.title("Switch Configuration Generator v" + version)
    root.iconbitmap(main_directory + r"Graphics\computer.ico")
    c = MainWindow(root) #instanciate the class and put it in the root window
    root.config(menu=c.menubar)
    sys.stdout.write = c.redirector #whenever sys.stdout.write is called, redirector is called.
    print(welcome)
    root.mainloop()





