from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re

driver = webdriver.Edge()

driver.get('https://www.arenaofvalor.com/web2017/heroDetails.html?id=521')

url = driver.page_source

soup = BeautifulSoup(url)

list_data = []

# bio = soup.find_all('div', attrs={'style': 'font-weight:bold; font-size:110%; border-bottom:1px solid black; background:linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #B44335) 90%; color:white; padding:3px 5px;'})

# list_data = []
# for ele in bio:
#     ele = ele.text.strip()
#     ele = re.sub(r" Link.+[a-zA-Z]", '', ele)
#     ele = re.sub(' +', ' ', ele)
#     list_data.append(ele)
# print(list_data)
for i in range (3):

    bio = soup.find_all('span', {'id': f'skill{i+1}name'})
    # for ele in bio:
    #     bio = ele.text.strip()
    #     bio = re.sub(r'([^\w]League of Legends[^\w])', '', bio)
    for ele in bio:
        bio = ele.text.strip()
        print(bio)
