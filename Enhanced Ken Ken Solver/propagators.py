#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def compute_domain(var):
    return var.cur_domain()

def prop_FC(csp, newVar=None):
    """Do full inference. If newVar is None we initialize the queue
    with all variables."""
    pruned = []
    var_queue = csp.get_all_vars() if not newVar else [newVar]

    while var_queue:
        y=var_queue.pop()
        for constraint in csp.get_cons_with_var(y):
            for x in constraint.get_scope():
                S = compute_domain(x)
                for v in S:
                    valid_value_exists = constraint.has_support(x, v)
                    if not valid_value_exists:
                        x.prune_value(v)
                        pruned.append((x, v))
                T = compute_domain(x)
                if not T:
                    return False, pruned
    return True, pruned


def prop_FI(csp, newVar=None):
    '''Do full inference. If newVar is None we initialize the queue
       with all variables.'''
    #IMPLEMENT
    inference = []
    var_queue = csp.get_all_vars() if not newVar else [newVar]

    while var_queue:
        y=var_queue.pop()
        for constraint in csp.get_cons_with_var(y):
            for x in constraint.get_scope():
                S = compute_domain(x)
                for v in S:
                    valid_value_exists = constraint.has_support(x, v)
                    if not valid_value_exists:
                        x.prune_value(v)
                        inference.append((x, v))
                T = compute_domain(x)
                if not T:
                    return False, inference
                if S != T and x not in var_queue:
                    var_queue.append(y)
    return True, inference