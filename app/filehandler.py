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

import itertools

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.jvm import JavaLexer

from app import app, mongo
from mappings import api_map


def get_calls_set():
    """
    Retrieves a set of all API method calls for which usage examples have been mined. Used for autocomplete and to avoid
    an unnecessary call to the db in case query is invalid.
    :return: a set of API method calls
    """
    calls_lists = get_calls_dict().values()
    calls_set = set(itertools.chain.from_iterable(calls_lists))
    return calls_set


def get_calls_dict():
    """
    Retrieves the API methods for which usage examples have been mined for all the APIs specified in the mappings.
    :return: a dictionary in the form {'API1': [API_method1, API_method2], 'API2': []}
    """
    calls = dict()
    for api in api_map.keys():
        calls[api] = list(get_api_calls(api))
    return calls


def get_api_calls(api):
    """
    Retrieves the API methods of an API for which usage examples have been mined.
    :param api: library/project for which API usage examples have been mined
    :return: a set of API methods belonging to the API, for which HApiDoc mined examples
    """
    calls = set()
    with app.app_context():
        try:
            project_calls = mongo.db[api].find_one({"type": "list"})
            calls.update(project_calls['calls'])
        except:
            print 'Could not retrieve API calls from the DB.'
    return calls


def get_query_info(query):
    """
    Identifies the project to which the API method call belongs from the query. This is done based on the package name
    and using the provided mappings.
    :param query: the query
    :return: the project and the fully qualified name of the api method (which happens to be the same as the query)
    """
    api_method = query
    for proj, package in api_map.items():
        if query.startswith(package):
            project = proj
    return project, api_method


def post_process_content(org_docs, api_method):
    """
    Processes the content retrieved from mongo before presenting this to the users.
    :param org_docs: documents retrieved from mongo
    :param api_method: the fully qualified name of the target API method
    :return:
    """
    docs = list(org_docs)
    for doc in docs:
        doc['content'] = highlight(doc['content'], JavaLexer(), HtmlFormatter(linenos=True))
        doc['also-calls'] = list(doc['calls'])
        doc['also-calls'].remove(api_method)
    return docs
