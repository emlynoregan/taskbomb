from google.appengine.api.taskqueue import taskqueue
from flask import request
import logging
import json
from im_task import task
import time
from im_futuretest import register_test
from im_future import future, GenerateOnAllChildSuccess, FutureReadyForResult,\
    setlocalprogress

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

        time.sleep(2)        
        
        return "ok"
    

@task(queue="background")
def DoTaskBomb(depth, ix, ballast):
    logging.debug("depth:%s, ix:%s, ballast size:%s" % (depth, ix, len(ballast) if ballast else -1))
    if depth:
        for newix in range(2):
            DoTaskBomb(depth-1, newix, ballast)
    time.sleep(2)        

@task(queue="background")
def DoTaskBombWider(depth, ix, ballast):
    logging.debug("depth:%s, ix:%s, ballast size:%s" % (depth, ix, len(ballast) if ballast else -1))
    if depth:
        for newix in range(4):
            DoTaskBombWider(depth-1, newix, ballast)
    time.sleep(2)        

def TaskBombDepth10UsingTaskExperiment():
    def Go():
        DoTaskBomb(10, 0, None)
    return "Task Bomb, Depth = 10, @task", Go

def TaskBombDepth16UsingTaskExperiment():
    def Go():
        DoTaskBomb(16, 0, None)
    return "Task Bomb, Depth = 16, @task", Go

def TaskBombDepth8UsingWiderExperiment():
    def Go():
        DoTaskBombWider(8, 0, None)
    return "Task Bomb, WIDER, Depth = 8, @task", Go

def TaskBombDepth10UsingWiderExperiment():
    def Go():
        DoTaskBombWider(10, 0, None)
    return "Task Bomb, WIDER, Depth = 10, @task", Go


@register_test(description = "task bomb 4 wide, 7 deep", queue="background")
def TaskBomb4Wide7DeepTest(futurekey):
    def DoTaskBomb(childfuturekey, depth, ix, weight):
        if depth:
            for newix in range(4):
                lchildOnAllChildSuccess = GenerateOnAllChildSuccess(childfuturekey, 0, lambda a,b: a+b)
                future(DoTaskBomb, parentkey = childfuturekey, onallchildsuccessf=lchildOnAllChildSuccess, weight=weight/4, futurename="DoTaskBomb %s, %s, %s" % (depth-1, newix, weight/4), queue="background")(depth-1, newix, weight/4)
            time.sleep(2)
            raise FutureReadyForResult("waiting")
        else:
            time.sleep(2)
            setlocalprogress(childfuturekey, weight)
            return 1

    lonAllChildSuccess = GenerateOnAllChildSuccess(futurekey, 0, lambda a,b: a+b)
    future(DoTaskBomb, parentkey = futurekey, onallchildsuccessf=lonAllChildSuccess, weight=100, futurename="DoTaskBomb %s, %s, %s" % (7, 0, 100), queue="background")(7, 0, 100)

    raise FutureReadyForResult("waiting")

