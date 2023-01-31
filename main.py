# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:32:11 2023

@author: Administrator
"""

import requests,re,time
import pandas as pd

Sess = requests.Session()
def get_top_zhuce_year(domian):
    print(domian)
    cookies = {
        'ASPSESSIONIDSSDSCTQR': 'KDJHLHCAEBDADPFENEOKLONI',
        'safedog-flow-item': '',
        'Hm_lvt_cd7ec33eb1c5bb5135d59f9ca8e86873': '1675139432',
        'Hm_lpvt_cd7ec33eb1c5bb5135d59f9ca8e86873': '1675139442',
    }
    
    headers = {
        'authority': 'www.nic.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.nic.top',
        'referer': 'https://www.nic.top/cn/support.asp?topdomain=bizha',
        'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
        'x-requested-with': 'XMLHttpRequest',
    }
    
    data = {
        'domainName': domian,
    }
    
    response = Sess.post('https://www.nic.top/cn/whoischeck.asp', cookies=cookies, headers=headers, data=data)
    try:
        creation_year = re.findall('Creation Date: (.*?)T', response.text)[0]
        creation_year = creation_year.split('-')[0] #注册年份
        expiry_year = re.findall('Expiry Date: (.*?)T', response.text)[0]
        expiry_year = expiry_year.split('-')[0] #到期年份
        zhuce_year = int(expiry_year) - int(creation_year) #注册年份
        print(zhuce_year)
        return zhuce_year
    except:
        if 'available' in response.text:
            print('available')
            return 'available'
        else:
            return '-'

def get_wang_zhuce_year(domian):
    print(domian)
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'http://nic.wang/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
    }
    
    params = {
        'domainName': '%s.wang'%domian,
        'callback': 'jsonp1675140599905',
    }
    
    response = Sess.get('http://whois.wang/whois/', params=params, headers=headers, verify=False)
    try:
        creation_year = re.findall('Creation Date: (.*?)T', response.text)[0]
        creation_year = creation_year.split('-')[0] #注册年份
        expiry_year = re.findall('Expiry Date: (.*?)T', response.text)[0]
        expiry_year = expiry_year.split('-')[0] #到期年份
        zhuce_year = int(expiry_year) - int(creation_year) #注册年份
        print(zhuce_year)
        return zhuce_year
    except:
        if 'exist' in response.text:
            print('available')
            return 'available'
        else:
            return '-'

def com_alexa_rank(domain):
    print(domain)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
    }
    
    params = {
        'cli': '10',
        'url': '%s.com'%domain,
    }
    
    response = Sess.get('http://data.alexa.com/data', params=params, headers=headers, verify=False)
    try:
        RANK = re.findall('RANK="(.*?)"', response.text)[0]
    except:
        RANK = '-'
    return RANK


def baidu_index_shoulu(domain):
    print(domain)
    url = 'https://index.baidu.com/api/SugApi/sug?inputword[]=%s&ischeckType=15'%domain
    sug_json = requests.get(url).json()
    sug_word = sug_json['data']['wordlist']
    if len(sug_word) ==0:
        return '未收录'
    sug_word = sug_json['data']['wordlist'][0]['name']
    if domain == sug_word:
        return '已收录'
    else:
        return '未收录'

shuangping_df = pd.read_excel('双拼.xlsx',sheet_name = 0)
#shuangping_df['com的alexa排名'] = shuangping_df['双拼'].apply(com_alexa_rank)
#shuangping_df['top注册时长'] = shuangping_df['双拼'].apply(get_top_zhuce_year)
#shuangping_df['wang注册时长'] = shuangping_df['双拼'].apply(get_wang_zhuce_year)
#shuangping_df['百度指数收录'] = shuangping_df['双拼'].apply(baidu_index_shoulu)
#shuangping_df.to_excel('shuangping_result1.xlsx')



