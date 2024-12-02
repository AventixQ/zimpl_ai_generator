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
    prompt_sets = load_prompt(prompt_file_sets)
    
    try:
        response_sets = query_openai_model(prompt_sets, task)
    except Exception as e:
        print(f"Error: {e}")

    ### CREATE PARAMETERS

    prompt_file_param = "add_parameters.txt"
    prompt_param = load_prompt(prompt_file_param)
    
    try:
        task_param = task + f"\nUse created sets: {response_sets}.\nWrite only parameters as an answer."
        response_param = query_openai_model(prompt_param, task_param)
    except Exception as e:
        print(f"Error: {e}")

    ### DECISION VARIABLES
    prompt_file_variables = "decision_variables_param.txt"
    prompt_var = load_prompt(prompt_file_variables)
    
    try:
        task_var = task + f"\nUse created sets: {response_sets} and given parameters {response_param}.\nWrite only decision variables as an answer."
        response_var = query_openai_model(prompt_var, task_var)
    except Exception as e:
        print(f"Error: {e}")
        
        
    ### DEFINE OBJECTIVE
    prompt_file_objective = "define_objective_param.txt"
    prompt_obj = load_prompt(prompt_file_objective)
    
    try:
        task_obj = task + f"\nUse created sets: {response_sets} and given parameters {response_param}. Use created decision variables: {response_var}.\nWrite only objective as an answer."
        response_obj = query_openai_model(prompt_obj, task_obj)
    except Exception as e:
        print(f"Error: {e}")
        
    ### ADD CONSTRAINS
    prompt_file_constrains = "constraints_param.txt"
    prompt_con = load_prompt(prompt_file_constrains)
    
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
    prompt_var = load_prompt(prompt_file_variables)
    
    try:
        response_var = query_openai_model(prompt_var, task)
    except Exception as e:
        print(f"Error: {e}")
        
        
    ### DEFINE OBJECTIVE
    prompt_file_objective = "define_objective.txt"
    prompt_obj = load_prompt(prompt_file_objective)
    
    try:
        task_obj = task + f"\nUse created decision variables: {response_var}.\nWrite only objective as an answer."
        response_obj = query_openai_model(prompt_obj, task_obj)
    except Exception as e:
        print(f"Error: {e}")
        
    ### ADD CONSTRAINS
    prompt_file_constrains = "constraints.txt"
    prompt_con = load_prompt(prompt_file_constrains)
    
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
    

if __name__ == "__main__":
    response = generator('''
A nutritionist wants to create a diet plan for a patient. The diet must satisfy daily nutritional requirements at the lowest possible cost. The patient needs at least 50 grams of protein, 30 grams of fat, and 80 grams of carbohydrates per day. The nutritionist has identified three foods with the following nutritional content per unit and costs:
Food 1: 10g protein, 5g fat, 15g carbs, cost $2
Food 2: 4g protein, 10g fat, 20g carbs, cost $3
Food 3: 5g protein, 2g fat, 8g carbs, cost $1''',1)
    print(response)