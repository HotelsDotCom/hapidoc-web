"""
Copyright (C) 2018 Expedia Group.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import os
import time

import requests
from flask import render_template, redirect, url_for, jsonify, request

from app import app, mongo, mongodb_host, mongodb_port
from filehandler import get_calls_dict, get_calls_set, get_query_info, post_process_content
from forms import SearchForm

web_pass = os.environ['HAPIDOC_WEB_PASS']

# get all calls
calls = get_calls_set()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Endpoint that servers the home page. Can be used for searching.
    """
    form = SearchForm(request.form)
    # in case of invalid call don't do anything
    if form.search_form.data not in calls:
        return render_template('index.html', form=form)

    return redirect(url_for('search_results', query=form.search_form.data))


@app.route('/search_results/<query>', methods=['GET', 'POST'])
def search_results(query):
    """
    Endpoint used for showing results. Can also be used for searching.
    :param query: the query
    """
    form = SearchForm(request.form)
    # check if this is a new search from the results endpoint
    if form.search_form.data in calls:
        return redirect(url_for('search_results', query=form.search_form.data))
    project, api_method = get_query_info(query)
    mongo_docs = mongo.db[project].find({'type': 'result', 'calls': api_method})
    docs = post_process_content(mongo_docs, api_method)

    return render_template('results.html', form=form, data=docs)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """
    Endpoint called for autocomplete.
    """
    search = request.args.get('term')
    app.logger.debug(search)

    return jsonify(json_list=list(calls))


@app.route('/refresh', methods=['POST'])
def refresh():
    """
    Endpoint called by HApiDocIndexer whenever new content has been indexed.
    A call to this endpoints triggers a call to mongo to retrieve the updated content
    """
    if request.json['pass'] == web_pass:
        global calls
        calls = get_calls_set()
        return 'Re-indexing...'


@app.route('/calls', methods=['GET'])
def get_calls():
    """
    Returns the APIs and their method calls for which usage examples have been mined in a JSON format.
    """
    return jsonify(get_calls_dict())


@app.route('/healthcheck', methods=['GET'])
def health_check():
    """
    Performs a healthcheck in the service and in the db.
    """
    mongo_request = requests.get('http://' + mongodb_host + ':' + mongodb_port)
    mongo_healthy = mongo_request.status_code == 200
    cur_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    health_info = {
        'hapidocweb': {'healthy': True, 'message': cur_time},
        'mongo': mongo_healthy
    }

    return jsonify(health_info)
