import os
import openai

openai_api_key = ""

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY nie został znaleziony w pliku .env")

openai.api_key = openai_api_key

def load_prompt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Plik {file_path} nie został znaleziony.")

def query_openai_model(prompt,task, model="gpt-4o-mini"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": task}],
        temperature=0.0,
        max_tokens=512
    )
    return response['choices'][0]['message']['content']

def main():
    
    task = '''
    Write decision variables in ZIMPL code for this task: A factory manufactures two types of gadgets, regular and premium. Each gadget requires the use of two operations, assembly and finishing, and there are at most 12 hours available for each operation. A regular gadget requires 1 hour of assembly and 2 hours of finishing, while a premium gadget needs 2 hours of assembly and 1 hour of finishing. Due to other restrictions, the company can make at most 7 gadgets a day. If a profit of $20 is realized for each regular gadget and $30 for a premium gadget, how many of each should be manufactured to maximize profit?
    '''
    
    ### ZBIORY I PRARAMETRY
    
    
    
    ### DECISION VARIABLES
    prompt_file_variables = "prompt1.txt"
    prompt_var = load_prompt(prompt_file_variables)
    
    try:
        response_var = query_openai_model(prompt_var, task)
        #print(f"Decision variables:\n{response_var}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        
        
    ### DEFINE OBJECTIVE
    prompt_file_objective = "prompt2.txt"
    prompt_obj = load_prompt(prompt_file_objective)
    
    try:
        task = task + f"\nUse created decision variables: {response_var}.\nWrite only objective as an answer."
        response_obj = query_openai_model(prompt_obj, task)
        #print(f"Define objective:\n{response_obj}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        
    ### ADD CONSTRAINS
    prompt_file_constrains = "prompt3.txt"
    prompt_con = load_prompt(prompt_file_constrains)
    
    try:
        task = task + f"\nUse created decision variables: {response_var} and define objective {response_obj}.\nWrite only constrains as an answer."
        response_con = query_openai_model(prompt_con, task)
        #print(f"Constrains:\n{response_con}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        
    total_response = f"{response_var}\n{response_obj}\n{response_con}"
    
    print(total_response)

if __name__ == "__main__":
    main()
