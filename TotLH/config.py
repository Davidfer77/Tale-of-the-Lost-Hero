import os
import json
from importlib import resources


def cfg_item(*items):
    dat= Config.get_instance().data
    for key in items:
        dat = dat[key]
    return dat

class Config:

    __instance = None
    __json_path, __json_filename = "TotLH.assets.config", "config.json"

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config()
        return Config.__instance
    
    def __init__(self):
        if Config.__instance is None:
            Config.__instance = self
            
            with resources.path(Config.__json_path, Config.__json_filename) as json_path:
                with open(json_path) as f:
                    self.data = json.load(f)
        else:
            raise Exception("Config is allowed to have only one instance")
