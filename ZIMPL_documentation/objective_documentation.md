# Objective in Zimpl

In Zimpl, there can be **at most one objective** statement in a model. The objective can either be to **minimize** or **maximize** a function. 

The general structure of an objective statement is as follows:
```plaintext
<minimize/maximize> <name>: <objective_expression>;
```

Where:
- **minimize** or **maximize**: Specifies whether the objective is to minimize or maximize the expression.
- **name**: The name of the objective function.
- **objective_expression**: A linear expression that represents the objective function.

If there is a constant **offset** in the objective function (a constant value added or subtracted), Zimpl automatically generates an internal variable `@@ObjOffset` with a coefficient of 1. This variable is added to the objective function with the appropriate coefficient.

The reason for this is that neither the **lp** nor **mps** formats have a portable way to include a constant offset directly in the objective function.

## Objective Declaration Syntax

### Syntax:
```plaintext
<minimize/maximize> <objective_name>: <linear_expression>;
```

### Examples:

```plaintext
minimize cost: 12 * x1 - 4.4 * x2 + 5
              + sum <a> in A : u[a] * y[a]
              + sum <a,b,c> in C with a in E and b > 3 : -a/2 * z[a,b,c];
```
In this example:
- The objective is to **minimize** the cost.
- The cost is a linear combination of terms, including the variable `x1`, `x2`, and `y[a]`, along with an offset (constant 5) and additional terms involving the variable `z[a,b,c]`.

```plaintext
maximize profit: sum <i> in I : c[i] * x[i];
```
In this example:
- The objective is to **maximize** the profit.
- The profit is a sum of products of the coefficient `c[i]` and the variable `x[i]`.

### Important Notes:
- There can be only one **minimize** or **maximize** statement in the model.
- **Objective offsets** are handled automatically by Zimpl by adding an internal variable `@@ObjOffset` with a coefficient of 1 when needed.