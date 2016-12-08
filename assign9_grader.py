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
    if g is not '':
        with open(os.path.join("grading_scripts/asgt09", g), "r") as f:
            lines = f.read().split("\n")
            first_line = lines[0].split(" ")
            to_grade = first_line[0]
            points=first_line[1]
            f_tests = []
            for l in lines[1:]:
                l_temp = l.split(" ")
                print(l_temp)
                try:
                    f_tests.append((l_temp[0], l_temp[1]))
                except:
                    pass
            tests.append((to_grade, int(points), f_tests))

student_results = []

for (name, email) in student_list.STUDENT_LIST:
    result = "Test Summary:\n\n"
    total_points = 0
    print(name)



    if os.path.exists(os.path.join(assign_directory, name)):
        for (cur_file, cur_points, cur_tests) in tests:
            print("\t%s" %(cur_file))
            result = result + cur_file + " tests:\n"
            run_file = os.path.join(assign_directory, name, cur_file)
            total_points = total_points + cur_points
            cur_deduction = 0
            if os.path.exists(run_file):
                for (test_input, expected) in cur_tests:
                    try:
                        cmd = command + [run_file, test_input]
                        out = subprocess.check_output(cmd)
                        if out.find(expected) != -1:
                            result = result + "\t|" + test_input.ljust(16) + " : PASS\n"
                        else:
                            result = result + "\t|" + test_input.ljust(16) +  " : FAIL\n"
                            result = result + "\t\tExpected: " + expected + "\n"
                            cur_deduction = cur_deduction + 0.5
                    except Exception as e:
                        print("error on %s" %(run_file))
                        print(e)

                if cur_deduction < cur_points:
                    total_points = total_points + cur_points - cur_deduction
                cur_deduction = 0

        result = result + "\n\n"
        result = result + "Correctness points: %i/11" %(total_points)

        result = result + "\n\n#5 Points  /3\n#7 Points  /3\n#8 Points  /3\n\nTotal Points:  /20\n\nGrader Comments:"

        with open(os.path.join(assign_directory, name, "grades.txt"), 'w+') as f_grades:
            f_grades.write(result)


