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


class Subject(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    mark = ndb.FloatProperty()

class Work(ndb.Model):
    subject = ndb.StructuredProperty(Subject)
    name = ndb.StringProperty(indexed=False)
    mark = ndb.FloatProperty()
    pond = ndb.IntegerProperty() #mark % over 100


class SubjectsHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subject = "ALS"

    def get(self):
        template_values = {
            'subject': self.subject
        }

        template = JINJA_ENVIRONMENT.get_template("subjects.html")
        self.response.write(template.render(template_values))
        self.response.write("subjects get")

    def post(self):
        self.response.write("subjects post")

class DetailedSubjectHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subject = "ALS"
        self.work = "exam1"
        self.mark = 2.00
        self.pond = 0.40
        self.total = self.mark * self.pond

    def get(self):
        template_values = {
            'subject': self.subject,
            'work': self.work,
            'mark': self.mark,
            'pond': self.pond * 100,
            'total': self.total
        }

        template = JINJA_ENVIRONMENT.get_template("detailed_subject.html")
        self.response.write(template.render(template_values))

class AddSubjectHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subjectName = self.request.get("subjectName")


    def __get__(self):
        self.response.write("add get")

    def post(self):
        self.response.write("add post")
        newSubject = Subject(name = self.subjectName)
        newSubject.put()


app = webapp2.WSGIApplication(
    [('/subjects', SubjectsHandler), ('/detailed_subject', DetailedSubjectHandler),
        ('/add_subject', AddSubjectHandler)#, ('/add_work', AddWorkHandler)
], debug=True)
