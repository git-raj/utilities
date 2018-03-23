# -*- coding: utf-8 -*-
"""

@author: Saroj Lamichhane
"""
import os
import time

import paramiko



class SFTP(object):
    '''
    SFTP class.

    '''
    def __init__(self, user, passwd, url, transfer_details):
        '''
        @parms
        user: username for ftp site login
        passwd: password for stp site login
        url: ftp site hyperlink
        transfer_details: dictonary of transfer paths
            eg. transfer_details = {'sftp_inbound':'/sftp/inboud/',
                        'sftp_outbound':'/sftp/outbound/',
                        'local_inbound':'\\mydir\\inboud\',
                        'local_outbound':'\\mydir\\outbound\\'}
        '''

        self.user = user
        self.passwd = passwd
        self.url = url
        self.details = transfer_details

    #get ssh connectivity
    def get_ssh(self):
        '''
        get ssh connectivity
        '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.url, username=self.user, password=self.passwd)
        ssh = ssh
        return ssh

    #core get file process
    def process_get_files(self):
        '''
        downloads files via sftp
        '''
        path = self.details['sftp_outbound']
        localpath = self.details['local_inbound']

        with self.get_ssh().open_sftp() as sftp:
            file_list = [os.path.join(path, file) \
                        for file in sftp.listdir(path)]
            for file in file_list:
                file_name = file.split(path)[1].replace('\\', '')
                if os.path.exists(os.path.join(localpath, file_name)):
                    print('{} has already been downloaded.'.format(file_name))
                else:
                    sftp_file = file.split(path)[1]
                    ftp_file = sftp_file.replace('/', '').replace('\\', '')
                    win_format_file = localpath+ftp_file
                    file1 = '/'+localpath+'/'+ftp_file

                    print('Downloading file: {}'.format(ftp_file))
                    sftp.get(file1, win_format_file)

                    print('Download complete./n')

                    #delete file in server
                    print('Deleting {} from server.'.format(file1))
                    sftp.remove(file1)


    #core upload file process
    def process_upload_files(self):
        '''
        uploads file via sftp
        '''
        localpath = self.details['local_outbound']
        path = self.details['sftp_inbound']
        with self.get_ssh().open_sftp() as sftp:
            file_list = [f for f in os.listdir(localpath) \
            if os.path.isfile(os.path.join(localpath, f))]
            for file in file_list:
                file_loc = os.path.join(localpath, file)
                file_ftp = path+file

                print('Uploading Local file: {} .'.format(file_loc))

                sftp.put(file_loc, file_ftp)
                print('Upload complete')

                os.remove(file_loc)
                print('Local file: {} deleted.'.format(file_loc))



#main method to invoke the SFTP process
def main(user, passwd, url, transfer_details, loop_in):
    '''
    @parms
    user: username for ftp site login
    passwd: password for stp site login
    url: ftp site hyperlink
    loop_in: loop time to check for new files for transfer
    transfer_detail: dictonary of transfer paths
        eg.    transfer_detail = {'sftp_inbound':'/sftp/inboud/',
                        'sftp_outbound':'/sftp/outbound/',
                        'local_inbound':'\\mydir\\inboud\',
                        'local_outbound':'\\mydir\\outbound\\'}

    '''
    while True: #or any condition boolean check for looping construct.

        print('checking for files to download and upload.')
        sftp_obj = SFTP(user, passwd, url, transfer_details)
        sftp_obj.process_get_files()
        sftp_obj.process_upload_files()

        time.sleep(loop_in)
        print('...')



#initiate here
if __name__ == '__main__':

    #reading the config file
    import configparser
    config = configparser.ConfigParser()
    config.read('SFTP_Config.ini')

    URL = config['Login info']['FTP_Site']
    USER = config['Login info']['Username']
    PASSWD = config['Login info']['Password']


    TRANSFER_DETAILS = {'sftp_inbound':config['Transfer Details']['Sftp_Inbound'],
                        'sftp_outbound':config['Transfer Details']['Sftp_Outbound'],
                        'local_inbound':config['Transfer Details']['Local_Inbound'],
                        'local_outbound':config['Transfer Details']['Local_Outbound']}

    LOOP_IN = int(config['Check Frequency']['Loop_Time'])


    #calling main method for SFTP
    main(USER, PASSWD, URL, TRANSFER_DETAILS, LOOP_IN)
