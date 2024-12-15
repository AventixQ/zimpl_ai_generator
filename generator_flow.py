import os
import openai
from dotenv import load_dotenv

def load_prompt(file_path):
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found")

    openai.api_key = openai_api_key
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    
def read_documentation(file):
    with open(file, "r",encoding="utf-8") as file:
        documentation_content = file.read()
    documentation_content = f"Here is a fragment of the documentation from ZIMPL: {documentation_content}"
    return documentation_content

def query_openai_model(prompt,task, model="gpt-4o-mini"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": task}],
        temperature=0.0,
        max_tokens=512
    )
    return response['choices'][0]['message']['content']

def collect_param(user_input):
    task = f'''
    Write decision variables in ZIMPL code for this task: {user_input}
    '''
    
    ###################################
    ########### PROMPT FLOW ###########
    ###################################

    ### CREATE SETS
    prompt_file_sets = "create_sets.txt"
    task_sets = task + "\nCreate sets for given promp. Write only sets as an answer. Do not add anything that is not starting with 'set'."
    prompt_sets = load_prompt(prompt_file_sets)#+read_documentation("ZIMPL_documentation\\set_documentation.md")
    
    try:
        response_sets = query_openai_model(prompt_sets, task_sets)
    except Exception as e:
        print(f"Error: {e}")

    ### CREATE PARAMETERS

    prompt_file_param = "add_parameters.txt"
    prompt_param = load_prompt(prompt_file_param)#+read_documentation("ZIMPL_documentation\\params_documentation.md")
    
    try:
        task_param = task + f"\nUse created sets: {response_sets}.\nWrite only parameters as an answer. Do not add anything that is not starting with 'param'."
        response_param = query_openai_model(prompt_param, task_param)
    except Exception as e:
        print(f"Error: {e}")

    ### DECISION VARIABLES
    prompt_file_variables = "decision_variables_param.txt"
    prompt_var = load_prompt(prompt_file_variables)#+read_documentation("ZIMPL_documentation\\variables_documentation.md")
    
    try:
        task_var = task + f"\nUse created sets: {response_sets} and given parameters {response_param}.\nWrite only decision variables as an answer."
        response_var = query_openai_model(prompt_var, task_var)
    except Exception as e:
        print(f"Error: {e}")
        
        
    ### DEFINE OBJECTIVE
    prompt_file_objective = "define_objective_param.txt"
    prompt_obj = load_prompt(prompt_file_objective)#+read_documentation("ZIMPL_documentation\\objective_documentation.md")
    
    try:
        task_obj = task + f"\nUse created sets: {response_sets} and given parameters {response_param}. Use created decision variables: {response_var}.\nWrite only objective as an answer."
        response_obj = query_openai_model(prompt_obj, task_obj)
    except Exception as e:
        print(f"Error: {e}")
        
    ### ADD CONSTRAINS
    prompt_file_constrains = "constraints_param.txt"
    prompt_con = load_prompt(prompt_file_constrains)#+read_documentation("ZIMPL_documentation\\constrains_documentation.md")
    
    try:
        task_con = task + f"\nUse created sets: {response_sets} and given parameters {response_param}. Use created decision variables: {response_var} and define objective {response_obj}.\nWrite only constrains as an answer."
        response_con = query_openai_model(prompt_con, task_con)
    except Exception as e:
        print(f"Error: {e}")
        
    total_response = f"{response_sets}\n\n{response_param}\n\n{response_var}\n\n{response_obj}\n\n{response_con}"
    
    return total_response

def no_collect_param(user_input):
    task = f'''
    Write decision variables in ZIMPL code for this task: {user_input}
    '''
    ###################################
    ########### PROMPT FLOW ###########
    ###################################

    ### DECISION VARIABLES
    prompt_file_variables = "decision_variables.txt"
    prompt_var = load_prompt(prompt_file_variables)#+read_documentation("ZIMPL_documentation\\variables_documentation.md")
    
    try:
        response_var = query_openai_model(prompt_var, task)
    except Exception as e:
        print(f"Error: {e}")
        
        
    ### DEFINE OBJECTIVE
    prompt_file_objective = "define_objective.txt"
    prompt_obj = load_prompt(prompt_file_objective)#+read_documentation("ZIMPL_documentation\\objective_documentation.md")
    
    try:
        task_obj = task + f"\nUse created decision variables: {response_var}.\nWrite only objective as an answer."
        response_obj = query_openai_model(prompt_obj, task_obj)
    except Exception as e:
        print(f"Error: {e}")
        
    ### ADD CONSTRAINS
    prompt_file_constrains = "constraints.txt"
    prompt_con = load_prompt(prompt_file_constrains)#+read_documentation("ZIMPL_documentation\\constrains_documentation.md")
    
    try:
        task_con = task + f"\nUse created decision variables: {response_var} and define objective {response_obj}.\nWrite only constrains as an answer."
        response_con = query_openai_model(prompt_con, task_con)
    except Exception as e:
        print(f"Error: {e}")
        
    total_response = f"{response_var}\n\n{response_obj}\n\n{response_con}"
    
    return total_response

def generator(user_input, option = 0):
    if option: result = collect_param(user_input)
    else: result = no_collect_param(user_input)
    return result

def normal_generator(user_input):
    task = f'''
    Write ZIMPL code for this task: {user_input}. Do not add anything excluding code. You must not start with \\'\\'\\'zimpl and end with \\'\\'\\'.
    '''
    try:
        response = query_openai_model(prompt="You are helpful assistant.",task=task)
    except Exception as e:
        print(f"Error: {e}")
        response = ""
    return response

def validate_generator(input_correct, input_to_evaluate):
    prompt_name = "validation_param.txt"
    prompt_val = load_prompt(prompt_name)
    task = f'''
    Provide evaluation for this code: {input_to_evaluate}. Do not add anything excluding code. To help you with evaluation, use correct code created for the same task: {input_correct}. Remember that even if they may be different, code, which you are evaluating still can be correct.
    '''
    try:
        response = query_openai_model(prompt=prompt_val,task=task)
    except Exception as e:
        print(f"Error: {e}")
        response = ""
    return response
    

if __name__ == "__main__":
    response = generator('''
A bakery produces two types of cookies: chocolate chip and caramel. The bakery anticipates daily demand for a minimum of 80 caramelized & 120 chocolate chip cookies. Due to a lack of raw materials and labor, the bakery can produce 120 caramel cookies and 140 chocolate chip cookies daily. For the bakery to be viable, it must sell a minimum of 240 cookies each day. Every chocolate chip cookie served generates $0.75 in profit, whereas each caramel biscuit generates $0.88. The solution to the number of chocolate chip and caramel cookies that the bakery must produce each day to maximize profit may be determined using linear programming.''',1)
    print(response)