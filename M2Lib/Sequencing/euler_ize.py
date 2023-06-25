"""
	Differential Equations Initializer

		Turns a python function into a generator

		The function is meant to represent a Differential Equation

		Python will try to approximate this equation be using infinite generator.

		The accuracy of this approximation will most likely diverge from the real value as the generate keeps yielding!

"""

from functools import wraps
from typing import Callable
from ..formatting.table import show_rounded

## ------------------------------------ ##

	#### Initializing Differential Equation ####


def linear_interpolation(y0, slope, h):
	"""
		Basically connects two points be knowing:
			- The vertical component of the first one
			- The horizontal difference between the points
			- And the slop of the line formed by these two points

		Returns the vertical component of second point
	"""
	return y0 + h*slope


def diff_y(*Y, h):
	"""
		Input:      at the time t =  t0

			y is [y(t0), y''(t0), y''(t0), y'''(t0) ... y'_n_(t0)]

		Returns:      at the time t =  t0 + h

			[y(t0+h), y''(t0+h), y''(t0+h), y'''(t0+h) ... y'_n-1_(t0+h)]

	"""
#      Definition of the Derivative:      #slope
#         dy/dx = (y(x+h) - y(x))/((x + h) - (x))   where h -> 0

#      This can be rearranged into:  y(x+h) = y(x) + h*dy/dt

#      This definition of the derivative must apply for all y'
#         y'_n+1_(x) = (y'_n_(x+h) - y'_n_(x))/((x + h) - (x))

	def df(y):
		return linear_interpolation(y[0], y[1], h)  # in-place-fix for h

	return [*map(df, zip(Y, Y[1:]))]      # zip stops at the shorter list

# - - - - - - - -

def fetch_header(n:int, var:tuple = ('t', 'y'), gen_dy_dt: Callable = lambda y: (lambda n: y + (n+1)*"'")):
	t, y = var
	dy_dt = gen_dy_dt(y)
	return t, y, *map(dy_dt, range(n-2))

# - - - - - - - -


def euler_ize(
		*y, t0=.0, h=.1,
		verbose: bool = True, loop: int = 10, rounded2: int = 6
	):
	"""
		Transform a differential function written in the form:

			y'_n_ = f(t, y, y', y''..., y'_n-1_)

		Into an infinite sequence which approximates the value of y by applying the euler method

		This function can handle arbitrary number of initial conditions

		Parameters:

			- t0, *y
			- h must be specified as `h = ` otherwise inaccessible!

			Printing-Options:
				- verbose otherwise won't show!   set to true be default
				- loop how many steps
				- rounded2 rounded to n decimals points

		Returns function that returns a generator.
		The Generator isn't initialized in case 4 reset!
	"""
	def wrapper(f):
		@wraps(f)
		def yielder(t=t0, y=y):
			def dy(t, *y):
				"""
					Vectorized Differential Step Value:
						- Increments t
						- find all y'_n-1_(t+h) values based on the values of y'_n_(t)
						- inputs t+h, all-y'-up-2 y'_n-1_(t+h) into f to find y'_n_(t+h)

						Returns [t+h, *y'_n_(t+h)]
				"""
				return [*(Y := [t + h, *diff_y(*y, h=h)]), f(*Y)]

			yn = [t, *y, f(t, *y)]   # initiates values

			while True:               # infinite yielder!!!
				yield yn
				yn = dy(*yn)

		if verbose:
			show_rounded(yielder, fetch_header, loop+1, rounded2)

		return yielder
	return wrapper

## ------------------------------------ ##

################
##### Main #####
################


def main():
	print(__doc__)

if __name__ == '__main__':
	main()
