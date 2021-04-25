from sympy.solvers import solve
from sympy import Symbol

r = Symbol('r')
result = solve(61.98/(1+r) + 65.08/(1+r)**2 + 68.33/(1+r)**3 + \
               71.75/(1+r)**4 + 75.34/(1+r)**5 + \
               75.35*(1.0402)/((r-0.0402)*(1+r)**5)-1468.36, r)
print("all results:")
print(result)
print("final result")
for rs in result:
    try:
        if rs > 0:
            print(rs)
    except TypeError:
        # To capture non-real error
        pass