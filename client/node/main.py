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
