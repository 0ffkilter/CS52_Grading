#!/usr/bin/env python3

import sys
import subprocess
import os
import os.path as path
import argparse
from argparse import RawTextHelpFormatter
from grader_utils import *
from student_list import STUDENT_LIST

def grade_print(assign_num, folder_directory, start_with=""):
    """
    Print an assignment

    assign_num:         number of assignment (integer)
    folder_directory:   directory that assignment FOLDER is located in (where the submission folder is)
    start_with:         partial or complete username to start grading at
    """

    assign_dir = parse_folder(folder_directory, assign_num)


    #Standardize file name of assignment submission
    file_name = "asgt" + "0" if assign_num < 10 else ""
    file_name += str(assign_num) + ".sml"

    #Target directory name
    target_name = "asgt" + "0" if assign_num < 10 else ""
    target_name += str(assign_num) + '-ready'

    #get list of files
    miss_list, files = extract_files(assign_dir, SUFFIX, file_name, target_name)

    #Trim list of files if starting not at the beginning
    if s_next != "":
        files = start_next(s_next, files, 1)
    elif s_with != "":
        files = start_early(s_with, files)

    if len(miss_list) != 0:
        raw_input("Enter to continue")

    for (name, f_name) in files:
       print_file(os.path.join(assign_dir, dname, file_name), file_name)

def grade_assign(assign_num, folder_directory, s_with, s_next):
    """
    Grade an assignment

    assign_num:         number of assignment (integer)
    folder_directory:   directory that assignment FOLDER is located in (where the submission folder is)
    s_with:         partial or complete username to start grading at
    s_next:         partial or complete username to start grading after

    Return val: none
    """

    assign_dir = parse_folder(folder_directory, assign_num)


    #Standardize file name of assignment submission
    file_name = "asgt" + "0" if assign_num < 10 else ""
    file_name += str(assign_num) + ".sml"

    #Target directory name
    target_name = "asgt" + "0" if assign_num < 10 else ""
    target_name += str(assign_num) + '-ready'

    #get list of files
    miss_list, files = extract_files(assign_dir, SUFFIX, file_name, target_name)

    #Trim list of files if starting not at the beginning
    if s_next != "":
        files = start_next(s_next, files, 1)
    elif s_with != "":
        files = start_early(s_with, files)


    #Parse grading script name
    grading_name = "grading_scripts/asgt" + "0" if assign_num < 10 else ""
    grading_name += str(assign_num) + "_grading.sml"

    #Get directory of grading_scripts
    grading_path = os.path.join(os.getcwd(), grading_name)

    if len(miss_list) != 0:
        raw_input("Enter to continue")

    for (name, f_name) in files:

        #Print Name
        print("Name : " + name + "\n")

        #Run the file through the script
        result, term = run_file(os.path.join(target_name, f_name), grading_path)

        print(result)
        if term:
            print("Terminated early, timeout limit reached")


        print("Name : " + name + " finished\n")
        #Get options after running file
        inp = raw_input(INPUT_STRING + "t: run with longer timeout (60 seconds)" if term else "")

        """
        c: continue (also just pressing enter works)
        r: rerun file (assumed that it's been edited)
        o: open file for editing in Nano
        e: exit
        t: run without timeout (potentially dangerous)
        """
        while inp != "c" and inp != "C" and inp != "":
            if inp == "r" or inp == "R":
                result, term = run_file(os.path.join(target_name, f_name), grading_path)
                print(result)
                if term:
                    print("Terminated early, timeout limit reached")
                print("Name : " + name + " finished\n")
                inp = raw_input(INPUT_STRING + "t: run with longer timeout (60 seconds)" if term else "")
            elif inp == "t" or inp == "T":
                result, term = run_file(os.path.join(target_name, f_name), grading_path, 60)
                print(result)
                if term:
                    print("Terminated early, timeout limit reached")
                print("Name : " + name + " finished\n")
                inp = raw_input(INPUT_STRING)

            elif inp == "o" or inp == "O":
                open_file(os.path.join(assign_dir, dname, file_name))
                inp = raw_input(INPUT_STRING)
            else:
                sys.exit(0)

def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('--assign-dir', action='store', dest='assign_dir', default=os.getcwd(), type=str, help=
            """
            Where the assign directory is. If no option is specified, it is assumed the folder is in the current directory.
            """)

#     parser.add_argument('--grading-option', action='store', dest='grading_option', default='default', type=str, help=
            # """
            # Which option to choose for grading:

            # default  : grade those in tograde.txt
            # latest   : grade the absolute latest entries, even if late
            # on-time  : only grade the latest on time things

            # """)

    parser.add_argument('--hide-email', action='store', dest='email_silent', default='false', type=bool, help=
            """
            Hide email address when grading, only display the username

            false    : display entire email
            true     : only display username, hide @____.edu

            """)

    parser.add_argument('--assign', action='store', dest='assign_num', default='-1', type=int, help =
            """
            Which assign to grade - as an integer
            """)

    parser.add_argument('--start-with', action='store', dest='start_with', default='', type=str, help=
            """
            Which name to start with (can be partial string)
            """)

    parser.add_argument('-p', action='store_true', help =
            """
            Print flag.  Overrides other actions
            """)

    parser.add_argument('--start-next', action='store', dest='start_next', default='', type=str, help=
            """
            Start the assignment AFTER the one containing the string given.  Can be partial name
            """)


    res = parser.parse_args()
    print(res.start_with)
    if res.assign_num < 0:
        print("assign number required with --assign")
        sys.exit(0)

    if (res.p):
        grade_print(res.assign_num, res.assign_dir, res.start_with)
    else:
        grade_assign(res.assign_num, res.assign_dir, res.start_with, res.start_next)

if __name__ == "__main__":
    main()
