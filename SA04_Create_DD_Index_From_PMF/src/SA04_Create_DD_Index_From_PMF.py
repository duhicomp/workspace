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
        documents_tag_dict = {'Id': 0, 'FilePath': 0 , 'ThreeByteCode': 0, 'PreBatchFormat': 0,'PaperTypePage1':0, 'PaperTypeOther':0, 'PageCount':0, 'Name':0, 'TypeIdentifier':0}
        delivery_address_tag_dict ={'Id':0, 'Addressee':0, 'PrimaryAddress':0, 'SecondaryAddress':0,'City':0, 'State':0, 'Zip':0, 'DeliveryMatchesMailingAddress':0, 'SerialNumber':0, 'RoutingCode':0}
        inserts_tag_dict = {'Name':0}
        
        for pmf_child in pmf_root:
            #pmf_logger.info("PMF TAG:" + pmf_child.tag + " PMF Text:" + str(pmf_child.text))
            pmf_param={}
            pmf_document = {}
            pmf_inserts = {}
            pmf_delivery_addresses = {}

            if pmf_child.tag == "Documents":
                pmf_documents_root = pmf_child
                pmf_logger.info("Documents Tag")
                for pmf_documents_document_tag in pmf_documents_root:
                    

                    pmf_documents_document_root = pmf_documents_document_tag
                    for  pmf_documents_document_tag in pmf_documents_document_root:
                        pmf_logger.info("DOCUMENT TAG:" + pmf_documents_document_tag.tag + " DOCUMENT Text:" + str(pmf_documents_document_tag.text))
                        if pmf_documents_document_tag.tag in list(documents_tag_dict.keys()):
                            pmf_document[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            documents_tag_dict[pmf_documents_document_tag.tag] += 1
                            
                for dict_keys in list(pmf_documents_document_tag.keys()):
                        if documents_tag_dict[dict_keys] > 1:
                            raise Exception('Check the <DeliveryAddress> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                        documents_tag_dict[dict_keys] = 0
                
                pmf_logger.info("pmf_documents dictionary contents:\n" + str(pmf_document))
                #TODO: Need to add the pmf_documents to the pmf_param so that if we have multiple Document iteration we keep a record of it
            
            if pmf_child.tag == "Inserts":
                pmf_inserts_root = pmf_child
                pmf_logger.info("Inserts Tag")
                for pmf_insertes_Insert_tag in pmf_inserts_root:
                    pmf_inserts_insert_root = pmf_insertes_Insert_tag
                    
                    for  pmf_inserts_insert_tag in pmf_inserts_insert_root:
                        pmf_logger.debug("Insert TAG:" + pmf_inserts_insert_tag.tag + " Insert Text:" + str(pmf_inserts_insert_tag.text))
                        if pmf_inserts_insert_tag.tag in list(inserts_tag_dict.keys()):
                            pmf_inserts[pmf_inserts_insert_tag.tag] = pmf_inserts_insert_tag.text
                            inserts_tag_dict[pmf_inserts_insert_tag.tag] += 1
                    
                    for dict_keys in list(inserts_tag_dict.keys()):
                        if inserts_tag_dict[dict_keys] > 1:
                            raise Exception('Check the <DeliveryAddress> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                        inserts_tag_dict[dict_keys] = 0
                        
                    pmf_logger.info("pmf_inserts dictionary contents:\n" + str(pmf_inserts))
                    #TODO: Need to add the pmf_inserts to the pmf_param so that if we have multiple Document iteration we keep a record of it
            if pmf_child.tag == "DeliveryAddresses":
                pmf_delivery_add_root = pmf_child
                pmf_logger.info("Delivery Addresses")
                for delivery_addresses_tag in pmf_delivery_add_root:
                    pmf_delivery_addresses_address_root = delivery_addresses_tag
                    for  pmf_delivery_addrs_address_tag in pmf_delivery_addresses_address_root:
                        pmf_logger.info("Delivery Address TAG:" + pmf_delivery_addrs_address_tag.tag  + " Delivery Address Text:" + str(pmf_delivery_addrs_address_tag.text))
                        if pmf_delivery_addrs_address_tag.tag in list(delivery_address_tag_dict.keys()):
                            pmf_delivery_addresses[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            delivery_address_tag_dict[pmf_delivery_addrs_address_tag.tag] += 1
                    #error handling
                    #re-initialize dictionary keys
                    for dict_keys in list(delivery_address_tag_dict.keys()):
                        if delivery_address_tag_dict[dict_keys] > 1:
                            raise Exception('Check the <DeliveryAddress> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                        delivery_address_tag_dict[dict_keys] = 0
                    pmf_logger.info("pmf_delivery_addresses dictionary contents:\n" + str(pmf_delivery_addresses))
                    #TODO: Need to add the pmf_inserts to the pmf_delivery_addresses so that if we have multiple Document iteration we keep a record of it
        
        
        del pmf_document
        del pmf_inserts
        del pmf_delivery_addresses

        del documents_tag_dict
        del delivery_address_tag_dict
        del inserts_tag_dict
        
if __name__ == "__main__":
    mylogger = set_logging()
    check_pmf(mylogger)
    parse_pmf(mylogger)
    