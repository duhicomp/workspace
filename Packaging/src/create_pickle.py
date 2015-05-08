'''
Created on May 5, 2015

@author: mabdul-aziz
'''

import csv
import pickle
import logging
import datetime
def setup_logging():
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    cur_date_s=str(datetime.date.today()).replace("-","")
    log_filename = "../logs/create_pickle" + cur_date_s 
    
    fh = logging.FileHandler(log_filename )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_formatter)
    
    my_logger.addHandler(ch)
    my_logger.addHandler(fh)
    
    return my_logger

def table_to_pickle(in_table, out_pickle_filename):
    prop_dict={}
    rows_dict=csv.DictReader(open(in_table),delimiter="\t")
    
    iteration=0
    for row in rows_dict:
        mon_logger.info("contents of current row =" + str(row))
        if iteration == 0 :
            iteration += 1
            continue
        mon_logger.info("row=" + str(row))
        row_dict={}
        prop_Key = ''
        for dict_key in list(row.keys()):
            
            mon_logger.info("Property value " + dict_key + "has the value" + str(row[dict_key]))
            if dict_key == 'Key':
                prop_Key = row["Key"]
                mon_logger.info("The Key for this row is:" + prop_Key)
            else:
                row_dict[dict_key] = row[dict_key] 
        if prop_Key:
            prop_dict[prop_Key]=row_dict
        del row_dict
        iteration += 1
    mon_logger.info("prop_dict=" + str(prop_dict))
    
    mon_pickle_fd=open('../resources/' + out_pickle_filename,'wb')
    pickle.dump(prop_dict,mon_pickle_fd)
    mon_pickle_fd.close()

    return

mon_logger = setup_logging()
if __name__=="__main__":
    
#     in_RulesDef = "../resources/PrintReadyAppsRulesPropTable.csv"
    in_DocumentObjectsGenDef = "../resources/DocumentPagesObjectsGeneralPropTable.csv"
#     in_DocumentPagesObjectsTypesPropTable="../resources/DocumentPagesObjectsTypesPropTable.csv"
    in_PrintReadyAppsRulesPropTable="../resources/MA_TEST_LM_PrintReadyAppsRulesPropTable.csv"
#     in_DocumentObjectsDataContentDef='../resources/BarcodesContentPropTable.csv'
     
#     out_pickle_filename = str(str(in_RulesDef.split('/')[-1]).split('.')[0])
#     mon_logger.info('out_pickle_filenmae=' + out_pickle_filename)
#     table_to_pickle(in_RulesDef,out_pickle_filename)
#     
    out_pickle_filename = str(str(in_DocumentObjectsGenDef.split('/')[-1]).split('.')[0])
    mon_logger.info('out_pickle_filenmae=' + out_pickle_filename)
    table_to_pickle(in_DocumentObjectsGenDef,out_pickle_filename)
    
#     out_pickle_filename = str(str(in_DocumentPagesObjectsTypesPropTable.split('/')[-1]).split('.')[0])
#     mon_logger.info('out_pickle_filenmae=' + out_pickle_filename)
#     table_to_pickle(in_DocumentPagesObjectsTypesPropTable,out_pickle_filename)
#     
    out_pickle_filename = str(str(in_PrintReadyAppsRulesPropTable.split('/')[-1]).split('.')[0])
    mon_logger.info('out_pickle_filenmae=' + out_pickle_filename)
    table_to_pickle(in_PrintReadyAppsRulesPropTable,out_pickle_filename)
    
#     out_pickle_filename = str(str(in_DocumentObjectsDataContentDef.split('/')[-1]).split('.')[0])
#     print('out_pickle_filenmae=' + out_pickle_filename)
#     table_to_pickle(in_DocumentObjectsGenDef,out_pickle_filename)