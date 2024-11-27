# ZIMPL AI Generator

The ZIMPL AI Generator allows users to generate ZIMPL code for optimization problems. It provides an intuitive interface for defining optimization scenarios and automatically generates decision variables, an objective function, and constraints.

## How to use

**1. Prepare your environment:**

- install python >=3.8
- create virtual environment:
`python -m venv myenv`
- install all requirement libraries:
`pip install -r requirements.txt`

**2. Set your generator**

- create file `.env` and save your OpenAI key as `OPENAI_API_KEY="YOUR_KEY"`

**3. Run streamlit app:** `streamlit run chat_app.py`

## Streamlit chat functionality

### Functionalities

**1. Problem Input: Users can describe their optimization problem.**

**2. ZIMPL Code generator**

The application processes the input and generates:

- .... #TODO
- Decision variables
- An objective function
- Constraints

**3. Interactive Sidebar**

Results are saved for future in the side interface. Saved results include the problem description and the corresponding ZIMPL code. Provides a list of all saved results for easy navigation. Allows users to view, edit, or delete saved results directly.