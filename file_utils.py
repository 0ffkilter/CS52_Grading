import os
import shutil
import glob
from config import ASSIGNMENT_FILES
import time
from grading_scripts import student_list

class DirectoryNotFound(OSError):
    pass    

def get_files(assign_number):
    return ASSIGNMENT_FILES.get(assign_number, None)

def check_files(files, file_dir):
    file_list = []
    for (directory, sub_dirs, sub_files) in os.walk(file_dir):
        files_present = []
        files_missing = []
        for f in files:
            if f in sub_files:
                files_present.append(f)
            else:
                files_missing.append(f)
        file_list.append((directory, {present:files_present, missing:files_missing}))

def get_files_missing(file_list):
    return_list = []
    for (directory, files) in file_list:
        for f in files[files_missing]:
            return_list.append(os.path.join(directory, f))
    return return_list

def get_files_present(file_list):
    return_list = []
    for (directory, files) in file_list:
        for f in files[files_present]:
            return_list.append(os.path.join(directory, f))
    return return_list

def gather_assignment(assign_number, student_list=student_list.STUDENT_LIST):
    files = get_files(assign_number)
    src_dir = "asgt0%i-submissions" %(assign_number)
    tgt_dir = "asgt0%i-ready" %(assign_number)
    move_files(files, src_dir, tgt_dir, student_list)

def anyCase(st) :
    return "".join(["[%s%s]" %(c.lower(), c.upper()) if c.isalpha() else c for c in st])

def refresh_file(assign_number, student_name):
    files = get_files(assign_number)
    src_dir = "asgt0%i-submissions" %(assign_number)
    tgt_dir = "asgt0%i-ready" %(assign_number)
    move_files(files, src_dir, tgt_dir, [student_name])

def move_files(files, source_dir, target_dir, stdt_list=student_list.STUDENT_LIST):
    if not os.path.exists(source_dir):
        if re.match("(asgt0)([1-9]{1})(-submissions)", source_dir) is None:
            raise FileNotFoundError("Source Destination doesn't exist")
        else:
            raise FileNotFoundError("No submission folder found for given assignment")


    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
        created = False

    return_list = []
    for (student, email, section) in stdt_list:
        print("%s : %s" %(student, email))
        possibleFiles = glob.glob(os.path.join(source_dir, "*", anyCase(email), "*"))
        if len(possibleFiles) == 0:
            return_list.append((student, []))
            print("\tNo Submission")

        file_list = []

        #possible matches
        for result in possibleFiles:

            #if it has a timestamp in it
            if re.match("201[6|7](-(\d){2}){2}T", result) is not None:

                #strip the time
                time = datetime.strptime(directory, src_dir + "/%Y-%m-%dT%H+%M+%S+%f" + directory[directory.find("Z"):])

                #Now, for each of the files in there
                for (dirpath, dirnames, filenames) in os.walk(result):
                    for f in filenames:
                        #if it's one of the files we're looking for
                        if f in files:

                            #get the student id
                            student_id = dirpath.split("-")[-1]
                            new_file_list = []
                            #for each of the files we've found for for this student
                            for (cur_path, file_name, timestamp) in file_list:
                                #if it matches the name
                                if file_name == f:
                                    #if the new one is older keep the previous one
                                    if time > timestamp:
                                        new_file_list.append((cur_path, file_name,timestamp))
                                    else:
                                        #keep the one we just found
                                        new_file_list.append((dirpath, file, time))
                                else:
                                    #if it doesn't match, keep the old no matter what
                                    new_file_list.append((cur_path, file_name, timestamp))
                            file_list = new_file_list 

        #okay, so now file_list contains triples of (directory, name, time) - time to record the missing ones

        present_list = []
        missing_list = []
        file_tgt_dir = os.path.join(target_dir, student)

        if not os.path.exists(file_tgt_dir):
            os.makedirs(file_tgt_dir)
        for (d, n, t) in file_list:
            file_src_name = os.path.join(d,n)
            file_tgt_name = os.path.join(file_tgt_dir, "name-%s" %(n))
            present_list.append(n)
            if not os.path.exists():
                shutil.copy(os.path.join(file_src_name, file_tgt_name))


        for f in files:
            found = False
            for (d, n, t) in file_list:
                if n == f:
                    found = True
            if not found:
                missing_list.append(f)
        student_list.append((student, present_list, missing_list))

  
