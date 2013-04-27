from datetime import datetime

def log(line):
	filename = '/srv/tigerapps/logs/pounce_logs/log.txt'
	file = open(filename, 'a')
	time = str(datetime.now())
	message = time + ':  ' + line + '\n'
	file.write(message)
	print message
	file.close()