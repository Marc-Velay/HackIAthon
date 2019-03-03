# coding: utf-8 
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
import os.path
import tornado.httpserver
import tornado.options
import tornado.web
from wtforms.fields import IntegerField
from wtforms.validators import Required
from wtforms_tornado import Form
items = []
index = True
symptomes = False
pathologie = False


class SumForm(Form):
    a = IntegerField(validators=[Required()])
    b = IntegerField(validators=[Required()])

class SumHandler(RequestHandler):
    def get(self):
         form = SumForm(self.request.arguments)
         if form.validate():
            self.write(str(form.data['a'] + form.data['b']))

class Index(RequestHandler):
    def get(self):
        dict1 = {"index1":True, "index2":True, "symptomes" : False, "pathologie":False} 
        self.render('test.htm',dict1=dict1)

class Symptomes(RequestHandler):
    def get(self):
        dict1 = {"index1":True, "index2":False, "symptomes" :True , "pathologie":False}
        self.render('test.htm',dict1=dict1)

class Pathologie(RequestHandler):
    def get(self):
        dict1 = {"index1":True, "index2":False, "symptomes" :True , "pathologie":True, }
        self.render('test.htm',dict1=dict1)

class Feedback(RequestHandler):
    def get(self):
        self.render({'templates/feedback.htm'})

def make_app():
    urls = [
        ("/", Index),
        ("/add", SumHandler),
        ("/symptomes", Symptomes),
        ("/pathologie", Pathologie),
        ("/feedback", Feedback)
        ]
    return Application(urls, debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8880)
    IOLoop.current().start()
