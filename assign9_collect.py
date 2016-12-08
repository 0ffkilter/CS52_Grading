import glob
import os
from grading_scripts import student_list
import sys
from datetime import datetime
import shutil

"""
Extracts files from submission download folder into new folder

src_dir:        Source directory of asgtN_submissions
dir_sfx:        suffix for file names (-latest, -ontime)
f_name:         file name to look for
tgt_dir:        target dir where the files are going
sdt_list:       list of students in (name, userid) format

Return Value:   a list of files in (name, filename) format

"""
sdt_list = student_list.STUDENT_LIST
tgt_dir = 'asgt09-ready'
src_dir = 'asgt09-submissions'
dir_sfx = '-ready'
file_list = [
          'asgt09-1.jff',
          'asgt09-2.jff',
          'asgt09-3.jff',
          'asgt09-4.jff',
          'asgt09-5.txt',
          'asgt09-6.jff',
          'asgt09-7.jff',
          'asgt09-8.jff',
        ]

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



#Create target dir if it doesn't exist
if not os.path.exists(tgt_dir):
    os.makedirs(tgt_dir)

for (name, userid) in sdt_list :
    print("===")
    possibleFiles = glob.glob(src_dir + "/*" + anyCase(userid) + "*")
    if len (possibleFiles) == 0 :
        sys.stdout.write("Missing: " + name  + ", " + userid + "\n")
    else:
        files = []
        for directory in possibleFiles:
            print("dir " + directory)
            if "Z-" in directory:
                time = datetime.strptime(directory, src_dir + "/%Y-%m-%dT%H+%M+%S+%f" + directory[directory.find("Z"):])
                print(time)
                for (dirpath, dirnames, filenames) in os.walk(directory):
                    for f in filenames:
                        if ".zip" in f:
                            try:
                                shutil.unpack_archive(f)
                            except:
                                pass
                for (dirpath, dirnames, filenames) in os.walk(directory):
                    for f in filenames:
                        print(f)
                        if f in file_list:
                            if (f, time, dirpath) not in files:
                                files.append((f, time, dirpath))
                            else:
                                append = False
                                for (a_file, t, d) in files:
                                    if a_file == f:
                                        if t < time:
                                            files.remove((a_file, t, d))
                                            append = True
                                if append:
                                    files.append((f, time, dirpath))
        for (f, t, d) in files:
            from_dir = os.path.join(d, f)
            to_dir = os.path.join(tgt_dir, name)
            if not os.path.exists(to_dir):
                os.mkdir(to_dir)
            shutil.copy(from_dir, os.path.join(to_dir, f))
