import argparse
import os

import easygui

import uuid

import json

import requests


CONFIG_STRUCTURE = {
    'basic': [
        'main_server',
        'node_uuid',
        'server_password',
    ]
}


class FrpManExceptions(Exception):
    pass


class Config:
    """ Config Class
    Basic Configuration of FrpMan Node Client
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
                raise FrpManExceptions('Invalid Config')
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


def dev():
    # Startup
    # Configuration
    c = Config()


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
