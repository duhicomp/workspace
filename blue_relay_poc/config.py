import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite://:memory:'
    API_BASE = '/api/v1.0'
    APP_TYPES = {140: 'Template', 204: 'BKO'}

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfigMySQL(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sefas:sefas@farnsworth/sefas'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sefas:sefas@localhost/sefas'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sefas:sefas@10.6.71.1/sefas'
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    DESIGNER_HOME = r'C:\OpenPrint\Designer'
    MO_CONSOLE = os.path.join(DESIGNER_HOME, '/adf/openprint/designer/')
    #DESIGNER_HOSTNAME = 'localhost'
    DESIGNER_HOSTNAME = '10.6.71.1'
    MOPASSOWRD = ''
    MOLOGIN = 'root'
    LOG_FILE_PATH = r'D:\MA_Sefas\Clients\BlueRelay\temp\blue_api.log'
    TEMPLATES_PATH = os.path.join(DESIGNER_HOME, 'home', 'opWD', 'default', 'common', 'template')
    MO_CONSOLE_PORT = 9080
    OPINSTALLDIR = 'C:\\OpenPrint\\Designer\\bin\\backstage\\windows'
    OPWD = 'D:\\MA_Sefas\\Clients\\BlueRelay\\Test_Env'
    PROTOCOL = 'http'
    SMD_HOST = DESIGNER_HOSTNAME
    SMD_PORT = 29904
    REMOTE_PYTHON_EXE = 'C:\\Python26\\python.exe'
    REMOTE_DL_PARSING_SCRIPT = 'C:\\Users\\Sefas\\PycharmProjects\\PyCharm_Workspace\\blue_relay_poc\\parse_dataloader_id.py'
    REMOTE_DESIGNER_PATH = 'C:\\OpenPrint\\Designer'
    REMOTE_SMD_HOST ='10.6.71.1'
    REMOTE_SMD_PORT = 29900
    REMOTE_DESIGNER = True

class TestingConfig(Config):
    TESTING = True
