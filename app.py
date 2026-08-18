import pandas as pd
import streamlit as st

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# Streamlit page settings
st.set_page_config(
    page_title="Data Analysis Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Data Analysis Agent")
st.write("Upload a CSV file, view charts, and ask questions using a free local Ollama agent.")


# CSV upload
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Please upload a CSV file to start analysis.")
    st.stop()


# CSV read
try:
    df = pd.read_csv(uploaded_file)

except Exception as error:
    st.error(f"CSV file read nahi ho saki: {error}")
    st.stop()


# Agent tools: CSV data direct use hoga.
# Streamlit session state use nahi ho rahi, isliye agent error nahi aayega.
def build_tools(data):

    @tool
    def dataset_overview() -> str:
        """Get rows, columns, column names, and data types."""

        return (
            f"Rows: {len(data)}\n"
            f"Columns: {len(data.columns)}\n\n"
            f"Column names:\n{', '.join(data.columns)}\n\n"
            f"Data types:\n{data.dtypes.astype(str).to_string()}"
        )

    @tool
    def numeric_summary() -> str:
        """Get count, mean, minimum, maximum, and quartiles for numeric columns."""

        numeric_data = data.select_dtypes(include="number")

        if numeric_data.empty:
            return "This dataset has no numeric columns."

        return numeric_data.describe().to_string()

    @tool
    def top_categories(column: str) -> str:
        """Get the top 10 most frequent values for a valid column name."""

        if column not in data.columns:
            return (
                f"Column '{column}' does not exist.\n"
                f"Available columns: {', '.join(data.columns)}"
            )

        return data[column].value_counts().head(10).to_string()

    @tool
    def total_by_group(group_column: str, value_column: str) -> str:
        """Sum a numeric column grouped by another column."""

        if group_column not in data.columns:
            return f"Column '{group_column}' does not exist."

        if value_column not in data.columns:
            return f"Column '{value_column}' does not exist."

        if not pd.api.types.is_numeric_dtype(data[value_column]):
            return f"'{value_column}' is not a numeric column."

        result = (
            data.groupby(group_column)[value_column]
            .sum()
            .sort_values(ascending=False)
            .head(20)
        )

        return result.to_string()

    return [
        dataset_overview,
        numeric_summary,
        top_categories,
        total_by_group,
    ]


# Uploaded CSV ke liye tools create karna
tools = build_tools(df)


# Data preview
st.subheader("1. Data Preview")
st.dataframe(df.head(20), width="stretch")


# Quick summary
st.subheader("2. Quick Summary")

column_1, column_2, column_3 = st.columns(3)

column_1.metric("Rows", len(df))
column_2.metric("Columns", len(df.columns))
column_3.metric("Missing Values", int(df.isnull().sum().sum()))


# Data types
with st.expander("View column names and data types"):
    st.dataframe(
        pd.DataFrame(
            {
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
            }
        ),
        width="stretch",
    )


# Visualization
st.subheader("3. Data Visualization")

numeric_columns = df.select_dtypes(include="number").columns.tolist()
category_columns = df.select_dtypes(exclude="number").columns.tolist()

if numeric_columns:
    chart_type = st.selectbox(
        "Select chart type",
        ["Bar chart: total by category", "Line chart", "Histogram"],
    )

    value_column = st.selectbox(
        "Select numeric column",
        numeric_columns,
    )

    if chart_type == "Bar chart: total by category":
        if category_columns:
            group_column = st.selectbox(
                "Select category column",
                category_columns,
            )

            chart_data = (
                df.groupby(group_column)[value_column]
                .sum()
                .sort_values(ascending=False)
                .head(20)
            )

            st.bar_chart(chart_data)

        else:
            st.warning("No category column available for a bar chart.")

    elif chart_type == "Line chart":
        st.line_chart(df[value_column])

    elif chart_type == "Histogram":
        histogram_data = (
            pd.cut(df[value_column], bins=10)
            .value_counts()
            .sort_index()
        )

        st.bar_chart(histogram_data)

else:
    st.warning("No numeric columns found, so charts cannot be created.")


# Free local Ollama model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

available_columns = ", ".join(df.columns)


# Create Data Analysis Agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=f"""
You are a careful data analysis assistant.

Available dataset columns are:
{available_columns}

Always use the available tools before answering a dataset question.
Never invent values.
Use exact column names.
""",
)


# Ask Agent section
st.subheader("4. Ask the Data Analysis Agent")

question = st.text_input(
    "Ask a question about your CSV data",
    placeholder="Example: What is the total Sales for each Category?",
)

if st.button("Ask Agent", type="primary"):
    if not question:
        st.warning("Please write a question first.")

    else:
        with st.spinner("Agent is analyzing your data..."):
            try:
                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": question,
                            }
                        ]
                    }
                )

                answer = result["messages"][-1].content

                st.success("Analysis complete")
                st.write(answer)

            except Exception as error:
                st.error(f"Agent error: {error}")