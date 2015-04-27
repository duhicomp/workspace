'''
Created on Mar 27, 2015

@author: Duhi
'''
from cgitb import html
'''
CREATE TABLE episode (
        id INTEGER PRIMARY KEY NOT NULL,                                #1
        podcast_id INTEGER NOT NULL,                                    #2
        title TEXT NOT NULL DEFAULT '',                                 #3   
        description TEXT NOT NULL DEFAULT '',                           #4
        url TEXT NOT NULL,                                              #5
        published INTEGER NOT NULL DEFAULT 0,                           #6
        guid TEXT NOT NULL,                                             #7
        link TEXT NOT NULL DEFAULT '',                                  #8   
        file_size INTEGER NOT NULL DEFAULT 0,                           #9
        mime_type TEXT NOT NULL DEFAULT 'application/octet-stream',     #10
        state INTEGER NOT NULL DEFAULT 0,                               #11 
        is_new INTEGER NOT NULL DEFAULT 0,                              #12
        archive INTEGER NOT NULL DEFAULT 0,                             #13  
        download_filename TEXT NULL DEFAULT NULL,                       #14 
        total_time INTEGER NOT NULL DEFAULT 0,                          #15
        current_position INTEGER NOT NULL DEFAULT 0,                    #16
        current_position_updated INTEGER NOT NULL DEFAULT 0,            #17
        last_playback INTEGER NOT NULL DEFAULT 0,                       #18
        payment_url TEXT NULL DEFAULT NULL                              #19  
    )
'''
eposide_lst=[]
eposide_dict={
              'id':'',                          #1 
              'podcast_id':'',                  #2
              'title':'',                       #3
              'description':'',                 #4
              'url':'',                         #5
              'puplished':'',                   #6
              'guid':'',                        #7
              'link':'',                        #8
              'file_size':'',                   #9
              'mime_type':'audio/mpeg',         #10
              'state':'1',                      #11
              'is_new':'1',                     #12
              'archive':'0',                    #13
              'download_filename':'',           #14
              'total_time':'',                  #15
              'currnet_position':'0',           #16               
              'current_position_updated':'0',   #17
              'last_playback':'',               #18
              'payment_url':''                  #19
              }
import os
import logging
from pygoogle import pygoogle
import datetime
import time
import urllib2
from bs4 import BeautifulSoup 
import sqlite3

def get_webpage(page_url, my_logger):
    
    response = urllib2.urlopen(page_url)

    # Get the URL. This gets the real URL. 
#     my_logger("The URL is: ", response.geturl())
    # Getting the code
#     my_logger("This gets the code: ", response.code)
    # Get the Headers. 
    # This returns a dictionary-like object that describes the page fetched, 
    # particularly the headers sent by the server
#     my_logger("The Headers are: ", response.info())
#     Get the date part of the header
#     my_logger("The Date is: ", response.info()['date'])
    # Get the server part of the header
#     my_logger("The Server is: ", response.info()['server'])
    
    pod_html = response.read()
    return pod_html
def get_info_from_html(html_mem, html_parse_logger):
    html_soup = BeautifulSoup(html_mem)
#     html_parse_logger.info(html_soup.prettify())
#     html_soup.find(id="class")
    
    #<div class="date">Apr 27, 2012</div>
    
    for div in html_soup.find_all('div', attrs='date'):
        html_parse_logger.info(div)
        if '2014' not in str(div) and '20152' not in str(div):
            podcast_date= str(div).strip("</div>").strip('<div class="date">')
            html_parse_logger.info('Podcast Date=' + podcast_date)
    html_soup.body.find('div',attrs={'class':'date'}).text 
    description = html_soup.body.find('div', attrs={'class':'description'}).text
    html_parse_logger.info(description)
    return podcast_date, description
    
def set_logger():
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    log_filename = '../log/add_podcast_' + cur_date_s 
    
    fh = logging.FileHandler(log_filename )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_formatter)
    
    my_logger.addHandler(ch)
    my_logger.addHandler(fh)
    
    return my_logger

if __name__ == "__main__":
    
    cur_date_s=str(datetime.date.today()).replace("-","")
    
    logger = set_logger() 
        
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
        
        pod_html= get_webpage(podcast_desc_url,logger)
        # <img src="//hw1.thisamericanlife.org/sites/default/files/imagecache/large_square/episodes/463_lg.jpg" alt="463: Mortal Vs. Venial" title="" width="200" height="200" class="imagecache imagecache-large_square"/>      </div>
        #              <h1 class="node-title">463: Mortal Vs. Venial</h1>
        #      <div class="date">Apr 27, 2012</div>
        
        logger.debug("****************************************** Description Page Contents: BEGIN ******************************************")
        logger.debug("\t\t"  + str(pod_html))
        logger.debug("****************************************** Description Page Contents: END   ******************************************")
        podcast_date, podcast_description = get_info_from_html(pod_html,logger)
        
        logger.debug("****************************************** Description Description and Date: BEGIN ******************************************")
        logger.debug("\t\t"  + str(podcast_description))
        logger.debug("\t\t"  + str(podcast_date))
        logger.debug("****************************************** Description Description and Date: END   ******************************************")
        #now I need to read this part of the html (pod_html)
        #<img src="//hw1.thisamericanlife.org/sites/default/files/imagecache/large_square/episodes/463_lg.jpg" alt="463: Mortal Vs. Venial" title="" width="200" height="200" class="imagecache imagecache-large_square"/>      </div>
        #<h1 class="node-title">463: Mortal Vs. Venial</h1>
        #<div class="date">Apr 27, 2012</div>
        #<div class="description">
        #Religion makes it pretty clear what differentiates mortal sins from venial ones. Mortal are the really bad sins and venial the lesser ones. But in our everyday lives, it can be really difficult to determine just how bad we've been. This week we have stories of people trying to figure out that question.      </div>
        
        del search_urls
        del pod_html
        time.sleep(60)
    logger.debug("++++++++++++++++++++++++++++++++++++++++++++++ Searched files ++++++++++++++++++++++++++++++++++++++++++++++")
    logger.debug(str(podcasts_lst))
    logger.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    