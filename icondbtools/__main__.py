# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys


def run_last_block(args):
    if args.help:
        print(f'{sys.argv[0]} {args.command}')


def main():
    command_handlers = {
        'lastblock': run_last_block
    }

    parser = argparse.ArgumentParser(
        prog='icondbtools',
        description='icon db tools')
    parser.add_argument(
        'command',
        help='blockbyheight blockbyhash lastblock stateroothash',
        required=True)

    args = parser.parse_args()

    command_handler = command_handlers[args.command]
    if command_handler:
        command_handler(args)


if __name__ == '__main__':
    main()
