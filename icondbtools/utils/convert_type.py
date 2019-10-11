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

from iconservice.base.address import Address


def str_to_int(value: str) -> int:
    if isinstance(value, int):
        return value

    if value.startswith('0x') or value.startswith('-0x'):
        base = 16
    else:
        base = 10

    return int(value, base)


def object_to_str(value) -> str:
    if isinstance(value, Address):
        return str(value)
    elif isinstance(value, int):
        return hex(value)
    elif isinstance(value, bytes):
        return f'0x{value.hex()}'

    return value


def remove_0x_prefix(value):
    if is_0x_prefixed(value):
        return value[2:]
    return value


def is_0x_prefixed(value):
    return value.startswith('0x')


def convert_hex_str_to_bytes(value: str):
    """Converts hex string prefixed with '0x' into bytes."""
    return bytes.fromhex(remove_0x_prefix(value))


def is_str(value):
    str_types = (str,)
    return isinstance(value, str_types)


def convert_hex_str_to_int(value: str):
    """Converts hex string prefixed with '0x' into int."""
    if is_str(value):
        return int(value, 16)
    else:
        return value
