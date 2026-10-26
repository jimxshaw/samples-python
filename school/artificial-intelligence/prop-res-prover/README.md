# CS 4365 Assignment 3, Part II: Resolution Theorem Prover

Propositional resolution prover written in Python 3 (standard library only).

## How to run

```
python3 main.py <input_file>
```

Example:

```
python3 main.py example_in.txt
```

Output goes to standard output. To save it:

```
python3 main.py example_in.txt > out.txt
```

## Input format

- One clause per line; literals are separated by a single space.
- A negated literal is prefixed with `~` (for example `~p q`).
- The first n-1 lines are the knowledge base (CNF). The last line is the clause to test.
- Blank lines are ignored.

## Output format

One line per clause in the final KB, in the order added:

```
<number>. <literals> {<parent_i>,<parent_j>}
```

- Input clauses and the negated goal have empty parents: `{}`.
- The empty clause is printed as `Contradiction`.
- The last line is `Valid` (a contradiction was found) or `Fail` (no new clauses can be produced).

## Algorithm summary

1. Read the KB and the goal clause. Duplicate literals within a clause are removed.
2. Negate the goal (De Morgan) and add each resulting unit clause to the KB, left to right.
3. For each clause i, in order, try to resolve it with every earlier clause j (in order).
   New clauses are appended to the end of the KB, so the KB grows while it is processed.
4. A resolvent is **not** added if it is a tautology or if the KB already has a clause with the same set of literals.
5. Stop as soon as the empty clause is produced (`Valid`), or when every clause has been processed (`Fail`).

## Files

- `main.py`: the entire program (entry point).

## Notes

- Clauses are compared as sets of literals, so `q ~p` and `~p q` are the same clause.
- Literal order in a printed clause follows the order it was generated (clause i's remaining literals, then clause j's).
- No external libraries are used. Tested with Python 3 on Linux.