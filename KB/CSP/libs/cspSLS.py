from KB.CSP.libs.cspProblem import CSP, Constraint
from KB.CSP.libs.display import Displayable
import random

class SLSearcher(Displayable):
    def __init__(self, csp):
        self.csp = csp
        self.variables_to_select = {var for var in self.csp.variables if len(var.domain) > 1}
        self.current_assignment = None

    def search(self, max_steps, prob_best=1.0, prob_anycon=1.0):
        # Implementazione semplificata del motore SLS
        self.current_assignment = {var: random.choice(var.domain) for var in self.csp.variables}
        for i in range(max_steps):
            if self.csp.consistent(self.current_assignment):
                return self.current_assignment
            # Logica di flip dei valori per minimizzare i conflitti...
        return self.current_assignment