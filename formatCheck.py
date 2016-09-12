#! /usr/bin/env python
#
#  formatCheck :  a program to verify (and repair) the format of SML files
#                 submitted in CS 52. All lines must be at most 80 characters
#                 long and end with <LF>. The <CR> character may not appear
#                 anywhere in the file.
#
#  Rett Bull
#  Pomona College
#  19 August 2006
#
#
import os, sys


#  a simple usage message
def usage () :
    sys.stderr.write ("Usage: " + sys.argv[0] + " [-h|-f] <filename> ...\n")
    sys.exit ()


#  a more verbose help message
def helpMessage () :
    progname = sys.argv[0]
    slash = progname.rfind ("/")
    if slash != -1 :
       progname = progname[slash + 1:]
    sys.stdout.write ("Usage:\n")
    sys.stdout.write ("   " + progname \
                      + " -h               print this message\n")
    sys.stdout.write ("   " + progname + " <filenames>      check the files\n")
    sys.stdout.write ("   " + progname + " -f <filenames>   repair the files\n")
    sys.stdout.write ("       The original file is saved as <filename>.DOS\n")


# verify that a file is correctly formatted
def checkFile (fname, isStrict) :
    linecount = 0
    file = open (fname, 'r')

    for line in file :
        linecount = linecount + 1
        if 80 < len (line):
           sys.stdout.write (fname + 
                             ", line " + str (linecount) + " is too long.\n")
        if 0 <= line.find ("\t") :
           sys.stdout.write (fname + 
                             ", line " + str (linecount) + " contains <TAB>.\n")




#  fix a file
def fixFile (fname) :
    dstfilename = fname
    srcfilename = dstfilename + ".DOS"
    os.rename (dstfilename, srcfilename)

    warning = False
    srcfile = open (srcfilename, 'r')
    dstfile = open (dstfilename, 'w')

    for line in srcfile :
        line = line.replace ("\r", "")
	line = line.replace ("\t", "    ")
        if len (line) == 0 or line[-1] != "\n" :
           line = line + "\n"
        while 80 < len (line) :
            warning = True
	    dstfile.write (line[0:79] + "\n")
            line = line[79:]
        dstfile.write (line)

    if warning :
       sys.stderr.write (fname + 
                      " WARNING: some lines were broken into shorter ones.\n")


#
# main script
#
helpFlag   = False
fixFlag    = False
strictFlag = False
arguments=sys.argv[1:]

# check options
for arg in arguments :
    if arg[0] == "-" :
       del arguments[0]
       if arg == "-h" :
          helpFlag = True
       elif arg == "-f" :
          fixFlag  = True
       elif arg == "-S" :
          strictFlag = True
       elif arg == "--" :
          break
       else :
          usage ()
    else:
       break

# execute main program
if helpFlag :
   helpMessage ()
else :
   if len (arguments) == 0 :
      usage ()
   elif fixFlag :
      for filename in arguments :
          fixFile (filename)
   else :
      for filename in arguments :
          checkFile (filename, strictFlag)


