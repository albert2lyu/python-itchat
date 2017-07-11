from datetime import datetime
now = datetime.now()
print(now, type(now))
dt_time = datetime(1970, 1, 3, 0, 0, 0)
print(dt_time.strftime('%Y-%m-%d %H:%M:%S'))
print(dt_time.timestamp())
print(datetime.fromtimestamp(0.0))
