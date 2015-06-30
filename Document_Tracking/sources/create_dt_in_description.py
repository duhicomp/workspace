'''
Created on Jun 30, 2015

@author: mabdul-aziz
'''
from producer_lib.DocumentTrackingStream import DocumentTrackingStream
from producer_lib import DbIndexingClient


def create_dt_in_idx_description(dt_desc_file):
    dt_in_idx_desc_lst=[]
    #[DbIndexingClient.INPUT_CSV_DELIMITER, "\t"],
    #[DbIndexingClient.INPUT_DEF_COLUMN, 0, "jobid"],
    dt_in_idx_desc_lst.append([DbIndexingClient.INPUT_CSV_DELIMITER, "\t"])
    dt_desc_fd = open(dt_desc_file, 'r')
    try:
        for seq,dt_desc_ln in enumerate(dt_desc_fd):
            if seq == 0:
                pass
            else:
                pyvar_clmn_name = str(dt_desc_ln.split('\t')[1]) 
                dt_in_idx_desc_lst.append([DbIndexingClient.INPUT_DEF_COLUMN, seq-1, pyvar_clmn_name])
                 
        print dt_in_idx_desc_lst
    except:
        raise Exception('Something Wrong happened')
    finally:
        dt_desc_fd.close()
    return

def create_db_tbl_dscription(dt_desc_file):
    dt_db_tbl_desc_lst=[]
    db_tbl_name = "DOCUMENT_TRACKING_SA"
    #[DbIndexingClient.DBTABLE_DEF, db_table],
    #[DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "JOB_ID", "jobid",      DbIndexingClient.COLCONST],
    dt_db_tbl_desc_lst.append([DbIndexingClient.DBTABLE_DEF, db_tbl_name])
    dt_desc_fd = open(dt_desc_file, 'r')
    try:
        for seq,dt_desc_ln in enumerate(dt_desc_fd):
             
            if seq != 0 and dt_desc_ln.strip() != '' :
                print('seq=' + str(seq) +"\t contents:" + dt_desc_ln )
                pyvar_db_clmn_name = str(dt_desc_ln.split('\t')[0])
                pyvar_idx_clmn_name = str(dt_desc_ln.split('\t')[1])
                pyvar_clmn_type = str(dt_desc_ln.split('\t')[2])
                if pyvar_clmn_type.strip() == 'STR' or pyvar_clmn_type == 'str' :
                    dt_db_tbl_desc_lst.append([DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, pyvar_db_clmn_name, pyvar_idx_clmn_name , DbIndexingClient.COLINPUT],)
                elif pyvar_clmn_type.strip() == 'INT' or pyvar_clmn_type == 'int' :
                    dt_db_tbl_desc_lst.append([DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_INT, pyvar_db_clmn_name, pyvar_idx_clmn_name , DbIndexingClient.COLINPUT],)
                 
        print dt_db_tbl_desc_lst
    except:
        raise Exception("Something wrong happned")
    finally:
        dt_desc_fd.close()
    return


if __name__ == '__main__':
    dt_desc_file = '../resources/DT_Description.txt'
    create_dt_in_idx_description(dt_desc_file)
    create_db_tbl_dscription(dt_desc_file)
    print("seems to finish successfully")