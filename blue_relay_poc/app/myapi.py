#from __future__ import unicode_literals

import os
import requests

from flask import Flask, request, jsonify, session, abort, url_for, current_app
from flask.ext.restful import Api, Resource

from app import api
from app import db
from app import app
from app import db_tables

from smd import osCommandClient as occ

# TODO: Error reporting and error handling
# TODO: Add archive repository action
# TODO: add encrypted password logic?
# TODO: Authenticate api user

with app.app_context():
    APP_TYPES = current_app.config['APP_TYPES']


def call_http(html_name, param_dict):
    hostname = current_app.config['DESIGNER_HOSTNAME']
    mo_console_port = current_app.config['MO_CONSOLE_PORT']
    mo_server = hostname + ':' + str(mo_console_port)

    protocol = current_app.config['PROTOCOL']

    req_url = protocol + '://'
    req_url += mo_server
    req_url += '/servlet/designer'

    param_dict['name'] = current_app.config['MOLOGIN']
    param_dict['passwd'] = current_app.config['MOPASSOWRD']
    param_dict['htmlsource']= protocol + '://' + mo_server + '/openprint/middleoffice/dynhtml/MiddleOffice/moc' + html_name + '.html'

    try:
        r = requests.get(url=req_url,params=param_dict)
        current_app.logger.info('sending request to url:{}'.format(r.url))
        current_app.logger.info(r.text)
    except:
        current_app.logger.error('The request made to the url:' + req_url + ' with the parameters:' + str(param_dict) + ' failed')


def query_db(sql_statement):
    current_app.logger.info('Executing the SQL statement:' + sql_statement)
    try:
        result = db.session.execute(sql_statement)
    except:
        current_app.logger.error('SQL Execution error !' )

    return result


def get_dataloader(templates_path, app_id):
        """
        Utility function to return the dataloader associated with an application.
        it returns remake for BKO application and the dataloader name (from the Template xml file) for Middle Office
        (Composition)Template
        """
        current_app.logger.debug('in get_dataloader')
        found = False
        dataloader_name = ''
        dataloder_id = ''
        template_xml_fd = open(os.path.join(templates_path))
        # TODO: Check if .xml file exists, raise an error if it does not
        current_app.logger.debug(templates_path)
        for xml_line in template_xml_fd:
            if 'repository:DataManager' in xml_line:
                xml_line_lst = xml_line.split(' ')
                for xml_line_elem in xml_line_lst:
                    if str(str(xml_line_elem).split('=')[0]).strip('"') == 'name':
                        dataloader_name = str(str(xml_line_elem).split('=')[1]).strip('"')
                    if str(str(xml_line_elem).split('=')[0]).strip('"') == 'resdescid':
                        current_app.logger.debug('Dataloader Resource ID:' + str(xml_line_elem).split('=')[1] )
                        for id_char in str(str(xml_line_elem).split('=')[1]).strip('"'):
                            if id_char.isdigit():
                                dataloder_id += id_char
                found = True
        if not found :
            current_app.logger.error('Unable to determine the dataloader from the Template .xml file:' + template_xml_fd)

        current_app.logger.info('dataloader_name:' + dataloader_name)
        current_app.logger.info('dataloader_id:' + dataloder_id)

        return dataloader_name, dataloder_id


def get_dataloader_remote(app_id):
    # remote_python_home = 'C:\\Python26'
    remote_python_home = current_app.config['REMOTE_PYTHON_EXE']
    remote_script_name = current_app.config['REMOTE_DL_PARSING_SCRIPT']
    remote_opwd_path = current_app.config['REMOTE_DESIGNER_PATH']
    smd_host = current_app.config['REMOTE_SMD_HOST']
    smd_port = current_app.config['REMOTE_SMD_PORT']

    myclient = occ.OsCommandClient("UTF-8", smd_host, smd_port)
    myclient.connect()

    command_line = ' '.join([os.path.join(remote_python_home, 'python'),remote_script_name, remote_opwd_path, str(app_id),])
    print(command_line)
    exit_code = myclient.command(command_line)
    print(myclient.getStdOut())
    print(myclient.getStdErr())
    print('myclient exit code:' + str(exit_code))

    myclient.disconnect()
    return(exit_code)

def tag_exists(app_name, app_id):
    result = query_db('select ID from TAG where USER_NAME = "' + str(app_name) + '_' + str(app_id) + '"')

    tags_lst = []

    for row in result:
        dict_row={}
        dict_row['ID'] = row['ID']
        tags_lst.append(url_for('tag', tag_name = str(app_name) + '_' + str(app_id)) )

    return tags_lst


def delete_tag(tag_name,tag_id, version_id):
    '''
    Utility function to delete a version of the tag, called recursivly to delete a tag and its versions
    :param tag_name: tag name to be deleted
    :param tag_id: the resource id of the tag
    :param version_id: the version of the tag
    :return:
    '''
    result = query_db('select ENVIRONNEMENT_PARENT from environnement_tag_lnk where TAG_CHILD = ' + str(tag_id))
    if result.rowcount != 0:
        current_app.logger.debug('in ENV PARENT ')
        row = result.first()
        env_parent_id = row['ENVIRONNEMENT_PARENT']
        current_app.logger.debug('env_parent_id = ' + str(env_parent_id))

        result = query_db('select NAME from ENVIRONNEMENT where ID= "' + str(env_parent_id) + '"')
        if result.rowcount != 0:
            row = result.first()
            env_name = row['NAME']
            # Remove tag from env
            param_dict = {}
            param_dict['action'] = 'RemoveTagFromEnv'
            html_name = 'RemoveTagFromEnv'
            param_dict['envName'] = env_name
            param_dict['userTagName'] = tag_name
            param_dict['version'] = version_id
            param_dict['user'] = '' #user?
            param_dict['password'] = '' #user?
            param_dict['loginpassthrough'] = 'true'

            call_http(html_name, param_dict)

    # Then remove tag
    param_dict = {}
    html_name = 'RemoveTag'
    param_dict['userTagName'] = tag_name
    param_dict['version'] = str(version_id)
    param_dict['loginpassthrough'] = 'true'

    call_http(html_name , param_dict)

    # TODO: Return message, environment or tags
    return {}


###
# BEGIN API
###

class Echo(Resource):
    """
    Resource for testing
    """
    def post(self):
        return request.data


class Applications(Resource):
    def get(self):
        app_list = []
        # results = query_db('select ID from RES_DESC where RESTYP_PARENT = 140 OR RESTYP_PARENT = 204')
        select_statement = db_tables.ResDesc.select(db_tables.ResDesc.columns.ID)\
                    .where((db_tables.ResDesc.columns.RESTYP_PARENT == 140) |
                           (db_tables.ResDesc.columns.RESTYP_PARENT == 204))
        print select_statement
        results = db.session.execute(select_statement)
        for row_apps in results:
            dict_row = dict()
            dict_row['ID'] = row_apps['ID']
            app_list.append(url_for('application', app_id=dict_row['ID']))
        current_app.logger.debug("Applications in repository:" + str(app_list))
        return {'apps': app_list}


class Application(Resource):
    def get(self, app_id):
        result = query_db('select RESTYP_PARENT,NAME from RES_DESC where ID ="{0!s}"'.format(app_id))
        if result.rowcount == 0:
            msg = 'unable to locate the application with resource id = {0!s}'.format(app_id)
            current_app.logger.error(msg)
            return jsonify(error='000003', message=msg)

        row_apps = result.first()
        current_app.logger.debug('DB returned: {0!s}'.format(row_apps))
        dict_row = dict()
        current_app.logger.debug('row contents are:' + str(row_apps))
        dict_row['ID'] = str(app_id)
        if row_apps['RESTYP_PARENT'] in APP_TYPES.keys():
            dict_row['type'] = APP_TYPES[row_apps['RESTYP_PARENT']]
        else:
            msg = 'Unsupported resource type (RESTYPE_PARENT)= {0!s}'.format(row_apps['RESTYP_PARENT'])
            current_app.logger.error(msg)
            return jsonify(error='000004', message=msg)

        dict_row['name'] = row_apps['NAME']
        # TODO: can this be made through SMD?

        if dict_row['type'] == 'BKO':
            dict_row['dataloader_name'] = 'remake'
            id_result = query_db('select distinct ID from RES_DESC where RESTYP_PARENT = 147 and NAME = "remake"' )
            id_row = id_result.first()
            dict_row['dataloader_id'] = id_row['ID']
        elif dict_row['type'] == 'Template':
            if current_app.config['REMOTE_DESIGNER']:
                dataloader_id = get_dataloader_remote(str(app_id))
                dict_row ['DATALOADER_ID'] = dataloader_id
                name_result = query_db('select NAME from RES_DESC where ID = "{0!s}"'.format(dataloader_id))
                name_row = name_result.first()
                dict_row ['DATALOADER_NAME'] = name_row['NAME']
            else:
                template_path = current_app.config['TEMPLATES_PATH']
                current_app.logger.debug("template_paths" + template_path)
                template_xml_path = os.path.join(template_path, str(app_id) + '.xml')
                dataloader_name, dataloader_id = get_dataloader(template_xml_path, str(app_id))
                if not os.path.exists(template_xml_path):
                    msg = 'unable to locate the Template xml file: {0}'.format(template_xml_path)
                    current_app.logger.debug(msg)
                    return jsonify(error='000005', message=msg)
                dict_row ['DATALOADER_NAME'], dict_row ['DATALOADER_ID'] = get_dataloader(template_xml_path, str(dict_row['ID']))

        actions = {}

        tags_url = tag_exists(dict_row['name'], app_id)
        if not tags_url:
            actions['create_tag'] = ('POST', url_for('tags', app_id=dict_row['ID']))
            dict_row['actions'] = actions
        else:
            dict_row['tag'] = tags_url

        current_app.logger.debug("apps_dict:" + str(dict_row))
        return dict_row


class Tags(Resource):
    """
    Resource for getting list of tag resource URLs
    """
    def get(self):
        # result = db.session.execute('select distinct USER_NAME from TAG where NAME = "User"')
        result = query_db('select distinct USER_NAME from TAG where NAME = "User"')

        current_app.logger.info(dir(result))
        current_app.logger.info(result.keys())
        tags_list = []
        for row in result:
            tags_list.append(url_for('tag', tag_name=row['USER_NAME']))

        return {'tags': tags_list}

    def post(self):
        app_id = request.args.get("app_id")

        if not app_id:
            current_app.logger.error('No Application ID provided to create the tag')
            return {'error': '000001', 'message':'Application resource ID is needed to create the tag'}

        current_app.logger.info('Creating tag for Application with app_id = {0!s} '.format(app_id))

        result = query_db('select RESTYP_PARENT from RES_DESC where ID = "{0!s}"'.format(app_id))
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])

        current_app.logger.debug('dict_row =' + str(dict_row ))
        current_app.logger.debug("RESTYP_PARENT = " + str(dict_row['RESTYP_PARENT']) )

        if dict_row['RESTYP_PARENT'] == 204: #BKO
            dataloader_name = 'remake'
        elif dict_row['RESTYP_PARENT'] == 140: #TEMPLATE
            template_paths = current_app.config['TEMPLATES_PATH']
            template_xml_path = os.path.join(template_paths, str(app_id) + '.xml')
            if current_app.config['REMOTE_DESIGNER']:
                dataloader_id = get_dataloader_remote(str(app_id))
                name_result = query_db('select NAME from RES_DESC where ID = "{0!s}"'.format(dataloader_id))
                name_row = name_result.first()
                dataloader_name = name_row['NAME']
                print(str(dataloader_id))
            else:
                dataloader_name, dataloader_id = get_dataloader(template_xml_path, str(app_id))
        else:
            return {'error':'000002', 'message':'Unknown resource type: {0!s}'.format(dict_row['RESTYP_PARENT'])}
        # result = db.session.execute('select NAME from RES_DESC where ID = {0!s} '.format(app_id))
        result = query_db('select NAME from RES_DESC where ID = {0!s} '.format(app_id))
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])
        application_name = dict_row ['NAME']
        tag_name = '_'.join([application_name, str(app_id)])

        param_dict = dict()
        param_dict['action'] = 'CreateNewTag'
        html_name = 'TagsProperties'
        param_dict['tagName'] = tag_name
        param_dict['tagDesc'] = 'The Application ' + application_name + ' Tag'
        param_dict['dataloaderNameID'] = dataloader_name
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        # TODO: Figure out why db.session.execute doesn't work below, but db.engine.execute does? What is the difference
        result = db.engine.execute('select ID from TAG where USER_NAME = "' + tag_name + '"')
        #result = query_db('select ID from TAG where USER_NAME = "' + tag_name + '"')
        if result.rowcount == 0:
            msg = 'unable to locate TAG name = {0}'.format(tag_name)
            current_app.logger.error(msg)
            return jsonify(error='000003', message=msg)
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row['ID']

        param_dict = dict()
        param_dict['action'] = 'AddResourcesInTag'
        html_name = 'TagManageResources'
        param_dict['tagIdList'] = str(tag_id)
        param_dict['tagNameOrOpAppliList'] = tag_name
        param_dict['resIdList'] = str(app_id)
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        return {'tag': url_for('tag', tag_name=tag_name)}


class Tag(Resource):
    def get(self, tag_name):
        result = query_db('select VERSION from TAG where NAME = "User" and USER_NAME = "'+ tag_name + '"' )
        if result.rowcount == 0:
            msg = 'Unable to locate the tag named: {0}'.format(tag_name)
            current_app.logger.error(msg)
            return {'error': "Tag '{0}' not found".format(tag_name)}, 404

        tag_versions_url_lst = []
        for row in result:
            dict_row = dict([(x, row[x]) for x in result.keys()])
            current_app.logger.debug(dict_row)
            tag_versions_url_lst.append(url_for('tag_version', tag_name=tag_name , version_id=dict_row['VERSION']))

        actions = dict()
        actions['delete tag'] = url_for('tag_delete',tag_name=tag_name)

        current_app.logger.debug(str(tag_versions_url_lst))
        return {'tag_versions': tag_versions_url_lst, 'actions': actions }

    def delete(self, tag_name):
        results = query_db('select ID,VERSION from TAG where USER_NAME ="{}"'.format(tag_name))

        if results.rowcount == 0:
            msg = 'Unable to locate the TAG name={0!s}'.format(tag_name)
            current_app.logger.debug('Unable to locate the TAG name={0!s}'.format(tag_name))
            return jsonify(error='000013', message=msg)

        for row in results:
            dict_row = dict([(x, row[x]) for x in results.keys()])
            current_app.logger.debug(str(dict_row))
            tag_version = dict_row['VERSION']
            tag_id = dict_row['ID']
            delete_tag(tag_name, tag_id, tag_version)

        return {}


class TagDeploy(Resource):
    def get(self, tagname, version_id):
        env_id = request.args.get('env_id')
        # result = db.session.execute('select distinct NAME from environnement where ID = :env_id', {'env_id': env_id})
        result = query_db('select distinct NAME from environnement where ID = {0!s}'.fomrat(env_id))

        if result.rowcount == 0:
            msg = 'Unable to locate the environment with ID: {0!s}'.format(env_id)
            current_app.logger.error(msg)
            return jsonify(error='000006', message=msg)

        row = result.first()
        env_name = row['NAME']
        # TODO: To deploy the code to an Environment other than local host
        # TODO: Do we really need to GenerateProjectorTree? it is enabled for now per transfertTag.bat

        param_dict = dict()
        param_dict['action'] = 'TransfertTag'
        html_name = 'TagAction'
        param_dict['tagName'] = tagname
        param_dict['tagVersion'] = version_id
        param_dict['env'] = env_name
        param_dict['withCompil'] = '1'
        param_dict['genProjTree'] = '1'
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        # TODO: return something here
        return {}


class TagNewVersion(Resource):
    def get(self,tag_name, version_id):
        # result = db.session.execute('select ID from TAG where USER_NAME = :tag_name and VERSION = :version_id', {'tag_name': tag_name, 'version_id':version_id})
        result = query_db('select ID from TAG where USER_NAME = "{0}" and VERSION = {1!s}'.format(tag_name, version_id))
        if result.rowcount == 0:
            msg = 'Unable to locate the TAG: {0} version:"{1!s}"'.fomrat(tag_name, version_id)
            current_app.logger.error(msg)
            return jsonify(error='000009', message=msg )

        row = result.first()

        current_app.logger.info("Content of row for tag_id query: " + str(row))

        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row['ID']

        param_dict = dict()
        param_dict['action'] = 'TagNewVersion'
        html_name = 'TagsProperties'
        param_dict['tagIdList'] = str(tag_id)
        param_dict['tagNameOrOpAppliList'] = tag_name
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        # result_max = db.session.execute('select max(VERSION) from TAG where USER_NAME ="' + tag_name + '"')
        result_max = query_db('select max(VERSION) from TAG where USER_NAME ="' + tag_name + '"')

        row_max = result_max.first()
        max_version=row_max[0]

        current_app.logger.info('Max version of the tag:' + tag_name + 'is version:' + str(max_version) )
        major_version = int(str(max_version).split('.')[0])
        minor_version = int(str(max_version).split('.')[1])
        return {'tag_version': url_for('tag_version', tag_name = tag_name , version_id = str(major_version) + '.' + str(minor_version+1))}


class TagUpdate(Resource):
    """
    Class responsible for updating tag resources

    Used to update
    * dataloader
    * application
    * etc
    """
    def get(self,tag_name, version_id):
        current_app.logger.info('Updating Tag name = ' + tag_name + ' and version' + str(version_id))
        app_name = tag_name[:-4]
        current_app.logger.debug('Application name = ' + app_name )
        # result = db.session.execute('select ID from TAG where USER_NAME = :tag_name and VERSION = :version_id', {'tag_name': tag_name, 'version_id':version_id})
        result = query_db('select ID from TAG where USER_NAME ="{0}"and VERSION = {1!s}'.format(tag_name, version_id) )
        if result.rowcount == 0:
            msg = 'unable to resolve ID for tag name: {0}, version: {1!s}'.format(tag_name, version_id)
            current_app.logger.debug(msg)
            return jsonify(error='000010', message=msg)

        row = result.first()
        current_app.logger.debug("Content of row for tag_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row ['ID']

        # result = db.engine.execute('select distinct ID,RESTYP_PARENT from RES_DESC where NAME ="' + app_name + '"')
        result = query_db('select distinct ID,RESTYP_PARENT from RES_DESC where NAME ="' + app_name + '"')
        if result.rowcount == 0:
            msg = 'Unable to locate the applccation : {1}'.format(app_name)
            current_app.logger.debug(msg)
            return jsonify(error='000011', message=msg)

        row = result.first()
        current_app.logger.debug("Content of row for app_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        app_id = dict_row ['ID']

        # Update the dataloader first
        param_dict = dict()
        param_dict['action'] = 'UpdateTagElements'
        html_name = 'TagManageResources'
        param_dict['tagIdList'] = str(tag_id)
        param_dict['tagNameOrOpAppliList'] = tag_name
        param_dict['resIdList'] = ''
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        # Then remove the application from the tag (to update all the secondary resources)
        param_dict = dict()
        param_dict['action'] = 'RemoveResourcesInTag'
        html_name = 'TagManageResources'
        param_dict['tagIdList'] = str(tag_id)
        param_dict['tagNameOrOpAppliList'] = tag_name
        param_dict['resIdList'] = str(app_id)
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        # Re-insert the applicaiton into the tag
        param_dict = {}
        param_dict['action'] = 'AddResourcesInTag'
        html_name = 'TagManageResources'
        param_dict['tagIdList'] = str(tag_id)
        param_dict['tagNameOrOpAppliList'] = tag_name
        param_dict['resIdList'] = str(app_id)
        param_dict['loginpassthrough'] = 'true'

        call_http(html_name, param_dict)

        return {'tag_version': url_for('tag_version', tag_name=tag_name, version_id=version_id)}


class TagVersion(Resource):
    def get(self, tag_name, version_id):
        current_app.logger.info('Properties for Tag name =' + tag_name+ ' Version:' + str(version_id))
        result = query_db('select * from TAG where NAME = "User" and USER_NAME = "{0}" and VERSION = {1!s} '.format(tag_name, version_id))
        if result.rowcount == 0:
            msg = 'Unable to locate TAG name: {0} with the ID:{1!}'.format(tag_name, version_id)
            current_app.logger.error(msg)
            return jsonify(error='000012', message=msg)
        row = result.first()
        dict_row = dict([(x, row[x]) for x in result.keys()])

        current_app.logger.debug('Tag version =' + version_id)

        tag_object = dict()
        tag_object['tag_name'] = dict_row['USER_NAME']
        # Actions are per tag version
        actions = dict()
        # Update tag
        actions['update_tag'] = url_for('tag_update', tag_name=tag_name, version_id=version_id)
        # create new version
        actions['new_version'] = url_for('tag_new_version', tag_name=tag_name, version_id=version_id)
        # Delete tag
        actions['delete_tag'] = ('DELETE', url_for('tag_version', tag_name=tag_name, version_id=version_id))
        tag_object['actions'] = actions
        return tag_object

    def delete(self, tag_name, version_id):
        result = query_db('select ID from TAG where USER_NAME = :tag_name and VERSION = :version_id', {'tag_name': tag_name, 'version_id':version_id})

        if result.rowcount == 0:
            msg = 'Unable to locate the TAG name={0!s} and version: {1!s}'.format(tag_name,version_id)
            current_app.logger.debug(msg)
            return jsonify(error='000005', message=msg)

        row = result.first()
        current_app.logger.debug("Content of row for tag_id query: " + str(row))
        dict_row = dict([(x, row[x]) for x in result.keys()])
        tag_id = dict_row ['ID']

        delete_tag(tag_name,tag_id, version_id)

        return {}


class Environments(Resource):
    """
    Resource for Production Environments
    """
    def get(self):
        env_list = []
        # result = db.session.execute('select ID from ENVIRONNEMENT where STANDALONE = 0 or STANDALONE = 1')
        result = query_db('select ID from ENVIRONNEMENT where STANDALONE = 0 or STANDALONE = 1')
        for row in result:
            dict_row = dict()
            dict_row['ID'] = row['ID']
            env_list.append(url_for('environment', env_id=dict_row['ID']))
        return {'environments': env_list}

    def post(self):
        env_name = request.args.get('name')
        env_opwd = request.args.get('path')
        env_type = 'ENV_TEST'

        opInstallDir = current_app.config['OPINSTALLDIR']

        current_app.logger.debug('env_name : ' + env_name )
        current_app.logger.debug('env_opwd: ' + env_opwd)
        if not os.path.exists(env_opwd):
            os.makedirs(env_opwd)

        # First check env_name does not exist
        result = query_db('select * from ENVIRONNEMENT where NAME="' + env_name + '"')

        if result.rowcount == 0:
            # TODO: To deploy the code to an Environment other than local host
            param_dict = dict()
            param_dict['action'] = 'AddEnvironnement'
            html_name = 'EnvironnementAction'
            param_dict['loginpassthrough'] = 'true'
            param_dict['envID'] = ''
            param_dict['nameEnv'] = env_name
            param_dict['description'] = 'The API created environement ' + env_name
            param_dict['hprodEngine'] = opInstallDir
            param_dict['htype'] = env_type
            param_dict['opWD'] = env_opwd
            #Standalone Environment configurable?
            param_dict['A_standalone'] = 'true'
            # A_remote is a value of 0 or 1, are we creating a remote enviornemnte
            param_dict['A_remote'] = '0'
            param_dict['remote'] = ''
            #remote OS configurable?
            param_dict['os'] = ''
            # remote smd configurable?
            param_dict['remote_SMD'] = ''
            #remote Python configurable?
            param_dict['remote_Python'] = ''
            param_dict['hfunctions'] = ''
            param_dict['hdomaines'] = ''
            param_dict['hressources'] = ''

            call_http(html_name, param_dict)
        else:
            row = result.first()
            msg = 'Environnement name {0} already exists, its ID ={1!s}'.format(env_name, row['ID'])
            current_app.logger.error(msg)
            return jsonify(error='000011',message=msg )
        result_b = db.engine.execute('select * from ENVIRONNEMENT where NAME="' + env_name + '"')
        #result_b = query_db('select * from ENVIRONNEMENT where NAME="{0}"'.format(env_name))
        row = result_b.first()
        env_id = row['ID']
        current_app.logger.debug('env_id =' + str(env_id))
        return {'environment': url_for('environment', env_id = env_id)}


class Environment(Resource):
    def get(self, env_id):
        tags_lst = []
        env_results = query_db('select NAME, TYPE, OPWD from ENVIRONNEMENT where ID=' + str(env_id))
        if env_results .rowcount == 0:
            msg = 'Unable to locate the environment with id: {0!s}'.format(env_id)
            current_app.logger.error(msg)
            return jsonify(error='000008', message=msg)
        env_row = env_results.first()
        env_name = env_row['NAME']
        env_type = env_row['TYPE']
        env_path = env_row['OPWD']

        # result = db.session.execute('select STATUS,TAG_CHILD from ENVIRONNEMENT_TAG_LNK where ENVIRONNEMENT_PARENT = ' + str(env_id))
        result = query_db('select STATUS,TAG_CHILD from ENVIRONNEMENT_TAG_LNK where ENVIRONNEMENT_PARENT = ' + str(env_id))

        for row in result:
            current_app.logger.debug('TAG_ID = ' + str(row['TAG_CHILD']))
            tag_result = query_db('select USER_NAME, VERSION from TAG where ID = ' + str(row['TAG_CHILD']))
            row_t =tag_result.first()
            tags_lst.append(url_for('tag_version', tag_name = row_t['USER_NAME'], version_id =  row_t['VERSION']))

        current_app.logger.debug(str(tags_lst))

        return {'tags': tags_lst,'NAME':env_name, 'TYPE':env_type, 'PATH':env_path}

    def delete(self, env_id):
        result = query_db('select NAME from ENVIRONNEMENT where ID="' + str(env_id) + '"')
        # result = db.session.execute('select NAME from ENVIRONNEMENT where ID="' + str(env_id) + '"')
        if result.rowcount == 0:
            return {'error': 'Environment does not exist'}

        row = result.first()

        param_dict = dict()
        param_dict['action'] = 'DeleteOneEnvironnement'
        param_dict['loginpassthrough'] = 'true'
        param_dict['envID'] = str(env_id)
        html_name = 'EnvironnementAction'

        call_http(html_name, param_dict)

        return {}


with app.app_context():
    api_base_url = current_app.config['API_BASE']

api.add_resource(Echo, '/'.join([api_base_url, 'echo']), endpoint='echo')
api.add_resource(Applications, '/'.join([api_base_url, 'applications']), endpoint='applications')
api.add_resource(Application, '/'.join([api_base_url, 'application/<int:app_id>']), endpoint='application')
api.add_resource(Tags, '/'.join([api_base_url, 'tags']), endpoint='tags')
api.add_resource(Tag, '/'.join([api_base_url, 'tag/<tag_name>']), endpoint='tag')
api.add_resource(TagVersion, '/'.join([api_base_url, 'tag/<tag_name>/versions/<version_id>']), endpoint='tag_version')
api.add_resource(TagNewVersion, '/'.join([api_base_url, 'tag/<tag_name>/versions/<version_id>/new_version']), endpoint='tag_new_version')
api.add_resource(TagDeploy, '/'.join([api_base_url, 'tag/<tagname>/versions/<version_id>/deploy']), endpoint='tag_deploy')
api.add_resource(TagUpdate, '/'.join([api_base_url, 'tag/<tag_name>/versions/<version_id>/update']), endpoint='tag_update')
api.add_resource(Environments, '/'.join([api_base_url, 'environments']), endpoint='environments')
api.add_resource(Environment, '/'.join([api_base_url, 'environment/<int:env_id>']), endpoint='environment')

