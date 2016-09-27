#!/usr/bin/env python3
from __future__ import print_function
import sys
import subprocess
import os
import os.path as path
import argparse
from argparse import RawTextHelpFormatter
from grader_utils import *
from student_list import STUDENT_LIST
import re


def grade_print(assign_num, folder_directory, s_with, s_next):
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
       print_file(os.path.join(target_name, f_name), file_name)

def grade_file(assign_num, f_name):
    """
    Grade one file

    assign_num:         assignment number
    f_name:             name of file to grade
    """

    assign_name = "asgt" + "0" if assign_num < 10 else ""
    assign_name += str(assign_num)

    #Standardize file name of assignment submission
    file_name = assign_name + ".sml"

    grading_list_file = open(os.path.join(os.getcwd(), "grading_scripts", assign_name, (assign_name + "_lst.txt")), 'rU')
    grading_files = grading_list_file.read().split("\n")

    grading_files = [parse_pre_line(os.path.join(os.getcwd(), "grading_scripts", assign_name, f)) for f in grading_files]
    grading_pre, style_points, total_points = grading_files[0]
    grading_scripts = grading_files[1:]


    passed = 0
    failed = 0
    halt = 0
    total_deduction = 0

    (too_long, tabs, total) = format_check(f_name)

    deduct_list = []

    num_pat = assign_name + "_(.*).sml"

    for (f_script, points, tests) in grading_scripts:
        (r, err) = run_file(os.path.join(f_name), grading_pre, f_script)

        res = parse_result(r)

        if res ==  "ERR":
            print("Error reached")
            print("Traceback: \n" + "\n".join(r.splitlines()[-TRACEBACK_LENGTH:]))
        else:
            print(res)

        c_pass = res.count(" PASS")
        c_fail = res.count(" FAIL")
        c_halt = int(tests) - c_pass - c_fail

        if (c_halt > 0):
            print("Test timed out\n")
            any_timeout = True


        passed += c_pass
        failed += c_fail
        halt += c_halt

        points = float(points)
        tests = int(tests)

        c_deduction = deduct_points(points, tests, c_pass, c_fail, c_halt)

        if (c_deduction > 0):
            deduct_list.append((re.findall(num_pat, f_script)[0], c_deduction))

        total_deduction += c_deduction

        if c_deduction > 0:
            print(str(c_deduction) + " points taken off on previous problem\n\n")


    print("\n\n====Summary====")
    print("Pass:  " + str(passed))
    print("Fail:  " + str(failed))
    print("Halt:  " + str(halt))
    print("Total: " + str(passed + failed + halt) + "\n")

    style_deduction = 0
    if too_long > 0:
        style_deduction += 0.5
    if tabs > 0:
        style_deduction += 0.5

    print("# too long lines: " + str(too_long))
    print("# lines w/ tabs: " + str(tabs) + "\n")

    print("Correctness Deductions:")
    for (n, d) in deduct_list:
        print(n + ": -" + str(d))
    print("\n")


    style_points = int(style_points)
    total_points = int(total_points)

    print("Style: " + str(style_points - style_deduction) + "/" + str(style_points))
    print("Correctness: " + str(total_points - total_deduction - style_points) + "/" + str(total_points - style_points) + "\n")


    print("\nSuggested score: " + str(total_points - total_deduction - style_deduction) + "/" + str(total_points))




def grade_assign(assign_num, folder_directory, s_with, s_next, silent_grade=False, no_confirm=False, outfile=""):
    """
    Grade an assignment

    assign_num:         number of assignment (integer)
    folder_directory:   directory that assignment FOLDER is located in (where the submission folder is)
    s_with:         partial or complete username to start grading at
    s_next:         partial or complete username to start grading after

    Return val: none
    """

    grades = []
    assign_dir = parse_folder(folder_directory, assign_num)

    assign_name = "asgt" + "0" if assign_num < 10 else ""
    assign_name += str(assign_num)

    #Standardize file name of assignment submission
    file_name = assign_name + ".sml"

    grading_list_file = open(os.path.join(os.getcwd(), "grading_scripts", assign_name, (assign_name + "_lst.txt")), 'rU')
    grading_files = grading_list_file.read().split("\n")

    grading_files = [parse_pre_line(os.path.join(os.getcwd(), "grading_scripts", assign_name, f)) for f in grading_files]
    grading_pre, style_points, total_points = grading_files[0]
    grading_scripts = grading_files[1:]

    #Target directory name
    target_name = assign_name + '-ready'

    #get list of student files
    miss_list, files = extract_files(assign_dir, SUFFIX, file_name, target_name)

    #Trim list of files if starting not at the beginning
    if s_next != "":
        files = start_next(s_next, files, 1)
    elif s_with != "":
        files = start_early(s_with, files)
    if len(miss_list) != 0:
        raw_input("Enter to continue")

    for (name, f_name) in files:

        #Print Name
        if not silent_grade:
            print("Name : " + name + "\n")
        else:
            print("=", end="")

        # #Run the file through the script
        passed = 0
        failed = 0
        halt = 0
        total_deduction = 0
        any_timeout=False
        (too_long, tabs, total) = format_check(os.path.join(target_name, f_name))

        deduct_list = []

        num_pat = assign_name + "_(.*).sml"
        for (f_script, points, tests) in grading_scripts:
            (r, err) = run_file(os.path.join(target_name, f_name), grading_pre, f_script)

            res = parse_result(r)

            if res ==  "ERR":
                if not silent_grade:
                    print("Error reached")
                    print("Traceback: \n" + "\n".join(r.splitlines()[-TRACEBACK_LENGTH:]))
            else:
                if not silent_grade:
                    print(res)

            c_pass = res.count(" PASS")
            c_fail = res.count(" FAIL")
            c_halt = int(tests) - c_pass - c_fail

            if (c_halt > 0):
                if not silent_grade:
                    print("Test timed out\n")
                any_timeout = True


            passed += c_pass
            failed += c_fail
            halt += c_halt

            points = float(points)
            tests = int(tests)

            c_deduction = deduct_points(points, tests, c_pass, c_fail, c_halt)
            if (c_deduction > 0):
                deduct_list.append((re.findall(num_pat, f_script)[0], c_deduction))

            total_deduction += c_deduction

            if c_deduction > 0 and not silent_grade:
               print(str(c_deduction) + " points taken off on previous problem\n\n")


        style_points = int(style_points)
        total_points = int(total_points)

        style_deduction = 0
        if too_long > 0:
            style_deduction += 0.5
        if tabs > 0:
            style_deduction += 0.5


        if not silent_grade:
            print("\n\n====Summary====")
            print("Pass:  " + str(passed))
            print("Fail:  " + str(failed))
            print("Halt:  " + str(halt))
            print("Total: " + str(passed + failed + halt) + "\n")


            print("# too long lines: " + str(too_long))
            print("# lines w/ tabs: " + str(tabs) + "\n")


            print("Correctness Deductions:")
            for (n, d) in deduct_list:
                print(n + ": -" + str(d))
            print("\n")

            print("Style: " + str(style_points - style_deduction) + "/" + str(style_points))
            print("Correctness: " + str(total_points - total_deduction - style_points) + "/" + str(total_points - style_points) + "\n")

            print("\nSuggested score: " + str(total_points - total_deduction - style_deduction) + "/" + str(total_points))

            # result, term = run_file(os.path.join(target_name, f_name), grading_path)

            # print(result)
            # if term:
            #     print("Terminated early, timeout limit reached")


            print(name + " finished\n")

            grades.append((name, (total_points - total_deduction - style_deduction)))


        if not no_confirm:
            print(INPUT_STRING)
            inp = raw_input("t: run with longer timeout (60 seconds)" if any_timeout else "")

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
    if outfile != "":
        o_file = open(outfile, 'w');

        g_sum = 0
        for (n, g) in grades:
            o_file.write("%s : %s\n" %(n, g))
            g_sum += g

        o_file.write("Avg: " + str(g_sum/len(grades)))





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

    parser.add_argument('-silent-grade', action='store_true', help =
            """
            Don't print anything
            """)

    parser.add_argument('-no-confirm', action='store_true', help =
            """
            Don't confirm, keep oging after grading
            """)

    parser.add_argument('--outfile', action='store', dest='outfile', default='', type=str, help=
            """
            Where to output grades
            """)

    parser.add_argument('--start-next', action='store', dest='start_next', default='', type=str, help=
            """
            Start the assignment AFTER the one containing the string given.  Can be partial name
            """)

    parser.add_argument('--timeout', action='store', dest='timeout', default=3, type=int, help=
            """
            timeout (in seconds) to wait before force terminating problem
            """)

    parser.add_argument('--traceback-length', action='store', dest='traceback_length', default=6, type=int, help=
            """
            how many lines of error to print
            """)

    parser.add_argument('--run-file', action='store', dest='file', default='', type=str, help=
            """
            Run one specific file.  Should be in the current directory
            """
            )

    res = parser.parse_args()
    print(res.start_with)
    if res.assign_num < 0:
        print("assign number required with --assign")
        sys.exit(0)

    TIMEOUT=res.timeout
    TRACEBACK_LENGTH=res.traceback_length

    if (res.p):
        grade_print(res.assign_num, res.assign_dir, res.start_with, res.start_next)
    else:
        if (res.file != ""):
            grade_file(res.assign_num, res.file)
        else:
            grade_assign(res.assign_num, res.assign_dir, res.start_with,
                    res.start_next, silent_grade=res.silent_grade, no_confirm=res.no_confirm, outfile=res.outfile)

if __name__ == "__main__":
    main()
