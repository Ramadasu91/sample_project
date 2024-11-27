import streamlit as st
from esprima import parseScript

# Function to parse JavaScript code using Esprima
def parse_code_with_esprima(code):
    """
    Parses JavaScript code into an Abstract Syntax Tree (AST)
    and extracts functions and variables.
    """
    try:
        ast = parseScript(code)
        functions = []
        variables = []

        for node in ast.body:
            if node.type == "VariableDeclaration":
                variables.extend([decl.id.name for decl in node.declarations])
            elif node.type == "FunctionDeclaration":
                functions.append(node.id.name)

        return {"functions": functions, "variables": variables, "ast": ast}
    except Exception as e:
        return {"error": str(e)}

# Function to generate a summary from the AST analysis
def summarize_code(ast_analysis):
    """
    Summarizes the extracted information from the AST analysis.
    """
    functions = ast_analysis.get("functions", [])
    variables = ast_analysis.get("variables", [])

    summary = "Summary of Code:\n"
    summary += f"- Functions: {', '.join(functions) if functions else 'None'}\n"
    summary += f"- Variables: {', '.join(variables) if variables else 'None'}\n"
    return summary

# Streamlit application
st.title("JavaScript Code Analyzer")

# Input: User pastes JavaScript code
code_input = st.text_area("Paste your JavaScript code here:")

if st.button("Analyze Code"):
    if not code_input.strip():
        st.error("Please provide valid JavaScript code.")
    else:
        # Step 1: Parse the code using Esprima
        ast_analysis = parse_code_with_esprima(code_input)
        if "error" in ast_analysis:
            st.error(f"Parsing Error: {ast_analysis['error']}")
        else:
            # Step 2: Generate and display the summary
            st.success("Code successfully parsed.")
            st.text(summarize_code(ast_analysis))

if st.button("Ask a Question"):
    question = st.text_input("Enter your question:")
    if question.strip():
        ast_analysis = parse_code_with_esprima(code_input)
        if "error" in ast_analysis:
            st.error(f"Error: {ast_analysis['error']}")
        else:
            # Handle basic queries
            if "function" in question.lower():
                st.info("Here are the detected functions:")
                st.write(ast_analysis.get("functions", "No functions detected."))
            elif "variable" in question.lower():
                st.info("Here are the detected variables:")
                st.write(ast_analysis.get("variables", "No variables detected."))
            else:
                st.warning("Sorry, I can't answer that question yet!")
