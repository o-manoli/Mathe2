"""
	Template Differenzengleichung mit Polynomial Störfunktion
"""

from sympy import (
	symbols, Eq, Function, Equality, Symbol,
	rsolve, solve, rsolve_poly,
	Lambda, Poly
)

import sympy as sp

from IPython.display import display
from IPython.core.display import Markdown

PM = lambda S: display(Markdown(S))	 # print Markdown

k = symbols('k')
y = Function('y')
l = symbols('lambda')

def Solve(eq:Equality, *Y0s, y:Function = y, k:Symbol = k):

	PM(f"# Lösung")

	display(eq)

	C_Poly = eq.lhs.subs(k, 0)

	C_Poly = C_Poly.replace(y, Lambda((k), l**k))

	PM(f"## Charakteristisches Polynom")

	display(sp.factor(C_Poly))

	C_Poly = Poly(C_Poly)

	for i, root in enumerate(C_Poly.all_roots(), 1):
		display(Eq(symbols(f"\\lambda_{{{i}}}"), root))

	PM(f"## Homogene Lösung")

	# h. Lösung
	h_sol = rsolve(eq.lhs, y(k))

	display(Eq(Function("y_h")(k), h_sol))

	# resolv_poly takes coefficients starting with a0 y^0, a1 y^1, a2 y^2 ...
	Coeffs = C_Poly.all_coeffs()[::-1]

	# p. Lösung
	# coeff [a0 y^0, a1 y^1, a2 y^2 ...]
	p_sol = rsolve_poly(Coeffs, eq.rhs, k)

	PM(f"## Inhomogene Lösung")

	display(Eq(Function("y_p")(k), p_sol))

	sol = h_sol + p_sol

	PM(f"## Allgemeine Lösung")

	display(Eq(y(k), sol))

	def gen_eqs(*XY, x = k, y = sol):
		"""
			Generates Equation System from Starting Values
		"""
		def gen_eq(x0, y0, x=x, y=y):
			return Eq(y.subs(x, x0), y0)
		return [gen_eq(x0, y0) for x0, y0 in XY]

	init_eqs = gen_eqs(*Y0s)

	PM(f"## Lösung des Anfangswertproblem")

	for r in init_eqs:
		display(r)

	C = solve(init_eqs)

	for key, value in C.items():
		display(Eq(key, value))

	ans = sol.subs(C)

	PM(f"### Einsetzen")

	display(Eq(y(k), ans))

	return ans

