import time
import gevent
from datetime import datetime

class Soon(object):

    def __init__(self):
        self.register = {}
         
    def schedule(self, func, *args, **kw_args):
        name = kw_args.pop("name", None)
        start = kw_args.pop("start", None)
        interval = kw_args.pop("interval", None)
        
        if interval is not None:
            if isinstance(interval, dict):
                interval = interval.get("days", 0) * 86400 + interval.get("hours", 0) * 3600 + interval.get("minutes", 0) * 60 + interval.get("seconds", 0)
        
        if isinstance(start, datetime):
            delay = (start - datetime.now()).total_seconds()
        elif isinstance(start, dict):
            delay = start.get("days", 0) * 86400 + start.get("hours", 0) * 3600 + start.get("minutes", 0) * 60 + start.get("seconds", 0)
        else:
            delay = interval
            
        if name is None:
            name = func.__name__
            
        if interval is not None:
            self.register[name] = gevent.spawn_later(delay, self.schedule_interval, func, name, interval, *args, **kw_args)
        else:
            self.register[name] = gevent.spawn(self.schedule_once, func, delay, name)
            
    def schedule_interval(self, func, name, interval, *args, **kw_args):
        gevent.spawn(func, *args, **kw_args)
        self.register[name] = gevent.spawn_later(interval, self.schedule_interval, func, name, interval, *args, **kw_args)
    
    def schedule_once(self, func, delay, name):
        gevent.sleep(delay)
        func()
        del self.register[name]
    
    def unschedule(self, name):
        if name in self.register:
            gevent.kill(self.register[name])
            del self.register[name]
    
    def clear(self):
        for key in register:
            self.unschedule(key)
        
    def list(self):
        return [name for name in self.register]
            
