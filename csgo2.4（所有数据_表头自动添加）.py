# -*- coding:utf-8 -*-
import time
import re
import os
import requests
from lxml import etree
import pandas as pd
from cookie_wenjian import cookies_shezhi
requests.packages.urllib3.disable_warnings()#忽略警告
number=["10000"]
# <editor-fold desc="常规设置">
localtime = time.localtime(time.time())
a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
nowtime = re.sub(':', '-', a)
str = ''
shangpin_list = ["蝴蝶 -StatTrak", "爪子 -StatTrak", "刺刀 -StatTrak", "折叠 -StatTrak", "锯齿 -StatTrak", "流浪者匕首 -StatTrak",
                "骷髅匕首 -StatTrak", "熊刀 -StatTrak", "短剑 -StatTrak", "弯刀 -StatTrak", "海豹短刀 -StatTrak", "折刀 -StatTrak",
                "穿肠刀 -StatTrak", "手套 久经", "裹手 久经", "USP -StatTrak", "格洛克", "沙漠之鹰 -StatTrak", "AK -StatTrak",
                "AWP -StatTrak", "A1 -StatTrak", "A4 -StatTrak"]
try:
    NMB = int(input("输入1是抓取所有(去除暗金），2是抓取指定的，3测试用："))
    if NMB ==1:
        shangpin=['-StatTrak']
    elif NMB ==2:
        shangpin = shangpin_list
    elif NMB ==3:
        shangpin = ['印花集 -StatTrak']
    else:
        print("输入有误，默认获取指定的商品")
        shangpin = shangpin_list
except:
    print("输入有误，默认获取指定的商品")
    shangpin = shangpin_list
pricemin = int(input("输入最低价格："))
threedaysjiaoyi = int(input("请输入三日最低交易量："))
jiange = float(input("请输入间隔时间："))
# </editor-fold>
cookies_shezhi = cookies_shezhi.replace(" ","")
headers = {
    "cookie":cookies_shezhi,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3880.400 QQBrowser/10.8.4554.400"
}
try:
    zanting = int(input("输入1是输出窗口会停留，2是不停留（默认不停留）:"))
except:
    zanting = "2"
url_id = "https://csspzn.com/pages/watchInfo.php?id="

def jiance(data):
    temp_number = 0
    for i in data:
        if i == '￥' or i == '¥'or i =='%'  or i =='':
            i = '无数据'
            data[temp_number] = i
            data.insert(temp_number,i)
        temp_number += 1
    return data



def geshi(last,name):
    global number
    last = str.join(last)
    re.sub('\s', ' ', last)
    jiaoyi = last.replace("\n", "").replace("\t", "")  # 合并列表中的元素，除去多余符号和空格
    jiaoyi = re.sub("3天", '', jiaoyi)
    number = re.sub("7天", '', jiaoyi)  # 删除多余数字
    number = re.findall("\d+", number)  # 查找交易量数字
    del number[0:2]  # 删除今日和昨日
    name.append(number[0])
    name.append(number[1])
    x = name
    x = jiance(x)
    del x[0]
    # print("删除前监测点",name)
    #判断C5价格有无  以及在售
    # 没有信息的情况下，没有在售数字，只有售价，这里就只删除售价就行了（IGEX相同）
    # if x[9] =='￥' and x[10]  == '￥':#IG C5都没有数据
    #     del x[10],x[-3]
    # else:
    #     if x[11] == '￥':# IG有数据C5没有
    #         del x[11],x[-3]#x[12] 删除C5在售价格  ，x[-3]删除C5时间
    #     else:#IG C5都有数据
    #         del x[11],x[11], x[-3]
    # if x[9] =='￥': #判断IGEX价格有无  以及在售
    #     del x[9]#删除IGEX售价
    #     del x[14]#删除IGEX时间
    #     del x[2], x[3]#短租长租删除年比率
    #     if x[5] == "￥0":
    #         x[5] = "1"
    #         x.insert(6, "1")
    #         print("修正结果",x)
    #     # print("x 网页数据更新在这里删数据", x)
    # else:
    #     del x[9],x[9]#删除IGEX售价和在售
    #     del x[14]#删除IGEX时间
    #     del x[2], x[3]#短租长租删除年比率
    #     if x[5] == "￥0":
    #         x[5] = "1"
    #         x.insert(6, "1")
    #         print("修正结果",x)
    # print("x 网页数据更新在这里删数据", x)
    return x

def get_page_source(url):                                       #拿取页面源代码
    resp = requests.get(url, headers=headers,verify=False)
    return resp.text

def sort_inf(lastjiaoyi):
    try:
        # print("交换顺序监测点1",lastjiaoyi)
        lastjiaoyi[0:14] = lastjiaoyi[0], lastjiaoyi[5], lastjiaoyi[7], lastjiaoyi[2], lastjiaoyi[4], lastjiaoyi[1], \
                           lastjiaoyi[3], lastjiaoyi[8], lastjiaoyi[12], lastjiaoyi[13], lastjiaoyi[6], lastjiaoyi[10], \
                           lastjiaoyi[11], lastjiaoyi[9]
        # 名字	短租比	长租比	短租价	长租价	BUFF售价	BUFF在售	悠悠有品售价	悠悠有品挂单数量	steam售价	BUFF更新时间	steam更新时间	三日租赁成交量	七日租赁成交量
        # print("三日交易",number[0])
        if int(number[0]) < threedaysjiaoyi:
            pass
        else:
            changzujia = lastjiaoyi[4]
            changzujia = re.sub('¥', '', changzujia)
            duanzujia = lastjiaoyi[6]
            duanzujia = re.sub('¥', '', duanzujia)
            buffjiage = lastjiaoyi[1]
            # print(lastjiaoyi)
            buffjiage = re.sub('￥', '', buffjiage)
            # print(duanzujia,changzujia,buffjiage)
            changzuhuibao = float((float(changzujia) * 21) / float(buffjiage))
            duanzuhuibaolv = float((float(duanzujia) * 15) / float(buffjiage))
            lastjiaoyi[3], lastjiaoyi[5] = changzuhuibao, duanzuhuibaolv
    except:
        # print("交换顺序监测点2", lastjiaoyi)
        lastjiaoyi[0:14] = lastjiaoyi[0], lastjiaoyi[5], lastjiaoyi[7], lastjiaoyi[2], lastjiaoyi[4], lastjiaoyi[1], \
                           lastjiaoyi[3], lastjiaoyi[8], lastjiaoyi[12], lastjiaoyi[13], lastjiaoyi[6], lastjiaoyi[10], \
                           lastjiaoyi[11], lastjiaoyi[
                               9]  # 名称	buff价格	uu价格	长租回报率	长租租金	短租回报率	短租租金	租赁供货数量	3日成交量	7日成交量	在售量	buff更新时间	steam更新时间	steam价格
        if int(number[0]) < threedaysjiaoyi:
            pass
        else:
            changzujia = lastjiaoyi[4]
            changzujia = re.sub('¥', '', changzujia)
            duanzujia = lastjiaoyi[6]
            duanzujia = re.sub('¥', '', duanzujia)
            uujiage = lastjiaoyi[2]
            # print(lastjiaoyi)
            uujiage = re.sub('￥', '', uujiage)
            # print(duanzujia,changzujia,buffjiage)
            changzuhuibao = float((float(changzujia) * 21) / float(uujiage))
            duanzuhuibaolv = float((float(duanzujia) * 15) / float(uujiage))
            lastjiaoyi[3], lastjiaoyi[5] = changzuhuibao, duanzuhuibaolv
    return lastjiaoyi


def parse_data(pgsource):               #拿到页面数据
    tree = etree.HTML(pgsource)
    tolist = tree.xpath('//*[@class="list-view-item"]')
    # print("监测点1",tolist)
    result = []
    for i in tolist:
        '''ids = i.xpath("./div[1]/@id")
        ids = ids[0].split("_")[1]
        resp_id = requests.get(url=(url_id + f"{ids}"), headers=headers, verify=False)
        resp_id = resp_id.text
        tree = etree.HTML(resp_id)
        linshi_baifenchangduanxinxi = tree.xpath('/html/body/p/font[@color="green"]/text()')
        linshi_baifenchangduanxinxi = linshi_baifenchangduanxinxi[0]
        obj = re.compile(r"短租:(?P<baifenduanzu>.*?\%).*?长租:(?P<baifenchangzu>.*?\%)")
        resultchangduan = obj.findall(linshi_baifenchangduanxinxi)
        duanbaifen = resultchangduan[0][0]
        changbaifen = resultchangduan[0][1]
        time.sleep(jiange)'''
        # print(i)
        name = i.xpath('./*//font/text()')
        # print("name监测点",name)
        jiaoyi = i.xpath('./div[@class="list-view-item-inner"]/div[@class="meta-left"]/span[@data-filter-match]/text()')
        # print("jiaoyi监测点",jiaoyi)
        lastjiaoyi = geshi(jiaoyi,name)     #格式化数据             name是商品信息
        # print("lastjiaoyi监测点",lastjiaoyi)
        result.append(lastjiaoyi)
    # print(lastjiaoyi)                         #[一条数据]
    return result

def main():
    global number
    # t_columns = ["Region", "Sequence Fragment", "Residues", "Length"]

    # form_head = [['名称', 'BUFF价格', 'UU价格', '长租回报率', '长租租金', '短租回报率', '短租租金', '租赁在售', '3日成交量', '7日成交量', 'BUFF在售量',
    #                'BUFF更新时间', 'STEAM更新时间', 'STEAM售价', '长租比', '短租比']]

    form_head =[['名字','短租比','年短租比','长租比','年长租比','短租价','长租价','BUFF','BUFF在售','IGEX','IGEX在售','C5','C5在售','悠悠','悠悠租赁中','STEAM','STEAM在售','BUFF更新时间','STEAM更新时间','IGXE更新时间','C5更新时间','今日','昨日','三日','七日']] #原始所有
    lst = []
    new_data = pd.DataFrame(form_head)
    lst.append(new_data)
    for shangpinname in shangpin:
        print(f"正在获取{shangpinname}")
        for pages in range(1, 500):
            # print("判断三日交易",threedaysjiaoyi)
            judgenumber=int(number[0])
            if judgenumber<threedaysjiaoyi:
                number = ["10000"]
                break
            # print("1处没有事情")                     #judgenumber
            url = f'https://csspzn.com/api/getAjax.php?/pages/items.php&T=&P=3%E6%97%A5%E4%BA%A4%E6%98%93%E9%87%8F%E2%86%93&PriceMin={pricemin}&PriceMax=&Name={shangpinname}&ST=All&TradesMin=&TradesMax=&page={pages}'
            a=get_page_source(url)      #获取页面源代码
            datalist=parse_data(a)      #解析
            if "无结果" in a:
                break
            # print(datalist)  # 拿到数据 [[一条数据],[一条数据]...]
            new_data = pd.DataFrame(datalist)
            lst.append(new_data)
    print("爬取完毕, 开始合并数据")

    df = pd.concat(objs=lst, axis=0,ignore_index=True)
    # print(df)
    # 保存数据
    df.to_excel(fr'.\csgo{nowtime}.xlsx')
    print("写入完毕")


if __name__=='__main__':
    main()
    # savepath = fr'csgo{nowtime}.xlsx'
    if zanting =='1':
        os.system('pause')
