from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import shutil


# ref = https://stackpython.co/tutorial/web-scraping-python-beautifulsoup-requests

cols = ['Name', 'Type', 'Skills', 'Bio', 'File_name']

name_list = pd.read_csv('/Users/kontawat/Documents/ICT/IR/Elastic_Search/Data_Dota2/name.csv')
data = pd.DataFrame(columns= cols)

for i in name_list['name']:

    url = f"https://dota2.fandom.com/wiki/{i}"

    res = requests.get(url)
    res.encoding = "utf-8"

    # Check HTTP Status Code
    # 200 Ok
    # 301 Move Permanently
    # 404 Not Found
    # 500 Internal Server Error

    if res.status_code == 200:

        soup = BeautifulSoup(res.text, 'html.parser')
        # Ref: https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
        name = soup.find_all('h1', {'class': 'page-header__title'})
        for ele in name:
            name = ele.text.strip()
        
        # Bio
        bio = soup.find_all('div', attrs={'style':'display:table-cell; font-style: italic;'})
        for ele in bio:
            bio = ele.text.strip()
        

        # Type
        role = soup.find_all('a', attrs={'title': 'Role'})
        list_role = []
        for ele in role:
            list_role.append(ele.text.strip())

        # Skills
        skills = soup.find_all('div', attrs={'style': 'font-weight:bold; font-size:110%; border-bottom:1px solid black; background:linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #B44335) 90%; color:white; padding:3px 5px;'})
        list_skill = []
        for ele in skills:
            ele = ele.text.strip()
            ele = re.sub(r" Link.+[a-zA-Z]", '', ele)
            ele = re.sub(' +', ' ', ele)
            list_skill.append(ele)

        images_character = soup.find('a', class_="image").findAll('img')
        for image in images_character:
            full_url = image.attrs['data-src']
        r = requests.get(full_url, stream=True)
        file_name = f"{name}_image.jpg"
        if r.status_code == 200:                     #200 status code = OK
            with open(f"./images/images_Dota2/" + file_name , 'wb') as f: 
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        
        
        list_row = [str(name), list_role, list_skill, str(bio), str(file_name)]
        data = data.append(pd.Series(list_row, index=data.columns[:len(list_row)]), ignore_index = True)
        
        
        # Successful connection
        print(f"{i} Successful")



    elif res.status_code == 404:
        print(f"{i} Error 404 page not found")
    else:
        print("Not both 200 and 404")

data.to_csv('Data_Dota.csv', index=False)