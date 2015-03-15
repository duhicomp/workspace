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

def list_dir_entry(wd, p_state,file_q):
#     start_t=datetime.datetime.now()
    list_dir(wd, p_state, file_q)
#     listdir_elapsed_t = datetime.datetime.now() - start_t
    p_state= 4
#     file_q.close()
    
def list_dir(wd, file_q, p_state):
    rootdir = wd
    try:
        
        for files in os.listdir(rootdir):
            filePath=os.path.join(rootdir,files)
            if os.path.isdir(filePath):
                list_dir(filePath, file_q,p_state)
            else:
                print("Appending file to the list :" + filePath)
                file_q.append(filePath)
                
    except:
        p_state= 3    
    return


def calc_hash(file_q, result_q, p_state):
    print('size of the queue =' + str(len(file_q)))
#     while True:
    for i in range(len(file_q)):
        file_to_hash_path = file_q[i]
        print("Calculating the filesize of: " + file_to_hash_path)
        with open(file_to_hash_path, 'rb') as f:
            hash_t_start = datetime.datetime.now()
            sha1 = hashlib.sha224()
            while True:
                data =  f.read(4096 * 10)
                if not data:
                    break
                sha1.update(data)
        line = [ str(i),str(os.path.getsize(file_to_hash_path) ),file_to_hash_path, str(sha1.hexdigest()),str(datetime.datetime.now()-hash_t_start)]
        line_str = "\t".join(line)
        result_q.append(line_str)

        if p_state== 4:
            p_state = 5
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
            if p_state == 5:
                print("updating the state to 6")
                p_state = 6
                break   
            1
    print("eXITING")


if __name__=="__main__":
    files_to_hash_q=[]
    output_q=[]
    p_state=0
    
    WD= b"D:\\"
    out_file="D:\CODE\\results_out.log"
    
    list_dir_entry(WD,files_to_hash_q,p_state)      # start 4 worker processes
    calc_hash(files_to_hash_q,output_q,p_state)
    hash_result_writer(output_q,p_state,out_file)
    

    
    