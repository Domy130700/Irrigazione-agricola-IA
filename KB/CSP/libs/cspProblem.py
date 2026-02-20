import random

class Variable(object):
    def __init__(self, name, domain, position=None):
        self.name = name   
        self.domain = list(domain) 
        self.position = position if position else (random.random(), random.random())
        self.size = len(domain)

    def __str__(self): return self.name
    def __repr__(self): return self.name

class Constraint(object):
    def __init__(self, scope, condition, string=None, position=None):
        self.scope = scope
        self.condition = condition
        self.string = string
        self.position = position

    def can_evaluate(self, assignment):
        return all(v in assignment for v in self.scope)

    def holds(self, assignment):
        return self.condition(*tuple(assignment[v] for v in self.scope))

class CSP(object):
    def __init__(self, title, variables, constraints):
        self.title = title
        self.variables = variables
        self.constraints = constraints
        self.var_to_const = {var:set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def consistent(self, assignment):
        return all(con.holds(assignment) for con in self.constraints if con.can_evaluate(assignment))