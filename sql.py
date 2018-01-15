# -*- coding: utf-8 -*-
# @Time    : 2018/1/10 17:46
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : sql.py
# @Software: PyCharm
import pymysql


class RuKu():

    def __init__(self):
        # self.conn = pymysql.connect(host='localhost', db='zy', user='root', passwd='123456', charset='utf8')
        self.cur = self.conn.cursor()
        if self.cur:
            print("连接成功")
        else:
            print("连接失败")

    def select(self, link):
        self.cur = self.conn.cursor()  # connection.cursor()：返回一个游标对象，该对象可以用于查询并从数据库中获取结果。
        a = "select count(1) from CHinaLand where Url='%s'" %(link)
        self.cur.execute(a)
        row = self.cur.fetchall()  # 将查询结果返回成一个元组（列表）
        print(row[0][0])
        return row[0][0]

    def saves(self, data, link):
        # print(link)
        # print(data[0] + '#行政区')
        # print(data[1] + '电子监管号')
        # print(data[2] + '项目名称')
        # print(data[3] + '项目位置')
        # print((data[4] + '面积(公顷)'))
        try:
            data[5]=self.Laiyuan(float(data[4]),float(data[5]))
        except:
            data[5] = '新增建设用地(来自存量库)'
        print(data[5]+'-------------------------------土地来源')
        # print(data[6] + '土地用途')
        # print(data[7] + '供地方式')
        # print(data[8] + '土地使用年限')
        # print(data[9] + '行业分类')
        # print(data[10] + '土地级别')
        # print(data[11] + '成交价格(万元)')
        # print(data[12] + '分期支付约定')
        # print(data[13] + '土地使用权人')
        # print(data[14] + '下限')
        # print(data[15] + '上限')
        # print(data[16] + '约定交地时间')
        # print(data[17] + '约定开工时间')
        # print(data[18] + '约定竣工时间')
        # print(data[19] + '实际开工时间')
        # print(data[20] + '实际竣工时间:')
        # print(data[21] + '批准单位:')
        # print(data[22] + '合同签订日期:')
        sql = "insert into CHinaLand(AdminRegion,ElectronicId,ProjectName,ProjectSeat,Acreage,LandSources,LandUse,LandSupply,LandUsageTerm,ClassificationIndustry,LandLevel,TransactionPrice,InstallmentPlan,LandUser,AgreedLimits,AgreedLimit,AgreedTime,ScheduledStartTime,ScheduledCompletionTime,ActualStartTime,ActualCompletionTime,Approvers,DateOfContract,Url) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19],data[20],data[21],data[22],link)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

    def Laiyuan(self,area,laiyuan):
        # area = str(area)
        # laiyuan = str(laiyuan)
        if area == laiyuan:
            return '现有建设用地'
        elif laiyuan ==0:
            return '新增建设用地'
        else:
            return '新增建设用地(来自存量库)'


# create table ChinaLand(ID int not null,AdminRegion varchar(255),ElectronicId varchar(255),ProjectName varchar(255),ProjectSeat varchar(255),Acreage varchar(255),LandSources varchar(255),LandUse varchar(255),LandSupply varchar(255),LandUsageTerm varchar(255),ClassificationIndustry varchar(255),LandLevel varchar(255),TransactionPrice varchar(255),InstallmentPlan varchar(255),LandUser varchar(255),AgreedLimits varchar(255),AgreedLimit varchar(255),AgreedTime varchar(255),ScheduledStartTime varchar(255),ScheduledCompletionTime varchar(255),ActualStartTime varchar(255),ActualCompletionTime varchar(255),Approvers varchar(255),DateOfContract varchar(255),CURRENT_TIME timestamp not null default current_timestamp,PRIMARY KEY (ID))




