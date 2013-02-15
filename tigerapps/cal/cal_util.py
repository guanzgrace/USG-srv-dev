from datetime import datetime

def strftime_yearopt(dt, fmt, comma=True):
    this_year = datetime.today().year
    if dt.year == this_year:
        return dt.strftime(fmt)
    if comma:
        return dt.strftime(fmt + ", %Y")
    return dt.strftime(fmt + " %Y")
