import data.db_access as dba
import rdflib
from rdflib import Graph, Literal, URIRef, BNode

class QueryFilter:
    def __init__(self, varname):
        pass


class QueryBuilder:
    def __init__(self, distinct=False, vars=None):
        self.proplist = []
        self.filterlist = []
        self.distinct = distinct
        self.varlist = set()
        if vars is not None:
            for v in vars:
                self.varlist.add(v)

    # prop in form (subject, predicate, object)
    # subject either string or rdflib BNode
    # predicate either string or reflib URIRef
    # object either string or rdflib BNode or rdflib Literal
    # if isfinalvar is true, variables will be added to select statement
    def add_property(self, prop, isfinalvar = False):
        self.proplist.append(prop)
        for p in prop:
            if not (isinstance(p, Literal) or isinstance(p, BNode) or isinstance(p, URIRef)) and isfinalvar:
                self.varlist.add(p)

    def format_var(self, varname):
        return '?' + str(varname)

    def format_subject(self, subj):
        subj_str = ''
        if isinstance(subj, BNode):
            subj_str = subj.n3()
        elif isinstance(subj, str):
            subj_str = '?' + subj
        else:
            raise Exception('incorrect subject type')
        return subj_str

    def format_predicate(self, pred):
        pred_str = ''
        if isinstance(pred, URIRef):
            pred_str = pred.n3()
        elif isinstance(pred, str):
            pred_str = '?' + pred
        else:
            raise Exception('incorrect predicate type')
        return pred_str

    def format_object(self, obj):
        obj_str = ''
        if isinstance(obj, Literal) or isinstance(obj, BNode) or isinstance(obj, URIRef):
            obj_str = obj.n3()
        elif isinstance(obj, str):
            obj_str = '?' + obj
        else:
            raise Exception('incorrect object type')
        return obj_str

    def get_query_text(self):
        variables_string = ' '.join([self.format_var(x) for x in self.varlist]).strip() if len(self.varlist) > 0 else '*'
        query = 'SELECT '
        query += 'DISTINCT ' if self.distinct else ''
        query += variables_string
        query += ' WHERE { \n'
        for p in self.proplist:
            query += f'{self.format_subject(p[0])} {self.format_predicate(p[1])} {self.format_object(p[2])} .\n'
        query += '}'

        return query