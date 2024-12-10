# Constraints in Zimpl

In Zimpl, constraints are defined using the `subto` keyword. The general structure for a **basic constraint** is:

```plaintext
subto name: term sense term;
```

Where:
- **name**: Any valid name starting with a letter.
- **term**: A linear expression similar to the objective term.
- **sense**: One of the following operators: `<=`, `>=`, or `==`.
  
Alternatively, a **ranged constraint** can be defined, which has the following form:

```plaintext
subto name: expr sense term sense expr;
```

Where:
- **expr**: A valid expression that evaluates to a number.
- **sense**: One of `<=`, `>=`, or `==`.
  
In ranged constraints, both senses must be equal and may not be `==`.

## Example Constraints

### Basic Constraints:
```plaintext
subto time: 3 * x1 + 4 * x2 <= 7;
subto space: 50 >= sum <a> in A : 2 * u[a] * y[a] >= 5;
subto weird: forall <a> in A : sum <a,b,c> in C : z[a,b,c] == 55;
subto c21: 6 * (sum <i> in A : x[i] + sum <j> in B : y[j])) >= 2;
subto c40: x[1] == a[1] + 2 * sum <i> in A do 2 * a[i] * x[i] * 3 + 4;
```

### Constraints with `if` statements:
Constraints can include **conditional statements** (if-then-else) where part of the constraint is conditional based on some criteria.

```plaintext
subto c2: sum <i> in I :
if (i mod 2 == 0) then 3 * x[i] else -2 * y[i] end <= 3;
```

### Constraints with `if` and `forall`:
You can also combine `if` conditions inside a `forall` statement.

```plaintext
subto c1: forall <i> in I do
if (i mod 2 == 0) then 3 * x[i] >= 4
else -2 * y[i] <= 3 end;
```

### Combining Constraints:
Multiple constraints can be grouped together using the `and` operator.

```plaintext
subto c1: forall <i> in I:
if (i > 3)
then if (i == 4)
then z[1] + z[2] == i
else z[2] + z[3] == i
end and
z[3] + z[4] == i and
z[4] + z[5] == i
else
if (i == 2)
then z[1] + z[2] == i + 10
else z[2] + z[3] == i + 10
end and
z[3] + z[4] == i + 10 and
z[4] + z[5] == i + 10
end;
```

## Constraint Attributes

Zimpl allows you to specify special attributes for constraints:

- **scale**: Scales the constraint before writing it to a file by dividing by the maximum absolute coefficient in the constraint.
- **separate**: Excludes the constraint from the initial LP but includes it later. It is written into the `USER CUTS` section of the LP file.
- **checkonly**: Similar to `separate`, but only checks feasibility, written into the `LAZY CUTS` section.
- **indicator**: Used for constraints involving indicator variables, which are treated as indicator constraints instead of using a big-M formulation.

### Examples:
```plaintext
subto c1: 1000 * x + 0.3 * y <= 5, scale, checkonly;
subto c2: x + y + z == 7, separate;
subto c3: vif x == 1 then y == 7 end, indicator;
```

## Special Ordered Sets (SOS)

Special ordered sets (SOS) are used in integer programming models to define sets of variables that are ordered in a specific way. Zimpl supports two types of SOS: type-1 and type-2.

### SOS Syntax:
```plaintext
sos name: [type1|type2] priority expr : term;
```

Where:
- **type1/type2**: The type of the special ordered set.
- **priority**: Optional, the priority of the SOS.
- **term**: Defined like terms in the objective.
  
### Examples:
```plaintext
sos s1: type1: 100 * x[1] + 200 * x[2] + 400 * x[3];
sos s2: type2 priority 100 : sum <i> in I: a[i] * x[i];
sos s3: forall <i> in I with i > 2: type1: (100 + i) * x[i] + i * x[i-1];
```

## Extended Constraints

Zimpl also supports **conditional constraints** using the `vif` keyword. The general form is:

```plaintext
vif boolean-constraint then constraint [else constraint] end
```

Where:
- **boolean-constraint**: A linear expression involving bounded integer or binary variables.
- **constraint**: The constraint to apply depending on the condition.

### Examples:
```plaintext
var x[I] integer >= 0 <= 20;
subto c1: vif 3 * x[1] + x[2] != 7
then sum <i> in I : y[i] <= 17
else sum <k> in K : z[k] >= 5 end;
subto c2: vif x[1] == 1 and x[2] > 5 then x[3] == 7 end;
subto c3: forall <i> in I with i < max(I) :
vif x[i] >= 2 then x[i + 1] <= 4 end;
```

## Extended Functions

Special functions can be used in Zimpl for terms involving variables. For example, the `vabs(t)` function computes the absolute value of the term `t`.

### Example:
```plaintext
var x[I] integer >= -5 <= 5;
subto c1: vabs(sum <i> in I : x[i]) <= 15;
subto c2: vif vabs(x[1] + x[2]) > 2 then x[3] == 2 end;
```