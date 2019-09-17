# -*- decoding: utf-8 -*-
import json
import random
import re
import execjs
import requests


def getRandomAgent():
    USER_AGENTS = [
     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    return USER_AGENTS[random.randint(0,9)]

def get_umidToken_csrf_token(login_account):
    url='https://passport.aliexpress.com/mini_login.htm?lang=zh_cn&appName=aebuyer&appEntrance=default&styleType=auto&bizParams=&notLoadSsoView=false&notKeepLogin=true&isMobile=false&loginId=haoemax0%40126.com&cssLink=https://i.alicdn.com/noah-static/4.0.2/common/css/reset-havana.css&cssUrl=https://i.alicdn.com/noah-static/4.0.2/common/css/reset-havana-new-page.css&showMobilePwdLogin=false&defaultCountryCode=ES&ut=&rnd=0.9085151696364684'
    header = {
        'user-agent':getRandomAgent()
    }
    params={
    'lang':'zh_cn',
    'appName':'aebuyer',
    'appEntrance':'default',
    'styleType':'auto',
    'bizParams':'',
    'notLoadSsoView':'false',
    'notKeepLogin':'true',
    'isMobile':'false',
    'loginId':login_account,
    'cssLink':'https://i.alicdn.com/noah-static/4.0.2/common/css/reset-havana.css',
    'cssUrl':'https://i.alicdn.com/noah-static/4.0.2/common/css/reset-havana-new-page.css',
    'showMobilePwdLogin':'false',
    'defaultCountryCode':'ES',
    'rnd':'0.9085151696364684',
    }
    session=requests.session()
    response=session.get(url,headers = header,params=params)
    response_string=response.text.encode('utf-8').decode('utf-8', 'ignore')
    token_pattern=re.compile(r'window\.viewData\s+=\s+(.*?);')
    result=token_pattern.findall(response_string,re.S)
    resultJson=json.loads(result[0])
    return session,resultJson['loginFormData']['umidToken'],resultJson['loginFormData']['csrf_token']

def login(session,login_account,umidToken,csrf_token):
    url='https://passport.aliexpress.com/newlogin/login.do'
    params={
        'loginId': login_account,
        'password2': get_password2(password),
        'keepLogin': 'false',
        'ua': '120',
        'umidGetStatusVal': '255',
        'screenPixel': '1366x768',
        'navlanguage': 'zh - CN',
        'navUserAgent': getRandomAgent(),
        'navPlatform': 'Win32',
        'appEntrance': 'aebuyer',
        'appName': 'aebuyer',
        'csrf_token': csrf_token,
        'fromSite': '13',
        'hsiz': 'GyF - 5lyonGi1JrXAX__zwA',
        'isMobile': 'false',
        'lang': 'zh_CN',
        'mobile': 'false',
        'umidToken': umidToken,
    }
    header = {
        'user-agent':getRandomAgent()
    }
    response=session.post(url,params=params,headers=header)
    return response.status_code

def get_password2(password):
    with open('testjs3.js','r',errors='ignore') as f:
        js_code=f.read()
    ctx=execjs.compile(js_code)
    return ctx.call("getPwd",password)

def checkLogin():
    loginUrl='https://myae.aliexpress.com/seller/account/accountPortal.htm?'
    header={
        'user-agent': getRandomAgent()
    }
    response=session.get(loginUrl,headers=header)
    if response.status_code == 200:
        print("登录成功！")
        print(response.text.encode("gbk",errors='ignore').decode("utf-8",errors='ignore'))
    else:
        print("登录失败！")


login_account='haoemax0@126.com'
password='tommycool999'
session,umidToken,csrf_token=get_umidToken_csrf_token(login_account)
checkLogin()
