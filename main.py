import requests
import re
import time
import leancloud
from leancloud import Object
import numpy as np
import matplotlib.pyplot as plt
import urllib
import pylab

cookies_str = '__cfduid=db094ef2f3beedc20886b275d7b63562c1471265946; tjpctrl=1471444728281; fDyj_2132_saltkey=UwpNz3YN; fDyj_2132_lastvisit=1471439439; fDyj_2132_sendmail=1; Hm_lvt_ef6071de284645b5fb2dee7870f09876=1471265950; Hm_lpvt_ef6071de284645b5fb2dee7870f09876=1471443041; fDyj_2132_lastact=1471443070%09member.php%09logging; fDyj_2132_ulastactivity=c7b927rhUdTCy4D9lAZZU1etnuzgT2U3B2qlZSXrCcRQt4R%2FEt1H; fDyj_2132_sid=oSaHL6; fDyj_2132_auth=fca8RdT77ViEyzQ1VWJnhM1M43mpSmV21wScIoNWGAyGvNWFZ%2FghoJSrYGzk8sm%2B5Va169x2KFNgtrQUzx93bPw9uA; fDyj_2132_lastcheckfeed=63340%7C1471443070; fDyj_2132_checkfollow=1; fDyj_2132_lip=108.162.215.202%2C1471442736'
cookies_list = cookies_str.split(';')
cookies = {}
for each in cookies_list:
    each = each.strip().split('=')
    cookies[each[0]] = each[1]

print(cookies)

class MZObject(Object):
    pass

def get_detail(url):
    try:
        content = requests.get(url, timeout=60, cookies=cookies).text
    except:
        time.sleep(2)
        try:
            content = requests.get(url, timeout=60, cookies=cookies).text
        except:
            content = ''
            print(url + u'出错！')
    if content == '':
        return

    try:
        content = str(content)
    except:
        print('解析出错！')
        return
    # print(content)

    title = re.findall(u'<title>(.*?)</title>', content, re.S)
    if len(title) != 0:
        title = title[0].strip()

    position = re.findall(u'<th>地点:</th>(.*?)</td>', content, re.S)
    if len(position) != 0:
        position = position[0][6:].strip()

    name = re.findall(u'<th>姓名:</th>(.*?)</td>', content, re.S)
    if len(name) != 0:
        name = name[0][6:].strip()

    age = re.findall(u'<th>年龄:</th>(.*?)</td>', content, re.S)
    if len(age) != 0:
        age = age[0][6:].strip()

    height = re.findall(u'<th>身高:</th>(.*?)</td>', content, re.S)
    if len(height) != 0:
        height = height[0][6:].strip()

    items = re.findall(u'<th>项目:</th>(.*?)</td>', content, re.S)
    if len(items) != 0:
        items = items[0][6:].strip()

    cost = re.findall(u'<th>花费:</th>(.*?)</td>', content, re.S)
    if len(cost) != 0:
        cost = cost[0][6:].strip()

    # description = re.findall(u'id="postmessage_\d+">(.*?)</table>', content, re.S)
    # if len(description) != 0:
    #     description = description[0][6:]

    print(title, '\n', position, '\n', name, '\n', age, '\n', height, '\n', items, '\n', cost, '\n', url)
    try:
        mz = MZObject()
        mz.set('title', title)
        mz.set('name', name)
        mz.set('position', position)
        mz.set('age', age)
        mz.set('height', height)
        mz.set('items', items)
        mz.set('cost', cost)
        mz.set('url', url)
        mz.save()
    except:
        time.sleep(2)
        try:
            mz = MZObject()
            mz.set('title', title)
            mz.set('name', name)
            mz.set('position', position)
            mz.set('age', age)
            mz.set('height', height)
            mz.set('items', items)
            mz.set('cost', cost)
            mz.set('url', url)
            mz.save()
        except leancloud.LeanCloudError as e:
            print(e)
            print('SAVE ERROR!')


def get_detail_num(url):
    try:
        index_content = requests.get(url, timeout=60, cookies=cookies).text
    except:
        time.sleep(2)
        try:
            index_content = requests.get(url, timeout=60, cookies=cookies).text
        except:
            index_content = ''
            print(url + u'出错！')
    if index_content == '':
        return
    try:
        index_content = str(index_content)
    except:
        print('解析出错！')
        return
    # print(index_content)
    page_nums = re.findall('onclick="previewThread\(\'(.*?)\', \'normalthread', index_content)
    return page_nums


def main():
    i = 1
    for ii in range(104):
        ss = str(ii + 1)
        index_url = 'http://www.xianchawang.info/forum-40-' + ss + '.html'
        page_nums = get_detail_num(index_url)
        # print(page_nums)
        for num in page_nums:
            print(i)
            detail_url = 'http://www.xianchawang.info/thread-' + num + '-1-1.html'
            detail_url2 = 'http://www.xianchawang.org/thread-' + num + '-1-1.html'
            i += 1
            query_list = query.equal_to('url', detail_url).find()
            query_list2 = query.equal_to('url', detail_url2).find()
            if len(query_list) + len(query_list2) > 0:
                continue

            get_detail(detail_url)
            print('\n')

filter_list = [u'北京', u'朝阳', u'海淀', u'丰台', u'东城', u'西城', u'昌平', u'家', u'北三环', u'朝阳区', u'西城区', u'-']

def my_query():
    mz_dict = {}
    query.limit(500)
    query_list = query.find()
    skip_num = 500
    while len(query_list) != 0:
        print(len(query_list) + skip_num - 500)
        for each in query_list:
            position = each.get(u'position').decode('utf8')
            if (position not in mz_dict) and (position not in filter_list):
                query.equal_to(u'position', position)
                count = query.count()
                position_list = []
                flag = False
                for k, v in mz_dict.items():
                    if v != 0:
                        position_list.append(k)
                for s in position_list:
                    if position in s:
                        mz_dict[position] = mz_dict[s] + count
                        mz_dict[s] = 0
                        flag = True
                        break
                    if s in position:
                        mz_dict[s] += count
                        mz_dict[position] = 0
                        flag = True
                        break
                if not flag:
                    mz_dict[position] = count
        m_query = leancloud.Query(u'MZObject')
        m_query.skip(skip_num)
        m_query.limit(500)
        query_list = m_query.find()
        skip_num += 500

    mz_dict[u'和平里'] += mz_dict[u'煤炭大厦']
    mz_dict[u'煤炭大厦'] = 0
    return mz_dict

def my_query2():
    mz_dict = {}
    query.limit(500)
    query_list = query.find()
    skip_num = 500
    while len(query_list) != 0:
        print(len(query_list) + skip_num - 500)
        for each in query_list:
            cost = each.get(u'cost')
            cost = re.findall('\d+', cost)
            for c in cost:
                c = int(c)
                if c >= 50:
                    cost = c
                    break
            if mz_dict.get(cost):
                mz_dict[cost] += 1
            else:
                if isinstance(cost, list):
                    cost = -1
                mz_dict[cost] = 1

        m_query = leancloud.Query(u'MZObject')
        m_query.skip(skip_num)
        m_query.limit(500)
        query_list = m_query.find()
        skip_num += 500

    return mz_dict

def my_query3():
    mz_dict = {}
    query.limit(500)
    query_list = query.find()
    skip_num = 500
    while len(query_list) != 0:
        print(len(query_list) + skip_num - 500)
        for each in query_list:
            height = each.get(u'height').decode('utf8')
            height = re.findall('\d+', height)
            for c in height:
                c = int(c)
                if c <= 150:
                    height = '150以下'
                    height = 1
                    break

                elif 150 < c <= 155:
                    height = '150-155'
                    height = 2
                    break

                elif 155 < c <= 160:
                    height = '155-160'
                    height = 3
                    break

                elif 160 < c <= 165:
                    height = '160-165'
                    height = 4
                    break

                elif 165 < c <= 170:
                    height = '165-170'
                    height = 5
                    break

                elif 170 < c <= 175:
                    height = '170-175'
                    height = 6
                    break

                elif 175 < c <= 180:
                    height = '175-180'
                    height = 7
                    break

                elif c >= 180:
                    height = '180以上'
                    height = 8
                    break

            if height in mz_dict.keys():
                mz_dict[height] += 1
            else:
                if isinstance(height, list):
                    height = '不详'
                    height = 9
                mz_dict[height] = 1

        m_query = leancloud.Query(u'MZObject')
        m_query.skip(skip_num)
        m_query.limit(500)
        query_list = m_query.find()
        skip_num += 500

    return mz_dict

ss = [u'150以下', u'150-155', u'155-160', u'160-165', u'165-170', u'170-175', u'175-180', u'180以上', u'不详']

def barGraph(wcDict):
    keylist = [key[0] for key in ss]
    vallist = [key[1] for key in wcDict]
    barwidth = 0.35
    xVal = np.arange(len(ss))
    plt.xticks(xVal, keylist, rotation=45)
    plt.bar(xVal, vallist, width=barwidth, color='#EE5C42')
    plt.title(u'北京某服务业身高分布')
    plt.show()


leancloud.init('sgfKhqxiz3u8C46F4A9Myyjv-gzGzoHsz', 'nzVh0qbHmRLSd4w2zkk1DL6R')
query = leancloud.Query('MZObject')

# my_dict = my_query2()
# my_dict = sorted(my_dict.items(), key=lambda d: d[0], reverse=False)
# # my_dict = my_dict[:10]
# print(len(my_dict))
# for each in my_dict:
#     print(each[0], ': ', each[1])

# my_dict = my_dict[:20]
# barGraph(my_dict)


main()

# index_content = requests.get('http://www.xianchawang.org/forum-50-1.html').content
# index_content = str(index_content).decode('gbk')
# print index_content

# http://www.cdt-ec.com/tenderNoticeInfo/960000000000014511/downloadNotice
# http://www.cdt-ec.com/web/zbcg_detail.html?param=960000000000014511&str=2
# http://www.bidding.csg.cn/searchsrv/srv/file/download/1200017900/e072c0913a564afd96ed09afb5ce64ad">SJ-2016-07招标公告附件.rar</a>
# http://www.bidding.csg.cn/searchsrv/srv/file/download/1200017871/0ae6271cf32a4f679a0f0e2beb86e905

# urllib.urlretrieve('http://www.bidding.csg.cn/searchsrv/srv/file/download/1200017871/0ae6271cf32a4f679a0f0e2beb86e905', 'hhhh')



# def get_hu_stock_list():
#     pass
#
# def get_shen_stock_list():
#     pass
#
# def get_stock_info():
#     pass
#
# def main():
#     pass


