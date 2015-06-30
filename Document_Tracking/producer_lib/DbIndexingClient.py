#
# Python client class to Jdbc SqlExecFactory SMD service
# This class call an SMD service to put the content of an index file to a database table
# To do that a definition of the input file is done with his association with the database table
# 2 services are defined :
# Insert to insert new elements in the database
# Update to update some fields of already inserted element
#       
__revision__ = '$Revision$'
__date__ ='$Date$'

import sys
import os
import os.path
from Connector import Connector,SmdClientError
from jdbcclient import JdbcClient

# Constant definition must be the the same than the one defined in : com.sefas.gridclient.sqlservices.SqlIndexingFactory
# those constant became Tag Name when they are sent as parameter to the SqlIndexingFactory

# main tag for the defintion of the input files
XML_TAG_MAIN_INPUT = "Input"

# File type list definition
FILE_TYPE_CSV = "FILE_TYPE_CSV"                   # list of column 2 mode for the file : Fix column size or dynamic column size with delimiter
FILE_TYPE_VPF_IDX = "FILE_TYPE_VPF_IDX"           # techsort index file simple (without application information)
FILE_TYPE_TSM_VPF_IDX = "FILE_TYPE_TSM_VPF_IDX"   # techsort index file complete (with application information)

# Key identifiers for definition of the input file structure
INPUT_DEF_COLUMN  = 'Column'                      # definition of a column of the input CVS file
INPUT_DEF_COLID   = 'COLID'                       # definition of the id of the column
INPUT_DEF_COLNAME = 'COLNAME'                     # assign a name to the column id
INPUT_DEF_COLSIZE = 'COLSIZE'                     # if there is no delimiter, the size of the column must de defined for each column

INPUT_CSV_DELIMITER = 'Delimiter'              # definition of the delimiter for FILE_TYPE_CSV
INPUT_DELIMITER_CHAR= 'DELIMITER_CHAR'            # value of the delimiter char

# Structure of the definition of the input file (Python format is table of table)
XML_INPUT_DETAIL = {INPUT_DEF_COLUMN:[INPUT_DEF_COLID,INPUT_DEF_COLNAME]
                    ,INPUT_CSV_DELIMITER:[INPUT_DELIMITER_CHAR]}
# Structure of the definition of the input file (Python->Java format is XML)
"""
<XML_TAG_MAIN_INPUT>
    <INPUT_CVS_DELIMITER><INPUT_DELIMITER_CHAR>X</INPUT_DELIMITER_CHAR></INPUT_CVS_DELIMITER>
    <INPUT_DEF_COLUMN><INPUT_DEF_COLID>xxx</INPUT_DEF_COLID><INPUT_DEF_COLNAME>yyy</INPUT_DEF_COLNAME></INPUT_DEF_COLUMN>
</XML_TAG_MAIN_INPUT>
Example :
<Input>
    <Column><COLID>1</COLID><COLNAME>DocumentID</COLNAME></Column>
</Input>
"""

# main tag for the defintion of the database definition
XML_TAG_MAIN_DB = "Database"

# Key definition for the definition of the database table structure
DBTABLE_DEF = 'TableDefinition'
DBTABLE_DEF_NAME_VALUE = 'TABLENAME'

# Definition of the association between the database column and the input file column or a constant 
DBTABLE_DEF_COL = 'ColumnAssociation'

# Definition of the association between the input file column and the database column for an update
DBTABLE_UPDATE_KEY = 'UpdateKeyColumn'

# Type of the association with the database column
VALUETYPE = 'VALUETYPE'     # Identifier of the parameter
COLINPUT = 'InputName'      # association with the input file (Name of the column in the input file)
COLCONST = 'Constant'       # association with a constant 
COLNAME = 'COLNAME' # database column name
COLVALUE = 'COLVALUE'       # input file column name or constant value

# Type of the value
COLTYPE = 'COLTYPE'      # identifier of the Column who define the type
COLTYPE_STR = "VARCHAR"  # Type is String (default value)
COLTYPE_INT = "INTEGER"  # Type in an integer


# Structure of the definition of the database for request (Python format is table of table)
XML_DB_DETAIL = {DBTABLE_DEF:[DBTABLE_DEF_NAME_VALUE]
                ,DBTABLE_DEF_COL:[COLTYPE, COLNAME, COLVALUE, VALUETYPE]
                ,DBTABLE_UPDATE_KEY:[COLTYPE, COLNAME,COLVALUE,VALUETYPE]
                }
# Structure of the definition of the input file (Python->Java format is XML)
"""
<XML_TAG_MAIN_DB>
    <DBTABLE_DEF_NAME><DBTABLE_DEF_NAME_VALUE>X</DBTABLE_DEF_NAME_VALUE></DBTABLE_DEF_NAME>
    <DBTABLE_UPDATE_KEY>
        <COLTYPE>xxx</COLTYPE>
        <COLNAME>yyy</COLNAME>
        <COLVALUE>xxx</COLVALUE>
        <VALUETYPE>xxx</VALUETYPE>
    </DBTABLE_UPDATE_KEY>
    <DBTABLE_DEF_COL>
        <COLTYPE>xxx</COLTYPE>
        <COLNAME>yyy</COLNAME>
        <COLVALUE>xxx</COLVALUE>
        <VALUETYPE>xxx</VALUETYPE>
    </DBTABLE_DEF_COL>
</XML_TAG_MAIN_DB>
Example :
<Input>
    <Column><COLID>1</COLID><COLNAME>DocumentID</COLNAME></Column>
</Input>
"""
# SQL Request called on the Server 
# for insert with a simple parameter
"""
<Database>
    <TableName><TABLENAME>X</TABLENAME></TableName>
    <ColumnAssociation>
        <COLTYPE>VARCHAR</COLTYPE>
        <COLNAME>business_id</COLNAME>
        <COLVALUE>1</COLVALUE>
        <VALUETYPE>Constant</VALUETYPE>
    </ColumnAssociation>
    <ColumnAssociation>
        <COLTYPE>VARCHAR</COLTYPE>
        <COLNAME>document_id</COLNAME>
        <COLVALUE>DOC_ID</COLVALUE>
        <VALUETYPE>InputName</VALUETYPE>
    </ColumnAssociation>
</Database>

insert into DOCUMENT_TRACKING (business_id, document_id) values ('1',?)
? -> will take successivelly all the values of the input column name DOC_ID

If there is DBTABLE_UPDATE_KEY definition, they are managed as DBTABLE_DEF_COL no diferencies in that case

"""

# for update with a simple parameter
"""
<Database>
    <TableName><TABLENAME>X</TABLENAME></TableName>
    <UpdateKeyColumn>
        <COLTYPE>VARCHAR</COLTYPE>
        <COLNAME>business_id</COLNAME>
        <COLVALUE>1</COLVALUE>
        <VALUETYPE>Constant</VALUETYPE>
    </UpdateKeyColumn>
    <UpdateKeyColumn>
        <COLTYPE>VARCHAR</COLTYPE>
        <COLNAME>document_id</COLNAME>
        <COLVALUE>DOC_ID</COLVALUE>
        <VALUETYPE>InputName</VALUETYPE>
    </UpdateKeyColumn>
    <ColumnAssociation>
        <COLTYPE>INTEGER</COLTYPE>
        <COLNAME>document_status</COLNAME>
        <COLVALUE>DOC_STATUS</COLVALUE>
        <VALUETYPE>InputName</VALUETYPE>
    </ColumnAssociation>
</Database>

update DOCUMENT_TRACKING set document_status=? where business_id='1' and business_id=?
first  : ? -> will take successivelly all the values of the input column name DOC_STATUS
second : ? -> will take successivelly all the values of the input column name DOC_ID

If there is DBTABLE_UPDATE_KEY definition, they are managed as DBTABLE_DEF_COL no diferencies in that case

"""
class DbIndexingClient(JdbcClient):
    """Python Client interface to the SqlFactory SMD service """

    FETCH_ALL = -1 # get all results in one call (USE CAUTIOUSLY)
    CLASSFACTORY = 'com.sefas.gridclient.sqlservices.SqlIndexingFactory'
    _INDEX_FILE_ = 'indexFile'
    _UPDATE_INDEX_FILE_ = 'updateIndexFile'
        
    

    
    def __init__ ( self , 
                   encoding="UTF8" , # default encoding to UTF8
                   hostName="localhost" ,
                   port=29100,
                   variableDict = None 
                 ):
        """ constructor just store provided object information """
        self._host = hostName 
        self._port = port
        self._connection = None
        self._encoding = encoding 
        self._variableDict = variableDict 

    def arrayToXml(self, arrayType, array):
        if arrayType == 'INPUT':
            mainTag=XML_TAG_MAIN_INPUT
            colLst=XML_INPUT_DETAIL
        elif arrayType == 'DB':
            mainTag=XML_TAG_MAIN_DB
            colLst=XML_DB_DETAIL
        resu = []
        resu.append('<%s>' % (mainTag))
        for a in array:
            curColLst = colLst[a[0]]
            resu.append('<%s>' % (a[0]))
            i = 1
            for tagName in curColLst:
                resu.append('<%s>%s</%s>' % (tagName,a[i],tagName))            
                i = i + 1
            resu.append('</%s>' % (a[0]))            
        resu.append('</%s>' % (mainTag))
        return ''.join(resu)
    def __index( self , callMethod, dbHandle , inputFile, inputType, inputFileDescription, databaseTableDescription):
        if self._connection == None:
            return None
        """ execute provided sql statement on given dbHandle """ 
        self._connection.marshall( Connector.SET_METHOD , callMethod ) #IGNORE:E1101
        # populate parameters
        self._connection.marshall( Connector.DEF_INTEGER , "dbHandle"  ) #IGNORE:E1101
        self._connection.marshall( Connector.SET_VALUE , "dbHandle" , str(dbHandle) ) #IGNORE:E1101
        self._connection.marshall( Connector.DEF_STRING , "inputFile"  ) #IGNORE:E1101
        self._connection.marshall( Connector.SET_VALUE , "inputFile" , inputFile ) #IGNORE:E1101
        self._connection.marshall( Connector.DEF_STRING , "inputType"  ) #IGNORE:E1101
        self._connection.marshall( Connector.SET_VALUE , "inputType" , inputType ) #IGNORE:E1101
        self._connection.marshall( Connector.DEF_STRING , "inputFileDescription"  ) #IGNORE:E1101
        self._connection.marshall( Connector.SET_VALUE , "inputFileDescription" , self.arrayToXml('INPUT',inputFileDescription) ) #IGNORE:E1101
        self._connection.marshall( Connector.DEF_STRING , "databaseTableDescription"  ) #IGNORE:E1101
        self._connection.marshall( Connector.SET_VALUE , "databaseTableDescription" , self.arrayToXml('DB',databaseTableDescription) ) #IGNORE:E1101
        # proceed with call 
        ret = self._connection.marshall( Connector.CALL ) #IGNORE:E1101
        # marshall cursor id back or None if cursorId is -1
        returned = self._connection.unmarshall( ret ) #IGNORE:E1101
        if returned == -1 :
            return None
        return returned
        
    def indexCsv( self , dbHandle , inputFile, inputType, inputFileDescription, databaseTableDescription):
        self.__index( DbIndexingClient._INDEX_FILE_ , dbHandle , inputFile, inputType, inputFileDescription, databaseTableDescription)
        
    def updateIndexCsv( self , dbHandle , inputFile, inputType, inputFileDescription, databaseTableDescription):
        self.__index( DbIndexingClient._UPDATE_INDEX_FILE_ , dbHandle , inputFile, inputType, inputFileDescription, databaseTableDescription)
        
    def __updateStr(self, info):
        if info[1] == COLTYPE_INT:
            return '%s=%s' % (info[2],info[3])
        return "%s='%s'" % (info[2],info[3])
        
    def updateDatabase( self , dbHandle, databaseTableDescription):
        setStr = []
        whereStr = []
        tableStr = []
        for requestInfo in databaseTableDescription:
            if requestInfo[0] == DBTABLE_DEF:
                tableStr.append(requestInfo[1])
            elif requestInfo[0] == DBTABLE_DEF_COL:
                setStr.append(self.__updateStr(requestInfo))
            elif requestInfo[0] == DBTABLE_UPDATE_KEY:
                whereStr.append(self.__updateStr(requestInfo))
        request = "update %s set %s where %s" % (''.join(tableStr), ', '.join(setStr), ' and '.join(whereStr))
        # print request
        mycursor = self.execSql(dbHandle , request)

#
# module main is just a practical sample test
# of JdbcClient usage
#
if __name__ == '__main__':
    myencoding = "ISO-8859-1" 
    myclient = DbIndexingClient(myencoding)
    try :
        myclient.connect()
        # load the JdbcDriver 
        # myclient.sqlInit("oracle.jdbc.driver.OracleDriver") 
        myclient.sqlInit("com.mysql.jdbc.Driver") 
        # connect the database 
        myDb = myclient.sqlOpen("jdbc:oracle:thin:@figaro:1521:FIGARODB" ,"producer_1_1a" , "producer" ) 
        # myDb = myclient.sqlOpen("jdbc:mysql://localhost/mo1" ,"MO1" , "MO1" ) 
        # myDb = myclient.sqlOpen("jdbc:mysql://localhost:3306/python" ,"python" , "python" ) 
        print 'my Db handle is : ' , myDb

        # TEST Indexing a Simple TechSort index File 
        """
String - InputFileName to be loaded 
String - InputFile type = Fixed or CSV
Dict - InputFileFormat = csv example : {{delimiter, '\t'},{'column',0,'identifier'},{'column',1,'name'}...}
.........................Fixed example : {{'column',0,'identifier','NUMBER', 20},{'column',1,'name','STRING', 30}...}

Dict - DatabaseTableFormat = {{'TableName','JOB_STATUS_AFTER_INSERT'},{ColumnName,ColumnType,Value,ValueType},{'Identifier','INTEGER','Identifier','InputName'},{'NAME','VARCHAR','Name','InputName'},{'VPFFile','VARCHAR','fichierAssocie.vpf','Constant'}...}
        """
        samplePath = "D:/Temp/producer"
        inputFile = "%s/000023.vpf.ind" % (samplePath)
        inputVPF = "%s/000023.vpf" % (samplePath)
        inputType = FILE_TYPE_VPF_IDX
        inputFileDescription = [[INPUT_CSV_DELIMITER,'\t']
                                ,[INPUT_DEF_COLUMN,1,'LASTNAME']
                                ,[INPUT_DEF_COLUMN,2,'FIRSTNAME']
                                ,[INPUT_DEF_COLUMN,3,'CLIENTID']
                                ]
        databaseTableDescription = [[DBTABLE_DEF,'JOB_STATUS_AFTER_INSERT']
                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'LAST_NAME','LASTNAME', COLINPUT]
                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'FIRST_NAME','FIRSTNAME', COLINPUT]
                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'CLIENT_ID','CLIENTID', COLINPUT]
                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'VPF_FILE',inputVPF, COLCONST]
                                    ,[DBTABLE_DEF_COL,COLTYPE_INT,'BUSYNESSID','BID000001', COLCONST]
#                                    ,[DBTABLE_DEF_COL,COLTYPE_INT,'JOBID','NULL', COLCONST]
#                                    ,[DBTABLE_DEF_COL,COLTYPE_INT,'FILEID','NULL', COLCONST]
                                    ]
        print myclient.arrayToXml('INPUT',inputFileDescription)
        print myclient.arrayToXml('DB',databaseTableDescription)
        myclient.indexCsv(myDb , inputFile, inputType, inputFileDescription, databaseTableDescription) 

        inputFile = "%s/000023.vpf.ind" % (samplePath)
        inputVPF = "%s/000023.vpf" % (samplePath)
        inputType = FILE_TYPE_VPF_IDX
        inputFileDescription = [[INPUT_CSV_DELIMITER,'\t']
                                ,[INPUT_DEF_COLUMN,1,'LASTNAME']
                                ,[INPUT_DEF_COLUMN,2,'FIRSTNAME']
                                ,[INPUT_DEF_COLUMN,3,'CLIENTID']
                                ]
        databaseTableDescription = [[DBTABLE_DEF,'JOB_STATUS_AFTER_INSERT']
                                    ,[DBTABLE_UPDATE_KEY,COLTYPE_STR,'BUSYNESSID','BID000001', COLCONST]
                                    ,[DBTABLE_UPDATE_KEY,COLTYPE_STR,'CLIENT_ID','CLIENTID', COLINPUT]
#                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'LAST_NAME','LASTNAME', COLINPUT]
#                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'FIRST_NAME','FIRSTNAME', COLINPUT]
#                                    ,[DBTABLE_DEF_COL,COLTYPE_STR,'VPF_FILE',inputVPF, COLCONST]
                                    ,[DBTABLE_DEF_COL,COLTYPE_INT,'JOBID','00001', COLCONST]
#                                    ,[DBTABLE_DEF_COL,COLTYPE_INT,'FILEID','NULL', COLCONST]
                                    ]
        print myclient.arrayToXml('INPUT',inputFileDescription)
        print myclient.arrayToXml('DB',databaseTableDescription)
        myclient.updateIndexCsv(myDb , inputFile, inputType, inputFileDescription, databaseTableDescription) 
        myclient.sqlClose(myDb) 
        myclient.disconnect()

    except SmdClientError , e :
        print "service instanciation error : " , str(e)
  
