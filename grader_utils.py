from __future__ import print_function
import os, subprocess
from threading import Timer
from grading_scripts import student_list
import shutil
import glob
import sys
import threading
import thread
import multiprocessing
import re
import signal

#input string for user input after running file
INPUT_STRING = "c to continue, r to rerun, o to open file (in Nano), e to exit \n"

#timeout (in secs) to run each command for before force quitting
TIMEOUT = 3

#where to print to
PRINTER_NAME = 'Edmunds_229'

#either -latest or -ontime
SUFFIX = '-latest'

#how many lines to print when it errors
TRACEBACK_LENGTH = 6

#deprecated
def run_sml(cmd, queue):
    """
    Run an sml command and pipe the output back into the queue

    cmd:            the command to run
    queue:          the queue to send information back to
    """

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    pid = proc.pid
    queue.put("PID:" + str(pid))
    while (proc.returncode == None):
        queue.put(proc.stdout.readline())
        proc.poll()

def run_file(student, grading_pre, grading, timeout=TIMEOUT):
    """
    Run a file through the grading script
    Runs shell command 'cat pregrade.sml asgtN.sml grading_script.sml | sml'

    student:        File to run
    grading:        Grading script to compare against

    Return Value: (output, timeout) - timeout=True if process was terminated
    """
    #Get the abs path of the pregrade sml file
    pregrade = os.path.join(os.getcwd(), "pregrade.sml")
    if os.path.isdir(grading):
        return
    #old command, does the same
    #cmd = r'echo "use \"%s\"; use \"%s\"; use \"%s\";" | sml -Cprint.depth=100, -Cprint.length=1000' %(pregrade, student, grading)
    files = [pregrade, student, grading_pre, grading]

    with open(os.path.join(os.getcwd(), "tmp.sml"), 'w') as outfile:
        for f_name in files:
            with open(f_name) as infile:
                for line in infile:
                    outfile.write(line)

    cmd = ["timeout", str(timeout), "sml", "tmp.sml"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()

    return (out, err!= None)

"""
    cmd = ["sml", "tmp.sml"]
    #set up multiprocessing queue for data retrieval
    queue = multiprocessing.Queue()
    #start separate process and timeout after certain number of seconds
    p = multiprocessing.Process(target=run_sml, args=(cmd, queue))
    p.start()
    p.join(timeout)

    #kill process and return results depending on if the process timed out or not
    term = False
    if(p.is_alive()):
        term = True
        p.terminate()
        p.join()
    result = ""
    while not queue.empty():
        cur=queue.get()
        if "PID:" in cur:
            pid = int(cur[4:])
        else:
            result += cur
    try:
        os.kill(pid, signal.SIGTERM)
    except:
        pass

    return(result, term)
"""

def print_file(file_name, asgt_name):
    """
    Prints a file

    file_name:          name of file to print
    asgt_name:          Title of file

    Return Value: none
    """
    try:

        cmd = r'lpr %s -T %s -P %s -o cpi=14 -o lpi=8 -o sides=two-sided-long-edge -o page-left=72 -o page-right=72 -o prettyprint' %(file_name, asgt_name, PRINTER_NAME)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0].decode("utf-8").splitlines()
    except:
        print('lpr error \n')
        return;

def anyCase(st) :
    """ Written by Everett Bull
    Return a globbing string, capitalization does not matter

    st:     string to glob

    Return Value: globbed String
    """

    result = ""
    for c in st :
        if c.isalpha() :
            result = result + '[' + c.lower() + c.upper() + ']'
        else :
            result = result + c
    return result

def extract_files(src_dir, dir_sfx, f_name, tgt_dir, sdt_list=student_list.STUDENT_LIST):
    """
    Extracts files from submission download folder into new folder

    src_dir:        Source directory of asgtN_submissions
    dir_sfx:        suffix for file names (-latest, -ontime)
    f_name:         file name to look for
    tgt_dir:        target dir where the files are going
    sdt_list:       list of students in (name, userid) format

    Return Value:   a list of files in (name, filename) format

    @Credit to Everett Bull
    """
    miss_list = []
    ret_list = []
    created = True
    #Create target dir if it doesn't exist
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
        created = False

    for (name, userid) in sdt_list :
        possibleFiles = glob.glob(src_dir + "/" + anyCase(userid) + dir_sfx + "/" + f_name)
        if len (possibleFiles) == 0 :
            sys.stdout.write("Missing: " + name  + ", " + userid + "\n")
            miss_list.append(name + '-' + f_name)
        elif 1 < len (possibleFiles) :
            sys.stdout.write("Multiple matches: " + name  + ", " + userid + "\n")
        else :
            sourcePath = possibleFiles[0]
            destinationPath = tgt_dir + "/" + name + "-" + f_name
            ret_list.append((name, (name + '-' + f_name)))
            if not created:
                shutil.copy (sourcePath, destinationPath)

    return (miss_list,ret_list)

def parse_pre_line(line):
    """
    Splits a line from the _lst.txt files

    line:       line to split
    """

    opts = line.split(" ")
    if len(opts) != 3:
        return ("", "", "")
    name = opts[0]

    opt_a = opts[1]
    #either style points or points for the problem
    opt_b = opts[2]
    #either total asgt points or number of tests

    return (name, opt_a, opt_b)

def deduct_points(points, total, passed, failed, halted):
    """
    returns a number of points to deduct based on the test results

    0.5 points are deducted if at least one test fails.
    all points are deducted if all tests fail.
    for each additional test failed, another half a point is deducted.
    all points cannot be deducted if at least one test is passed.

    total:      total number of tests
    passed:     how many passed
    failed:     "   "   failed
    halted:     "   "   didn't finish

    Return Value: number of points to take off
    """
    deduction = 0

    #All points lost if no tests pass
    if passed == 0:
        return points


    #take off half a point for failing at least one test
    if failed > 0:
        deduction = 0.5

    #if half or more than half of the tests are failed,take off another half a point
    if (passed / float(total)) <= 0.5:
        deduction += 0.5

    #if only a quarter or less of the tests pass, take off another half a point
    if (passed / (float(total)) <=0.25):
        deduction += 0.5

    #Can't take off more than the total number of points
    #But since at least one test passed, have to get a minimum of 0.5 points for the problem.
    deduction = min(deduction, points - 0.5)


    return deduction


def roundPartial (value, resolution):
    return round (value / resolution) * resolution

def format_check(f_name) :
    """
    Return number of lines that are incorrectly formatted

    file:               list of lines in file

    Return Value: (#lines too long, #lines contain tab, #lines)

    @Credit to Everett Bull
    """

    too_long = 0
    contains_tab = 0
    comments = 0
    linecount = 0

    file = open(f_name, 'r')

    for line in file :
        linecount = linecount + 1
        comments += min(line.count("(*"), line.count("*)"))
        if 80 < len (line):
           too_long += len(line) - 80
        if 0 <= line.find ("\t") :
           contains_tab += 1

    return (too_long, contains_tab, comments, linecount)


def parse_folder(folder_directory, assign_num):
    """
    Returns correct assignment directory

    folder_directory:   directory of submission folder
    assign_num:         assignment number

    Return Value:       Path of correct assign directory
    """
    assign_name = "asgt" + "0" if assign_num < 10 else ""
    assign_name += str(assign_num) + "-submissions"
    assign_dir = os.path.join(folder_directory, assign_name)

    return assign_dir


#Deprecated
def read_tograde(a_dir):
    """
    Reads the tograde.txt file

    a_dir:          directory of .txt file

    Return Value: list of files
    """

    f = open(os.path.join(a_dir, "tograde.txt"), "r")
    return f.read().splitlines();

def parse_result(result, start_txt="--START--", end_txt="--END--"):
    """
    Parse and return sml output with regex

    result:         string to parse
    start_txt:      beginning of regex
    end_txt:        end of regex
    """
    pat = start_txt + "(.*)" + end_txt
    res = re.findall(pat, result, re.DOTALL)
    if len(res) == 0:
        res = re.findall(start_txt + "(.*)", result, re.DOTALL)
        if len(res) == 0:
            return "ERR"
    return res[0]

#Deprecated
def parse_filename(filename):
    """
    Parses the filenames to get id and email out

    filename:       filename to read

    Return Value: (ID, @school.edu, Filename)
    """

    late_txt = ""
    if ("LATE") in filename:
        filename = filename[:-6].strip()
        late_txt = " LATE SUBMISSION"
    name = filename[filename.find("Z")+2:]
    idx = name.find("@")
    return (name[:idx] + late_txt, name[idx:], filename)

def start_next(start_with, lst, n=1):
    """
    Start at the nth assignment past string containing start_with

    start_with:     String to compare against
    lst:            list of filenames
    n:              nth element
    """

    return start_early(start_with, lst)[n:]

def start_early(start_with, lst):
    """
    Truncates list of files early if grading isn't starting at first alphabetical file

    start_with:     String to compare against
    lst:            list of filenames

    Return Value:   Modified list of filenames
    """

    print("start with: " + start_with)
    if start_with == "":
        return lst
    idx = 0
    for i in range(len(lst)):
        if lst[i][0].startswith(start_with):
            break
    if not i == len(lst) - 1:
        return lst[i:]

    return lst

def open_file(filename):
    """
    Open a file in Nano

    filename:       filename to open

    Return Value:   none
    """

    subprocess.call(["nano", filename])

