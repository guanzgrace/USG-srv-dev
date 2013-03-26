import requests
import json
import os

data = requests.get('http://etcweb.princeton.edu/mobile/map/json.php')
content = data.content
locations = json.loads(content)['location']
d = {}
for loc in locations:
    code = int(loc['location_code'])
    del loc['location_code']
    d[code] = loc
f = open(os.path.join(os.path.dirname(__file__), '../campus_map_bldgs_info.py'), 'w')
f.write('campus_info='+str(d))
