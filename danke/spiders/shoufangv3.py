import scrapy
import arrow
import os
import math
import requests
from lxml import etree
from urllib.parse import urlencode
from functools import reduce
import time
import random

from danke.items import ShoufangV3Contract, ShoufangV3DetailItem


def isLeapYear(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    # 断言：年份不为整数时，抛出异常。
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, ‘不是闰年‘)
        days_sum = 365
        return days_sum


def getAllDayPerYear(years):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)
    # print(all_date_list)
    return all_date_list


def getAllMonthPerYear(years):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    start_date = '%s-1-1' % years
    end_date = '%s-1-31' % years
    a = 0
    all_month_list = []
    while a < 12:
        month_start_date = arrow.get(start_date).shift(months=a).format("YYYY-MM-DD")
        month_end_date = arrow.get(end_date).shift(months=a).format("YYYY-MM-DD")
        a += 1
        all_month_list.append((month_start_date, month_end_date))
    # print(all_date_list)
    return all_month_list


class DkSpider(scrapy.Spider):
    name = 'shoufangv3'
    allowed_domains = ['www.danke.com']
    headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36 DingTalk(6.0.0-macOS-14426516) nw Channel/201200',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'referer': 'https://www.danke.com/admin/pangu/arm/contract/landlord/list?page=5',
            # 'referer': 'https://www.danke.com/admin',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            #'cookie': 'DK_SSO_TGC=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyMjA1LDEiLCJhdWQiOiJwaHBBZG1pbiIsImlhdCI6MTYxNTcxMzA4M30.WPmL1bhGemZyAo_mKo5w9p5vIBGH2FXxNoK0UDMsxT4'
            #'cookie': 'staff_user_info=%7B%22avatar%22%3A%22%22%2C%22city%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22email%22%3A%22chenzhihong%40danke.com%22%2C%22expireTime%22%3A1615720283827%2C%22loginClientId%22%3A%22phpAdmin%22%2C%22loginTime%22%3A1615713083827%2C%22mobile%22%3A%2217710342123%22%2C%22name%22%3A%22%E9%99%88%E6%B2%BB%E5%AE%8F%22%2C%22renewalSeconds%22%3A7200%2C%22uid%22%3A2205%2C%22userId%22%3A2205%2C%22userType%22%3A1%2C%22userTypeEnum%22%3A%22CORP_USER%22%7D'
            'cookie': 'SSO_SESSION_ID=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyMjA1LDEiLCJhdWQiOiJwaHBBZG1pbiIsImlhdCI6MTYxNzI0NjU4M30.wWwNwR1l4Kg7AVNM2-WE1Z__K63duAKnYif0yJaE2fY'
            #'cookie': 'SSO_REFRESH_TOKEN=N_3BfY8WFwgofYjopW08W-_z7xjdfEhSd8Imea4mAPni6g4zXy2JZqbowolqaxo2lmeH4KLnHbk5_DH6vTqJmQ%3D%3D.5e1ce2b06ea310484708b2bbeed064a8834da04e64c7136f370cee4ffbaa71da',
            #'cookie': 'XSRF-TOKEN=eyJpdiI6IlkrSnV6VlwvWkplN3crVWhHVzN2V05BPT0iLCJ2YWx1ZSI6IlBpK2czRWs3SFhLZlViNTk1Z3BaYlwvK2dKczY2NDh6ZG9pRWIrVjVZN1pTOHRcL0xubm84R0V5TXJjZUNuS1MwZWN1QVpqZ0lEczNkcHlUemQrZU1DZWc9PSIsIm1hYyI6IjIwYmRjNjJjYjdlNzAxOThkNDcxMDI1YWQ4ZDJmMmRjMzZiODdiN2U3YTEwNzk5OTcyODY0ZTFjMGM2N2M5MmIifQ%3D%3D'
            #'cookie': 'session=eyJpdiI6IjR1VUJNOUNROGF3V0s4TFlWSkhkNGc9PSIsInZhbHVlIjoiZHpnVG0rZjlTSlwvdnNMSGF5cDhYZVBObEwzZ2tJamVDaEdheThsODhkM1ZJazJVVFlTNXM0ZWt5Z2ZUb3JwNm9YUk1LRmw5NkI3dWQwdDZvY1RtTnlnPT0iLCJtYWMiOiJkOGE2YjQ5ZWI2Mzc4MDVmZWMwYWMwNDNmZDJkYWFjM2JjNGE2YjlhOWRkNTIwNDI1YjgyNGMwNmNlYzllZjk0In0%3D'
        }

    def get_data_count(self, city, start_date, end_date):
        page1_url = 'https://www.danke.com/admin/pangu/arm/contract/landlord/list'
        params = {
            'city': city,
            'number': '',
            'suite_id': '',
            'address': '',
            'block_name': '',
            'dealer_name': '',
            'keeper_name': '',
            'landlord_id_name': '',
            'landlord_mobile': '',
            'sign_date-lower': start_date,
            'sign_date-upper': end_date,
            'start_date-lower': '',
            'start_date-upper': '',
            'type': '',
            'manage_status': '',
            'status': '',
            'stage': '',
            'first_payment_date-lower': '',
            'first_payment_date-upper': '',
            'all_rent_date-lower': '',
            'all_rent_date-upper': '',
            'end_date-lower': '',
            'end_date-upper': '',
            'has_measure': ''
        }
        page1_ret = requests.get(page1_url, headers=self.headers, params=params)
        # with open('page1.html', 'w') as f:
        #     f.write(page1_ret.content.decode())
        # 获取总数据量
        tree = etree.HTML(page1_ret.content.decode())
        # with open('query_data_count.html', 'w') as f:
        #     f.write(page1_ret.content.decode())
        h5_text = tree.xpath('//div[@class="ibox-content"]/h4/text()')
        if h5_text:
            count = int(h5_text[0].strip()[3:-8])
        else:
            count = 0
        return count

    def start_requests(self):
        cities = ['北京市', '深圳市', '上海市', '杭州市', '天津市', '武汉市', '南京市', '广州市',
                  '成都市', '苏州市', '无锡市', '重庆市', '西安市']

        city = '重庆市'
        month = ('', '')  #
        base_url = 'https://www.danke.com/admin/pangu/arm/contract/landlord-v3/list-es'
        params = {
            'city': city,
            'number': '',
            'suite_id': '',
            'elec_hire_v3_approve_status': '',
            'hand_over_approve_status': '',
            'address': '',
            'block_name': '',
            'dealer_name': '',
            'keeper_name': '',
            'landlord_id_name': '',
            'landlord_mobile': '',
            'sign_date-lower': month[0],
            'sign_date-upper': month[1],
            'start_date-lower': '',
            'start_date-upper': '',
            'type': '',
            'manage_status': '',
            'status': '',
            'stage': '',
            'first_payment_date-lower': '',
            'first_payment_date-upper': '',
            'all_rent_date-lower': '',
            'all_rent_date-upper': '',
            'end_date-lower': '',
            'end_date-upper': '',
            'has_measure': '',
            'page': ''
        }

        for page in range(1, 118):
            print('正在抓取 %s %d/%d 页' % (city, page, 117))
            params.update(page=str(page))
            url = base_url + '?' + urlencode(params)
            yield scrapy.Request(url, headers=self.headers,
                                 dont_filter=True,
                                 callback=self.parse_contract,
                                 cb_kwargs={
                                     'city': city,
                                     'month': month[0],
                                     'page': page
                                 })


    def parse_contract(self, response, **kwargs):
        city = kwargs['city']
        month = kwargs['month']
        page = kwargs['page']

        rows = response.xpath('//table[@class="table"]//tr')
        for row_index, row in enumerate(rows[1:]):
            contract_num = row.xpath('./td[1]//text()').getall()  # 合同编号
            contract_num = reduce(lambda x, y: x.strip() + y.strip(), contract_num)
            print('抓取到：%s %s 第%d页 条数：%d/%d %s' % (city, month, page, row_index + 1, len(rows[1:]), contract_num))

            detail_id = row.xpath('./td[1]/a/@href').get()  # detail_id
            detail_id = detail_id.split('/')[-1]

            seller = row.xpath('./td[2]/text()').get()  # 所属销售
            owner_name = row.xpath('./td[3]/text()').get()  # 业主姓名
            state = row.xpath('./td[4]//text()').getall()  # 状态
            if state:
                if len(state) == 1:
                    state = state[0].strip()
                else:
                    state = reduce(lambda x, y: x.strip() + ' ' + y.strip(), state)
            else:
                state = ''
            manage_state = row.xpath('./td[5]//text()').getall()  # 管理状态
            if manage_state:
                if len(manage_state) == 1:
                    manage_state = manage_state[0].strip()
                else:
                    manage_state = reduce(lambda x, y: x.strip() + ' ' + y.strip(), manage_state)
            else:
                manage_state = ''
            approval = row.xpath('./td[6]/span/text()').getall()  # 审核内容
            if approval:
                if len(approval) == 1:
                    approval = approval[0].strip().replace('&nbsp', '')
                else:
                    approvals = []
                    for item in approval:
                        clean_data = item.strip().replace('&nbsp', '')
                        approvals.append(clean_data)
                    approval = ' '.join(approvals)
            else:
                approval = ''
            pay_order = row.xpath('./td[7]//text()').getall()  # 付款单
            if pay_order:
                if len(pay_order) == 1:
                    pay_order = pay_order[0].strip()
                else:
                    pay_order = reduce(lambda x, y: x.strip() + ' ' + y.strip(), pay_order)
            else:
                pay_order = ''
            reward = row.xpath('./td[8]/text()').get()  # 收房签约奖励
            sign_date = row.xpath('./td[9]/text()').get()  # 签署日期
            rent_start_date = row.xpath('./td[10]/text()').get()  # 起租日期
            department_addr = row.xpath('./td[11]//text()').getall()  # 公寓地址
            if department_addr:
                if len(department_addr) == 1:
                    department_addr = department_addr[0].strip()
                else:
                    department_addr = reduce(lambda x, y: x.strip() + ' ' + y.strip(), department_addr)
            else:
                department_addr = ''
            item = ShoufangV3Contract()
            item['detail_id'] = detail_id
            item['city'] = city
            item['c_month'] = month
            item['page'] = page
            item['index'] = row_index
            item['contract_num'] = contract_num
            item['seller'] = seller
            item['owner_name'] = owner_name
            item['state'] = state
            item['manage_state'] = manage_state
            item['approval'] = approval
            item['pay_order'] = pay_order
            item['reward'] = reward
            item['sign_date'] = sign_date
            item['rent_start_date'] = rent_start_date
            item['department_addr'] = department_addr
            yield item
            # 业主手机号
            owner_url = 'https://www.danke.com/admin/pangu/arm/contract/landlord-v3/contract-info/{}'.format(detail_id)
            yield scrapy.Request(owner_url, headers=self.headers, dont_filter=True,
                                 callback=self.parse_detail,
                                 cb_kwargs={
                                     'detail_id': detail_id
                                 })

    def parse_detail(self, response, **kwargs):
        detail_id = kwargs['detail_id']
        owner_phone = response.xpath('//p[@id="lego-landlord_mobile"]/text()').get()
        if owner_phone:
            owner_phone = owner_phone.strip()
        if not owner_phone:
            owner_phone = response.xpath('//input[@id="lego-landlord_mobile"]/@value').get()
            if owner_phone:
                owner_phone = owner_phone.strip()

        urgency_phone = response.xpath('//p[@id="lego-urgencyMobile"]/text()').get()
        if urgency_phone:
            urgency_phone = urgency_phone.strip()
        if not urgency_phone:
            urgency_phone = response.xpath('//input[@id="lego-urgencyMobile"]/text()').get()
            if urgency_phone:
                urgency_phone = urgency_phone.strip()

        square = response.xpath('//p[@id="lego-area"]/text()').get()
        if square:
            square = square.strip()
        if not square:
            square = response.xpath('//input[@id="lego-area"]/@value').get()
            if square:
                square = square.strip()
        item = ShoufangV3DetailItem()
        item['detail_id'] = detail_id
        item['owner_phone'] = owner_phone
        item['urgency_phone'] = urgency_phone
        item['square'] = square
        yield item
