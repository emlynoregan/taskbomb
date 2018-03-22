from flask import render_template, request, redirect
 
from experiments.taskbomb import TaskBombDepth10Experiment, TaskBombDepth16Experiment,\
    TaskBombDepth10WithBallastExperiment, TaskBombDepth16WithBallastExperiment, \
    TaskBombDepth10UsingTaskExperiment, TaskBombDepth16UsingTaskExperiment, \
    TaskBombDepth8UsingWiderExperiment, TaskBombDepth10UsingWiderExperiment

def get_switchboard(app):
    experiments = [
        TaskBombDepth10Experiment(),
        TaskBombDepth16Experiment(),
        TaskBombDepth10WithBallastExperiment(),
        TaskBombDepth16WithBallastExperiment(),
        TaskBombDepth10UsingTaskExperiment(),
        TaskBombDepth16UsingTaskExperiment(),
        TaskBombDepth8UsingWiderExperiment(),
        TaskBombDepth10UsingWiderExperiment()
    ]

    @app.route('/', methods=["GET", "POST"])
    def switchboard():
        if request.method == "GET":
            return render_template("switchboard.html", experiments = enumerate(experiments))
        else:
            if not request.form.get("run") is None:
                index = int(request.form.get("run"))
                experiment = experiments[index]
                _ = experiment[1]() # runs the experiment
                reporturl = "report" #%s" % (("?key=%s" % resultobj.urlsafe()) if resultobj else "")
                return redirect(reporturl)
