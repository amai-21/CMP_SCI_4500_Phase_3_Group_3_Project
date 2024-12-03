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
import graphC

if __name__ == "__main__":
    valid = validityChecker.programA()
    isValid = valid.didCheckFail() 
    print(f'Is Valid: {isValid}')
    
    
    report5.generate_report_5_main()
    print("Report 5 generated.")
    
    input(f"Thank you for using Phase III. Validity check logs are found in the directory. Files from file scan for validity are found in ValidityChecks.txt \n Press enter to Generate Reports.")
    
    graphA.generate_graph_a()
    print("Graph A generated.\n")

    

    graphC.generate_graph_c_main()
    print("Graph C generated.\n")

    