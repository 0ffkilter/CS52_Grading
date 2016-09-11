#!/usr/bin/env python3

import sys
import subprocess
import os
import os.path as path
import argparse
from argparse import RawTextHelpFormatter
from grader_utils import *

def grade_print(assign_num, folder_directory, start_with=""):
    """
    Print an assignment

    assign_num:         number of assignment (integer)
    folder_directory:   directory that assignment FOLDER is located in (where the submission folder is)
    start_with:         partial or complete username to start grading at
    """

    assign_dir = parse_folder(folder_directory, assign_num)

    #Parse filenames in the tograde.txt
    assigns = read_tograde(assign_dir)
    #Filter out names if truncating early
    names = start_early(start_with, sorted([parse_filename(a) for a in assigns]))

    #Standardize file name of assignment submission
    file_name = "asgt" + "0" if assign_num < 10 else ""
    file_name += str(assign_num) + ".sml"

    for (name, email, dname) in names:
        print_file(os.path.join(assign_dir, dname, file_name))

def grade_assign(assign_num, folder_directory, hide_email, start_with):
    """
    Grade an assignment

    assign_num:         number of assignment (integer)
    folder_directory:   directory that assignment FOLDER is located in (where the submission folder is)
    hide_email:         option, currently does nothing
    start_with:         partial or complete username to start grading at

    Return val: none
    """

    assign_dir = parse_folder(folder_directory, assign_num)

    #Parse filenames in the tograde.txt
    assigns = read_tograde(assign_dir)
    #Filter out names if truncating early
    names = start_early(start_with, sorted([parse_filename(a) for a in assigns]))

    #Standardize file name of assignment submission
    file_name = "asgt" + "0" if assign_num < 10 else ""
    file_name += str(assign_num) + ".sml"

    #Parse grading script name
    grading_name = "grading_scripts/asgt" + "0" if assign_num < 10 else ""
    grading_name += str(assign_num) + "_grading.sml"

    #Get directory of grading_scripts
    grading_path = os.path.join(os.getcwd(), grading_name)

    for (name, email, dname) in names:

        #Print Name
        print("Name : " + name + "\n")

        #Run the file through the script
        run_file(os.path.join(assign_dir, dname, file_name), grading_path)

        #Get options after running file
        inp = input(input_string)

        """
        c: continue (also just pressing enter works)
        r: rerun file (assumed that it's been edited)
        o: open file for editing in Nano
        e: exit
        """
        if inp != "c" and inp != "C" and inp != "":
            if inp == "r" or inp == "R":
                run_file(os.path.join(assign_dir, dname, file_name), grading_path)
                inp = input(input_string)
            elif inp == "o" or inp == "O":
                open_file(os.path.join(assign_dir, dname, file_name))
                inp = input(input_string)
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

    res = parser.parse_args()
    print(res.start_with)
    if res.assign_num < 0:
        print("assign number required with --assign")
        sys.exit(0)

    if (res.p):
        grade_print(res.assign_num, res.assign_dir, res.start_with)
    else:
        grade_assign(res.assign_num, res.assign_dir, res.email_silent, res.start_with)

if __name__ == "__main__":
    main()
