from django.template.loader import render_to_string
import requests
import datetime
from bs4 import BeautifulSoup


url = 'http://clusters-lamp.princeton.edu/cgi-bin/clusterinfo.pl'
PRINTER_BLDGS = {
    '1901': '1901H',
    '1937': '1937H',
    '1981': 'HARGH',
    'Blair': 'BLAIR',
    'Bloomberg_315': 'BLOOM',
    'Brown': 'BROWN',
    'Brush_Gallery': 'JADWH',
    'Butler_D033': '1976H',
    # Butler Apts
    'Campus_Club': 'CCAMP',
    'CJL': 'CENJL',
    'Dod': 'DODHA',
    'Edwards': 'EDWAR',
    'Fields_Cntr': 'CFCTR',
    'Firestone': 'FIRES',
    'Fisher_213': 'FISHH',
    'Forbes': 'FORBC',
    'Forbes_Lib': 'FORBC',
    'Foulke': 'FOULK',
    'Friend_016': 'FRIEN',
    'Friend_017': 'FRIEN',
    'Frist_200': 'FRIST',
    'Frist_300': 'FRIST',
    'Grad_College': 'GRADC',
    # Hibben
    'Holder_B11': 'HOLDE',
    'Holder_B31': 'HOLDE',
    'Lauritzen_409': 'HARGH',
    # Lawrence_1
    # Lawrence_14
    'Little_North': 'LITTL',
    'Little_South': 'LITTL',
    'Madison': 'MADIS',
    'McCosh_B59': 'MCCOS',
    'New_GC': 'GRADC',
    'Pyne': 'PYNEH',
    'Scully_269': 'SCULL',
    'Scully_309': 'SCULL',
    'Spelman': 'SPELM',
    'Whitman_Lib': 'HARGH',
    'Wilcox': 'WILCH',
    'Witherspoon': 'WITHR',
    'Wright': 'PATTN',
    'Wu': 'WILCH'
}


class Printer:
    def __init__(self, bldg, room, loc, color, status):
        self.bldg = str(bldg)
        self.room = str(room)
        self.loc = str(loc)
        self.color = str(color)
        self.status = str(status)
    def __str__(self):
        return "%s: %s" % (self.loc, self.status)
    __repr__ = __str__


####
# The following functions are common to all modules in pom.scrape
# We may want to put them in a class for OO-programming purposes
####

def get_bldgs():
    return tuple(PRINTER_BLDGS.values())

def scrape():
    '''returns dict of list of printers, bldg_code:[printers]'''
    timestamp = datetime.datetime.now()
    
    resp = requests.get(url)
    bs = BeautifulSoup(resp.content)
    table = bs.find('table')
    rows = table.find_all('tr')[1:]
    clusters = {}
    for row in rows:
        ps = row.find_all('p')
        loc = ps[0].contents[0][:-1].rstrip('*')
        bldg = ps[1]
        room = ps[2]
        statusTag = ps[3]
        if loc in PRINTER_BLDGS:
            code = PRINTER_BLDGS[loc]
        else:
            continue
        
        printers = []
        for font_tag in statusTag.find_all('font'):
            try:
                status = font_tag.contents[0]
                color = font_tag.attrs['color']
            except:
                continue
            p = Printer(bldg, room, loc, color, status)
            printers.append(p)
        if code in clusters:
            clusters[code] += printers
        else:
            clusters[code] = printers

    return (timestamp, clusters)

def render(scraped=None):
    if not scraped:
        scraped = scrape()
    timestamp, printer_mapping = scraped
    printer_list = [printer for bldg_code,printers_bldg in printer_mapping.items() for printer in printers_bldg]
    printer_list = sorted(printer_list, key=lambda printer: printer.loc)
    html = render_to_string('pom/data_printers.html',
                            {'printers' : printer_list})
    return {'timestamp': timestamp.strftime("%b %e, %l:%M %p"),
            'html': html}

