from bs4 import BeautifulSoup
import requests
import pandas as pd

# ref = https://stackpython.co/tutorial/web-scraping-python-beautifulsoup-requests

cols = ['name', 'bio']

name_list = pd.read_csv(r'C:\Users\Puter\Documents\GitHub\Elastic_Search\Data_Dota2\name.csv')
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
            
        list_row = [str(name), str(bio)]
        data = data.append(pd.Series(list_row, index=data.columns[:len(list_row)]), ignore_index = True)

        # Successful connection
        print(f"{i} Successful")
    elif res.status_code == 404:
        print(f"{i} Error 404 page not found")
    else:
        print("Not both 200 and 404")

data.to_csv('Data.csv', index=False)