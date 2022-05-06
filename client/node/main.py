import argparse

import requests

import easygui

import json
import uuid


class Settings:
    def __init__(self):
        pass

    class Basic:
        main_server = str()
        password = str()
        node_uuid = uuid.UUID('12345678-abcd-abcd-abcd-123456789011')

    def save(self):
        with open('config.json', 'w') as f_obj:
            config = {
                'main_server': self.Basic.main_server,
                'password': self.Basic.password,
                'uuid': str(self.Basic.node_uuid),
            }
            json.dump(config, f_obj)

    def list(self):
        return dir(self.Basic)


class Main:
    def __init__(self):
        self.settings = Settings()

    def configuration(self):
        main_server = easygui.enterbox(
            msg='Please enter FrpMan Main Server Address',
            title='Configuration',
            default='http://example.com',
            strip=True
        )
        if main_server is None:
            return
        password = easygui.enterbox(
            msg='Please Enter Server Management Password',
            title='Configuration',
            default='Password',
        )
        if password is None:
            return
        node_uuid = easygui.enterbox(
            msg='Please Enter Node\'s UUID',
            title='Configuration',
            default=str(uuid.uuid4()),
        )
        if node_uuid is None:
            return
        if main_server and password and node_uuid:
            self.settings.Basic.main_server = main_server
            self.settings.Basic.password = password
            self.settings.Basic.node_uuid = uuid.UUID(node_uuid)
            self.settings.save()
            try:
                server_info = requests.get(f"{self.settings.Basic.main_server}/node/node_api")
            except ConnectionError:
                pass


def dev():
    root = Main()
    print(list(root.settings))
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
