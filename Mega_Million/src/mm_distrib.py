'''
Created on Nov 3, 2014

@author: mabdul
'''
import urllib.request
import datetime 

'''
Download Winning Numbers from www.calottery.com on 10/31/2014 12:31:13 PM for MEGA MILLIONS

Draw #     Draw Date             Number_1    Number_2    Number_3    Number_4    Number_5     Mega
------  -----------------        --------    --------    --------    --------    --------    ------

976     Tue. Oct 28, 2014          3          50          57          58          60          11

'''

def get_new_file(mm_filename):
    #txt_file = urlopen('http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=mega-millions')
    
    
    win_nu_fd=open(mm_filename, "w") #TODO:write the file in a tempdir, calc hash, if different than one already exist, update exisiting file
    
    url = "http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=mega-millions"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    buffer=response.read().decode('utf-8')

    print (buffer)
    print('writing buffer')
    win_nu_fd.write(buffer.replace("\r\n","\n"))
    
    win_nu_fd.close()
    del request


def format_input(mm_filename):
    infile= "../resources/Wining_Numbers_DB.txt"
    #TODO: create a temp dir to right the formatted txt directory
    outfile = mm_filename.replace(".txt", "_frmt.txt")
    infd=open(infile,"r")
    outfd=open(outfile,"w")
    
    try:
    
        for mega_line in infd:
            if mega_line.strip() != "" :
                line_lst=mega_line.split("     ")
                line_lst2=[]
                for ele in line_lst:
                    
                    if ele.strip():
                        line_lst2.append(ele)
                print(line_lst2)
                outfd.write("\t".join(line_lst2) + "\n")
                del line_lst2
    finally:
        infd.close()
        outfd.close()    

def calc_distribution():
    
#     infile= "../resources/Wining_Numbers_DB.tab"
    cur_date_s=str(datetime.date.today()).replace("-","")
    print("current date is:" + cur_date_s)
    mm_filename = '../resources/Wining_Numbers_DB' + cur_date_s + '.txt'
    get_new_file(mm_filename)
    format_input(mm_filename) 
    mega_dict={}
    mega_num_dict={}
#     infd=open(mm_filename,"r")
    mm_fd=open(mm_filename.replace('.txt','_frmt.txt'),"r")
    
    try:
        for mega_line in mm_fd:
            line_lst=mega_line.split("\t")
            
            if len(line_lst) > 0 and line_lst[0].isdigit():
                print(line_lst)
                for mm_index in range(2,7):
                    if line_lst[mm_index].strip() not in  mega_dict:
                        mega_dict.update({line_lst[mm_index]:1})
                    else: 
                        mega_dict.update({line_lst[mm_index]:mega_dict[line_lst[mm_index]]+1})
                #TODO: a loop for the mega number [8]
                if line_lst[7].strip('\n') not in  mega_num_dict:
                    mega_num_dict.update({line_lst[7].strip('\n'):1})
                else: 
                    mega_num_dict.update({line_lst[7].strip('\n'):mega_num_dict[line_lst[7].strip('\n')]+1})
    finally:
        dict_lst=[]
        mega_num_lst=[]
        lst_ind=0
        for dict_keys in mega_dict:
            # ends up with a tuple (Number, Frequency)
            dict_lst.insert(lst_ind,(dict_keys, mega_dict[dict_keys] ))
            lst_ind+=1
        lst_ind=0    
        for dict_keys in mega_num_dict:
            # ends up with a tuple (Number, Frequency)
            mega_num_lst.insert(lst_ind,(dict_keys, mega_num_dict[dict_keys] ))
            lst_ind+=1
            
        dict_lst.sort()
        print(mega_dict)
        print("and the Mega numbers are:")
        print(mega_num_dict)
        print(dict_lst)
        sorted_by_second = sorted(dict_lst, key=lambda tup: tup[1])
        print("Sorted By Frequency")
        mega_sorted_by_second = sorted(mega_num_lst, key=lambda tup: tup[1])
        print(sorted_by_second)
        print("and the mega numbers sorted by frequency")
        print(mega_sorted_by_second)
        mm_fd.close()
            
if __name__=="__main__":
    
    calc_distribution()