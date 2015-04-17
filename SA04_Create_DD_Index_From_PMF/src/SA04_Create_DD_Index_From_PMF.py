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
    
    log_filename = '../resources/out/generate_param_' + cur_date_s 
    fh = logging.FileHandler(log_filename )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_formatter)
    
    logger.addHandler(ch)
    #logger.addHandler(fh)
    return logger

def check_pmf(pmf_logger):
    return
    
def parse_pmf(pmf_logger):
    indir= "../resources/in"
    for pmf_file in os.listdir(indir):
        pmf_logger.info("Parsing input PMF file:" + os.path.join(indir,pmf_file))
        pmf_tree = ET.parse(os.path.join(indir,pmf_file))
        pmf_root=pmf_tree.getroot()
        #documents_root
        #inserts_root
        #Delivery Addresses
        #other tags
        for pmf_child in pmf_root:
            #pmf_logger.info("PMF TAG:" + pmf_child.tag + " PMF Text:" + str(pmf_child.text))
            if pmf_child.tag == "Documents":
                pmf_documents_root = pmf_child
                for pmf_documents_document_tag in pmf_documents_root:
                    pmf_documents_document_root = pmf_documents_document_tag
                    for  pmf_documents_document_tag in pmf_documents_document_root:
                        pmf_logger.info("DOCUMENT TAG:" + pmf_documents_document_tag.tag + " DOCUMENT Text:" + str(pmf_documents_document_tag.text))
                    
                    
            if pmf_child.tag == "Inserts":
                pmf_inserts_root = pmf_child
                for pmf_insertes_Insert_tag in pmf_inserts_root:
                    pmf_inserts_insert_root = pmf_inserts_insert_tag    
            if pmf_child.tag == "DeliveryAddresses":
                pmf_Inserts_root = pmf_child
                    
        

if __name__ == "__main__":
    mylogger = set_logging()
    check_pmf(mylogger)
    parse_pmf(mylogger)
    