import importlib.util
import configparser
import ruamel.yaml
import subprocess
import importlib
import threading
import traceback
import requests
import hashlib
import discord
import inspect
import asyncio
import zipfile
import logging
import gettext
import random
import psutil
import shutil
import nbtlib
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
import requests
import hashlib
import uuid

from werkzeug.serving import make_server, WSGIRequestHandler
from flask import Flask, send_file, abort, request, send_from_directory
from abc import abstractmethod
from discord.ext import commands
from datetime import datetime
from typing import Union, Callable
from pathlib import Path

package_path        = os.path.dirname(__file__)
embed_colour        = 0x2f3136
blank_space         = '‎ '
omit_space          = '\u2063'
emoji_dir           = '📦'
emoji_file          = '📄'
emoji_new_command   = '📦'
emoji_pin           = '📌'
emoji_writing       = '🗒️'
emoji_warning       = '⚠️'
emoji_update        = '🔄'
emoji_arrow_left    = '⬅️'
emoji_arrow_right   = '➡️'
emoji_arrow_down    = '⤵️'
check               = '✔'
uncheck             = '✖'

### Mover estos a sus respectivos lugares
request_size_limit  = 5 * 1024**2
max_processes       = 5

allowed_languages   = [ 'en', 'es']
panel_commands      = [ 'start-all', 'stop-all', 'start', 'stop', 'kill', 'restart', 'reload mdplugins']
console_commands    = [ 'start', 'stop', 'kill', 'restart', 'reload mdplugins']
terminal_commands   = [ 'mkdir <name>', 
                        'zip <dir:index>', 
                        'unzip <file:index>', 
                        'cd <dir:index | file:index>', 
                        'del <dir:index | file:index>',  
                        'copy <dir:index | file:index> <mcdis_path>', 
                        'move <dir:index | file:index> <mcdis_path>',
                        'rename <dir:index | file:index> <new_name>']

# logging.getLogger('werkzeug').setLevel(logging.ERROR)
# WSGIRequestHandler.log_request = lambda *args, **kwargs: None