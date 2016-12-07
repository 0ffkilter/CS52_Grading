import os
import subprocess
import sys
import re

print("Preflight Checks")

out = ""
err = None

assign_file = "asgt0%i.sml" %(assignment)

if not os.path.exists(assign_file):
    print("file not found")
    sys.exit(1)

try:
    cmd = "(cat %s ; echo \"print(\\\"Compilation_Test\\\");\") | sml" %(assign_file)
    out = subprocess.check_output(cmd, shell=True)
except:
    print("Compilation Failed")
    sys.exit(1)

if "Compilation_Test" in out:
    print("Compilation".ljust(16) + " : pass")
else:
    print("Compilation".ljust(16) + " : fail")
    print("Cannot perform type checks")
    sys.exit(1)


print("\n\n====Function Type Check====")

actual_string = "\tActual:  %s"
not_found = "Function not found"
fn_string = "val %s = fn : %s"
for function, typedef in type_checks:
    if fn_string %(function, typedef) in out:
        print(function.ljust(16) + " : pass")
    else:
        print(function.ljust(16) + " : fail")
        print("\tExpected: %s" %(typedef))
        if function in out:
            idx = out.find(function) + len(function)
            actual = out[idx+7:out.find("\n", idx)]
            print(actual_string %(actual))
        else:
            print(actual_string %(not_found))

lines = out.split("\n")

warning_string = ""

for l in lines:
    if "nonexhaustive" in l:
        warning_string = warning_string + "\nMatch Nonexhaustive at line %s" %(l[l.find(":")+1:l.find(" ")])
    elif "generalized" in l:
        warning_string = warning_string + "\nVariable Type Warning at line %s" %(l[l.find(":")+1:l.find(" ")])
    elif "operators" in l:
        warning_string = warning_string + "\nOperator Warning at line %s" %(l[l.find(":")+1:l.find(" ")])
if warning_string is not "":
    warning_string = "\n\n====Warnings====" + warning_string
    print(warning_string)
