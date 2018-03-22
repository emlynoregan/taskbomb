from google.appengine.api.taskqueue import taskqueue
from flask import request
import logging

def TaskBombDepth10Experiment(app):
    def Go():
        # implement the taskbomb here
        taskqueue.add(
               url='/taskbomb',
               params={'depth': 10, "ix": 0}
            )

    @app.route('/taskbomb', methods=["POST"])
    def taskbomb():
        depth = int(request.values.get("depth"))
        myix = request.values.get("ix")
        logging.debug("depth: %s" % depth)
        logging.debug("myix: %s" % myix)
        
        if depth:
            for ix in range(2):
                taskqueue.add(
                       url='/taskbomb',
                       params={'depth': depth - 1, "ix": ix}
                    )
        
        return "ok"
    
    return "Task Bomb, Depth = 10", Go

