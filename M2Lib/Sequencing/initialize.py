"""
	initializer

		Turns a python function into a generator

		The function is meant to represent a mathematical sequence

		Which will be turned into an infinite sequence!

"""


from typing import Callable, Iterable
from functools import wraps, singledispatch

from types import FunctionType

from ..formatting.table import show

## ------------------------------------ ##

		#### Sequencing Algorithm ####

def independent_yielder(f:Callable, n0, h) -> Iterable:
	@wraps(f)
	def yielder(n = n0, h = h):
		while True:		# infinite yielder!!!
			yield n, f(n)
			n += h
	return yielder()

def depended_yielder(f:Callable, n0, *a_, h) -> Iterable:
	@wraps(f)
	def yielder(n = n0, a_ = a_, h = h):
		while True:		# infinite yielder!!!
			a = f(n, *a_)
			yield n, a
			a_ = [*a_[1:], a]		# update dependencies
			n += h
	return yielder()


## ------------------------------------ ##

###############################################
################ Initializing #################
###############################################

def post_process(processor:Callable):
	def decorator(f:Callable):
		@wraps(f)
		def wrapper(*args, **kwargs):
			r = f(*args, **kwargs)
			return processor(r)
		return wrapper
	return decorator

def fetch_header(n:int, var:tuple = ('n', 'a'), gen_dy_dt: Callable = lambda y: (lambda n:f"{y}({'n' if not n else '+'+str(n)})")):
	t, y = var
	dy_dt = gen_dy_dt(y)
	return t, y, *map(dy_dt, range(n-2))

def show_sequence(verbose:bool, *args, **kwargs) -> Callable:
	if not verbose:
		return post_process(lambda x: x)
	def print_first(X):
		show(X, fetch_header,  *args, **kwargs)
		return X
	return post_process(print_first)

@singledispatch
def initialize(
		n0 = 0, *a_, h = 1,
		verbose: bool = True, loop: int = 10
	) -> Callable:
	"""
		Initialize a mathematical sequence with starting values and turns it into a infinite sequence!

			- The sequence must return a single value #the-value-of-the-sequence-at-that-index

			- The sequence must accept at least one parameter n #an-index

			- The sequence can have as many "RELATIVE" recursive dependencies as needed or none at all

		Returns an wrapper, which turns a sequence into an infinite yielder!

		The generator returns a tuple of the sequence value with the corresponding index

			(n, a_n)	#index-value-pair

		parameter:
			- n0   stating index                                  Default 0
			- a_   starting value of the relative dependencies
			- h    each time n will be shifted be step.           Default 1

		The generator has internal state, which will be changed
		Each time #next is called upon the generator:

			n += h
			a = f(n, *a_)	# where *a_ previous terms

		The sequence can be written as a function of (n, *a_) #a_ are previous-terms
		The previous terms can also be written as a parameter

			For k previous dependency:
				f(n, a_{n-k}, a_{n-k-1}, a_{n-k-2}.... , a_{n-1})

			f(n, a0, a1, a2)

		The order is important!

		Unfortunately f must be depended on n!

	"""
	def generator_factory(n0, *a_, h) -> Callable:
		@show_sequence(verbose, loop)
		def wrapper(f:Callable):
			@wraps(f)
			def yielder():
				if len(a_):
					return depended_yielder(f, n0, *a_, h = h)
				return independent_yielder(f, n0, h)
			return yielder
		return wrapper
	return generator_factory(n0, *a_, h=h)

@initialize.register    # allow for zeor args decorators
def _(f:FunctionType):
	return initialize(0)(f)   # needs at least on arg to properly sort the dispatch

#############################################
################# Main ######################
#############################################

def main():
	print(__doc__)

if __name__ == '__main__':
	main()
