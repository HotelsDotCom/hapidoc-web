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

import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_pymongo import PyMongo


mongodb_host = os.environ['MONGO_DB_HOST']
mongodb_port = os.environ['MONGO_DB_PORT']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hapidoc'
app.config['MONGO_DBNAME'] = 'hapidocdb'
app.config['MONGO_URI'] = 'mongodb://' + mongodb_host + ":" + mongodb_port + '/' + app.config['MONGO_DBNAME']

mongo = PyMongo(app)
bs = Bootstrap(app)
manager = Manager(app)

from app import views
