# AI-Powered Supply Chain Query Assistant

A Natural Language-to-SQL assistant that lets users query a supply chain database using plain English — no SQL knowledge required. Built with Groq's Llama-3, Streamlit, and MySQL, the tool translates business questions into secure SQL queries and returns real-time insights.

## 🎯 Problem It Solves

Business teams often need data from operational databases but don't know SQL, creating a bottleneck where every question has to go through a data analyst. This assistant removes that bottleneck by letting non-technical users self-serve their own data questions in plain English.

## 🛠️ Technologies Used

- **Python** — core application logic
- **Groq API (Llama-3)** — natural language understanding and SQL generation
- **Streamlit** — interactive web interface
- **MySQL** — backend supply chain database
- **Prompt Engineering** — structured prompting for reliable, safe SQL generation

## 📌 Features

- Converts plain-English questions into SQL queries in real time
- Validates generated SQL before execution to prevent unsafe or malformed queries
- Connects directly to a MySQL database for live data retrieval
- Returns results in a clean, readable format via a Streamlit interface
- Enables non-technical users to explore supply chain data without writing a single line of SQL

## ⚙️ How It Works

1. User types a question in plain English (e.g., *"Which category had the highest cancellation rate last month?"*)
2. The query is sent to Groq's Llama-3 model along with the database schema as context
3. The model generates a corresponding SQL query
4. The query is validated to check for safety and correctness before execution
5. The validated query runs against the MySQL database
6. Results are displayed back to the user in the Streamlit app



## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- MySQL database with supply chain data
- Groq API key


### Configuration

Create a `.env` file in the root directory with your credentials:

```
GROQ_API_KEY=your_groq_api_key
DB_HOST=your_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

### Run the App

http://localhost:8501/

<img width="953" height="740" alt="image" src="https://github.com/user-attachments/assets/a3a374bb-9586-4bca-830f-7281ff056a29" />


## 📋 Project Status

✅ Core NL-to-SQL pipeline complete
✅ Query validation implemented
✅ Streamlit interface functional

## 🔮 Future Improvements

- Add support for more complex multi-table queries
- Visualize results with charts directly in the app
- Add query history and saved queries per user

