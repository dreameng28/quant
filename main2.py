import leancloud
import re


leancloud.init('sgfKhqxiz3u8C46F4A9Myyjv-gzGzoHsz',
               'nzVh0qbHmRLSd4w2zkk1DL6R')


class MZObject(leancloud.Object):
    pass
query = leancloud.Query('MZObject')

query.limit(500)
query_list = query.find()
mz_dict = {}
skip_num = 500
while len(query_list) > 0:
    print(len(query_list))
    for each in query_list:

        # 找出height符合条件的
        height = str(each.get('height'))
        height = re.findall('(\d+)', height, re.S)
        for num in height:
            num = int(num)
            if num >= 150:
                height = num
                break
        if isinstance(height, list):
            height = 0

        # 找出cost符合条件的
        cost = str(each.get('cost'))
        cost = re.findall('(\d+)', cost, re.S)
        for num in cost:
            num = int(num)
            if num >= 50:
                cost = num
                break
        if isinstance(cost, list):
            cost = 10000

        # 找出age符合条件的
        age = str(each.get('age'))
        age = re.findall('(\d+)', age, re.S)
        for num in age:
            num = int(num)
            if num >= 15:
                age = num
                break
        if isinstance(age, list):
            age = 100

        title = str(each.get('title'))

        if cost == 300 and age <= 44 and height >= 168:
            name = str(each.get('name'))
            print(title)
            print(name, height, age, cost)
            print('\n')
    query = leancloud.Query('MZObject')
    query.limit(500)
    query.skip(skip_num)
    skip_num += 500
    query_list = query.find()

# print(len(mz_dict))
# mz_list = sorted(mz_dict.items(), key=lambda d: d[1], reverse=True)
# for each in mz_list:
#     print(each[0], ': ', each[1])
