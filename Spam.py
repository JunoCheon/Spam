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
    try:
        bs = BeautifulSoup(driver.page_source,'html.parser')
        text = bs.find_all('p')[0]
        if text.text == '이웃이 없습니다.':
            print('이웃이 없습니다.')
            return
    except:
        pass
    for i in range(10):
        scrollDown(driver)
     
def scrollDown(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

def getIds(sourse):
    bs = BeautifulSoup(sourse, 'html.parser')
    links = bs.findAll('a', {'class':'link___8Sha'})   

    foundIds = []
    for link in links:
        fid = link.get('href')
        foundIds.append(fid[fid.rfind('/')+1::])
    return foundIds

#check duplicate from my txt file
def checkDuplicate(ids,crwalcsv):
    #ids : list of ids
    #crwalcsv : csv file name
    try:
        f = open(crwalcsv, 'r', encoding='utf-8')
    except:
        f = open(crwalcsv, 'w', encoding='utf-8')
        f.close()
        f = open(crwalcsv, 'r', encoding='utf-8')
    lines = f.readlines()
    lines = [id.strip() for id in lines]
    f.close()
    # remove Duplicate and Return ids
    return list(set(ids) - set(lines))
    
def crawl(crwalcsv,fristID = 'cjhnono1'):
    # fristID = 'cjhnono1'
    IDset = set([fristID])

    while(True):
        # origin_df=pd.read_csv('crawl.csv',encoding='utf-8')
        # url='https://nid.naver.com/nidlogin.login'


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
        ids = getIds(browser.page_source)
        IDset.update(checkDuplicate(ids,crwalcsv))

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



def sendMail(firstid, id, pw, title, body,crwalcsv):
    
    IDset = crawl(crwalcsv,firstid)
    
    #write csv file
    with open(crwalcsv, 'w', encoding='utf-8') as f:
        for id in IDset:
            f.write(id+'\n')
        f.close()

    
    
    #send mail
    recipients = [a+'@naver.com' for a in IDset]
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

    server = smtplib.SMTP_SSL('smtp.naver.com',465)
    server.ehlo()
    server.login(email_id,email_pw)
    server.sendmail(message['From'],recipients,message.as_string())
    server.quit()
    
def readTextFile(fileName):
    # return :  title, body
    f = open(fileName, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    
    title = lines[0]
    body = ""
    for line in lines[1:]:
        body += line
    return title, body

# id = input("Press Enter Naver ID\n")
# pw = input("Press Enter Naver PW\n")
#portNum = int(input("Press Enter Port Number\n"))

def myinput():
    id = input("Press Enter Naver ID\n")
    pw = input("Press Enter Naver PW\n")
    #portNum = int(input("Press Enter Port Number\n")
    firstid = input("Press Enter First ID\n")
    mytxt = input("Press Enter Mail Text File Name(ex : C:\\Users\\user\\Desktop\\Spam\\mail.txt)\n")
    crwalcsv = input("Press Enter Id List File Name(ex : C:\\Users\\user\\Desktop\\Spam\\list.csv)\n")
    title, body = readTextFile(mytxt)
    print("제목 : ")
    print(title)
    print("본문 : ")
    print(body)
    
    return id, pw, firstid, title, body, crwalcsv

id, pw, firstid, title, body, crwalcsv = myinput()
# firstid = input("Press Enter First ID\n")
sendMail(firstid, id, pw, title, body,crwalcsv)