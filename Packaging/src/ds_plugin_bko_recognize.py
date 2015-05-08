'''
Created on May 8, 2015

@author: mabdul-aziz
'''
'''
Script name: dwf_scripts_projectcode_listoldfiles.py
Author: Mohammed Abdul-Aziz 
Rev:0.1
Date:04/08/2015
'''

from techrtime import *
import logging
import os
import bko_api as bko
import pickle
import ds_plugin_bko_vpfutil as vpf_util


def setup_logging():
  ############## LOGGING definition
  loglevel = logging.WARN
  #if techvars.app_param_debug == 'Y':
  loglevel = logging.DEBUG
  logpath = os.path.split(techvars.RMK_VPF_OUT)[0]
  logfilename = 'app_debug.log'
  logfile = logpath + os.sep + logfilename
  logfilemode = 'w'
  logformat = '%(asctime)s [%(levelname)s]: %(message)s'
  logdateformat = '%m/%d/%Y %I:%M:%S %p'
  logging.basicConfig(filename=logfile, filemode=logfilemode, level=loglevel, format=logformat, datefmt=logdateformat)
 
def evaluate_rules_str(rules_str,detect_rules_dict):
  # operands_value_dict will go away 
  logging.debug("in the evaluate_rules_str() ")
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
  if len(split_rules_logic_lst) == 1:
      anded_lst.append(temp_OR)
  if perform_and:
      anded_lst.append(temp_OR)
  logging.debug("contents of the anded_lst is:" + str(anded_lst))
  temp_OR = 0
  for or_elemen in anded_lst: 
      temp_OR = temp_OR or or_elemen
  return temp_OR    
  logging.debug("Final result of the logical operation (" + rules_str + ") is \n " + str(temp_OR))
          
def evaluate_rule(rule,rules_value_dict):
  #setup code probably move it somewhere else)
  ret_val=0
  logging.debug("Rule is Rule: " + rule + " is: " + str(rules_value_dict['RULES'][rule]) )
  """The Function to implement the rules"""
  vpf_object_key = rules_value_dict['RULES'][rule]['Object']
  logging.debug("vpf_object_key :" + vpf_object_key )
  rules_ActionTrigger=rules_value_dict['RULES'][rule]['ActionTrigger']
  logging.debug("rules_ActionTrigger :" + rules_ActionTrigger )
  rules_Action_Default=rules_value_dict['RULES'][rule]['Default']
  logging.debug("rules_Action_Default :" + rules_Action_Default)
  rules_DetectionType=rules_value_dict['RULES'][rule]['DetectionType']
  logging.debug("rules_DetectionType:" + rules_DetectionType)
  rules_CustomCondition=rules_value_dict['RULES'][rule]['CustomCondition']
  logging.debug("rules_CustomCondition:" + rules_CustomCondition)
  rules_Values=rules_value_dict['RULES'][rule]['Values']
  logging.debug("rules_Values:" + rules_Values)
  rules_Filter=rules_value_dict['RULES'][rule]['Filter']
  logging.debug("rules_Filter:" + rules_Filter)
  logging.debug("VPF object is : " + vpf_object_key + " is: " + str(rules_value_dict['VPF_OBJECTS'][vpf_object_key]) )
  vpf_object_type = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['ObjectType']
  logging.debug("vpf_object_type :" + vpf_object_type )
  vpf_object_x = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['PositionX']
  logging.debug("vpf_object_x :" + vpf_object_x )
  vpf_object_y = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['PositionY']
  logging.debug("vpf_object_y :" + vpf_object_y )
  vpf_object_w = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Width']
  logging.debug("vpf_object_w :" + vpf_object_w )
  vpf_object_h = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Height']
  logging.debug("vpf_object_h :" + vpf_object_h )
  vpf_object_side = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Side']
  logging.debug("vpf_object_side:" + vpf_object_side )
  vpf_object_orientation = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Orientation']
  logging.debug("vpf_object_orientation :" + vpf_object_orientation )
  
  vpf_object_contents = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['DataContent']
  #substring
  #vpf_object_substring  = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['Substring']
  #vpf_object_string_start = vpf_object_substring.split(":,|") 
  if vpf_object_type.upper() == "TEXT":
      #if object type is TEXT, get text associated properties: font name, font size
      vpf_object_fname = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['FontName']
      vpf_object_fsize = rules_value_dict['VPF_OBJECTS'][vpf_object_key]['ObjectType']
  
      vpf_objects_zone = bko.getCurrentPage().newZone(float(vpf_object_x), float(vpf_object_y), float(vpf_object_w), float(vpf_object_h))
      if vpf_object_fname:
          logging.debug("Grabbing vpf objects from the zone using font:" + vpf_object_fname)
          
      objects_lst = vpf_util.getVPFObjects(vpf_objects_zone,[bko.VPFText])
      for elem in objects_lst:
          #if type(elem) == bko.VPFText:
              logging.debug("Returned object :" + str(elem.getText().strip() ))
      if rules_ActionTrigger.upper() == "EQUALSTO":
        for val in rules_Values.split(":,|"):
            for elem in objects_lst:
                if type(elem) == bko.VPFText:
                    if elem.getText() == val:
                        logging.debug("Equal value to the reference value:"  + str(val) + "was found in the zone: " + logging.debug("Returned object :" + str(elem.getText().strip())) )
                        ret_val=1
                        break
      if rules_ActionTrigger.upper() == "CONTAINS":
          for val in rules_Values.split(":,|"):
            for elem in objects_lst:
                if type(elem) == bko.VPFText:
                    if val in elem.getText().strip() :
                        logging.debug("Zone contents: "+ elem.getText().strip()  + "Contains the reference value:"+ str(val) )
                        ret_val=1
                        break
  #if vpf_object_type.upper() == "IMAGE:
  #filter objects based on bko.VPFImage
  return ret_val
#################GLOBAL_SETUP#####################################

setup_logging()
bko.setUnit(bko.Unit('pica', 100))
#techvars.Detection:Rule1 or Rule2
#techvars.Indexation:Rule3 or Rule4
#techvars.Enhancement:Rule5 and rule6
#techvars.RulesDef:Path to PrintReadyAppsRulesPropTable pickle
#techvars.DocumentObjectsGenDef:Path to DocumentPagesObjectsGeneralPropTable pickle
#techvars.DocumentObjectsDataContentDef:Path to BarcodesContentPropTable pickle


def detection_function():
  logging.debug("entering the detection function: detection_function()")
  #rules_str = techvars.Detection
  rules_str= ca_getcustomvalue("rules_str", "1")
  rules_pickel =ca_getcustomvalue("rules_pickle_path", "1") 
  doc_obj_def_pickel = ca_getcustomvalue("objects_picke_path", "1")
  #Once Development is done, get the path of the pickle files from the techvars
  logging.debug("rules_str=:" + rules_str)
  logging.debug("rules_pickel=:" + rules_pickel)
  logging.debug("doc_obj_def_pickel =:" + doc_obj_def_pickel )
  detect_dict = {"RULES":{},"VPF_OBJECTS":{}}

  if os.path.exists(rules_pickel):
      rules_pickel_fd=open(rules_pickel,'rb')
      detect_dict["RULES"]= pickle.load(rules_pickel_fd)
      rules_pickel_fd.close
  else:
      logging.info("Unable to locate the rules pickle file in:" + rules_pickel)
      raise Exception("Unable to locate the rules pickle file in:" + rules_pickel)
  if os.path.exists(doc_obj_def_pickel):
      doc_obj_def_pickel_fd=open(doc_obj_def_pickel,'rb')
      detect_dict["VPF_OBJECTS"]= pickle.load(doc_obj_def_pickel_fd)
  else:
      logging.info("Unable to locate the Objects Properties pickle file in:" + doc_obj_def_pickel)
      raise Exception("Unable to locate the Objects Properties pickle file in:" + doc_obj_def_pickel)
  
  logging.debug("contents of the detect_dict are:" + str(detect_dict))
  ret_val = evaluate_rules_str(rules_str,detect_dict)
  logging.debug("returning value:" + str(ret_val))
  techvars.CusVar_Result = str(ret_val)
