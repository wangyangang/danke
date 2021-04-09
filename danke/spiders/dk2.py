import scrapy
import arrow
import os
import math
import requests
from lxml import etree
from urllib.parse import urlencode
from functools import reduce

from danke.items import ChufangContractItem, ChufangRenterItem, ChufangUrgencyItem


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


class DkSpider2(scrapy.Spider):
    name = 'dk2'
    allowed_domains = ['www.danke.com']
    headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36 DingTalk(6.0.0-macOS-14426516) nw Channel/201200',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'referer': 'https://www.danke.com/admin/pangu/arm/contract/landlord/list?page=5',
            # 'referer': 'https://www.danke.com/admin',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            # 'cookie': 'DK_SSO_TGC=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyMDE3LDEiLCJhdWQiOiJwaHBBZG1pbiIsImlhdCI6MTYxNTI5NDAxMH0.sQp2DhKP_vjNGXvemfaIqwSSt4zZBRZZvJ849irsDGc'
            # 'cookie': 'staff_user_info=%7B%22avatar%22%3A%22https%3A%2F%2Fstatic-legacy.dingtalk.com%2Fmedia%2FlADPDgQ9rWXRmFPNBDjNBDg_1080_1080.jpg%22%2C%22city%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22email%22%3A%22zhanglidong%40danke.com%22%2C%22expireTime%22%3A1615301210423%2C%22loginClientId%22%3A%22phpAdmin%22%2C%22loginTime%22%3A1615294010423%2C%22mobile%22%3A%2217319090902%22%2C%22name%22%3A%22%E5%BC%A0%E7%AB%8B%E5%86%AC%22%2C%22renewalSeconds%22%3A7200%2C%22uid%22%3A2017%2C%22userId%22%3A2017%2C%22userType%22%3A1%2C%22userTypeEnum%22%3A%22CORP_USER%22%7D'
            'cookie': 'SSO_SESSION_ID=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyMjA1LDEiLCJhdWQiOiJwaHBBZG1pbiIsImlhdCI6MTYxNTM4NjEyNH0.qYXJCEZpWQ6LmLL0xqQl_XYlI1hTBrc4YneiwPfotUk'
            # cookie: SSO_REFRESH_TOKEN=rXEoZDiqP7JT92r4C7sjDe_z7xjdfEhSd8Imea4mAPni6g4zXy2JZqbowolqaxo2TzED0eTxrvtjRiQX-0v23Q%3D%3D.635e97a2cd999c2b3655d05dd8340f04ab92e350ae651d68e497f803909b865f
            # cookie: XSRF-TOKEN=eyJpdiI6IjBReWJcL1F0VTRRTXBSWENlb0pCdzRRPT0iLCJ2YWx1ZSI6IjcyNGs2Z2hyN1g0MWJIa2hzdStTVDhZMzI3SEVsZjhlS3lmcjlDU0hjOUw5U0hsZlgyUUYxb3BiZDU4WDlZRVdNTlRXZnIwNDdFczE4SjBiazJ4TTBBPT0iLCJtYWMiOiIwNTNlZmM2ZmU4Y2M2Y2ExZmE2OTViMDk0MzgyZTM0YjQwZDU5NDBiZjk2YTZlMjM2ZjdjYjY4MjgzNGNmZTllIn0%3D
            # cookie: session=eyJpdiI6IlZGSzhvWkE4YiszNUJTTEJ4VHgwZXc9PSIsInZhbHVlIjoiNEEzVGh0aStHcVZncjVobnMxWmFaZTIxZ2FpY05MRndDSXRyWXZwYTNzWGoyN1NRY2dGVXJFQjN0d1dUOFFuTDRaRGl3dGFKbGlzTFhjQmoybUFIaWc9PSIsIm1hYyI6ImNiNTlkMGY0MzZiOGM3MDNhYTIzMzg3ZTZlZTJlMzQ0Y2JmNTIwYmM5YjA3NmE3YzgzN2U5NDA5ZDdlMjEzODkifQ%3D%3D'
        }

    def get_data_count(self, city, start_date, end_date):
        page1_url = 'https://www.danke.com/admin/pangu/arm/contract/customer-v4/list'
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
            'terminate_type': '',
            'ele_contract_status': '',
            'sign_source': '',
            'finance_entry_stage': '',
            'finance_business_stage': '',
            'finance_stage_is_pass': '',
            'contract_approve_status': '',
            'contract_approve_by_name': '',
            'ele_delivery_status': '',
            'delivery_approve_status': '',
            'delivery_approve_by_name': '',
            'monthly_pay_way': '',
            'payment_cycle': '',
            'rent_months': '',
            'end_date-lower': '',
            'end_date-upper': '',
            'previous_terminate_type': '',
            'subcompany_name': ''
        }
        page1_ret = requests.get(page1_url, headers=self.headers, params=params)
        # with open('page1.html', 'w') as f:
        #     f.write(page1_ret.content.decode())
        # 获取总数据量
        tree = etree.HTML(page1_ret.content.decode())
        h5_text = tree.xpath('//div[@class="ibox-content"]/h5/text()')[0]
        count = int(h5_text.strip()[4:-9])
        return count

    def start_requests(self):
        cities = ['北京市', '深圳市', '上海市', '杭州市', '天津市', '武汉市', '南京市', '广州市',
                  '成都市', '苏州市', '无锡市', '重庆市', '西安市']
        years = ['20' + str(item) for item in range(10, 20)]  # 10-19年有数据

        for city in cities:
            for year in years:
                months = getAllMonthPerYear(year)
                for start_date, end_date in months:
                    data_count = self.get_data_count(city, start_date, end_date)
                    print('%s %s %s 数据量: %d' % (city, start_date, end_date, data_count))
                    page_count = math.ceil(data_count / 50)
                    base_url = 'https://www.danke.com/admin/pangu/arm/contract/customer-v4/list'
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
                        'monthly_pay_way': '',
                        'rent_months': '',
                        'first_approve_by_name': '',
                        'end_date-lower': '',
                        'end_date-upper': '',
                        'previous_terminate_type': '',
                        'subcompany_name': '',
                        'page': ''
                    }

                    for page in range(1, page_count + 1):
                        print('正则抓取 %s %s %d/%d 页' % (city, start_date[:7], page, page_count))
                        params.update(page=str(page))
                        url = base_url + '?' + urlencode(params)
                        yield scrapy.Request(url, headers=self.headers,
                                             dont_filter=True,
                                             callback=self.parse_contract,
                                             cb_kwargs={
                                                'city': city,
                                                'start_date': start_date,
                                                'page': page
                                             })

    def parse_contract(self, response, **kwargs):
        city = kwargs['city']
        start_date = kwargs['start_date']
        page = kwargs['page']

        rows = response.xpath('//table[@class="table"]//tr')
        for row_index, row in enumerate(rows[1:]):
            contract_num = row.xpath('./td[1]//text()').getall()  # 合同编号
            contract_num = reduce(lambda x, y: x.strip() + y.strip(), contract_num)
            print('抓取到：%s %s 第%d页 条数：%d/%d %s' % (city, start_date, page, row_index + 1, len(rows[1:]), contract_num))

            detail_id = row.xpath('./td[1]/a/@href').get()  # detail_id
            detail_id = detail_id.split('/')[-1]

            department = row.xpath('./td[2]//text()').getall()  # 公寓
            department = reduce(lambda x, y: x.strip() + y.strip(), department)
            seller = row.xpath('./td[3]/text()').get()  # 所属销售
            approver = row.xpath('./td[4]/text()').get()  # 审批人
            business_circle = row.xpath('./td[5]/text()').get()  # 商圈
            maintainer = row.xpath('./td[6]/text()').get()  # 维护人
            renter = row.xpath('./td[7]//text()').getall()  # 租户
            if renter:
                renter = reduce(lambda x, y: x.strip() + ' ' + y.strip(), renter)
            else:
                renter = ''
            manage_state = row.xpath('./td[8]/span/text()').get()  # 管理状态
            approval = row.xpath('./td[9]/span/text()').getall()  # [审批]下架-资质-内容-物业交割
            approval = reduce(lambda x, y: x.strip() + ' ' + y.strip(), approval)
            state = row.xpath('./td[10]/span/text()').getall()  # 状态
            state = reduce(lambda x, y: x.strip() + ' ' + y.strip(), state)
            sign_reward_state = row.xpath('./td[11]/text()').get()  # 签约奖励付款状态
            monthly_pay_method = row.xpath('./td[12]/text()').get()  # 月付方式
            income_state = row.xpath('./td[13]/text()').get()  # 进件状态
            business_state = row.xpath('./td[14]/text()').get()  # 业务状态
            sign_date = row.xpath('./td[15]/text()').get()  # 签署日期
            rent_start_date = row.xpath('./td[16]/text()').get()  # 起租日期

            item = ChufangContractItem()
            item['detail_id'] = detail_id
            item['city'] = city
            item['start_date'] = start_date
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

            owner_url = 'https://www.danke.com/admin/pangu/arm/contract/customer/contract-user/{}'.format(detail_id)
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
        renter_mobile = response.xpath('//i[@class="fa fa-mobile"][1]/following-sibling::a[1]/text()').get()
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
        item = ChufangUrgencyItem()
        item['detail_id'] = detail_id
        item['phone'] = urgency_mobile
        yield item
