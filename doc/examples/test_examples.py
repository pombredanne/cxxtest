# Imports
import pyutilib.th as unittest
import glob
import os
from os.path import dirname, abspath, basename
import sys
import re

currdir = dirname(abspath(__file__))+os.sep
datadir = currdir

compilerre = re.compile("^(?P<path>[^:]+)(?P<rest>:.*)$")
dirre      = re.compile("^([^%s]*/)*" % re.escape(os.sep))
failure    = re.compile("^(?P<prefix>.+)file=\"(?P<path>[^\"]+)\"(?P<suffix>.*)$")

#print "FOO", dirre 
def filter(line):
    if 'Running' in line or "IGNORE" in line:
        return True
    pathmatch = compilerre.match(line) # see if we can remove the basedir
    failmatch = failure.match(line) # see if we can remove the basedir
    #print "HERE", pathmatch, failmatch
    if failmatch:
        parts = failmatch.groupdict()
        #print "X", parts
        line = "%s file=\"%s\" %s" % (parts['prefix'], dirre.sub("", parts['path']), parts['suffix'])
    elif pathmatch:
        parts = pathmatch.groupdict()
        #print "Y", parts
        line = dirre.sub("", parts['path']) + parts['rest']
    return line

# Declare an empty TestCase class
class Test(unittest.TestCase): pass

if not sys.platform.startswith('win'):
    # Find all *.sh files, and use them to define baseline tests
    for file in glob.glob(datadir+'*.sh'):
        bname = basename(file)
        name=bname.split('.')[0]
        if os.path.exists(datadir+name+'.txt'):
            Test.add_baseline_test(cwd=datadir, cmd=file, baseline=datadir+name+'.txt', name=name, filter=filter)

# Execute the tests
if __name__ == '__main__':
    unittest.main()
