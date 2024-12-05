import os
import subprocess

def run_scip_and_extract_solution(zpl_content, scip_path):
    os.environ["PATH"] += os.pathsep + scip_path
    
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
zpl_content = """
var x integer;    # number of adult members
var y integer;    # number of junior members

# function
maximize income: 20*x + 8*y;

# constrains
subto c1: 20*x + 8*y >= 800; # Minimum Income Requirement
subto c2: x + y <= 50; # Total Membership Restriction
subto c3: x/4 <= y; # Junior Membership Ratio
subto c4: x/3 >= y; # Junior Membership Ratio
"""
SCIP_PATH = r"C:\Program Files\SCIPOptSuite 9.1.0\bin"
is_valid, solution = run_scip_and_extract_solution(zpl_content, SCIP_PATH)

print(f"Is Valid: {is_valid}\n\nSolution:\n{solution}")
