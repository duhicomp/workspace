#!/usr/bin/env python

################################################################################
# Name: ParParser.py
# Description: This module parse a Remake .par file generate by Producer
# Copyright (c) 2007 Sefas Innovation
# Author Vinh Pham Duc
# Created on February 12, 2007
################################################################################
__revision__ = '$Revision$'
__date__ = '$Date$'

from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler

#################### JOB ####################
# <JOB>
#     <CUSTOMER>SEFAS</CUSTOMER>
#     <DEPARTMENT>SEFAS</DEPARTMENT>
#     <DOCUMENT_TYPE>AEGIS</DOCUMENT_TYPE>
#     <JOB_RECEIVED_DATE>20030403120247</JOB_RECEIVED_DATE>
#     <SLA_DUE_DATE>0</SLA_DUE_DATE>
#     <SLA_WARNING_OFFSET>0</SLA_WARNING_OFFSET>
#     <PROC_TYPE> </PROC_TYPE>
# </JOB>
JOB = 'JOB'
#CUSTOMER = 'CUSTOMER'
#DEPARTMENT = 'DEPARTMENT'
#DOCUMENT_TYPE = 'DOCUMENT_TYPE'
#JOB_RECEIVED_DATE = 'JOB_RECEIVED_DATE'
#SLA_DUE_DATE = 'SLA_DUE_DATE'
#SLA_WARNING_OFFSET = 'SLA_WARNING_OFFSET'
#PROC_TYPE = 'PROC_TYPE'

#################### ANADATA ####################
# <ANADATA>
#     <SORT_W>N</SORT_W>
#     <SERVICE_W>1</SERVICE_W>
#     <SORT_700>N</SORT_700>
#     <SERVICE_700>1</SERVICE_700>
#     <SORT_1400>N</SORT_1400>
#     <SERVICE_1400>1</SERVICE_1400>
#     <SORT_120>Y</SORT_120>
#     <SERVICE_120>1</SERVICE_120>
#     <MIXED_WEIGHT>N</MIXED_WEIGHT>
#     <AVERAGE_WEIGHT>60</AVERAGE_WEIGHT>
#     <BUNDLE_SIZE>25</BUNDLE_SIZE>
#     <FILE_SPLITTING>Y</FILE_SPLITTING>
#     <MAIL_PIECE_TYPE>LETTER</MAIL_PIECE_TYPE>
#     <FILE_ORDER>E</FILE_ORDER>
#     <SEQUENCE> </SEQUENCE>
# </ANADATA>
ANADATA = 'ANADATA'
#SORT_W = 'SORT_W'
#SERVICE_W = 'SERVICE_W'
#SORT_700 = 'SORT_700'
#SERVICE_700 = 'SERVICE_700'
#SORT_1400 = 'SORT_1400'
#SERVICE_1400 = 'SERVICE_1400'
#SORT_120 = 'SORT_120'
#SERVICE_120 = 'SERVICE_120'
#MIXED_WEIGHT = 'MIXED_WEIGHT'
#AVERAGE_WEIGHT = 'AVERAGE_WEIGHT'
#BUNDLE_SIZE = 'BUNDLE_SIZE'
#FILE_SPLITTING = 'FILE_SPLITTING'
#MAIL_PIECE_TYPE = 'MAIL_PIECE_TYPE'
#FILE_ORDER = 'FILE_ORDER'
#SEQUENCE = 'SEQUENCE'

#################### ADF_SPLIT ####################
# <ADF_SPLIT>
#     <CODE_SPLIT> </CODE_SPLIT>
#     <ENVELOPE_SPLIT>0</ENVELOPE_SPLIT>
#     <INSERT_SPLIT>0</INSERT_SPLIT>
#     <PAGE_SPLIT>0</PAGE_SPLIT>
# </ADF_SPLIT>
ADF_SPLIT = 'ADF_SPLIT'
#CODE_SPLIT = 'CODE_SPLIT'
#ENVELOPE_SPLIT = 'ENVELOPE_SPLIT'
#INSERT_SPLIT = 'INSERT_SPLIT'
#PAGE_SPLIT = 'PAGE_SPLIT'

#################### INPUTFILE ####################
# <LIST_INPUTFILE NB_ITERATIONS="2">
#     <INPUTFILE NO_IT="1">
#         <JOBID>512345</JOBID>
#         <CUSTOMER>AMERGE</CUSTOMER>
#         <DEPARTMENT>AMERGE</DEPARTMENT>
#         <DOCUMENTTYPE>BILLS_STATEMENTS</DOCUMENTTYPE>
#         <PATH>C:/clients/development/btnew/jobs/bills_statements/512345</PATH>
#     </INPUTFILE>
# </LIST_INPUTFILE>
LIST_INPUTFILE = 'LIST_INPUTFILE' 
INPUTFILE = 'INPUTFILE'
NO_IT = 'NO_IT'
#NB_ITERATIONS = 'NB_ITERATIONS'
#JOBID = 'JOBID'
#DOCUMENTTYPE = 'DOCUMENTTYPE'
#PATH = 'PATH'

#################### OUTPUTFILE ####################
# <LIST_OUTPUTFILE NB_ITERATIONS="1">
#     <OUTPUTFILE NO_IT="1">
#         <FILENUMBER>01</FILENUMBER>
#         <FILENAME>BAD</FILENAME>
#         <FORMTYPE></FORMTYPE>
#         <PRINTING_REQUIREMENTS></PRINTING_REQUIREMENTS>
#         <MAILING_REQUIREMENTS></MAILING_REQUIREMENTS>
#         <ENVELOPE_ID> </ENVELOPE_ID>
#         <HOPPER1> </HOPPER1>
#         <HOPPER2> </HOPPER2>
#         <HOPPER3> </HOPPER3>
#         <HOPPER4> </HOPPER4>
#         <HOPPER5> </HOPPER5>
#         <HOPPER6> </HOPPER6>
#         <HOPPER7> </HOPPER7>
#         <HOPPER8> </HOPPER8>
#         <HOPPER9> </HOPPER9>
#     </OUTPUTFILE>
# </LIST_OUTPUTFILE>
LIST_OUTPUTFILE = 'LIST_OUTPUTFILE' 
OUTPUTFILE = 'OUTPUTFILE'
#FILENUMBER = 'FILENUMBER'
#FILENAME = 'FILENAME'
#FORMTYPE = 'FORMTYPE'
#PRINTING_REQUIREMENTS ='PRINTING_REQUIREMENTS'
#MAILING_REQUIREMENTS = 'MAILING_REQUIREMENTS'
#ENVELOPE_ID = 'ENVELOPE_ID'
#HOPPER = 'HOPPER'
# Old version of .par file ?
LIST_OUTPUTTYPE = 'LIST_OUTPUTTYPE' 
OUTPUTTYPE = 'OUTPUTTYPE'

#################### STOCKCODE ####################
# <LIST_STOCKCODE NB_ITERATIONS="1">
#     <STOCKCODE NO_IT="1">
#         <STKNAME>9999</STKNAME>
#         <LOGICAL>MAIN</LOGICAL>
#         <PHYSICAL>MAIN</PHYSICAL>
#     </STOCKCODE>
# </LIST_STOCKCODE>
LIST_STOCKCODE = 'LIST_STOCKCODE' 
STOCKCODE = 'STOCKCODE'
#STKNAME = 'STKNAME'
#LOGICAL = 'LOGICAL'
#PHYSICAL = 'PHYSICAL'

class ParParser(ContentHandler):
    
    def __init__(self, parms, logger = None):
        self.buffer = ''

        # .par files parameters
        self._params = parms

        # logger for message trace
        self._logger = logger
        
        # List of Job atttributes
        self._inJob = False
        self._jobAttrs = {}
        self._params[JOB] = self._jobAttrs

        # List of Anadata atttributes
        self._inAnadata = False
        self._anadataAttrs = {}
        self._params[ANADATA] = self._anadataAttrs
        
        # List of AdfSplit atttributes
        self._inAdfSplit = False
        self._adfSplitAttrs = {}
        self._params[ADF_SPLIT] = self._adfSplitAttrs
        
        # List of Input files in .par file    
        self._inInputFile = False
        self._listInputFile = {}
        self._params[LIST_INPUTFILE] = self._listInputFile
        self._inputFile = {}

        # List of Output files in .par file
        self._inOutputFile = False
        self._listOutputFile = {}
        self._params[LIST_OUTPUTFILE] = self._listOutputFile
        self._outputFile = {}

        # List of Stock codes in .par file
        self._inStockCode = False
        self._listStockCode = {}
        self._params[LIST_STOCKCODE] = self._listStockCode
        self._stockCode = {}

        # Dynamic tags
        self._inDynamicTag = False
        self._curTagName = ''
        self._dynamicTags = {}

    ############################################################
    # Add dynamic tags.
    ############################################################
    def addDynamicTags(self, dynamicTags):
        self._dynamicTags = dynamicTags

    ##############################################################################
    # Called before the parser starts processing the first element in the document
    ##############################################################################
    #def startDocument(self):
    #    printMsg "--------  Document Start --------"
    
    ##############################################################################
    # Called when the parser reaches the end of the document
    ##############################################################################
    #def endDocument(self):
    #    printMsg "--------  Document End --------"        
    
    ##############################################################################
    # Check if tagName is dynamic tag
    ##############################################################################
    def isDynamicTag(self, tagName):
       for tagNbr in self._dynamicTags:
          if self._dynamicTags[tagNbr] == tagName:
              return True
       return False
        
    ############################################################
    # Called when the parser finds a start tag.
    ############################################################
    def startElement(self,name,attrs):
        self.printMsg ('start name : ' + name)
        #if not attrs is None :
        #    for attrName in attrs.keys():     
        #        printMsg '          attrs [', attrName, '] value [', attrs.get(attrName), ']'
        self.buffer = ''
        if name == JOB:
            self._inJob = True
        elif name == ANADATA:
            self._inAnadata = True
        elif name == ADF_SPLIT:
            self._inAdfSplit = True
        elif name == INPUTFILE:    
            inIter = attrs.get(NO_IT)    
            self._inputFile = {}
            self._listInputFile[inIter] = self._inputFile 
            self._inInputFile = True
        elif name == OUTPUTFILE or name == OUTPUTTYPE:    
            outIter = attrs.get(NO_IT)    
            self._outputFile = {}
            self._listOutputFile[outIter] = self._outputFile 
            self._inOutputFile = True
        elif name == STOCKCODE:    
            stockIter = attrs.get(NO_IT)    
            self._stockCode = {}
            self._listStockCode[stockIter] = self._stockCode 
            self._inStockCode = True
        elif self.isDynamicTag(name):
            self._curTagName = name
            self._tagAttrs = {}
            self._params[name] = self._tagAttrs
            self._inDynamicTag = True
            
        
    ############################################################
    # Called when the parser finds an end tag.
    ############################################################
    def endElement(self,name):
        self.printMsg ('end name [' + name + '] value [' + self.buffer.strip() + ']')
        
        if name == JOB:
            self._inJob = False
        elif name == ANADATA:
            self._inAnadata = False
        elif name == ADF_SPLIT:
            self._inAdfSplit = False
        elif name == INPUTFILE:
            self._inInputFile = False
        elif name == OUTPUTFILE or name == OUTPUTTYPE:
            self._inOutputFile = False
        elif name == STOCKCODE:
            self._inStockCode = False
        elif self.isDynamicTag(name):        
            self._inDynamicTag = False
            self._curTagName = ''

        if (self._inJob == True):
            self._jobAttrs[name] = self.buffer.strip()
        elif (self._inAnadata == True):
            self._anadataAttrs[name] = self.buffer.strip()
        elif (self._inAdfSplit == True):
            self._adfSplitAttrs[name] = self.buffer.strip()
        elif (self._inInputFile == True):
            self._inputFile[name] = self.buffer.strip()
        elif (self._inOutputFile == True):
            self._outputFile[name] = self.buffer.strip()
        elif (self._inStockCode == True):
            self._stockCode[name] = self.buffer.strip()
        elif (self._inDynamicTag == True):
            #self.printMsg ('$$$$$$$$$$ curTagName: ' +self._curTagName + ' name: ' + name + ' buffer: ' + self.buffer.strip())
            self._tagAttrs[name] = self.buffer.strip()


    ##############################################################
    # Called when the parser finds data content within an element
    ##############################################################
    def characters(self,chars):
        self.buffer += chars

    ##############################################################
    # Parse a .par file (XML file)
    ##############################################################
    def parse(self,handler, xmlParamFile):
        self.printMsg ('** XMLParFile: ' + xmlParamFile)
        parser = make_parser()
        parser.setContentHandler(handler)
        try:
            parser.parse(open(xmlParamFile))
        except SAXException:
            self.printMsg ('** Error while parsing file: ' + xmlParamFile)
            return None
        return self._params
    
    ##############################################################
    # Get current JOB parameters
    ##############################################################
    def getJobParameters(self):
        return self._params[JOB]
    
    ##############################################################
    # Get current ANADATA parameters
    ##############################################################
    def getAnadataParameters(self):
        return self._params[ANADATA]

    ##############################################################
    # Get current ADF_SPLIT parameters
    ##############################################################
    def getAdfSplitParameters(self):
        return self._params[ADF_SPLIT]
    
    ##############################################################
    # Get current list of input files parameters
    ##############################################################
    def getInputFilesParameters(self):
        return self._params[LIST_INPUTFILE]
    
    ##############################################################
    # Get current list of output files parameters
    ##############################################################
    def getOutputFilesParameters(self):
        return self._params[LIST_OUTPUTFILE]

    ##############################################################
    # Get current list of stock codes parameters
    ##############################################################
    def getStockCodesParameters(self):
        return self._params[LIST_STOCKCODE]

    ##############################################################
    # Get current list of dynamic tag parameters
    ##############################################################
    def getDynamicTagParameters(self, tagName):
        if self.isDynamicTag(tagName):
            return self._params[tagName]
        else:
            self.printMsg ("Can't find Dynamic Tag: " +tagName)
    
    ##############################################################
    # Get current list of stock codes parameters
    ##############################################################
    def printMsg(self, message):
        if self._logger is not None:
            # USING INFO log4py
            self._logger.info(message)
        else :
            print message

    ##############################################################
    # Dump the content of .par file loaded in memory
    ##############################################################
    def dumpParameters(self, parameters):    
        self.printMsg ("========== .PAR FILE CONTENTS ==========")
        self.printMsg ('---------- JOB ----------')
        attrs = parameters[JOB]
        for attrName in attrs:
            self.printMsg (attrName + ': ' + attrs[attrName])

        self.printMsg ('---------- ANADATA ----------')
        attrs = parameters[ANADATA]
        for attrName in attrs:
            self.printMsg (attrName + ': ' + attrs[attrName])

        self.printMsg ('---------- ADF_SPLIT ----------')
        attrs = parameters[ADF_SPLIT]
        for attrName in attrs:
            self.printMsg (attrName + ': ' + attrs[attrName])

        self.printMsg ('---------- INPUT FILE(S) ----------')
        listInputFile = parameters[LIST_INPUTFILE]
        listKeys = listInputFile.keys()
        listKeys.sort()
        for i in listKeys:
            keys = listInputFile[i].keys()
            keys.sort()
            self.printMsg ('----- [' + i + ']-----')
            for attrName in keys:
                 self.printMsg (attrName + '['+i+']: ' + listInputFile[i][attrName])

        self.printMsg ('---------- OUTPUT FILE(S) ----------')
        listOutputFile = parameters[LIST_OUTPUTFILE]
        listKeys = listOutputFile.keys()
        listKeys.sort()
        for i in listKeys:
            keys = listOutputFile[i].keys()
            keys.sort()
            self.printMsg ('----- [' + i + ']-----')
            for attrName in keys:
                self.printMsg (attrName + '['+i+']: ' + listOutputFile[i][attrName])

        self.printMsg ('---------- STOCK CODE(S) ----------')
        listStockCode = parameters[LIST_STOCKCODE]
        listKeys = listStockCode.keys()
        listKeys.sort()
        for i in listKeys:
            keys = listStockCode[i].keys()
            keys.sort()
            self.printMsg ('----- [' + i + ']-----')
            for attrName in keys:
                self.printMsg (attrName + '['+i+']: ' + listStockCode[i][attrName])
        self.printMsg ("==========================================")

        
if __name__ == '__main__':
    import sys
    xmlParFile = ' '.join(sys.argv[1:])
    #xmlParFile = 'D:\\DEV\\scripts\\python\\test\\split_proc_ip.par'
    xmlParFile = 'D:\\DEV\\scripts\\python\\test\\nosplit_noproc.par'
    #xmlParFile = 'D:\\DEV\\scripts\\python\\test\\premerge.par'
    params = {}
    
    # Add dynamic tags
    #dynamicTags = {}
    #dynamicTags[0] = 'CUST_TAG1'
    #dynamicTags[1] = 'CUST_TAG2'
    #dynamicTags[2] = 'REMAKE'
    h = ParParser(params)
    #h.addDynamicTags(dynamicTags)
    params = h.parse(h, xmlParFile)
    #h.dumpParameters(params)
    
    print '---------- BEGIN TEST STOCK CODE(S) ----------'
    listStockCodes = h.getStockCodesParameters()
    listKeys = listStockCodes.keys()
    listKeys.sort()
    for i in listKeys:
        keys = listStockCodes[i].keys()
        keys.sort()
        print '----- [',i,']-----'
        for attrName in keys:
            print attrName,'['+i+']: ',listStockCodes[i][attrName]
    print '---------- END TEST STOCK CODE(S) ----------'
    
    # Test dynamic tag
    #tagName = 'REMAKE'
    #print '---------- BEGIN TEST DYNAMIC TAG [' + tagName + '] ----------'
    #listDynamicTag = h.getDynamicTagParameters(tagName)
    #listKeys = listDynamicTag.keys()
    #for attrName in listKeys:
    #    print attrName,': ',listDynamicTag[attrName]
    #print '---------- END TEST DYNAMIC TAG [' + tagName + '] ----------'
    
        
