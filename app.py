import streamlit as st
from nl_to_sql import generate_sql, is_query_safe, execute_query

st.set_page_config(page_title="AI-Powered Query Assistant", layout="centered")

st.title("AI-Powered Query Assistant")
st.write("Ask questions about the supply chain database in plain English.")

question = st.text_input("Enter your question:", placeholder="e.g. Which warehouse has the most delayed orders?")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL..."):
            sql = generate_sql(question)

        st.subheader("Generated SQL")
        st.code(sql, language="sql")

        safe, message = is_query_safe(sql)

        if not safe:
            st.error(f"Query blocked: {message}")
        else:
            with st.spinner("Running query..."):
                columns, results = execute_query(sql)

            if columns is None:
                st.error(results)
            else:
                st.subheader("Results")
                if len(results) == 0:
                    st.info("No results found.")
                else:
                    st.dataframe([dict(zip(columns, row)) for row in results])