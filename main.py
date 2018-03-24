import logging

logging.info("Started Initialising Instance 09:25")

from jsonschema import validate

# import boto
# import cachetools
# import certifi
# import chardet
# import click
# import cloudpickle
# import firebase_admin
# from github import Github
# import google
# import google.auth
# import google.api
# import google.api_core
# import google.cloud
# import google.logging
# import google.longrunning
# import google.oauth2
# import google.protobuf
# import google.resumable_media
# import google.rpc
# import google.type
# import idna
# import im_debouncedtask
# import im_future
# import im_futuregcscompose
# import im_futuregcsfilesharded
# import im_futurendbsharded
# import im_futuretest
# import im_gcscacher
# import im_memcacher
# import im_gcsfilesharded
# import im_ndbsharded
# import im_qsb
# import im_task
# import im_util
# import integration
# import jinja2
# import jsonschema
# import jwt
# import markupsafe
# import passlib
# import pkg_resources
# import pyasn1
# import pyasn1_modules
# import pystache
# import pytz
# import requests
# import requests_toolbelt
# import rsa
# import simplejson
# import snippets
# import sUTL
# import uritemplate
# import urllib3
# import werkzeug
# import six
# import xmltodict
# 
# 
# import requests #@UnusedImport
# import requests_toolbelt.adapters.appengine
#   
# # Use the App Engine Requests adapter. This makes sure that Requests uses
# # URLFetch.
# requests_toolbelt.adapters.appengine.monkeypatch()

################ minimum
from flask import Flask

app = Flask(__name__)

from handlers.switchboard import get_switchboard
from handlers.report import get_report
from experiments.taskbomb import RegisterTaskBombHandlersForFlask
from im_task_flask import setuptasksforflask

get_switchboard(app)
get_report(app)
setuptasksforflask(app)

from im_futuretest_flask import register_futuretest_handlers
register_futuretest_handlers(app)

RegisterTaskBombHandlersForFlask(app)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

logging.info("Finished Initialising Instance")
