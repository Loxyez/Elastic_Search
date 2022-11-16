from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import requests
import shutil

cols = ['Name', 'Type', 'Skills', 'Bio', 'File_name']

name_list = pd.read_csv('/Users/kontawat/Documents/ICT/IR/Elastic_Search/Data_Rov/name.csv')
data = pd.DataFrame(columns=cols)

driver = webdriver.Chrome()
for i in name_list['name']:

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

    iBigPic = soup.find('i', attrs={'class':'iBigPic'})
    full_url = "https://www.arenaofvalor.com/images/heroes/skin/"+ iBigPic.find('img').attrs['src'].split("/")[-1]
    r = requests.get(full_url, stream=True)
    file_name = f"{name}_image.jpg"
    if r.status_code == 200:                     # 200 status code = OK
        with open(f"./images/images_rov/" + file_name , 'wb') as f: 
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    list_row = [str(name), list_role, list_skill, str(bio), file_name]
    data = data.append(pd.Series(list_row, index=data.columns[:len(list_row)]), ignore_index = True)

data.to_csv('Data_ROV.csv', index=False)