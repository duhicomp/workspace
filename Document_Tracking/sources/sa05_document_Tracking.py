'''
Created on Jun 30, 2015

@author: mabdul-aziz
'''

import csv
import os
from producer_lib.jdbcclient import JdbcClient
from producer_lib.DocumentTrackingStream import DocumentTrackingStream
from producer_lib import DbIndexingClient

class saDocumentTracking:
    def __init__(self,in_dt_description_file, in_input_index_fname, out_dt_idx_file):
        self.in_dt_description_file = in_dt_description_file
        self.in_input_index_fname = in_input_index_fname 
        self.out_dt_idx_file = out_dt_idx_file
        self.myencoding = "ISO-8859-1"
        self.host = os.environ.get('SMD_HOST', 'localhost')
        self.port = int(os.environ.get('SMD_PORT', '29110'))
        self.jdbcDriver = os.environ.get('JDBC_DRIVER', 'com.microsoft.sqlserver.jdbc.SQLServerDriver')
        self.jdbcString = os.environ.get('JDBC_STRING','jdbc:sqlserver://10.6.100.2\SAPRODUCER:1433')
        self.dbUser = os.environ.get('PRODUCER_DB_USER_','adf')
        self.dbPassword = os.environ.get('PRODUCER_DB_PASSWRD_','sefas123')
        self.db_tbl_name = os.environ.get('DT_TBL_NAME',"DOCUMENT_TRACKING_SA")
        self.myclient = None
        self.myDb = None
        
    def connectDB(self):
        self.myclient = JdbcClient(self.myencoding,self.host,self.port)
        self.myclient.connect()
        self.myclient.sqlInit(self.jdbcDriver)
        self.myDb = self.myclient.sqlOpen(self.jdbcString, self.dbUser, self.dbPassword)

    def disconnectDB(self):
        # Close connection

        self.myclient.sqlClose(self.myDb)
        self.myDb = None
        self.myclient.disconnect()
       
    def create_dt_index(self):
        pyvar_dt_desc_fd = open(self.in_dt_description_file)
        pyvar_index_dict=csv.DictReader(open(self.in_input_index_fname),delimiter="\t")
        pyvar_dt_index_fd = open(self.out_dt_idx_file, 'w')
        pyvar_dt_index_lst =[]
        curnt_dsc_line = 0
        
        for line_num, dt_desc_line in enumerate(pyvar_dt_desc_fd):
            print('line_num=' + str(line_num))
            if curnt_dsc_line == 0:
                pass
            else:
                pyvar_dt_index_lst.append(str(dt_desc_line.split('\t')[1]).strip())
            curnt_dsc_line += 1
        print pyvar_dt_index_lst
        
        for pyvar_index_line in pyvar_index_dict:
            print pyvar_index_line
            pyvar_dt_doc_track_idx_line = []
            for idx_elem in pyvar_dt_index_lst:
                pyvar_dt_doc_track_idx_line.append(pyvar_index_line[idx_elem])
            print '\t'.join(pyvar_dt_doc_track_idx_line)
            pyvar_dt_index_fd.write('\t'.join(pyvar_dt_doc_track_idx_line) + '\n')
        pyvar_dt_index_fd.close()
        return
    
    def create_dt_in_file_desc_lst(self):
        pyo_dt_desc_lst = []
        return pyo_dt_desc_lst
    def insert_dt_index(self):
        try : 
            #Configurable environment parameters

            myencoding = "ISO-8859-1"
            host = os.environ.get('SMD_HOST', 'localhost')
            port = int(os.environ.get('SMD_PORT', '29110'))
            jdbcDriver = os.environ.get('JDBC_DRIVER', 'oracle.jdbc.driver.OracleDriver')
            jdbcString = os.environ.get('JDBC_STRING','jdbc:oracle:thin:@pcdemo:1521:ORCL')
            dbUser = os.environ.get('PRODUCER_DB_USER_','adf')
            dbPassword = os.environ.get('PRODUCER_DB_PASSWRD_','sefas123')
            myclient = JdbcClient(myencoding,host,port)
            
            # Define DB connection to use
            myclient = DbIndexingClient.DbIndexingClient(myencoding, host, port)
            myclient.connect()
            myclient.sqlInit(jdbcDriver)
            myDb = myclient.sqlOpen(jdbcString, dbUser, dbPassword)
            
            # Define data structures
            inputType = DbIndexingClient.FILE_TYPE_VPF_IDX
            #inputFileDescription =  [
            #                         [DbIndexingClient.INPUT_CSV_DELIMITER, "\t"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 0, "jobid"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 1, "filenumber"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 2, "docid"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 3, "packetid"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 4, "database"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 5, "policystate"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 6, "policyid"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 7, "addressee"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 8, "addressid"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 9, "primaryaddress"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 10, "secondaryaddress"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 11, "city"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 12, "addressstate"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 13, "zip"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 14, "receptiondate"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 15, "dispositioncode"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 16, "processeddate"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 17, "operatorid"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 18, "pullrequest"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 19, "pullrequestconfirm"],
            #                         [DbIndexingClient.INPUT_DEF_COLUMN, 20, "safeflag"]
            #                        ]

            inputFileDescription  = self.create_dt_in_idx_description()
            print inputFileDescription  
            db_table = "DOCUMENT_TRACKING_SA"
            #databaseTableDescription =  [
            #                             [DbIndexingClient.DBTABLE_DEF, db_table],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "JOB_ID", "jobid",      DbIndexingClient.COLCONST],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "FILE_NUMBER", "filenumber", DbIndexingClient.COLCONST],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "DOCUMENT_ID", "docid",       DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "PACKET_ID", "packetid",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "SRC_DATABASE", "database",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "POLICY_STATE", "policystate",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "POLICY_ID", "policyid",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "ADDRESSEE", "addressee",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "ADDRESS_ID", "addressid",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "PRIMARY_ADDRESS", "primaryaddress",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "SECONDARY_ADDRESS", "secondaryaddress",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "CITY", "city",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "PKG_STATE", "addressstate",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "ZIP", "zip",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "RECEPTION_DATE", "receptiondate",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "DISPOSITION_CODE", "dispositioncode",     DbIndexingClient.COLINPUT],
            #                              [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "PROCESSED_DATE", "processeddate",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "OPERATOR_ID", "operatorid",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "PULL_REQUEST", "pullrequest",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "PULL_REQUEST_CONFIRM", "pullrequestconfirm",     DbIndexingClient.COLINPUT],
            #                             [DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "SAFE_FLAG", "safeflag",     DbIndexingClient.COLINPUT]
            #                            ]
            databaseTableDescription  = self.create_db_tbl_dscription()
            print databaseTableDescription  
            # Process Document Tracking

            #myclient.indexCsv(myDb, index_filename, inputType, inputFileDescription, databaseTableDescription)
            #myclient.indexCsv(myDb, self.out_dt_idx_file, inputType, inputFileDescription, databaseTableDescription)

            # Close connection
            #myclient.sqlClose(myDb)
            #myDb = None
            #myclient.disconnect()
         

        except Exception ,e:
            raise self.log("Insert Document Tracking Info Failed : " + str(e))
            
        #return
        
    def update_dt_index(self):
        return
    
    def create_dt_in_idx_description(self):
        dt_in_idx_desc_lst=[]
        #[DbIndexingClient.INPUT_CSV_DELIMITER, "\t"],
        #[DbIndexingClient.INPUT_DEF_COLUMN, 0, "jobid"],
        dt_in_idx_desc_lst.append([DbIndexingClient.INPUT_CSV_DELIMITER, "\t"])
        dt_desc_fd = open(self.dt_desc_file, 'r')
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

    def create_db_tbl_dscription(self):
        dt_db_tbl_desc_lst=[]
        db_tbl_name = "DOCUMENT_TRACKING_SA"
        #[DbIndexingClient.DBTABLE_DEF, db_table],
        #[DbIndexingClient.DBTABLE_DEF_COL, DbIndexingClient.COLTYPE_STR, "JOB_ID", "jobid",      DbIndexingClient.COLCONST],
        dt_db_tbl_desc_lst.append([DbIndexingClient.DBTABLE_DEF, db_tbl_name])
        dt_desc_fd = open(self.dt_desc_file, 'r')
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

if __name__ == "__main__":
    input_index_fname = '../resources/merged_output_s.ind' 
    dt_description_file = '../resources/DT_Description.txt'
    dt_idx_file = '../resources/dt_merged_output.ind'
    pyo_dt_batching = saDocumentTracking(dt_description_file, input_index_fname, dt_idx_file)
    pyo_dt_batching.create_dt_index()
    pyo_dt_batching.insert_dt_index()
    #screate_dt_index(dt_description_file, input_index_fname, dt_idx_file)