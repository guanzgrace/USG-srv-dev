from datetime import datetime, timedelta

def get_time_query(timeselect, start_day=None):
    """
    Returns a query object appropriate for the timeselect and start_day
    """
    
    if timeselect == "upcoming":
        title = "Upcoming Events"
        q = Q(event_date_time_start__gte=start_day)
        return (title, q)

    elif timeselect == "day":
        title = "Events - Day"
        end_day = start_day + timedelta(days=1)
    elif timeselect == "week":
        title = "Events - Week"
        start_day -= timedelta(days=start_day.weekday())
        end_day = start_day + timedelta(weeks=1)
    elif timeselect == "month":
        title = "Events - Month"
        start_day -= timedelta(days=start_day.day)
        end_day = start_day + timedelta(weeks=1)

    q = Q(event_date_time_start__gte=start_day, event_date_time_start__lte=end_day)
    return (title, q)
