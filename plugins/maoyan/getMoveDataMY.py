'''
Author: GoogTech
Date: 2021-01-02 17:22:43
LastEditTime: 2021-01-03 18:12:00
LastEditors: Please set LastEditors
Description: 获取猫眼今日票房排行榜、电影榜单
'''
import requests
from bs4 import BeautifulSoup

import sys
# 打印所有 python 解释器可以搜索到的所有路径
sys.path.append('../../')
# print(sys.path)
# 导入自定义包
from tools.ttsTool import *

# 请求头
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


class moviceDataMY(object):

    # 获取网页 html 内容
    @staticmethod
    def get_HTMLText(url):
        request = requests.get(url, headers=headers)
        request.encoding = request.apparent_encoding
        html_text = request.text
        return html_text

    # 获取猫眼今日票房排行榜
    @staticmethod
    def today_MoviceRanking():
        html =  moviceDataMY.get_HTMLText("https://maoyan.com/")
        soup = BeautifulSoup(html, 'lxml')
        topOne_movice_name = soup.find(
            'span', class_='ranking-top-moive-name')  # 获取排名第 1 的电影名称
        all_ranking_no = soup.find_all('i', class_='ranking-index')
        all_movice_name = soup.find_all('span', class_='ranking-movie-name')
        all_ranking_no_text, all_movice_name_text = ['1'], [
            topOne_movice_name.get_text()
        ]
        # 获取排行榜中的剩余的 4 部电影的排名编号及名称
        count = 0
        for no in all_ranking_no:
            if count < 4:
                count += 1
                all_ranking_no_text.append(no.get_text())
        count = 0
        for name in all_movice_name:
            if count < 4:
                count += 1
                all_movice_name_text.append(name.get_text())
        return all_ranking_no_text, all_movice_name_text

    #  格式化遍历输出今日票房排行榜
    @staticmethod
    def showData_Today_MoviceRanking():
        all_movice_no_text, all_movice_name_text = moviceDataMY.today_MoviceRanking(
        )
        # 存储数据, 用于语音播报
        forcast_txt = "以下播报的是猫眼今日票房排行榜 : \t\n"
        print('{}\t{:5}\t\n'.format('序号', '电影名称'))
        for i, j in zip(all_movice_no_text, all_movice_name_text):
            print('{}\t{:5}\t\n'.format(i, j))
            forcast_txt += '第{}名: \t{:5}。\t\n'.format(i, j)
        return forcast_txt

    # 获取天猫正在热映的电影口碑榜
    # 注: 有时候返回空数据即用不了, 因为猫眼会验证身份
    @staticmethod
    def movice_Ranking():
        datas = []
        html = moviceDataMY.get_HTMLText("https://maoyan.com/board")
        soup = BeautifulSoup(html, 'lxml')
        all_movice_no = soup.find_all('i', class_='board-index')  # 获取所有电影编号
        all_movice_name = soup.find_all('p', class_='name')  # 获取所有电影名称
        for movice_no, movice_name in zip(all_movice_no, all_movice_name):
            datas.append([movice_no.string, movice_name.a.string])
        return datas

    # 格式化遍历输出正在热映的电影口碑榜
    @staticmethod
    def showData_Movice_Ranking():
        datas = moviceDataMY.movice_Ranking()
        # 存储数据, 用于语音播报
        forcast_txt = "以下播报的是猫眼正在热映的排名前十的电影口碑榜 : \t\n"
        print('{}\t{:5}\t\n'.format('序号', '电影名称'))
        for i, j in datas:
            print('{}\t{:5}\t\n'.format(i, j))
            forcast_txt += '第{}名: \t{:5}。\t\n'.format(i, j)
        return forcast_txt

    # 运行获取天猫正在热映的电影数据的程序
    @staticmethod
    def run_movice_ranking():
        # 获取猫眼正在热映的排名前十的电影口碑榜数据
        datas = moviceDataMY.showData_Movice_Ranking()
        # 语音播报猫眼正在热映的排名前十的电影口碑榜, 最后将其文本数据推送到微信
        ttsToool.Voice_broadcast(forcast_txt=datas)
    
    # 运行获取猫眼今日票房排行榜数据的程序
    @staticmethod
    def run_today_movice_ranking():
        datas = moviceDataMY.showData_Today_MoviceRanking()
        ttsToool.Voice_broadcast(forcast_txt=datas)
        

"""2020 01 02 : 获取猫眼今日票房排行榜
序号    电影名称        

1       送你一朵小红花  

2       温暖的抱抱      

3       拆弹专家2       

4       心灵奇旅        

5       晴雅集
"""
