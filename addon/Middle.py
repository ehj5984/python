#!/usr/bin/env python
# coding: utf-8

# ## MIDDLE

# In[1]:


# 라이브러리 선언 
import pandas as pd 
from selenium import webdriver
# 드라이버 위치 설정
driver_loc = "../addon/chromedriver/chromedriver.exe"

# 웹 브라우저 설정 및 브라우저 팝업
options = webdriver.ChromeOptions()
options = options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(executable_path=driver_loc, options=options)

# 웹페이지 파싱 최대3초 기다림
driver.implicitly_wait(3)

# 브라우저 열기
targetUrl = "https://www.daisomall.co.kr/"
driver.get(targetUrl)

# 액션 대상 요소 탐색 후 적용
BtnX = '//*[@id="header"]/div[4]/div/div[1]/ul/li[9]/a/img'

categoryBtn = driver.find_element_by_xpath(BtnX)
categoryBtn.click()

puppyBtn = driver.find_element_by_xpath('//*[@id="nav_sub"]/li[13]/a')
puppyBtn.click()

puppyFoodBtn = driver.find_element_by_xpath('//*[@id="container"]/div[3]/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/a')
puppyFoodBtn.click()

# 현재 페이지 소스 가져오기
targetUrl = driver.current_url
pgSource = driver.page_source

# 라이브러리 선언
from bs4 import BeautifulSoup
import requests , bs4

# targeturl의 page source를 parser로 떠주기 
resp = requests.get(url=targetUrl)
resp.encoding="utf-8"
html = resp.text
htmlObj = bs4.BeautifulSoup(pgSource, "html.parser")

#가격 따기 
allPrice = htmlObj.find(name ="div", attrs={ "class": "warp_goods"})

Price = allPrice.findAll(name ="strong", attrs = {"class":"color_2a"})



# 제품명 따기
allName = htmlObj.find(name ="div", attrs = {"class":"warp_goods"})

Name = allName.findAll(name ="li", attrs ={"class":"goods-list-pname"} )


# 빈 배열 생성 
nameList =[]
priceList =[]

# for 문 으로 배열에 밀어넣기 
for i in range (0, len(Name)):
    eachName = Name[i]  
    nameText = eachName.text
    realnameText = nameText.replace("\n","")
    nameList.append(realnameText)
    
    eachPrice = Price[i]
    priceText = eachPrice.text
    priceList.append(priceText)
    
    
pd.DataFrame(zip(nameList,priceList))

# 제목이 들어갈 컬럼 리스트 정의
columnList = ["제품명", "가격"]


# 데이터 프레임화 후 제목 넣어줌
finalResult = pd.DataFrame(zip(nameList,priceList), columns = columnList)

finalResult
finalResult.to_csv("./finalResult.csv", index= False , encoding ="ms949")


# SMTP 프로토콜 로드
import smtplib

# 이메일을 간단하게 보낼수 있는 라이브러리 로드
from email.message import EmailMessage

import pickle
pw = "shmvnsvtwneuyprc"    
pickle.dump(pw, open("pw.pickle", 'wb'))
pw = pickle.load(open('pw.pickle', 'rb'))

# GMAIL 메일 설정
smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)
# 서버 연결을 설정하는 단계
smtp_gmail.ehlo()
# 연결을 암호화
smtp_gmail.starttls()
 
userid = "ginnyzip5984@gmail.com"


# 로그인 아이디 / 앱 비밀번호
userid = "ginnyzip5984@gmail.com"
userpw = "shmvnsvtwneuyprc"
smtp_gmail.login(userid, userpw)

### 3. 수신자 목록 정의 및 불러오기

import pandas as pd
finalResult =pd.read_csv("./finalResult.csv")

### 4. 메일전송

msg=EmailMessage()

# 제목 입력
msg['Subject']="중간고사 - 이혜진"
 
# 내용 입력
msg.set_content("강아지 사료")
 
# 보내는 사람
msg['From']='ginnyzip5984@gmail.com'
 
# 받는 사람
msg['To'] ='ehj5984@hanmail.net'


file='finalResult.csv'
fp = open(file,'rb')
file_data=fp.read()

msg.add_attachment(file_data,
                   maintype='text',
                   subtype='plain',
                   filename=file)

# 메일 전송
smtp_gmail.send_message(msg)
smtp_gmail.close()


# In[ ]:




