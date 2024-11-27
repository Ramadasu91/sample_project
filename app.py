import streamlit as st
from esprima import parseScript
from eslint import ESLint

# Parse JavaScript code using Esprima
def parse_code_with_esprima(code):
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

# Lint JavaScript code using ESLint
def lint_code_with_eslint(code):
    try:
        eslint = ESLint()
        linting_results = eslint.lint_text(code)
        return linting_results[0]["messages"] if linting_results else []
    except Exception as e:
        return [{"message": str(e)}]

# Summarize AST analysis into a readable format
def summarize_code(ast_analysis):
    functions = ast_analysis.get("functions", [])
    variables = ast_analysis.get("variables", [])

    summary = "Summary of Code:\n"
    summary += f"- Functions: {', '.join(functions) if functions else 'None'}\n"
    summary += f"- Variables: {', '.join(variables) if variables else 'None'}\n"
    return summary

# Streamlit application
st.title("JavaScript Code Analyzer")

# Input for JavaScript code
code_input = st.text_area("Paste your JavaScript code here:")

if st.button("Analyze Code"):
    if not code_input.strip():
        st.error("Please provide valid JavaScript code.")
    else:
        # Step 1: Parse the code
        ast_analysis = parse_code_with_esprima(code_input)
        if "error" in ast_analysis:
            st.error(f"Parsing Error: {ast_analysis['error']}")
        else:
            st.success("Code successfully parsed.")
            st.text(summarize_code(ast_analysis))
        
        # Step 2: Lint the code
        lint_results = lint_code_with_eslint(code_input)
        if lint_results:
            st.subheader("Linting Results")
            for issue in lint_results:
                st.error(f"[{issue.get('ruleId', 'No Rule ID')}] {issue.get('message')} at line {issue.get('line', '-')}")
        else:
            st.success("No linting issues found!")

if st.button("Ask a Question"):
    question = st.text_input("Enter your question:")
    if question.strip():
        ast_analysis = parse_code_with_esprima(code_input)
        if "function" in question.lower():
            st.info("Here are the detected functions:")
            st.write(ast_analysis.get("functions", "No functions detected."))
        elif "variable" in question.lower():
            st.info("Here are the detected variables:")
            st.write(ast_analysis.get("variables", "No variables detected."))
        else:
            st.warning("Sorry, I can't answer that question yet!")
