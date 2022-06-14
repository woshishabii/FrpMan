import argparse
import os

import easygui

import uuid

import json


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
    def __init__(self):
        # Init Basic Var
        self.settings = {}
        # Check Configuration File
        if os.path.exists('configs.json'):
            self.NEW_CONFIG = False
        else:
            self.NEW_CONFIG = True

    def load(self):
        # Read config form file
        with open('configs.json', 'r') as f_obj:
            file = json.load(f_obj)
            if not self.validate_config(file):
                self.init_new_config()
            else:
                self.settings = file.copy()

    def init_new_config(self):
        self.settings['basic'] = {
            'main_server': '',
            'node_uuid': '',
            'server_password': '',
        }
        self.configuration_window()

    def configuration_window(self):
        user_input = easygui.multenterbox(
            msg="Type Basic Information about this Node Server",
            title="Setup",
            fields=['Main Server Address', 'Node UUID', 'Password'],
            values=['http://example.com', str(uuid.uuid4()), 'PASSWORD'],
        )
        if user_input is None:
            raise FrpManExceptions

    @staticmethod
    def validate_config(config: dict) -> bool:
        if type(config) != dict:
            return False
        if 'basic' not in config:
            return False
        for _ in CONFIG_STRUCTURE['basic']:
            if _ not in config['basic']:
                return False
        return True


def dev():
    # Startup
    # Configuration
    pass


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
