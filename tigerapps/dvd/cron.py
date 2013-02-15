import emails
import datetime

emails.notify_if_late()
now = datetime.datetime.now()

f = open("/srv/logs/dvd_cron.log", "a")
f.write(str(now))
f.write("\n")
f.close()

