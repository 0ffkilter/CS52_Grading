import os, subprocess
from threading import Timer
from student_list import STUDENT_LIST
import shutil
import glob
import sys
import threading
import thread
import multiprocessing

INPUT_STRING = "c to continue, r to rerun, o to open file (in Nano), e to exit \n"

TIMEOUT = 5

PRINTER_NAME = 'Edmunds_229'

SUFFIX = '-latest'

def run_sml(cmd, queue):
    """
    Run an sml command and pipe the output back into the queue

    cmd:            the command to run
    queue:          the queue to send information back to
    """

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while (proc.returncode == None):
        queue.put(proc.stdout.readline())
        proc.poll()

def run_file(student, grading, timeout=TIMEOUT):
    """
    Run a file through the grading script
    Runs shell command 'cat pregrade.sml asgtN.sml grading_script.sml | sml'

    student:        File to run
    grading:        Grading script to compare against

    Return Value: (output, timeout) - timeout=True if process was terminated
    """

    #Get the abs path of the pregrade sml file
    pregrade = os.path.join(os.getcwd(), "pregrade.sml")

    #old command, does the same
    #cmd = r'echo "use \"%s\"; use \"%s\"; use \"%s\";" | sml -Cprint.depth=100, -Cprint.length=1000' %(pregrade, student, grading)
    cmd = r'cat %s %s %s | sml' %(pregrade, student, grading)

    #set up multiprocessing queue for data retrieval
    queue = multiprocessing.Queue()

    #start separate process and timeout after certain number of seconds
    p = multiprocessing.Process(target=run_sml, args=(cmd, queue))
    p.start()
    p.join(timeout)

    #kill process and return results depending on if the process timed out or not
    term = False
    if(p.is_alive()):
        term = True;
        p.terminate()
        p.join()
    result = ""
    while not queue.empty():
        result += queue.get()

    return(result, term)

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

def extract_files(src_dir, dir_sfx, f_name, tgt_dir, sdt_list=STUDENT_LIST):
    """ Written by Everett Bull
    Extracts files from submission download folder into new folder

    src_dir:        Source directory of asgtN_submissions
    dir_sfx:        suffix for file names (-latest, -ontime)
    f_name:         file name to look for
    tgt_dir:        target dir where the files are going
    sdt_list:       list of students in (name, userid) format

    Return Value:   a list of files in (name, filename) format
    """
    miss_list = []
    ret_list = []

    #Create target dir if it doesn't exist
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)

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
            shutil.copy (sourcePath, destinationPath)
            ret_list.append((name, (name + '-' + f_name)))

    return (miss_list,ret_list)

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

