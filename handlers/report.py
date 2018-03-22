from flask import render_template

def get_report(app):
    @app.route('/report', methods=["GET", "POST"])
    def report():
        return render_template(
            "report.html"
        )
        
#         keystr = request.args.get('key')
#         level = int(request.args.get('level', 0))
#         key = ndb.Key(urlsafe=keystr) if keystr else None
#         obj = key.get() if key else None
#         if obj:
#             if request.method == "POST":
#                 cancel = request.form.get("cancel")
#                 if cancel:
#                     obj.cancel()
# 
#             def futuremap(future, flevel):
#                 if future:
#                     urlsafe = future.key.urlsafe()
#                     return "<a href='report?key=%s&level=%s'>%s</a>" % (urlsafe, flevel, urlsafe)
#                 else:
#                     return None
#                 
#             objjson = obj.to_dict(level = level, maxlevel = level + 5, futuremapf = futuremap)
# 
#             return render_template(
#                 "report.html", 
#                 objjson = json.dumps(objjson, sort_keys=True, indent=2),
#                 keystr = keystr,
#                 iscancellable = isinstance(obj, _Future) and not obj.has_result()
#             )
#         else:
#             return render_template(
#                 "report.html"
#             )
            

    return report

