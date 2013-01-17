import emails
import datetime

emails.notify_if_late()
now = datetime.datetime.now()

f = open("/srv/tigerapps/logs/dvd_cron_logs", "a")
f.write(str(now))
f.write("\n")
f.close()

