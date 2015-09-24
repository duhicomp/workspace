__author__ = "Eric Christoffersen"

import os

from flask import Flask, request, jsonify, session, render_template
import flask

from app import models
from app import db
from app import app

def printsession(f):
    def inner(*args, **kwargs):
        print session
        return f(*args, **kwargs)
    return inner

# Set up Routes
# @app.route('/')
# @printsession
# #@login_required
# def index():
#     print session
#     #return "test"
#     return render_template("index.html")

class DocumentFactorySolutionsView(flask.views.MethodView):
    def get(self):
        return render_template('index.html')

app.add_url_rule('/', view_func=DocumentFactorySolutionsView.as_view('dfs_view'), methods=['GET'])

@app.route('/jobproperties')
def jobprops():
    return render_template("jobproperties.html")

@app.route('/test')
def testing():
    return render_template("test.html")

@app.route('/configuration/jobproperties')
def interface_job_properties():
    curr_page = request.args.get("page", "1")
    try:
        curr_page = int(curr_page)
    except:
        curr_page = 1
    job_types = models.JobType.query.all()
    job_types_paginate = models.JobType.query.paginate(curr_page, 2, False)
    print job_types_paginate.total
    return render_template("jobtypes.html", job_types=job_types_paginate)
