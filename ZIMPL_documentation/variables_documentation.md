# Variables in Zimpl

Variables in Zimpl, like parameters, can be indexed. A variable must be one of three possible types:
1. **Continuous (Real)** – The default type.
2. **Binary** – Values are always between 0 and 1.
3. **Integer** – Whole number values.

Variables may have lower and upper bounds. The default bounds are:
- Lower bound: **0**
- Upper bound: **infinity**

However, it is possible to set bounds to specific values, including **-infinity** for lower bounds. For binary variables, the values are always constrained between 0 and 1.

Additionally, variables can be declared as **implicit**, meaning they are assumed to have an integral value in any optimal solution to the integer program, even if they are declared as continuous. The **implicit** declaration is only useful with solvers that support this feature, such as SCIP (http://scip.zib.de) when linked with Zimpl. In all other cases, the variable is treated as continuous.

You can also specify **initial values** for integer variables using the `startval` keyword, and you can set a **branching priority** using the `priority` keyword. These values are used by solvers like CPLEX if the `-r` command line switch is provided.

## Variable Declaration Syntax

### Syntax:
```plaintext
var <name> [<index_set>] <type> >= <lower_bound> <= <upper_bound> <optional_keywords>;
```

### Examples:

```plaintext
var x1;                       # Continuous variable with default bounds (0, infinity)
var x2 binary;                 # Binary variable (0 or 1)
var x3 integer >= -infinity;   # Integer variable with no upper bound
var y[A] real >= 2 <= 18;      # Continuous variable indexed by A with bounds [2, 18]
var z[<a,b> in C] integer >= a * 10 <= if b <= 3 then p[b] else infinity end; 
                              # Integer variable indexed by <a, b> in set C, with dynamic bounds
var w implicit binary;         # Implicit binary variable, treated as integer by solvers supporting implicit declaration
var t[k in K] integer >= 1 <= 3 * k startval 2 * k priority 50; 
                              # Integer variable indexed by k in set K, with startval and priority
```

### Explanation of Keywords:
- `binary`: Specifies the variable as binary (values between 0 and 1).
- `integer`: Specifies the variable as integer (whole numbers).
- `real`: Specifies the variable as continuous (default type).
- `>= <lower_bound>`: Defines the lower bound of the variable.
- `<= <upper_bound>`: Defines the upper bound of the variable.
- `startval <value>`: Specifies an initial value for the integer variable.
- `priority <value>`: Sets the branching priority for the variable (used in solvers like CPLEX).
- `implicit`: Declares the variable as implicit, useful with solvers that can treat it as integral even if continuous.