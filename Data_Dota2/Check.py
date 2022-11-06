from bs4 import BeautifulSoup
from 
import requests
import re

url = "https://wildrift.leagueoflegends.com/en-us/champions/ahri/"
bio_url = "https://universe.leagueoflegends.com/en_US/story/champion/ahri/"

res = requests.get(url)
res_bio = requests.get(bio_url)
res.encoding = "utf-8"
res_bio.encoding = "utf-8"

soup = BeautifulSoup(res.text, 'html.parser')
soup_bio = BeautifulSoup(res_bio.text, 'html.parser')

list_data = []

# bio = soup.find_all('div', attrs={'style': 'font-weight:bold; font-size:110%; border-bottom:1px solid black; background:linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #B44335) 90%; color:white; padding:3px 5px;'})

# list_data = []
# for ele in bio:
#     ele = ele.text.strip()
#     ele = re.sub(r" Link.+[a-zA-Z]", '', ele)
#     ele = re.sub(' +', ' ', ele)
#     list_data.append(ele)
# print(list_data)

# bio = soup.find_all('h3', {'class': 'heading-08 ChampionDetailHero-module--championName--eyJEV'})
# for ele in bio:
#     bio = ele.text.strip()

if res_bio.status_code == 200:

    bio = soup_bio.find(id='CatchElement')

    print(bio)
