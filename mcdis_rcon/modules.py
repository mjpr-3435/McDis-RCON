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
import zipimport
import gettext
import socket
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
from flask import Flask, send_file, abort, request, send_from_directory, redirect
from abc import abstractmethod
from discord.ext import commands
from datetime import datetime
from typing import Union, Callable
from pathlib import Path

mcdis_vers          = "0.4.13a"
package_path        = os.path.dirname(__file__)
embed_colour        = 0x2f3136
blank_space         = '‎ '
omit_space          = '\u2063'
emoji_dir           = '📦'
emoji_file          = '📄'
emoji_new_command   = '📦'
emoji_pin           = '📌'
emoji_log           = '🗒️'
emoji_warning       = '⚠️'
emoji_update        = '🔄'
emoji_arrow_left    = '⬅️'
emoji_arrow_right   = '➡️'
emoji_arrow_down    = '⤵️'
check               = '✔'
uncheck             = '✖'

allowed_languages   = [ 'en', 'es']
panel_commands      = [ 'start', 'stop', 'kill', 'restart', 'mdreload']
console_commands    = [ 'start', 'stop', 'kill', 'restart', 'mdreload']
terminal_commands   = [ 'mkdir <name>', 
                        'zip <dir:index>', 
                        'unzip <file:index>', 
                        'cd <dir:index | file:index>', 
                        'del <dir:index | file:index>',  
                        'copy <dir:index | file:index> <mcdis_path>', 
                        'move <dir:index | file:index> <mcdis_path>',
                        'rename <dir:index | file:index> <new_name>']

logging.getLogger('werkzeug').setLevel(logging.ERROR)
WSGIRequestHandler.log_request = lambda *args, **kwargs: None