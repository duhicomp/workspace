'''
Created on May 7, 2015

@author: mabdul-aziz
'''
#from techrtime import *
import logging
import os
#import bko_api as bko
import pickle

def setup_logging(app_param_debug="N"):
    ############## LOGGING definition
    loglevel = logging.WARN
    if app_param_debug == 'Y':
        loglevel = logging.DEBUG
    logpath = "../logs"
    logfilename = 'app_debug.log'
    logfile = logpath + os.sep + logfilename
    logfilemode = 'w'
    logformat = '%(asctime)s [%(levelname)s]: %(message)s'
    logdateformat = '%m/%d/%Y %I:%M:%S %p'
    logging.basicConfig(filename=logfile, filemode=logfilemode, level=loglevel, format=logformat, datefmt=logdateformat)
   
def evaluate_rules_str(rules_str,operands_value_dict):
        # operands_value_dict will go away 
        split_rules_logic_lst=rules_str.split()
        logging.debug("split_rules_logic_lst contents: " + str(split_rules_logic_lst))
        anded_lst=[]
        anded_flag=0
        perform_and = 0
        for rule_elem in split_rules_logic_lst:
            if not anded_flag:
                if not perform_and: 
                    temp_OR=evaluate_rule(rule_elem,operands_value_dict)
                    logging.debug("temp_OR value: " + str(temp_OR))
                else:
                    temp_or_II=evaluate_rule(rule_elem,operands_value_dict)
                    temp_OR = temp_OR and temp_or_II 
                    logging.debug("temp_OR value (anded with next element): " + str(temp_OR))
                anded_flag = 1
            else:     
                operator=rule_elem
                if operator.upper() == "AND":
                    perform_and = 1
                elif operator.upper() == "OR":
                    anded_lst.append(temp_OR)
                    logging.debug("writing to the adned_lst:" + str(temp_OR))
                    perform_and = 0
                anded_flag = 0
        
        if perform_and:
            anded_lst.append(temp_OR)
        logging.debug("contents of the anded_lst is:" + str(anded_lst))
        temp_OR = 0
        for or_elemen in anded_lst: 
            temp_OR = temp_OR or or_elemen
            
        logging.debug("Final result of the logical operation (" + rules_str + ") is \n " + str(temp_OR))
        
def evaluate_rule(rule,rules_value_dict):
        """The Function to implement the rules"""
        logging.debug("Value for Rule: " + rule + " is: " + str(rules_value_dict[rule]) )
        # get the object for the Rule
        # apply the condition for the rule
        # custome python
        # regular expression 
        return rules_value_dict[rule]   
#################GLOBAL_SETUP#####################################

#techvars.Detection:Rule1 or Rule2
#techvars.Indexation:Rule3 or Rule4
#techvars.Enhancement:Rule5 and rule6
#techvars.RulesDef:Path to PrintReadyAppsRulesPropTable pickle
#techvars.DocumentObjectsGenDef:Path to DocumentPagesObjectsGeneralPropTable pickle
#techvars.DocumentObjectsDataContentDef:Path to BarcodesContentPropTable pickle


def detection_function():
    
    #rules_str = techvars.Detection
    
    #Once Development is done, get the path of the pickle files from the techvars
    #rules_pickel= techvars.RulesDef
    #doc_obj_def_pickel = techvars.DocumentObjectsGenDef
    #doc_obj_data_ContentDef_pickle = techvars.DocumentObjectsDataContentDef
    rules_pickel = "D:\\MA_Sefas\\Clients\\Packaging\\dict_pickles\\PrintReadyAppsRulesPropTable"
    doc_obj_def_pickel = "D:\\MA_Sefas\\Clients\\Packaging\\dict_pickles\\DocumentPagesObjectsGeneralPropTable"
    #Do I really need the doc_obj_data_ContentDef_pickle here, it is for Barcode Enhancements
    #doc_obj_data_ContentDef_pickle = "/home/adf/ma_test_pickles/BarcodesContentPropTable"
    detect_dict = {"RULES":{},"VPF_OBJECTS":{}}
    #probably put all the contents in one dictionary
    if os.path.exists(rules_pickel):
        detect_dict["RULES"]= pickle.load(open(rules_pickel,'rb'))
    else:
        raise Exception("unable to locate the Detection RULES pickle file: " + rules_pickel)
    if os.path.exists(doc_obj_def_pickel):
        detect_dict["VPF_OBJECTS"]= pickle.load(open(doc_obj_def_pickel,'rb'))
    else:
        raise Exception("unable to locate the Document Detection objects pickle file: " + doc_obj_def_pickel)
    #doc_obj_def_dict = pickle.load(doc_obj_def_pickel)
    #doc_obj_data_ContentDef_dict = pickle.load(doc_obj_data_ContentDef_pickle)
#     logging.debug("contents of the detect_dict are:" + str(detect_dict))
    print("contents of the detect_dict are:" + str(detect_dict))
    return

if __name__ == "__main__":
    setup_logging()
    detection_function()