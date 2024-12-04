"""
Language: Python 3

IDE: VS Code

HOW TO RUN: Navigate to where the python project and execute as python {projectname}.py, because python is an interpreted language, an external library is used to "compile" it for an executable.
    So you can either run the script or click on the executable. It was produced with a library called pyinstaller and ran with this command:
     python c:.users.rohan.appdata.local.packages.pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0.localcache.local-packages.python312.site-packages.pyinstaller. --onefile {projectA}.py
    Where the periods are forward slashes. (unicode parsing problem if leaving path in multi line comment)
Authors: Rohan Keenoy, Justin Macapanpan (from phase II)

Date: 10/24/2024

DATA STRUCTURES: A pandas dataframe is commonly used in scientific applications, it can be thought of as a N-d array,can have headers, and is structured as the csv is structured. 
    For this project using a dataframe is a no brainer. R has a similar structure. A dictionary is used to append to rows in a dataframe. This generated per row-entry.  An array called listOfDirectoryFiles is initalized as a class variable, this is a simple array that holds on to
    files to traverse. This is the structure called "L" in the specification.
    
General Flow: basically just opperates straight down the checks with a flag variable called "checkFailed" in the function OpenFilesAndCheck, if a check is failed , it calls a function to write to file that it failed, 
this does not happen on the exception of a warning though - it will just print a warning and set the flag back to 0, which is valid. It then continues. 

EXTERNAL files: Any file that is valid is used in the directory, generated a ValidityChecks.txt file.

External preperation: Because python is an interpreted language a software pyinstaller will be used to generate an executable. 
    
References:
    0.)Regex testing on : https://regex101.com/
    1.) Date checks: https://www.geeksforgeeks.org/python-validate-string-date-format/, 
    format reference https://pynative.com/python-datetime-format-strftime/
    2.) General Pandas referencing on documentation site: https://pandas.pydata.org/docs/getting_started/index.html
    
"""
import os
import pandas as pd
import re
import time
from datetime import datetime
class programA:
    #insantiation of class variables
    def __init__(self):
        self.introMessage = "---------Welcome to program Validity Checker of phase III. This program is for validating patterns in file names and checks the validity of file contents. ---------\n"
        #data strucutre "L per assignment document"
        self.listOfDirectoryFiles = []
        self.fileName = "ValidityChecks.txt"
        self.fileCreated = False
        self.fileCheck = pd.DataFrame()
        self.currentFile = ""
        self.currentLine = 3
        self.isValidToContinue = 0
        self.names =[]
        self.numOfIndvFiles = 0
        self.firstAndLast = {}
        #self.checkFailed = 0
    
        self.classDriver()
    #write to that file whatever is sent (successful, failure, warning messages, called from main program loop)
    def writeToValidityFile(self, toWrite):
        if self.fileCreated == True:
            with open(self.fileName, "a") as validCheck:
                validCheck.write(f"{toWrite} . \n")
    #create a file, will not create a new file everytiem with fileCreatede flag
    def createFile(self):
        if self.fileCreated == False:
            with open(self.fileName, "w") as  validCheck:
                self.fileCreated = True
    #initial format checking for each file in directory, checks the name and class columns
    def initialFormatCheck(self):
        if self.fileCheck.empty:
            self.writeToValidityFile(f"FILE {self.currentFile}: CSV is empty.")
            return 1
        elif self.fileCheck.shape[0] < 2 or self.fileCheck.shape[1] < 2:
            self.writeToValidityFile(f"FILE {self.currentFile}: Initial check for shape failed on line 0 or 1")
            return 1
        #A CHECK FOR THE FIRST LAST NAME
        elif pd.isna(self.fileCheck.iloc[0,0]) or pd.isna(self.fileCheck.iloc[0,1]) or  (self.fileCheck.iloc[0, 0] == False or self.fileCheck.iloc[0, 1] == False) :
            self.writeToValidityFile(f"FILE {self.currentFile}: Initial check for name failed on line 1")
            return 1
        #acheck for CLASS NAME
        elif pd.isna(self.fileCheck.iloc[1,0]) or self.fileCheck.iloc[1,0] != "CS 4500" :
            self.writeToValidityFile(f"FILE {self.currentFile}: Initial check for CLASS name failed on line 2")
            return 1
        else:
            return 0
    #check if there is aditional lines after the name and class name lines
    def checkForAdditionalLines(self):
        if self.fileCheck.shape[0] > 2:
            return 1
        return 0
    #https://www.geeksforgeeks.org/python-validate-string-date-format/
    #date check 
    def dateCheck(self, date):
        #format reference https://pynative.com/python-datetime-format-strftime/
        format = "%m/%d/%Y"
        isDateValid = True
        try:
            isDateValid = bool(datetime.strptime(date,format))
        except:
            isDateValid = False
                
        if isDateValid == False:
            return 1
        else:
            return 0
    #function to check for people involved column
    def checkPplInvolved(self,ppl):
        ppl = int(ppl)
        if ppl < 1 or ppl > 50:
            return 1
        else:
            return 0
    #activity code checking
    def checkActivityCode(self, activityCode):
        validCodes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D"]
        if str(activityCode) in validCodes:
            #print("Activity code valid")
            return 0
        else:
            return 1
    #note validity checking 
    def checkNote(self, activityCode, note):
        if activityCode == "D":
            if(len(note)< 1):
                return 1
        elif "," in note:
            return 1
        elif len(note) > 80:
            return 1
        else:
            return 0
    #name check for phase III    
    def checkNames(self):
        for file in self.listOfDirectoryFiles:
            df = pd.read_csv(file,header = None)
            #last name check
            lastName = df.iloc[0,0]
            #first name check
            firstName = df.iloc[0,1]
            if lastName not in self.firstAndLast:
                self.firstAndLast[lastName] = firstName
                print(f"LASTNAME: {lastName} FIRSTNAME: {firstName} LOADED into program")
            else:
                input(f"!!! Last name had been previously loaded into program. Name {lastName} loaded into dictionary previously. press enter to exit. . .")
                return 1
        return 0
    #this is used in phase III master for the other files to retrieve first and last names.
    def getNames(self):
        return self.firstAndLast    
                 
    #base check for fromat, this is the "main loop" basically if something fails, a flag is set and it breaks the flow 
    def openFilesAndCheck(self):
        print(self.listOfDirectoryFiles)
        #main loop for checking
        for file in self.listOfDirectoryFiles:
            checkedFailed = 0
            self.currentFile = file
            self.fileCheck = pd.read_csv(f"{file}",header = None, na_filter=False)
            print(self.fileCheck)
            self.createFile()
            #self.initialFormatCheck(fileCheck)
            #check initial format
            checkedFailed = self.initialFormatCheck()
            if checkedFailed == 1:
                continue
            #check if there are additional lines, if return 0 then it is just the header and is empty
            if (self.checkForAdditionalLines() < 1):
                # we are done checking so
                self.writeToValidityFile(f"FILE {self.currentFile}: Initial check for CLASS name failed line 2")
                continue
            #we can now iterate through the rows of the dataframe checking each column, it is assumed if we make it here that the file starts at row 3.
            for index, row in self.fileCheck.iloc[2:].iterrows():
                self.currentLine = index+1
                #date check
                date = row[0]
                checkedFailed = self.dateCheck( date)
                if checkedFailed == 1:
                    self.writeToValidityFile(f"FILE {self.currentFile}: check for date failed on line {self.currentLine}")
                    break
                #Justin BLOC
                timeCheck1 = row[1]
                timeCheck2 = row[2]
                try:
                    checkedFailed = self.timeCheck(timeCheck1, timeCheck2)
                    if checkedFailed ==1:
                        self.writeToValidityFile(f"FILE {self.currentFile}: time elapsed exceeds end of day on line {self.currentLine}")                        
                    #self.writeToValidityFile(f"FILE {self.currentFile}: TIME SUCCESS {self.currentLine}")
                except:
                    checkedFailed = 1
                    self.writeToValidityFile(f"FILE {self.currentFile}: time is not in HH:MM format on line {self.currentLine}")
                if checkedFailed == 1:
                    break
                
                #check if time elapsed is greater than 4 hours
                checkedFailed = self.overTimeCheck(timeCheck1, timeCheck2)
                if checkedFailed == 1:
                    self.writeToValidityFile(f"********WARNING****** FILE {self.currentFile}: time elapsed exceeds 4 hours on line {self.currentLine}. Scan was continued for other checks")
                    checkFailed = 0
                #END JUSTIN 
                pplInvolved = row[3]
                checkedFailed = self.checkPplInvolved(pplInvolved)
                if checkedFailed == 1:
                    self.writeToValidityFile(f"File {self.currentFile}: check for 3rd column, people invovled, failed on line {self.currentLine}")
                    break
                
                activityCode = row[4]
                checkedFailed = self.checkActivityCode(activityCode)
                if checkedFailed ==1:
                     self.writeToValidityFile(f"File {self.currentFile}: check for 4th column, activity code, failed on line {self.currentLine}")
                     break
                note = row[5]
                checkedFailed = self.checkNote(activityCode, note)
                if checkedFailed == 1:
                    self.writeToValidityFile(f"File {self.currentFile}: check for 5th column, activity code, failed on line {self.currentLine} This could be because other was selected as an activity code and no note was entered > 1 OR contains a comma OR is longer than 80 chars. ")
                    break
                
            if checkedFailed == 1:
                self.isValidToContinue = checkedFailed
                continue
            
            self.writeToValidityFile(f"FILE {self.currentFile}: SUCCESSFUL - Is a valid file.")
            
    #Justin Bloc   
    #time check for making sure they are valid
    def timeCheck(self, t1, t2):
        #This only checks it for the HH:MM:SS format and assume military time
        format = "%H:%M"
        
        if(  datetime.strptime(t2, format).hour < datetime.strptime(t1, format).hour ):
            return 1
        elif datetime.strptime(t2, format).hour == datetime.strptime(t1, format) and datetime.strptime(t2, format).minute < datetime.strptime(t1, format).minute:
            return 1
        else:
            return 0

    #Justin Bloc 2
    #This function checks if the elapsed time is greater than 4 hours, which is unacceptable according to the specifications
    def overTimeCheck(self, t1, t2):
        #This function assumes t2 > t1, so it is called chronologically after timeCheck which makes sure that t2 > t1
        #if(  (datetime.strptime(t2, format).hour +((datetime.strptime(t2, format).minute)/60)) - (datetime.strptime(t1, format).hour+((datetime.strptime(t1, format).minute)/60)) >4  ):
        format = "%H:%M"
        delta = (datetime.strptime(t2,format)-datetime.strptime(t1,format))
        if( delta.seconds/3600 >= 4  ):
            return 1
        else:
            return 0
    #End justin Block
    #checks directory
    #actually retrieves and checks files initially from directory
    def fileChecks(self):
        #modified my old regex from phase A, tested on regex101.com. 
        #posted the image for doc in server
        count = 0
        regPat = r"^[A-Za-z]+[lL][oO][gG]\.[cC][sS][vV]$"
        for file in os.listdir():
            if re.match(regPat,file):
                count +=1
                self.listOfDirectoryFiles.append(file)
        print(f"LENGTH {len(self.listOfDirectoryFiles)}")
        
        boolNameCheck = self.checkNames()
        if boolNameCheck > 0:
            input(f"There are more than 10 individuals in the directory files. Name check failed with {boolNameCheck}\nPress Enter to exit . . .")
            exit(1)
        if len(self.listOfDirectoryFiles) <= 1:
            #print("There are no valid files matching pattern: X (any capital letter) + [lL][oO][gG]\.[cC][sS][vV] \n EXITING.......")
            #had to put this in so when an executable is generated it doesn't quit extremely fast
            input("No files found fitting the specification. Less than one file Press enter to end program. . .")
            exit(1)
        if len(self.listOfDirectoryFiles) > 9:
            input("More than 10 individuals found in log files. Press enter to exit. . .")
            exit(1)
        print(f"Total valid file names found {count}\n With more than one file found, opening a new file called ValidityChecks.txt")
        if len(self.listOfDirectoryFiles)> 0:
            self.openFilesAndCheck()
        #sorta redundant, meh
        
    def didCheckFail(self):
        return self.isValidToContinue
    #just a bit of a driver that runs all this on instantaition of the class
    def classDriver(self):
        
        print(self.introMessage)
        input("Press enter key to continue....")
        self.fileChecks()
        input(f"Thank you for using Program A. Validity check logs are in file {self.fileName}. \n Press enter to Generate Reports.")
        
            

'''if __name__ == "__main__":
    programA()'''