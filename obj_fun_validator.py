import re

def parse_solution(solution):
    """
    Parse a SCIP solution string into a dictionary with objective value and variable amounts.
    """
    solution_lines = solution.strip().split("\n")
    # Extract objective value
    obj_value = float(re.search(r"objective value:\s+([-\d.]+)", solution_lines[0]).group(1))
    
    # Extract variables and their values
    variables = {}
    for line in solution_lines[1:]:
        match = re.match(r"(x\$\S+)\s+([\d.]+)", line)
        if match:
            variable_name = match.group(1)
            variable_value = float(match.group(2))
            variables[variable_name] = variable_value
    
    return obj_value, variables

def compare_solutions(test_solution, correct_solution):
    """
    Compare two SCIP solutions to determine if they are semantically equivalent.
    """
    # Parse both solutions
    test_obj, test_vars = parse_solution(test_solution)
    correct_obj, correct_vars = parse_solution(correct_solution)
    
    # Check if objective values match
    if test_obj != correct_obj:
        return False, "Objective values do not match."
    
    # Check if variable amounts match (ignoring variable names)
    test_values = sorted(test_vars.values())
    correct_values = sorted(correct_vars.values())
    
    if test_values != correct_values:
        return False, "Variable values do not match."
    
    return True, "Solutions are semantically equivalent."

# Example usage
test_solution = """
objective value:                                   10
x$Lignite                                           1   (obj:4)
x$Anthracite                                        2   (obj:3)
"""

correct_solution = """
objective value:                                   10
x$Anthraciete                                        2   (obj:3)
x$Lignite                                           1   (obj:4)
"""

result, message = compare_solutions(test_solution, correct_solution)
print(message)