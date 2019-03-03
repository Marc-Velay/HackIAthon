import tornado.ioloop
import tornado.web
import socket
from urllib.parse import urlparse
from neo4j import GraphDatabase
from collections import Counter


class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            querry = session.write_transaction(self._get_pathologies, message)
            print(querry)

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
                    r_final[names.index(r[0])] = r
        else:
            r_final = res
        return r_final

db = HelloWorldExample("bolt://134.157.26.238:7687", user="neo4j", password="toto")
list_sym = ["Leucopenie", "?deme"]
db.print_greeting(list_sym)
