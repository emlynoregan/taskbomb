from google.appengine.api.taskqueue import taskqueue
from flask import request
import logging

def TaskBombDepth10Experiment():
    def Go():
        # implement the taskbomb here
        taskqueue.add(
               url='/taskbomb',
               params={'depth': 10, "ix": 0}
            )

    return "Task Bomb, Depth = 10", Go

def TaskBombDepth12Experiment():
    def Go():
        # implement the taskbomb here
        taskqueue.add(
               url='/taskbomb',
               params={'depth': 12, "ix": 0}
            )

    return "Task Bomb, Depth = 12", Go

def TaskBombDepth14Experiment():
    def Go():
        # implement the taskbomb here
        taskqueue.add(
               url='/taskbomb',
               params={'depth': 14, "ix": 0}
            )

    return "Task Bomb, Depth = 14", Go

def TaskBombDepth16Experiment():
    def Go():
        # implement the taskbomb here
        taskqueue.add(
               url='/taskbomb',
               params={'depth': 16, "ix": 0}
            )

    return "Task Bomb, Depth = 16", Go

def RegisterTaskBombHandlersForFlask(app):
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
    

