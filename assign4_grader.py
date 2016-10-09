#!/usr/bin/env python3
from __future__ import print_function
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

file_list = ['dblabs.a52',
             'power.a52',
             'ackermann.a52',
             'asgt04-4a.txt',
             'asgt04-4b.txt']

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

pat = "CS52 says > (.*)"

for (name, email) in student_list.STUDENT_LIST:
    print(name)

    for (f_name, g) in grading:
        f_compiled = f_name.replace(".a52", ".m52")
        for (test, points, args, answer) in g:
            str_args = " ".join(args)
            to_grade = os.path.join('asgt04-ready', name, f_name)
            if os.path.exists(to_grade):
                tmp_file = open("tmp.txt", "w")
                tmp_file.write("\n".join(args))
                cmd = ["java",
                       "-jar",
                       "cs52-machine.jar",
                       "-p",
                       os.path.join('asgt04-ready', name, f_name),
                       "-u",
                       "tmp.txt"]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                out, err = proc.communicate()
                print(out)
                res = re.findall(pat, out)
                if (len(res) > 0):
                    correct = str(res[0] == answer)
                    print(test + " " + str_args + " " + res[0] + " " + answer + " " + correct)

                tmp_file.close()
                sys.exit(0)

def main():
    pass

if __name__ == "__main__":
    main()
