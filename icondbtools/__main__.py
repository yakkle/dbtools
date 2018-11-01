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
import shutil

from .block_database_reader import BlockDatabaseReader
from .icon_service_syncer import IconServiceSyncer
from .state_database_reader import StateDatabaseReader, StateHash
from .timer import Timer


def print_last_block(args):
    db_path: str = args.db

    block_reader = BlockDatabaseReader()
    block_reader.open(db_path)
    block: dict = block_reader.get_last_block()
    block_reader.close()

    print(block)


def print_block(args):
    db_path: str = args.db
    height: int = args.height

    block_reader = BlockDatabaseReader()
    block_reader.open(db_path)
    block: dict = block_reader.get_block_hash_by_block_height(height)
    block_reader.close()

    print(block)


def print_transaction_result(args):
    db_path: str = args.db
    tx_hash: str = args.tx_hash

    block_reader = BlockDatabaseReader()
    block_reader.open(db_path)
    tx_result: dict = block_reader.get_transaction_result_by_hash(tx_hash)
    block_reader.close()

    print(tx_result)


def sync(args):
    db_path: str = args.db
    start: int = args.start
    count: int = args.count
    stop_on_error: bool = args.stop_on_error
    no_commit: bool = args.no_commit
    write_precommit_data: bool = args.write_precommit_data
    builtin_score_owner: str = args.builtin_score_owner
    fee: bool = bool(args.fee)
    audit: bool = bool(args.fee)
    deployer_whitelist: bool = bool(args.deployer_whitelist)
    score_package_validator: bool = bool(args.score_package_validator)

    # If --start option is not present, set start point to the last block height from statedb
    if start < 0:
        try:
            state_db_path = '.statedb/icon_dex'
            reader = StateDatabaseReader()
            reader.open(state_db_path)
            block: 'Block' = reader.get_last_block()
            start = block.height + 1
        except:
            start = 0
        finally:
            reader.close()

    print(f'loopchain_db_path: {db_path}\n'
          f'start: {args.start}, {start}\n'
          f'count: {count}')

    syncer = IconServiceSyncer()
    syncer.open(
        fee=fee,
        audit=audit,
        deployer_whitelist=deployer_whitelist,
        score_package_validator=score_package_validator,
        builtin_score_owner=builtin_score_owner)
    syncer.run(
        db_path, start_height=start, count=count,
        stop_on_error=stop_on_error, no_commit=no_commit,
        write_precommit_data=write_precommit_data)
    syncer.close()


def clear(args):
    """Clear .score and .statedb

    :param args:
    :return:
    """
    paths = ['.score', '.statedb']
    for path in paths:
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass


def run_command_state_hash(args):
    """Create hash from state db

    :param args:
    :return:
    """
    timer = Timer()
    db_path: str = args.db

    reader = StateDatabaseReader()
    reader.open(db_path)

    timer.start()
    state_hash: 'StateHash' = reader.create_state_hash()
    timer.stop()

    reader.close()

    print(state_hash)
    print(f'elapsedTime: {timer.duration()} seconds')


def run_command_state_last_block(args):
    """Read the last block from statedb

    :param args:
    :return:
    """
    db_path: str = args.db

    try:
        reader = StateDatabaseReader()
        reader.open(db_path)

        block: 'Block' = reader.get_last_block()
        print(f'height: {block.height}\n'
              f'timestamp: {block.timestamp}\n'
              f'prev_hash: 0x{block.prev_hash.hex()}\n'
              f'block_hash: 0x{block.hash.hex()}')
    finally:
        reader.close()


def main():
    mainnet_builtin_score_owner = 'hx677133298ed5319607a321a38169031a8867085c'

    parser = argparse.ArgumentParser(prog='icondbtools', description='icon db tools')

    subparsers = parser.add_subparsers(title='subcommands')

    # create the parser for the 'sync' command
    parser_sync = subparsers.add_parser('sync')
    parser_sync.add_argument('--db', type=str, required=True)
    parser_sync.add_argument('-s', '--start', type=int, default=-1, help='start height to sync')
    parser_sync.add_argument(
        '-c', '--count', type=int, default=999999999, help='The number of blocks to sync')
    parser_sync.add_argument(
        '-o', '--owner',
        dest='builtin_score_owner',
        default=mainnet_builtin_score_owner,
        help='BuiltinScoreOwner')
    parser_sync.add_argument(
        '--stop-on-error',
        action='store_true',
        help='stop running when commit_state is different from state_root_hash')
    parser_sync.add_argument(
        '--no-commit', action='store_true', help='Do not commit')
    parser_sync.add_argument(
        '--write-precommit-data', action='store_true', help='Write precommit data to file')
    parser_sync.add_argument('--fee', type=int, default=1, help='Enable fee')
    parser_sync.add_argument('--audit', type=int, default=1, help='Enable audit')
    parser_sync.add_argument('--deployer-whitelist', type=int, default=0, help='Enable deployer whitelist')
    parser_sync.add_argument('--score-package-validator', type=int, default=0, help='Enable score package validator')
    parser_sync.set_defaults(func=sync)

    # create the parser for lastblock
    parser_last_block = subparsers.add_parser('lastblock')
    parser_last_block.add_argument('--db', type=str, required=True)
    parser_last_block.set_defaults(func=print_last_block)

    # create the parser for block
    parser_block = subparsers.add_parser('block')
    parser_block.add_argument('--db', type=str, required=True)
    parser_block.add_argument('--height', type=int, default=0, help='start height to sync', required=True)
    parser_block.set_defaults(func=print_block)

    # create the parser for txresult
    parser_block = subparsers.add_parser('txresult')
    parser_block.add_argument('--db', type=str, required=True)
    parser_block.add_argument(
        '--hash', dest='tx_hash', help='tx hash without "0x" prefix', required=True)
    parser_block.set_defaults(func=print_transaction_result)

    # create the parser for clear
    parser_clear = subparsers.add_parser('clear', help='clear .score and .statedb')
    parser_clear.set_defaults(func=clear)

    # create the parser for statehash
    parser_state_hash = subparsers.add_parser('statehash')
    parser_state_hash.add_argument('--db', type=str, required=True)
    parser_state_hash.set_defaults(func=run_command_state_hash)

    # create the parser for statelastblock
    parser_state_last_block = subparsers.add_parser('statelastblock')
    parser_state_last_block.add_argument('--db', type=str, required=True)
    parser_state_last_block.set_defaults(func=run_command_state_last_block)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    args = parser.parse_args()
    print(args)
    args.func(args)


if __name__ == '__main__':
    main()
