from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re

driver = webdriver.Edge()

url = "https://dota2.fandom.com/wiki/Abaddon"

res = requests.get(url)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, 'html.parser')

name = soup.select('div img')

images_url = name[0]['src'] 

print(images_url)