import logging

# logging.info("Entered main.py")

################################################
################################################
# Include these next couple of lines to cause task
# stick, comment out to run cleanly
try:
    for i in xrange(10000):
        logging.debug("these logging statements should set off taskstick")
except:
    pass
################################################
################################################

from flask import Flask

app = Flask(__name__)

from handlers.switchboard import get_switchboard
from handlers.report import get_report
from experiments.taskbomb import RegisterTaskBombHandlersForFlask

get_switchboard(app)
get_report(app)

RegisterTaskBombHandlersForFlask(app)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# logging.info("Left main.py")
