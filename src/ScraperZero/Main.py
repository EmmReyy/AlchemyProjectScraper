from bs4 import BeautifulSoup, NavigableString, Tag
import requests

url = "https://en.uesp.net/wiki/Skyrim:Ingredients"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

table = soup.find('table', class_= 'wikitable striped2_1')
rows = table.find_all('tr')

name = rows[1]['id']
count = 1
ingredients = []

while count < len(rows):
    if rows[count].has_attr('id'):

        for child in list(filter(lambda x: isinstance(x, Tag), rows[count].children)):
            if child.has_attr('rowspan') and not child.has_attr('style'):
                ingredients.append(child.find('a').text)


    count+=1
