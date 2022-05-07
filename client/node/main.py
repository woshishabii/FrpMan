import requests

import argparse

import easygui

import json
import uuid

import os


class Settings:
    def __init__(self):
        self.settings = {}
        if os.path.exists('config.json'):
            self.load()
            self.NEW_CONFIG = False
        else:
            self.default()
            self.NEW_CONFIG = True

    def default(self):
        self.settings['basic'] = {
            'main_server': '',
            'node_uuid': '',
            'password': ''
        }
        # Don't modify while running
        self.settings['LOCAL_INFO'] = {
            'version': '0.0.1',
            'build': 'alpha',
        }

    def save(self):
        with open('config.json', 'w') as f_obj:
            json.dump(self.settings, f_obj)

    def load(self):
        with open('config.json', 'r') as f_obj:
            self.settings = json.load(f_obj)
            # print(self.settings)


class Main:
    def __init__(self):
        self.settings = Settings()

    def configuration(self):
        basic_info = easygui.multenterbox(
            msg='Enter Basic Info About the Node',
            title='Configuration',
            fields=['FrpMan Main Server', 'Node UUID', 'Password'],
            values=['http://example.com', str(uuid.uuid4()), 'Password'],
        )
        # print(basic_info)
        if basic_info is None:
            self.wrong_configuration()
        for _ in basic_info:
            if _ == '':
                self.wrong_configuration()
        (
            self.settings.settings['basic']['main_server'],
            self.settings.settings['basic']['node_uuid'],
            self.settings.settings['basic']['password']
        ) = basic_info
        self.settings.save()

    @staticmethod
    def wrong_configuration():
        easygui.msgbox(
            msg='Wrong Configuration, exiting now',
            title='Error - Invalid Config',
            ok_button='Exit'
        )
        exit(ValueError('Wrong Configuration'))

    @staticmethod
    def invalid_json_format():
        easygui.msgbox(
            msg='INVALID Response from Main Server, exiting now',
            title='Error - Invalid Server',
            ok_button='Exit'
        )
        raise ValueError('Invalid Server')

    @staticmethod
    def no_connection(e):
        easygui.msgbox(msg=e)
        exit(e)

    def fetch_main_server_info(self):
        print('Fetching Server Info')
        try:
            info = requests.get(f'{self.settings.settings["basic"]["main_server"]}/node/server_info/')
        except requests.exceptions.ConnectionError as e:
            self.no_connection(e)
        # print(info.text)
        if 'application/json' not in info.headers['Content-Type']:
            self.invalid_json_format()
        info_j = json.loads(info.text)
        try:
            if not info_j['frp_man_valid']:
                self.invalid_json_format()
        except KeyError as e:
            self.invalid_json_format()
        print('Valid')


def dev():
    root = Main()
    if root.settings.NEW_CONFIG:
        root.configuration()
    root.fetch_main_server_info()


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
