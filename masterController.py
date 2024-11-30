'''
Author: Rohan Keenoy
Program Launches Reporting and graphing after verification of correct files. 
'''
import validityChecker
import Report2
import Report3
import Graph3


if __name__ == "__main__":
    valid = validityChecker.programA()
    isValid = valid.didCheckFail() 
    print(f'Is Valid: {isValid}')
    
    input(f"Thank you for using Phase III. Validity check logs are found in the directory. Files from file scan for validity are found in ValidityChecks.txt \n Press enter to Generate Reports.")