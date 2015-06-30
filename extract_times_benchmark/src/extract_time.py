'''
Created on Feb 17, 2015

@author: mabdul-aziz
'''
'''
Created on Feb 10, 2015

@author: mabdul
'''
import os
import logging

def extract_logs(WD):
    begin_time = ''
    end_time = ''
    #WD = 'D:\\MA_Sefas\\Clients\\LibertyMutual\\LM04\\Benchmarking\\d700010_d7000012_DEV0L14P_Benchmark_Files_2'
    out_log_dir = os.path.join(WD,"OUT")
    out_log_fileName = os.path.join(out_log_dir ,"extractl")
    extract_log = os.path.join(out_log_dir ,"times_extract")
    logging.basicConfig(
                        level=logging.DEBUG,
                        datefmt='%m-%d %H:%M'
                        )
    #logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logFormatter = logging.Formatter('%(levelname)-8s %(message)s')
    rootLogger = logging.getLogger()
    
    fileHandler = logging.FileHandler( out_log_fileName + ".log", mode='w', delay=False)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    log_file='../resources/d022793-HOM0LRP3.PERF.log'
    with open(extract_log,'w') as extract_fd:
        for stage_dir in os.listdir(os.path.join(WD,'IN')):
            logging.info('in DIR:' +os.path.join(WD ,'IN', stage_dir))
            for stage_logs in os.listdir(os.path.join(WD ,'IN', stage_dir)):
                logging.info('in DIR:' +os.path.join(WD ,'IN', stage_dir,stage_logs))
                log_file = os.path.join(WD ,'IN', stage_dir,stage_logs)
                if log_file.endswith('.log'):
                    with open(log_file,'r') as logfd:
                            for log_line in logfd:
                                if "{BEGIN:" in log_line or "BEGIN: " in log_line:
                                    log_lst = log_line.split()
                                    logging.info("->".join(log_lst))
                                    extract_fd.write("->".join(log_lst) + '\n')
                                    logging.info("Time=" + str(log_lst[1]) )
                                    begin_time = str(log_lst[1])
                                    start_t_h = str(log_lst[1].split(':')[0])
                                    start_t_m = str(log_lst[1].split(':')[1])
                                    start_t_s = str(str(log_lst[1].split(':')[2]).split(',')[0])
                                    start_t_ms = str(str(log_lst[1].split(':')[2]).split(',')[1])
                                elif "{END" in log_line or "END: " in log_line:
                                    log_lst = log_line.split()
                                    logging.info("->".join(log_lst))
                                    extract_fd.write("->".join(log_lst) + '\n')
                                    end_time = str(log_lst[1])
                                    end_t_h = str(log_lst[1].split(':')[0])
                                    end_t_m = str(log_lst[1].split(':')[1])
                                    end_t_s = str(str(log_lst[1].split(':')[2]).split(',')[0])
                                    end_t_ms = str(str(log_lst[1].split(':')[2]).split(',')[1])
                                    
                                    delta_t_ms = (1000 *((int(end_t_h) * 60 * 60) + (int(end_t_m) *60) + int(end_t_s) ) + int(end_t_ms)) - (1000 *((int(start_t_h) * 60 * 60) + (int(start_t_m) *60) + int(start_t_s) ) + int(start_t_ms)) 
                                    logging.info('delta_t_ms = ' + str(delta_t_ms))  
                                    extract_fd.write('delta_t_ms = ' + str(delta_t_ms) + "\n")
                                    
                                    delta_t_s = float(delta_t_ms)/1000
                                    logging.info('delta_t_s = ' + str(delta_t_s))  
                                    extract_fd.write('delta_t_s = ' + str(delta_t_s) + "\n")
                                    if delta_t_s > 60.00:
                                        delta_t_m = int(delta_t_s/60)
                                        delta_t_s = delta_t_s - (delta_t_m * 60)
                                        logging.info('delta_t_m = ' + str(delta_t_m))  
                                        extract_fd.write('delta_t_m = ' + str(delta_t_m))
                                        logging.info('delta_t_s = ' + str(delta_t_s))  
                                        extract_fd.write('delta_t_s = ' + str(delta_t_s)) 
    logging.info('End Log file')                 
     
        
if __name__ == "__main__": 
    WD="D:\\MA_Sefas\\Clients\\LibertyMutual\\LM04\\Benchmarking\\d700010_d7000012_DEV0L14P_Benchmark_Files_2"
    extract_logs(WD)