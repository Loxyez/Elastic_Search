from bs4 import BeautifulSoup
import requests
import re

url = "https://dota2.fandom.com/wiki/Abaddon"

res = requests.get(url)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, 'html.parser')

list_data = []

bio = soup.find_all('div', attrs={'style': 'font-weight:bold; font-size:110%; border-bottom:1px solid black; background:linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #B44335) 90%; color:white; padding:3px 5px;'})

list_data = []
for ele in bio:
    ele = ele.text.strip()
    ele = re.sub(r" Link.+[a-zA-Z]", '', ele)
    ele = re.sub(' +', ' ', ele)
    list_data.append(ele)
print(list_data)
