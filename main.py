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
from google.appengine.ext.db import delete
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
    mark = ndb.FloatProperty(default=0)

class Work(ndb.Model):
    subject = ndb.StringProperty()
    name = ndb.StringProperty(indexed=True)
    mark = ndb.FloatProperty()
    pond = ndb.FloatProperty() #mark % over 100


class SubjectsHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subjects = Subject.query()
        self.works = Work.query()

    def get(self):
        for subject in self.subjects:
            self.works = Work.query(Work.subject == subject.name)
            time.sleep(0.4)
            for work in self.works:
                subject.mark = work.mark * (work.pond/100)
            subject.put()
        time.sleep(0.2)   # not a good fix
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

class DeleteSubjectHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subjectName = self.request.get('subjectToDelete')

    def get(self):
        pass

    def post(self):
        subjectToDelete = Subject.query(Subject.name == self.subjectName )
        for subject in subjectToDelete:
            ndb.delete_multi([subject.key])
        self.redirect("/")

class DeleteWorkHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subjectName = self.request.GET['subject']
        self.workName = self.request.get('workToDelete')
        self.workToDelete = self.subjectName + self.workName

    def get(self):
        template_values = {
            'subjectName': self.subjectName,
        }

        template = JINJA_ENVIRONMENT.get_template("delete_work.html")
        self.response.write(template.render(template_values))

    def post(self):
        worksToDelete = Work.query( Work.name == self.request.get('workToDelete'), Work.subject == self.subjectName )
        for work in worksToDelete:
            ndb.delete_multi([work.key])
        self.redirect("/detailed_subject?subject=" + self.subjectName)

class DetailedSubjectHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subject = Subject(id=self.request.GET['subject'], name=self.request.GET['subject'])
        self.works = Work.query(Work.subject == self.subject.name)

    def get(self):
        for work in self.works:
            self.subject.mark += work.mark * (work.pond/100)
        self.subject.put()
        time.sleep(0.1)   # not a good fix
        template_values = {
            'subject': self.subject,   # send subject to take total mark
            'works': self.works
        }

        template = JINJA_ENVIRONMENT.get_template("detailed_subject.html")
        self.response.write(template.render(template_values))

    def post(self):
        pass

class AddWorkHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.subject = Subject(id=self.request.GET['subject'], name=self.request.GET['subject'])
        self.work = Work(id=self.subject.name + self.request.get('workName'), name=self.request.get('workName'), mark=float(self.request.get('workMark', '0.0')), pond=float(self.request.get('workPonderation', '0.0')), subject=self.subject.name)
        works = Work.query(Work.subject == self.subject.name)
        self.ponds = 0
        for work in works:
            self.ponds += work.pond

    def get(self):
        time.sleep(0.1)   # not a good fix
        # self.response.write(self.subjectName)
        template_values = {
            'subject': self.subject
        }

        template = JINJA_ENVIRONMENT.get_template("add_work.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.works = Work.query(Work.subject == self.subject.name)

        for work in self.works:
            self.subject.mark += work.mark * (work.pond/100)
        self.subject.put()
        newWork = Work(id=self.subject.name + self.work.name, name=self.work.name, mark=self.work.mark, pond=self.work.pond, subject=self.subject.name)
        print(self.ponds)
        if ((100 - self.ponds) >= newWork.pond):
            newWork.put()
        else:
            template_values = {
                'subject': self.subject,
                'pondOver': True
            }

            template = JINJA_ENVIRONMENT.get_template("add_work.html")
            self.response.write(template.render(template_values))
        time.sleep(0.1)   # not a good fix
        self.redirect("/detailed_subject?subject=" + self.subject.name)


app = webapp2.WSGIApplication(
    [('/', SubjectsHandler), ('/detailed_subject', DetailedSubjectHandler),
        ('/add_subject', AddSubjectHandler), ('/add_work', AddWorkHandler),
        ('/delete_subject', DeleteSubjectHandler), ('/delete_work', DeleteWorkHandler)
], debug=True)