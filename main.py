#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

#from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
    extensions=[ "jinja2.ext.autoescape" ],
    autoescape=True)


"""class Subject(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    mark = ndbFloatProperty()

class Work(ndb.Model):
    subject = ndb.StructuredProperty(Subject)
    mark = ndb.FloatProperty()
    pond = ndb.IntegerProperty() #mark % over total
"""


class MainHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subject ="ALS"
        # self.request.get("subject", "ALS")

    def get(self):
        template_values = {
            'subject': self.subject
        }

        template = JINJA_ENVIRONMENT.get_template("subjects.html")
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication(
    [('/subjects', MainHandler)
], debug=True)
