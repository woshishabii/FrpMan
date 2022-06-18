import argparse
import os
import platform

import easygui

import uuid

import json
import tarfile
import zipfile
import hashlib

import requests

CONFIG_STRUCTURE = {
    'basic': [
        'main_server',
        'node_uuid',
        'server_password',
    ]
}
FILEDIR = 'source'


class FrpManExceptions(Exception):
    pass


class StaticConfig:
    """ StaticConfig Class
    Basic Configuration of FrpMan Node Client
    these configs shouldn't be changed while running
    """
    def __init__(self):
        """ Initial Method
        :var self.config: Dict that stores the config
        :var self.NEW_CONFIG: Judging First Run
        """
        # Initial a new config
        # First, we should try to load config from file
        self.config = {}
        if os.path.exists('config.json'):
            # If it exists, we should validate
            self.NEW_CONFIG = False
            self.load()
            if self.validate_config(self.config):
                pass
            else:
                raise FrpManExceptions('Invalid StaticConfig')
        else:
            self.NEW_CONFIG = True
            # Ask user to fill the form
            self.initial_new_config()

    @staticmethod
    def validate_config(config: dict) -> bool:
        if type(config) is not dict:
            return False
        if 'basic' not in config:
            return False
        for _ in CONFIG_STRUCTURE['basic']:
            if _ not in config['basic']:
                return False
        return True

    def initial_new_config(self):
        # Initial a new config
        self.config = {
            'basic': {
                'main_server': '',
                'node_uuid': '',
                'server_password': '',
            }
        }
        form = easygui.multenterbox(
            msg='Fill the basic information about the node',
            title='Configuration',
            fields=['Main Server Address', 'Node UUID', 'Password'],
            values=['No "/" at end', str(uuid.uuid4()), ''],
        )
        if form is None:
            raise FrpManExceptions('Empty Form')
        (
            self.config['basic']['main_server'],
            self.config['basic']['node_uuid'],
            self.config['basic']['server_password'],
        ) = form
        self.save()

    def load(self):
        with open('config.json', 'r') as c_obj:
            self.config = json.load(c_obj)

    def save(self):
        with open('config.json', 'w') as c_obj:
            json.dump(self.config, c_obj)


class DynamicConfig:
    """ DynamicConfig Class
    These configs are usually gotten from the server on startup
    Sync with the main server
    """
    def __init__(self, static: StaticConfig):
        """ Initial Method
        Creates a DynamicConfig Instance
        and Get Update From the Server """
        self.valid = False
        self.response = {}
        self.static = static
        self.server_info = {}
        self.node_info = {}
        self.get_data()

    def get_data(self):
        """ Get Data From Main Server
        Including:
        /node/server_info API
        /node/node_api API
        """
        # Get server_info API
        self.response = json.loads(requests.get(f'{self.static.config["basic"]["main_server"]}/node/server_info/').text)
        if 'frp_man_valid' in self.response:
            self.valid = True
            self.server_info = self.response.copy()
            print('OK')
        else:
            self.valid = False
            raise FrpManExceptions('Invalid Server Response, is the main server down?')
        # Get node_api
        url = f'{self.static.config["basic"]["main_server"]}/node/node_api/{self.static.config["basic"]["node_uuid"]}|{self.static.config["basic"]["server_password"]}'
        self.response = json.loads(requests.get(url).text)
        if 'error' in self.response:
            raise FrpManExceptions(self.response['error'])
        self.node_info = self.response.copy()


class Channel:
    """ Channel Class
    Defines Each Channel """

    def __init__(self):
        pass

    def generate_files(self):
        """ Generates FRPS Files """
        pass


class FrpMan:
    """ FrpMan Main Class
    Defines the most during the program
    """
    def __init__(self):
        """ Init method
        Create a new instance of FrpMan"""
        self.system = ''
        self.machine = ''
        self.static_config = StaticConfig()
        self.dynamic_config = DynamicConfig(self.static_config)

    def start(self):
        pass

    def check_files(self):
        """ Check Files Function
        Check and download automatically files needed for FrpMan
        List of files
        - Frps Bin File
        - Checksum
        """
        # Create File Dir
        if not os.path.exists(FILEDIR):
            print('[LOG] FILE DIR not exists, Creating a new one.')
            os.mkdir(FILEDIR)
        # Create Frps Files Dir
        if not os.path.exists(f'{FILEDIR}/frps'):
            print('[LOG] FRPS DIR not exists, Creating one')
            os.mkdir(f'{FILEDIR}/frps')
        if not os.path.exists(f'{FILEDIR}/frps/archive'):
            os.mkdir(f'{FILEDIR}/frps/archive')
        # Check FRPS Files nad versions
        # Check Platform
        # Tested on Windows 11, Kali Linux
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        if self.machine == 'x86_64':
            self.machine = 'amd64'
        print(f'[LOG] Detected Environment: {self.system} - {self.machine}')
        if self.system == 'windows':
            self.dl_name = f'frp_0.41.0_{self.system}_{self.machine}.zip'
        else:
            self.dl_name = f'frp_0.41.0_{self.system}_{self.machine}.tar.gz'
        self.dl_url = f'https://github.com/fatedier/frp/releases/download/v0.41.0/{self.dl_name}'
        print(f'[LOG] Downloading FRPS File: {self.dl_url}')
        if os.path.exists(f'./source/frps/archive/{self.dl_name}'):
            if input('[INFO] Older Download Detected, Remove?') == 'y':
                os.remove(f'./source/frps/archive/{self.dl_name}')
                self.dl = requests.get(self.dl_url, allow_redirects=True)
                with open(f'./source/frps/archive/{self.dl_name}', 'wb') as d_obj:
                    d_obj.write(self.dl.content)
            else:
                pass
        else:
            self.dl = requests.get(self.dl_url, allow_redirects=True)
            with open(f'./source/frps/archive/{self.dl_name}', 'wb') as d_obj:
                d_obj.write(self.dl.content)
        self.dl_checksum_url = 'https://github.com/fatedier/frp/releases/download/v0.41.0/frp_0.41.0_sha256_checksums.txt'
        print(f'[LOG] Downloading FRPS Checksum File: {self.dl_checksum_url}')
        if os.path.exists(f'./source/frps/frp_sha256_checksums.txt'):
            if input('[INFO] Older Download Detected, Remove?') == 'y':
                os.remove('./source/frps/frp_sha256_checksums.txt')
                self.dl_checksum = requests.get(self.dl_checksum_url, allow_redirects=True)
                with open(f'./source/frps/frp_sha256_checksums.txt', 'w') as cs_obj:
                    cs_obj.write(self.dl_checksum.text)
            else:
                pass
        else:
            self.dl_checksum = requests.get(self.dl_checksum_url, allow_redirects=True)
            with open(f'./source/frps/frp_sha256_checksums.txt', 'w') as cs_obj:
                cs_obj.write(self.dl_checksum.text)
        # Validate File
        with open('./source/frps/frp_sha256_checksums.txt') as cs_obj:
            for line in cs_obj:
                if line.strip().split()[1] == self.dl_name:
                    print(f'[LOG] Expected SHA256: {line.strip().split()[0]}')
                    self.dl_sha256 = line.strip().split()[0]
                    break
        with open(f'./source/frps/archive/{self.dl_name}', 'rb') as dl_obj:
            self.dl_real_sha256 = hashlib.new('sha256', dl_obj.read()).hexdigest()
            print(f'[LOG] Actual Checksum: {self.dl_real_sha256}')
            if not self.dl_real_sha256 == self.dl_sha256:
                raise FrpManExceptions('Mismatched Checksum')
            else:
                print('[LOG] Matched SHA256')
        # Extract Files
        print(f'[LOG] Extracting {self.dl_name}')
        if self.dl_name.endswith('.tar.gz'):
            self.dl_tf = tarfile.open(f'./source/frps/archive/{self.dl_name}')
            self.dl_tf.extractall('./source/frps/')
        elif self.dl_name.endswith('.zip'):
            with zipfile.ZipFile(f'./source/frps/archive/{self.dl_name}') as zf_obj:
                zf_obj.extractall('./source/frps')


def dev():
    # For test only
    fm = FrpMan()
    fm.check_files()


def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="-==Frp Manager Node Client==-")
    parser.add_argument('--developer', action='store_true', required=False)
    args = parser.parse_args()

    if args.developer:
        dev()
    else:
        main()
