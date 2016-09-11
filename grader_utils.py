import os, subprocess
from threading import Timer
from student_list import STUDENT_LIST
import shutil
import glob
import sys

INPUT_STRING = "c to continue, r to rerun, o to open file (in Nano), e to exit \n"

TIMEOUT = 15

PRINTER_NAME = 'Edmunds_229'

SUFFIX = '-latest'

def run_file(student, grading):
    """
    Run a file through the grading script
    Runs shell command 'cat pregrade.sml asgtN.sml grading_script.sml | sml'

    student:        File to run
    grading:        Grading script to compare against

    Return Value: output of sml command
    """
    pregrade = os.path.join(os.getcwd(), "pregrade.sml")
    #cmd = r'echo "use \"%s\"; use \"%s\"; use \"%s\";" | sml -Cprint.depth=100, -Cprint.length=1000' %(pregrade, student, grading)
    cmd = r'cat %s %s %s | sml' %(pregrade, student, grading)

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    kill_proc = lambda p: p.kill()
    timer = Timer(TIMEOUT, kill_proc, [proc])

    try:
        print("starting file")
        timer.start()
        result = proc.communicate()[0].decode("utf-8").splitlines()
    finally:
        timer.cancel()

    for r in result:
        print(r);
    return result

def print_file(file_name, asgt_name):
    """
    Prints a file

    file_name:          name of file to print
    asgt_name:          Title of file

    Return Value: none
    """
    try:
        cmd = r'lpr %s -T %s -p -P %s' %(file_name, asgt_name, PRINTER_NAME)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0].decode("utf-8").splitlines()
    except:
        print('lpr error')
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

    ret_list = []

    #Create target dir if it doesn't exist
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)

    for (name, userid) in sdt_list :
        possibleFiles = glob.glob(src_dir + "/" + anyCase(userid) + dir_sfx + "/" + f_name)
        if len (possibleFiles) == 0 :
            sys.stdout.write("Missing: " + name  + ", " + userid + "\n")
        elif 1 < len (possibleFiles) :
            sys.stdout.write("Multiple matches: " + name  + ", " + userid + "\n")
        else :
            sourcePath = possibleFiles[0]
            destinationPath = tgt_dir + "/" + name + "-" + f_name
            shutil.copy (sourcePath, destinationPath)
            ret_list.append((name, (name + '-' + f_name)))

    return ret_list

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

