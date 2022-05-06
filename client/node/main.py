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
            title='Error',
            ok_button='Exit'
        )
        raise ValueError('Wrong Configuration')


def dev():
    root = Main()
    if root.settings.NEW_CONFIG:
        root.configuration()


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
