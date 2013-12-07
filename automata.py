import png

######FOREGROUND COLORS#####
BLACK = 30
BLUE = 34
GREEN = 32
CYAN = 36
RED = 31
PURPLE = 35
YELLOW = 33
GRAY = 37
######NONCOLOR TRAITS######
DEFAULT = 0
BOLD = 1
DIM = 2
UNDERLINED = 4
BLINK = 5
INVERT = 7 #inverts foreground and background colors
HIDDEN = 8
NONCOLORS = BOLD, DIM, UNDERLINED, BLINK, INVERT, HIDDEN
##########RESET##########
RESET_ALL = 0
RESET = 20 #add this to a non color trait to make the reset value
#######BACKGROUND COLORS##### 
BACKGROUND = 10 #Add this to a foreground color to get the background code
BACKGROUND_LIGHT = 70 #same as above but lighter

def makerules():
	domain = list(reversed([tuple(int(char) for char in "{:0>3b}".format(i)) for i in range(8)]))
	rules = []
	for i in range(256):
		i_ = map(int, "{:0>8b}".format(i))
		cases = {domain[n]:i_[n] for n in range(8)}
		def rule(p, q, r, cases=cases):
			return cases[(p, q, r)]
		rules.append(rule)
		rules[i].__name__ = rules[i].__name__ + str(i)
	return rules

RULE = makerules()

def color(*colors, **kwargs):
	"""Color can be either an integer or a list of integers."""
	colors = list(colors)
	reset = kwargs.get("reset", 0)
	assert(isinstance(reset, int) or reset is None)
	if colors[0] not in NONCOLORS:
		colors.insert(0, 0)
	color = "\033[{}m".format(';'.join(map(str, colors)))
	reset = '' if reset is None else "\033[{}m".format(reset)
	return color + "{}" + reset

def automata(func, rows, colors=(GREEN + BACKGROUND, YELLOW + BACKGROUND), default_chr=' ', ic=None, verbose=True):
	if ic is None:
		last_row = [0]*(2*rows+1)
		last_row[(2*rows+1)/2] = 1
	else:
		side = [0]*(2*row + 1) / 2
		last_row = side + list(ic) + side
	current_row = last_row[:]
	d = len(current_row)-1
	if verbose:
		print "Generating {} rows of {}.".format(rows, func.__name__)
		print pretty(last_row, colors, default_chr)
	for _ in range(rows):
		for i, q in enumerate(last_row):
			p = last_row[i-1]
			r = last_row[(i+1)%d]
			current_row[i] = func(p,q,r)
		if verbose:
			print pretty(current_row, colors, default_chr)
		last_row = current_row[:]
	return current_row

def automata_(func, rows, ic=None):
	if ic is None:
		last_row = [0]*(2*rows+1)
		last_row[(2*rows+1)/2] = 1
	else:
		side = [0]*(2*row + 1) / 2
		last_row = side + list(ic) + side
	current_row = last_row[:]
	d = len(current_row)-1
	yield current_row
	for _ in range(rows):
		for i, q in enumerate(last_row):
			p = last_row[i-1]
			r = last_row[(i+1)%d]
			current_row[i] = func(p,q,r)
		yield current_row
		last_row = current_row[:]

def make_pngs(rows, cp=None):
	for rule in RULE:
		pic = open(rule.__name__+".png", 'wb')
		if cp is None:
			writer = png.Writer(width=2*rows+1, height=rows+1, greyscale=True, bitdepth=1)
			writer.write(pic, automata_(rule, rows))
		pic.close()

def pretty(list_, colormap, default=None):
	return ''.join(color(colormap[char]).format(char if default is None else default) for char in list_)
	
if __name__=="__main__":
	make_pngs(40)
