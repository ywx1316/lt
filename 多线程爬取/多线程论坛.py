from queue import Queue
from threading import Thread
import requests
from lxml import etree
import re
import random
import time


# 爬虫类
class CrawlInfo(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        userAgent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
            'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50']
        agent = random.choice(userAgent)
        header = {"User-Agent": agent}
        while self.url_queue.empty() == False:
            url = self.url_queue.get()
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                self.html_queue.put(response.text)


# 解析类
class ParseInfo(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while self.html_queue.empty() == False:
            e = etree.HTML(self.html_queue.get())
            # 标题
            titles = e.xpath('//a[@class="s xst"]/text()')
            # 帖子ID
            tzid_urls = e.xpath('//th/a[@href="javascript:;"]/@id')
            postsID = []
            for i in tzid_urls:
                ret = "".join(re.compile('\d', re.S).findall(i))
                postsID.append(ret)
                # 作者ID
            title = e.xpath('//td[@class="by"]/cite/a/@href')
            title_urls = [i for i in title if len(i) <= len(title[1])]
            authorsID = []
            for i in title_urls:
                res = "".join(re.compile('\d', re.S).findall(i))
                authorsID.append(res)
            with open('lt.txt', 'a', encoding='utf-8') as f:
                for bt, postID, authorID in zip(titles, postsID, authorsID):
                    # print(f'帖子ID：{postID}：{bt}，作者ID：{authorID}')
                    f.write(f'帖子ID：{postID}：{bt}，作者ID：{authorID}\n')


if __name__ == '__main__':
    # 存储url的容器
    url_queue = Queue()
    # 存储内容的容器
    html_queue = Queue()
    base_url1 = 'https://www.discuz.net/forum-developer-{}.html'
    base_url2 = 'https://www.dismall.com/forum-45-1.html'
    base_url3 = 'https://www.discuz.net/forum-2-{}.html'
    base_url4 = 'https://www.discuz.net/forum-flea-{}.html'
    base_url5 = 'https://www.discuz.net/forum-70-{}.html'
    for i in range(1, 21):
        new_url1 = base_url1.format(i)
        url_queue.put(new_url1)
        url_queue.put(base_url2)
    time.sleep(20)
    for i in range(1, 501):
        new_url2 = base_url3.format(i)
        url_queue.put(new_url2)
    time.sleep(20)
    for i in range(1, 55):
        new_url3 = base_url4.format(i)
        url_queue.put(new_url3)
    time.sleep(20)
    for i in range(1, 501):
        new_url4 = base_url5.format(i)
        url_queue.put(new_url4)
    print('爬取完成')

    # 创建一个爬虫
    crawl_list = []
    for i in range(0, 3):
        crawl1 = CrawlInfo(url_queue, html_queue)
        crawl_list.append(crawl1)
        crawl1.start()

    for crawl in crawl_list:
        crawl.join()
    parse_list = []
    for i in range(0, 3):
        parse = ParseInfo(html_queue)
        parse_list.append(parse)
        parse.start()
    for parse in parse_list:
        parse.join()
