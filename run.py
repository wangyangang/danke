"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   4/8/21 - 12:05 PM
"""
from scrapy import cmdline
from config import Config

cfg = Config()
city = cfg.config['city']
sign_date_lower = cfg.config['sign_date_lower']
sign_date_upper = cfg.config['sign_date_upper']
cmd = 'scrapy run chufang -c %s -d %s %s' % (city, sign_date_lower, sign_date_upper)
print(cmd)
cmdline.execute(cmd.split())