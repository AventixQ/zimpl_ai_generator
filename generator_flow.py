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

def generator(user_input):

    task = f'''
    Write decision variables in ZIMPL code for this task: {user_input}
    '''
    
    ###################################
    ########### PROMPT FLOW ###########
    ###################################

    ### CHECK IF GIVEN INPUT IS PROMPT #TODO



    ### COLLECTIONS AND PARAMETERS #TODO



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
        task = task + f"\nUse created decision variables: {response_var}.\nWrite only objective as an answer."
        response_obj = query_openai_model(prompt_obj, task)
    except Exception as e:
        print(f"Error: {e}")
        
    ### ADD CONSTRAINS
    prompt_file_constrains = "constrains.txt"
    prompt_con = load_prompt(prompt_file_constrains)
    
    try:
        task = task + f"\nUse created decision variables: {response_var} and define objective {response_obj}.\nWrite only constrains as an answer."
        response_con = query_openai_model(prompt_con, task)
    except Exception as e:
        print(f"Error: {e}")
        
    total_response = f"{response_var}\n\n{response_obj}\n\n{response_con}"
    
    return total_response

if __name__ == "__main__":
    response = generator("A factory manufactures two types of gadgets, regular and premium. Each gadget requires the use of two operations, assembly and finishing, and there are at most 12 hours available for each operation. A regular gadget requires 1 hour of assembly and 2 hours of finishing, while a premium gadget needs 2 hours of assembly and 1 hour of finishing. Due to other restrictions, the company can make at most 7 gadgets a day. If a profit of $20 is realized for each regular gadget and $30 for a premium gadget, how many of each should be manufactured to maximize profit?")
    print(response)