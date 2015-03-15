'''
Created on Jun 7, 2014

@author: Duhi
'''
'''
Created on Jun 6, 2014

@author: Duhi
'''
import os
import hashlib
import datetime
from multiprocessing import Queue, Value, Process, Pool
import logging
def list_dir_entry(wd, file_q, p_state):
    print("In list Dir entry")
    list_dir(wd, file_q, p_state)
    p_state.value= 4
    file_q.close()
    
def list_dir(wd, file_q, p_state):
    rootdir = wd
    try:
        
        for files in os.listdir(rootdir):
            filePath=os.path.join(rootdir,files)
            if os.path.isdir(filePath):
                list_dir(filePath, file_q,p_state.value)
            else:
                print("Appending file to the list :" + filePath)
                file_q.put(filePath)
                
    except:
        p_state.value= 3    
    return


def calc_hash(file_q, result_q, p_state):
    print('size of the queue =' + str(len(file_q)))
    while True:
#     for i in range(len(file_q)):
        file_to_hash_path = file_q.get()
        print("Calculating the filesize of: " + file_to_hash_path)
        with open(file_to_hash_path, 'rb') as f:
            hash_t_start = datetime.datetime.now()
            sha1 = hashlib.sha224()
            while True:
                data =  f.read(4096 * 10)
                if not data:
                    break
                sha1.update(data)
        line = [ str(os.path.getsize(file_to_hash_path) ),file_to_hash_path, str(sha1.hexdigest()),str(datetime.datetime.now()-hash_t_start)]
        line_str = "\t".join(line)
        result_q.put(line_str)

        if p_state.value== 4:
            p_state.value = 5
#             result_q.close()
            break
        
def hash_result_writer(result_q, p_state, out_file_lst):
    with open(out_file_lst,"w") as fd: 
        print('file opened for writing')
        header_l = ["Seq_No", "file Size" ,"File", "File Hash", "time to Hash" ]
#         header_l = ["file Size" ,"File"]
        fd.write("\t".join(header_l) + '\n')
#         while True:
        for i in range(len(result_q)):
#             line = result_q.get()
            line = result_q[i]
            fd.write(line + '\n')
            if p_state.value == 5:
                print("updating the state to 6")
                p_state.value = 6
                break   
            1
#     print("eXITING")


if __name__=="__main__":
    
    WD='"D:\\VMs\\Privacy\\Hailey_Young"'
    out_file="D:\CODE\\results_out.log"
    
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/temp/myapp.log',
                    filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    
    # Now, we can log to the root logger, or any other logger. First the root...
    logging.info('In the main section, initializing logger.')
    
    # Now, define a couple of other loggers which might represent areas in your
    # application:
    
    logger1 = logging.getLogger('myapp.area1')
    logger2 = logging.getLogger('myapp.area2')
    
    files_to_hash_q=Queue()
    output_q=Queue()
    p_state=Value("i",0)
    
    WD='D:\\\MP3\\'
    out_file="D:\CODE\\results_out.log"
    multi_pool= Pool(processes=3)        
    fd=open('D:\CODE\\test1.txt','w')
    fd.write('test1')
    fd.close()
    
    res1=multi_pool.apply_async(list_dir_entry, args=(WD,files_to_hash_q,p_state,))      # start 4 worker processes
    res2=multi_pool.apply_async(calc_hash, args=(files_to_hash_q,output_q,p_state,))
    res3=multi_pool.apply_async(hash_result_writer, args=(output_q,p_state,out_file, ))
    

    multi_pool.close()
    print("pool closed")
    multi_pool.join()
    print("joined")
    
    
    