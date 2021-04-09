"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   4/8/21 - 3:52 AM
"""
import json
import os


class Config:
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = None

    def __init__(self):

        with open(self.config_path, 'r', encoding='utf8') as f:
            self.config = json.loads(f.read())
