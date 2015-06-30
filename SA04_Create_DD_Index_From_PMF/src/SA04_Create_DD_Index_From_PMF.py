'''
Created on Mar 12, 2015

@author: mabdul-aziz
'''
import xml.etree.ElementTree as ET
import logging
import os
import datetime
import pickle

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
        if pmf_file.endswith(".xml"):
            pmf_logger.info("Parsing input PMF file:" + os.path.join(indir,pmf_file))
            pmf_tree = ET.parse(os.path.join(indir,pmf_file))
            pmf_root=pmf_tree.getroot()
    
            pmf_param={
                       'docs':[], 
                       'inserts':[],
                       'delviery_addresses':[],
                       'Id':'',
                       'PolicyIdentifier':'',
                       'State':'',
                       'MasterId':'',
                       'JobType':'',
                       'Database':'',
                       'SpanishLanguage':'',
                       'InsertPageCountEquivalent':'',
                       'BarcodeID':'',
                       'ServiceTypeID':'',
                       'MailerID':''
                       }
            
            documents_tag_dict = {'Id': 0, 'FilePath': 0 , 'ThreeByteCode': 0, 'PreBatchFormat': 0,'PaperTypePage1':0, 'PaperTypeOther':0, 'PageCount':0, 'Name':0, 'TypeIdentifier':0}
            delivery_address_tag_dict ={'Id':0, 'Addressee':0, 'PrimaryAddress':0, 'SecondaryAddress':0,'City':0, 'State':0, 'Zip':0, 'DeliveryMatchesMailingAddress':0, 'SerialNumber':0, 'RoutingCode':0}
            inserts_tag_dict = {'Name':0}
            pmf_tag_dict={'Id': 0,'PolicyIdentifier': 0, 'State': 0, 'MasterId':0, 'JobType':0, 'Database':0, 'SpanishLanguage':0, 'InsertPageCountEquivalent':0, 'BarcodeID':0,'ServiceTypeID': 0, 'MailerID': 0}
            pmf_document={}
            pmf_inserts={}
            pmf_delivery_addresses={}
            for pmf_child in pmf_root:
                if pmf_child.tag == "Documents":
                    pmf_documents_root = pmf_child
                    pmf_logger.info("Documents Tag")
                    for pmf_documents_document_tag in pmf_documents_root:
                        pmf_document = {}
                        pmf_documents_document_root = pmf_documents_document_tag
                        for  pmf_documents_document_tag in pmf_documents_document_root:
                            pmf_logger.info("DOCUMENT TAG:" + pmf_documents_document_tag.tag + " DOCUMENT Text:" + str(pmf_documents_document_tag.text))
                            if pmf_documents_document_tag.tag in list(documents_tag_dict.keys()):
                                pmf_document[pmf_documents_document_tag.tag] = pmf_documents_document_tag.text
                                documents_tag_dict[pmf_documents_document_tag.tag] += 1
#                                 if pmf_documents_document_tag.tag == "FilePath":
#                                         if not os.path.exists(pmf_documents_document_tag.text):
#                                             pmf_logger.info("Unable to locate the input file:" + pmf_documents_document_tag.text)
#                                             raise("Unable to locate the input file:" + pmf_documents_document_tag.text)
#                                     
                                
                        for dict_keys in list(pmf_documents_document_tag.keys()):
                            if documents_tag_dict[dict_keys] > 1:
                                pmf_logger.info('Invalid input PMF File: Check the <Document> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                                raise Exception('Check the <Document> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                            if documents_tag_dict[dict_keys] == 0:
                                pmf_logger.info('Invalid input PMF File: The <Document> <' + dict_keys + '> tag does not exist in the input PMF file:' + os.path.join(indir,pmf_file))
                                raise Exception('Invalid input PMF File: The <Document> <' + dict_keys + '> tag does not exist in the input PMF file:' + os.path.join(indir,pmf_file))
                            documents_tag_dict[dict_keys] = 0
                            
                        pmf_logger.info("pmf_documents dictionary contents:\n" + str(pmf_document))
                        pmf_parm_lst=pmf_param['docs']
                        pmf_parm_lst.append(pmf_document)
                        del pmf_document
                        
                    pmf_logger.info("pmf_parm['docs'] dictionary contents:\n" + str(pmf_param['docs']))
                   
                    pmf_logger.info("pmf_parm dictionary contents:\n" + str(pmf_param))
                    
    
                if pmf_child.tag == "Inserts":
                    pmf_inserts_root = pmf_child
                    pmf_logger.info("Inserts Tag")
                    for pmf_insertes_Insert_tag in pmf_inserts_root:
                        #pmf_inserts = {}
                        pmf_inserts_insert_root = pmf_insertes_Insert_tag
                        
                        for  pmf_inserts_insert_tag in pmf_inserts_insert_root:
                            pmf_logger.debug("Insert TAG:" + pmf_inserts_insert_tag.tag + " Insert Text:" + str(pmf_inserts_insert_tag.text))
                            if pmf_inserts_insert_tag.tag in list(inserts_tag_dict.keys()):
                                pmf_inserts[pmf_inserts_insert_tag.tag] = pmf_inserts_insert_tag.text
                                inserts_tag_dict[pmf_inserts_insert_tag.tag] += 1
                        
                        for dict_keys in list(inserts_tag_dict.keys()):
                            if inserts_tag_dict[dict_keys] > 1:
                                pmf_logger.info('Invalid input PMF File: Check the <Insert> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                                raise Exception('Invalid input PMF File: Check the <Insert> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                            if inserts_tag_dict[dict_keys] == 0:
                                pmf_logger.info('Invalid input PMF File: The <Insert> <' + dict_keys + '> tag does not exist in the input PMF file:' + os.path.join(indir,pmf_file))
                                raise Exception('Invalid input PMF File: The <Insert> <' + dict_keys + '> tag does not exist in the input PMF file:' + os.path.join(indir,pmf_file))
                            inserts_tag_dict[dict_keys] = 0
                            
                        pmf_logger.info("pmf_inserts dictionary contents:\n" + str(pmf_inserts))
                        pmf_param['inserts'].append(pmf_inserts)
    
                    pmf_logger.info("pmf_parm['inserts'] dictionary contents:\n" + str(pmf_param['inserts']))
    
                    pmf_logger.info("pmf_parm dictionary contents:\n" + str(pmf_param))
                    
                if pmf_child.tag == "DeliveryAddresses":
                    pmf_delivery_add_root = pmf_child
                    pmf_logger.info("Delivery Addresses")
                    for delivery_addresses_tag in pmf_delivery_add_root:
                        #pmf_delivery_addresses = {}
                        pmf_delivery_addresses_address_root = delivery_addresses_tag
                        for  pmf_delivery_addrs_address_tag in pmf_delivery_addresses_address_root:
                            pmf_logger.info("Delivery Address TAG:" + pmf_delivery_addrs_address_tag.tag  + " Delivery Address Text:" + str(pmf_delivery_addrs_address_tag.text))
                            if pmf_delivery_addrs_address_tag.tag in list(delivery_address_tag_dict.keys()):
                                pmf_delivery_addresses[pmf_delivery_addrs_address_tag.tag] = str(pmf_delivery_addrs_address_tag.text if pmf_delivery_addrs_address_tag.text else '-')
                                delivery_address_tag_dict[pmf_delivery_addrs_address_tag.tag] += 1
                                
                        for dict_keys in list(delivery_address_tag_dict.keys()):
                            if delivery_address_tag_dict[dict_keys] > 1:
                                pmf_logger.info('Invalid input PMF File: Check the <DeliveryAddress> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                                raise Exception('Invalid input PMF File: Check the <DeliveryAddress> <' + dict_keys + '> tag, more than one occurance in the same iteration' )
                            if delivery_address_tag_dict[dict_keys] == 0:
                                pmf_logger.info('Invalid input PMF File: The <DeliveryAddress> <' + dict_keys + '> tag does not exist in the input PMF file:' + os.path.join(indir,pmf_file))
                                raise Exception('Invalid input PMF File: The <DeliveryAddress> <' + dict_keys + '> tag does not exist in the input PMF file:' + os.path.join(indir,pmf_file))
                            delivery_address_tag_dict[dict_keys] = 0
                            
                        pmf_logger.info("pmf_delivery_addresses dictionary contents:\n" + str(pmf_delivery_addresses))
                        pmf_param['delviery_addresses'].append(pmf_delivery_addresses)
                    pmf_logger.info("pmf_param['delviery_addresses'] dictionary contents:\n" + str(pmf_param['delviery_addresses']))
                if pmf_child.tag in list(pmf_param.keys()):
                    pmf_logger.info("Tag Name: " + pmf_child.tag + " value:" + pmf_child.text)
                    pmf_param[pmf_child.tag] = pmf_child.text
                    pmf_tag_dict[pmf_child.tag] += 1
                    pmf_logger.info("pmf_param dictionary contents:\n" + str(pmf_param))
                 
            
            for dict_keys in list(pmf_tag_dict.keys()):
                if pmf_tag_dict[dict_keys] > 1:
                    pmf_logger.info('Check the <Packet> <' + dict_keys + '> tag, more than one  in the same iteration' )
                    raise Exception('Check the <Packet> <' + dict_keys + '> tag, more than one  in the same iteration' )
                if pmf_tag_dict[dict_keys] == 0:
                    pmf_logger.info('The <Packet> <' + dict_keys + '> tag is missing in the input PMF file:' + os.path.join(indir,pmf_file))
                    raise Exception('The <Packet> <' + dict_keys + '> tag is missing in the input PMF file:' + os.path.join(indir,pmf_file))
            
            pmf_logger.info("pmf_param dictionary contents:\n" + str(pmf_param))
            
    
            del documents_tag_dict
            del delivery_address_tag_dict
            del inserts_tag_dict
    

            del pmf_inserts
            del pmf_delivery_addresses
            #TODO: write the dictionary as a pickle
            #TODO: test if we can we parse the pickle from within designer?
            #directory structure of the batching 
        if not os.path.exists('../resources/out/' + pmf_file.strip('.xml')):    
            os.mkdir('../resources/out/' + pmf_file.strip('.xml'))
        pickle_filepath = '../resources/out/' + pmf_file.strip('.xml')+ os.sep + pmf_file.strip('.xml') + '.pkl'
        dict_pickle=open(pickle_filepath,'w')
        try:
            pickle.dump(pmf_param, dict_pickle)
        except:
            pmf_logger.info('Error Writing the pickel file:' + pickle_filepath)
            raise Exception('Error Writing the pickel file:' + pickle_filepath)
        finally:
            dict_pickle.close()
    return pmf_param

def read_job_properties(file,key):
    jp_dict={}
    keys_in_seq={}
    jp_fd=open(file,'r')
    header_lst = jp_fd.readline().strip(os.linesep).split('\t')
    key_seq=0
    for headers_elem in header_lst:
        jp_dict[headers_elem ]=[]
        keys_in_seq[str(key_seq)] = headers_elem 
        key_seq+=1
         
    for jp_line in jp_fd:
        rawline=jp_line.strip(os.linesep).split('\t')
        raw_elem_cnt=0
        for rawline_elem in rawline:
            jp_dict[keys_in_seq[str(raw_elem_cnt)]].append(rawline_elem)
            raw_elem_cnt += 1
            
        
    print(str(jp_dict))
    return

def write_param_files(mon_logger, pmf_dict):
    docs_lst = pmf_dict['docs']
    inserts_lst = pmf_dict['inserts']
    delivery_addresses_lst=pmf_dict['delviery_addresses']
    cur_iter=0
    for doc_iter in docs_lst:
        mon_logger.info("current Document ID:" + doc_iter['Id'])
        doc_fd=open(os.path.join('../resources/out',doc_iter['Id']+ '.param'),'w')
        write_parameter(doc_fd,'jobtype',pmf_dict['JobType'])
        write_parameter(doc_fd,'documentID',doc_iter['Id'])
        write_parameter(doc_fd,'docRank',str(cur_iter))
        cur_iter += 1
        write_parameter(doc_fd,'documentName',doc_iter['Name'])
        write_parameter(doc_fd,'documentType',doc_iter['ThreeByteCode'])
        write_parameter(doc_fd,'printPreparationFormat',doc_iter['PreBatchFormat'])
        write_parameter(doc_fd,'docPaperTypePage1',doc_iter['PaperTypePage1'])
        write_parameter(doc_fd,'docPaperTypeOther',doc_iter['PaperTypeOther'])
        write_parameter(doc_fd,'policystate',pmf_dict['State'])
        write_parameter(doc_fd,'database',pmf_dict['Database'])

        num_inserts = len(inserts_lst)
        mon_logger.info("Number of Insert (Iterations):" + str(num_inserts))
        for insert_iter in range(1,6):
            if insert_iter < num_inserts:
                write_parameter(doc_fd,'insert' + str(insert_iter),inserts_lst[insert_iter]['Name'])
            else:
                write_parameter(doc_fd,'insert' + str(insert_iter),'-')
        
    #TODO: job properties table reader 
    addr_fd=open(os.path.join('../resources/out',pmf_dict['Id'] + '.addr'),'w')
    for addr_iter in delivery_addresses_lst:
        addr_fd.write('\t'.join([addr_iter['DeliveryMatchesMailingAddress'], addr_iter['Addressee'], addr_iter['PrimaryAddress'], str(addr_iter['SecondaryAddress']), addr_iter['City'], addr_iter['State'],addr_iter['Id'], addr_iter['SerialNumber'], addr_iter['RoutingCode']]))
   
#         documents_tag_dict = {'Id': 0, 'FilePath': 0 , 'ThreeByteCode': 0, 'PreBatchFormat': 0,'PaperTypePage1':0, 'PaperTypeOther':0, 'PageCount':0, 'Name':0, 'TypeIdentifier':0}
#         delivery_address_tag_dict ={'Id':0, 'Addressee':0, 'PrimaryAddress':0, 'SecondaryAddress':0,'City':0, 'State':0, 'Zip':0, 'DeliveryMatchesMailingAddress':0, 'SerialNumber':0, 'RoutingCode':0}
#         inserts_tag_dict = {'Name':0}
#         pmf_tag_dict={'Id': 0,'PolicyIdentifier': 0, 'State': 0, 'MasterId':0, 'JobType':0, 'Database':0, 'SpanishLanguage':0, 'InsertPageCountEquivalent':0, 'BarcodeID':0,'ServiceTypeID': 0, 'MailerID': 0}
#         

def write_parameter(mon_fd, param_name,param_val):
    mon_fd.write('-V app_param_' + param_name + '="' + param_val + '"\n')
    
if __name__ == "__main__":
    mylogger = set_logging()
    pmf_dict = parse_pmf(mylogger)
    mylogger.info("Contents of pmf_dict is:" + str(pmf_dict))
    write_param_files(mylogger, pmf_dict)
    read_job_properties('../resources/in/Job_Properties_tbl','030')