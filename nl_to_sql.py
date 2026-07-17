import os
import mysql.connector
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

SCHEMA = """
Table: orders
- Order_ID (varchar) - primary key
- Product_ID (varchar) - foreign key referencing products.Product_ID
- Warehouse_ID (varchar) - foreign key referencing warehouses.Warehouse_ID
- Supplier_ID (varchar) - foreign key referencing suppliers.Supplier_ID
- Order_Date (varchar)
- Expected_Delivery_Date (date)
- Actual_Delivery_Date (varchar)
- Order_Status (varchar)
- Quantity_Ordered (int)

Table: products
- Product_ID (varchar) - primary key
- Product_Name (varchar)
- Category (varchar)
- Unit_Price_INR (decimal)

Table: warehouses
- Warehouse_ID (varchar) - primary key
- Warehouse_City (varchar)
- Warehouse_Capacity (int)

Table: suppliers
- Supplier_ID (varchar) - primary key
- Supplier_Name (varchar)
- Supplier_Rating (decimal)
- Region (varchar)

Table: inventory
- Product_ID (varchar) - foreign key referencing products.Product_ID
- Warehouse_ID (varchar) - foreign key referencing warehouses.Warehouse_ID
- Stock_Quantity (int)
- Reorder_Level (int)
"""


def generate_sql(user_question):
    prompt = f"""
You are a MySQL expert. Given the database schema below, write a single SQL SELECT query that answers the user's question.

Rules:
- Only return the SQL query, nothing else. No explanations, no markdown, no code fences.
- Only use SELECT statements. Never use INSERT, UPDATE, DELETE, or DROP.
- Use proper JOINs based on the foreign key relationships described in the schema.

Schema:
{SCHEMA}

Question: {user_question}

SQL Query:
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def is_query_safe(sql_query):
    cleaned = sql_query.strip().lower()

    if not cleaned.startswith("select"):
        return False, "Only SELECT queries are allowed."

    dangerous_keywords = ["drop", "delete", "update", "insert", "alter", "truncate", "create", "grant", "revoke"]
    for keyword in dangerous_keywords:
        if keyword in cleaned:
            return False, f"Query contains a forbidden keyword: '{keyword}'"

    return True, "Query is safe."


def execute_query(sql_query):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return columns, results
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"


if __name__ == "__main__":
    question = "Which supplier has the lowest rating?"
    sql = generate_sql(question)
    print("Generated SQL:\n", sql)

    safe, message = is_query_safe(sql)
    print("\nValidation result:", message)

    if safe:
        columns, results = execute_query(sql)
        print("\nColumns:", columns)
        print("Results:")
        for row in results:
            print(row)
    else:
        print("Query blocked for safety reasons.")