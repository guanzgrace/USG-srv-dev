from django.template.loader import render_to_string
import requests
import datetime
from bs4 import BeautifulSoup
from pom.bldg_info import *


url_stub = 'http://facilities.princeton.edu/dining/_Foodpro/menu.asp?locationNum=0'
DINING_HALLS = {
    'WILCH': (2, "Butler/Wilson College: "),
    'MADIH': (1, "Rocky/Mathey College: "),
    'FORBC': (3, ""),
    'HARGH': (8, ""),
    'CENJL': (5, ""),
    'GRADC': (4, ""),
}


class Menu:
    def __init__(self):
        self.meals = {}
    def __str__(self):
        return str(self.meals)
    __repr__ = __str__

class Meal:
    def __init__(self):
        self.entrees = []
    def __str__(self):
        return str(self.entrees)
    __repr__ = __str__

class Entree:
    def __init__(self):
        self.attributes = {}
        self.color = '#000000' #default black

    def __str__(self):
        return str(self.attributes)
    __repr__ = __str__

MENUS_ORDER = {'Breakfast':0, 'Brunch':1, 'Lunch':2, 'Dinner':3}
def sorter(name):
    if name in MENUS_ORDER:
        return MENUS_ORDER[name]
    else:
        return 4


def scrape_single(bldg_code):
    """Scrape the menu page for the given dining hall and return the data
    as a menu object"""
    hall_num = DINING_HALLS[bldg_code][0]
    url = url_stub + str(hall_num)
    
    resp = requests.get(url)
    bs = BeautifulSoup(resp.content)
    menu = Menu()
    #menu.title = bs.title.contents[0]
    for meal_xml in bs.find_all('meal'):
        meal = Meal()
        meal.name = unicode(meal_xml.attrs['name'])
        for entree_xml in meal_xml.find_all('entree'):
            entree = Entree()
            entree.attributes['name'] = unicode(entree_xml.next.contents[0])
            for c in entree_xml.contents[1:]:
                entree.attributes[c.name] = unicode(c.contents[0])
                if unicode(c.contents[0]) == 'y':
                    if (c.name == 'vegan'):
                        entree.color = '#0000FF' #blue
                    elif (c.name == 'vegetarian'):
                        entree.color = '#00AA00' #dark green
                    elif (c.name == 'pork'):
                        entree.color = '#8000FF' #purple
                    elif (c.name == 'nuts'):
                        entree.color = '#990000' #brownish red
            meal.entrees.append(entree)
        menu.meals[meal.name] = meal
    return menu


####
# The following functions are common to all modules in pom.scrape
# We may want to put them in a class for OO-programming purposes
####

def get_bldgs():
    return tuple(DINING_HALLS.keys())

def scrape():
    """Return a list of menus, one for each dining hall"""
    timestamp = datetime.datetime.now()
    menus = {}
    for bldg_code in DINING_HALLS:
        menus[bldg_code] = scrape_single(bldg_code)
    return (timestamp, menus)

def render(scraped=None):
    if not scraped:
        scraped = scrape()
    timestamp, menu_mapping = scraped
    menu_list = [(bldg_code,
                  DINING_HALLS[bldg_code][1] + BLDG_INFO[bldg_code][0],
                  menu) \
                 for bldg_code, menu in menu_mapping.items()]
    menu_list = sorted(menu_list, key = lambda x: x[1])
    for tup in menu_list:
        tup[2].meals = [(name, meal) for name, meal in tup[2].meals.items()]
        tup[2].meals = sorted(tup[2].meals, key = lambda x: sorter(x[0]))
    html = render_to_string('pom/data_menus.html',
                            {'menus': menu_list})
    return {'timestamp': timestamp.strftime("%B %e, %l:%M %p"),
            'html': html}
