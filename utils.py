"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   3/21/21 - 10:22 AM
"""
import requests
from lxml import etree


def get_data_count(city, start_date, end_date):
    page1_url = 'https://www.danke.com/admin/pangu/arm/contract/landlord/list'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36 DingTalk(6.0.0-macOS-14426516) nw Channel/201200',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'referer': 'https://www.danke.com/admin/pangu/arm/contract/landlord/list?page=5',
        # 'referer': 'https://www.danke.com/admin',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'DK_SSO_TGC=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyMjA1LDEiLCJhdWQiOiJwaHBBZG1pbiIsImlhdCI6MTYxNTcxMzA4M30.WPmL1bhGemZyAo_mKo5w9p5vIBGH2FXxNoK0UDMsxT4'
        # 'cookie': 'staff_user_info=%7B%22avatar%22%3A%22%22%2C%22city%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22email%22%3A%22chenzhihong%40danke.com%22%2C%22expireTime%22%3A1615720283827%2C%22loginClientId%22%3A%22phpAdmin%22%2C%22loginTime%22%3A1615713083827%2C%22mobile%22%3A%2217710342123%22%2C%22name%22%3A%22%E9%99%88%E6%B2%BB%E5%AE%8F%22%2C%22renewalSeconds%22%3A7200%2C%22uid%22%3A2205%2C%22userId%22%3A2205%2C%22userType%22%3A1%2C%22userTypeEnum%22%3A%22CORP_USER%22%7D'
        'cookie': 'SSO_SESSION_ID=eyJraWQiOiJzaW0wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIyNSwxIiwiYXVkIjoicGhwQWRtaW4iLCJpYXQiOjE2MTYyOTA3MzF9.hd4c5aCu0jyRKdEref6ozek2vyiBCvRtgHMAFMnFLk4'
        # 'cookie': 'SSO_REFRESH_TOKEN=N_3BfY8WFwgofYjopW08W-_z7xjdfEhSd8Imea4mAPni6g4zXy2JZqbowolqaxo2lmeH4KLnHbk5_DH6vTqJmQ%3D%3D.5e1ce2b06ea310484708b2bbeed064a8834da04e64c7136f370cee4ffbaa71da',
        # 'cookie': 'XSRF-TOKEN=eyJpdiI6IlkrSnV6VlwvWkplN3crVWhHVzN2V05BPT0iLCJ2YWx1ZSI6IlBpK2czRWs3SFhLZlViNTk1Z3BaYlwvK2dKczY2NDh6ZG9pRWIrVjVZN1pTOHRcL0xubm84R0V5TXJjZUNuS1MwZWN1QVpqZ0lEczNkcHlUemQrZU1DZWc9PSIsIm1hYyI6IjIwYmRjNjJjYjdlNzAxOThkNDcxMDI1YWQ4ZDJmMmRjMzZiODdiN2U3YTEwNzk5OTcyODY0ZTFjMGM2N2M5MmIifQ%3D%3D'
        # 'cookie': 'session=eyJpdiI6IjR1VUJNOUNROGF3V0s4TFlWSkhkNGc9PSIsInZhbHVlIjoiZHpnVG0rZjlTSlwvdnNMSGF5cDhYZVBObEwzZ2tJamVDaEdheThsODhkM1ZJazJVVFlTNXM0ZWt5Z2ZUb3JwNm9YUk1LRmw5NkI3dWQwdDZvY1RtTnlnPT0iLCJtYWMiOiJkOGE2YjQ5ZWI2Mzc4MDVmZWMwYWMwNDNmZDJkYWFjM2JjNGE2YjlhOWRkNTIwNDI1YjgyNGMwNmNlYzllZjk0In0%3D'
    }
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
    page1_ret = requests.get(page1_url, headers=headers, params=params)
    # with open('page1.html', 'w') as f:
    #     f.write(page1_ret.content.decode())
    # 获取总数据量
    tree = etree.HTML(page1_ret.content.decode())
    with open('query_data_count.html', 'w') as f:
        f.write(page1_ret.content.decode())
    h5_text = tree.xpath('//div[@class="ibox-content"]/h4/text()')
    if h5_text:
        count = int(h5_text[0].strip()[3:-8])
    else:
        count = -1
    return count


if __name__ == '__main__':
    count = get_data_count('北京市', '', '2016-12-31')
    print(count)