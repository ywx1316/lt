import requests
from lxml import etree
from bs4 import BeautifulSoup
import re

def html_get(url):
    headars = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}

    response = requests.get(url, headers=headars)
    e = etree.HTML(response.text)

    # 标题
    titles = e.xpath('//a[@class="s xst"]/text()')

    # 帖子ID
    tzid_urls=e.xpath('//th/a[@href="javascript:;"]/@id')
    postsID=[]
    for i in tzid_urls:
        ret="".join(re.compile('\d', re.S).findall(i))
        postsID.append(ret)

    # 作者ID
    title = e.xpath('//td[@class="by"]/cite/a/@href')
    title_urls=[i for i in title if len(i)<=len(title[1])]
    authorsID=[]
    for i in title_urls:
        res="".join(re.compile('\d', re.S).findall(i))
        authorsID.append(res)

    #with open('discuz_result.txt', 'a', encoding='utf-8') as f:    #保存到本地
    for bt,postID,authorID in zip(titles,postsID,authorsID):
        print(f'帖子ID：{postID}：{bt}，作者ID：{authorID}')
            #f.write(f'帖子ID：{postID}：{bt}，作者ID：{authorID}\n')


def main():
    for a in range(1,21):
        url=f'https://www.discuz.net/forum-developer-{a}.html'  #Discuz!-插件与模板交流
        url1='https://www.dismall.com/forum-45-1.html'        # 应用中心
        print(f'——————————————————正在爬取第{a}页——————————————————————')
        html_get(url)
        html_get(url1)
    # 后面速度过快会失败
    # for a in range(1,501):
    #     url2=f'https://www.discuz.net/forum-2-{a}.html'   # Discuzl-安装使用
    #     print(f'——————————————————正在爬取第{a}页——————————————————————')
    #     html_get(url2)
    # for a in range(1,55):
    #     url3 = f'https://www.discuz.net/forum-flea-{a}.html'  # 站长帮
    #     print(f'——————————————————正在爬取第{a}页——————————————————————')
    #     html_get(url3)
    # for a in range(1,501):
    #     url4=f'https://www.discuz.net/forum-70-{a}.html'   # Discuz!-BUG与问题交流
    #     print(f'——————————————————正在爬取第{a}页——————————————————————')
    #     html_get(url4)

if __name__ == '__main__':
    # 入口
    main()
