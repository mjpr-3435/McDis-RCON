from ..modules import *
from ..utils import *

class Uploader():
    def __init__(self):
        self.is_running     = False
        self.overwrite      = False
        self.path_to_upload = '.'