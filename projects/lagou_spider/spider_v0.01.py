#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 20:18:55 2018

@author: xujq

create database jobs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

"""

import requests
import time
from sqlalchemy import create_engine
import pandas as pd
from random import choice
import json
import numpy as np
import pymysql as pmq
import sqlalchemy
import random


#connection = pmq.connect(host='127.0.0.1',
#                             port=3306,
#                             user='root',
#                             password='1881128xx',
#                             db='jobs',
#                             charset='utf8',
#                             cursorclass=pmq.cursors.DictCursor)

#with connection.cursor() as cursor:
#    sql = 'INSERT INTO test (c1, c2) VALUES (%s, %s)'
#    cursor.execute(sql, ('Robin', 'Zhyea'))
#connection.commit()

connection = sqlalchemy.create_engine('mysql+mysqldb://root:1881128xx@127.0.0.1:3306/jobs?charset=utf8')    

def get_header():
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?px=default&city=%E6%B7%B1%E5%9C%B3&district=%E5%8D%97%E5%B1%B1%E5%8C%BA",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.lagou.com",
        "Connection":"keep-alive",
        "Cookie":"user_trace_token=20160214102121-0be42521e365477ba08bd330fd2c9c72; LGUID=20160214102122-a3b749ae-d2c1-11e5-8a48-525400f775ce; tencentSig=9579373568; pgv_pvi=3712577536; index_location_city=%E5%85%A8%E5%9B%BD; SEARCH_ID=c684c55390a84fe5bd7b62bf1754b900; JSESSIONID=8C779B1311176D4D6B74AF3CE40CE5F2; TG-TRACK-CODE=index_hotjob; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1485318435,1485338972,1485393674,1485423558; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1485423598; _ga=GA1.2.1996921784.1455416480; LGRID=20170126174002-691cb0a5-e3ab-11e6-bdc0-525400f775ce",
        "Origin": "https://www.lagou.com",
        "Upgrade-Insecure-Requests":"1",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
        }
    return (headers)

def get_form(page_number,kd = "数据分析师"):
    data={"first":"false","pn":page_number,"kd":kd}
    return(data)
    
    
def format_tool(piece_data):
    if type(piece_data) == list:
        data = ",".join(piece_data)
    elif type(piece_data) == str:
        data = piece_data
    elif piece_data is None:
        data = ''
    else:
        data = piece_data
    return data
        


s = requests.Session()
s.keep_alive = False
s.adapters.DEFAULT_RETRIES = 10

url = "https://www.lagou.com/jobs/positionAjax.json?city=上海"
pages = (1,100)

for page_number in range(pages[0],pages[1]):
    print("pages : %i"%page_number)
    resp=s.post(url, data=get_form(page_number), headers=get_header())
    resp.encoding="utf-8"
    txt = resp.text
    page_data=json.loads(resp.text)["content"]["positionResult"]["result"]
    info_len = len(page_data)
    df = pd.DataFrame()
    for list_num in range(info_len):
        json_data = page_data[list_num]
        print(json_data["companyFullName"])
        tmps = pd.Series(dict(
            approve=format_tool(json_data["approve"]),
            businessZones = format_tool(json_data["businessZones"]),
            companyId = format_tool(json_data["companyId"]),
            companyLabelList=format_tool(json_data["companyLabelList"]),
            companyShortName = format_tool(json_data["companyShortName"]),
            companySize = format_tool(json_data["companySize"]),
            createTime = format_tool(json_data["createTime"]),
            education = format_tool(json_data["education"]),
            financeStage = format_tool(json_data["financeStage"]),
            firstType = format_tool(json_data["firstType"]),
            industryField = format_tool(json_data["industryField"]),
            jobNature = format_tool(json_data["jobNature"]),
            positionAdvantage = format_tool(json_data["positionAdvantage"]),
            positionId = format_tool(json_data["positionId"]),
            positionName = format_tool(json_data["positionName"]),
            city = format_tool(json_data["city"]),
            salary = format_tool(json_data["salary"]),
            secondType = format_tool(json_data["secondType"]),
            workYear = format_tool(json_data["workYear"]),
            district = format_tool(json_data["district"]),
            score = format_tool(json_data["score"]),
            publisherId = format_tool(json_data["publisherId"]),
            positionLables = format_tool(json_data["positionLables"]),
            industryLables = format_tool(json_data["industryLables"]),
            imState = format_tool(json_data["imState"]),
            companyFullName = format_tool(json_data["companyFullName"]),
            subwayline = format_tool(json_data["subwayline"]),
            stationname = format_tool(json_data["stationname"]),
            linestaion = format_tool(json_data["linestaion"]),
            longitude = format_tool(json_data["longitude"]),
            latitude = format_tool(json_data["latitude"]),
            scrapy_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        df = pd.concat([df,tmps],axis=1)
    df = df.T
    df.reset_index(inplace=True,drop=True)
    df.to_sql(con = connection, name = "job_info", if_exists = 'append',index=False)
    time.sleep(3+random.random()*5)
    


