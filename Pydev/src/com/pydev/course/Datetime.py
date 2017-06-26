'''
Created on 2017年6月26日

@author: xusheng
'''

from datetime import datetime, timedelta, timezone

if __name__ == '__main__':
    now = datetime.now()
    utcnow = datetime.utcnow()
    print('now(+8) = %s' % now)
    print('utc now = %s' % utcnow)
    
    construct_dt = datetime(2010, 1, 1, 8, 0)
    ts = construct_dt.timestamp()
    print('ts = %s' % ts)
    print('dt(+8) constructed from ts = %s' % datetime.fromtimestamp(ts))
    print('utc dt constructed from ts = %s' % datetime.utcfromtimestamp(ts))
    
    
    str2dt = datetime.strptime('2010-1-1 08:00:00', '%Y-%m-%d %H:%M:%S')
    print('str2dt(%%Y-%%m-%%d %%H:%%M:%%S) = %s' % str2dt)    
    print('dt2str(Weekday, Month Date Hour:Minute) = %s' % str2dt.strftime('%a, %b %d %H:%M'))
    
    print('now(+8) + 1day1hour = %s' % (now + timedelta(days=1, hours=1)))

    print('now(-1) = %s' % now.astimezone(timezone(-timedelta(hours=1))))