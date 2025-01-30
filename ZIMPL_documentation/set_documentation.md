# Tuples and Sets in ZIMPL

## Tuples
A tuple is an ordered vector of fixed dimension where each component is either a number or a string.

## Sets
Sets consist of a finite number of tuples. Each tuple is unique within a set. In ZIMPL:
- All sets are internally ordered, but there is no particular order.
- Sets are delimited by braces `{` and `}`, respectively.
- All tuples of a specific set have the same number of components.
- The type of the n-th component for all tuples must be the same, i.e., they must be either all numbers or all strings.
- The definition of a tuple is enclosed in angle brackets `<` and `>`, e.g., `<1,2,"x">`. The components are separated by commas.

### One-Dimensional Tuples
If tuples are one-dimensional, it is possible to omit the tuple delimiters in a list of elements. However, in this case, they must be omitted from all tuples in the definition:
- Valid: `{1,2,3}`
- Invalid: `{1,2,<3>}`

## Set Definitions
Sets are defined with the `set` statement, which consists of the keyword `set`, the name of the set, an assignment operator `:=`, and a valid set expression.

### Example:
```zimpl
set A := { 1, 2, 3 };
set B := { "hi", "ha", "ho" };
set C := { <1,2,"x">, <6,5,"y">, <787,12.6,"oh"> };
```

## Referencing Sets
Sets are referenced using a template tuple, consisting of placeholders that are replaced by the values of the components of the respective tuple. For example, a set `S` consisting of two-dimensional tuples can be referenced by `<a,b>` in `S`.

### Example:
```zimpl
<1,b> in S
```
This will only return tuples where the first component is `1`.

## Set Functions and Operators
Table 4 lists the set functions and operators available in ZIMPL.

### Example Set Operations:
- **A * B** (Cross product): `{(x, y) | x ∈ A ∧ y ∈ B}`
- **A + B** (Union): `{x | x ∈ A ∨ x ∈ B}`
- **A \ B** (Difference): `{x | x ∈ A ∧ x ∉ B}`
- **A ∆ B** (Symmetric difference): `{x | (x ∈ A ∧ x ∉ B) ∨ (x ∈ B ∧ x ∉ A)}`
- **proj(A, t)** (Projection): Projects `A` onto the components specified by tuple `t`.

### Example Set Expressions:
```zimpl
set D := A cross B;
set E := { 6 to 9 } union A without { 2, 3 };
set F := { 1 to 9 } * { 10 to 19 } * { "A", "B" };
set G := proj(F, <3,1>);  // Results in: { <"A",1>, <"A",2">, ... <"B",9> }
```

## Conditional Sets
You can restrict a set to tuples that satisfy a Boolean expression using the `with` clause. The expression is evaluated for each tuple, and only tuples for which the expression evaluates to `true` are included in the new set.

### Example:
```zimpl
set F := { <i,j> in Q with i > j and i < 5 };
set A := { "a", "b", "c" };
set B := { 1, 2, 3 };
set V := { <a,2> in A*B with a == "a" or a == "b" };
```
This will result in:
```zimpl
{ <"a",2>, <"b",2> }
```

## Indexed Sets
Indexed sets allow you to index one set with another set, resulting in a set of sets. Indexed sets are accessed by adding the index in brackets `[]`.

### Example:
```zimpl
set I := { 1..3 };
set A[I] := <1> {"a","b"}, <2> {"c","e"}, <3> {"f"};
set B[<i> in I] := { 3 * i };
set P[] := powerset(I);
set S[] := subsets(I, 2);
```

### Functions for Indexed Sets:
- **powerset(A)** generates all subsets of `A`: `{X | X ⊆ A}`
- **subsets(A, n)** generates all subsets of `A` with `n` elements.
- **indexset(A)** returns the index set of `A`: `{1 ... |A|}`

### Example of Indexed Set Operations:
```zimpl
set U := union <i> in I : A[i];
set IN := inter <j> in J : P[j];  // empty!
```

## Summary of Set Functions:
- **A*B** (cross product)
- **A+B** (union)
- **A-B** (difference)
- **A ∆ B** (symmetric difference)
- **proj(A, t)** (projection)
- **argmin** (minimum argument)
- **argmax** (maximum argument)
- **if ... then ... else ... end** (conditional sets)
