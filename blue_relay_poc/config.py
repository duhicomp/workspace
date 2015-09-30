import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfigMySQL(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sefas:sefas@farnsworth/sefas'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sefas:sefas@localhost/sefas'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sefas:sefas@10.6.71.1/sefas'
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    DESIGNER_HOME = 'C:\\OpenPrint\\Designer_7_1_2_8'
    MO_CONSOLE = os.path.join(DESIGNER_HOME, '/adf/openprint/designer/')
    JAVA_HOME = 'C:\Program Files (x86)\Java\jdk1.8.0_25' #os.path.join('C:\Program Files (x86)', 'Java', 'jdk1.8.0_25') #
    DESIGNER_HOSTNAME = 'localhost'
    #DESIGNER_HOSTNAME = '10.6.71.1'
    MOPASSOWRD = ''
    MOLOGIN = 'mabdul-aziz'
    LOG_FILE_PATH = 'D:\\MA_Sefas\\Clients\\BlueRelay\\temp\\api.log'
    TEMPLATES_PATH = os.path.join(DESIGNER_HOME, 'home', 'opWD', 'default', 'common', 'template')
    MO_CONSOLE_PORT = 9080
    OPINSTALLDIR = 'C:\\OpenPrint\\Designer_7_1_2_8\\bin\\backstage\\windows'
    OPWD = 'D:\\MA_Sefas\\Clients\\BlueRelay\\Test_Env'
    PROTOCOL = 'http'

class TestingConfig(Config):
    TESTING = True
