#!/usr/bin/env python3

import sys
import subprocess
import os
import os.path as path
import argparse
from argparse import RawTextHelpFormatter
from grader_utils import read_tograde
from grader_utils import start_early
from grader_utils import parse_filename
from grader_utils import run_file
from grader_utils import open_file
from grader_utils import input_string

def grade_assign(assign_num, folder_directory, hide_email, start_with):

    #Find assign folder
    assign_name = "asgt" + "0" if assign_num < 10 else ""
    assign_name += str(assign_num) + "-submissions"
    assign_dir = os.path.join(folder_directory, assign_name)
    #Parse filenames in the tograde.txt
    assigns = read_tograde(assign_dir)
    names = start_early(start_with, sorted([parse_filename(a) for a in assigns]))

    file_name = "asgt" + "0" if assign_num < 10 else ""
    file_name += str(assign_num) + ".sml"

    #Parse grading script name
    grading_name = "grading_scripts/asgt" + "0" if assign_num < 10 else ""
    grading_name += str(assign_num) + "_grading.sml"

    grading_path = os.path.join(os.getcwd(), grading_name)

    for (name, email, dname) in names:
        print("Name : " + name + "\n")
        run_file(os.path.join(assign_dir, dname, file_name), grading_path)
        inp = input(input_string)
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


    res = parser.parse_args()
    print(res.start_with)
    if res.assign_num < 0:
        print("assign number required with --assign")
        sys.exit(0)
    grade_assign(res.assign_num, res.assign_dir, res.email_silent, res.start_with)

if __name__ == "__main__":
    main()
