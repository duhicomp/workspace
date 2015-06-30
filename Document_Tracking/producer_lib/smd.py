#
# Python Java Vm launcher
# in middleoffice / producer development context
#
__revision__ = '$Revision$'
__date__ ='$Date$'

from java import SmdLauncher

_MYJAVA_      = "C:/j2sdk1.4.2_11/bin/java.exe" 
_MYHOMELIBS_  = "f:/sefasbuild/current" 
_MYVMARGS_    = '-Dlog4j.configuration="d:/producer/utils/log4J.properties"'
_MYJDBC_ = ["F:/oracle/ora10/jdbc/lib/classes12.jar"]

#
# module main is just a practical sample test
# of JavaLauncher usage
#
if __name__ == '__main__':
    smd = SmdLauncher( _MYJAVA_ , _MYVMARGS_ , _MYJDBC_ )
    import sys
    smd.execute( _MYHOMELIBS_ , sys.argv ) 
