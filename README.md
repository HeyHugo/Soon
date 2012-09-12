Soon
====

In process async scheduling library using [gevent](http://www.gevent.org/), schedule functions to execute at a certain time or by an interval.


Usage
-----

Import and initialize
	from soon Import Soon

	''' It's highly likely you want the following two imports as well as monkey patching '''
	import gevent 
	from gevent import monkey

	monkey.patch_all() # monkey is your friend
	
	soon = Soon()

Define a function we can use for show:
	def task():
		print "executing a task!"
	
Schedule a task to execute in 1 day and 3 hours:
	soon.schedule(task, start={"days":1, "hours":3})
	
Schedule a task to execute 2012-10-01 05.00 pm:
	from datetime import datetime
	soon.schedule(task, start=datetime(2012, 10, 1, 17, 0))
	
Schedule a task to execute every 30 seconds:
	soon.schedule(interval=30)
	
Schedule a task to execute every 30 minutes, starting from 2012-10-01 05.00 pm:
	soon.schedule(task, start=datetime(2012, 10, 1, 17, 0), interval={"minutes":30})
	
Return a list with names of all scheduled tasks
	soon.list()
	
Unschedule a task:
	soon.unschedule("taskname")

Pass schedule the keyword arg `name` to specify a name for your task

Clear all scheduled tasks:
	soon.clear()