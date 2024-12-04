"""
Language: Python 3

IDE: VS Code

HOW TO RUN: Navigate to where the python project and execute as python {projectname}.py, because python is an interpreted language, an external library is used to "compile" it for an executable.
    So you can either run the script or click on the executable. It was produced with a library called pyinstaller and ran with this command:
     python c:.users.rohan.appdata.local.packages.pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0.localcache.local-packages.python312.site-packages.pyinstaller. --onefile {projectA}.py
    Where the periods are forward slashes. (unicode parsing problem if leaving path in multi line comment)
Authors: Rohan Keenoy
Lead Programmer: Rohan Keenoy

Date: 10/24/2024

DATA STRUCTURES: A pandas dataframe is commonly used in scientific applications, it can be thought of as a N-d array,can have headers, and is structured as the csv is structured. 
    For this project using a dataframe is a no brainer. R has a similar structure. A dictionary is used to append to rows in a dataframe. This generated per row-entry.  An array called listOfDirectoryFiles is initalized as a class variable, this is a simple array that holds on to
    files to traverse. Dictionaries are used for checking distinct names. validity checker checks for phase I and phase II specification as well as phase III checks < 10, >1, and distinct names. 
    all programs were developed individually and are
    
General Flow: all programs were developed individually and are pieced together by a flag bool returned by validity checks. 

EXTERNAL files: Any file that is valid is used in the directory, generated a ValidityChecks.txt file.

External preperation: Because python is an interpreted language a software pyinstaller will be used to generate an executable. 
    
References:
    0.)Regex testing on : https://regex101.com/
    1.) Date checks: https://www.geeksforgeeks.org/python-validate-string-date-format/, 
    format reference https://pynative.com/python-datetime-format-strftime/
    2.) General Pandas referencing on documentation site: https://pandas.pydata.org/docs/getting_started/index.html
    
"""
import validityChecker
import report1
import Report2
import Report3
import report4
import report5 
import graphA
import GraphB
import graphc
'''driver of the programs, each program is individually ran since they were developed independently, some require class construction such as validity checker,
others are called by main function (invoked by this driver)'''
if __name__ == "__main__":
    valid = validityChecker.programA()
    isValid = valid.didCheckFail() 
    firstAndLastNameDict = valid.getNames()
    print(f"File loaded and processed for {firstAndLastNameDict}")
    #print(f'Is Valid: {isValid}')
    #valid will return 1 if the program is not valid per program A of phase II or for new checks including duplicate names in phase III.
    if (isValid == 0):
        input(f"Phase III:: Validity check logs are found in the directory. Files from file scan for validity are found in ValidityChecks.txt \n Press enter to Generate Reports. They all save to text files")
        input("Press Enter to generate report 1.")
        report1.df_to_txt_main(firstAndLastNameDict)
        input("Press Enter to generate report 2 .")
        Report2.report2Main(firstAndLastNameDict)
        input("Press Enter to generate report 3.")
        Report3.report3Main(firstAndLastNameDict)
        input("Press Enter to generate report 4.")
        report4.report4Main(firstAndLastNameDict)
        input("Press Enter to generate report 5.")
        report5.generate_report_5_main(firstAndLastNameDict)
        input("Press Enter to generate graph A.")
        graphA.graphAMain()
        #i included the input in my report :)
        GraphB.graphBMain()
        input("Press enter to generate graph C.")
        graphc.generate_graph_c_main()
        print("Graph C generated.\n")
        input("Reports are generated and saved as report[num].txt. Graphs are displayed. Thank you for using phase III. Press enter to exit.")
    else:
        input("Files were invalid. Please see Validity Checks.txt to see which ones. Press Enter to exit Phase III.")