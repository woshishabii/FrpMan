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
        # Initial a new config
        # First, we should try to load config from file
        if os.path.exists('config.json'):
            # If it exists, we should validate
            self.NEW_CONFIG = False
            with open('config.json', 'r') as c_obj:
                self.config = json.load(c_obj)
                if self.validate_config(self.config):
                    pass
                else:
                    raise FrpManExceptions('Invalid Config')
        else:
            self.NEW_CONFIG = True
        pass

    @staticmethod
    def validate_config(config: dict) -> bool:
        if type(config) is not dict:
            return False
        return True

    def initial_new_config(self):
        pass


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
