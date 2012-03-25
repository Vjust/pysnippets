import sys
import re

pat=sys.argv[1]
input_line = sys.argv[2]
print '\n Current pattern :%s\n' % (pat)
print '\n Current input-line:%s\n' % (input_line)




matches=re.findall(pat, input_line)
print "\n these are the matches:"
for m in matches:
    print "\t\tm = %s" % ( str(m) )
    print "\n phone - %d-%d-%d" % m


a=re.compile(r"""[(]{0,1} # an optional paren
                 (\d{3})  # first group - 3 digits
                 [)]{0,1} # closing parens
                 \s* # any number of spaces
                 [-]* # any hypens
                 \s* # any number of spaces
                 (\d{3,3}) # second group of digits
                 \s*-\s* # any white space 
                 (\d{4,4}) # group of 4 digits
                 """ , re.X)

matches2=a.findall(input_line)
print "\n (2) these are the matches:"
for m in matches2:
    print "\t\tm = %s" % ( str(m) )
    phone="%s-%s-%s" % m
    #try:
    #    print "\n phone= %d-%d-%d" % m
    #except TypeError:
    #    print "exception m=%s" % (str(m))
    print "\n Phone = " + phone

for i in m:
    print i

print type(m)
