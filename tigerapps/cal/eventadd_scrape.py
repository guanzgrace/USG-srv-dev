"""
This was used to scrape the path to princeton site in fall 2013.

The ultimate goal was to use this experience to learn how to
devise a general algorithm for scraping events from sites.

Unfortunately, given the complexity of this one assignment alone,
such a general algorithm seems way too hard...
"""

from BeautifulSoup import BeautifulSoup, NavigableString
from datetime import datetime, timedelta
import logging
import re
import requests

from cal.models import CalUser, Event, EventCategory, EventCluster




def invert_bldg_info():
    from pom.bldg_info import BLDG_INFO
    locations = {}
    alt_locations = set()
    for bldg_code, (name, alt_names, show) in BLDG_INFO.iteritems():
        locations[name] = bldg_code
        for alt_name in alt_names:
            locations[alt_name] = bldg_code
            alt_locations.add(alt_name)
    return locations, alt_locations


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


def parse_time(unparsed_day, unparsed_time):
    """Parse unparsed_time on path to princeton website."""
    if len(unparsed_time.split(":")[0]) == 1:
        unparsed_time = '0' + unparsed_time
    if unparsed_time.endswith('a.m.'):
        unparsed_time.replace('a.m.', 'AM')
    else:
        unparsed_time.replace('p.m.', 'PM')
    return datetime.strptime(
        "%s %s" % (unparsed_day, unparsed_time),
        "%B %d%Y %I:%M %p")




class Page(object):

    def __init__(self, content, user, tags=[], **kwargs):
        self.content = content
        self.user = user
        self.cluster_tags = tag_names_to_tags(tags)
        self.kwargs = kwargs
        self.locations, self.alt_locations = invert_bldg_info()


    @classmethod
    def from_scrape(cls, url, **kwargs):
        kwargs['url'] = url
        resp = requests.get(url)
        print "Scraped %s" % url
        return cls(resp.content, **kwargs)


    def handle(self):
        bs = BeautifulSoup(self.content)
        if 'container' in self.kwargs:
            # TODO
            bs = bs.find("div", self.kwargs['container']).find("div", "view-content")

        ele = bs.find('h3')
        tmp_day = ele.text.split(',')[-1].strip()
        tmp_day += str(datetime.today().year)

        while ele.nextSibling:
            ele = ele.nextSibling
            if type(ele) == NavigableString:
                continue
            elif ele.name == 'h3':
                tmp_day = ele.text.split(',')[-1].strip()
                tmp_day += str(datetime.today().year)
            elif ele.name == 'div':
                # Get all div's with a certain class.
                bs_event = ele

                bs_title = bs_event.find(attrs={'class':self.kwargs['cluster_title']}).find('a')
                cluster_title = bs_title.string

                tmp_description = bs_event.find('p')
                if tmp_description:
                    cluster_description = strip_tags(unicode(bs_event.find('p')), ['a'])
                else:
                    cluster_description = ""
                if 'url' in self.kwargs:
                    cluster_url = "http://path.princeton.edu" + bs_title['href']
                    cluster_description += ("<p>Note: This event was automatically added from"
                        " <a href='http://path.princeton.edu'>Path to Princeton</a>, and may not"
                        " be fully accurate.  Click <a href='%s'>here</a> for the original event.</p>"
                        % (cluster_url,))

                # TODO
                tmp_starttime = bs_event.find(attrs={'class':"date-display-start"})
                if tmp_starttime:
                    tmp_starttime = tmp_starttime.text
                    event_date_time_start = parse_time(tmp_day, tmp_starttime)
                    tmp_endtime = bs_event.find(attrs={'class':"date-display-end"}
                        ).text
                    event_date_time_end = parse_time(tmp_day, tmp_endtime)
                else:
                    tmp_starttime = bs_event.find(attrs={'class':"date-display-single"}
                        ).text
                    event_date_time_start = parse_time(tmp_day, tmp_starttime)
                    event_date_time_end = event_date_time_start + timedelta(hours=1)

                # TODO
                tmp_location = bs_event.find(attrs={'class':self.kwargs['event_location']})
                if tmp_location:
                    event_location_objs = tmp_location.find(attrs={'class':'field-content'}).findAll('li')
                    if len(event_location_objs) == 1:
                        event_location_str = event_location_objs[0].text
                        success = False
                        if event_location_str in self.locations:
                            event_location = self.locations[event_location_str]
                            if event_location_str in self.alt_locations:
                                event_location_details = event_location_str
                            else:
                                event_location_details = ""
                        else:
                            # Try various methods..
                            for c in [", ", " - "]:
                                if c in event_location_str:
                                    parts = event_location_str.split(c)
                                    for i, els in enumerate(parts):
                                        if els in self.locations:
                                            event_location = self.locations[els]
                                            parts.pop(i)
                                            event_location_details = c.join(parts)
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
                        event_location_details = "; ".join([
                            elo.text for elo in event_location_objs])
                else:
                    event_location = ""
                    event_location_details = ""

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

                print (u"Added event '%s' (%s - %s)" % (
                    cluster_title,
                    event_date_time_start,
                    event_date_time_end)).encode('ascii', 'ignore')




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
            event_location = 'views-field views-field-field-orientation-location',
        )
        page.handle()
