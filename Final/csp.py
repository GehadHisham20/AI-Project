#return the first element
def first(iterable, default=None):
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

#compare
def is_in(elt, seq):
    return any(x is elt for x in seq)

#count the number of true items
def count(seq):
    return sum(bool(x) for x in seq)

class Problem(object):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal
    
class CSP(Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
    
    #add to assignment
    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1
    
    #remove from assignment
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
    
    #return the number of conflicts
    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    #assign all variables with all constraints satisfied
    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))
    
    #make sure we prune values from domains
    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
    
    #start inferences from assuming var=value
    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    #remove var=value
    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))
    
    #Return all values for var that aren't currently ruled out
    def choices(self, var):
        return (self.curr_domains or self.domains)[var]
    
    #undo
    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])

def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)

def check(csp, Xi, Xj, removals):
    checked = False
    for x in csp.curr_domains[Xi][:]:
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            checked = True
    return checked

#filter function if FC or AC
def ApplyFilter(csp, var, value, assignment, removals,f):
    if f == "FC":
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b):
                        csp.prune(B, b, removals)
                if not csp.curr_domains[B]:
                    return False
        return True
    elif f == "AC3":
        queue = None
        queue= [(x, var) for x in csp.neighbors[var]]
        if queue is None:
            queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
        csp.support_pruning()
        while queue:
            (Xi, Xj) = queue.pop()
            if check(csp, Xi, Xj, removals):
                if not csp.curr_domains[Xi]:
                    return False
                for Xk in csp.neighbors[Xi]:
                    if Xk != Xi:
                        queue.append((Xk, Xi))
        return True

#Backtracking
def BTAlgorithm(csp,filter="None"):
    def BT(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = first_unassigned_variable(assignment, csp)
        for value in unordered_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                inferences= True
                if filter != "None":
                    inferences = ApplyFilter(csp, var, value, assignment, removals, filter)
                if inferences:
                    result = BT(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = BT({})
    assert result is None or csp.goal_test(result)
    return result