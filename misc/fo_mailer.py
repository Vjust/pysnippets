import smtplib, os,re, time
import dbi
import odbc
import fileinput,string,sys
import time
import client_config
import myfuncs


xxx_offices={'xxx_w':'OfficeCity'}
xxx_offices={'xxx_w':'OfficeCity'}



db_conn=odbc.odbc(client_config.app1_odbc_name)
db_cursor=db_conn.cursor()
db_cursor.execute("SELECT user_name, address, time_sent, resend_count,DATEDIFF (DAY, TIME_RECEIVED, TODAY(*)) days, time_received, (log_sent-confirm_sent) rep_diff from sysremoteusers")
db_result_set=db_cursor.fetchall()
db_conn.close()

user_name=0
address=1
time_sent=2
resend_count=3
days=4
time_received=5
rep_diff=6

myform="%-20s %-10s %-30s"

rep_status="\r\n\r\Replication Management System Status \r\n"
rep_status=rep_status+'\r\n'+'Field Office'+'\t'+'Days'+'\t'+'log_sent-confirm_sent'+'\r\n'
##for eachrow in db_result_set:
##    rep_status=rep_status+'\r\n'+app1_offices[eachrow[user_name]]+'\t\t'+ str(eachrow[days])+'\t\t'+ str(eachrow[rep_diff])

for eachrow in db_result_set:
    rep_status=rep_status+'\r\n'+\
        myform % (app1_offices['app19_w'].strip(),
        str(eachrow[days]).strip(),
                  str(eachrow[rep_diff]).strip())

rep_status=rep_status+"\r\n\r\n"


db_conn = odbc.odbc(client_config.app2_odbc_name)
db_cursor=db_conn.cursor()
db_cursor.execute("SELECT user_name, address, time_sent, resend_count,DATEDIFF (DAY, TIME_RECEIVED, TODAY(*)) days, time_received, (log_sent-confirm_sent) rep_diff from sysremoteusers")
db_result_set=db_cursor.fetchall()
db_conn.close()

user_name=0
address=1
time_sent=2
resend_count=3
days=4
time_received=5
rep_diff=6

myform="%-20s %-10s %-30s"

rep_status=rep_status+ "\r\n\r\napp2 Replication Status for field offices\r\n"
rep_status=rep_status+'\r\n'+'Field Office'+'\t'+'Days'+'\t'+'log_sent-confirm_sent'+'\r\n'
##for eachrow in db_result_set:
##    if (eachrow[user_name] != 'app29_t' and eachrow[user_name] != 'app29_d') :
##        rep_status=rep_status+'\r\n'+app2_offices[eachrow[user_name]]+'\t\t'+ str(eachrow[days])+'\t\t'+ str(eachrow[rep_diff])

for eachrow in db_result_set:
    if (eachrow[user_name] != 'app29_t' and eachrow[user_name] != 'app29_d') :
        rep_status=rep_status+'\r\n'+\
            myform % (app2_offices['app29_w'].strip(),
                      str(eachrow[days]).strip(),
                      str(eachrow[rep_diff]).strip())

rep_status=rep_status+"\r\n\r\n"


dclient prompt(prompt):
    return raw_input(prompt).strip()


#-- search for our procs.


mytime=time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
status_message='Running Processes at ' + mytime

db_service_count=0
repl_service_count=0

fd=os.popen(client_config.abv_dir_name+'/tlist.exe')
for line in fd:
    if re.search('dbremote', line):
        repl_service_count=repl_service_count+1
    if re.search('dbsrv9', line):
        db_service_count=db_service_count+1

fd.close()

if repl_service_count==0:
    status_message=status_message + \
    '\r\nNo replication services seem to be running'
else:
    status_message=status_message + '\r\n' +\
    str(repl_service_count) + ' Replication service(s) are running'

if db_service_count==0:
    status_message=status_message + '\r\n' +\
        'No DB services seem to be running'
else:
    status_message=status_message + '\r\n' + \
        str(repl_service_count) + ' DB service(s) are running'

status_message=status_message+"\r\n"


#to read last few lines of app1 rep_debug file   
app1_filenm = client_config.app1_db_dir + "/" + client_config.app1_rep_log
app1_log_string = ""
count = 0
try:
    for line in fileinput.input(app1_filenm):
        count_app1 = fileinput.lineno()
except IOError:
    app1_log_string = app1_log_string+ "\n\nFile " + app1_filenm +" not found"
else:  
    for line in fileinput.input(app1_filenm):
        if count_app1 < 10:
            app1_log_string = app1_log_string + line
        elif fileinput.lineno() > (count_app1 - 10):
            if(count < 10):
                app1_log_string = app1_log_string + line
            count = count+1

    app1_log_string = "\n\n Last few lines from app1 rep_debug.log file :\n\n" + app1_log_string

#to read last few lines of app2 rep_debug file
app2_filenm = client_config.app2_db_dir + "/" + client_config.app2_rep_log
app2_log_string = ""
count = 0
try:
    for line in fileinput.input(app2_filenm):
        count_app2 = fileinput.lineno()
except IOError:
    app2_log_string = app2_log_string+ "\n\nFile " + app2_filenm +" not found"
else:  
    for line in fileinput.input(app2_filenm):
        if count_app2 < 10:
            app2_log_string = app2_log_string + line
        elif fileinput.lineno() > (count_app2 - 10):
            if(count < 10):
                app2_log_string = app2_log_string + line
            count = count + 1

    app2_log_string = "\n\n Last few lines from app2 rep_debug.log file :\n\n" + app2_log_string    


size_string="\n\nFile Sizes:\n"
app1_size_string=myfuncs.myfsize(client_config.app1_db_dir + "\\" + client_config.app1_db_name + ".db", "MB")
app1log_size_string=myfuncs.myfsize(client_config.app1_db_dir + "\\" + client_config.app1_db_name + ".log", "KB")
app1rep_size_string=myfuncs.myfsize(client_config.app1_db_dir + "\\" + client_config.app1_rep_log, "KB")
app2_size_string=myfuncs.myfsize(client_config.app2_db_dir + "\\" + client_config.app2_db_name + ".db", "MB")
app2log_size_string=myfuncs.myfsize(client_config.app2_db_dir + "\\" + client_config.app2_db_name + ".log", "KB")
app2rep_size_string=myfuncs.myfsize(client_config.app2_db_dir + "\\" + client_config.app2_rep_log , "KB")
size_string += "app1 DB Size = " + app1_size_string + "\n"
size_string += "app1 Log Size = " + app1log_size_string + "\n"
size_string += "app1 RepLog Size = " + app1rep_size_string + "\n"
size_string += "app2 DB Size = " + app2_size_string + "\n"
size_string += "app2 Log Size = " + app2log_size_string + "\n"
size_string += "app2 RepLog Size = " + app2rep_size_string + "\n"

line_re=re.compile("^[IWE]\. [0-9][0-9].*")

app1_rep_summary="\napp1 Rep Log Summary counts:\n"
app1_replist=open(client_config.app1_db_dir+"\\"+client_config.app1_rep_log).readlines()
mydict={}
for line in app1_replist:
    	if re.search(line_re, line):
		myfuncs.parse_line(mydict, line)

for k,v in mydict.iteritems():
	for i,j in v.iteritems():
		app1_rep_summary += k + ' -> ' + i + ' -> ' + str(j) + "\n"


app2_rep_summary="\napp2 Rep Log Summary counts:\n"
app2_replist=open(client_config.app2_db_dir+"\\"+client_config.app2_rep_log).readlines()
mydict={}
for line in app2_replist:
    	if re.search(line_re, line):
		myfuncs.parse_line(mydict, line)

for k,v in mydict.iteritems():
	for i,j in v.iteritems():
		app2_rep_summary += k + ' -> ' + i + ' -> ' + str(j) + "\n"


## Now email the data to the recepients.
fromaddr = "xxx@xxxx.org"
    
toaddrs  = [
    #	    "xxxx@xxx.com",\
    #        "xxx@xx.xx",\
             "mail.vjrao@gmail.com"
            ]

subject = "Field office replication  status (Office:" + client_config.office_name + ")"


# Add the From: and To: headers at the start
msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs), subject))

msg = msg + status_message + rep_status + app1_log_string + app2_log_string + size_string + app1_rep_summary + app2_rep_summary
# print "Message is:"+msg +"end of msg"

#print "Message length is " + repr(len(msg))

server = smtplib.SMTP(client_config.smtp_host)
print "connected to SMTP"
#server.login(client_config.smtp_user, client_config.smtp_pwd)
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()


#print msg