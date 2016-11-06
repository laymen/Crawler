# -*- coding: UTF-8 -*-

__author__ = 'Mouse'
import requests
import json
import re
import base64
import rsa
import binascii

agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}


def get_logininfo():
    preLogin_url = r'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&' \
                   r'su=&rsakt=mod&client=ssologin.js(v1.4.18)'
    html = requests.get(preLogin_url).text
    jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
    data = json.loads(jsonStr)
    servertime = data["servertime"]
    nonce = data["nonce"]
    pubkey = data["pubkey"]
    rsakv = data["rsakv"]
    return servertime, nonce, pubkey, rsakv


def get_su(username):
    """加密用户名，su为POST中的用户名字段"""
    su = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    return su


def get_sp(password, servertime, nonce, pubkey):
    pubkey = int(pubkey, 16)
    key = rsa.PublicKey(pubkey, 65537)
    # 以下拼接明文从js加密文件中得到
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    message = message.encode('utf-8')
    sp = rsa.encrypt(message, key)
    # 把二进制数据的每个字节转换成相应的2位十六进制表示形式。
    sp = binascii.b2a_hex(sp)
    return sp


def login(su, sp, servertime, nonce, rsakv):
    post_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        "pagerefer": "http://weibo.com/' + zhaoliying + '?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=' + str(1)",
        "vsnf": "1",
        "su": su,
        "service": "miniblog",
        "servertime": servertime,
        "nonce": nonce,
        "pwencode": "rsa2",
        "rsakv": rsakv,
        "sp": sp,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "prelt": "126",
        "url": "http://open.weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype": "META",
    }
    login_url = r'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    session = requests.Session()
    res = session.post(login_url, data=post_data, headers=headers)
    html = res.content.decode('gbk')

    info = re.findall(r"location\.replace\(\'(.*?)\'", html)[0]
    print(info)
    login_index = session.get(info, headers=headers)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    weibo_pa = r'<title>(.*?)</title>'
    userName = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    print('登陆成功，你的用户名为：'+userName)

    return session


#调用模拟登录的程序，从网页中抓取指定URL的数据，获取原始的HTML信息存入raw_html.txt中
def get_rawhtml(session, url):
    response = session.get(url)
    content = response.text
    print(content)
    #print "成功爬取指定网页源文件并且存入raw_html.txt"
    return content   #返回值为原始的HTML文件内容


def crawler(session, number, url):
    for n in range(number):
        n = n + 1
        url = 'http://weibo.com/' + url + '?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=' + str(n)
        print("crawler url", url)
        content = get_rawhtml(session, url)  # 调用获取网页源文件的函数执行
        print("page %d get success and write into raw_html.txt"%n)


def main_carwler(session, url, page_num):
    print("URL", url)
    crawler(session, page_num, url)   #调用函数开始爬取

if __name__ == '__main__':
    servertime, nonce, pubkey, rsakv = get_logininfo()
    print("servertime is :", servertime)
    print("nonce is :", nonce)
    print("pubkey is :", pubkey)
    print("rsakv is :", rsakv)
    name = input('请输入用户名：')
    su = get_su(name)
    password = input('请输入密码：')
    sp = get_sp(password, servertime, nonce, pubkey)
    session = login(su, sp, servertime, nonce, rsakv)
    print("session is ", session)

    weibo_url = "zhaoliying"
    main_carwler(session, weibo_url, 2)