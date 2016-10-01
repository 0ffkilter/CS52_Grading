#CS 52 Autograder for FA16 Semester

Because knowing the answer doesn't help you get there.  Also the tests are based on the assignment.  No tricks here!

Written by Matthew Gee, with formating and parsing help from scripts written by Everett Bull

##Requirements:

 - Python 2.7
 - SML
  - Note: SML must be in path for this to work
 - Not Windows (sorry)

#Installation
 1. Install Python 2.7 (if not on computer already)
 2. Install SML
 3. Clone (Recommended) or Download repo

#Pre Grading
 1. Download Submission zip from submit.cs.pomona.edu
 2. Download grading_scripts.zip from Sakai
    - Alternatively, clone from submodule (talk to Matt about access to this)
 3. Unzip grading_scripts.zip into grading_scripts
 4. Move Submission zip into CS52_grading/

#Usage:
 1. Python2 --assign N
 2. After file is run:
   - 'c'/enter: continue
   - 'r': rerun file
   - 'o': open in nano
   - 'e': exit
   - 't': run with longer timeout (60 seconds instead of 3)
    
    
##Command Line Arguments

 --assign N
    The assign number.  MANDATORY

 --assign-dir DIR
    In case the submission folder is in a different directory.  If nothing is inputted, the grader assumes the folder is in the cs52_grading/ directory
     
 --start-with NAME
    Start with an assignment that isn't first alphabetical (arranged by last name)
     
 --start-next NAME
    Start the assignment after the one specified by this argument.  Uses same parsing as --start-with.  --Start-with has priority over this open.

--run-file FILE
    run grading scripts on one file.  

--out-file FILE
    print results of grading (name, score) to destination file.  Overwrites any data currently in file

--traceback-length LEN
    number of lines to print when an error occurs. Defaults to 6

--timeout TIME
    sets timeout.  Default 3 (seconds)

--round-to NUM
    partial decimal to round to (i.e 0.25)  Default 0.5

--hide-email
    deprecated

##Command Line Flags

 -p 
    flag that tells it to print, specified by printer in grader_utils.py (Default is Edmunds 229 printer)

-silent-grade
    flag that will not print anything until all the files are graded - recommend to print results to file if you do this

-no-confirm
    flag that will remove the continuation confirmation, and will proceed to next assignment automatically after finishing one

