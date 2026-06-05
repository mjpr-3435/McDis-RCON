import importlib
import importlib.util
import configparser
import ruamel.yaml
import threading
import subprocess
import traceback
import requests
import hashlib
import discord
import inspect
import asyncio
import zipfile
import logging
import zipimport
import gettext
import aiohttp
import socket
import random
import psutil
import shutil
import nbtlib  # type: ignore[import-untyped]
import signal
import polib
import queue
import time
import json
import math
import glob
import sys
import re
import os
import uuid

from abc import abstractmethod
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, Union, cast

from discord.ext import commands
from flask import Flask, abort, redirect, request, send_file, send_from_directory
from werkzeug.serving import WSGIRequestHandler, make_server

__all__ = [
    'Any',
    'Callable',
    'Flask',
    'Path',
    'Union',
    'WSGIRequestHandler',
    'abort',
    'abstractmethod',
    'aiohttp',
    'asyncio',
    'commands',
    'configparser',
    'datetime',
    'discord',
    'gettext',
    'glob',
    'hashlib',
    'importlib',
    'inspect',
    'json',
    'logging',
    'make_server',
    'math',
    'nbtlib',
    'os',
    'polib',
    'psutil',
    'queue',
    'random',
    're',
    'redirect',
    'request',
    'requests',
    'ruamel',
    'send_file',
    'send_from_directory',
    'shutil',
    'signal',
    'socket',
    'subprocess',
    'sys',
    'threading',
    'time',
    'traceback',
    'uuid',
    'zipfile',
    'zipimport',
    'allowed_languages',
    'blank_space',
    'check',
    'console_commands',
    'cast',
    'embed_colour',
    'emoji_arrow_down',
    'emoji_arrow_left',
    'emoji_arrow_right',
    'emoji_dir',
    'emoji_file',
    'emoji_log',
    'emoji_new_command',
    'emoji_pin',
    'emoji_update',
    'emoji_warning',
    'mcdis_vers',
    'omit_space',
    'package_path',
    'panel_commands',
    'terminal_commands',
    'uncheck',
]

mcdis_vers = '0.4.33a'
package_path = os.path.dirname(__file__)
embed_colour = 0x2F3136
blank_space = '‎ '
omit_space = '\u2063'
emoji_dir = '📦'
emoji_file = '📄'
emoji_new_command = '📦'
emoji_pin = '📌'
emoji_log = '🗒️'
emoji_warning = '⚠️'
emoji_update = '🔄'
emoji_arrow_left = '⬅️'
emoji_arrow_right = '➡️'
emoji_arrow_down = '⤵️'
check = '✔'
uncheck = '✖'

allowed_languages: list[str] = ['en', 'es']
panel_commands: list[str] = ['start', 'stop', 'kill', 'restart', 'mdreload', 'adreload']
console_commands: list[str] = ['start', 'stop', 'kill', 'restart', 'mdreload']
terminal_commands: list[str] = [
    'mkdir <name>',
    'zip <dir:index>',
    'unzip <file:index>',
    'cd <dir:index | file:index>',
    'del <dir:index | file:index>',
    'copy <dir:index | file:index> <mcdis_path>',
    'move <dir:index | file:index> <mcdis_path>',
    'rename <dir:index | file:index> <new_name>',
]

logging.getLogger('werkzeug').setLevel(logging.ERROR)
WSGIRequestHandler.log_request = lambda *args, **kwargs: None  # type: ignore[method-assign]
