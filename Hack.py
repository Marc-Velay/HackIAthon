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
import socket
from urllib.parse import urlparse
from neo4j import GraphDatabase
from collections import Counter
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
        items = db.get_symptomes()
        print(items)
        dict1 = {"index1":True, "index2":True, "symptomes" : False, "pathologie":False,"Symptome_list":items} 
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

class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_pathologies(self, name_list):
        with self._driver.session() as session:
            querry = session.write_transaction(self._get_pathologies, name_list)
            return querry

    def get_symptomes(self):
        with self._driver.session() as session:
            querry = session.write_transaction(self._get_symptomes)
            return querry

    @staticmethod
    def _get_symptomes(tx):
        res = []
        for result in tx.run("MATCH (n:Sym) return n.name"):
            res.append(result[0])
        return res

    @staticmethod
    def _get_pathologies(tx, name_list):
        res = []
        for name in name_list:
            for result in tx.run("MATCH (a:Sym)-[r]->(f) "
                             "WHERE a.name = {name} "
                             "RETURN f.name, f.phenotype, r.strength", name=name):
                res.append((result[0]+' '+result[1], result[2]))
            counter = Counter([r[0] for r in res])
            if len(name_list) > 1:
                names = [name for name in counter if counter[name] == len(name_list)]
                res = [r for r in res if any(name in r for name in names)]
                strengths = [float(0)]*len(names)
                r_final = [0]*len(names)
                for r in res:
                    fl = float(r[1].replace(',', '.'))
                    if fl>strengths[names.index(r[0])]:
                        strengths[names.index(r[0])] = fl
                        r_final[names.index(r[0])] = range
                    else:
                        r_final = res
                return r_final
            
    

db = HelloWorldExample("bolt://134.157.26.238:7687", user="neo4j", password="toto")

def make_app():
    urls = [
        ("/", Index),
        ("/add", SumHandler),
        ("/symptomes", Symptomes),
        ("/pathologie", Pathologie),
        ("/feedback", Feedback),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {
            "path": "./images"
        })
        ]
    return Application(urls, debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8880)
    IOLoop.current().start()
