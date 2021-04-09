"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   4/8/21 - 2:13 AM
"""
import time

import scrapy.commands.crawl as crawl
from scrapy.exceptions import UsageError
from scrapy.commands import ScrapyCommand

import config


class Command(crawl.Command):
    def syntax(self):
        return "<spider_name> [options]"
        # return "[options] <spider>"

    def short_desc(self):
        return "Crawl danke"

    def long_desc(self):
        return "Crawl danke data to a MySQL database."

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

        parser.add_option("-c", "--city", type="str", dest="city", default="",
                          help="设置要爬取的城市名，如 北京市")
        parser.add_option("-d", "--dates", nargs=2, type="str", dest="sign_date", default=["", ""],
                          help="设置要爬取的签约起始日期和结束如期")

    def set_city(self, city):
        if len(city) != 3:
            raise UsageError('必须是三个字，比如：北京市')

        self.settings.set('CITY', city, priority='cmdline')

    def set_sign_date(self, sign_date):
        if len(sign_date) == 1 or len(sign_date) > 2:
            raise UsageError('签署日期必须是两个 或者不填')
        if len(sign_date) == 0:
            sign_date_lower = '1900-01-01'
            sign_date_upper = time.strftime("%Y-%m-%d", time.localtime())
        else:
            sign_date_lower = sign_date[0]
            sign_date_upper = sign_date[1]

        self.settings.set('SIGN_DATE_LOWER', sign_date_lower, priority='cmdline')
        self.settings.set('SIGN_DATE_UPPER', sign_date_upper, priority='cmdline')

    def run(self, args, opts):
        self.set_city(opts.city)
        self.set_sign_date(opts.sign_date)

        cfg = config.Config()

        self.settings.set("COOKIE", cfg.config['COOKIE'])
        self.crawler_process.crawl(args[0], **opts.spargs)
        self.crawler_process.start()


