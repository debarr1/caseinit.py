#!/usr/bin/env python
#====================================================================================================
# Title         : caseInit.py
# Version       : 1.0
# Last Modified : 05/01/2017
# Author        : David Barr
# Purpose       : A simple GUI that takes a user input of four characters to form part of the case 
#                 reference in the format 05 DF 0000 17.  This input is tested robustly and the 
#                 preceeding and trailing characters are automatically generated.  The following
#                 folder structure is generated with the option to omit optional (*) folders;
#                     05 DF 0000 17
#                     +---Acqusitions
#                     +---Level 1
#                         +---Case Files
#                             +---Griffeye(*)
#                             +---(IEF)
#                             +---UFED PA(*)
#                             +---X-Ways(*)
#                         +---Exports
#                             +---Griffeye(*)
#                             +---IEF(*)
#                             +---UFED PA(*)
#                             +---X-Ways(*)
#                     +---Level 2
#                         +---Exports
#                         +---Reports
#                 The "05 DF 0000 17/Level 1/IEF" folder is omitted to reduce redundant layers as
#                 IEF generates a subfolder on case creation.
#
#                 This script checks for eligible drives upon starting and creates the above folder
#                 structure on the drive letter specified by the user in the GUI upon user action.
#
#                 The menu allows for saving the log as a text file and also archiving the case as
#                 a zip file (NOT COMPLETE - DO NOT USE).
#====================================================================================================

from tkinter import *
import os, string, datetime, time, shutil
from tkinter import filedialog




def createDirectory(targetPath):
    #Accepts the string targetPath which it will create unless it exists already.
    #If folder exists, flag the boolean value so the user will be informed of errors.
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
        logEntry("Created " + targetPath)
    else:
        logEntry("ERROR: " + targetPath + " already exists, skipping")
        global boolError
        boolError = True




def createFolders():
    #Clear the log of welcome information, checks the user input and returns if invalid.
    #Generate the paths of all the folders to be created and pass them to createDirectory.
    #Let the user know if an error was generated.
    clearLog()
    reference = entryReference.get()
    if len(reference) != 4:
        logEntry("ERROR: Reference number is not 4 characters", False)
        return
    if reference.isdigit() == False:
        logEntry("ERROR: Reference number is not valid, illegal character", False)
        return
    reference = "05 DF " + entryReference.get() + " " + refYear
    logEntry("Creating folders for " + reference)
    selectedDrive = listDrive.get(ACTIVE)
    rootFolderPath = selectedDrive + "/" + reference
    createDirectory(rootFolderPath)
    
    #Create mandaroty folders
    createDirectory(rootFolderPath + "/" + "Acqusitions")
    createDirectory(rootFolderPath + "/" + "Level 1")
    createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Case Files")
    createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Exports")
    createDirectory(rootFolderPath + "/" + "Level 2")
    createDirectory(rootFolderPath + "/" + "Level 2" + "/" + "Exports")
    createDirectory(rootFolderPath + "/" + "Level 2" + "/" + "Reports")
    
    #Create case file (optional folders)
    if varCheckCaseGriffeye.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Case Files" + "/" + "Griffeye")
    else:
        logEntry("Case Files/Griffeye not selected, therefore not created")
    logEntry("Case Files/IEF is created by IEF, therefore not created")
    if varCheckCaseUFEDPA.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Case Files" + "/" + "UFED PA")
    else:
        logEntry("Case Files/UFED PA not selected, therefore not created")
    if varCheckCaseXWays.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Case Files" + "/" + "X-Ways")
    else:
        logEntry("Case Files/XWays not selected, therefore not created")
    
    #Create export (optional folders)
    if varCheckExportsGriffeye.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Exports" + "/" + "Griffeye")
    else:
        logEntry("Exports/Griffeye not selected, therefore not created")
    if varCheckExportsIEF.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Exports" + "/" + "IEF")
    else:
        logEntry("Exports/Griffeye not selected, therefore not created")
    if varCheckExportsUFEDPA.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Exports" + "/" + "UFED PA")
    else:
        logEntry("Exports/UFED PA not selected, therefore not created")
    if varCheckExportsXWays.get() == 1:
        createDirectory(rootFolderPath + "/" + "Level 1" + "/" + "Exports" + "/" + "X-Ways")
    else:
        logEntry("Exports/XWays not selected, therefore not created")
    
    #Conclude operation, let user know!
    if boolError == True:
        logEntry("Operation completed with errors, see log entries above")
    else:
        logEntry("Operation completed")




def archiveCase():
    #########///NOT YET IMPLEMENTED
    caseRoot = filedialog.askdirectory()
    shutil.make_archive(caseRoot[-13:], "zip", caseRoot)




def logEntry(string, boolStamp=True):
    #Accepts a string to be written to the log and a boolean value which defaults to True.
    #When the boolean is true, HH:MM:SS.00 preceeds the string.
    #The text widgit is activated making it mutable and deactivated afterwards to prevent editing.
    textLog.config(state=NORMAL)
    if boolStamp == True:
        entry = str(datetime.datetime.today())[11:22] + " " + string + "\n"
    else:
        entry = string + "\n"
    textLog.insert(END, entry)
    textLog.config(state=DISABLED)




def saveLog():
    #Opens a save file dialogue to select target file to recive contents of textLog.
    #asksaveasfile will return "None" if dialog is closed with the "cancel" button.
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(textLog.get(1.0, END))
    f.write(text2save)
    f.close()




def clearLog():
    #The text widget is activated, cleared and then deactivated.
    textLog.config(state=NORMAL)
    textLog.delete(1.0,END)
    textLog.config(state=DISABLED)




def cancelExit():
    #Exits the program, required command
    exit()




title = "HTCU Case Folder Creator"
version = "Version 1.0, last updated 05/01/2017"
boolError = False

root = Tk()
root.title("HTCU Case Folder Creator")
root.minsize(width=500, height=700)
root.maxsize(width=500, height=700)

#Add a menu
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Save Log", command=saveLog)
subMenu.add_command(label="Clear Log", command=clearLog)
subMenu.add_separator()
subMenu.add_command(label="Archive Case", command=archiveCase)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=cancelExit)

#Add a atatus bar
currentStatus="Waiting for user..."
status = Label(root, text=currentStatus, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

#Organise 3 frames, top (title) middle (folders) and bottom (buttons)
titleFrame = Frame(root)
titleFrame.pack()
referenceFrame = Frame(root)
referenceFrame.pack()
foldersFrame = Frame (root)
foldersFrame.pack()
buttonFrame = Frame(root)
buttonFrame.pack(side=BOTTOM)

#Enter to first frame //not currently in use
#labelTitle = Label(titleFrame, text="HTCU Case Folder Creator")
#labelTitle.pack()

#Enter labels and checkboxes to second frame
refYear = str(datetime.datetime.now())[2:4]
label05DF = Label(referenceFrame, text="05 DF")
label05DF.grid(row=0, column=0, sticky=E)
entryReference = Entry(referenceFrame, justify=CENTER, width=6)
entryReference.grid(row=0, column=1)
entryReference.insert(END, "0000")
entryReference.focus_set()
labelYear = Label(referenceFrame, text=refYear)
labelYear.grid(row=0, column=2, sticky=W)

labelAcqusitions = Label(foldersFrame, text="Acqusitions")
labelAcqusitions.grid(row=0, column=0, sticky=W)

labelLevel1 = Label(foldersFrame, text="Level 1")
labelLevel1.grid(row=1, column=0, sticky=W)

labelL1CaseFiles = Label(foldersFrame, text="        Case Files")
labelL1CaseFiles.grid(row=2, column=0, sticky=W)

labelCaseGriffeye = Label(foldersFrame, text="                Griffeye")
labelCaseGriffeye.grid(row=3, column=0, sticky=W)
varCheckCaseGriffeye = IntVar()
checkCaseGriffeye = Checkbutton(foldersFrame, variable=varCheckCaseGriffeye)
checkCaseGriffeye.grid(row=3, column=1, sticky=W)
checkCaseGriffeye.select()

labelCaseIEF = Label(foldersFrame, text="                IEF")
labelCaseIEF.grid(row=4, column=0, sticky=W)
checkCaseIEF = Checkbutton(foldersFrame, state=DISABLED)
checkCaseIEF.grid(row=4, column=1, sticky=W)

labelCaseUFEDPA = Label(foldersFrame, text="                UFED PA")
labelCaseUFEDPA.grid(row=5, column=0, sticky=W)
varCheckCaseUFEDPA = IntVar()
checkCaseUFEDPA = Checkbutton(foldersFrame, variable=varCheckCaseUFEDPA)
checkCaseUFEDPA.grid(row=5, column=1, sticky=W)
checkCaseUFEDPA.select()

labelCaseXWays = Label(foldersFrame, text="                X-Ways")
labelCaseXWays.grid(row=6, column=0, sticky=W)
varCheckCaseXWays = IntVar()
checkCaseXWays = Checkbutton(foldersFrame, variable=varCheckCaseXWays)
checkCaseXWays.grid(row=6, column=1, sticky=W)
checkCaseXWays.select()

labelL1Exports = Label(foldersFrame, text="        Exports")
labelL1Exports.grid(row=7, column=0, sticky=W)

labelExportsGriffeye = Label(foldersFrame, text="                Griffeye")
labelExportsGriffeye.grid(row=8, column=0, sticky=W)
varCheckExportsGriffeye = IntVar()
checkExportsGriffeye = Checkbutton(foldersFrame, variable=varCheckExportsGriffeye)
checkExportsGriffeye.grid(row=8, column=1, sticky=W)
checkExportsGriffeye.select()

labelExportsIEF = Label(foldersFrame, text="                IEF")
labelExportsIEF.grid(row=9, column=0, sticky=W)
varCheckExportsIEF = IntVar()
checkExportsIEF = Checkbutton(foldersFrame, variable=varCheckExportsIEF)
checkExportsIEF.grid(row=9, column=1, sticky=W)
checkExportsIEF.select()

labelExportsUFEDPA = Label(foldersFrame, text="                UFED PA")
labelExportsUFEDPA.grid(row=10, column=0, sticky=W)
varCheckExportsUFEDPA = IntVar()
checkExportsUFEDPA = Checkbutton(foldersFrame, variable=varCheckExportsUFEDPA)
checkExportsUFEDPA.grid(row=10, column=1, sticky=W)
checkExportsUFEDPA.select()

labelExportsXWays = Label(foldersFrame, text="                X-Ways")
labelExportsXWays.grid(row=11, column=0, sticky=W)
varCheckExportsXWays = IntVar()
checkExportsXWays = Checkbutton(foldersFrame, variable=varCheckExportsXWays)
checkExportsXWays.grid(row=11, column=1, sticky=W)
checkExportsXWays.select()

labelLevel2 = Label(foldersFrame, text="Level 2")
labelLevel2.grid(row=12, column=0, sticky=W)

labelL2Exports = Label(foldersFrame, text="        Exports")
labelL2Exports.grid(row=13, column=0, sticky=W)

labelL2Reports = Label(foldersFrame, text="        Reports")
labelL2Reports.grid(row=14, column=0, sticky=W)

#Enter button to third frame
buttonCreate = Button(buttonFrame, text="Create...", command=createFolders)
buttonCreate.pack(side=RIGHT)

#Add a textbox to the bottom for logging
textLog = Text(root, font=("Courier",9))
textLog.pack()
textLog.config(state=DISABLED)

#Detect logical volumes
availableDrives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

#Drive select listbox
listDrive = Listbox(titleFrame, height=5, width=10)
listDrive.pack()
for item in availableDrives:
    listDrive.insert(END, item)
listDrive.selection_set(first=0)

#Output welcome information
logEntry(title, False)
logEntry(version, False)
logEntry("Detected logical volumes are: " + str(availableDrives).strip('[]'), False)

root.mainloop()
