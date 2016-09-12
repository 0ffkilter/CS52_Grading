#CS 52 Autograder for FA16 Semester

Because knowing the answer doesn't help you get there.  Also the tests are based on the assignment.  No tricks here!

Written by Matthew Gee, with formating and parsing help from scripts written by Everett Bull

##Requirements:

 - Python 2.7
 - SML
  - Note: SML must be in path for this to work
 
 
#Usage:

 1. Clone or download repo (Cloning recommended, grader is still being worked on)
 2. Download submission zip from submit.cs.pomona.edu
 3. Download grading script from Sakai and student_list.py from Sakai
 4. Extract submission zip into cs52_grading/; put student_list into CS52_grading/ as well
 5. Move grading script into cs52_grading/grading_scripts
 6. CD into cs52_grading/
 7. Start grading with python ./grader.py --assign N
    - N is assignment number
    
    
##Command Line Arguments

 --assign-number N
     The assign number.  MANDATORY

 --assign-dir 
     In case the submission folder is in a different directory.  If nothing is inputted, the grader assumes the folder is in the cs52_grading/ directory
     
 --start-with
     Start with an assignment that isn't first alphabetical (arranged by last name)
     
 --start-next
     Start the assignment after the one specified by this argument.  Uses same parsing as --start-with.  --Start-with has priority over this open.
     
 -p 
    flag that tells it to print, specified by printer in grader_utils.py (Default is Edmunds 229 printer)
