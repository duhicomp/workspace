

from HTMLParser import HTMLParser
import logging
import os
import datetime
from bs4 import BeautifulSoup 

#from xml.dom.minidom import parse, parseString

def set_logger():
    cur_date_s=str(datetime.date.today()).replace("-","")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    log_filename = '../log/parse_html_' + cur_date_s 
    fh = logging.FileHandler(log_filename )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_formatter)
    
    logger.addHandler(ch)
    #logger.addHandler(fh)
    return logger
class MonHTMLParser(HTMLParser):
    def handle_startendtag(self, tag, attrs):
        print("ecnountered tag:" + tag)
        for attrs_iter in attrs:
            print("current attrs:" + str(attrs_iter))
            
        
        
    
if __name__== "__main__":
    in_html = "../resources/parse_this_html.html"
    
    #dom1 = parse(in_html) # parse an XML file by name
    


    
    html_fd = open(in_html,"r")
    html_mem = html_fd.read()
    html_parse_logger = set_logger()
    html_parse_logger.info("Parsing The html file :" + in_html)

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
    #<div class="description">
    #Religion makes it pretty clear what differentiates mortal sins from venial ones. Mortal are the really bad sins and venial the lesser ones. But in our everyday lives, it can be really difficult to determine just how bad we've been. This week we have stories of people trying to figure out that question.      </div>
    #</div>
    #html_parse_logger.info(html_soup.body.find('div', attrs={'class':'description'}).text)
    
# CREATE TABLE episode (
#         id INTEGER PRIMARY KEY NOT NULL,
#         podcast_id INTEGER NOT NULL,
#         title TEXT NOT NULL DEFAULT '',
#         description TEXT NOT NULL DEFAULT '',
#         url TEXT NOT NULL,
#         published INTEGER NOT NULL DEFAULT 0,
#         guid TEXT NOT NULL,
#         link TEXT NOT NULL DEFAULT '',
#         file_size INTEGER NOT NULL DEFAULT 0,
#         mime_type TEXT NOT NULL DEFAULT 'application/octet-stream',
#         state INTEGER NOT NULL DEFAULT 0,
#         is_new INTEGER NOT NULL DEFAULT 0,
#         archive INTEGER NOT NULL DEFAULT 0,
#         download_filename TEXT NULL DEFAULT NULL,
#         total_time INTEGER NOT NULL DEFAULT 0,
#         current_position INTEGER NOT NULL DEFAULT 0,
#         current_position_updated INTEGER NOT NULL DEFAULT 0,
#         last_playback INTEGER NOT NULL DEFAULT 0,
#         payment_url TEXT NULL DEFAULT NULL
#     )