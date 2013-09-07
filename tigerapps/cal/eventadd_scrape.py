from BeautifulSoup import BeautifulSoup, NavigableString
from datetime import datetime
import logging
import re
import requests

from cal.models import CalUser, Event, EventCategory, EventCluster




def invert_bldg_info():
    from pom.bldg_info import BLDG_INFO
    locations = {}
    for bldg_code, (name, alt_names, show) in BLDG_INFO.iteritems():
        locations[name.lower()] = bldg_code
        for alt_name in alt_names:
            locations[alt_name.lower()] = bldg_code
    return locations


def tag_names_to_tags(tag_names):
    tags = []
    for tag_name in tag_names:
        tag_name = re.sub("^\W", "", tag_name)
        if not tag_name:
            continue
        try:
            tag = EventCategory.objects.get(category_name__iexact=tag_name)
        except EventCategory.DoesNotExist:
            tag = EventCategory(category_name=tag_name)
            tag.save()
        tags.append(tag)
    return tags


def strip_tags(html, keep_tags):
    """
    Get the contents of C{html}, stripping out tags not in C{keep_tags}.
    """
    tag = BeautifulSoup(html)
    for inner_tag in tag.findAll(True):
        if inner_tag.name not in keep_tags:
            s = ""
            for c in inner_tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), keep_tags)
                s += unicode(c)
            inner_tag.replaceWith(s)
    return unicode(tag)




class Page(object):

    def __init__(self, content, user, tags=[], **kwargs):
        self.content = content
        self.user = user
        self.cluster_tags = tag_names_to_tags(tags)
        self.kwargs = kwargs
        self.locations = invert_bldg_info()


    @classmethod
    def from_scrape(cls, url, **kwargs):
        kwargs['url'] = url
        resp = requests.get(url)
        print "Scraped %s" % url
        return cls(resp.content, **kwargs)


    def handle(self):
        bs = BeautifulSoup(self.content)
        if 'container' in self.kwargs:
            bs = bs.find("div", self.kwargs['container'])

        # TODO
        tmp_day = bs.find(attrs={'class':"view-content"}
            ).find("h3").find("div")['class']
        tmp_day += str(datetime.today().year)

        # Get all div's with a certain class.
        bs_events = bs.findAll("div", self.kwargs['event'])
        for bs_event in bs_events:

            bs_title = bs_event.find(attrs={'class':self.kwargs['cluster_title']}).find('a')
            cluster_title = bs_title.string

            cluster_description = strip_tags(unicode(bs_event.find('p')), ['a'])
            # TODO
            if 'url' in self.kwargs:
                cluster_url = self.kwargs['url'] + bs_title['href']
                cluster_description += "<p>Path to Princeton link: <a href='%s'>%s</a>" % (
                    cluster_url, cluster_url)

            # TODO
            tmp_starttime = bs_event.find(attrs={'class':"date-display-start"}
                ).text
            if len(tmp_starttime.split(":")[0]) == 1:
                tmp_starttime = '0' + tmp_starttime
            if tmp_starttime.endswith('a.m.'):
                tmp_starttime.replace('a.m.', 'AM')
            else:
                tmp_starttime.replace('p.m.', 'PM')
            tmp_endtime = bs_event.find(attrs={'class':"date-display-end"}
                ).text
            if len(tmp_endtime.split(":")[0]) == 1:
                tmp_endtime = '0' + tmp_endtime
            if tmp_endtime.endswith('a.m.'):
                tmp_endtime.replace('a.m.', 'AM')
            else:
                tmp_endtime.replace('p.m.', 'PM')
            event_date_time_start = datetime.strptime(
                "%s %s" % (tmp_day, tmp_starttime),
                "%B%d%Y %I:%M %p")
            event_date_time_end = datetime.strptime(
                "%s %s" % (tmp_day, tmp_endtime),
                "%B%d%Y %I:%M %p")

            # TODO
            event_location_objs = bs_event.find(attrs={'class':self.kwargs['event_location']}
                ).find(attrs={'class':'field-content'}).findAll('li')
            if len(event_location_objs) == 1:
                event_location_str = event_location_objs[0].text.lower()
                success = False
                if event_location_str in self.locations:
                    event_location = self.locations[event_location_str]
                    event_location_details = ""
                else:
                    # Try various methods..
                    for c in [", ", " - "]:
                        if c in event_location_str:
                            for i, els in enumerate(event_location_str.split(c)):
                                if els in self.locations:
                                    event_location = self.locations[els]
                                    event_location_str.pop(i)
                                    event_location_details = c.join(event_location_str)
                                    success = True
                        if success:
                            break
                    if not success:
                        parts = event_location_str.split()
                        els = " ".join(parts[:-1])
                        if els in self.locations:
                            event_location = self.locations[els]
                            event_location_details = parts[-1]
                            success = True
                        if not success:
                            els = " ".join(parts[1:])
                            if els in self.locations:
                                event_location = self.locations[els]
                                event_location_details = parts[0]
                                success = True
                            if not success:
                                event_location = ""
                                event_location_details = event_location_str
            else:
                event_location = ""
                event_location_details = ";".join(event_location_objs)

            event_cluster = EventCluster(
                cluster_title = cluster_title,
                cluster_description = cluster_description,
                cluster_user_created = self.user,
            )
            event_cluster.save()
            for cluster_tag in self.cluster_tags:
                event_cluster.cluster_tags.add(cluster_tag)
            event_cluster.save()
            event = Event(
                event_cluster=event_cluster,
                event_date_time_start=event_date_time_start,
                event_date_time_end=event_date_time_end,
                event_location=event_location,
                event_location_details=event_location_details,
                event_user_last_modified=self.user,
                event_attendee_count=0,
            )
            event.save()

            print("Added event '%s' (%s - %s)" % (
                cluster_title, event_date_time_start, event_date_time_end))




def main(base_url, param=None, param_vals=None):
    user = CalUser.objects.get(user_netid='joshchen')
    if param:
        urls = []
        for param_val in param_vals:
            urls.append("%s?%s=%s" % (base_url, param, param_val))
    else:
        urls = [base_url]

    for url in urls:
        page = Page.from_scrape(url,
            user = user,
            tags = ["orientation"],
            container = 'view-p2p-orientation-events',
            event = 'views-row',
            cluster_title = 'field-content orientation-title',
            event_location = 'views-field views-field-field-orientation-location views-field-field-orientation-location',
        )
        page.handle()
