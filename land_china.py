# -*- coding: utf-8 -*-
# @Time    : 2018/1/10 11:32
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : land_china.py
# @Software: PyCharm
import datetime
import re
import traceback
import logging
import requests
import time
from bs4 import BeautifulSoup
from land.LandCHina_gqf import sql
from io import StringIO

class Spider():
    def __init__(self):
        self.saves = sql.RuKu()
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
        self.url = 'http://www.landchina.com/default.aspx?tabid=263'
        self.postData = {'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                         'TAB_QuerySortItemList': '282:False',
                         # 日期
                         'TAB_QuerySubmitConditionData': '9f2c3acd-0256-4da2-a659-6949c4671a2a:',
                         'TAB_QuerySubmitOrderData': '282:False',
                         # 第几页
                         'TAB_QuerySubmitPagerData': ''}
        self.rowName = [u'行政区', u'电子监管号', u'项目名称', u'项目位置', u'面积(公顷)', u'土地来源', u'土地用途', u'供地方式', u'土地使用年限', u'行业分类',
                        u'土地级别', u'成交价格(万元)', u'土地使用权人', u'约定容积率下限', u'约定容积率上限', u'约定交地时间', u'约定开工时间', u'约定竣工时间',
                        u'实际开工时间', u'实际竣工时间', u'批准单位', u'合同签订日期']
        self.info = [
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl',  # 0
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl',  # 1
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl',  # 2
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl',  # 3
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl',  # 4
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl',  # 5
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl',  # 6
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl',  # 7
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl',  # 8
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl',  # 9
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl',  # 10
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl',  # 11
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c1_0_ctrl',
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c2_0_ctrl',
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c3_0_ctrl',
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c4_0_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl',  # 12
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r23_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl']


    def handleDate(self, year, month, day):
        # 返回日期数据
        'return date format %Y-%m-%d'
        date = datetime.date(year, month, day)
        #        print date.datetime.datetime.strftime('%Y-%m-%d')
        return date  # 日期对象

    def timeDelta(self, year, month):
        # 计算一个月有多少天
        date = datetime.date(year, month, 1)
        try:
            date2 = datetime.date(date.year, date.month + 1, date.day)
        except:
            date2 = datetime.date(date.year + 1, 1, date.day)
        dateDelta = (date2 - date).days
        return dateDelta

    def getPageContent(self, pageNum, date):
        # 指定日期和页数，打开对应网页，获取内容
        postData = self.postData.copy()
        # 设置搜索日期
        queryDate = date.strftime('%Y-%m-%d') + '~' + date.strftime('%Y-%m-%d')
        postData['TAB_QuerySubmitConditionData'] += queryDate
        # 设置页数
        postData['TAB_QuerySubmitPagerData'] = str(pageNum)
        # 请求网页
        try:
            r = requests.post(self.url, data=postData, timeout=10, headers=self.header)
            r.encoding = 'gb18030'
            pageContent = r.text
            #        f=open('content.html','w')
            #        f.write(content.encode('gb18030'))
            #        f.close()
            return pageContent
        except Exception as e:
            print(e)
            self.getPageContent(pageNum, date)

    def getAllNum(self, date):
        # 1无内容  2只有1页  3 1—200页  4 200页以上
        firstContent = self.getPageContent(1, date)
        if u'没有检索到相关数据' in firstContent:
            print(date, 'have', '0 page')
            return 0
        pattern = re.compile(u'<td.*?class="pager".*?>共(.*?)页.*?</td>')
        result = re.search(pattern, firstContent)
        if result == None:
            print(date, 'have', '1 page')
            return 1
        if int(result.group(1)) <= 200:
            print(date, 'have', int(result.group(1)), 'page')
            return int(result.group(1))
        else:
            print(date, 'have', '200 page')
            return 200
            # 第三步

    def getLinks(self, pageNum, date):
        'get all links'
        pageContent = self.getPageContent(pageNum, date)
        links = []
        pattern = re.compile(u'<a.*?href="default.aspx.*?tabid=386(.*?)".*?>', re.S)
        results = re.findall(pattern, pageContent)
        for result in results:
            links.append('http://www.landchina.com/default.aspx?tabid=386' + result)
        # print(links)  # 得到每一页的url
        return links

    def getAllLinks(self, allNum, date):
        pageNum = 1
        allLinks = []
        while pageNum <= allNum:
            links = self.getLinks(pageNum, date)
            allLinks += links
            print('scrapy link from page', pageNum, '/', allNum)
            pageNum += 1
        print(date, 'have', len(allLinks), 'link')
        return allLinks

    def getLinkContent(self, link):
        print(link)
        if self.saves.select(link) == 0:
            'open the link to get the linkContent'
            try:
                r = requests.get(link, timeout=30, headers=self.header)
                r.encoding = 'gb18030'
                linkContent = r
                return linkContent
            except Exception as e:
                pass
                f = open('error.txt', 'a', encoding='utf-8')
                f.write('%s\n' % e)
                f.close()
                logging.basicConfig(level=logging.WARNING,
                                    filename='log.txt',
                                    filemode='w',
                                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
                # use logging
                fp = StringIO()
                traceback.print_exc(file=fp)
                message = fp.getvalue()
                print(message)
                logging.error(message)

    def getInfo(self, linkContent):
        data = []
        try:
            soup = BeautifulSoup(linkContent.text, 'lxml')
            for item in self.info:
                if soup.find(id=item) == None:
                    s = ''
                else:

                    s = soup.find(id=item).text
                    if s == None:
                        s = ''
                data.append(s)
            self.saves.saves(data, linkContent.url)
            return data
        except Exception as e:
            f = open('errors.txt', 'a', encoding='utf-8')
            f.write('%s\n' % e)
            f.close()
            logging.basicConfig(level=logging.WARNING,
                                filename='log.txt',
                                filemode='w',
                                format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
            # use logging
            fp = StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            print(message)
            logging.error(message)

    def saveAllInfo(self, allLinks, date):
        for (i, link) in enumerate(allLinks):
            linkContent = data = None
            linkContent = self.getLinkContent(link)
            if linkContent:
                data = self.getInfo(linkContent)
                print('save info from link', i + 1, '/', len(allLinks))
