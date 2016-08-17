__author__ = 'dreameng'

import requests
import datetime
import re

cookies_str = '__cfduid=db094ef2f3beedc20886b275d7b63562c1471265946; tjpctrl=1471444728281; fDyj_2132_saltkey=UwpNz3YN; fDyj_2132_lastvisit=1471439439; fDyj_2132_sendmail=1; Hm_lvt_ef6071de284645b5fb2dee7870f09876=1471265950; Hm_lpvt_ef6071de284645b5fb2dee7870f09876=1471443041; fDyj_2132_lastact=1471443070%09member.php%09logging; fDyj_2132_ulastactivity=c7b927rhUdTCy4D9lAZZU1etnuzgT2U3B2qlZSXrCcRQt4R%2FEt1H; fDyj_2132_sid=oSaHL6; fDyj_2132_auth=fca8RdT77ViEyzQ1VWJnhM1M43mpSmV21wScIoNWGAyGvNWFZ%2FghoJSrYGzk8sm%2B5Va169x2KFNgtrQUzx93bPw9uA; fDyj_2132_lastcheckfeed=63340%7C1471443070; fDyj_2132_checkfollow=1; fDyj_2132_lip=108.162.215.202%2C1471442736'
cookies_list = cookies_str.split(';')
cookies = {}
for each in cookies_list:
    each = each.strip().split('=')
    cookies[each[0]] = each[1]

print(cookies)

url = 'http://www.xianchawang.info/thread-22102-1-1.html'
content = requests.get(url, timeout=60, cookies=cookies).text
print(content)

dtstr = re.findall('发表于 (.*?)</em>', content, re.S)
print(dtstr)
date = dtstr[0]
date = re.findall('(\d+-\d+-\d+ \d+:\d+:\d+)', date, re.S)
date_time = datetime.datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S')
print(date_time)
print(datetime.datetime.now())
