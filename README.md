# SLR-Parser-Graph-Generator

![lr_parser_graph](https://github.com/user-attachments/assets/ff041b3b-f3ff-460b-9f84-5bd87b5c371b)

Single python script for generating parsing graph for SLR parser.

**WARNING: This is a self made tool for convenience of learning purpose.
Correctness is not guaranteed!**

## Usage

Define the grammar in the scripts like this:

```python
rules.append(Rule(Sym("S'"), [Sym("S")]))
rules.append(Rule(Sym("S"), [Sym("a"), Sym("b")]))
```

This would define the grammar: `S'->S, S->ab`.

> No need to add symbol to `syms`, for
> they would be added once they're created.

Afterwards run the python scripts, extract the graphviz script starting with
`digraph G ...` and run it with a dot engine to produce the image.
