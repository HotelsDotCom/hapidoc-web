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

from wtforms import StringField
from wtforms.validators import DataRequired

try:
    from flask_wtf import FlaskForm as Form
except ImportError:
    from flask_wtf import Form


class SearchForm(Form):
    search_form = StringField(render_kw={"placeholder": "type method"}, id='search-form-input',
                              validators=[DataRequired()])
