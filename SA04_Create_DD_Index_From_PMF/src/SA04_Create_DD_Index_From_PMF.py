'''
Created on Mar 12, 2015

@author: mabdul-aziz
'''
import xml.etree.ElementTree as ET
import logging
import os
import datetime

def set_logging():
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
    return logger
    
def parse_pmf(self,logger):
    indir= "../resources/in"
    for pmf_file in os.listdir(indir):
        logger.info("Parsing input PMF file:" + os.path.join(indir,pmf_file))
        pmf_tree = ET.parse(os.path.join(indir,pmf_file))
        
        

if __name__ == "__main__":
    mylogger = set_logging()
    parse_pmf(mylogger)
    