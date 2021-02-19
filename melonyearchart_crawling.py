#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import os


# In[10]:


# 2020 year chart(2020년 시대별 차트)
# https://www.melon.com/chart/age/list.htm?idx=1&chartType=YE&chartGenre=POP&chartDate=2020&moved=Y
headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36')
    }
 
age_url ="https://www.melon.com/chart/age/list.htm"
 
params = {
    'idx':'1',
    'chartType':'YE',     # Related to a 10-year search(10년 단위로 검색과 관련)
    'chartGenre':'KPOP',  # KPOP is domestic, POP is foreign(국내 차트는 KPOP, 해외 차트는 POP으로 지정)
    'chartDate':'2020',   # Select Year(연도 지정)
    'moved':'Y',
}
response = requests.get(age_url, params=params, headers = headers)
soup = BeautifulSoup(response.text, 'html.parser')
 
# Get the index value of each tag together with the enumerate(enumerate로 각 tag의 index값을 함께 가져온다) 
# 1 at the end of the line means that it starts from 1. If not, it starts from 0(라인 마지막의 1은 1부터 시작한다는 의미. 없으면 0부터 시작)
# There are many "a tags". Only get "a tag" containing the "playSong" is imported from the href element(a태그가 많다. 그 중에서 href요소 안에서 playSong문자를 포함하는 a태그만 가져온다)
for i, tag in enumerate(soup.select('a[href*=playSong]'),1):
    title = tag.text    
    js = tag['href']

    # Unlike the TOP100 crawling, the year chart has a single quotation('') of songId(시대별차트는 TOP100 크롤링과는 달리 songId부분이 ''홑따옴표로 되어있다)
    # Therefore, the regular expression needs to be modified(따라서 정규표현식을 아래처럼 수정)
    matched = re.search(r",'(\d+)'",js)
    # print(matched.group(1))  # print songId. for example, group(1) is 32313543, group(0)is ,'32313543'
    
    if matched:
        # output songId with group (1) at the end of url(url 마지막에 group(1)으로 songId 출력)
        song_Id = matched.group(1)
        song_url = 'https://www.melon.com/song/detail.htm?songId=' + song_Id
        print(i,title, song_url)


# In[ ]:




