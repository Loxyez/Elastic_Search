from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re

cols = ['Name', 'Type', 'Skills', 'Bio']

name_list = pd.read_csv('/Users/kontawat/Documents/ICT/IR/Elastic_Search/Data_Rov/name.csv')
data = pd.DataFrame(columns=cols)

for i in name_list['name']:

    driver = webdriver.Chrome()

    driver.get(f'https://www.arenaofvalor.com/web2017/heroDetails.html?id={i}')
    url = driver.page_source


    soup = BeautifulSoup(url, 'html.parser')

    # Name
    name = soup.find('em')
    for ele in name:
        name = ele.text.strip()

    # Skills
    list_skill = []
    for i in range (3):
        skills = soup.find_all('span', {'id': f'skill{i+1}name'})
        for ele in skills:
            skills = ele.text.strip()
            list_skill.append(skills)

    # Role
    list_role = []

    # Bio
    bio = soup.find_all('div', {'class': 'story-cont-wrap'})
    for ele in bio:
        bio = ele.text.strip()

    list_row = [str(name), list_role, list_skill, str(bio)]
    data = data.append(pd.Series(list_row, index=data.columns[:len(list_row)]), ignore_index = True)

data.to_csv('Data_ROV.csv', index=False)