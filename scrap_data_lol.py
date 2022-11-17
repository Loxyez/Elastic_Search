from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import shutil


def preprocess_name(name_og):
    # %27, _, ., -
    name = name_og.lower()
    name = name.replace("\'","-")
    name = name.replace("_","-")
    name = name.replace(".","")
    name = name.replace(" ", "-")
    name = name[:-1]

    if (name == "nunu-&-willump"):
        name = "nunu"
    elif name == "renata-glasc":
        name = "renata"
    print(name_og, " ", name)
    return name


def download_image_lol(name):
    file_name = f"{name}_image.png"
    name = preprocess_name(name)
    url = f"https://www.leagueoflegends.com/en-us/champions/{name}/"
    res = requests.get(url)
    res.encoding = "utf-8"
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        divs = soup.find('div', attrs={'data-testid':'overview:backgroundimage', 'class':'style__ForegroundAsset-sc-8gkpub-4 fyyYJz'})
        
        try: 
            images_url = divs.find('img',attrs={'class':'style__NoScriptImg-g183su-0 cipsic'}).attrs['src']
        except:
            print(name + " Unsuccessful")
        r = requests.get(images_url, stream=True)
        file_name = f"{name}_image.png"
        # 200 status code = OK
        if r.status_code == 200:                
            with open(f"./images/images_LoL/" + file_name , 'wb') as f: 
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                print(images_url)
        else:
            print("Can't download")






if __name__ == "__main__":

    # ref = https://stackpython.co/tutorial/web-scraping-python-beautifulsoup-requests

    cols = ['Name', 'Type', 'Skills', 'Bio', 'File_name']

    name_list = pd.read_csv('/Users/kontawat/Documents/ICT/IR/Elastic_Search/Data_LOL/name.csv')
    data = pd.DataFrame(columns=cols)

    for i in name_list['name']:

        url = f"https://leagueoflegends.fandom.com/wiki/{i}/LoL"
        # url_for_img = f"https://www.leagueoflegends.com/en-us/champions/{i.lower()}/"


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

            # # Save image from old website 
            # images_url = soup.find('img', attrs={'class':'pi-image-thumbnail'}).attrs['src']
            # r = requests.get(images_url, stream=True)
            file_name = f"{name}_image.png"
            # # 200 status code = OK
            # if r.status_code == 200:                
            #     with open(f"./images/images_LoL/" + file_name , 'wb') as f: 
            #         r.raw.decode_content = True
            #         shutil.copyfileobj(r.raw, f)
            download_image_lol(name)

            list_row = [name, str(role), str(list_skill), bio, file_name]
            data = data.append(pd.Series(list_row, index=data.columns[:len(list_row)]), ignore_index = True)

            # Successful connection
            print(f"{i} Successful")
        elif res.status_code == 404:
            print(f"{i} Error 404 page not found")
        else:
            print("Not both 200 and 404")
    data.to_csv('Data_LOL.csv', index=False)