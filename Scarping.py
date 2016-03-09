
from  lxml import html
from pwn import *

import requests
from bs4 import BeautifulSoup
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib


list_of_dicts = list()


def getEmailandSektor(url):
    """
    çekilen firma linklerinin içine  gidilip,Firmanin bilgileri çekiyor( mail, sektor,çalişan,sayisi,adresi,numarasi)
    """
    nameoffirm=url[43:len(url)]
    nameoffirm=nameoffirm.upper()
    print("NameofFirm:=",nameoffirm)
    page = requests.get(url)
    pagecontent = html.fromstring(page.content)
    mail = pagecontent.xpath('//div[@class="company_address"]/text()')
    info=pagecontent.xpath('//div[@class="company_details"]//span[@class="right"]/text()')
    print(mail)
    print(info)
    sector=None
    email=None
    for i in range(len(info)):
        if(len(info[i]) >4):
            sector=info[i]
            break

    str="E:"
    for i in range(len(mail)):
        if(str in mail[i]):
            email=mail[i]
    if email==None:
        print("Mail has not been type")
        return

    #print(email.strip(' '))
    email=email.strip('E: ')
    print(email)
    list_of_dicts.append({'name': nameoffirm, 'sector': sector,'mail': email,"sended":0})#Burda dict listeme ekliyor firma bilgilerin


    #WriteFile(url,nameoffirm,sector,email)


def WriteFile():
    with open('output.txt', "w") as ins:
        pickle.dump(list_of_dicts, ins)


def SendMail(to):
    fromaddr = "deneme03@hotmail.com"#your e-mail adress
    toaddr = to
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your subject message"
    body = "Your body message "
    msg.attach(MIMEText(body, 'plain'))
    part = MIMEApplication(open("/Users/admn/Downloads/CvOnurSabitSalman.pdf","rb").read())#path of your cv file
    part.add_header('Content-Disposition', 'attachment', filename="CvOnurSabitSalman.pdf")#name of your cv file with extension
    msg.attach(part)
    server = smtplib.SMTP('smtp.live.com', 587)
    server.starttls()
    server.login(fromaddr, "15.11Oss")#your mail password
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()





MainPage = requests.get('http://www.ariteknokent.com.tr/tr/kimler/teknokentli-firmalar')#itu deki tum firmalarin listelendiği sayfa
data = MainPage.text
soup = BeautifulSoup(data,"lxml")

query1 = soup.find("div", class_="back")
query2=query1.find("div", class_="box2")
count=0
for links in query2.find_all_next('a'):
    link=links.get('href')#Burda sirayla tüm firmalarin linklerini çekiyor

    if(len(link)>=43):
        print(link)
        try:
             getEmailandSektor(link)
        except IndexError:
            print("Not Valid Values")
    else:
        pass
    count=count+1

print("Number of Firm",len(list_of_dicts))





for i in range(len(list_of_dicts)):
    try:
         SendMail(list_of_dicts[i].get('mail'))#Burda sirayla tum mailere posta yolluyor,
         # İsterseniz dict listesi firmalari sektorle gore filtreleyip istediğiniz sektorde çalişan firmaya yollabilirsiniz
         print("Sended this mail "+list_of_dicts[i].get('mail'))
         list_of_dicts[i]['sended'] = 1;
    except Exception as e: print(e)



for i in range(len(list_of_dicts)):
    print(list_of_dicts[i])


#print('Bilişim' in list_of_dicts)

#WriteFile()












