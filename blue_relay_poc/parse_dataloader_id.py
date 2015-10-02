__author__ = 'mabdul-aziz'

import sys
import os

def get_dataloader_remote(template_path):
        """
        Utility function to return the dataloader associated with an application.
        it returns remake for BKO application and the dataloader name (from the Template xml file) for Middle Office
        (Composition)Template
        """
        found = False
        dataloader_name = ''
        dataloder_id = ''

        template_xml_fd = open(os.path.join(template_path),'r')
        # TODO: Check if .xml file exists, raise an error if it does not
        log_fd.write(template_path + 'n')
        for xml_line in template_xml_fd:
            if 'repository:DataManager' in xml_line:
                xml_line_lst = xml_line.split(' ')
                for xml_line_elem in xml_line_lst:
                    if str(str(xml_line_elem).split('=')[0]).strip('"') == 'name':
                        dataloader_name = str(str(xml_line_elem).split('=')[1]).strip('"')
                    if str(str(xml_line_elem).split('=')[0]).strip('"') == 'resdescid':
                        print('Dataloader Resource ID:' + str(xml_line_elem).split('=')[1] )
                        for id_char in str(str(xml_line_elem).split('=')[1]).strip('"'):
                            if id_char.isdigit():
                                dataloder_id += id_char
                found = True
        if not found :
            print('Unable to determine the dataloader from the Template .xml file:' + templates_path)
            return -1

        return dataloder_id



if __name__ == '__main__':
    app_id = sys.argv[2]
    template_path =os.path.join(sys.argv[1], 'home', 'opWD','default', 'common', 'template', str(app_id) + '.xml')
    ret_code = get_dataloader_remote(template_path)
    sys.exit(int(ret_code))
