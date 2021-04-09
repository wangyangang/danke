"""
@author:  wangyangang
@contact: wangyangang@wangyangang.com
@site:    https://wangyangang.com
@time:   3/21/21 - 3:17 PM
"""
import MySQLdb
import pandas as pd
import pymysql


def get_shoufang(city):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    passwd = '456wyg31'
    db = 'danke_shoufang'
    conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db)
    cursor = conn.cursor()
    # cursor.execute('set names utf8mb4')
    contract_sql = 'select detail_id, contract_num, seller, maintainer, department, business_circle, owner_name, ' \
                   'manage_state, pay_order, reward, approval, state, sign_date, rent_start_date ' \
                   'from shoufang_contract where city=%s'
    cursor.execute(contract_sql, (city,))
    contracts = cursor.fetchall()
    num = len(contracts)
    df_data = list()
    for contract_index, contract in enumerate(contracts):
        print('%d/%d' % (contract_index + 1, num))

        detail_id = contract[0]

        department_sql = 'select square from shoufang_department where detail_id=%s'
        cursor.execute(department_sql, (detail_id,))
        department = cursor.fetchone()
        square = department[0] if department else ''

        owner_sql = 'select phone from shoufang_owner where detail_id=%s'
        cursor.execute(owner_sql, (detail_id,))
        owner = cursor.fetchone()
        owner_phone = owner[0] if owner else ''

        urgency_sql = 'select phone from shoufang_urgency where detail_id=%s'
        cursor.execute(urgency_sql, (detail_id,))
        urgency = cursor.fetchone()
        urgency_phone = urgency[0] if urgency else ''

        df_data.append({
            'contract_num': contract[1],
            'seller': contract[2],
            'maintainer': contract[3],
            'department': contract[4],
            'business_circle': contract[5],
            'owner_name': contract[6],
            'manage_state': contract[7],
            'pay_order': contract[8],
            'reward': contract[9],
            'approval': contract[10].replace('&nbsp', ''),
            'state': contract[11],
            'sign_date': contract[12],
            'rent_start_date': contract[13],
            'owner_phone': owner_phone,
            'urgency_phone': urgency_phone,
            'square': square
        })

    df = pd.DataFrame(df_data)
    df.columns = ['合同编号', '所属销售', '维护人', '公寓', '商圈', '业主姓名', '管理状态', '付款单', '收房签约奖励',
                  '资质|内容审批', '状态', '签署日期', '起租日期', '业主电话', '紧急联系人电话', '产证面积']
    df.to_excel(city + '收房.xlsx', encoding='utf_8_sig', index=False)


def get_shoufangv3(city):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    passwd = '456wyg31'
    db = 'danke_shoufang'
    conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db)
    cursor = conn.cursor()
    # cursor.execute('set names utf8mb4')
    contract_sql = 'select detail_id, contract_num, seller, owner_name, state, ' \
                   'manage_state, approval, pay_order, reward, sign_date, rent_start_date, department_addr ' \
                   'from shoufangv3_contract where city=%s'
    cursor.execute(contract_sql, (city,))
    contracts = cursor.fetchall()
    num = len(contracts)
    df_data = list()
    for contract_index, contract in enumerate(contracts):
        print('%d/%d' % (contract_index + 1, num))

        detail_id = contract[0]

        detail_sql = 'select owner_phone, urgency_phone, square from shoufangv3_detail where detail_id=%s'
        cursor.execute(detail_sql, (detail_id,))
        detail = cursor.fetchone()

        df_data.append({
            'contract_num': contract[1],
            'seller': contract[2],
            'owner_name': contract[3],
            'state': contract[4],
            'manage_state': contract[5],
            'approval': contract[6],
            'pay_order': contract[7],
            'reward': contract[8],
            'sign_date': contract[9],
            'rent_start_date': contract[10],
            'department_addr': contract[11],
            'owner_phone': detail[0],
            'urgency_phone': detail[1],
            'square': detail[2]
        })

    df = pd.DataFrame(df_data)
    df.columns = ['合同编号', '所属销售', '业主姓名', '状态', '管理状态', '审核内容', '付款单',
                  '收房签约奖励', '签署日期', '起租日期', '公寓地址', '业主电话', '紧急联系人电话', '产证面积']
    df.to_excel(city + '收房v3.xlsx', encoding='utf_8_sig', index=False)


if __name__ == '__main__':
    cities = ['北京市', '深圳市', '上海市', '杭州市', '天津市', '武汉市', '南京市',
              '广州市', '成都市', '苏州市', '无锡市', '西安市', '重庆市']
    for city in cities:
        get_shoufangv3(city)