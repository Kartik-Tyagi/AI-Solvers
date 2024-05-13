#Look for #IMPLEMENT tags in this file.
'''
All encodings need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = caged_csp(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the FunPuzz puzzle.

The grid-only encodings do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - An enconding of a FunPuzz grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - An enconding of a FunPuzz grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. caged_csp (worth 25/100 marks) 
    - An enconding built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with FunPuzz cage constraints.

'''
from cspbase import *
import itertools

def allDiff(ls):
    return len(ls) == len(set(ls))

def binary_ne_grid(fpuzz_grid):
    ##IMPLEMENT
    n = fpuzz_grid[0][0]
    variables = [[Variable(f"V_{i}_{j}", list(range(1, n + 1))) for j in range(n)] for i in range(n)]
    csp = CSP("Binary Grid", [var for sublist in variables for var in sublist])
    
    varDoms = [variables[0][i].domain() for i in range(2)]
    
    sat_tuples = []
    for t in itertools.product(*varDoms):
        #NOTICE use of * to convert the list v to a sequence of arguments to product
        if allDiff(t):
            sat_tuples.append(t)

    for i in range(n):
        for j in range(n):
            for k in range(j + 1, n):
                c1 = Constraint(f"c1_{i}_{j}_{k}", [variables[i][j], variables[i][k]]) 
                c1.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(c1)
                c2 = Constraint(f"c2_{i}_{j}_{k}", [variables[j][i], variables[k][i]])   
                c2.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(c2)

    return csp, variables
    

def nary_ad_grid(fpuzz_grid):
    ##IMPLEMENT
    n = fpuzz_grid[0][0]
    variables = [[Variable(f"V_{i}_{j}", list(range(1, n + 1))) for j in range(n)] for i in range(n)]
    csp = CSP("N-ary Grid", [var for sublist in variables for var in sublist])
    
    varDoms = []
    for v in variables[0]:
        varDoms.append(v.domain())
        
    sat_tuples = []
    for t in itertools.product(*varDoms):
        #NOTICE use of * to convert the list v to a sequence of arguments to product
        if allDiff(t):
            sat_tuples.append(t)

    for i in range(n):
        c1 = Constraint(f"c1_{i}", variables[i]) 
        c1.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(c1)
        cols = []
        for j in range(n):
            cols.append(variables[j][i])
        c2 = Constraint(f"c2_{i}", cols)   
        c2.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(c2)

    return csp, variables

def cageConsistent(ls, result, operation):
    if (operation == 0):
        #add
        sum = 0
        for item in ls:
            sum = sum + item
        return sum == result
    elif (operation == 1):
        #sub
        for i in range(len(ls)):
            sum = result
            for j in range(len(ls)):
                if i != j:
                    sum = sum + ls[j]
            if sum == ls[i]:
                return True
        return False
    elif (operation == 2):
        #div
        for i in range(len(ls)):
            sum = result
            for j in range(len(ls)):
                if i != j:
                    sum = sum*ls[j]
            if sum == ls[i]:
                return True
        return False
    elif (operation == 3):
        #mul
        sum = 1
        for item in ls:
            sum = sum*item
        return sum == result
    else:
        print("Incorrect operation")
        return False

def caged_csp(fpuzz_grid):
    ##IMPLEMENT
    n = fpuzz_grid[0][0]
    csp, grid_vars = binary_ne_grid(fpuzz_grid)

    num_cages = len(fpuzz_grid)
    
    for i in range(1, num_cages):
        cage = fpuzz_grid[i]
        num_args = len(cage)
        num_vars = num_args - 2
        if (num_args == 2):
            num_vars = 1
        result = cage[num_vars]
        operation = cage[num_args - 1]
        var_inc = []
        for j in range(num_vars):
            var_key = cage[j]
            var_inc.append(grid_vars[int(var_key/10) - 1][int(var_key%10 - 1)])
        c3 = Constraint(f"c3_{i}", var_inc)
        varDoms = []
        for v in var_inc:
            varDoms.append(v.domain())
        sat_tuples = []
        if (num_vars > 1):
            for t in itertools.product(*varDoms):
                #NOTICE use of * to convert the list v to a sequence of arguments to product
                if cageConsistent(t, result, operation):
                    sat_tuples.append(t)
        else:
            for t in itertools.product(*varDoms):
                #NOTICE use of * to convert the list v to a sequence of arguments to product
                if t[0] == result:
                    sat_tuples.append(t)
        c3.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(c3)
    
    return csp, grid_vars