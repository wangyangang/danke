from itemadapter import ItemAdapter
import warnings
import sqlite3
import pandas as pd
import os


class ChufangPipeline:
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        dbname = settings['DBNAME']
        if not dbname.strip():
            raise ValueError('no database name!')
        self.settings = settings
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):
        dbname = spider.name
        spider.cookie = self.settings['COOKIE']
        spider.city = self.settings['CITY']
        spider.sign_date_lower = self.settings['SIGN_DATE_LOWER']
        spider.sign_date_upper = self.settings['SIGN_DATE_UPPER']
        self.init_database(dbname)

    def init_database(self, dbname):
        warnings.filterwarnings('ignore', message=".*exists.*")
        warnings.filterwarnings('ignore', message=".*looks like a.*")
        file_name = 'init_db.sql'
        # file_name = os.path.join(os.path.dirname(os.getcwd()), 'init_db.sql')
        with open(file_name, 'r', True, 'utf-8') as f:
            sql = f.read()
            self.cursor.executescript(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.insert(item)
        except Exception as e:
            print('保存失败-------------')
            print(e)
            print(item)
        return item

    def insert(self, item):
        maps = {
            'chufang_contract': self.insert_contract,
            'chufang_renter': self.insert_renter,
            'chufang_urgency': self.insert_urgency
        }
        func = maps[item.name]
        try:
            func(item)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def insert_contract(self, item):
        sql = 'insert into chufang_contract(detail_id, city, start_date, page, _index, contract_num,' \
              'department, seller, approver, business_circle, maintainer, renter, manage_state,' \
              'approval, state, sign_reward_state, monthly_pay_method, income_state, business_state,' \
              'sign_date, rent_start_date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?, ?, ?, ?)'
        params = (item['detail_id'], item['city'], item['start_date'], item['page'], item['index'], item['contract_num'],
                  item['department'], item['seller'], item['approver'], item['business_circle'], item['maintainer'], item['renter'], item['manage_state'],
                  item['approval'], item['state'], item['sign_reward_state'], item['monthly_pay_method'], item['income_state'], item['business_state'],
                  item['sign_date'], item['rent_start_date'])
        self.cursor.execute(sql, params)

    def insert_renter(self, item):
        sql = 'insert into chufang_renter(detail_id, phone) values (?, ?)'
        params = (item['detail_id'], item['phone'])
        self.cursor.execute(sql, params)

    def insert_urgency(self, item):
        sql = 'insert into chufang_urgency(detail_id, phone) values (?, ?)'
        params = (item['detail_id'], item['phone'])
        self.cursor.execute(sql, params)

    def close_spider(self, spider):
        # 保存数据到csv
        print('正在保存数据。。。')
        city = self.settings['CITY']
        sign_date_lower = self.settings['SIGN_DATE_LOWER']
        sign_date_upper = self.settings['SIGN_DATE_UPPER']

        sql = 'select detail_id, contract_num, department, seller, approver, business_circle, maintainer, ' \
              'renter, manage_state, approval, state, sign_reward_state, monthly_pay_method, ' \
              'income_state, business_state, sign_date, rent_start_date from chufang_contract ' \
              'where city=? and start_date=? order by page, _index'
        params = (city, sign_date_lower)
        self.cursor.execute(sql, params)
        contracts = self.cursor.fetchall()
        df_data = list()
        num = len(contracts)
        print('共%d条' % num)
        for contract_index, contract in enumerate(contracts):
            detail_id = contract[0]
            renter_sql = 'select phone from chufang_renter where detail_id=?'
            self.cursor.execute(renter_sql, (detail_id,))
            renter = self.cursor.fetchone()

            urgency_sql = 'select phone from chufang_urgency where detail_id=?'
            self.cursor.execute(urgency_sql, (detail_id,))
            urgency = self.cursor.fetchone()

            df_data.append({
                'contract_num': contract[1],
                'department': contract[2],
                'seller': contract[3],
                'approver': contract[4],
                'business_circle': contract[5],
                'maintainer': contract[6],
                'renter': contract[7],
                'manage_state': contract[8],
                'approval': contract[9],
                'state': contract[10],
                'sign_reward_state': contract[11],
                'monthly_pay_method': contract[12],
                'income_state': contract[13],
                'business_state': contract[14],
                'sign_date': contract[15],
                'rent_start_date': contract[16],
                'renter_phone': renter[0] if renter else '',
                'urgency_phone': urgency[0] if urgency else ''
            })
        if df_data:
            file_name = city + '-' + sign_date_lower + '-' + sign_date_upper + '.xlsx'
            df = pd.DataFrame(df_data)
            df.columns = ['合同编号', '公寓', '所属销售', '审批人', '商圈', '维护人', '租户', '管理状态',
                          '审批', '状态', '签约奖励付款状态', '月付方式', '进件状态',
                          '业务状态', '签署日期', '起租日期', '租户手机号', '紧急联系人手机号']
            df.to_excel(file_name, index=False)
            print('保存完毕, 文件名：%s' % file_name)




