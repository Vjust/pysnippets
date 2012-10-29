#! /usr/bin/env python
from os import listdir,sep
from os.path import isdir,basename
from sys import argv


indent='\t'

def tree (level, dir, print_files=False):
	try:
	    	print indent * level + '|---' + basename(dir)
		level+= 1
	        for x in listdir(dir):
	            path=dir + sep + x
	            if isdir(path):
	                tree(level,path)
		    else:
			if print_files:
				print  indent * level + '|-->'+ basename(path)
	except:
		pass
        
        

def usage():
	print "Usage: " + argv[0] + " [-f] dirname"
	return

def main():
    if len(argv) == 1:
        usage()
    elif len(argv) == 2:
        tree(0, argv[1])
    elif len(argv) == 3:
	tree(0, argv[2], True)

if __name__ == "__main__":
    main()

        
