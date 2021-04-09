import scrapy
import os
import math
import requests
from lxml import etree
from urllib.parse import urlencode
from functools import reduce
import time
import random
import re

from danke.items import ChufangContractItem, ChufangRenterItem, ChufangUrgencyItem


class DkSpider(scrapy.Spider):
    name = 'chufang'
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
            # 'cookie': 'SSO_SESSION_ID=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyMjA1LDEiLCJhdWQiOiJwaHBBZG1pbiIsImlhdCI6MTYxNzgxNDE3MH0.npvUL3UD6ZAhy-OORoG8DXISaDWslUgk_mQ8j80pT3w'
            #'cookie': 'SSO_REFRESH_TOKEN=N_3BfY8WFwgofYjopW08W-_z7xjdfEhSd8Imea4mAPni6g4zXy2JZqbowolqaxo2lmeH4KLnHbk5_DH6vTqJmQ%3D%3D.5e1ce2b06ea310484708b2bbeed064a8834da04e64c7136f370cee4ffbaa71da',
            #'cookie': 'XSRF-TOKEN=eyJpdiI6IlkrSnV6VlwvWkplN3crVWhHVzN2V05BPT0iLCJ2YWx1ZSI6IlBpK2czRWs3SFhLZlViNTk1Z3BaYlwvK2dKczY2NDh6ZG9pRWIrVjVZN1pTOHRcL0xubm84R0V5TXJjZUNuS1MwZWN1QVpqZ0lEczNkcHlUemQrZU1DZWc9PSIsIm1hYyI6IjIwYmRjNjJjYjdlNzAxOThkNDcxMDI1YWQ4ZDJmMmRjMzZiODdiN2U3YTEwNzk5OTcyODY0ZTFjMGM2N2M5MmIifQ%3D%3D'
            #'cookie': 'session=eyJpdiI6IjR1VUJNOUNROGF3V0s4TFlWSkhkNGc9PSIsInZhbHVlIjoiZHpnVG0rZjlTSlwvdnNMSGF5cDhYZVBObEwzZ2tJamVDaEdheThsODhkM1ZJazJVVFlTNXM0ZWt5Z2ZUb3JwNm9YUk1LRmw5NkI3dWQwdDZvY1RtTnlnPT0iLCJtYWMiOiJkOGE2YjQ5ZWI2Mzc4MDVmZWMwYWMwNDNmZDJkYWFjM2JjNGE2YjlhOWRkNTIwNDI1YjgyNGMwNmNlYzllZjk0In0%3D'
        }

    def get_data_count(self, city, start_date, end_date):
        page1_url = 'https://www.danke.com/admin/pangu/arm/contract/customer/list'
        params = {
            'city_name': city,
            'number': '',
            'dealer_name': '',
            'keep_name': '',
            'suite_id': '',
            'id_name': '',
            'mobile': '',
            'sign_date-lower': start_date,
            'sign_date-upper': end_date,
            'manage_status': '',
            'status': '',
            'payment_cycle': '',
            'wuye_approve_status': '',
            'terminate_type': '',
            'ele_contract_status': '',
            'finance_entry_stage': '',
            'finance_business_stage': '',
            'finance_stage_is_pass': '',
            'sign_date-monthly_pay_way': '',
            'sign_date-rent_months': '',
            'first_approve_by_name': '',
            'end_date-lower': '',
            'end_date-upper': '',
            'previous_terminate_type': '',
            'subcompany_name': '',
        }
        self.headers.update(cookie=self.cookie)
        page1_ret = requests.get(page1_url, headers=self.headers, params=params)
        # with open('page1.html', 'w') as f:
        #     f.write(page1_ret.content.decode())
        # 获取总数据量
        tree = etree.HTML(page1_ret.content.decode())
        # with open('query_data_count.html', 'w') as f:
        #     f.write(page1_ret.content.decode())
        h5_text = tree.xpath('//div[@class="ibox-content"]/h4/text()')
        if h5_text:
            ret = re.findall(r'\d+\.?\d*', h5_text[0])
            if ret:
                count = int(ret[0])
        else:
            count = 0
        return count

    def start_requests(self):
        city = self.city
        sign_date_lower = self.sign_date_lower
        sign_date_upper = self.sign_date_upper

        data_count = self.get_data_count(city, sign_date_lower, sign_date_upper)
        print(data_count)
        page_count = math.ceil(data_count / 50)
        if page_count > 200:
            page_count = 200
        base_url = 'https://www.danke.com/admin/pangu/arm/contract/customer/list'
        params = {
            'city_name': city,
            'dealer_name': '',
            'ele_contract_status': '',
            'end_date-lower': '',
            'end_date-upper': '',
            'finance_business_stage': '',
            'finance_entry_stage': '',
            'finance_stage_is_pass': '',
            'first_approve_by_name': '',
            'id_name': '',
            'keep_name': '',
            'manage_status': '',
            'mobile': '',
            'monthly_pay_way': '',
            'number': '',
            'payment_cycle': '',
            'previous_terminate_type': '',
            'rent_months': '',
            'sign_date-lower': sign_date_lower,
            'sign_date-upper': sign_date_upper,
            'status': '',
            'subcompany_name': '',
            'suite_id': '',
            'terminate_type': '',
            'wuye_approve_status': '',
            'page': ''
        }

        for page in range(1, page_count + 1):
            print('正在抓取 %s %s %d/%d 页' % (city, sign_date_lower, page, page_count))
            params.update(page=str(page))
            url = base_url + '?' + urlencode(params)
            yield scrapy.Request(url, headers=self.headers,
                                 dont_filter=True,
                                 callback=self.parse_contract,
                                 cb_kwargs={
                                     'city': city,
                                     'month': sign_date_lower,
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

            department = row.xpath('./td[2]//text()').getall()  # 公寓
            if department:
                if len(department) == 1:
                    department = department[0].strip()
                else:
                    department = reduce(lambda x, y: x.strip() + ' ' + y.strip(), department)
            else:
                department = ''

            seller = row.xpath('./td[3]/text()').get()  # 所属销售
            approver = row.xpath('./td[4]/text()').get()  # 审批人
            business_circle = row.xpath('./td[5]/text()').get()  # 商圈
            maintainer = row.xpath('./td[6]/text()').get()  # 维护人
            renter = row.xpath('./td[7]//text()').getall()  # 租户
            if renter:
                if len(renter) == 1:
                    renter = renter[0].strip()
                else:
                    renter = reduce(lambda x, y: x.strip() + ' ' + y.strip(), renter)
            else:
                renter = ''

            manage_state = row.xpath('./td[8]//text()').get()  # 管理状态
            if manage_state:
                if len(manage_state) == 1:
                    manage_state = manage_state[0].strip()
                else:
                    manage_state = reduce(lambda x, y: x.strip() + ' ' + y.strip(), manage_state)
            else:
                manage_state = ''

            approval = row.xpath('./td[9]//text()').getall()  # [审批]下架-资质-内容-物业交割
            if approval:
                if len(approval) == 1:
                    approval = approval[0].strip()
                else:
                    approval = reduce(lambda x, y: x.strip() + ' ' + y.strip(), approval)
            else:
                approval = ''

            state = row.xpath('./td[10]//text()').getall()  # 状态
            if state:
                if len(state) == 1:
                    state = state[0].strip()
                else:
                    state = reduce(lambda x, y: x.strip() + ' ' + y.strip(), state)
            else:
                state = ''

            sign_reward_state = row.xpath('./td[11]/text()').get()  # 签约奖励付款状态
            monthly_pay_method = row.xpath('./td[12]/text()').get()  # 月付方式
            income_state = row.xpath('./td[13]/text()').get()  # 进件状态
            business_state = row.xpath('./td[14]/text()').get()  # 业务状态

            sign_date = row.xpath('./td[15]/text()').get()  # 签署日期
            rent_start_date = row.xpath('./td[16]/text()').get()  # 起租日期

            item = ChufangContractItem()
            item['detail_id'] = detail_id
            item['city'] = city
            item['start_date'] = month
            item['page'] = page
            item['index'] = row_index

            item['contract_num'] = contract_num
            item['department'] = department
            item['seller'] = seller
            item['approver'] = approver
            item['business_circle'] = business_circle
            item['maintainer'] = maintainer
            item['renter'] = renter
            item['manage_state'] = manage_state
            item['approval'] = approval
            item['state'] = state
            item['sign_reward_state'] = sign_reward_state
            item['monthly_pay_method'] = monthly_pay_method
            item['income_state'] = income_state
            item['business_state'] = business_state
            item['sign_date'] = sign_date
            item['rent_start_date'] = rent_start_date
            yield item
            # 租户手机号
            owner_url = 'https://www.danke.com/admin/pangu/arm/contract/customer/bind-customer/{}/customer'.format(detail_id)
            yield scrapy.Request(owner_url, headers=self.headers, dont_filter=True,
                                 callback=self.parse_renter,
                                 cb_kwargs={
                                     'detail_id': detail_id
                                 })

            urgency_url = 'https://www.danke.com/admin/pangu/arm/contract/customer/item/{}/urgency'.format(detail_id)
            yield scrapy.Request(urgency_url, headers=self.headers, dont_filter=True,
                                 callback=self.parse_urgency,
                                 cb_kwargs={
                                     'detail_id': detail_id
                                 })

    def parse_renter(self, response, **kwargs):
        detail_id = kwargs['detail_id']
        renter_mobile = response.xpath('//p[@id="lego-mobile"]/text()').get()
        if renter_mobile:
            renter_mobile = renter_mobile.strip()
        item = ChufangRenterItem()
        item['detail_id'] = detail_id
        item['phone'] = renter_mobile
        yield item

    def parse_urgency(self, response, **kwargs):
        detail_id = kwargs['detail_id']
        urgency_mobile = response.xpath('//p[@id="lego-urgencyMobile"]/text()').get()
        if urgency_mobile:
            urgency_mobile = urgency_mobile.strip()
        item = ChufangRenterItem()
        item['detail_id'] = detail_id
        item['phone'] = urgency_mobile
        yield item
