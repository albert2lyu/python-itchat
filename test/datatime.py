from datetime import datetime
now = datetime.now()
print(now, type(now))
dt_time = datetime(2015, 12, 12, 13, 12, 23)
print(dt_time.strftime('%Y-%m-%d %H:%M:%S'))
