from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# ref = https://stackpython.co/tutorial/web-scraping-python-beautifulsoup-requests

cols = ['Name', 'Type', 'Skills', 'Bio']

name_list = pd.read_csv('/Users/kontawat/Documents/ICT/IR/Elastic_Search/Data_LOL/name.csv')
data = pd.DataFrame(columns=cols)

for i in name_list['name']:

    url = f"https://leagueoflegends.fandom.com/wiki/{i}/LoL"

    res = requests.get(url)
    res.encoding = "utf-8"

    if res.status_code == 200:

        soup = BeautifulSoup(res.text, 'html.parser')
        # Name
        name = soup.find_all('h1', {'class': 'page-header__title'})
        for ele in name:
            name = ele.text.strip()
            name = re.sub(r'([^\w]League of Legends[^\w])', '', name)
        
        # Bio
        bio = soup.find_all('div', {'style': 'line-height: 1.6em; text-align: center; font-size: 15px;'})
        for ele in bio:
            bio = ele.text.strip()

        # Skills
        skills = soup.find_all('div', attrs={'class': 'champion-ability__header'})
        list_skill = []
        for ele in skills:
            skills = ele.text.strip()
            skills = skills.split('\n')[0]
            list_skill.append(skills)

        # Type
        role = soup.find_all('div', attrs={'data-source': 'legacy'})
        for ele in role:
            role = ele.text.strip()
            role = re.sub(r'Legacy\n ', '', role)

        list_row = [name, str(role), str(list_skill), bio]
        data = data.append(pd.Series(list_row, index=data.columns[:len(list_row)]), ignore_index = True)

        # Successful connection
        print(f"{i} Successful")
    elif res.status_code == 404:
        print(f"{i} Error 404 page not found")
    else:
        print("Not both 200 and 404")

data.to_csv('Data_LOL.csv', index=False)