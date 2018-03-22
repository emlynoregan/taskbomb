from google.appengine.api.taskqueue import taskqueue
from flask import request
import logging
import json

def TaskBombDepth10Experiment():
    def Go():
        AddTask({'depth': 10, "ix": 0})

    return "Task Bomb, Depth = 10", Go

def TaskBombDepth12Experiment():
    def Go():
        AddTask({'depth': 12, "ix": 0})

    return "Task Bomb, Depth = 12", Go

def TaskBombDepth14Experiment():
    def Go():
        AddTask({'depth': 14, "ix": 0})

    return "Task Bomb, Depth = 14", Go

def TaskBombDepth16Experiment():
    def Go():
        AddTask({'depth': 16, "ix": 0})

    return "Task Bomb, Depth = 16", Go

def TaskBombDepth10WithBallastExperiment():
    def Go():
        AddTask({'depth': 10, "ix": 0, "ballast": "x"*80000})

    return "Task Bomb, Depth = 10, Ballast", Go

def TaskBombDepth16WithBallastExperiment():
    def Go():
        AddTask({'depth': 16, "ix": 0, "ballast": "x"*80000})

    return "Task Bomb, Depth = 16, Ballast", Go

def AddTask(payload):
    task = taskqueue.Task(url="/taskbomb", payload=json.dumps(payload))
    return task.add("background")

def RegisterTaskBombHandlersForFlask(app):
    @app.route('/taskbomb', methods=["POST"])
    def taskbomb():
        lpayload = json.loads(request.data)
        depth = int(lpayload.get("depth"))
        logging.debug("depth: %s" % depth)
        logging.debug("myix: %s" % lpayload.get("ix"))
        logging.debug("ballast size: %s" % len(lpayload.get("ballast") or ""))
        
        if depth:
            for ix in range(2):
                lpayload["depth"] = depth - 1
                lpayload["ix"] = ix
                AddTask(lpayload)
        
        return "ok"
    

