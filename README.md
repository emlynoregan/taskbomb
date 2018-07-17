# taskbomb
This app is for experimenting with adding many tasks quickly to appengine push queues. It's for investigating the
stuck task issue, which seems to occur under these circumstances.

## Stuck Task issue:
Sometimes, tasks get stuck in "running" state when not running; they have to time out and retry before 
they run properly. On the push queue this takes 10 minutes. 

## How to cause Task stick:
It seems to be caused by touching (?) particular external services in the app engine environment 
during initialisation of an instance. Initialisation is anything that happens while running main.py
(which happens once for an instance), which includes anything that happens when modules included in
main.py run.

The easiest way to make Task Stick happen is by logging anything during instance initialisation. The 
more logging that happens, the more likely Task Stick is to occur.

In this project at the top of main.py you will see a loop which logs 10,000 debug statements. If
you include this in the project, you will very likely see task stick. If you comment it out, task stick
will not occur.

## Other ways to induce Task stick
Many of the google cloud libraries seem to make task stick happen, just by importing. I think happens when you use
the requests toolbelt monkeypatch (the "requests" library is used by a lot of code including google's to make http requests, 
and needs the requests toolbelt monkeypatch to work on app engine). 

Note: I just went looking for the references to the requests toolbelt monkeypatch in the docs, it seems to be gone.
Perhaps this hack is no longer required?

Anyway, if you do have libraries which cause task stick, they'll be used like this:

	import <mylib>

	...

	def SomeFunc():
	    ...
		<mylib>.something(...) # do stuff with the library
		...
		
The workaround is to load <mylib> lazily, like so:

	def SomeFunc():
	    import <mylib>
	    ...
		<mylib>.something(...) # do stuff with the library
		...

This takes it out of the initialization time code.

## How to use this project

1 - Deploy to app engine
2 - Wait until there are no instances running in the background service
3 - Go to taskbomb911.appspot.com
4 - Click "taskbomb, depth = 16"
5 - Go to the cloud console, to the app engine task page

Normal operation: You should see the number of tasks ramp up to the max throughput of the queue, sit there for a few minutes, 
then run down and complete. You'll need to keep refreshing the page.

Task stick: You should see the number of tasks ramp up to the max throughput of the queue, sit there for a few minutes,
the run down to almost zero. You'll see a multiple of 8 tasks (8, 16, 24, 32?) stuck in the queue, just sitting there, for 10 minutes. 
Once they've been there for 10 minutes, they'll timeout and retry and complete immediately. Note the multiple of 8 is because each
instance runs 8 tasks, so each group of 8 represents a deadlocked instance.

