# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:14:22 2013

@author: shanef
"""

import sys
import getopt

def main(argv):
    numFiles = 0
    doEncode = True
    try:
       opts, args = getopt.getopt(argv,"hn:l")
    except getopt.GetoptError:
       print 'TVEncoder.py -n <number of files to process> - processes n recordings'
       print 'TVEncoder.py -l -n <number of files to process> - lists the files that will be processed without actually encoding them'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'TVEncoder.py -n <number of files to process> - processes n recordings'
          print 'TVEncoder.py -l -n <number of files to process> - lists the files that will be processed without actually encoding them'
          sys.exit()
       elif opt == "-n":
          numFiles = arg
       elif opt == "-l"):
          doEncode = True

    print "Get to work"

if __name__ == "__main__":
    main(sys.argv[1:])