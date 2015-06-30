#
# Python client class to Jdbc SqlExecFactory SMD service
#       
__revision__ = '$Revision$'
__date__ ='$Date$'

import sys
import os
import os.path
from Connector import Connector,SmdClientError
from StringReplaceUtils import *


class JdbcClient:
    """Python Client interface to the SqlFactory SMD service """

    FETCH_ALL = -1 # get all results in one call (USE CAUTIOUSLY)
    CLASSFACTORY = 'com.sefas.gridclient.sqlservices.SqlExecFactory'
    
    METHOD_NAME_SET_DBSCHEMA = "setDBSchema"
    METHOD_NAME_SET_DBCATALOG = "setDBCatalog"

    PARAM_NAME_DBSCHEMA = "dbSchema"
    PARAM_NAME_DBCATALOG = "dbCatalog"

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

    def connect( self ) :
        """ connect to SqlFactory Service """
        if ( self._connection != None ):
            return
        self._connection = Connector( self._host , self._port , self._encoding,  self.CLASSFACTORY )

    def sqlInit( self ,  jdbcDriver ):
        """ load JdbcDriver return Nothing or exception on failure """ 
        self._connection.marshall( Connector.SET_METHOD , "sqlInit" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_STRING , "driver"  )
        self._connection.marshall( Connector.SET_VALUE , "driver" , jdbcDriver )
        self._connection.marshall( Connector.DEF_STRING , "encoding"  )
        self._connection.marshall( Connector.SET_VALUE , "encoding" , self._encoding )
        # proceed with call 
        self._connection.marshall( Connector.CALL )

    def sqlOpen( self ,  jdbcString , userid , passwd ):
        """ connect to requested database through the provided jdbc string """ 
        self._connection.marshall( Connector.SET_METHOD , "sqlOpen" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_STRING , "dbstring"  )
        self._connection.marshall( Connector.SET_VALUE , "dbstring" , jdbcString )
        self._connection.marshall( Connector.DEF_STRING , "user"  )
        self._connection.marshall( Connector.SET_VALUE , "user" , userid )
        self._connection.marshall( Connector.DEF_STRING , "passwd"  )
        self._connection.marshall( Connector.SET_VALUE , "passwd" , passwd )
        # proceed with call 
        ret = self._connection.marshall( Connector.CALL )
        # marshall the Db id back
        return int(self._connection.unmarshall( ret ))
        
    def execSql( self , dbHandle , statement ):
        """ execute provided sql statement on given dbHandle """ 
        self._connection.marshall( Connector.SET_METHOD , "execSql" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_INTEGER , "dbHandle"  )
        self._connection.marshall( Connector.SET_VALUE , "dbHandle" , str(dbHandle) )
        self._connection.marshall( Connector.DEF_STRING , "statement"  )
        self._connection.marshall( Connector.SET_VALUE , "statement" , statement )
        # proceed with call 
        ret = self._connection.marshall( Connector.CALL )
        # marshall cursor id back or None if cursorId is -1
        returned = int(self._connection.unmarshall( ret ))
        if returned == -1 :
            return None
        return returned
        
    def callSql( self , dbHandle , callfx , *args  ):
        """ call callfx stored procedure with providing argument list """ 
        # build the jdbc call string argument
        statement = '{call %s (' % callfx
        statementArgs = ''
        for arg in args :
            statement = ''.join( [ statement , '?' ] )
            statementArgs = ''.join( [ statementArgs , "'" , arg  , "'" ] )
            if arg != args[-1] :
                statement = ''.join( [ statement , ',' ] )
                statementArgs = ''.join( [ statementArgs , ',' ] )
            
        statement = ' '.join( [ statement , ') }' ] )
        self._connection.marshall( Connector.SET_METHOD , "callSql" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_INTEGER , "dbHandle"  )
        self._connection.marshall( Connector.SET_VALUE , "dbHandle" , str(dbHandle) )
        self._connection.marshall( Connector.DEF_STRING , "statement"  )
        self._connection.marshall( Connector.SET_VALUE , "statement" , statement )
        self._connection.marshall( Connector.DEF_STRING , "statementargs"  )
        self._connection.marshall( Connector.SET_VALUE , "statementargs" , statementArgs )
        # proceed with call 
        ret = self._connection.marshall( Connector.CALL )
        # marshall cursor id back or None if cursorId is -1
        returned = int(self._connection.unmarshall( ret ))
        if returned == -1 :
            return None
        return returned
        
    def sqlCursorClose( self ,  csHandle ):
        """ close a previously opened cursor on a given database handle for concurent querries""" 
        self._connection.marshall( Connector.SET_METHOD , "sqlCursorClose" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_INTEGER , "cshandle"  )
        self._connection.marshall( Connector.SET_VALUE , "cshandle" , csHandle )
        # proceed with call 
        self._connection.marshall( Connector.CALL )
        
    def sqlClose( self ,  dbHandle ):
        """ close a previously opened db connection""" 
        self._connection.marshall( Connector.SET_METHOD , "sqlClose" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_INTEGER , "dbhandle"  )
        self._connection.marshall( Connector.SET_VALUE , "dbhandle" , dbHandle )
        # proceed with call 
        self._connection.marshall( Connector.CALL )
        
    def sqlFetch( self ,  csHandle , nbrow = 1):
        """ close a previously opened cursor on a given database handle for concurent querries""" 
        self._connection.marshall( Connector.SET_METHOD , "sqlFetch" ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_INTEGER , "cshandle"  )
        self._connection.marshall( Connector.SET_VALUE , "cshandle" , csHandle )
        self._connection.marshall( Connector.DEF_INTEGER , "nbrow"  )
        self._connection.marshall( Connector.SET_VALUE , "nbrow" , nbrow )
        # proceed with call 
        ret = self._connection.marshall( Connector.CALL )
        # unmarshall sqlresult back
        returned = self._connection.unmarshall( ret )
        if returned == -1 :
            return None
        # Fetch provides a Python compliant result back so using 
        # eval is simply fast and elegant here
        dc = self._connection._decoder # NB USED inside eval string
        returned = eval(returned , sys._getframe(0).f_globals ,sys._getframe(0).f_locals)
        if len(returned) == 0 :
            return None
        return returned
    
    def setDBSchema( self, dbSchema ):
        #ETHOD_NAME_SET_DBSCHEMA = "setDBSchema"
        self._connection.marshall( Connector.SET_METHOD, self.METHOD_NAME_SET_DBSCHEMA ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_STRING, self.PARAM_NAME_DBSCHEMA  )
        self._connection.marshall( Connector.SET_VALUE, self.PARAM_NAME_DBSCHEMA, dbSchema )
        # proceed with call 
        self._connection.marshall( Connector.CALL )

    def setDBCatalog( self, dbCatalog ):
        self._connection.marshall( Connector.SET_METHOD, self.METHOD_NAME_SET_DBCATALOG ) 
        # populate parameters
        self._connection.marshall( Connector.DEF_STRING, self.PARAM_NAME_DBCATALOG  )
        self._connection.marshall( Connector.SET_VALUE, self.PARAM_NAME_DBCATALOG, dbCatalog )
        # proceed with call 
        self._connection.marshall( Connector.CALL )
    
    def __trace( self , msg , verbose ) :
        if verbose :
            print msg

        
    def __isStoredProc( self , sqlStmt ):
        """ return true if current sqlstmt is a create function or package """
        curCheck = sqlStmt.replace('%%cr%%' , '').lstrip()
        storeprocChecker = curCheck.split(' ')
        if len(storeprocChecker) < 2 :
            return False
        if ( storeprocChecker[0] == 'CREATE' or 'create' ) :
            if storeprocChecker[1] == 'or' or 'OR' :
                pos = 3
            else :
                pos = 2
            if len(storeprocChecker) <= pos : 
                return False
              
            if storeprocChecker[pos] == 'package' or \
               storeprocChecker[pos] == 'PACKAGE' or \
               storeprocChecker[pos] == 'function' or \
               storeprocChecker[pos] == 'FUNCTION' or \
               storeprocChecker[pos] == 'trigger' or \
               storeprocChecker[pos] == 'TRIGGER' :
                return True
            else:
                if ( storeprocChecker[pos] == 'type' or \
                     storeprocChecker[pos] == 'TYPE' ) and \
                   ( storeprocChecker[pos+1] == 'body' or \
                     storeprocChecker[pos+1] == 'BODY' ) :
                    return True
                return False
            
    def __checkStoredProc( self , sqlStmt ):
        """ split non stored procedure sequences """
        if self.__isStoredProc(sqlStmt) :
            return None
        else:
            return sqlStmt.split(';')

    def __emptySql( self , sqlStmt ):
        """ check for empty sql statement """
        curCheck = sqlStmt.replace('%%cr%%' , '').lstrip()
        if curCheck == '' or curCheck == '.'  or curCheck == 'exit' :
            # dot is sometime used as kind of separator = ignore it
            return True
        return False
    
    def _purgeLeadingSpace( self , sqlStmts ):
        """ return sqlstm removing leading \n and spaces"""
        sqlStmts = sqlStmts.lstrip(' ')
        sqlStmts = sqlStmts.lstrip('\n')
        return sqlStmts
    
    def __procesQuoted ( self , sqlStmt ) :
        """ process ; inside quote """
        sqlStmt = sqlStmt.replace( ';' , '%%semicol%%' )
        return sqlStmt
        
        
    def __purgeComments( self , sqlStmts ) :
        """ purge ; / inside sqlcomments """
        sqlStmts = sqlStmts.split('\n')
        i = 0
        inMultiLineComment = False
        while i < len(sqlStmts) :
            # remove leading spaces
            sqlStmts[i] = sqlStmts[i].lstrip()
            sqlStmt = sqlStmts[i] 
            # check for -- / and ; in current line
            multiLineComPos = sqlStmt.find('/*')
            if multiLineComPos != -1 :
                inMultiLineComment = True
            if inMultiLineComment :
                multiLineComPosEnd = sqlStmt.find('*/')
                if multiLineComPosEnd == -1 :
                    del sqlStmts[i]
                else :
                    sqlStmts[i] = sqlStmt[multiLineComPosEnd+2:]
                    i = i+1
                    inMultiLineComment = False
            else :
                commentPos = sqlStmt.find('--')
                quotePos = sqlStmt.find("'")
                semicolPos = sqlStmt.find(';')
                # check for sqlplus / execute statement separator 
                wk = sqlStmts[i].strip()
                if len(wk) == 1 and wk == '/':
                    pass
                else :
                    # replace any / 
                    sqlStmts[i] = sqlStmt.replace( '/' , '%%slash%%' )
                    sqlStmt = sqlStmts[i] 
                if commentPos != -1 :
                    if semicolPos > commentPos :
                        sqlStmts[i] = sqlStmt.replace( ';' , '%%semicol%%' )
                else :
                    if semicolPos != -1 :
                        # only change when / or ; in constants
                        while quotePos != -1 :
                            # process multiple paired quoted 
                            endQuote = sqlStmt.find("'",quotePos+1)
                            sliced = self.__procesQuoted(sqlStmt[quotePos:endQuote+1])
                            newEndQuote = (quotePos-1) + len(sliced) # recomp after transformation
                            sqlStmts[i] = ''.join([sqlStmt[0:quotePos] , sliced , sqlStmt[endQuote+1:]   ])
                            sqlStmt = sqlStmts[i]
                            quotePos = sqlStmt.find("'",newEndQuote+1)
                    # don't care about '.' DOT end of sqlblocs and get rid of them
                    if len(wk) == 1 and wk == '.' :
                        del sqlStmts[i]

                i = i+1
        returned = '\n'.join(sqlStmts) ;
        return returned
        
    def __purgeLeadingComments( self , sqlStmts ) :
        """ purge -- before sql commands """
        sqlStmts = sqlStmts.replace('%%cr%%' , '\n')
        sqlStmts = sqlStmts.split('\n')
        # check for leading --
        while ( sqlStmts != [] ) and \
              (  len( sqlStmts[0] ) == 0 or \
                 sqlStmts[0][:2] == '--' ) :
            del sqlStmts[0]
        sqlStmts = '\n'.join(sqlStmts)
        return sqlStmts.replace('\n','%%cr%%')
        
    def __isDrop( self , sqlStmt ) :
        first = sqlStmt.split()[0].strip().upper()
        if first == 'DROP' :
            return True
        return False
        

    def __processScriptUnit( self , scriptFName , dbHandle , sqlStmt ) :
        """ process single script SQL element """
        try :
            isDrop = False
            sqlStmt = self.__purgeLeadingComments(sqlStmt)
            sqlStmt = sqlStmt.replace('}', '%%clbracket%%' )
            sqlStmt = sqlStmt.replace('{', '%%opbracket%%' )
            # check for emptyness after
            if not self.__emptySql(sqlStmt) :
                isDrop = self.__isDrop(sqlStmt) 
                cursor = self.execSql(dbHandle , sqlStmt)
                # fetch until the end of the resultset requesting 10 rows by fetch
                if cursor != None :
                    srows = self.sqlFetch( cursor , self.FETCH_ALL )
                    sqlStmt = sqlStmt.replace('%%cr%%' , '')
                    print scriptFName + ":"+ sqlStmt + " rows = " , srows
                    self.sqlCursorClose(cursor)
        except SmdClientError , f :
            # ignore error on SQL drop (May be refined) 
            if not isDrop :
                sqlStmt = sqlStmt.replace( '%%cr%%' , '\n' )
                print 'sqlprocessing error : ' + str(f)
                print 'on statement :' + sqlStmt
        
    def sqlScript( self , dbHandle , scriptFName , verbose = True ) :
        """ execute Sql semicolon separated SQL statement Script files based
            on oracle sqlplus script syntax 
        """
        # open the script file
        try :
            f = open( scriptFName ) 
            self.__trace( "*-- START processing sql script :" + scriptFName , verbose)
            sqlContent = f.read()
            if self._variableDict != None:
                sqlContent = replaceStringToString(sqlContent,self._variableDict,FORMAT_DEFAULT)
            
        except IOError :
            raise SmdClientError , "inexisting SQL script :" + scriptFName
        # get ridd of any SQL separators collision (/and ;) inside comments first
        sqlContent = sqlContent.split('\r')
        sqlContent = ''.join(sqlContent)
        sqlContent = self.__purgeComments(sqlContent)
        # locate /  in read buffer as basic command separator
        sqlStmts = sqlContent.split('/')
        print '%i sql statement(s) found in %s' % ( len(sqlStmts) , scriptFName )
        # for each semicolon separated SQL statement : process the statement
        for sqlStmt in sqlStmts :
            sqlStmt = self._purgeLeadingSpace(sqlStmt)
            # replace syntaxic SMD \n by %%cr%%
            sqlStmt = sqlStmt.replace('\n' , '%%cr%%' )
            # parse the beginning of the received statement toc check for CREATE PROCEDURE
            # where semicolons are not considered as statement separators
            if not self.__emptySql(sqlStmt) :
                # remove any comments before checking for stored proc
                sqlStmt = self.__purgeLeadingComments(sqlStmt)
                secondSplit = self.__checkStoredProc(sqlStmt)
                if secondSplit != None :
                    last = len(secondSplit)
                    iii = 0 
                    while iii < last :
                        secondSql = secondSplit[iii]
                        # check if current is a trigger,function or package which
                        # implies current is last then
                        if self.__isStoredProc(secondSplit[iii]) :
                            secondSql = ';'.join(secondSplit[iii:])
                            iii = last # force ending then
                        self.__processScriptUnit(scriptFName,dbHandle,secondSql)
                        iii = iii + 1
                else :
                    self.__processScriptUnit(scriptFName,dbHandle,sqlStmt)
        self.__trace( "*-- END processing sql script :" + scriptFName , verbose)


    def sqlScriptDir(  self , dbHandle , startDir , verbose = False) :
        """ process all .sql scripts located in provided directory """
        directories = [startDir]
        while len(directories) > 0 :
            directory = directories.pop()
            for name in os.listdir(directory):
                fullpath = os.path.join(directory,name)               
                if os.path.isfile(fullpath) and fullpath.endswith('.sql') :
                    # That's a file. process it as SQL. 
                    self.sqlScript(dbHandle,fullpath,verbose)
                elif os.path.isdir(fullpath):
                    directories.append(fullpath)  # It's a directory, store it.

    def disconnect( self ):
        """ Disconnect from SqlFactory Service """
        if ( self._connection != None ):
            self._connection.close() 
            self._connection = None

#
# module main is just a practical sample test
# of JdbcClient usage
#
if __name__ == '__main__':
    myencoding = "ISO-8859-1" 
    myclient = JdbcClient(myencoding)
    try :
        myclient.connect()
        # load the JdbcDriver 
        # myclient.sqlInit("oracle.jdbc.driver.OracleDriver") 
        myclient.sqlInit("com.mysql.jdbc.Driver") 
        # connect the database 
        # myDb = myclient.sqlOpen("jdbc:oracle:thin:@figaro:1521:FIGARODB" ,"scott" , "tiger" ) 
        # myDb = myclient.sqlOpen("jdbc:mysql://localhost/mo1" ,"MO1" , "MO1" ) 
        myDb = myclient.sqlOpen("jdbc:mysql://localhost/chicago" ,"scott" , "tiger" ) 
        print 'my Db handle is : ' , myDb
        mycursor = myclient.execSql(myDb , "SELECT * from 07192006_live") 
        # fetch until the end of the resultset requesting 10 rows by fetch
        rows = myclient.sqlFetch( mycursor )
        rownum = 1 
        while rows != None :
            print '%i row with DE8=%s' % (rownum,rows[0]['DE8'])
            rows = myclient.sqlFetch( mycursor )
            rownum = rownum + 1

        # test SQL scripting
        # myclient.sqlScript(myDb , "d:/producer/sql_create_tables/create_xdf_split_type_params.sql")
        # myclient.sqlScript(myDb , "d:/producer/sql_create_tables/create_adf_split_type_params.sql")
        # TEST QUOTING problem 
        mycursor = myclient.execSql(myDb , "SELECT * from RES_DESC WHERE ID=14") 
        # fetch until the end of the resultset requesting 10 rows by fetch
        rows = myclient.sqlFetch( mycursor , myclient.FETCH_ALL )
        print 'my second cursor handle is : ' , mycursor
        print "rows = " , rows
        for line in rows:
            colUnicode = line['COL1']
            # print french accents using codec encoding 
            print "col = " , colUnicode.encode(myencoding)

        myclient.sqlCursorClose(mycursor) 
        # SELECT WIT quotes test
        mycursor = myclient.execSql(myDb , "SELECT * FROM RES_DESC WHERE ID=14") 
        # mycursor = myclient.execSql(myDb , "SELECT * FROM EMP WHERE ename='SMITH'") 
        # mycursor = myclient.execSql(myDb , "select RES_DESC_CHILD from ENV_HIERAR_DESC_LNK where ENV_HIERAR_PARENT in(select ID from ENV_HIERAR where NAME = 'user1')") 
        rows = myclient.sqlFetch( mycursor , 10)
        print 'my cursor handle is : ' , mycursor
        while rows != None :
            print "rows = " , rows
            rows = myclient.sqlFetch( mycursor , 10)
        # fetch until the end of the resultset requesting 10 rows by fetch
        myclient.sqlCursorClose(mycursor) 
        mycursor = myclient.execSql(myDb , "SELECT * from ENVIRONNEMENT") 
        # fetch until the end of the resultset requesting 10 rows by fetch
        rows = myclient.sqlFetch( mycursor , myclient.FETCH_ALL )
        print 'my second cursor handle is : ' , mycursor
        print "rows = " , rows
        myclient.sqlCursorClose(mycursor) 
        # FETCH ALL test
        mycursor = myclient.execSql(myDb , "SELECT * from RES_DESC") 
        # fetch until the end of the resultset requesting 10 rows by fetch
        rows = myclient.sqlFetch( mycursor )
        while rows != None :
            print "rows = " , rows
            rows = myclient.sqlFetch( mycursor )
        print 'my second cursor handle is : ' , mycursor
        print "rows = " , rows
        myclient.sqlCursorClose(mycursor) 
        # INVALID SQL SYNTAX TEST
        print "looping lot of times"
        for ii in xrange(1000):
            mycursor = myclient.execSql(myDb , "SELECT * from ENVIRONNEMENT") 
            print "ii = " , ii
            # fetch until the end of the resultset requesting 10 rows by fetch
            rows = myclient.sqlFetch( mycursor  )
            while rows != None :
            #    print "rows = " , rows
                rows = myclient.sqlFetch( mycursor )
            # finally close the used cursor
            myclient.sqlCursorClose(mycursor) 
        # and the database
        myclient.sqlClose(myDb) 
        myclient.disconnect()

    except SmdClientError , e :
        print "service instanciation error : " , str(e)
  
