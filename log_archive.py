# -*- coding: utf-8 -*-
"""

@author: Saroj Lamichhane
"""
import os
from glob import glob
import time
import zipfile
import fnmatch
import logging


# run day constant, for logging datestamp
RUN_DAY = time.strftime("%Y-%m-%d")



def initiate_logging():
    '''
    initiate log files
    '''
    logfilename = os.path.join(os.path.dirname(os.path.realpath(__file__))\
                    , RUN_DAY+'_myapp.log')
    logging.basicConfig(filename=logfilename, level=logging.WARNING)


def _check_old_logs():
    old_log_files = []
    today_log = RUN_DAY+'_myapp.log'
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*sftp.log'):
            old_log_files.append(file)

    if today_log in old_log_files:
        old_log_files.remove(today_log)
    return old_log_files


def _archive_logs(logfile, log_archive):
    zip_file = zipfile.ZipFile(log_archive, mode='a')
    try:
        zip_file.write(logfile, compress_type=zipfile.ZIP_DEFLATED)
    finally:
        zip_file.close()
        os.remove(logfile)
        print('old log files archived into zip.\n')


def _check_log_archive():
    arch_file = _get_latest_archive()

    zip_file = zipfile.ZipFile(arch_file)
    size = sum([zinfo.file_size for zinfo in  zip_file.filelist])
    zip_mb = float(size)/(1000*1000)
    if zip_mb >= 100:
        zip_name = RUN_DAY+'.log_archive.zip'
    else:
        zip_name = arch_file

    return zip_name


def send_log_archive():
    '''
    send log files to zipped archive file
    '''
    log_file_list = _check_old_logs()
    if not log_file_list:
        print('no old logs to archive')
    else:
        zip_name = _check_log_archive()
        for file in log_file_list:
            _archive_logs(file, zip_name)


def _create_archive():
    archive_name = RUN_DAY+'.log_archive.zip'
    zip_file = zipfile.ZipFile(archive_name, mode='w')
    zip_file.close()

    return archive_name


def _get_latest_archive():
    date_and_file = []
    for filename in glob('*.log_archive.zip'):
        print('zipfilename: {}'.format(filename))
        print(filename.split(".")[0])
        date_and_file.append(((filename.split(".")[0]), filename))

    #if no archives are available create one and proceed
    if not date_and_file:
        print('creating new log archive zip.')
        archive_name = _create_archive()
    else:
        print(date_and_file)
        if len(date_and_file) == 1:
            archive_name = filename
        else:
            from operator import itemgetter
            k = date_and_file.sort(key=itemgetter(0))
            print(k)
            archive_name = date_and_file.sort(key=lambda tup: tup[0])
            print('sorted names: {}'.format(archive_name))
            archive_name = archive_name[0]

    return archive_name


def log_text():
    '''
    logging timestamp pattern
    '''
    logtext = '>>'+str(time.strftime("%Y-%m-%d %H:%M:%S"))+'->'
    return logtext


def my_func():
    '''
	all my_app functions/class& methods can contain logging info as below.

    '''
    logging.info(log_text()+'my message info')
    logging.warning(log_text()+'my message warning')

	
#main method
def main():
    '''
    @parms

    '''
    #log creation and archive
    initiate_logging()
    send_log_archive()
	
    #my app functions
    my_func()


#initiate here
if __name__ == '__main__':
    '''
    call main method
    '''
    main()
