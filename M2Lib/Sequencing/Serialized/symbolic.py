from typing import Callable, Iterable, Any
from functools import singledispatchmethod
from types import FunctionType

from sympy import Expr, Symbol, oo

# - - - - - - - - -

class SymbolicSerializedSequence:
	@singledispatchmethod
	def __init__(self, arg: Any) -> None:
		raise NotImplementedError("A SymbolicSerializedSequence must be defided by an Expr `Seq` or a function `Sub`")

	@__init__.register
	def _ (self, var:Symbol, Seq:Expr, Sub: Callable[[int|Expr], Expr] | None = None):
		self.Seq = Seq
		self.k = var
		if Sub is None:
			def Sububsitude(x, Seq:Expr | None= self.Seq) -> Expr:
				return Seq.subs({self.k: x}) # type: ignore
			Sub = Sububsitude
		self.Sub = Sub

	@__init__.register		# vertauchbar
	def _ (self, Seq:Expr, var:Symbol, Sub: Callable[[int|Expr], Expr] | None = None):
		self.__init__(var, Seq, Sub)

	@__init__.register		# Subsitude only series
	def _ (self, Sub: FunctionType):
		self.Sub = Sub
		self.k = None
		self.Seq = None

	@staticmethod
	def numerical(index:slice) -> Iterable:
		start = 0 if index.start is None else index.start
		stop = index.stop     # must be there!
		step  = 1 if index.step is None else index.step
		return range(start, stop+1, step)   # Series start at 0 too

	@singledispatchmethod      # general dispatch definition DEFAULT
	def __getitem__(self, index:Any):
		raise NotImplementedError('Unsupported Access')

	@__getitem__.register(int)    # Normal Sequence Behaviour
	def _(self, index) -> Expr:
		return self.Sub(index)

	@__getitem__.register(slice)  # A Series
	def _(self, index):
		if index.stop is None:    # Series limit to inf #TODO
			# regardless what the other values are! start, stop, step
			raise NotImplementedError("Still don't know how to do it")
		if index.stop is oo:      # Sequence limit to inf
			if self.Seq is not None:
				return self.Seq.limit(self.k, oo)
			raise NotImplementedError('This Series is defined by a function')
		if index.start is None:
			return sum(self.Sub(i) for i in self.numerical(index)) # type: ignore
		return [self.Sub(i) for i in self.numerical(index)]