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


grading_files = open("grading_scripts/asgt09/asgt09_lst.txt", "r").read()
grading_files = grading_files.split("\n")

assign_directory = "asgt09-ready"
jar_file = "grading_scripts/asgt09/jflap-cli.jar"
script_directory = "grading_scripts/asgt09"

command = ["java",
           "-jar",
           jar_file,
           "run"]


tests = []
for g in grading_files:
    with open(os.path.join("grading_scripts/asgt09", g), "r") as f:
        lines = f.read().split("\n")
        first_line = lines[0].split(" ")
        to_grade = first_line[0]
        points=first_line[1]
        f_tests = []
        for l in lines[1:]:
            l_temp = l.split(" ")
            f_tests.append((l_temp[0], l_temp[1]))
        tests.append((to_grade, points, f_tests))

student_results = []

for (name, email) in student_list.STUDENT_LIST:
    result = "Test Summary:\n\n"
    total_points = 0
    print(name)
    for (cur_file, cur_points, cur_tests) in tests:
        result = result + cur_file + " tests:\n"
        run_file = os.path.join(assign_directory, name, cur_file)
        total_points = total_points + cur_points
        cur_deduction = 0
        if os.path.exists(run_file):
            for (test_input, expected) in cur_tests:
                try:
                    proc = subprocess.Popen(command + [run_file, test_input] , stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    out, err = proc.communicate()
                    if out.find(expected) != -1:
                        result = result + "\t" + test_input + " : PASS\n".rjust("20")
                    else:
                        result = result + "\t" + test_input + " : FAIL\n".rjust("20")
                        result = result + "\t\tExpected: " + expected + "\n"
                        cur_deduction = cur_deduction + 0.5
                except:
                    print("error on %s" %(run_file))

            if cur_deduction < cur_points:
                total_points = total_points + cur_points - total_deduction

    result = result + "\n\n"
    result = result + "Correctness points: %i/17" %(total_points)

    result = result + "\n\n#5 Points  /3\n\nTotal Points:  /20\n\nGrader Comments:"

    with open(os.path.join(assign_directory, name, "grades.txt"), 'w+') as f_grades:
        f_grades.write(result)


