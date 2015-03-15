'''
Created on Oct 21, 2014

@author: mabdul
'''
'''
Created on Oct 20, 2014

@author: Duhi
'''
import os
import subprocess
import sys
import time
class monitor():
    def __init__(self):
        self.stdoutfile="../resources/processes_lst.lst"
        self.stderrfile="../resources/processes_lst.err"
        self.monlog="./process.log"
        self.proc_dict={}
        self.ln_cnt=0
        self.header_lst=[]
        
    def run_ps(self):
        stdout_fd=open(self.stdoutfile,"r")
        stderr_fd=open(self.stderrfile,"w")
        #we want to run "ps -u adf -o pid,%cpu,%mem,pri,sz,time,c,comm"
        paramlist=["ps","-u", "adf","-o", "pid,%cpu,%mem,pri,sz,time,c,comm"]
        exitcode = subprocess.call(paramlist, stdout=stdout_fd, stderr=stderr_fd, shell=False)
        if exitcode != 0:
            raise()
        
        stdout_fd.close()
        stderr_fd.close()

    def parse_proc_lst(self):
        print "in parse_proc_lst"
        if os.path.exists(self.stdoutfile):
            with open(self.stdoutfile, 'r') as stdout_fd:
                for lines in stdout_fd:
                    if self.ln_cnt==0:
                        self.header_lst=lines.split()
                        self.ln_cnt+=1
                        print "self.header_lst=" + str(self.header_lst)
                    else:
                        line_lst=lines.split()
                        print "line_lst=" + str(line_lst)
                        #if ("remake" in line_lst[7] or 
                        #"techafp" in line_lst[7] or
                        #"techcodr" in line_lst[7] or
                        #"techsort" in line_lst[7] or
                        #"techps" in line_lst[7] or
                        #"techpdf" in line_lst[7] or
                        #"techlcds" in line_lst[7] or
                        #"techmulti" in line_lst[7]):
                        if len(line_lst) > 1:
                            if not str(line_lst[0]) in self.proc_dict:
                                print "Key:" + str(line_lst[0]) + " not in self.proc_dict" 
                                self.proc_dict[str(line_lst[0])]=[line_lst]
                            else:
                                print "Key:" + str(line_lst[0]) + " already exists, adding to the list of list"
                                print "dict content of key is:" + str(self.proc_dict[str(line_lst[0])])
                                self.proc_dict[str(line_lst[0])].append(line_lst)
                            self.ln_cnt+=1
                                
        else:
            print "path" + self.stdoutfile + "does not exist"
        print "outside the with"
        print self.proc_dict
    def write_dict(self):
        print "To implement writing a dictionary"
        print "\t".join(self.header_lst)
        for elements in self.proc_dict:
            print(elements)
            for lst_elements in self.proc_dict[elements]:
                print "\t".join(lst_elements)
                     
         
        
if __name__ == "__main__" :
    print "in main"
    app_mon=monitor()
    try:
        while True:
            app_mon.run_ps()
            app_mon.parse_proc_lst()
            time.sleep(30)
            
    except KeyboardInterrupt:
        app_mon.write_dict()
        sys.exit(0)