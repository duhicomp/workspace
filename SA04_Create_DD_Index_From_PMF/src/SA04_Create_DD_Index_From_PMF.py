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
                pmf_logger.info("Documents Tag")
                for pmf_documents_document_tag in pmf_documents_root:
                    doc_id_cnt = 0
                    file_path_cnt = 0
                    TBC_cnt = 0 
                    PBF_cnt = 0
                    PTP1_cnt = 0
                    PTO_cnt = 0 
                    PCT_cnt = 0
                    doc_name_cnt = 0
                    doc_tid_cnt = 0
                    #TODO: Implement app_param ass a dictionary
                    pmf_param={}
                    pmf_documents = {}
                    pmf_inserts = {}
                    pmf_delivery_addresses = {}
                    
                    pmf_documents_document_root = pmf_documents_document_tag
                    for  pmf_documents_document_tag in pmf_documents_document_root:
                        pmf_logger.info("DOCUMENT TAG:" + pmf_documents_document_tag.tag + " DOCUMENT Text:" + str(pmf_documents_document_tag.text))
                        if pmf_documents_document_tag.tag == "Id":
                            #TODO: Add cur_doc_Id to app_param
                            cur_doc_Id = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            doc_id_cnt += 1
                            pmf_logger.info("Captured the value Document Id:" + cur_doc_Id)
                        if pmf_documents_document_tag.tag == "FilePath":
                            #TODO: Add cur_doc_file_path to app_param
                            cur_doc_file_path = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            file_path_cnt += 1
                            
                        if pmf_documents_document_tag.tag == "ThreeByteCode":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_TBC = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            TBC_cnt += 1
                            
                        if pmf_documents_document_tag.tag == "PreBatchFormat":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_PBF = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            PBF_cnt += 1
                            
                        if pmf_documents_document_tag.tag == "PaperTypePage1":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_PTP1 = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            PTP1_cnt += 1
                        if pmf_documents_document_tag.tag == "PaperTypeOther":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_pto = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            PTO_cnt += 1
                        if pmf_documents_document_tag.tag == "PageCount":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_pct = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            PCT_cnt += 1
                        if pmf_documents_document_tag.tag == "Name":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_name = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            doc_name_cnt += 1
                        if pmf_documents_document_tag.tag == "TypeIdentfier":
                            #TODO: Add cur_doc_TBC to app_param
                            cur_doc_tid = pmf_documents_document_tag.text
                            pmf_documents[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                            doc_tid_cnt += 1
                            
                if doc_id_cnt > 1:
                    pmf_logger.error("More than 1 Document <Id> found in the input PMF, check Document <Id>:" + pmf_documents['Id'])
                    raise Exception("More than 1 Document <Id> found in the input PMF, check Document <Id>:" + pmf_documents['Id'])
                if file_path_cnt > 1:
                    pmf_logger.error("More than 1 Document <FilePath> found in the input PMF, check Document <FilePath>:" + pmf_documents['FilePath'])
                    raise Exception("More than 1 Document <FilePath> found in the input PMF, check Document <FilePath>:" + pmf_documents['FilePath'])
                if TBC_cnt > 1:
                    pmf_logger.error("More than 1 Document <ThreeByteCode> found in the input PMF, check Document <ThreeByteCode>:" + pmf_documents['ThreeByteCode'])
                    raise Exception("More than 1 Document <ThreeByteCode> found in the input PMF, check Document <ThreeByteCode>:" + pmf_documents['ThreeByteCode'])
                if PBF_cnt > 1:
                    pmf_logger.error("More than 1 Document <PreBatchFormat> found in the input PMF, check Document <PreBatchFormat>:" + pmf_documents['PreBatchFormat'])
                    raise Exception("More than 1 Document <PreBatchFormat> found in the input PMF, check Document <PreBatchFormat>:" + pmf_documents['PreBatchFormat'])
                if PTP1_cnt > 1:
                    pmf_logger.error("More than 1 Document <PaperTypePage1> found in the input PMF, check Document <PaperTypePage1>:" + pmf_documents['PaperTypePage1'])
                    raise Exception("More than 1 Document <PaperTypePage1> found in the input PMF, check Document <PaperTypePage1>:" + pmf_documents['PaperTypePage1'])
                if PTO_cnt > 1:
                    pmf_logger.error("More than 1 Document <PageTypeOther> found in the input PMF, check Document <PageTypeOther>:" + pmf_documents['PageTypeOther'])
                    raise Exception("More than 1 Document <PageTypeOther> found in the input PMF, check Document <PageTypeOther>:" + pmf_documents['PageTypeOther'])
                if PCT_cnt > 1:
                    pmf_logger.error("More than 1 Document <PageCount> found in the input PMF, check Document <PageCount>:" + pmf_documents['PageCount'])
                    raise Exception("More than 1 Document <PageCount> found in the input PMF, check Document <PageCount>:" + pmf_documents['PageCount'])
                if doc_name_cnt > 1:
                    pmf_logger.error("More than 1 Document <Name> found in the input PMF, check Document <Name>:" + pmf_documents['Name'])
                    raise Exception("More than 1 Document <Name> found in the input PMF, check Document <Name>:" + pmf_documents['Name'])
                if doc_tid_cnt > 1:
                    pmf_logger.error("More than 1 Document <TypeIdentfier> found in the input PMF, check Document <TypeIdentfier>:" + pmf_documents['TypeIdentfier'])
                    raise Exception("More than 1 Document <TypeIdentfier> found in the input PMF, check Document <TypeIdentfier>:" + pmf_documents['TypeIdentfier'])
            pmf_logger.debug("pmf_documents dictionary contents:\n" + str(pmf_documents))        
            
            if pmf_child.tag == "Inserts":
                pmf_inserts_root = pmf_child
                pmf_logger.info("Inserts Tag")
                for pmf_insertes_Insert_tag in pmf_inserts_root:
                    pmf_inserts_insert_root = pmf_insertes_Insert_tag
                    #init count values in here
                    insert_name_cnt = 0
                    
                    for  pmf_inserts_insert_tag in pmf_inserts_insert_root:
                        pmf_logger.debug("Insert TAG:" + pmf_inserts_insert_tag.tag + " Insert Text:" + str(pmf_inserts_insert_tag.text))
                        if pmf_inserts_insert_tag.tag == "Name":
                            #TODO: Add cur_doc_Id to app_param
                            cur_insert_name = pmf_documents_document_tag.text
                            pmf_inserts[pmf_inserts_insert_tag.tag] = pmf_inserts_insert_tag.text
                            insert_name_cnt += 1
                            pmf_logger.info("Captured the value Insert Name:" + cur_insert_name)
                        
                    if insert_name_cnt > 1:
                        pmf_logger.error("More than 1 insert <Name> found in the input PMF, check insert <Name>:" + pmf_inserts['Name'])
                        raise Exception("More than 1 insert <Name> found in the input PMF, check insert <Name>:" + pmf_inserts['Name'])
                    
            if pmf_child.tag == "DeliveryAddresses":
                pmf_delivery_add_root = pmf_child
                pmf_logger.info("Delivery Addresses")
                for delivery_addresses_tag in pmf_delivery_add_root:
                    pmf_delivery_addresses_address_root = delivery_addresses_tag
                    #init count variables here
                    deliveyr_address_Id_cnt = 0
                    deliveyr_address_addressee_cnt = 0
                    deliveyr_address_primary_addr_cnt = 0
                    deliveyr_address_secondary_addr_cnt = 0
                    deliveyr_address_city_cnt = 0
                    deliveyr_address_state_cnt = 0
                    deliveyr_address_zip_cnt = 0
                    
                    for  pmf_delivery_addrs_address_tag in pmf_delivery_addresses_address_root:
                        pmf_logger.info("Delivery Address TAG:" + pmf_delivery_addrs_address_tag.tag  + " Delivery Address Text:" + str(pmf_delivery_addrs_address_tag.text))    
                        if pmf_delivery_addrs_address_tag.tag == "Id":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_Id= pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_Id_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address Id:" + delviery_address_Id)
                        if pmf_delivery_addrs_address_tag.tag == "Addressee":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_addressee = pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_addressee_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address Addressee:" + delviery_address_addressee)
                        
                        if pmf_delivery_addrs_address_tag.tag == "PrimaryAddress":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_primary_addr= pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_primary_addr_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address PrimaryAddress:" + delviery_address_primary_addr)
                        
                        if pmf_delivery_addrs_address_tag.tag == "SecondaryAddress":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_secondary_addr= pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_secondary_addr_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address SecondaryAddress:" + delviery_address_secondary_addr)
                        
                        if pmf_delivery_addrs_address_tag.tag == "City":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_city = pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_city_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address City:" + delviery_address_city)
                        
                        if pmf_delivery_addrs_address_tag.tag == "State":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_state = pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_state_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address State:" + delviery_address_state)
                        
                        if pmf_delivery_addrs_address_tag.tag == "Zip":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_zip = pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_zip_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address Zip:" + delviery_address_zip)
                        
                        if pmf_delivery_addrs_address_tag.tag == "Zip":
                            #TODO: Add cur_doc_Id to app_param
                            delviery_address_zip = pmf_delivery_addrs_address_tag.text
                            pmf_inserts[pmf_delivery_addrs_address_tag.tag] = pmf_delivery_addrs_address_tag.text
                            deliveyr_address_zip_cnt += 1
                            pmf_logger.info("Captured the value Delivery Address Zip:" + delviery_address_zip)
                            
                    if deliveyr_address_Id_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <Id> found in the input PMF, check Delivery Address <Id>:" + pmf_inserts['Id'])
                        raise Exception("More than 1 Delivery Address <Id> found in the input PMF, check Delivery Address <Id>:" + pmf_inserts['Id'])
                    
                    if deliveyr_address_addressee_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <Addressee> found in the input PMF, check Delivery Address <Addressee>:" + pmf_inserts['Addressee'])
                        raise Exception("More than 1 Delivery Address <Addressee> found in the input PMF, check Delivery Address <Addressee>:" + pmf_inserts['Addressee'])
                    
                    if deliveyr_address_primary_addr_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <PrimaryAddress> found in the input PMF, check Delivery Address <PrimaryAddress>:" + pmf_inserts['PrimaryAddress'])
                        raise Exception("More than 1 Delivery Address <PrimaryAddress> found in the input PMF, check Delivery Address <PrimaryAddress>:" + pmf_inserts['PrimaryAddress'])
                    
                    if deliveyr_address_secondary_addr_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <SecondaryAddress> found in the input PMF, check Delivery Address <SecondaryAddress>:" + pmf_inserts['SecondaryAddress'])
                        raise Exception("More than 1 Delivery Address <SecondaryAddress> found in the input PMF, check Delivery Address <SecondaryAddress>:" + pmf_inserts['SecondaryAddress'])
                    if deliveyr_address_city_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <City> found in the input PMF, check Delivery Address <City>:" + pmf_inserts['City'])
                        raise Exception("More than 1 Delivery Address <City> found in the input PMF, check Delivery Address <City>:" + pmf_inserts['City'])
                    if deliveyr_address_state_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <State> found in the input PMF, check Delivery Address <State>:" + pmf_inserts['State'])
                        raise Exception("More than 1 Delivery Address <State> found in the input PMF, check Delivery Address <State>:" + pmf_inserts['State'])
                    if deliveyr_address_zip_cnt > 1:
                        pmf_logger.error("More than 1 Delivery Address <Zip> found in the input PMF, check Delivery Address <Zip>:" + pmf_inserts['Zip'])
                        raise Exception("More than 1 Delivery Address <Zip> found in the input PMF, check Delivery Address <Zip>:" + pmf_inserts['Zip'])
                    
if __name__ == "__main__":
    mylogger = set_logging()
    check_pmf(mylogger)
    parse_pmf(mylogger)
    