import tempfile
import csv
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from agno.agent import Agent
from agno.models.cohere import Cohere
from agno.tools.duckdb import DuckDbTools
from agno.tools.pandas import PandasTools


# ==============================
# SESSION MEMORY
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "cohere_key" not in st.session_state:
    st.session_state.cohere_key = ""


# ==============================
# PREPROCESS FUNCTION
# ==============================
def preprocess_and_save(files):
    try:
        dfs = []

        for file in files:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])
            else:
                st.error("Unsupported file format.")
                return None, None, None

            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        # Clean string columns
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)

        # Convert date columns
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Save temp CSV for DuckDB
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

        return temp_path, df.columns.tolist(), df

    except Exception as e:
        st.error(e)
        return None, None, None


# ==============================
# UI
# ==============================
st.set_page_config(page_title="Enterprise AI Data Analyst", layout="wide")
st.title("📊 Enterprise AI Data Analyst (Cohere)")

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.selectbox("User Mode", ["Client", "Analyst", "Admin"])

    cohere_key = st.text_input("Cohere API Key", type="password")

    if cohere_key:
        st.session_state.cohere_key = cohere_key


# ==============================
# FILE UPLOAD
# ==============================
uploaded_files = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)


# ==============================
# PROCESS
# ==============================
if uploaded_files and st.session_state.cohere_key:

    temp_path, columns, df = preprocess_and_save(uploaded_files)

    if df is not None:

        # ==============================
        # DATA PREVIEW
        # ==============================
        st.subheader("📂 Data Preview")
        st.dataframe(df, use_container_width=True)

        # ==============================
        # DATA CLEANING
        # ==============================
        st.subheader("🧹 Data Cleaning")

        missing = df.isnull().sum()
        st.dataframe(missing)

        if st.button("Auto Clean Data"):
            df.ffill(inplace=True)  # modern fix
            df.drop_duplicates(inplace=True)
            st.success("Data cleaned successfully!")

        # ==============================
        # KPI DASHBOARD
        # ==============================
        st.subheader("📈 KPI Dashboard")

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:
            kpi_cols = st.columns(min(4, len(numeric_cols)))

            for i, col in enumerate(numeric_cols[:4]):
                kpi_cols[i].metric(col, round(df[col].mean(), 2))

        # ==============================
        # VISUALIZATION
        # ==============================
        st.subheader("📊 Visualization")

        if len(numeric_cols) > 0:
            chart_col = st.selectbox("Select column", numeric_cols)

            if st.button("Generate Chart"):
                st.line_chart(df[chart_col])

        # ==============================
        # FORECASTING
        # ==============================
        st.subheader("🔮 Forecasting")

        if len(numeric_cols) > 0:
            target = st.selectbox("Target Column", numeric_cols)

            if st.button("Predict Future Value"):
                X = np.arange(len(df)).reshape(-1, 1)
                y = df[target].values

                model = LinearRegression()
                model.fit(X, y)

                future = model.predict(np.array([[len(df) + 5]]))
                st.success(f"Predicted future value: {future[0]:.2f}")

        # ==============================
        # DUCKDB + AGENT
        # ==============================
        duckdb_tools = DuckDbTools()
        duckdb_tools.load_local_csv_to_table(path=temp_path, table="uploaded_data")

        data_analyst_agent = Agent(
            model=Cohere(
                api_key=st.session_state.cohere_key,
                id="command-a-03-2025"
            ),
            tools=[duckdb_tools, PandasTools()],
            system_message="""
You are an enterprise AI business and data analyst.
Use SQL and pandas to analyze the uploaded data.

Provide:
• Trends
• Risks
• Opportunities
• Forecasting insights
• Business recommendations.

Explain everything in simple business language.
""",
            markdown=True,
        )

        # ==============================
        # AI CHAT
        # ==============================
        st.subheader("💬 AI Chat")

        user_query = st.text_area("Ask questions about your data")

        if st.button("Submit Query"):
            if user_query.strip():
                with st.spinner("Analyzing data..."):
                    response = data_analyst_agent.run(user_query)

                    if hasattr(response, "content"):
                        response_content = response.content
                    else:
                        response_content = str(response)

                    st.session_state.chat_history.append(("User", user_query))
                    st.session_state.chat_history.append(("AI", response_content))
            else:
                st.warning("Please enter a query.")

        # ==============================
        # CHAT HISTORY
        # ==============================
        for role, msg in st.session_state.chat_history:
            if role == "User":
                st.write(f"👤 {msg}")
            else:
                st.write(f"🤖 {msg}")

        # ==============================
        # EXPORT INSIGHTS
        # ==============================
        if st.session_state.chat_history:
            export_text = "\n".join([f"{r}: {m}" for r, m in st.session_state.chat_history])

            st.download_button(
                "📥 Download Insights",
                export_text,
                file_name="insights.txt"
            )