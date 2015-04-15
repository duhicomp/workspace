'''
Created on Mar 27, 2015

@author: Duhi
'''
'''
CREATE TABLE episode (
        id INTEGER PRIMARY KEY NOT NULL,
        podcast_id INTEGER NOT NULL,
        title TEXT NOT NULL DEFAULT '',
        description TEXT NOT NULL DEFAULT '',
        url TEXT NOT NULL,
        published INTEGER NOT NULL DEFAULT 0,
        guid TEXT NOT NULL,
        link TEXT NOT NULL DEFAULT '',
        file_size INTEGER NOT NULL DEFAULT 0,
        mime_type TEXT NOT NULL DEFAULT 'application/octet-stream',
        state INTEGER NOT NULL DEFAULT 0,
        is_new INTEGER NOT NULL DEFAULT 0,
        archive INTEGER NOT NULL DEFAULT 0,
        download_filename TEXT NULL DEFAULT NULL,
        total_time INTEGER NOT NULL DEFAULT 0,
        current_position INTEGER NOT NULL DEFAULT 0,
        current_position_updated INTEGER NOT NULL DEFAULT 0,
        last_playback INTEGER NOT NULL DEFAULT 0,
        payment_url TEXT NULL DEFAULT NULL
    )
'''

import os
import logging
from pygoogle import pygoogle
import datetime
import time
if __name__ == "__main__":
    
    cur_date_s=str(datetime.date.today()).replace("-","")
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    log_filename = '../log/add_podcast_' + cur_date_s 
    fh = logging.FileHandler(log_filename )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
        
    #search_q="This American life 454"
    #search_req =pygoogle.pygoogle(log_level=logging.DEBUG,query=search_q,pages=1, hl="en")
    #search_req.display_results()
    
    root_path=r"\\Test_centos\raid5\Podcasts"
    podcasts_path =os.path.join(root_path, r"This American Life - 2012 - Complete Season - Episodes 454-482")
    gpodder_path = os.path.join(root_path, "Gpodder")
    db_path= os.path.join(gpodder_path + "Database")
    
    db_podcast_id = "2"
    db_podcast_state = "1"
    db_podcast_is_new = "1"
    db_podcast_archived = "0"
    db_podcast_total_time = "" #???? method to get the total time of an mp3
    db_podcast_cur_pos= "0"
    db_podcast_cur_pos_update = "0"
    db_podcast_last_plybck = "0"
    db_podcast_pyment_url = ""
    
    logger.debug("about to list the directory: " + podcasts_path)
    #TODO: check if you are logged into the SMB partition, if no, then log in
    podcasts_lst=os.listdir(podcasts_path)
    logger.debug(podcasts_lst)
    for pods in podcasts_lst:
        
        db_podcast_download_filename = pods
        logger.debug("Podcast filename:" + db_podcast_download_filename) 
        podcast_num = pods
        logger.debug("Podcast number:" + podcast_num )
        db_podcast_filesize = os.path.getsize(os.path.join(podcasts_path, pods))
        logger.debug("Podcast filesize:" + str(db_podcast_filesize))
        eposid_num=str(pods.split()[0])
        logger.debug("Podcast eposide number:" + eposid_num)
        db_podcast_title= " ".join(pods.split('_')[0].split()[1:])
        logger.debug("Podcast Title:" + db_podcast_title)

        
        search_q=pods
        logger.debug("Searching: " + pods)
        search_req =pygoogle.pygoogle(log_level=logging.DEBUG,query=search_q,pages=1, hl="en", my_logger=logger)
        #logger.debug("##########################################  Search Results: BEGIN ##########################################")
        #search_req.display_results()
        #logger.debug("##########################################  Search Results: END   ##########################################")
        
        search_urls = search_req.get_urls()
        logger.debug("Returned URLs from search:" + str(search_urls))
        
        for url_elem in search_urls:
            split_url_elem_lst = url_elem .split("/")
            logger.debug("Splitted url: " + str(split_url_elem_lst))
            if split_url_elem_lst[2] == "www.thisamericanlife.org":
                if len(split_url_elem_lst) > 3 and  split_url_elem_lst[3] == "radio-archives": 
                    if len(split_url_elem_lst) > 5 and eposid_num ==split_url_elem_lst[5]:# and ("www.thisamericanlife.org" in url_elem) and (db_podcast_title in url_elem):
                        podcast_desc_url=url_elem
                        break
        logger.debug("****************************************** Description URL ******************************************")
        logger.debug("\t\t"  + str(podcast_desc_url))
        logger.debug("*****************************************************************************************************")
        #get content of search_urls[0]
        del search_q
        time.sleep(60)
    logger.debug("++++++++++++++++++++++++++++++++++++++++++++++ Searched files ++++++++++++++++++++++++++++++++++++++++++++++")
    logger.debug(str(podcasts_lst))
    logger.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    