#!/usr/bin/env python

import sys
from ParameterContainer import ParameterContainer

HEADER_INDENT=''
HEADER_DOCUMENT_INDENT='   '
FILE_INDENT='   '
FILE_DETAIL_INDENT='      '
FILE_INPUT_INDENT='         '
FILE_DETAIL_INPUT_INDENT='            '


"""
<xml>
      <OUTPUTFILELIST>
            <FILE> 
                __ListFileReturnProducer[] -> HeaderReturnProducer.flush() 
            </FILE>
      </OUTPUTFILELIST>
</xml>

"""
class ReturnProducerUtils:
    
    def __init__(self,paramContainer, toInputDir=True, withXmlTag=False):
        if toInputDir :
            self.__returnFileName = "%s/%s.ret" % (paramContainer.getInputDir(), paramContainer.getJobID())
        else:
            self.__returnFileName = "%s/%s.ret" % (paramContainer.getFullPathJobDir(), paramContainer.getJobID())
        self.__headerReturnProducer = HeaderReturnProducer()
        self.__ListFileReturnProducer = []
        self.__withXmlTag = withXmlTag

    def setHeaderInformation(self, documentLst):
        self.__headerReturnProducer.setHeaderInformation(documentLst)

    def addFileReturn(self, fileReturn):
        # if fileReturn is FileReturnProducer:
        self.__ListFileReturnProducer.append(fileReturn)
        # else:
        #    raise Exception("Only FileReturnProducer instances can be added as File Return : %s not allowed" % (type(fileReturn)))
        
    def flush(self):
        f = open(self.__returnFileName,"w")
        f.writelines(self.getXml())
        f.close()
        
    def getXml(self):
        resu =[]
        if self.__withXmlTag :
            resu.append('<xml>\n')
        resu.append(self.__headerReturnProducer.flush())
        resu.append(HEADER_INDENT)
        resu.append('<OUTPUTFILELIST>\n')
        resu.append(''.join(''.join([FILE_INDENT,'<FILE>\n',value.flush(),FILE_INDENT,'</FILE>\n']) for value in self.__ListFileReturnProducer))
        resu.append(HEADER_INDENT)
        resu.append('</OUTPUTFILELIST>\n')
        if self.__withXmlTag :
            resu.append('</xml>\n')
        return ''.join(resu)

"""
<HEADER>
      <DOCUMENTS>__documentLst[] -> FileReturnProducer.flush() </DOCUMENTS>
</HEADER>

"""
class HeaderReturnProducer:
    
    def __init__(self):
        self.__documentLst = []

    def setHeaderInformation(self, documentLst):
        if documentLst is not None:
            if type(documentLst) is list:
                self.__documentLst = documentLst
            else:
                self.__documentLst = [documentLst]
        else:
            self.__documentLst = []
    
    def flush(self):
        return "%s<HEADER>\n%s%s</HEADER>\n" % (HEADER_INDENT, ''.join(''.join([HEADER_DOCUMENT_INDENT,'<DOCUMENTS>',str(value),'</DOCUMENTS>\n']) for value in self.__documentLst), HEADER_INDENT)

"""
<FILENUMBER>__fileNumber</FILENUMBER>
<FILETYPE>__fileType</FILETYPE>
<FILENAME>__fileName</FILENAME>
<DESCRIPTION>__fileDesc</DESCRIPTION>
<PAGES>__nbPages</PAGES>
<DOCUMENTS>__nbDocuments</DOCUMENTS>
<IMPRESSIONS>__nbImpression</IMPRESSIONS>
<PHYSICAL_PAGES>__nbPhysicalPages</PHYSICAL_PAGES>
<CHANNEL_PRIMARY>__channelPrimary</CHANNEL_PRIMARY>
<INPUTFILELIST>
     __lstInputFile[] -> InputFileReturnProducer.flush()
</INPUTFILELIST>
"""

class FileReturnProducer:
    
    def __init__(self,fileNumber,nbPages,nbDocuments,nbImpression,nbPhysicalPages,fileType = None,fileName = None,fileDescription = None,channelPrimary = None):
        self.__fileNumber = fileNumber
        self.__fileType = fileType
        self.__fileName = fileName
        self.__fileDesc = fileDescription
        self.__channelPrimary = channelPrimary
        self.__nbPages = nbPages
        self.__nbDocuments = nbDocuments
        self.__nbImpression = nbImpression
        self.__nbPhysicalPages = nbPhysicalPages
        self.__lstInputFile = []
    
    def addInputFile(self, jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages):
        self.__lstInputFile.append(InputFileReturnProducer(jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages))

    def append(self,resu,value,string):
        if value!= None:
            resu.append(string )
        
    def flush(self):
        resu =[]
        self.append(resu, self.__fileNumber, '%s<FILENUMBER>%02d</FILENUMBER>\n' % (FILE_DETAIL_INDENT, int(self.__fileNumber)))
        self.append(resu, self.__fileType, '%s<FILETYPE>%s</FILETYPE>\n' % (FILE_DETAIL_INDENT, self.__fileType))
        self.append(resu, self.__fileName, '%s<FILENAME>%s</FILENAME>\n' % (FILE_DETAIL_INDENT, self.__fileName))
        self.append(resu, self.__fileDesc, '%s<DESCRIPTION>%s</DESCRIPTION>\n' % (FILE_DETAIL_INDENT, self.__fileDesc))
        self.append(resu, self.__nbPages, '%s<PAGES>%s</PAGES>\n' % (FILE_DETAIL_INDENT, self.__nbPages))
        self.append(resu, self.__nbDocuments, '%s<DOCUMENTS>%s</DOCUMENTS>\n' % (FILE_DETAIL_INDENT, self.__nbDocuments))
        self.append(resu, self.__nbImpression, '%s<IMPRESSIONS>%s</IMPRESSIONS>\n' % (FILE_DETAIL_INDENT, self.__nbImpression))
        self.append(resu, self.__nbPhysicalPages, '%s<PHYSICAL_PAGES>%s</PHYSICAL_PAGES>\n' % (FILE_DETAIL_INDENT, self.__nbPhysicalPages))
        self.append(resu, self.__channelPrimary, '%s<CHANNEL_PRIMARY>%s</CHANNEL_PRIMARY>\n' % (FILE_DETAIL_INDENT, self.__channelPrimary))
        resu.append("%s<INPUTFILELIST>\n%s%s</INPUTFILELIST>\n" % (FILE_DETAIL_INDENT,''.join((value.flush()) for value in self.__lstInputFile),FILE_DETAIL_INDENT))
        return ''.join(resu)

""" 
<INPUTFILE>
      <JOBID>"input_file_job_id"</JOBID>
      <PAGES>"input_file_pages"</PAGES>
      <DOCUMENTS>"input_file_docs"</DOCUMENTS>
      <IMPRESSIONS>"input_file_imps"</IMPRESSIONS>
      <PHYSICAL_PAGES>"input_file_phys_pages"</PHYSICAL_PAGES>
</INPUTFILE>
"""
class InputFileReturnProducer:
        
    def __init__(self,jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages):
        self.__jobID = jobID
        self.__nbPages = nbPages
        self.__nbDocuments = nbDocuments
        self.__nbImpression = nbImpression
        self.__nbPhysicalPages = nbPhysicalPages

    def flush(self):
        resu =[]
        resu.append('%s<INPUTFILE>\n' % (FILE_INPUT_INDENT))
        resu.append('%s<JOBID>%s</JOBID>\n' % (FILE_DETAIL_INPUT_INDENT, self.__jobID) )
        resu.append('%s<PAGES>%s</PAGES>\n' % (FILE_DETAIL_INPUT_INDENT, self.__nbPages) )
        resu.append('%s<DOCUMENTS>%s</DOCUMENTS>\n' % (FILE_DETAIL_INPUT_INDENT, self.__nbDocuments) )
        resu.append('%s<IMPRESSIONS>%s</IMPRESSIONS>\n' % (FILE_DETAIL_INPUT_INDENT, self.__nbImpression) )
        resu.append('%s<PHYSICAL_PAGES>%s</PHYSICAL_PAGES>\n' % (FILE_DETAIL_INPUT_INDENT, self.__nbPhysicalPages) )
        resu.append('%s</INPUTFILE>\n' % (FILE_INPUT_INDENT))
        return ''.join(resu)

"""
write(RET_file,"<OUTPUTFILELIST>\n")
write(RET_file,"      <FILE>\n")
write(RET_file,"            <FILENUMBER>"opdd_job_print_file"</FILENUMBER>\n")
write(RET_file,"            <PAGES>"tot_pages"</PAGES>\n")
write(RET_file,"            <DOCUMENTS>"tot_docs"</DOCUMENTS>\n")
write(RET_file,"            <IMPRESSIONS>"tot_imps"</IMPRESSIONS>\n")
write(RET_file,"            <PHYSICAL_PAGES>"tot_physical"</PHYSICAL_PAGES>\n")
      write(RET_file,"            <INPUTFILELIST>\n")
            write(RET_file,"                  <INPUTFILE>\n")
            write(RET_file,"                        <JOBID>"input_file_job_id"</JOBID>\n")
            write(RET_file,"                        <PAGES>"input_file_pages"</PAGES>\n")
            write(RET_file,"                        <DOCUMENTS>"input_file_docs"</DOCUMENTS>\n")
            write(RET_file,"                        <IMPRESSIONS>"input_file_imps"</IMPRESSIONS>\n")
            write(RET_file,"                        <PHYSICAL_PAGES>"input_file_phys_pages"</PHYSICAL_PAGES>\n")
            write(RET_file,"                  </INPUTFILE>\n")
      write(RET_file,"            </INPUTFILELIST>\n")
write(RET_file,"      </FILE>\n")
write(RET_file,"</OUTPUTFILELIST>\n")
"""
"""
We assume that the print file is named <Job ID>-O<FileNumber>-0.lis, and that the VPF produced is the same, but not .vpf
e.g. 123456-O01-0.lis and 123456-O01-0.vpf
There is a table called required_file_types though that has the extensions that must exist for each output file - so we do validate this a bit
Looks like this
REQUIRED_FILE_TYPES_INDEX PRINTER_TYPE         MAILER_TYPE          FILE_TYPE_
------------------------- -------------------- -------------------- ----------
                       90                      KMFRRD               ecf
                        1 SCITEX_NFS                                lis
                        3 IBM_IPM                                   lis
                        5 XRX_DPS_FS                                lis
                        7                      DFWORKS              vpf
                       10 XRX_DPS_FS                                ef
                       12 FILE_COPY                                 lis
                        2 SCITEX_NFS                                ndx
                        4 XRX_FA                                    lis
                        6                      DFWORKS              IF0
                        8                      DFWORKS              vpf.ind
                       11 XRX_DPS                                   lis
So if Mailer_type = DFWORKS we expect to see 123456-O01-0.lis, .vpf, .IF0, .vpf.ind
"""

if __name__ == '__main__':
    param = ParameterContainer(sys.argv)
    returnProducer = ReturnProducerUtils(param)
    returnProducer.setHeaderInformation("myDoc")
    fileNumber = '0003'
    jobID = param.getJobID()
    nbPages = 1
    nbDocuments = 1
    nbImpression = 1
    nbPhysicalPages = 1
    fileReturn = FileReturnProducer(fileNumber,nbPages,nbDocuments,nbImpression,nbPhysicalPages)
    fileReturn.addInputFile(jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages)
    returnProducer.addFileReturn(fileReturn)
    print returnProducer.getXml()
    returnProducer.flush()
    sys.argv.append('-JOB')
    sys.argv.append('001001')
    jobID = param.getJobID()
    param = ParameterContainer(sys.argv)
    returnProducer = ReturnProducerUtils(param,True)
    returnProducer.setHeaderInformation(["myDoc1","myDoc2"])
    fileReturn = FileReturnProducer(fileNumber,nbPages,nbDocuments,nbImpression,nbPhysicalPages)
    fileReturn.addInputFile(jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages)
    fileReturn.addInputFile(jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages)
    fileReturn.addInputFile(jobID,nbPages,nbDocuments,nbImpression,nbPhysicalPages)
    returnProducer.addFileReturn(fileReturn)
    returnProducer.addFileReturn(fileReturn)
    print returnProducer.getXml()
    returnProducer.flush()
# print sys.argv
