#!/usr/bin/python

# replaces a `include with the full include file
#
# args
# $1 - file to remove includes from
# $2 - file to write output to
# $3 - list of directories to search for includes in (note: NON-RECURSIVE must specify all dirs)
#      includes are found relative to this path
#      this is equivalent to something like +incdir+

import sys
import re
import os

inVlog = sys.argv[1]
outVlog = sys.argv[2]

if inVlog == outVlog:
    sys.exit("The input and output file cannot be the same.")

# add directories to search list
incDirs = sys.argv[3:]
print("Using include dirs: " + str(incDirs))

# open file
with open(inVlog, 'r') as inFile:
    with open(outVlog, 'w') as outFile:
        # for each include found, search through all dirs and replace if found, error if not
        for line in inFile:
            match = re.match(r"^ *`include +\"(.*)\"", line)
            if match:
                # search for include and replace
                found = False
                for d in incDirs:
                    potentialIncFileName = d + "/" + match.group(1)
                    if os.path.exists(potentialIncFileName):
                        found = True
                        with open(potentialIncFileName, 'r') as incFile:
                            for iline in incFile:
                                outFile.write(iline)
                        break

                # must find something to include with
                if not found:
                    sys.exit("Couldn't find include to replace for " + str(potentialIncFileName))
            else:
                outFile.write(line)

print("Success")
