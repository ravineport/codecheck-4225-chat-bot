#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from SPARQLWrapper import SPARQLWrapper, JSON


class Bot():
    # Please write your code here.
    def __init__(self):
        self.sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')

    def recv_message(self, msg):
        msg = msg.strip()
        if re.match('bot', msg) == None or msg == 'bot':
            return None
        command_list = re.split(' +', msg)[1:]

        # ping pong
        if command_list[0] == 'ping':
            return 'pong'

        # abstract a word
        if command_list[0] == 'abst':
            return self.abst_word(command_list[1])

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connector.commit()
        except MySQLdb.Error, e:
            return 'error!'
        return ''

    def abst_word(self, word):
        query = u"""
            PREFIX abst: <http://dbpedia.org/ontology/abstract>
            SELECT ?x
            WHERE {{ <http://ja.dbpedia.org/resource/{}> abst: ?x .}}
        """.format(word.decode('utf-8'))
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return results['results']['bindings'][0]['x']['value']


if __name__ == '__main__':
    my_bot = Bot()
    input = raw_input().decode('utf-8')
    print my_bot.abst_word(input)
