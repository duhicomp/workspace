'''
Created on Feb 5, 2015

@author: mabdul-aziz
'''
import os
import time
import logging

#logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')



def clean_designer_jobs():
    print('The Current Time is: ' + time.ctime(currnet_time) )  
    for apps in apps_to_clean :
        logging.info("app to clean: " + apps)
        if apps in os.environ :
            path_to_clean = os.path.join(os.environ[apps],'jobs')
            logging.info('in the app directory:' + os.getenv(apps) )
            for job_folders in os.listdir(path_to_clean):
                logging.info("Evaluation the Folder: " + os.path.join(path_to_clean,job_folders) )
                #(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
                job_folder_creation_epoch_t = os.path.getctime(os.path.join(path_to_clean,job_folders))
                logging.info('Folder Creation Time is: ' +  time.ctime(job_folder_creation_epoch_t) )
                delta_t_sec = currnet_time - job_folder_creation_epoch_t
                logging.info('The Time difference between now, and creation date is=' + str(delta_t_sec ) + 'sec' )
                logging.info('in case you are wondering, that is=' + str(delta_t_sec/(60*60*24)) + 'days)' )
                if delta_t_sec > jobs_older_than*60*60*24:
                    logging.info("Deleting the Folder: " + os.path.join(path_to_clean,job_folders) )
                    os.unlink(os.path.join(path_to_clean,job_folders))
                else:
                    logging.info("No folder to be deleted at this time")
                #os.system('rmdir /s /q "%s"' % os.path.join(path_to_clean,job_folders))
        else:
            logging.info('error no key: ' + apps + 'in os.environ')
        
if __name__ == "__main__":
    
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    #rootLogger = logging.getLogger()
    #fileHandler = logging.FileHandler("{0}/{1}.log".format('../resources', 'clean_designer_job_dir'))
    #fileHandler.setFormatter(logFormatter)
    #rootLogger.addHandler(fileHandler)
    
    #consoleHandler = logging.StreamHandler()
    #consoleHandler.setFormatter(logFormatter)
    #rootLogger.addHandler(consoleHandler)
    
    
    logging.basicConfig(
                        filename="../resources/clean_designer_jobdir",
                        level=logging.DEBUG,
                        datefmt='%m-%d %H:%M'
                        )

    apps_to_clean=['DS','DR','DE']
    
    currnet_time = time.time()

    #jobs_older_than resolution is in days
    jobs_older_than = 3
    logging.info('Calling clean_designer_jobs()')
    try:
        clean_designer_jobs()
    except:
        logging.info('something went wrong when trying to call clean_designer_jobs()')
