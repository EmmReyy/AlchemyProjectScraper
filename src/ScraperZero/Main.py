from bs4 import BeautifulSoup, NavigableString, Tag
from dataclasses import dataclass, field, asdict
import requests
import json

@dataclass
class Ingredient:
    name : str
    effects: [str]
    firstEffect : str = field(init=False)
    secondEffect : str = field(init=False)
    thirdEffect : str = field(init=False)
    fourthEffect : str = field(init=False)

    def __post_init__(self):
        self.firstEffect = effects[0]
        self.secondEffect = effects[1]
        self.thirdEffect = effects[2]
        self.fourthEffect = effects[3]

url = "https://en.uesp.net/wiki/Skyrim:Ingredients"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

table = soup.find('table', class_= 'wikitable striped2_1')
rows = table.find_all('tr')

count = 1

listOfIngredients = []

def is_an_effect(tag):
    if "EffectPos" in tag.attrs.get('class', []) or "EffectNeg" in tag.attrs.get('class', []):
        return True
    else:
        return False


while count < len(rows):

    name = ""
    effects = []

    if rows[count].has_attr('id'):

        for child in list(filter(lambda x: isinstance(x, Tag), rows[count].children)):
            if child.has_attr('rowspan') and not child.has_attr('style'):
                name = child.find('a').text

        count+=1

        for child in list(filter(lambda x: isinstance(x, Tag), rows[count].children)):
            if is_an_effect(child):
                effects.append(child.get_text(strip=True))

        listOfIngredients.append(Ingredient(name, effects))

    count+=1

dictOfIngredients = []
for ing in listOfIngredients:
    dictOfIngredients.append(asdict(ing))

json_data = json.dumps(dictOfIngredients, indent=4)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dictOfIngredients, f, ensure_ascii=False, indent=4)
