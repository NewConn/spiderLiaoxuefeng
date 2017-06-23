# coding:utf-8
import requests

def getHtml(url):
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    r = requests.get(url, headers = head)
    r.raise_for_status()
    #r.encoding = r.apparent_encoding
    return r.text

domain = 'http://www.liaoxuefeng.com'           #廖雪峰的域名
path = r'E:\liaoxuefeng2\\'    #html要保存的路径
mainUrl = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
home = getHtml(mainUrl)

# 替换所有空格回车（这样容易好获取url）
geturl = home.replace("\n", "")
geturl = geturl.replace(" ", "")

# 得到包含url的字符串
list = geturl.split(r'em;"><ahref="')[1:]

# 强迫症犯了，一定要把第一个页面也加进去才完美
list.insert(0, '/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000">')

# 开始遍历url List
for li in list:
    url = li.split(r'">')[0]
    url = domain + url              #拼凑url
    html = getHtml(url)

    # 获得title为了写文件名
    title = html.split("<title>")[1]
    title = title.split(" - 廖雪峰的官方网站</title>")[0]

    # 要转一下码，不然加到路径里就悲剧了
    title = title.replace("/", " ")

    # 截取正文
    #html = html.split(r'<!-- block main -->')[1]
    html = html.split(r'<h4>您的支持是作者写作最大的动力！</h4>')[0]
    html = html.replace(r'src="', 'src="' + domain)

    # 加上头和尾组成完整的html
    html = "<html><body>" + html+"</body></html>"

    # 输出文件
    output = open(path + "%d" % list.index(li) + title + '.html', 'w')
    output.write(html)
    output.close()