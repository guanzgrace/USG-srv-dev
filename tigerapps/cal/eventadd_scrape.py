from BeautifulSoup import BeautifulSoup
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




class Page(object):

    def __init__(self, content, cluster_user_created, tags=[], **kwargs):
        self.content = content
        self.cluster_user_created = cluster_user_created
        self.tags = tag_names_to_tags(tags)
        self.kwargs = kwargs
        self.locations = invert_bldg_info()


    @classmethod
    def from_scrape(cls, url, **kwargs):
        resp = requests.get(url)
        return cls(resp.content, **kwargs)


    def handle(self):
        bs = BeautifulSoup(self.content)
        if 'container' in self.kwargs:
            bs = bs.find("div", self.kwargs['container'])

        # TODO
        tmp_day = bs.find(class="view-content").find("h3").find("div").attrs['class']

        # Get all div's with a certain class.
        bs_events = bs.findAll("div", self.kwargs['event'])
        for bs_event in bs_events:

            bs_title = bs_event.find(class=self.kwargs['cluster_title']).find('a')
            cluster_title = bs_title.content
            cluster_url = bs_title.attrs['href']

            cluster_description = bs_event.find('p').content
            cluster_description += "<p>Path to Princeton link: <a href='%s'>%s</a>" % (
                cluster_url, cluster_url)

            # TODO
            tmp_starttime = bs_event.find(class="date-display-start").content
            if len(tmp_starttime.split(":")[0]) == 1:
                tmp_starttime = '0' + tmp_starttime
            if tmp_starttime.endswith('a.m.'):
                tmp_starttime.replace('a.m.', 'AM')
            else:
                tmp_starttime.replace('p.m.', 'PM')
            tmp_endtime = bs_event.find(class="date-display-end").content
            if len(tmp_endtime.split(":")[0]) == 1:
                tmp_endtime = '0' + tmp_endtime
            if tmp_endtime.endswith('a.m.'):
                tmp_endtime.replace('a.m.', 'AM')
            else:
                tmp_endtime.replace('p.m.', 'PM')
            event_date_time_start = datetime.strptime(
                "%s %s" % (tmp_day, tmp_starttime),
                "%B%d %I:%M %p")
            event_date_time_end = datetime.strptime(
                "%s %s" % (tmp_day, tmp_endtime),
                "%B%d %I:%M %p")

            # TODO
            event_location_str = bs_event.find(class=kwargs['event_location']).content.lower()
            if event_location_str in self.locations:
                event_location = self.bldg_info[event_location_str]
                event_location_details = None
            else:
                event_location = None
                event_location_details = event_location_str

            event_cluster = EventCluster(
                cluster_title = cluster_title,
                cluster_description = cluster_description,
                cluster_user_created = self.cluster_user_created,
                cluster_tags = self.cluster_tags,
            )
            event = Event(
                event_cluster=event_cluster,
                event_date_time_start=event_date_time_start,
                event_date_time_end=event_date_time_end,
                event_location=event_location,
                event_location_details=event_location_details,
            )
            event_cluster.save()
            event.save()

            logging.info("Added event '%s' (%s - %s)" % (
                event_title, event_start_time, event_end_time))




def main(url):
    user = CalUser.get(username='joshchen')
    page = Page(url,
        cluster_user_created=user,
        tags="orientation",
        container='view-p2p-orientation-events',
        event='views-row',
        cluster_title='orientation-title',
        event_location='views-label-field-orientation-location',
    )
    page.handle()
