# 주소창에서 ko 또는 en 바꿔주면 리뷰 언어가 바뀐다.
# rating5부터 평가가 좋은 순부터 보이도록 default되어 있다.

import time
import pandas as pd
from bs4 import BeautifulSoup 
from datetime import datetime

from selenium import webdriver


driver=webdriver.Chrome('chromedriver')
driver.set_window_position(0,0)
driver.set_window_size(1000,1000)


# modifying headers
def interceptor(request):
    del request.headers['accept-language']
    request.headers['accept-language'] = 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7'

driver.request_interceptor = interceptor

# review link link
link = 'https://play.google.com/store/apps/details?id=air.com.speakingmax&hl=ko&showAllReviews=true'
# link = 'https://play.google.com/store/apps/details?id=net.teuida.teuida&hl=en&showAllReviews=true'
# how many scrolls we need
scroll_cnt = 50

# download chrome driver https://sites.google.com/a/chromium.org/chromedriver/home
# driver = webdriver.Chrome('./chromedriver')
driver.get(link)

# os.makedirs('result', exist_ok=True)

for i in range(scroll_cnt):
  # scroll to bottom
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  time.sleep(3)

  # click 'Load more' button, if exists
  try:
    xpath = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span"
    load_more = driver.find_element_by_xpath(xpath).click()
    # css_target = '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div > span > span'
    # load_more = driver.find_element_by_css_selector(css_target).click()
    print('*** Found a button...')
  except:
    print('Cannot find load more button...')

# get review containers
reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')

print('There are %d reviews avaliable!' % len(reviews))
print('Writing the data...')

# create empty dataframe to store data
df = pd.DataFrame(columns=['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment'])

# get review data
for review in reviews:
  # parse string to html using bs4
  soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')

  # reviewer
  name = soup.find(class_='X43Kjb').text

  # rating
  ratings = int(soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '').replace('개를 받았습니다.', '').strip())

  # review date
  date = soup.find(class_='p2TkOb').text
  date = datetime.strptime(date, '%Y년 %m월 %d일')
  date = date.strftime('%Y-%m-%d')

  # helpful
  helpful = soup.find(class_='jUL89d y92BAb').text
  if not helpful:
    helpful = 0
  
  # review text
  comment = soup.find('span', jsname='fbQN7e').text
  if not comment:
    comment = soup.find('span', jsname='bN97Pc').text
  
  # developer comment
  developer_comment = None
  dc_div = soup.find('div', class_='LVQB0b')
  if dc_div:
    developer_comment = dc_div.text.replace('\n', ' ')
  
  # append to dataframe
  df = df.append({
    'name': name,
    'ratings': ratings,
    'date': date,
    'helpful': helpful,
    'comment': comment,
    'developer_comment': developer_comment
  }, ignore_index=True)

# finally save the dataframe into csv file
filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv("teuida.csv", encoding='utf-8-sig', index=False)
driver.stop_client()
# driver.close()

print('Done!')