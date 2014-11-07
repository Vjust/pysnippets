from optparse import OptionParser

# using local dq module instead of the built-in collections.deque
#from collections import deque
from dq import dq as deque

from timeit import Timer

def search_no_gen(lines,pattern, his):
    """ Search for a pattern in a set of lines without using a 
    Generator function
    """
    new_line=[]
    previous_lines=deque([], his)
    for line in lines:
        if pattern in line:	
            new_line.append ( (line, previous_lines[:]))
        previous_lines.append(line)
    return new_line    


def search_gen(lines, pattern, history=5):
    """ Search for a pattern using a generator function """
    previous_lines=deque([], history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)


def main1():
    """Executes a search using a generator"""
    with open(filename) as f:
        for line, prevlines in search_gen(f, pattern, 5):
            pass
            #for pline in prevlines:
                #print (pline, end=' ')
            #print (line, end=' ')
            #print('-'*20)    
            
def main2():
    """Run a search w/o a generator """
    with open(filename) as f:
        nn=search_no_gen(f, pattern,5)
        return nn
        
        
if __name__ == "__main__":
    parser=OptionParser()
    parser.add_option("-f", "--file", dest="file",
                      default = "dictionary.txt")
    parser.add_option("-p", "--pattern", dest="pattern",
                      default = "secret")
    (options,args) = parser.parse_args()
    filename=options.file
    pattern=options.pattern
    k=main2()
    t1=Timer(setup="from __main__ import main1, main2", stmt="main1()")
    print( "With generator , using inbuilt dq {0:15.5f}".format(t1.timeit(10)))
    t2=Timer(setup="from __main__ import main1, main2", stmt="main2()")
    print( "Without generator , using custom dequeue {0:15.5f}".format(t2.timeit(10)))
