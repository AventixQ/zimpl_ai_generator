# Parameters in Zimpl

Parameters are used to define constants in Zimpl. They can be declared with or without an index set. Without an index, a parameter is simply a single value, which can either be a number or a string. For indexed parameters, there is one value for each member of the set. A default value can also be specified.

## Parameter Declaration

Parameters are declared using the `param` keyword, followed by the name of the parameter and, optionally, the index set in square brackets. After the assignment operator (`:=`), there is a list of pairs where:
- The first element of each pair is a tuple from the index set.
- The second element is the value of the parameter for this index.

### Syntax:
```plaintext
param <name> [<index_set>] := <tuple_1> <value_1>, <tuple_2> <value_2>, ... ;
```

### Examples:
```plaintext
set A := { 12 .. 30 };
set C := { <1,2,"x">, <6,5,"y">, <3,7,"z"> };

param q := 5;
param u[A] := <13> 17, <17> 29, <23> 14 default 99;
param amin := min A; # = 12
param umin := min <a> in A : u[a]; # = 14
param mmax := max <i> in { 1 .. 10 } : i mod 5;
param w[C] := <1,2,"x"> 1/2, <6,5,"y"> 2/3;
param x[<i> in { 1 .. 8 } with i mod 2 == 0] := 3 * i;
```

- Assignments do not need to be complete. For example, no value is provided for index `<3,7,"z">` in parameter `w`, but this is fine as long as it is never referenced.

## Parameter Tables

It is possible to initialize multi-dimensional indexed parameters from tables. This is particularly useful for two-dimensional parameters. The data is structured in a table format with `|` signs on each margin. 

The table requires:
1. A headline with column indices.
2. A single index for each row of the table.
3. The column index is one-dimensional, while the row index can be multi-dimensional.

The complete index for an entry is built by appending the column index to the row index. Entries are separated by commas, and any valid expression can be used. Additional entries can be added after the table.

### Example of Initializing Parameters from Tables:
```plaintext
set I := { 1 .. 10 };
set J := { "a", "b", "c", "x", "y", "z" };

param h[I*J] := | "a", "c", "x", "z" |
                |1| 12, 17, 99, 23 |
                |3| 4, 3, -17, 66*5.5 |
                |5| 2/3, -.4, 3, abs(-4)|
                |9| 1, 2, 0, 3 | default -99;

param g[I*I*I] := | 1, 2, 3 |
                  |1,3| 0, 0, 1 |
                  |2,1| 1, 0, 1 |;

param k[I*I] := | 7, 8, 9 |
                |4| 89, 67, 55 |
                |5| 12, 13, 14 |, <1,2> 17, <3,4> 99;
```

The last example is equivalent to:
```plaintext
param k[I*I] := <4,7> 89, <4,8> 67, <4,9> 55, <5,7> 12,
                <5,8> 13, <5,9> 14, <1,2> 17, <3,4> 99;
```