import os
import json


class Settings:
    def __init__(self):
        self.settings = {}
        # 判定是否新建配置
        if os.path.exists('config.json'):
            self.NEW_CONFIG = False
            self.load()
        else:
            self.NEW_CONFIG = True
            self.default()

    # 设置默认值 / Default Values for Settings
    def default(self):
        # 基本设置 / Basic Settings
        self.settings['basic'] = {
            'main_server': str(),
            'node_uuid': str(),
            'password': str(),
        }
        # 客户端信息 / Client Info
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
