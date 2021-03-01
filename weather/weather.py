import requests
from bs4 import BeautifulSoup
import json
import csv
import re

#url = 'http://www.weather.com.cn/weather15d/101110101.shtml'

def gethtmltext(url):
    """请求获得网页内容"""
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url,headers = kv,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问")
        # print(r.request.headers)
        return r.text
    except:
        print("访问错误")
        return " "

def get_counent(html):
    """处理得到有用信息保存数据"""
    final = [] #初始化一个列表保存数据
    bs = BeautifulSoup(html, "html.parser") #创建BeautifuSoup对象
    body = bs.body
    data = body.find('div', {'id': '7d'})  #找到div标签且id = 7d

    #下面爬取当天数据
    text = bs.find_all(text = re.compile("observe24h_data")) #寻找有相关内容的标签里的内容
    wheather_data = str(text).lstrip(r"['\nvar observe24h_data = ").rstrip(r";\n")
    #转为字符串类型，去除非JSON格式数据(去头去尾)
    jd = json.loads(wheather_data)
    #print(json['od']['od2']) #字典的访问方式，前面两次词典套娃，后面套娃列表格式
    final_day = [] #存放当天数据
    count = 0
    for t in jd['od']['od2']:
        if count > 23:
            continue
        count += 1
        temp = [t['od21'], t['od22'], t['od23'], t['od24'], t['od25'], t['od26'], t['od27'], t['od28']]
        final_day.append(temp) #final_day 是一个以列表为元素的二维列表

    #下面爬取7天的数据
    ul = data.find('ul') #找到所有ul标签
    li = ul.find_all('li') # 找到左右的li标签
    i = 0 #控制爬取天数
    for day in li:   #遍历找到每一个li
        if i < 7 and i > 0: 
            temp = [] #临时存放每天的数据
            date = day.find('h1').string #得到日期
            date = date[0:date.index('日')] #取出日期号
            temp.append(date)
            inf = day.find_all('p') #找出li下面的p标签，提取第一个p标签，即天气
            temp.append(inf[0].string)

            tem_low = inf[1].find('i').striing #找到最低气温

            if inf[1].find('span') is None: #天气预报可能没有最高气温
                tem_high = None
            else:
                tem_high = inf[1].find('span').string #找到最高气温
            temp.append(tem_low[:-1])
            if tem_high[-1] == '℃':
                temp.append(tem_high[:-1])
            else:
                temp.append(tem_high)
            
            wind_scale = inf[2].find('i').string  #找到风级
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1 - 1:index1]))
            final.append(temp)

        i = i + 1
    return final_day, final

def get_content2(html):
    """处理得到有用信息保存数据文件"""
    bs = BeautifulSoup(html, "html.parser") #创建Beautifulsoup对象
    body = bs.body
    data = body.find('div', {'id':'15d'}) #找到div标签且id = 15d
    ul = data.find('ul') # 找到所有的ul标签
    li = ul.find_all('li') # 找到左右的ul标签
    final = [] #初始化一个列表保存数据
    i = 0  #控制爬取天数
    for day in li:  #遍历找到的每一个li
        if i < 8:
            temp = []#临时存放每天的数据
            date = day.find('span', {'class':'time'}).string #得到日期
            date = date[date.index('(') + 1:-2] #取出日期号
            temp.append(date)
            weather = day.find('span', {'class':'wea'}).string #找到天气
            temp.append(weather)
            tem = day.find('span',{'class':'tem'}).text #找到温度
            temp.append(tem[tem.index('/') + 1:-1]) #找到最低气温
            temp.append(tem[:tem.index('/') - 1]) #找到最高气温
            wind = day.find('span', {'class':'wind'}).string #找到风向
            if '转' in wind: #如果风有变化
                temp.append(wind[:wind.index('转')])
                temp.append(wind[wind.index('转') + 1：])
            else: #如果没有变化，前后风向一致
                temp.append(wind)
                temp.append(wind)
            wind_scale = day.find('span',{'class':'wind1'}).string # 找到风级
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1 - 1:index1]))

            final.append(temp)
    return final

def write_to_csv(file_name, data, day=14):
    """保存为csv文件"""