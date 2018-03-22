# taskbomb
This app is for experimenting with adding many tasks quickly to appengine push queues. It's for investigating the
stuck task issue, which seems to occur under these circumstances.

## Stuck Task issue:
Sometimes, tasks get stuck in "running" state when not running; they have to time out and retry before they run properly. On the push queue 
this takes 10 minutes. 

What is "sometimes"? That's what I'm trying to characterize.
