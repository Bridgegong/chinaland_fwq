# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 18:48
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : spider.py
# @Software: PyCharm
from land.LandCHina_gqf import land_china


def run_spider():
    s = land_china.Spider()
    year = 2017
    month = 1
    day = 3
    delta = s.timeDelta(year, month)
    #一个月一个月的抓取
    while day <= delta:
        #日期
        date = s.handleDate(year, month, day)
        #页数
        allNum = s.getAllNum(date)
        #链接
        allLinks = s.getAllLinks(allNum, date)
        #信息
        s.saveAllInfo(allLinks,date)
        day += 1
        print(date,'KO!')

    print(date.strftime('%Y-%m'),'KO!')

if __name__ == '__main__':
    run_spider()