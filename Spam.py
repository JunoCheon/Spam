import time
from selenium import webdriver
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
from numpy import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def openNeighborUrl(driver, naverId):
    driver.get('https://m.blog.naver.com/BuddyList.nhn?blogId=%s' % naverId)
    for i in range(10):
        scrollDown(driver)
     
def scrollDown(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

def getIds(sourse):
    bs = BeautifulSoup(sourse, 'html.parser')
    links = bs.findAll('a', {'class':'link___8Sha'})   

    foundIds = []

    for count,link in enumerate(links):
        fid = link.get('href')
        foundIds.append(fid[fid.rfind('/')+1::])
    return foundIds



def crawl(fristID = 'cjhnono1'):
    # fristID = 'cjhnono1'
    IDset = set([fristID])

    while(True):
        # origin_df=pd.read_csv('crawl.csv',encoding='utf-8')
        # url='https://nid.naver.com/nidlogin.login'
        # id="cjhnono1"
        # pw="Sshshdi0930"


        browser=webdriver.Chrome(ChromeDriverManager().install())
        # browser.get(url)

        browser.implicitly_wait(2)

        # 로그인
        # browser.execute_script("document.getElementsByName('id')[0].value=\'"+ id + "\'")
        # browser.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")

        # browser.find_element(by=By.XPATH,value='//*[@id="log.login"]').click()
        # time.sleep(1)


        Id = random.choice(list(IDset))
        #print(Id)
        openNeighborUrl(browser, Id)
        IDset.update(getIds(browser.page_source))

        if len(IDset) > 500:
            print("ID 개수가 500개를 넘었습니다.")
            print("크롤링을 종료합니다.")
            IDset = list(IDset)[0:500]
            break
        time.sleep(1)
        browser.close()
        browser.quit()
        print("현재 ID 개수 :")
        print(len(IDset))
    return IDset



def sendMail(firstid, id, pw, title, body,portNum):
    recipients = [a+'@naver.com' for a in crawl(firstid)]
    message = MIMEMultipart()
    message['Subject'] = title
    message['From'] = id+"@naver.com"
    message['To'] = ",".join(recipients)

    content = """
        <html>
        <body>
            <h2>{title}</h2>
            <p>{body}</p>
        </body>
        </html>
    """.format(
    title = title,
    body = body
    )

    mimetext = MIMEText(content,'html')
    message.attach(mimetext)


    email_id = id
    email_pw = pw

    server = smtplib.SMTP_SSL('smtp.naver.com',portNum)
    server.ehlo()
    server.login(email_id,email_pw)
    server.sendmail(message['From'],recipients,message.as_string())
    server.quit()
    
#%%

id = input("Press Enter Naver ID\n")
pw = input("Press Enter Naver PW\n")
#portNum = int(input("Press Enter Port Number\n"))

firstid = input("이웃탐색을 시작할 ID를 입력하세요\n")

# Title = input("Press Enter Title")
# Body = input("Press Enter Body")
Title = """ 
안녕하세요, 자일리톨캔디 스마트스토어의 대표자 이원재입니다. 
"""
body = """ 
안녕하세요, 저는 별뜰무렵이라는 자일리톨 캔디 스마트스토어의 운영자입니다. \n
작성하신 블로그 글을 보고 메일 드리게 되었습니다. \n
\n
저희 별뜰무렵은 현재 네이버 스마트스토어 내에서 가장 좋은 가성비로 캔디를 판매중에 있습니다. \n
비싼 가격의 자일리톨 캔디를 모두가 저렴하게 즐기실 수 있으면 좋겠다는 마음으로 운영하고 있습니다.\n
자일리톨 캔디에 관심이 많은 분이시라면 좋은 품질의 상품을 저렴하게 구매할 수 있으실 것이라 자부하여 이렇게 실례를 무릅쓰고 추천 메일을 보내드립니다. \n
\n
혹시 저희 자일리톨캔디를 무료로 보내드리면 받아보실 의향이 있으신지요? \n
기타 사항 궁금하신 점이 있으시다면 회신 주십시오.\n
기다리고 있겠습니다. 좋은 하루 되세요~!\n
\n
\n
\n
―――――――――――――――――――――――――――――――――――――――――――
\n
별뜰무렵\n
\n
(02504) 서울시 동대문구 서울시립대로 163(전농동 90) 백주년기념관 217호\n
\n
별뜰무렵 스마트스토어 ｜ 대표\n
\n
\n
\n
이 원 재\n
\n
\n
Tel 010-9043-9549 Email wonjae961004@naver.com\n
\n
"""

print(Title)
print(body)
sendMail(firstid, id, pw, Title, body,portNum = 465)
# %%
