import streamlit as st
from generator_flow import generator

if "results" not in st.session_state:
    st.session_state["results"] = []

if "selected_index" not in st.session_state:
    st.session_state["selected_index"] = None

st.title("ZIMPL Code Creator AI")

st.write("""
Enter a description of the optimization problem and the model will generate decisions, objective function, and constraints in ZIMPL.
""")

user_input = st.text_area("Describe your problem:", height=150)

if st.button("Generate code in ZIMPL"):
    if user_input.strip():
        with st.spinner("Generating answer..."):
            try:
                response = generator(user_input)
                st.success("Code is generated.")
                st.text_area("Code ZIMPL:", response, height=300)
                st.session_state["results"].append({
                    "problem": user_input,
                    "code": response
                })
                st.session_state["selected_index"] = len(st.session_state["results"]) - 1
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a description of the problem")

st.sidebar.title("About application")
st.sidebar.info("""
The application is a part of an engineering thesis concerning the creation and verification of optimization problem tasks using AI.
""")

st.sidebar.title("Saved Results")

if st.session_state["results"]:
    if st.session_state["selected_index"] is None:
        st.session_state["selected_index"] = 0

    selected_index = st.sidebar.selectbox(
        "Select a result to view:",
        options=range(len(st.session_state["results"])),
        format_func=lambda x: f"Problem {x + 1}",
        index=st.session_state["selected_index"]
    )

    st.session_state["selected_index"] = selected_index

    selected_result = st.session_state["results"][selected_index]
    st.sidebar.subheader(f"Problem {selected_index + 1}")
    st.sidebar.text_area("Problem Description:", selected_result["problem"], height=100)
    st.sidebar.text_area("Generated Code:", selected_result["code"], height=150)

    if st.sidebar.button("🗑️ Delete Selected Result"):
        del st.session_state["results"][selected_index]

        if st.session_state["results"]:
            st.session_state["selected_index"] = 0
        else:
            st.session_state["selected_index"] = None
        st.rerun()

else:
    st.sidebar.info("No saved results yet.")
