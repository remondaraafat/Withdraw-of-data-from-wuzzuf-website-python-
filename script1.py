import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title=[]
company_name=[]
location_name=[]
skills=[]
links=[]
salary=[]
responsibilities=[]
date=[]
page_num=0

while True:
    try:
        result =requests.get(f"https://wuzzuf.net/search/jobs/?a=navbl&q=python&start={page_num}")

        src=result.content

        soup=BeautifulSoup(src,"lxml")

        page_limit=int(soup.find("strong").text)
        if (page_num>page_limit//15):
            print("pages endded , terminate")
            break
            

        job_titles = soup.find_all("h2", {"class":"css-m604qf"})
        company_names=soup.find_all("a",{"class":"css-17s97q8"})
        locations_names=soup.find_all("span",{"class":"css-5wys0k"})
        job_skills=soup.find_all("div",{"class":"css-y4udm8"})
        posted_new=soup.find_all("div",{"class":"css-4c4ojb"})
        posted_old=soup.find_all("div",{"class":"css-do6t5g"})
        posted=(*posted_new,*posted_old)


        for i in range (len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs["href"])
            company_name.append(company_names[i].text)
            location_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)
            date.append(posted[i].text)
        page_num=+1
        print("page switched")
    except:
        print("error occured")
        break

for link in links:
    result=requests.get(link)
    src=result.content
    soup=BeautifulSoup(src,"lxml")
    salaries=soup.find("span",{"class":"css-4xky9y"})
    salary.append(salaries)
    requirements=soup.find("div",{"class":"css-1t5f0fr"}).ul
    respo_text=""
    for li in requirements.find_all("li"):
        respo_text += li.text+"| "
    respo_text=respo_text[:-2]
    responsibilities.append(respo_text)

file_list=[job_title,company_name,date,location_name,skills,links,salary,responsibilities]
exported=zip_longest(*file_list)
with open("/projects/script_test.csv","w")as myfile:
    wr=csv.writer(myfile)
    wr.writerow(["job_title","company_name","date","location","skills","links","salary","responsibilities"])
    wr.writerows(exported)