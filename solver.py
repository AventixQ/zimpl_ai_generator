import os
import subprocess

def run_scip_and_extract_solution(zpl_content, scip_path):
    if SCIP_PATH not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + SCIP_PATH

    
    try:
        # Write ZPL content to a temporary file
        with open("temp.zpl", "w") as temp_file:
            temp_file.write(zpl_content)
        
        # Run SCIP
        process = subprocess.Popen(
            ["scip"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        commands = """
        read temp.zpl
        opt
        display solution
        quit
        """
        stdout, _ = process.communicate(input=commands)
        
        # Extract solution from SCIP output
        if "objective value:" in stdout:
            solution_start = stdout.index("objective value:")
            solution = stdout[solution_start:].strip()
            
            # Remove the trailing "SCIP>"
            solution = solution.split("SCIP>")[0].strip()
            return True, solution
        else:
            return False, "No solution found"
    finally:
        # Remove the temporary file
        path_files = ["temp.zpl", "temp.lp", "temp.tbl"]
        for file in path_files:
            if os.path.exists(file):
                os.remove(file)


# How to use
zpl_content = '''
# Sets
set CoalTypes := {"Lignite", "Anthracite"};
set Activities := {"Cutting", "Washing"};

# Decision Variables
var LigniteProd >= 0;  # tons of Lignite produced
var AnthraciteProd >= 0;  # tons of Anthracite produced
var TotalProd >= 0;  # total tons of coal produced

# Parameters for profit per ton
param profit[CoalTypes] := 
    <"Lignite"> 4, 
    <"Anthracite"> 3;

# Parameters for time requirements per ton (matrix representation)
param time[CoalTypes * Activities] :=
            | "Cutting", "Washing" |
|"Lignite"   |      3,        4 |
|"Anthracite"|      4,        2 |;

# Parameters for available time per activity
param available_time[Activities] := 
    <"Cutting"> 12, 
    <"Washing"> 8;

# Parameters for desired total production
param desired_total_prod := 3;

# Decision Variables
var LigniteProd integer >= 0;  # tons of Lignite produced
var AnthraciteProd integer >= 0;  # tons of Anthracite produced
var TotalProd integer >= 0;  # total tons of coal produced

# Objective function
maximize total_profit: profit["Lignite"] * LigniteProd + profit["Anthracite"] * AnthraciteProd;

# Constraints
subto time_constraints: 
    forall <a> in Activities do
        sum <c> in CoalTypes: time[c,a] * x[c] <= available_time[a];

subto production_constraint: 
    LigniteProd + AnthraciteProd = desired_total_prod;
'''
SCIP_PATH = r"C:\Program Files\SCIPOptSuite 9.1.0\bin"
is_valid, solution = run_scip_and_extract_solution(zpl_content, SCIP_PATH)

print(f"Is Valid: {is_valid}\n\nSolution:\n{solution}")
