from collections import defaultdict
from typing import Iterable, Iterator, Callable, Generator
from functools import wraps

#############################################
################ FORMATTING #################
#############################################

def line_separator(
		repeat_line_pattern:int    = 12,
		line_pattern:str           = '-',
		line_patter_sep: str       = ' ',
		padding_top:str            = '\n',
		padding_bottom:str         = 2*'\n'
	):
	"""
		Just for printing a horizontal line

		- - - - - - - - - - - - - - - - -
	"""
	print(padding_top, end='')
	print(*(repeat_line_pattern*line_pattern),sep=line_patter_sep, end=padding_bottom)

# --------------

##########################
#### Table Formatting ####
##########################

def solidify(f: Callable):
	@wraps(f)
	def wrapper(S, *args, **kwargs):
		return f(tuple(S), *args, **kwargs)
	return wrapper

@solidify
def table(A:Iterable, cell_formatting:str = '{}') -> tuple:
	"""
		Formatted Table

		A must be a "Matrix" of str!
	"""

	def fetch_max_colum_width(Matrix:Iterable) -> dict:
		column_width = defaultdict(lambda: 0)   # in case incomplete rows

		def compare(x:int, at:int) -> None:
			# change the value if a max is found otherwise keep len_max[at] as is
			column_width[at] = x if x > column_width[at] else column_width[at]

		for row in Matrix:
			for i, x in enumerate(row):
				compare(len(x), i)

		return column_width

	def generate_cell_format(padding:int, alignment:str = '^') -> str:
		return cell_formatting.format("{" + f":{alignment}{padding}" + "}")

	cell_format = tuple(map(generate_cell_format, fetch_max_colum_width(A).values()))

	def format_cell(i:int, word:str, cell_format=cell_format):
		return cell_format[i].format(word)

	def format_line(line:Iterable, padding:str = ''):
		fIW = lambda IW: format_cell(IW[0], IW[1])      # just index, word
		return *map(fIW, enumerate(line)),

	S = tuple(map(format_line, A))

	return S

def find_max_column_num(A:Iterable):
	return max(map(len, A))      # map the len function on each row of A

def join(A:Iterable, cell_format:str, line_format:str = "{}", cell_binding:str = '', line_binding:str = '\n') -> str:
	join_cells = lambda W: cell_binding.join(cell_format.format(w) for w in W)

	join_lines = lambda L: line_binding.join(line_format.format(l) for l in L)

	return join_lines(map(join_cells, A))

@solidify
def table_view(A:Iterable, header_formatter:Callable, cell:str = "   {}   ", verbose:bool = True) -> str:

	S = [header_formatter(find_max_column_num(A)), tuple(), *A]

	S = join(table(S), cell)

	if verbose:
		print(S)

	return S

# -----------------

## Markdown Format

def markdown_padding_line(widths:tuple) -> tuple:
	"""
		Only supports :-:
	"""
	def fetch_padding(width:int):
		return ((width-2)*'-').join(2*':') if width > 2 else ":-:"

	return *map(fetch_padding, widths),

@solidify
def markdown_table(A:Iterable, header_formatter:Callable, verbose:bool = True) -> str:

	columns_num = find_max_column_num(A)

	S = [header_formatter(columns_num), *A]

	S = table(S, cell_formatting = " {} ")

	widths = *map(len, S[0]),

	S = [S[0], markdown_padding_line(widths), *S[1:]]

	S = join(S, cell_format="{}", line_format = "|{}|", cell_binding = '|')

	if verbose:
		print(S)

	return S


# ------------------

## Show

def loop(A:Iterator, n: int = 10) -> Generator:
	"""
		loops over an infinite sequence n times
	"""
	while (n := n - 1) > 0:      # countdown
		yield next(A)

def show(A:Callable, header_formatter:Callable, n: int = 10, pre_process:Callable = lambda x: x ) -> None:

	pre_processed = lambda Row: tuple(map(lambda x: f"{pre_process(x)}", Row))   # row-wise

	S = map(pre_processed, loop(A(), n))

	markdown_table(S, header_formatter, verbose=True)

def show_rounded(A:Callable, header_formatter:Callable, n: int = 10, rounded2:int = 6) -> None:

	show(A, header_formatter, n, pre_process=lambda x: round(x, rounded2))
