#CS 52 Autograder for FA16 Semester

Because knowing the answer doesn't help you get there.  Also the tests are based on the assignment.  No tricks here!

##Requirements:

 - Python 3.5
 - SML
  - Note: SML must be in path for this to work
 
 
#Usage:

 1. Clone or download repo (Cloning recommended, grader is still being worked on)
 2. Download submission zip from submit.cs.pomona.edu
 3. Extract into cs52_grading/ 
 4. CD into cs52_grading/
 5. Start grading with python3 ./grader.py --assign N
    - N is assignment number
    
    
##Command Line Arguments

 --assign-number N
     The assign number.  MANDATORY

 --assign-dir 
     In case the submission folder is in a different directory.  If nothing is inputted, the grader assumes the folder is in the cs52_grading/ directory
    
 --hide-email
     Currently does nothing
     
  --start-with
     Start with an assignment that isn't first alphabetical (arranged by dci usernames)  Can be a partial string, does not need to be the whole dci username (just the first few letters are sufficient)
