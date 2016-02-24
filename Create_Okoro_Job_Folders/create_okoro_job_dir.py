__author__ = 'mabdul-aziz'
import os
import shutil
import sys
from optparse import OptionParser


#setup_logging
def mylog(msg, verbose=True):
    if verbose:
        print(msg)


parse = OptionParser(usage='usage: %prog [options]')
parse.add_option('--in_dispatch_dir', '-i', help='The input job dispatch directory, PDF and ind file are expected ')
parse.add_option('--test_id', '-t', help='The test ID value for the output job directory')
parse.add_option('--test_cycle', '-c', help='The test ID value for the output job directory')
parse.add_option('--output_directory', '-o', help='The output directory where the test cycle input files will be created')
parse.add_option('--size', '-s', help='The number of document for this cycle')
parse.add_option('--master_index_def', '-m', help='Path to the master index definition')
parse.add_option('--verbose', '-v', action='store_true', default=True, help='Turn on verbose mode')

options, positionals = parse.parse_args()

if len(positionals) == 0:
    parse.print_usage()


# read in job folder index (arg1, or use argument parser)
# locate input pdf folder, ensure input pdf file exists
# read in test_id and test cycle (argument 2 and argument 3)

# read the input arguments
# -i D:\MA_Sefas\Clients\Incepture\Okoro\Okoro_performance\input\dispatch_002077-O02-00
# -o D:\MA_Sefas\Clients\Incepture\Okoro\Okoro_performance\output -t test1 -c 1 -s 1050
in_dir = options.in_dispatch_dir
mylog("input directory=" + in_dir, options.verbose)
job_id = str(str(os.path.basename(in_dir).split('_')[1]).split('-')[0])
mylog("job_id=" + job_id, options.verbose)

out_dir = os.path.join(options.output_directory, options.test_id + '_cycle_' + options.test_cycle)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
mylog("output_directory=" + out_dir , options.verbose)

cycle_doc_size = options.size
mylog('cycle documents size:' + cycle_doc_size )

in_index = os.path.join(in_dir, job_id + '_dispatch.ind')
mylog('in_index =' + in_index)

out_index = os.path.join(out_dir , job_id + '_dispatch.ind')
mylog('output index =' + in_index)

test_id = options.test_id
test_cycle = options.test_cycle
mylog('generating file for test_id=' + test_id + ' test_cycle' + test_cycle)

index_lst = list()
last_index_line = ''

out_index_line_lst = list()
if os.path.exists(in_index) :
    in_index_fd = open(in_index, 'r')
    out_index_fd = open(out_index,'w')
    for index_line_numb, index_line in enumerate(in_index_fd):
        mylog('index_line_numb:' + str(index_line_numb))
        # mylog('index line number ' + str(index_line_numb) + ' contents' + index_line)
        if index_line_numb > 0:
            if index_line.strip() != '':
                last_index_line = index_line.strip()
                index_lst.append(index_line)
                offset = str(str(index_line.split('\t')[0]).split('_')[0])
                num_pages = str(str(index_line.split('\t')[0]).split('_')[1])
                mylog('offset:' + offset)
                mylog('num_pages:' + num_pages)
            pdf_file_name = str(index_line.split('\t')[-1]).strip()
            mylog('pdf_file_name:' + pdf_file_name)
            if os.path.exists(os.path.join(in_dir, pdf_file_name)):
                test_cycle_filename = '_'.join([str(pdf_file_name.split('_')[0]), test_id, test_cycle, '_'.join(pdf_file_name.split('_')[1:]) ])
                mylog('text cycle filename:' + test_cycle_filename)
                shutil.copyfile(os.path.join(in_dir, pdf_file_name), os.path.join(out_dir, test_cycle_filename))
            else:
                mylog('PDF file path:' + os.path.join(in_dir, pdf_file_name) + ' does not exist')
            out_index_line_lst = index_line.split('\t')[0:-1]
            out_index_line_lst.append(test_cycle_filename)
            mylog('out_index_line_lst' + str(out_index_line_lst ))
            out_index_fd.write('\t'.join(out_index_line_lst) + '\n')
        else:
            out_index_fd.write(index_line)


    in_index_fd.close()
    if cycle_doc_size > index_line_numb :
        # implement logic to duplicate index line and documents, incrementing sequence number
        mylog('last index line:' + str(index_line_numb))
        mylog('last offset:' + offset)
        mylog('last num_pages:' + num_pages)
        offset = str(int(offset) + int(num_pages))
        new_num_pages = str(str(last_index_line.split('\t')[0]).split('_')[1])
        mylog('new index_line :' + new_num_pages)

        input_index_num_lines = len(index_lst)
        while cycle_doc_size > index_line_numb:

            index_line_numb += 1

    out_index_fd.close()

else:
    raise Exception('Unable to locate the input index file' + in_index)


