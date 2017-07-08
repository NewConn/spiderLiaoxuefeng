# coding:utf-8
import requests
import time
import random
from bs4 import BeautifulSoup
import pdfkit
# import re
# import urllib.parse

def delay():
    delayTime = random.uniform(1, 3)
    time.sleep(delayTime)


def getHtml(url):
    #head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'isession=d2VpYm86MDAxNDkzOTMzNjk5MTM3ZjhiZDJiNTJlZjdjNDY0OWIwMTk2ZjQ0MmE5YjdkY2IwMDA6MTQ5ODI4MzUxMjg1Mjo1NmU3ODQ4NDlmYjFlZmVmZGM0ZmM4ZWZhMzM3MTRiYjIyZjlkOGMy',
            'DNT':'1',
            'Host':'www.liaoxuefeng.com',
            'Referer':'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }
    r = requests.get(url, headers = head)
    r.raise_for_status()
    #r.encoding = r.apparent_encoding
    return r


def parse_menu(response):
    # 解析目录结构,获取所有URL目录列表
    url_index = {}
    domain = r'http://www.liaoxuefeng.com'
    soup = BeautifulSoup(response.content, "html.parser")
    menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
    for li in menu_tag.find_all("li"):
        url = li.a.get("href")
        title = li.a.string
        title = title.replace('/', '_')
        url = domain + url
        url_index[title] = url
    return url_index

def parse_body(response):
    # 解析正文
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find_all(class_="x-wiki-content")[0]

    # 加入标题, 居中显示
    title = soup.find('h4').get_text()
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag('h1')
    title_tag.string = title
    center_tag.insert(1, title_tag)
    body.insert(1, center_tag)

    html = str(body)
    # body中的img标签的src相对路径的改成绝对路径
    pattern = "(<img .*?src=\")(.*?)(\")"
    # start_url = r'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
    # domain = '{uri.scheme}://{uri.netloc}'.format(uri=urllib.parse(start_url))
    # def func(m):
    #     if not m.group(2).startswith("http"):
    #         rtn = "".join([m.group(1), domain, m.group(2), m.group(3)])
    #         return rtn
    #     else:
    #         return "".join([m.group(1), m.group(2), m.group(3)])
    #
    # html = re.compile(pattern).sub(func, html)
    # html = html_template.format(content=html)
    html = html.encode("utf-8")
    return html


def save_PDF(htmls):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, "廖雪峰的Python.pdf", options=options)

def main():
    domain = 'http://www.liaoxuefeng.com'  # 廖雪峰的域名
    # path = r'E:\code\spiderLiaoxuefeng\save\\'  # html要保存的路径
    # path = r'/Users/newconn/Documents/PythonProjects/spiderLiaoxuefeng/save//'
    path = r'./save//'
    mainUrl = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
    home_page = getHtml(mainUrl)
    url_index = parse_menu(home_page)
    num = 0
    htmls = []
    for title, url in url_index.items():
        # delay()
        chapter = getHtml(url)
        html = parse_body(chapter)
        f_name = path + "%d" % num + title + '.html'
        num = num + 1
        with open(f_name, 'wb') as output:
            output.write(html)
        htmls.append(f_name)
    # save_PDF(htmls)
main()