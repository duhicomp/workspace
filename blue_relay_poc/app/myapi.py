#from __future__ import unicode_literals

import os

from flask import Flask, request, jsonify, session, abort, url_for, current_app
from flask.ext.restful import Api, Resource

from app import api
from app import db

import subprocess
# TODO: Error reproting and error handling

def execute_moconsole_cmd(java_cmd):
    """
    Utility function to exeute the moconsol command in a separate process using the subprocess module.
    """
    mologin = current_app.config['MOLOGIN']
    mopassword = current_app.config['MOPASSOWRD']
    cmd = java_cmd
    cmd += ' ' + mologin
    cmd += ' "' + mopassword + '"'

    print str(cmd)
    ret_code = 0
    stdout_fd= open(os.path.join(current_app.config['LOG_PATH'],'stdout.txt'), 'a')
    stderr_fd= open(os.path.join(current_app.config['LOG_PATH'],'stderr.txt'), 'a')
    ret_code = subprocess.call(cmd, stdout=stdout_fd, stderr=stderr_fd)
    stdout_fd.close()
    stderr_fd.close()
    # TODO: Check return code, and handle error, How? you ask?
    return


def get_dataloader(tempaltes_path, app_id):
        """
        Utility function to return the dataloader associated with an application.
        it returns remake for BKO application and the dataloader name (from the Template xml file) for Middle Office
        (Composition)Template
        """
        print 'in get_dataloader'
        found = False
        dataloader_name = ''
        dataloder_id = ''
        template_xml_fd = open(os.path.join(tempaltes_path, app_id + '.xml'))
        print os.path.join(tempaltes_path, app_id + '.xml')
        for xml_line in template_xml_fd:
            if 'repository:DataManager' in xml_line:
                xml_line_lst = xml_line.split(' ')
                for xml_line_elem in xml_line_lst:
                    if str(str(xml_line_elem).split('=')[0]).strip('"') == 'name':
                        dataloader_name = str(str(xml_line_elem).split('=')[1]).strip('"')
                    if str(str(xml_line_elem).split('=')[0]).strip('"') == 'resdescid':
                        print ( 'Dataloader Resource ID:' + str(xml_line_elem).split('=')[1] )
                        for id_char in str(str(xml_line_elem).split('=')[1]).strip('"'):
                            if id_char.isdigit():
                                dataloder_id += id_char
                found = True
        if not found :
            # TODO: Manage error here
            print 'A Warning here ill be in order'
        print 'dataloader_name:' + dataloader_name
        print 'dataloader_id:' + dataloder_id
        return dataloader_name, dataloder_id
        pass


def tag_exists(app_name,app_id):
    result = db.session.execute('select ID from TAG where USER_NAME = "' + str(app_name) + '_' + str(app_id) + '"')
    # row = result.first()
    # if not row:
    #     return False
    # else:
    #     return True
    tags_lst = []

    for row in result:
        dict_row={}
        dict_row['ID'] = row['ID']
        print(str(dict_row))
        tags_lst.append( url_for('tag', tag_name = str(app_name) + '_' + str(app_id)) )
    return tags_lst

def delete_tag(tag_name,tag_id, version_id):
    hostname = current_app.config['DESIGNER_HOSTNAME']
    mo_consol_port = current_app.config['MO_CONSOLE_PORT']
    mo_hostname = hostname + ':' + str(mo_consol_port)

    # TODO: Check if tag is deploy to an environment
    # Check if Tag is deployed in an environment
    result = db.session.execute('select ENVIRONNEMENT_PARENT from environnement_tag_lnk where TAG_CHILD = ' + str(tag_id))
    if result.rowcount != 0:
        print('in ENV PARENT ')
        row = result.first()
        env_parent_id = row['ENVIRONNEMENT_PARENT']
        print('env_parent_id = ' + str(env_parent_id))
        result = db.session.execute('select NAME from ENVIRONNEMENT where ID= "' + str(env_parent_id) + '"')
        if result.rowcount != 0:
            # implement a loop
            row = result.first()
            env_name = row['NAME']
            hostname = current_app.config['DESIGNER_HOSTNAME']

            ###### REMOVE CODE FROM ENV FIRST #####
            java_cmd = ''
            java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
            java_cmd += ' -Xms64m'
            java_cmd += ' -Xmx256m'
            java_cmd += ' -DcryptedPassword=true'
            #TODO: Tag is in remote env
            java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt'
            java_cmd += ' RemoveTagFromEnv'
            java_cmd += ' http'
            java_cmd += ' ' + mo_hostname
            java_cmd += " " + env_name
            java_cmd += ' "' + tag_name + '" '
            java_cmd += '"' + str(version_id)+ '" '

            execute_moconsole_cmd(java_cmd)

    # ###### THEN REMOVE TAG ###
    # "%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt RemoveTag %protocol% %serverName% "%tagUserName%"  "%tagVersion%" %MOlogin% "%MOpassword%"
    java_cmd = ''
    java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
    java_cmd += ' -Xms64m'
    java_cmd += ' -Xmx256m'
    java_cmd += ' -DcryptedPassword=true'
    java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt'
    java_cmd += ' RemoveTag'
    java_cmd += ' http'
    java_cmd += ' ' +mo_hostname
    java_cmd += ' "' + tag_name + '" '
    java_cmd += '"' + str(version_id)+ '" '

    execute_moconsole_cmd(java_cmd)
    return

class Echo(Resource):
    """
    Resource for testing
    """
    def post(self):
        return request.data


class CreateEnv(Resource):
    # def get(self, env_name, env_type):
    def get(self):
        env_name = request.args.get('env_name')
        env_type = 'ENV_TEST'
        env_opwd = request.args.get('env_opwd')
        print('env_name : ' + env_name )
        print('env_opwd: ' + env_opwd)
        if not os.path.exists(env_opwd):
            os.makedirs(env_opwd)
        # First check env_name does not exist
        result = db.session.execute('select * from ENVIRONNEMENT where NAME="' + env_name + '"')

        if result.rowcount == 0:
            hostname = current_app.config['DESIGNER_HOSTNAME']
            mo_consol_port = current_app.config['MO_CONSOLE_PORT']
            opInstallDir = current_app.config['OPINSTALLDIR']
            opWD = current_app.config['OPWD']
            mo_hostname = hostname + ':' + str(mo_consol_port)
            # "%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt CreateEnvironment %protocol% %serverName% "%EnvironmentName%" "%Description%" "%ProductionEngine%" "%EnvironmentType%" "%opWD%" "%StandAlone%" %MOlogin% "%MOpassword%"
            java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
            java_cmd += ' -Xms64m'
            java_cmd += ' -Xmx256m'
            java_cmd += ' -DcryptedPassword=true'
            java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt'
            java_cmd += ' CreateEnvironment'
            java_cmd += ' http '
            # TODO: To deploy the code to an enviornment other than local host
            java_cmd += mo_hostname
            java_cmd += ' "' + env_name + '"'
            # Description
            java_cmd += ' " The API created environement ' + env_name + '"'
            java_cmd += ' "' + opInstallDir + '"'
            #env_type = ENV_TEST or ENV_PRODUCTION
            java_cmd += ' "' + env_type + '"'
            java_cmd += ' "' + env_opwd + '"'
            java_cmd += ' "true"'

            execute_moconsole_cmd(java_cmd)

            #logic to return enviornment link

            #/api/v1.0/environments/62
        result_b = db.engine.execute('select * from ENVIRONNEMENT where NAME="' + env_name + '"')
        row = result_b.first()
        env_id = row['ID']
        print('env_id =' + str(env_id))
        return url_for('enviornment', env_id = env_id)


class Environments(Resource):
    """
    Resource for Production Environments
    """
    def get(self):
        env_list = []
        result = db.session.execute('select ID from ENVIRONNEMENT where STANDALONE = 0 or STANDALONE = 1')
        for row in result:
            dict_row={}
            dict_row['ID'] = row['ID']
            # dict_row['NAME'] = row['NAME']
            print(str(dict_row))
            # env_list.append( {'Enviornment Name:' : dict_row['NAME'] , 'URL' : url_for('enviornment', env_id=dict_row['ID'])} )
            env_list.append(url_for('enviornment', env_id=dict_row['ID']))
        return jsonify({'environments':env_list})


class Enviornment(Resource):
    def get(self, env_id):
        tags_lst = []
        env_results = db.session.execute('select NAME, TYPE, OPWD from ENVIRONNEMENT where ID=' + str(env_id))
        env_row = env_results.first()
        env_name = env_row['NAME']
        env_type = env_row['TYPE']
        env_path = env_row['OPWD']
        result = db.session.execute('select STATUS,TAG_CHILD from ENVIRONNEMENT_TAG_LNK where ENVIRONNEMENT_PARENT = ' + str(env_id))
        for row in result:
            print('TAG_ID = ' + str(row['TAG_CHILD']))
            tag_result = db.session.execute('select USER_NAME, VERSION from TAG where ID = ' + str(row['TAG_CHILD']))
            #for row_t in tag_result:
            row_t =tag_result.first()
            #dict_row={}
            #dict_row['USER_NAME'] = row_t['USER_NAME']
            tags_lst.append(url_for('tag_version', tag_name = row_t['USER_NAME'], version_id =  row_t['VERSION']))
            # tags_lst.append(url_for('tag', tag_name=row_t['USER_NAME']))
        print(str(tags_lst))
        return jsonify({'tags': tags_lst,'NAME':env_name, 'TYPE':env_type, 'PATH':env_path})


class Tags(Resource):
    """
    Resource for getting list of tag resource URLs
    """
    def get(self):
        result = db.session.execute('select distinct USER_NAME from TAG where NAME = "User"')
        print result
        print dir(result)
        print result.keys()
        tags_list = []
        for row in result:
            dict_row={}
            dict_row['USER_NAME'] = row['USER_NAME']
            tags_list.append(url_for('tag', tag_name=dict_row['USER_NAME']))
        print 'testing'
        return jsonify({'tags': tags_list}
        )


class Tag(Resource):
    def get(self, tag_name):
        print("in Tag class, tag_name=" + tag_name)
        result = db.session.execute('select VERSION from TAG where NAME = "User" and USER_NAME = :tag_name', {'tag_name': tag_name})
        if result.rowcount == 0:
            abort(404)
        tag_versions_url_lst = []
        for row in result:
            dict_row = dict([(x, row[x]) for x in result.keys()])
            print str(dict_row)
            tag_versions_url_lst.append(url_for('tag_version', tag_name = tag_name , version_id =  dict_row['VERSION']) )
        actions = {}
        actions['delete tag'] = url_for('tag_delete',tag_name=tag_name)
        print str(tag_versions_url_lst)
        return jsonify({'tag_versions': tag_versions_url_lst, 'actions': actions })


class TagDeploy(Resource):
    def get(self, tagname, version_id):
        env_id = request.args.get('env_id')
        # implementes logic described in transfertTag.bat
        hostname = current_app.config['DESIGNER_HOSTNAME']
        mo_consol_port = current_app.config['MO_CONSOLE_PORT']
        mo_hostname = hostname + ':' + str(mo_consol_port)
        result = db.session.execute('select distinct NAME from environnement where ID = :env_id', {'env_id': env_id})
        if result.rowcount == 0:
            abort(404)
        row = result.first()
        env_name = row['NAME']
        #CMD
        #"%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt TransfertTag %protocol% %serverName% "%TagName%" "%TagVersion%" "%EnvironmentName%" "%WithCompil%" "%GenerateProjectorTree%" %MOlogin% "%MOpassword%"
        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt'
        java_cmd += ' TransfertTag'
        java_cmd += ' http '
        # TODO: To deploy the code to an enviornment other than local host
        java_cmd += mo_hostname
        java_cmd += ' "' + tagname + '"'
        java_cmd += ' "' + str(version_id) + '"'
        java_cmd += ' "' + env_name + '"'
        #"%WithCompil%"
        java_cmd += ' "1"'
        # "%GenerateProjectorTree%"
        # TODO: Do we really need to GenerateProjectorTree? it is enabled for now per transfertTag.bat
        java_cmd += ' "1"'

        execute_moconsole_cmd(java_cmd)

        return url_for('enviornment', env_id=env_id)


class TagNewVersion(Resource):
    def get(self,tag_name, version_id):
        hostname = current_app.config['DESIGNER_HOSTNAME']
        mo_consol_port = current_app.config['MO_CONSOLE_PORT']
        mo_hostname = hostname + ':' + str(mo_consol_port)

        result = db.session.execute('select ID from TAG where USER_NAME = :tag_name and VERSION = :version_id', {'tag_name': tag_name, 'version_id':version_id})
        if result.rowcount == 0:
            abort(404)
        row = result.first()
        print("Content of row for tag_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row ['ID']

        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt'
        java_cmd += ' TagNewVersion'
        java_cmd += ' ' + mo_hostname
        java_cmd += ' http'
        java_cmd += ' "' + str(tag_id) + '"'
        #java_cmd += ' "' + tag_name + '"'
        java_cmd += ' " "'

        execute_moconsole_cmd(java_cmd)

        #potential bug here, when we have version 1.1 and 1.2, and then we create version from 1.1, we should end up with 1.2, but the created tag will be 1.3
        result_max = db.session.execute('select max(VERSION) from TAG where USER_NAME ="' + tag_name + '"')
        if result_max.rowcount == 0:
            print("No result_max returned?")
            abort(404)

        row_max = result_max.first()
        print(row_max[0])

        max_version=row_max[0]

        print('Max version of the tag:' + tag_name + 'is version:' + str(max_version) )
        major_version = int(str(max_version).split('.')[0])
        minor_version = int(str(max_version).split('.')[1])
        return url_for('tag_version', tag_name = tag_name , version_id = str(major_version) + '.' + str(minor_version+1) )


class TagUpdate(Resource):
    """
    Class responsible for updating tag resources

    Used to update
    * dataloader
    * application
    * etc
    """
    def get(self,tag_name, version_id):
        print('Tag name = ' + tag_name)
        hostname = current_app.config['DESIGNER_HOSTNAME']
        mo_consol_port = current_app.config['MO_CONSOLE_PORT']
        mo_hostname = hostname + ':' + str(mo_consol_port)
        app_name = tag_name[:-4]
        print('Application name = ' + app_name )
        result = db.session.execute('select ID from TAG where USER_NAME = :tag_name and VERSION = :version_id', {'tag_name': tag_name, 'version_id':version_id})
        if result.rowcount == 0:
            abort(404)
        row = result.first()
        print("Content of row for tag_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row ['ID']

        result = db.engine.execute('select distinct ID,RESTYP_PARENT from RES_DESC where NAME ="' + app_name + '"')
        if result.rowcount == 0:
            abort(404)
        row = result.first()
        print("Content of row for app_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        app_id = dict_row ['ID']
        app_type = dict_row ['RESTYP_PARENT']
        # updateTagManageResources.bat, to update the dataloader
        # "%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt %action% %serverName% %protocol% "%tagIdList%" "%tagNameOrOpAppliList%" "%resIdList%" "%MOlogin%" "%MOpassword%"
        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt UpdateTagElements '
        java_cmd += mo_hostname
        java_cmd += ' http'
        java_cmd += ' "' + str(tag_id) + '"'
        java_cmd += ' "' + tag_name + '"'
        java_cmd += ' "DATALOADERS"'

        execute_moconsole_cmd(java_cmd)

        #to update the tage, first remove the primary resource (applicaton), then add it back in
        #remove application from tag
        #"%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt %action% %serverName% %protocol% "%tagIdList%" "%tagNameOrOpAppliList%" "%resIdList%" "%MOlogin%" "%MOpassword%"
        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt RemoveResourcesInTag '
        java_cmd +=  mo_hostname
        java_cmd += ' http'
        java_cmd += ' "' + str(tag_id) + '"'
        java_cmd += ' "' + tag_name + '"'
        java_cmd += ' "' + str(app_id) + '"'

        execute_moconsole_cmd(java_cmd)

        #Insert applicaiton into the tag
        #"%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt CreateNewTag %serverName% %protocol% "%TagName%" "%TagDescription%" "%DataLoaderNameID%" "%MOlogin%" "%MOpassword%"
        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt AddResourcesInTag '
        java_cmd += mo_hostname
        java_cmd += ' http'
        java_cmd += ' "' + str(tag_id) + '"'
        java_cmd += ' "' + tag_name + '"'
        java_cmd += ' "' + str(app_id) + '"'

        execute_moconsole_cmd(java_cmd)

        return url_for('tag_version', tag_name=tag_name, version_id=version_id)


class TagVersion(Resource):
    def get(self,tag_name, version_id):
        print('Tag name =' + tag_name)
        print('Tag version =' + version_id)
        result = db.session.execute('select * from TAG where NAME = "User" and USER_NAME = :tag_name and VERSION = :version_id ', {'tag_name': tag_name, 'version_id': version_id})
        if result.rowcount == 0:
            abort(404)
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])
        print str(dict_row)
        tag_object = {}
        tag_object['tag_name'] = dict_row['USER_NAME']
        # Actions are per tag version
        actions = {}
        # Update tag
        actions['update_tag']= url_for('tag_update', tag_name=tag_name, version_id=version_id)
        # create new version
        actions['new_version']= url_for('tag_new_version', tag_name=tag_name, version_id=version_id)
        # Delete tag
        actions['delete_tag']= url_for('tag_version_delete', tag_name=tag_name, version_id=version_id)
        tag_object['actions'] = actions
        return jsonify(tag_object)


class TagDelete(Resource):
    def get(self, tag_name):
        print('here I am ')
        results = db.session.execute('select ID,VERSION from TAG where USER_NAME ="' + tag_name + '"')
        if results.rowcount == 0:
            abort(404)
        for row in results:
            dict_row = dict([(x, row[x]) for x in results.keys()])
            print str(dict_row)
            tag_version = dict_row['VERSION']
            tag_id = dict_row['ID']
            delete_tag(tag_name, tag_id, tag_version)
            print('here I am back from delete_tag')

        return {}


class TagDeleteVersion(Resource):
    def get(self, tag_name, version_id):
        result = db.session.execute('select ID from TAG where USER_NAME = :tag_name and VERSION = :version_id', {'tag_name': tag_name, 'version_id':version_id})
        if result.rowcount == 0:
            abort(404)
        row = result.first()
        print("Content of row for tag_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row ['ID']
        delete_tag(tag_name,tag_id, version_id)
        return {}


class Applications(Resource):
    def __init__(self):
        self.desinger_path = current_app.config['DESIGNER_HOME']

    def get(self):
        app_list=[]
        results = db.session.execute('select ID from RES_DESC where RESTYP_PARENT = 140 OR RESTYP_PARENT = 204')
        for row_apps in results:
            dict_row = dict()
            dict_row ['ID'] = row_apps['ID']
            app_list.append(url_for('application', app_id=dict_row['ID']))
        print "apps:" + str(app_list)
        return jsonify({'apps': app_list})


class AppCreateTag(Resource):
    def get(self):
        app_id = request.args.get("app_id")
        hostname = current_app.config['DESIGNER_HOSTNAME']
        mo_consol_port = current_app.config['MO_CONSOLE_PORT']
        mo_hostname = hostname + ':' + str(mo_consol_port)

        print('app_id = ' + str(app_id))
        result = db.session.execute('select RESTYP_PARENT from RES_DESC where ID = "' + str(app_id) + '"')
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])
        print('dict_row =' + str(dict_row ))
        print ("RESTYP_PARENT = " + str(dict_row['RESTYP_PARENT']) )
        if dict_row['RESTYP_PARENT'] == 204: #BKO
            dataloader_name = 'remake'
            id_result = db.session.execute('select distinct ID from RES_DESC where RESTYP_PARENT = ' + '147 and NAME = "remake"' )
            id_row = id_result.first()
            dataloader_id = id_row ['ID']
        elif dict_row['RESTYP_PARENT'] == 140: #TEMPLATE
            template_paths = current_app.config['TEMPLATES_PATH']
            dataloader_name, dataloader_id = get_dataloader(template_paths, str(app_id))

        result = db.session.execute('select NAME from RES_DESC where ID = '  + str(app_id))
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])
        application_name = dict_row ['NAME']
        tag_name = application_name  + '_' + str(app_id) # TODO: replace _TAG with _res_id

        #"%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt CreateNewTag %serverName% %protocol% "%TagName%" "%TagDescription%" "%DataLoaderNameID%" "%MOlogin%" "%MOpassword%"
        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt CreateNewTag '
        java_cmd += mo_hostname
        java_cmd += ' http'
        java_cmd += ' "' + tag_name + '"'
        java_cmd += ' "The Application ' + application_name  + ' Tag"'
        java_cmd += ' ' + dataloader_name + ':' +  str(dataloader_id)

        execute_moconsole_cmd(java_cmd)

        #updateTagManageResources
        #"%JAVA_HOME%\bin\java" -Xms64m -Xmx256m -DcryptedPassword=%cryptedPassword% -classpath "%class%" com.sefas.service.integration.moconsole.MoConsoleClt %action% %serverName% %protocol% "%tagIdList%" "%tagNameOrOpAppliList%" "%resIdList%" "%MOlogin%" "%MOpassword%"
        print('Executing SQL Statement: select ID from TAG where USER_NAME = "' + tag_name + '"')
        # TODO: Figure out why db.session.execute doesn't work below, but db.engine.execute does? What is the difference
        #result = db.session.execute('select ID from TAG where USER_NAME = "' + tag_name + '"')
        result = db.engine.execute('select ID from TAG where USER_NAME = "' + tag_name + '"')
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row['ID']

        java_cmd = '"' + os.path.join(current_app.config['JAVA_HOME'], 'bin', 'java') + '"'
        java_cmd += ' -Xms64m'
        java_cmd += ' -Xmx256m'
        java_cmd += ' -DcryptedPassword=true'
        java_cmd += ' -classpath "' + os.path.join(current_app.config['DESIGNER_HOME'], 'home', 'html', 'MiddleOffice', 'applet','swasdksrv.jar') + '" com.sefas.service.integration.moconsole.MoConsoleClt AddResourcesInTag '
        java_cmd += hostname + ':' + str(mo_consol_port)
        java_cmd += ' http'
        java_cmd += ' "' + str(tag_id) + '"'
        java_cmd += ' "' + tag_name + '"'
        java_cmd += ' "' + str(app_id) + '"'

        execute_moconsole_cmd(java_cmd)

        return url_for('tag', tag_name=tag_name )


class Application(Resource):
    def __init__(self):
        self.APP_TYPES = {140:'Template', 204:'BKO', 147:'Dataloader'}

    def get(self,app_id):
        results = db.session.execute('select RESTYP_PARENT,NAME from RES_DESC where ID = "' + str(app_id) + '"')
        for row_apps in results:
            dict_row = dict()
            dict_row ['ID'] = str(app_id)
            dict_row ['APP_TYPE'] = self.APP_TYPES[row_apps['RESTYP_PARENT']]
            dict_row ['NAME'] = row_apps['NAME']
            template_paths = current_app.config['TEMPLATES_PATH']
            print("template_paths" + template_paths)
            if dict_row ['APP_TYPE'] == 'BKO':
                dict_row ['DATALOADER_NAME'] = 'remake'
                id_result = db.session.execute('select distinct ID from RES_DESC where RESTYP_PARENT = ' + '147 and NAME = "remake"' )
                id_row = id_result.first()
                dict_row ['DATALOADER_ID'] = id_row ['ID']
            elif dict_row ['APP_TYPE'] == 'Template':
                dict_row ['DATALOADER_NAME'], dict_row ['DATALOADER_ID'] = get_dataloader(template_paths, str(dict_row['ID']))
            actions = {}
            #if not tag_exists(dict_row ['NAME']):
            tags_url = tag_exists(dict_row ['NAME'],app_id)
            if not tags_url:
                actions['create_tag']= url_for('app_tag_create', app_id=dict_row ['ID'])
                dict_row ['ACTIONS'] = actions
            else:
                dict_row ['TAG'] = tags_url
        print "apps_dict:" + str(dict_row)
        return jsonify(dict_row)


api_base_url = "/api/v1.0"
api.add_resource(Echo, '/'.join([api_base_url, 'echo']), endpoint='echo')
api.add_resource(Environments, '/'.join([api_base_url, 'environments']), endpoint='environments')
api.add_resource(Enviornment, '/'.join([api_base_url, 'environments/<int:env_id>']), endpoint='enviornment')
api.add_resource(CreateEnv, '/'.join([api_base_url, 'environments/create']), endpoint='enviornments_create')
api.add_resource(Tags, '/'.join([api_base_url, 'tags']), endpoint='tags')
api.add_resource(Tag, '/'.join([api_base_url, 'tags/<tag_name>']), endpoint='tag')
api.add_resource(TagDelete, '/'.join([api_base_url, 'tags/<tag_name>/delete']), endpoint='tag_delete')
api.add_resource(TagDeleteVersion, '/'.join([api_base_url, 'tags/<tag_name>/versions/<version_id>/delete']), endpoint='tag_version_delete')
api.add_resource(TagNewVersion, '/'.join([api_base_url, 'tags/<tag_name>/versions/<version_id>/new_version']), endpoint='tag_new_version')
api.add_resource(TagVersion, '/'.join([api_base_url, 'tags/<tag_name>/versions/<version_id>']), endpoint='tag_version')
api.add_resource(TagDeploy, '/'.join([api_base_url, 'tags/<tagname>/versions/<version_id>/deploy']), endpoint='tag_deploy')
api.add_resource(TagUpdate, '/'.join([api_base_url, 'tags/<tag_name>/versions/<version_id>/update']), endpoint='tag_update')
api.add_resource(Applications, '/'.join([api_base_url, 'applications']), endpoint='applications')
api.add_resource(Application, '/'.join([api_base_url, 'applications/<int:app_id>']), endpoint='application')
api.add_resource(AppCreateTag, '/'.join([api_base_url, 'tags/create']), endpoint='app_tag_create')


