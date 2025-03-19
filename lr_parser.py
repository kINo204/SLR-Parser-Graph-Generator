# 1. Define the grammar.
class Sym:
	def __init__(self, name):
		self.name = name
		global syms
		syms.add(self)
	def __eq__(self, o): return self.name == o.name
	def __hash__(self): return hash(self.name)
	def __str__(self): return self.name

class Rule:
	def __init__(self, left, rights):
		self.left = left
		self.rights = rights
	def __str__(self):
		l = self.left
		rs = ""
		for r in self.rights:
			rs += str(r)
		return f"{l}::={rs}"

rules = []
syms = set()

# Put the grammar here.

rules.append(Rule(Sym("S'"), [Sym("S")]))

rules.append(Rule(Sym("S"), [Sym("C"),Sym("D")]))
rules.append(Rule(Sym("S"), [Sym("D"),Sym("C")]))

rules.append(Rule(Sym("C"), [Sym("a"),Sym("C"),Sym("b")]))
rules.append(Rule(Sym("C"), [Sym("a"),Sym("b")]))

rules.append(Rule(Sym("D"), [Sym("D"),Sym("b")]))
rules.append(Rule(Sym("D"), [Sym("b")]))

print("Rules given:")
for r in rules:
	print(r)

# 2. Generate the canonical collection.
class Item:
	def __init__(self, pos, rule):
		self.pos = pos
		self.rule = rule
	def __hash__(self):
		global rules
		return hash(self.pos) * len(rules) + hash(self.rule)
	def __eq__(self, o):
		global rules
		return self.pos == o.pos and rules.index(self.rule) == rules.index(o.rule)
	def __lt__(self, o):
		return hash(self) < hash(o)
	def __str__(self):
		l = self.rule.left
		rl = [r for r in self.rule.rights]
		rl.insert(self.pos, ".")
		rs = ""
		for r in rl:
			rs += str(r)
		return f"{l}::={rs}"

def closure(items):
	R = [i for i in items]
	T = [i for i in R]
	while True:
		for item in R:
			if item.pos >= len(item.rule.rights): continue
			B = item.rule.rights[item.pos]
			for rule in rules:
				if B == rule.left:
					to_add = Item(0, rule)
					replicated = False
					for to_cmp in T:
						if to_cmp == to_add:
							replicated = True
							break
					if not replicated:
						T.append(Item(0, rule))
		if len(T) == len(R): break
		R = [i for i in T]
	return T

def goto(items, sym):
	res = []
	for item in items:
		if item.pos >= len(item.rule.rights): continue
		if item.rule.rights[item.pos] != sym: continue
		new_items = closure([Item(item.pos+1, item.rule)])
		for new_item in new_items:
			replicated = False
			for to_cmp in res:
				if new_item == to_cmp:
					replicated = True
					break
			if not replicated:
				res.append(new_item)
	return res

collection = [closure([Item(0,rules[0])])]
edges = []

while True:
	T = [i for i in collection]
	for item_set in collection:
		for sym in syms:
			tar = goto(item_set, sym)
			replicated = False
			for to_cmp in T:
				if sorted(tar) == sorted(to_cmp):
					replicated = True
					break
			if (len(tar) > 0):
				e = [item_set,sym,tar]
				replicated_edge = False
				for e_to_cmp in edges:
					if e == e_to_cmp:
						replicated_edge = True
						break;
				if not replicated_edge:
					edges.append(e)
				if not replicated:
					T.append(tar)
	if len(T) == len(collection): break
	collection = [i for i in T]
collection = [i for i in T]

print("Canonical collections:")
for item_set in collection:
	print(f"#{collection.index(item_set)}")
	for item in item_set:
		print(item)

def to_graphviz():
	s = 'digraph G {\n'
	# Nodes.
	for item_set in collection:
		ind = collection.index(item_set)
		s_items = ""
		for item in item_set:
			s_items += str(item)+"\\l"
		s += f'\tI{ind} [shape=box,xlabel="I{ind}",label="{s_items}"]\n'
	# Edges.
	for e in edges:
		s += f'\tI{collection.index(e[0])} -> I{collection.index(e[2])} [label="{e[1]}"]\n'
	s += '}'
	return s

print(to_graphviz())
