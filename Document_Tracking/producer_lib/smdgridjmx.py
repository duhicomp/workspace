#
# Python Grid Jmx launching 
# in middleoffice / producer development context
#
__revision__ = '$Revision$'
__date__ ='$Date$'

from java import SmdGridLauncher

_MYJAVA_         = "C:/jdk1.6.0/bin/java.exe" 

_MYHOMELIBS_     = "f:/sefasbuild/current" 
_SMDJARS_ = [ _MYHOMELIBS_ +'/new/lib/sfsmdlware.jar' , \
              _MYHOMELIBS_ +'/new/lib/grid.jar', \
              _MYHOMELIBS_ +'/new/lib/gridjmx.jar', \
              _MYHOMELIBS_ +'/runimported/log4j/log4j-1.2.15.jar' \
            ] 

# log4J system options follow
_LOG4J_OPTIONS_  = '-Dlog4j.configuration="d:/netbeansprojects/smdsources/log4J.properties"'
# options for jmx standard monitoring follow
_JMX_OPTIONS_    = [ '-Dcom.sun.management.jmxremote.ssl=false' ,
                     '-Dcom.sun.management.jmxremote.authenticate=false' ,
                     '-Dcom.sun.management.jmxremote.port=8004' ,
                     '-Dcom.sun.management.jmxremote'
                   ]
# specify smd home where dlauncher.properties is located                   
_SMD_HOME_ = '-Home d:/netbeansprojects/smdsources' 
# ask smd to load MProcessFactory at startup to resolve grid nodes
_INITIAL_LOAD_ = '-Load com.sefas.gridclient.MProcessFactory' 
# define default encoding
_ENCODING_ = '-Encoding ISO-8859-1'
_SMD_ARGS_ = [ _SMD_HOME_ , _INITIAL_LOAD_ , _ENCODING_ ]
_SMD_VMARGS_    = _JMX_OPTIONS_ + [ _LOG4J_OPTIONS_ ] 


#
# module main is just a practical sample test
# of SmdGridLauncher usage
#
if __name__ == '__main__':
    smd = SmdGridLauncher( _MYJAVA_ , ' '.join(_SMD_VMARGS_)   )
    smd.execute( _MYHOMELIBS_ , _SMD_ARGS_ , _SMDJARS_) 
