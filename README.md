#CS 52 Autograder for FA16 Semester

Because knowing the answer doesn't help you get there.  Also the tests are based on the assignment.  No tricks here!

Written by Matthew Gee, with formating and parsing help from scripts written by Everett Bull

##Requirements:

 - Python 2.7
 - SML
  - Note: SML must be in path for this to work
 
#Installation
 1. Clone (Recommended) or Download repo
 2. Download student_list.py from Sakai
 3. Move student_list.py into CS52_grading/

#Pre Grading
 1. Download Submission zip from submit.cs.pomona.edu
 2. Download grading scripts from Sakai
 3. Move grading scripts into CS52_grading/grading_scripts
 4. Move Submission zip into CS52_grading/

#Usage:
 1. Python2 --assign N
 2. After file is run:
 
   'c'/enter: continue
   'r': rerun file
   'o': open in nano
   'e': exit
   't': run with longer timeout (60 seconds instead of 5)
    
    
##Command Line Arguments

 --assign N
     The assign number.  MANDATORY

 --assign-dir 
     In case the submission folder is in a different directory.  If nothing is inputted, the grader assumes the folder is in the cs52_grading/ directory
     
 --start-with
     Start with an assignment that isn't first alphabetical (arranged by last name)
     
 --start-next
     Start the assignment after the one specified by this argument.  Uses same parsing as --start-with.  --Start-with has priority over this open.
     
 -p 
    flag that tells it to print, specified by printer in grader_utils.py (Default is Edmunds 229 printer)
