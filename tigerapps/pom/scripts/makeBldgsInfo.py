import requests
import json
import os
import operator

data = requests.get("http://etcweb.princeton.edu/mobile/map/json.php")
content = data.content
locations = json.loads(content)["location"]
#We want to reorganize how the loaded json is key-valued
d = {}
for loc in locations:
    code = int(loc["location_code"])
    del loc["location_code"]
    d[code] = loc
#Now we save line by line
f = open(os.path.join(os.path.dirname(__file__), "../campus_map_bldgs_info.py"), "w")
f.write("campus_info = {\n")
l = sorted(d.items(), key=operator.itemgetter(0))
for k,v in l:
    f.write("  %d: {\n" % k)
    for k1,v1 in v.iteritems():
        if type(v1) == unicode:
            if "'" in v1:
                f.write(u"    u'%s': u'''%s''',\n" % (unicode(k1),unicode(v1)))
            else:
                f.write(u"    u'%s': u'%s',\n" % (unicode(k1),unicode(v1)))
        else:
            f.write(u"    u'%s': %s,\n" % (unicode(k1),unicode(v1)))
    f.write("  },\n")
f.write("}")
f.close()

