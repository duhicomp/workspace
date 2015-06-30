#
# Python Java Vm launcher
# in middleoffice / producer development context
#
__revision__ = '$Revision$'
__date__ ='$Date$'

class JavaLauncher :
    """ 
      launch the java interpretor and misc usefull Java dbtools 
      from a python shell
    """

    def __init__( self , javaloc , vmArgs ) :
        self._javaloc = javaloc 
        self.vmArgs   = vmArgs

    def execute ( self , className , jars , args ) :
        """ start given class execution """
        classep = ':'
        import sys
        if sys.platform[0:3] == 'win' :
            classep = ';' 
        javaArgs = [ self.vmArgs , '-cp' , classep.join(jars) , className , ' '.join(args) ] 
        print '%s %s' % ( self._javaloc , ' '.join(javaArgs) ) 
        import os 
        os.spawnv( os.P_WAIT , self._javaloc , javaArgs )


class SmdLauncher ( JavaLauncher )  :
    """ SMD launching """
     
    def __init__( self , javaloc , vmargs ,  jdbcjars ) :
        JavaLauncher.__init__( self , javaloc , vmargs )  
        if jdbcjars == None :
            self._jdbcjars = []
        else :
            self._jdbcjars = jdbcjars

    def execute ( self , homelib , args ) :
        """ proceed with smd launching """
        smdjars = [ homelib +'/new/lib/sfsmdlware.jar' , \
                    homelib +'/new/lib/grid.jar', \
                    homelib +'/runimported/log4j/log4j-1.2.15.jar' \
                  ] 
        smdjars.extend( self._jdbcjars )
        JavaLauncher.execute( self , \
                              "com.sefas.gridclient.MarshallerDaemon" , \
                              smdjars , \
                              args )

class SmdGridLauncher ( JavaLauncher )  :
    """ SMD GRID launching REQUEST JRE 1.5 at least for Jmx support """
     
    def __init__( self , javaloc , vmargs ) :
        JavaLauncher.__init__( self , javaloc , vmargs )  

    def execute ( self , homelib , args , smdjars) :
        """ proceed with smd launching """
        JavaLauncher.execute( self , \
                              "com.sefas.jmx.smd.JmxMarshallerDaemon" , \
                              smdjars , \
                              args )

class DbXmlExport ( JavaLauncher ) :
    """ export Producer db in XML mode using MO tools """
    pass


class DbXmlImport ( JavaLauncher ) :
    """ export Producer db in XML mode using MO tools """
    pass

#
# module main is just a practical sample test
# of JavaLauncher usage
#
if __name__ == '__main__':
    pass
