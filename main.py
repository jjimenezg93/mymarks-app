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
import time

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
    subject = ndb.StringProperty()
    name = ndb.StringProperty(indexed=False)
    mark = ndb.FloatProperty()
    pond = ndb.IntegerProperty() #mark % over 100


class SubjectsHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subjects = Subject.query()

    def get(self):
        time.sleep(0.125)   # not a good fix
        template_values = {
            'subjects': self.subjects
        }

        template = JINJA_ENVIRONMENT.get_template("subjects.html")
        self.response.write(template.render(template_values))

    def post(self):
        pass

class AddSubjectHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subjectName = self.request.get('subjectName')

    def get(self):
        pass

    def post(self):
        newSubject = Subject(id = self.subjectName, name = self.subjectName)
        newSubject.put()
        self.redirect("/")

class DetailedSubjectHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        print(self.request.GET)
        self.subjectName = self.request.GET['subject']
        self.works = Work.query(Work.subject == self.subjectName)
        # self.work = Work(subject="ALS", name="examen", mark=5, pond=45)

    def get(self):
        time.sleep(0.125)   # not a good fix
        self.response.write(self.subjectName)
        template_values = {
            'name': self.subjectName
        }

        template = JINJA_ENVIRONMENT.get_template("detailed_subject.html")
        self.response.write(template.render(template_values))

    def post(self):
        pass

class AddWorkHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.workName = self.request.get("workName")
        self.workMark = float(self.request.get("workMark"))
        self.workPonderation = int(self.request.get("workPonderation"))

    def get(self):
        pass

    def post(self):
        newWork = Work(id=self.workName, subject="ALS", name=self.workName, mark=self.workMark, pond=self.workPonderation)
        newWork.put()
        self.redirect("/detailed_subject?subject=" + self.request.GET['subject'])


app = webapp2.WSGIApplication(
    [('/', SubjectsHandler), ('/detailed_subject', DetailedSubjectHandler),
        ('/add_subject', AddSubjectHandler), ('/add_work', AddWorkHandler)
], debug=True)
