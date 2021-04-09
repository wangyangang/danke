# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoufangContract(scrapy.Item):
    name = 'shoufang_contract'
    # 合同基本信息

    detail_id = scrapy.Field()  # detail_id
    city = scrapy.Field()  # 城市
    c_month = scrapy.Field()  # 日期
    page = scrapy.Field()  # 第几页
    index = scrapy.Field()  # 在该页的位置

    contract_num = scrapy.Field()  # 合同编号
    seller = scrapy.Field()  # 所属销售
    maintainer = scrapy.Field()  # 维护人
    department = scrapy.Field()  # 公寓
    business_circle = scrapy.Field()  # 商圈
    owner_name = scrapy.Field()  # 业主姓名
    manage_state = scrapy.Field()  # 管理状态
    pay_order = scrapy.Field()  # 付款单
    reward = scrapy.Field()  # 收房奖励
    approval = scrapy.Field()  # 资质|内容审批
    state = scrapy.Field()  # 状态
    sign_date = scrapy.Field()  # 签署日期
    rent_start_date = scrapy.Field()  # 起租日期


class ShoufangOwnerItem(scrapy.Item):
    name = 'shoufang_owner'
    # 租户信息
    detail_id = scrapy.Field()  # detail_id
    phone = scrapy.Field()  # 租户电话


class ShoufangUrgencyItem(scrapy.Item):
    name = 'shoufang_urgency'
    # 紧急联系人信息
    detail_id = scrapy.Field()  # detail_id
    phone = scrapy.Field()  # 紧急联系人电话


class ShoufangDepartmentItem(scrapy.Item):
    name = 'shoufang_department'
    # 紧急联系人信息
    detail_id = scrapy.Field()  # detail_id
    square = scrapy.Field()  # 产证面积


class ShoufangV3Contract(scrapy.Item):
    name = 'shoufangv3_contract'
    # 合同基本信息

    detail_id = scrapy.Field()  # detail_id
    city = scrapy.Field()  # 城市
    c_month = scrapy.Field()  # 日期
    page = scrapy.Field()  # 第几页
    index = scrapy.Field()  # 在该页的位置

    contract_num = scrapy.Field()  # 合同编号
    seller = scrapy.Field()  # 所属销售
    owner_name = scrapy.Field()  # 业主姓名
    state = scrapy.Field()  # 状态
    manage_state = scrapy.Field()  # 管理状态
    approval = scrapy.Field()  # 审核内容
    pay_order = scrapy.Field()  # 付款单
    reward = scrapy.Field()  # 收房签约奖励
    sign_date = scrapy.Field()  # 签署日期
    rent_start_date = scrapy.Field()  # 起租日期
    department_addr = scrapy.Field()  # 公寓地址


class ShoufangV3DetailItem(scrapy.Item):
    name = 'shoufangv3_detail'
    detail_id = scrapy.Field()  # detail_id
    owner_phone = scrapy.Field()  # 业主电话
    urgency_phone = scrapy.Field()  # 紧急联系人电话
    square = scrapy.Field()  # 产证面积


class ChufangContractItem(scrapy.Item):
    name = 'chufang_contract'
    # 合同基本信息

    detail_id = scrapy.Field()  # detail_id
    city = scrapy.Field()  # 城市
    start_date = scrapy.Field()  # 日期
    page = scrapy.Field()  # 第几页
    index = scrapy.Field()  # 在该页的位置

    contract_num = scrapy.Field()  # 合同编号
    department = scrapy.Field()  # 公寓
    seller = scrapy.Field()  # 所属销售
    approver = scrapy.Field()  # 审批人
    business_circle = scrapy.Field()  # 商圈
    maintainer = scrapy.Field()  # 维护人
    renter = scrapy.Field()  # 租户
    manage_state = scrapy.Field()  # 管理状态
    approval = scrapy.Field()  # [审批]下架-资质-内容-物业交割
    state = scrapy.Field()  # 状态
    sign_reward_state = scrapy.Field()  # 签约奖励付款状态
    monthly_pay_method = scrapy.Field()  # 月付方式
    income_state = scrapy.Field()  # 进件状态
    business_state = scrapy.Field()  # 业务状态
    sign_date = scrapy.Field()  # 签署日期
    rent_start_date = scrapy.Field()  # 起租日期


class ChufangRenterItem(scrapy.Item):
    name = 'chufang_renter'
    # 租户信息
    detail_id = scrapy.Field()  # detail_id
    phone = scrapy.Field()  # 租户电话


class ChufangUrgencyItem(scrapy.Item):
    name = 'chufang_urgency'
    # 紧急联系人信息
    detail_id = scrapy.Field()  # detail_id
    phone = scrapy.Field()  # 紧急联系人电话
