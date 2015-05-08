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
   
def evaluate_rules_str(rules_str,detect_rules_dict):
        # operands_value_dict will go away 
        print("in the evaluate_rules_str() ")
        split_rules_logic_lst=rules_str.split()
        logging.debug("split_rules_logic_lst contents: " + str(split_rules_logic_lst))
        anded_lst=[]
        anded_flag=0
        perform_and = 0
        for rule_elem in split_rules_logic_lst:
            if not anded_flag:
                if not perform_and: 
                    temp_OR=evaluate_rule(rule_elem,detect_rules_dict)
                    logging.debug("temp_OR value: " + str(temp_OR))
                else:
                    temp_or_II=evaluate_rule(rule_elem,detect_rules_dict)
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
    
    print("Rule is Rule: " + rule + " is: " + str(rules_value_dict['RULES'][rule]) )
    """The Function to implement the rules"""
    vpf_object_key = rules_value_dict['RULES'][rule]['ObjectKey']
    print("vpf_object_key :" + vpf_object_key )
    print("VPF object is is : " + vpf_object_key + " is: " + str(rules_value_dict['VPF_OBJECTS'][vpf_object_key]) )
    vpf_object_type = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['ObjectType']
    print("vpf_object_type :" + vpf_object_type )
    vpf_object_x = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['PositionX']
    print("vpf_object_x :" + vpf_object_x )
    vpf_object_y = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['PositionY']
    print("vpf_object_y :" + vpf_object_y )
    vpf_object_w = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Width']
    print("vpf_object_w :" + vpf_object_w )
    vpf_object_h = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Height']
    print("vpf_object_h :" + vpf_object_h )
    vpf_object_side = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Side']
    print("vpf_object_side:" + vpf_object_side )
    vpf_object_orientation = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Orientation']
    print("vpf_object_orientation :" + vpf_object_orientation )
    
    vpf_object_contents = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['DataContent']
    #substring
    vpf_object_substring  = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Substring']
    vpf_object_string_start = vpf_object_substring.split(":,:") 
    if vpf_object_type.upper() == "TEXT":
        #if object type is TEXT, get text associated properties: font name, font size
        vpf_object_fname = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['FontName']
        vpf_object_fsize = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['ObjectType']
    
    #vpf_objects_zone = bko.getCurrentPage().newZone(vpf_object_x, vpf_object_y, vpf_object_w, vpf_object_h)
    # get the object for the Rule
    
    # apply the condition for the rule
    
    # custome python
    
    # regular expression 
    
    # return rules_value_dict[rule]   
#################GLOBAL_SETUP#####################################

# techvars.Detection:Rule1 or Rule2
# techvars.Indexation:Rule3 or Rule4
# techvars.Enhancement:Rule5 and rule6
# techvars.RulesDef:Path to PrintReadyAppsRulesPropTable pickle
# techvars.DocumentObjectsGenDef:Path to DocumentPagesObjectsGeneralPropTable pickle
# techvars.DocumentObjectsDataContentDef:Path to BarcodesContentPropTable pickle


def detection_function():
    
    #rules_str = techvars.Detection
    rules_str = "Rule_1"
    
    #Once Development is done, get the path of the pickle files from the techvars
    #rules_pickel= techvars.RulesDef
    #doc_obj_def_pickel = techvars.DocumentObjectsGenDef
    #doc_obj_data_ContentDef_pickle = techvars.DocumentObjectsDataContentDef
    
    rules_pickel = "../resources/PrintReadyAppsRulesPropTable"
    doc_obj_def_pickel = "../resources/DocumentPagesObjectsGeneralPropTable"
    #Do I really need the doc_obj_data_ContentDef_pickle here, it is for Barcode Enhancements
    #doc_obj_data_ContentDef_pickle = "/home/adf/ma_test_pickles/BarcodesContentPropTable"
    
    detect_dict = {"RULES":{},"VPF_OBJECTS":{}}

    if os.path.exists(rules_pickel):
        detect_dict["RULES"]= pickle.load(open(rules_pickel,'rb'))
    else:
        raise Exception("unable to locate the Detection RULES pickle file: " + rules_pickel)
    if os.path.exists(doc_obj_def_pickel):
        detect_dict["VPF_OBJECTS"]= pickle.load(open(doc_obj_def_pickel,'rb'))
    else:
        raise Exception("unable to locate the Document Detection objects pickle file: " + doc_obj_def_pickel)
#     doc_obj_def_dict = pickle.load(doc_obj_def_pickel)
#     doc_obj_data_ContentDef_dict = pickle.load(doc_obj_data_ContentDef_pickle)
#     logging.debug("contents of the detect_dict are:" + str(detect_dict))
    print("contents of the detect_dict['RULES'] are:" + str(detect_dict["RULES"]))
    print("contents of the detect_dict['VPF_OBJECTS'] are:" + str(detect_dict["VPF_OBJECTS"]))
    evaluate_rules_str(rules_str,detect_dict)
    return

if __name__ == "__main__":
    setup_logging()
    detection_function()