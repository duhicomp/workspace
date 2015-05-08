'''
Created on May 6, 2015

@author: mabdul-aziz
'''

def evaluate_rules_str(rules_str,operands_value_dict):
    # operands_value_dict will go away 
    split_rules_logic_lst=rules_str.split()
    print("split_rules_logic_lst contents: " + str(split_rules_logic_lst))
    anded_lst=[]
    anded_flag=0
    perform_and = 0
    for rule_elem in split_rules_logic_lst:
        if not anded_flag:
            if not perform_and: 
                temp_OR=evaluate_rule(rule_elem,operands_value_dict)
                print("temp_OR value: " + str(temp_OR))
#                 anded_lst.append(temp_OR)
            else:
                temp_or_II=evaluate_rule(rule_elem,operands_value_dict)
                temp_OR = temp_OR and temp_or_II 
                print("temp_OR value (anded with next element): " + str(temp_OR))
            anded_flag = 1
        else:     
            operator=rule_elem
            if operator.upper() == "AND":
                perform_and = 1
            elif operator.upper() == "OR":
                anded_lst.append(temp_OR)
                print("writing to the adned_lst:" + str(temp_OR))
                perform_and = 0
            else:   
                anded_lst.append(temp_OR)
            anded_flag = 0
    if len(split_rules_logic_lst) == 1:
        anded_lst.append(temp_OR)
    if perform_and:
        anded_lst.append(temp_OR)
    print ("contents of the anded_lst is:" + str(anded_lst))
    temp_OR = 0
    for or_elemen in anded_lst: 
        temp_OR = temp_OR or or_elemen
        
    print("Final result of the logical operation (" + rules_str + ") is \n " + str(temp_OR))
def evaluate_rule(rule,rules_value_dict):
    """The Function to implement the rules"""
    print("Value for Rule: " + rule + " is: " + str(rules_value_dict[rule]) )
    return rules_value_dict[rule]
if __name__ == "__main__":
    #Rules_lst="Rule1 or Rule2 AND Rule3 or Rule4 and Rule5"
    Rules_lst="Rule1"
#                 ''' 0 OR 0 AND 1 OR 1 and 0 '''
                     
    rules_value_dict={'Rule1':1, 'Rule2':1, 'Rule3':0, 'Rule4':1, 'Rule5':0}
    evaluate_rules_str(Rules_lst,rules_value_dict)
    