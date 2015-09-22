'''
Created on Apr 28, 2014

@author: Duhi
'''

import os
import sys
import datetime
import hashlib
import multiprocessing
from multiprocessing import Process, Queue, Lock, Value,JoinableQueue
import logging
import traceback

#test

class dedup():
    
    def __init__(self, wd, out_file_lst = 'C:\\Users\\Duhi\\Documents\\Dedup_OUT.csv'):
        self.wd = wd
        self.out_file_lst = out_file_lst
        self.files_to_hash_queue= Queue(-1)
        self.logging_q= Queue()
        #self.results_q= Queue()
        self.results_q= JoinableQueue()
        self.block_size = 4096 * 10
        self.status_lock=Lock()
        self.item=0
        self.done_os_walk = 0
        self.list_dir_state = Value("i",0)
        self.list_dir_done = Value("i",0)
        self.py_processes=[]
        
    def list_dir(self):
        self.logging_q.put("list_dir\t in the list_dir  function")
        rootdir = self.wd
        self.logging_q.put("list_dir\t Working Directory=" + str(rootdir))
        self.status_lock.acquire()
        self.done_os_walk=1
        self.status_lock.release()
        
        try:
            self.logging_q.put("list_dir\t About to walk rootdir=" + rootdir)
            for root, subFolders, files in os.walk(rootdir):
                self.status_lock.acquire()
                self.done_os_walk=2
                self.status_lock.release()
                for file_to_list in files:
                    filePath = os.path.join(root,file_to_list)
                    self.files_to_hash_queue.put(filePath)
        except:
            self.status_lock.acquire()
            self.done_os_walk=3
            self.status_lock.release()
            self.logging_q.put("list_dir\t Something wrong happened, must likely the hash function just blew up, improper EOF probably ")
            return 1
            sys.exit(1)
        finally:
            self.status_lock.acquire()
            self.done_os_walk = 4
            self.list_dir_done=1
            self.status_lock.release()
            #self.files_to_hash_queue.close()
            #if I decided to go with the "DONE" approach, I need to write as many writes as there is parallel, or use a multiprocessing Value() to indicate done
#             self.files_to_hash_queue.put("DONE")
#             self.files_to_hash_queue.put("DONE")
            self.files_to_hash_queue.close()
            self.logging_q.put("list_dir\t exiting the list_dir() function")
            sys.exit(0)
        
        
    def calc_hash(self, file_path):
        self.logging_q.put("calc_hash:\t in the calc_hash() function, this should be called for each file")
        try:
            self.logging_q.put("calc_hash\t Trying to open file:" + file_path)
            
            f = open(file_path, 'rb')
            sha1 = hashlib.sha224()
        
            try:
                while True:
                    data =  f.read(self.block_size)
                    if not data:
                        break
                    sha1.update(data)
            except:
                self.logging_q.put("calc_hash\t something wrong happened during hashing?")
    
            finally:
                f.close()
        except:
            self.logging_q.put("calc_hash\t unable to open file" + file_path)
            
        my_hexdigest = sha1.hexdigest()
        self.logging_q.put("calc_hash\t Exiting the calc_hash() function, this should be called for each file")
        self.logging_q.put("calc_hash\t hexdigest for file" + file_path + " =" + str(my_hexdigest))
        return str(my_hexdigest)
        
    def pull_queue(self):
        while True:
            self.logging_q.put("reading a file path from the queue")
            try:
                in_data=self.files_to_hash_queue.get()
#                 if in_data == "DONE":
#                     self.logging_q.put("Breaking from the while loop")
#                     break
#                 else:
                file_to_hash_path = in_data
                
                self.item +=1
                cur_item = self.item
                
                self.logging_q.put("Hashing the file:" + file_to_hash_path)
                hash_t_start=datetime.datetime.now()
                hash_str = self.calc_hash(file_to_hash_path)
                self.logging_q.put("returned hash value:" + hash_str)
                line_str = "\t".join([str(cur_item) ,str(os.path.getsize(file_to_hash_path) ),str(file_to_hash_path), hash_str, str(datetime.datetime.now()-hash_t_start)])
                self.logging_q.put("result line"+line_str) 
                self.results_q.put(line_str)
            #except Queue._closed:
            
            except :
                self.logging_q.put("Issues with reading the queue, unicode related? file_to_hash_path=" + file_to_hash_path)
                break
            if self.logging_q._closed and self.logging_q.empty():
                print("pull queue empty")
                sys.exit(0)
                break 
            self.logging_q.put("done Hashing the file:" + file_to_hash_path )
            if self.files_to_hash_queue.empty() and self.list_dir_done == 1:
                self.logging_q.put("Breaking from the while loop")
                self.results_q.put(line_str)
                break
        self.logging_q.put("outside the while loop, about to break")
        self.logging_q.put("calling sys.exit(0)")

        sys.exit(0)
        
    def receive(self, output_path):
        logPath='../resources'
        for logfiles in os.listdir(logPath):
            if logfiles.endswith('.log'):
                os.unlink(os.path.join(logPath,logfiles))
        fileName='dedup'
        logging.basicConfig(
                            level=logging.DEBUG,
                            datefmt='%m-%d %H:%M'
                            )
        logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        rootLogger = logging.getLogger()
        
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName), mode='w', delay=False)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
        
        while True:
            try:
                record = self.logging_q.get()
                rootLogger.debug(record)
                ele_pos=0
                for p_elem in self.py_processes:
                    if not p_elem.is_alive():
                        rootLogger.debug("PID:***" + str(p_elem.pid) + "*** exit code:" + str(p_elem.exitcode) )
                        p_elem.join()
                        del self.py_processes[ele_pos]
                    ele_pos += 1
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)
                
        while True:
            try:
                result_fd=open(os.path.join(output_path,"dedup_out.csv"),"w")
                result_ine = self.results_q.get()
                result_fd.write(result_ine)
                rootLogger.debug(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)
            finally:
                result_fd.close()
                
                
if __name__ == "__main__":
#TODO:result_q writer
#Issues with pull_queue
    try:
        WD = b"D:\\Movies"
        dedup_obj=dedup(wd=WD)
        p1 = Process(target=dedup_obj.list_dir, args=())
        p2 = Process(target=dedup_obj.pull_queue, args=() )
        p3 = Process(target=dedup_obj.pull_queue, args=() )
        
        p1.start()
        dedup_obj.logging_q.put("p1 PID=" + str(p1.pid)) 
        p2.start()
        dedup_obj.logging_q.put("p2 PID=" + str(p2.pid))
        p3.start()
        
        dedup_obj.logging_q.put("p3 PID=" + str(p3.pid))
        dedup_obj.py_processes.append(p1)
        dedup_obj.py_processes.append(p2)
        dedup_obj.py_processes.append(p3)
        
        dedup_obj.receive(WD)
        sys.exit(0)
        
    except KeyboardInterrupt:
        for p_ele in dedup_obj.py_processes:
            p_ele.terminate()
        sys.exit(1)