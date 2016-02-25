#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author: shaozhi.zhang
#Date: 2015/10/08
#Version: v20151008

import psycopg2
from functools import wraps 
import json
import requests 
from requests import Request, Session
from requests.auth import HTTPDigestAuth
import logging

logger = logging.FileHandler('bi.log')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setFormatter(formatter)

def formatSql(func):
    '''execute sql, fetchall and return data.'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        cursor = func(*args, **kwargs)
        table = kwargs.get('table') 
        ttype = kwargs.get('ttype')
        #format sql.
        if ttype == 0:
            sql = "select customer_id, name, email, mobile, register_platform, register_source, register_date from %s" % table
        elif ttype == 1:
            sql = "select order_id, customer_id, order_date, order_total_amount, order_real_amount, product_id, product_num, product_type, amount from %s" % table 

        #select table and fetchall data. 
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception, e:
            logger.info(e)
        return data 
    return wrapper

@formatSql
def conndb(host='127.0.0.1',
           dbname='',
           user='',
           password='',
           port=5432,
           table='',
           ttype=0):
    '''connection postgresql.'''

    #define our connection string.
    conn_string = "host='%s' dbname='%s' user='%s' password='%s' port=%d" % (host, dbname, user, password, port)

    try:
        #get a connection, if a connect cannot be made an exception will be raised here.
        conn = psycopg2.connect(conn_string)

        #conn.cursor will return a cursor object, you can use this cursor to perform queries. 
        cursor = conn.cursor()
    except Exception, e:
        logger.info(e)

    return cursor

def userParse(data):
    '''
    function: parser jzl_d_member table source data.
    example:
        ```
        {
            "customers": [
            {
                "customer_id": "3333",      //客户ID
                "name": "张三",             //客户姓名
                "email": "zhangsan@qq.com", //客户的注册邮箱
                "mobile": "1345678234",     //客户的注册手机
                “register_platform": 1,     //注册平台：1-PC 2-微信 3-IOS 4-安卓 5-WAP 6-其他
                "register_source": 1,       //注册来源：1: 手机号 2: Email 3: QQ 4: 新浪微博 5: 微信
                “register_date": "2013-08-07” //注册日期
            },
            {
                "customer_id": "4444",
                "name": "李四",
                "email": "lisi@qq.com",
                "mobile": "1345678234",
                “register_platform": 1,
                "register_source": 2,
                “register_date": "2013-08-07”
            }
            ]
        }
        ``` 
    '''
    #单个用户信息.
    member_dc={}
    #多个用户信息列表.
    member_ld=[]
    #完整的用户信息.
    user_dc={}
    for i in data:
        member_dc['customer_id'] = i[0]
        member_dc['name'] = i[1]
        member_dc['email'] = i[2]
        member_dc['mobile'] = i[3]
        member_dc['register_platform'] = i[4]
        member_dc['register_source'] = i[5]
        member_dc['register_date'] = i[6].strftime('%Y-%m-%d')
        member_ld.append(member_dc)
        member_dc={}
    user_dc['customers'] = member_ld 
    json_data = json.dumps(user_dc) 
    return json_data

def orderParse(data):
    '''
    function: parser jzl_f_order table source data.
    example:
      ```
       {
            "orders": [
                {
                    "order_id": 11111,          //订单ID
                    "customer_id": "3333",      //客户ID
                    "order_date": "2015-09-08",     //订单日期
                    "order_total_amount": 200.5,    //订单的金额（包含优惠劵等）
                    "order_real_amount": 190.5,     //订单的实际金额(客户实际支付的金额)
                    "products": [
                        {
                            "product_id": 2222, //商品ID
                            "product_num": 3,       //该商品在本次订单中的数量
                            "product_type": 1,      //商品类型(比如是否赠送商品)
                            "amount": 30.5          //该商品在本次订单中的金额
                        },
                        {
                            "product_id": 3333,
                            "product_num": 3,
                            "product_type": 2,
                            "amount": 99
                        }
                    ]
                },
                {
                    "order_id": 66666,
                    "customer_id": "3333",
                    "order_date": "2015-09-08",
                    "order_total_amount": 200.5,
                    "order_real_amount": 190.5,
                    "products": [
                        {
                            "product_id": 4444,
                            "product_num": 3,
                            "product_type": 1,
                            "amount": 30.5
                        },
                        {
                            "product_id": 5555,
                            "product_type": 1,
                            "product_num": 3,
                            "amount": 99
                        }
                    ]
                }
             ]
        }       
        ```
    '''
    #从postgresql中获取到的order 源数据.
    order_dc={} 
    #格式化完之后的订单数据.
    orders_dc={}
    orders_ld=[]
    #格式化完成的整体数据. 
    data_dc = {} 

    for i in data:
        if i[0] in order_dc:
            order_dc[i[0]].append(i)
        else:
            order_dc[i[0]]=[]
            order_dc[i[0]].append(i)
    #return order_dc
    for k, v in order_dc.iteritems():
        #同一个订单下的多个产品列表.
        products_ld=[]
        #同一个订单下的某一个产品信息.
        products_dc={}
        tmp_data = order_dc[k][0]
        orders_dc['order_id']=tmp_data[0]
        orders_dc['customer_id']=tmp_data[1]
        orders_dc['order_date']=tmp_data[2].strftime('%Y-%m-%d')
        orders_dc['order_total_amount']=float(tmp_data[3]) 
        orders_dc['order_real_amount']=float(tmp_data[4])
        for i in v:
            products_dc['product_id'] = i[5]
            products_dc['product_num'] = i[6]
            products_dc['product_type'] = i[7]
            products_dc['amount'] = float(i[8])
            products_ld.append(products_dc)
            products_dc={}
        orders_dc['products'] = products_ld
        orders_ld.append(orders_dc)
        orders_dc={}
    data_dc['orders'] = orders_ld   
    json_data = json.dumps(data_dc)
    return json_data 

def postInfo(data, post_type=0):
    '''
    function: user info and order info post to jiuzhilan.
    API url: 
        - https://api.pydevops.com/v1/user     #user info api interface. 
        - https://api.pydevops.com/v1/order    #order info api interface.

    post_type:
        - 0     #user info api interface.
        - 1     #order info api interface.
    '''

    chal = {
       'algorithm': 'MD5',
        'cnonce': '015b38c9119bbda5',
        'content-type': 'application/json',
        'nc': '00000001',
        'nonce': '1389832695:d3c620a9e645420228c5c7da7d228f8c',
        'qop': 'auth',
        'realm': 'api.pydevops.com',
        'response': '07f0d429dffed172f4751ecadd02e68e',
        'uri': '/sms/messages',
        'username': '+lw4CNmllLo=' 
    }
    if post_type == 0:
        try:
            r = requests.post('https://api.pydevops.com/v1/user', 
                              auth=HTTPDigestAuth('+lw4CNmllLo=', 'qmc7pMiSrQXo7Q+lx/6c0A=='),
                              verify='/data/bi/pydevops.com.pem',
                              headers=chal,
                              data=data)
            return r.text
        except Exception, e:
            logger.info(e)
            return '推送失败用户信息失败,请联系pydevops.com技术人员.'
    elif post_type == 1:
        try:
            r = requests.post('https://api.pydevops.com/v1/order',
                              auth=HTTPDigestAuth('+lw4CNmllLo=', 'qmc7pMiSrQXo7Q+lx/6c0A=='),
                              verify='/data/bi/pydevops.com.pem',
                              headers=chal,
                              data=data)
            return r.text
        except Exception, e:
            logger.info(e)
            return '推送订单信息失败,请联系pydevops技术人云.'
            
def main():
    '''
    function: main function.
    table:
        - jzl_d_member      user table.
        - jzl_f_order       order from table.
    ttype:
        - 0     jzl_d_member table data(user info).
        - 1     jzl_f_order table data(order from info).
    '''
    host='x.x.x.x'
    dbname='nicainicaibudao'
    user='nicainicaibudao'
    password='nicainicaibudao'
    port=5432

    #user data. 
    user_data = conndb(host=host, dbname=dbname, user=user, password=password, port=port, table='jzl_d_member', ttype=0)
    #order from data. 
    order_data = conndb(host=host, dbname=dbname, user=user, password=password, port=port, table='jzl_f_order', ttype=1)
    #user json data.
    user_json_data = userParse(user_data)
    #order json data.
    order_json_data = orderParse(order_data)
    print postInfo(user_json_data, post_type=0)

if __name__ == "__main__":
    main()
