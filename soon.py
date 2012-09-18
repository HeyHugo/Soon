import gevent
from gevent import monkey
from datetime import datetime

monkey.patch_all()

__all__ = ("schedule", "unschedule", "clear", "list")

_register = {}
         
def schedule(func, *args, **kw_args):

    def schedule_interval(func, name, interval, *args, **kw_args):
        gevent.spawn(func, *args, **kw_args)
        _register[name] = gevent.spawn_later(interval, schedule_interval, func, name, interval, *args, **kw_args)
    
    def schedule_once(func, delay, name, *args, **kw_args):
        gevent.sleep(delay)
        func(*args, **kw_args)
        del _register[name]

    name = kw_args.pop("name", None)
    start = kw_args.pop("start", None)
    interval = kw_args.pop("interval", None)
    
    if isinstance(start, datetime):
        delay = (start - datetime.now()).total_seconds()
    elif isinstance(start, dict):
        delay = start.get("days", 0) * 86400 + start.get("hours", 0) * 3600 + start.get("minutes", 0) * 60 + start.get("seconds", 0)
    else:
        delay = start
        
    if name is None:
        name = func.__name__
        
    if interval is not None:
    
        if isinstance(interval, dict):
            interval = interval.get("days", 0) * 86400 + interval.get("hours", 0) * 3600 + interval.get("minutes", 0) * 60 + interval.get("seconds", 0)
            
        if delay is None:
            delay = interval

        _register[name] = gevent.spawn_later(delay, schedule_interval, func, name, interval, *args, **kw_args)
        
    else:
        _register[name] = gevent.spawn(schedule_once, func, delay, name, *args, **kw_args)
        
def unschedule(name):
    if name in _register:
        gevent.kill(_register[name])
        del _register[name]

def clear():
    for key in _register:
        unschedule(key)
    
def list():
    return [name for name in _register]