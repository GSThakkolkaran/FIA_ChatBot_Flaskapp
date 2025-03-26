from flask import Flask, request, jsonify, render_template
import pandas as pd
import demjson3
from sqlalchemy import create_engine
import requests
import urllib
import time
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

# Database connection
server = "localhost"
database = "master"
username = "SA"
password = "MyStrongPass123"

connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TrustServerCertificate=yes;"
)

quoted = urllib.parse.quote_plus(connection_string)
connection_uri = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(quoted)
engine_azure = create_engine(connection_uri, echo=False)

# Together AI API details
API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = "35c48c4d5f73003a9990fdcc01756be7b093b88c6183195706b2de96e8d1d5a5"  # Replace with your API key
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"


def ask_llama(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.json()}"
    except requests.RequestException as e:
        return f"Request failed: {str(e)}"


def generate_SQL_query(natural_query: str) -> str:
    schema={"sql_query": "GENERATED_SQL_QUERY_HERE"}
    """Generate only the query condition using LLaMA 3.3 70B and return it as JSON."""
    prompt = f"""
            You are an AI assistant that generates SQL queries based on user input.  
            Your task is to convert the user's natural language request into a valid SQL query for a table with the following schema:

            ###Table name : compliance_data

            ### **User Query:** "{natural_query}" 

            ##Table information
            
            - `Company`: Name of the company (nvarchar)  
            - `Tax_Compliance`: Yes or No (nvarchar)  
            - `Audit_Compliance`: Yes or No (nvarchar)  
            - `Financial_Statement_Filed`: Yes or No (nvarchar)  
            - `AML_Compliance`: Yes or No (nvarchar)  
            - `Penalty_Amount`: Numerical (int, in dollars)  
            - `Annual_Revenue`: Company revenue in USD (int)  
            - `Profit_Declared`: Profit in dollars (int)  
            - `Total_Assets`: Value of assets in dollars (int)  
            - `Submission_Status`: Low or Medium or High (nvarchar)  
            
            ### Constraints:
            1. Generate a valid **T-SQL query** based on the user request.
            2. Ensure the output is strictly in **JSON format** with the key `"sql_query"`.
            3. Do **not** include any additional text, explanations, or comments in the output.
            4.nvarchar values shold be in single qouts, example 'No' , 'Low'
            
            ### Output Format:{schema}
        """
    response_text = ask_llama(prompt)
    return response_text


def generate_natural_response(user_question, df):
    prompt=f"""
    Generates a meaningful natural language response based on the user's question and a Pandas DataFrame.

    Parameters:
    user_question: The natural language question asked by the user{user_question}.
    Answer: {df} 

    Returns:
    A well-formed response based on the data. just give answer only.
    """
    response_text = ask_llama(prompt)
    return response_text


def generate_response(user_query):
    response = generate_SQL_query(user_query)
    res = demjson3.decode(response)
    sql_query = res['sql_query']
    result = pd.read_sql_query(sql_query, engine_azure)
    
    if not result.empty:
        if result.shape[0] < 4:
            time.sleep(10)
            output = generate_natural_response(user_query, result)
        else:
            output = result.to_html(index=False, escape=False)
    else:
        output = "No data found."
    return output

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def compliance_chatbot():
    try:
        user_query = request.json.get("query", "")
        response = generate_response(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
