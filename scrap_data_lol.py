from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# ref = https://stackpython.co/tutorial/web-scraping-python-beautifulsoup-requests

cols = ['Name', 'Type', 'Skills', 'Bio']

name_list = pd.read_csv(r'C:\Users\Puter\Documents\GitHub\Elastic_Search\Data_LOL')
data = pd.DataFrame(columns=cols)

for i in name_list['name']:

    url = f"https://hero.fandom.com/wiki/{i}"

    res = requests.get(url)
    res.encoding = "utf-8"

    if res.status_code == 200:

        soup = BeautifulSoup(res.text, 'html.parser')
        name = soup.find_all('h3', {'class': 'heading-08 ChampionDetailHero-module--championName--eyJEV'})
        for  ele in name:
            name = ele.text.strip()
        
        

    break