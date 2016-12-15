#!/usr/bin/env python3
from __future__ import print_function
from time import sleep
import sys
import subprocess
import os
import os.path as path
import argparse
from argparse import RawTextHelpFormatter
from grading_scripts import student_list
import jflap_tester.test
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
        words = g.split(" ")
        #file, isTuring, numTests, points
        tests.append((words[0], words[2], words[3], int(words[1])))

for (name, email) in student_list.STUDENT_LIST:
    result = "Test Summary:\n\n"
    total_points = 0
    print(name)

    if os.path.exists(os.path.join(assign_directory, name)):
        for (cur_file, isTuring, num_tests, cur_points) in tests:
            print("\t%s" %(cur_file))
            result = result + "\n" + cur_file + "\n"
            result = result + ("=" * 22) + "\n"
            num_failed = 0
            test_results = []
            try:
                test_results = jflap_tester.test.runTests(os.path.join(assign_directory, name, (cur_file+".jff").replace("_", "-")),
                                            os.path.join(script_directory, cur_file+".txt"), True if isTuring == "1" else False)
            except RecursionError:
                result = result + "\t Turing Machine Failed to Halt - cannot proceed\n"
                print("recursion error")
            except:
                print("foo")
            else:
                for (test_input, did_pass, expected) in test_results:
                    if did_pass:
                        result = result + (test_input).ljust(16) + ": pass\n"
                    else:
                        result = result + (test_input).ljust(16) + ": fail\n"
                        result = result + "\tExpected: " + ("Accept\n" if expected else "False\n")
                        num_failed = num_failed + 1
                total_points = total_points + max(0, cur_points - (num_failed * 0.5))
            result = result + ("=" * 22) + "\n"

        result = result + "\nCorrectness points: %i/17" %(total_points)

        result = result + "\n\n#5 Points  /3\n\nTotal Points:  /20\n\nGrader Comments:"
        print(result)
        with open(os.path.join(assign_directory, name, "grades.txt"), 'w+') as f_grades:
            f_grades.write(result)


