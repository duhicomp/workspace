'''
Created on Feb 4, 2015

@author: mabdul-aziz
'''

input_file="../resources/LM04_master_index_def"
master_def="../resources/master_def.cmd"
line_cnt=0
with open(input_file,"r") as fin:
    with open(master_def,"w") as fout:
        for idx_line in fin:
            print("idx_line:" + idx_line)
            idx_field_name = str(idx_line.split()[0])
            if idx_field_name.strip() != "" :
                print("writing the line:" + "DEFINE(" + idx_field_name + "=" + str(line_cnt) + ")") 
                fout.write("DEFINE(" + idx_field_name + "=" + str(line_cnt) + ")\n")
                line_cnt += 1 
    
print("Exiting, something with the withs?")