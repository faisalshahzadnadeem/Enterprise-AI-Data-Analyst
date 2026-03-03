# 📊 Enterprise AI Data Analyst (Cohere + DuckDB + Streamlit)

An enterprise-grade AI-powered data analysis application built with **Streamlit**, **Cohere LLM**, **DuckDB**, and **Scikit-Learn**.

This tool allows users to upload CSV or Excel files, clean data, generate KPIs, visualize trends, perform forecasting, and interact with an AI Data Analyst agent using natural language queries.

---

## 🚀 Features

### 📂 Multi-File Upload

* Supports `.csv` and `.xlsx`
* Combines multiple files into a single dataset
* Handles missing values like `NA`, `N/A`, and `missing`

### 🧹 Automatic Data Cleaning

* Forward fills missing values
* Removes duplicates
* Converts date columns automatically
* Cleans string formatting for SQL compatibility

### 📊 Data Preview

* Interactive dataframe display
* Missing value summary

### 📈 KPI Dashboard

* Automatically detects numeric columns
* Displays average metrics for up to 4 KPIs

### 📊 Visualization

* Dynamic column selection
* One-click line chart generation

### 🔮 Forecasting

* Linear Regression-based future prediction
* Predicts value for upcoming data points

### 🧠 AI Data Analyst (Powered by Cohere)

* Uses **Agno Agent Framework**
* SQL analysis via DuckDB
* Pandas-based data manipulation
* Business-level explanations
* Provides:

  * Trends
  * Risks
  * Opportunities
  * Forecasting insights
  * Strategic recommendations

### 💬 AI Chat Interface

* Ask questions about uploaded data
* Maintains session chat history
* Business-friendly AI explanations

### 📥 Export Insights

* Download chat conversation as `.txt` file

---

## 🏗️ Tech Stack

* **Frontend**: Streamlit
* **LLM Model**: Cohere (`command-a-03-2025`)
* **Agent Framework**: Agno
* **SQL Engine**: DuckDB
* **Data Processing**: Pandas, NumPy
* **Machine Learning**: Scikit-Learn (Linear Regression)

---

## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/enterprise-ai-analyst.git
cd enterprise-ai-analyst
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a requirements file, install manually:

```bash
pip install streamlit pandas numpy scikit-learn agno cohere duckdb openpyxl
```

---

## 🔑 Cohere API Key

You must provide a valid **Cohere API Key** in the sidebar before using AI features.

Get your key from:
👉 [https://dashboard.cohere.com/](https://dashboard.cohere.com/)

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser.

---

## 🧠 How It Works

1. User uploads CSV/Excel files.
2. Files are merged and cleaned.
3. Data is stored temporarily as a CSV.
4. DuckDB loads the dataset as a SQL table.
5. Agno Agent connects:

   * Cohere LLM
   * DuckDB tools
   * Pandas tools
6. User asks natural language questions.
7. Agent runs SQL + Pandas analysis.
8. AI returns business-friendly insights.

---

## 🏢 User Modes

The application supports three modes:

* **Client** – Business users
* **Analyst** – Data analysts
* **Admin** – Advanced users

(Mode can be extended for role-based access control.)

---

## 📊 Example Use Cases

* Sales trend analysis
* Revenue forecasting
* Customer churn detection
* Risk assessment
* Financial modeling
* KPI tracking dashboards
* Business intelligence automation

---

## 🔐 Security Notes

* API keys are stored only in session state.
* Uploaded files are processed locally.
* Temporary CSV files are generated for DuckDB execution.

For production:

* Add authentication
* Use encrypted secrets management
* Deploy behind secure server

---

## 🛠️ Future Improvements

* Role-based AI response behavior
* Advanced forecasting models (ARIMA, Prophet)
* Automated anomaly detection
* Dashboard export to PDF
* Multi-agent orchestration
* Real-time database connections
* Vector memory integration (RAG)

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built as an Enterprise AI Business Intelligence System using:

* Cohere LLM
* Agno Agents
* DuckDB SQL Engine
* Streamlit Framework

