#!/usr/bin/env python3
from __future__ import print_function
from time import sleep
import sys
import subprocess
import os
import os.path as path
import argparse
from argparse import RawTextHelpFormatter
from grader_utils import *
from grading_scripts import student_list
import re
import time
import csv

file_list = ['dblabs.a52',
             'power.a52',
             'ackermann.a52',
             'asgt04-4a.txt',
             'asgt04-4b.txt']

total_tests = 13

answer_string = "CS52 says > "

grading_files = open("grading_scripts/asgt04/asgt04_lst.txt", "r").read()
grading_files = grading_files.split("~")

p1_files = grading_files[0].split("\n")
p2_files = grading_files[1].split("\n")
p3_files = grading_files[2].split("\n")

p1_grading = []
for line in p1_files:
    args = line.split(" ")
    if len(args) >= 3:
        p1_grading.append((args[0], args[1], args[2:-1], args[-1]))

p2_grading = []
for line in p2_files:
    args = line.split(" ")
    if len(args) >= 3:
        p2_grading.append((args[0], args[1], args[2:-1], args[-1]))

p3_grading = []
for line in p3_files:
    args = line.split(" ")
    if len(args) >= 3:
        p3_grading.append((args[0], args[1], args[2:-1], args[-1]))

grading = [("dblabs.a52", p1_grading), ("power.a52", p2_grading), ("ackermann.a52", p3_grading)]

student_results = []
for (name, email) in student_list.STUDENT_LIST:
    print(name)
    num_correct = 0
    pts = 0
    test_results = []
    for (f_name, g) in grading:
        time.sleep(0.2)
        f_compiled = f_name.replace(".a52", ".m52")

        to_grade = os.path.join('asgt04-ready', name, f_name)
        if os.path.exists(to_grade):
            print(f_name + " grade")
            for (test, points, args, answer) in g:
                str_args = " ".join(args)
                tmp_file = open("tmp.txt", "w+")
                tmp_file.write("\n".join(args))
                tmp_file.close()
                sys.stdin.flush()
                finished = False
                for i in range(20):
                    cmd = ["timeout",
                           "2",
                           "java",
                           "-jar",
                           "cs52-machine.jar",
                           "-p",
                           os.path.join('asgt04-ready', name, f_name),
                           "-u",
                           "tmp.txt"]
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    out, err = proc.communicate()
                    if "stdin" not in out:
                        break
                o = out[out.find(answer_string):]
                if o.find(answer) > -1:
                    pts = pts + int(points)
                    num_correct = num_correct + 1
                    test_results.append((test, 1, answer, answer))
                else:
                    test_results.append((test, 0, out, answer))
        else:
            print(f_name + " not submitted")
            for (test, p, a, a2) in g:
                test_results.append((test, -1, "", answer))

    foura = os.path.join("asgt04-ready", name, "asgt04-4a.txt")
    test = "4a"
    if os.path.exists(foura):
        print("asgt04-4a.txt grade")
        cmd = ["java",
               "-jar",
               "cs52-machine.jar",
               "-p",
               "asgt04-4.a52",
               "-u",
               foura]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()

        o = out[out.find(answer_string):]
        if o.find("-47") > -1:
            pts = pts + 1
            num_correct = num_correct + 1
            test_results.append((test, 1, "-47", "-47"))
        else:
            test_results.append((test, 0, out, "-47"))
    else:
        test_results.append((test, -1, "", "1000"))
        print("asgt04-4a.txt not submitted")

    fourb = os.path.join("asgt04-ready", name, "asgt04-4b.txt")
    test = "4b"
    if os.path.exists(fourb):
        print("asgt04-4b.txt grade")
        cmd = ["java",
               "-jar",
               "cs52-machine.jar",
               "-p",
               "asgt04-4.a52",
               "-u",
               fourb]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        o = out[out.find(answer_string):]

        if o.find("1000") > -1:
            pts = pts + 1
            num_correct = num_correct + 1
            test_results.append((test, 1, "1000", "1000"))
        else:
            test_results.append((test, 0, out, "1000"))

    else:
        test_results.append((test, -1, "", "1000"))
        print("asgt04-4b.txt not submitted")

    print("Student: " + name + " " + str(pts) + "/17")
    print("")
    student_results.append((name, pts, num_correct, test_results))

result = "Grading Report for Assignment 4:\n\n"

total_pts = []

pass_string = "Passed\n".rjust(12)
fail_string = "Failed\n".rjust(12)

csv_output = open('asgt04.csv', 'wb')
writer = csv.writer(csv_output)
test_dict = {}
score_dict = {}
pass_dict = {}
fail_dict = {}
nosb_dict= {}

print(len(student_results))
for (student, pts, num_correct, test_results) in student_results:
    result = ""
    if pts in score_dict:
        score_dict[pts] += 1
    else:
        score_dict[pts] = 1

    if num_correct in test_dict:
        test_dict[num_correct] += 1
    else:
        test_dict[num_correct] = 1

    curRow = []
    result = result + student + ":\n"

    result = result + "Autograded Portion: \n"
    result = result + "Tests passed:     : " + str(num_correct) + "/15\n"
    result = result + "Correctness Points: " + str(pts) + "/17\n"
    curRow.append(num_correct)
    curRow.append(pts)
    total_pts.append(pts)
    for test, res, actual, expected in test_results:
        if res == 1:
            if test in pass_dict:
                pass_dict[test] += 1
            else:
                pass_dict[test] = 1
            result = result + "    " + test.ljust(16) + pass_string
        elif res == 0:
            if test in fail_dict:
                fail_dict[test] += 1
            else:
                fail_dict[test] = 1
            result = result + "    " + test.ljust(16) + fail_string
            result = result + "    " + "Expected: ".rjust(12) + expected + "\n"
            result = result + "    " + "Actual: ".rjust(12) + actual + "\n"
        else:
            if test in nosb_dict:
                nosb_dict[test] += 1
            else:
                nosb_dict[test] = 1

            result = result + "    " + test.ljust(16) + "Not Submitted\n".rjust(12)
        curRow.append(res)
    result = result + "\n"
    result = result + "=====================================\n"
    result = result + "Grader Comments:"
    result = result + "\n\n\n\n\n\n\n\n\n\n"
    result = result + "Final Score: /17"
    try:
        grades_name = os.path.join("asgt04-ready", student, "grades.txt")
        f_student = open(grades_name, 'w+')
        f_student.write(result)
        f_student.close()
    except:
        pass
    writer.writerow(curRow)




writer.writerow([])

for key,value in test_dict.items():
    writer.writerow([key, value])

writer.writerow([])

for key,value in score_dict.items():
    writer.writerow([key, value])

writer.writerow([])

for key,value in pass_dict.items():
    writer.writerow([key, value])

writer.writerow([])

for key,value in fail_dict.items():
    writer.writerow([key, value])

writer.writerow([])

for key,value in nosb_dict.items():
    writer.writerow([key, value])

csv_output.close()



def main():
    pass

if __name__ == "__main__":
    main()
