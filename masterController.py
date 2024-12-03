'''
Author: Rohan Keenoy
Program Launches Reporting and graphing after verification of correct files. 
'''
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
    #print(f'Is Valid: {isValid}')
    #valid will return if the program is valid per program A of phase II.
    if (isValid):
        input(f"Phase III:: Validity check logs are found in the directory. Files from file scan for validity are found in ValidityChecks.txt \n Press enter to Generate Reports.")
        #report1
        Report2.report2Main()
        Report3.report3Main()
        #report4
        #report5.generate_report_5_main()
        graphA.graphAMain()
        GraphB.graphBMain()
        graphc.generate_graph_c_main()
        print("Graph C generated.\n")
        input("Reports are generated and saved as report[num].txt. Graphs are displayed. Thank you for using phase III. Press enter to exit.")
    else:
        input("Files were invalid. Please see Validity Checks.txt to see which ones. Press Enter to exit Phase III.")