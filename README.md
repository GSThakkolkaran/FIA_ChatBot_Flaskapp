# FIA_ChatBot_Flaskapp
# FIA Compliance Chatbot - Setup & Run Guide

This document provides step-by-step instructions to set up and run the FIA Compliance Chatbot using Flask.

## 1. Prerequisites
Before running the chatbot, ensure you have the following installed:
- Python (version 3.7 or later)
- pip (Python package manager)
- Microsoft ODBC Driver for SQL Server (for database connection)

## 2. Project Structure
Make sure your project is structured as follows:

```
Flask_App/
│── main.py                 # Flask backend  
│── requirements.txt         # Dependencies  
│── templates/               # HTML files must be inside this folder  
│   ├── index.html           # Chatbot frontend  
│── compliance.csv           # Sample dataset  
```

## 3. Sample Dataset
A sample dataset named `compliance.csv` is included for testing. It contains sample financial compliance data:
```
Company,Tax_Compliance,Audit_Compliance,Penalty_Amount
ABC Corp,Yes,No,5000
XYZ Ltd,No,Yes,10000
DEF Inc,Yes,Yes,0
```

## 4. Install Dependencies
Navigate to the project directory and install the required dependencies:

```bash
pip install -r requirements.txt
```

## 5. Run the Flask Application
Start the chatbot server by running:

```bash
python main.py
```

You should see output similar to:

```
 * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
```

## 6. Access the Chatbot
- Open your browser and go to:
  ```
  http://127.0.0.1:8000/
  ```
- Start interacting with the chatbot!

## 7. Troubleshooting
### Issue: Template Not Found
Ensure your `index.html` file is inside the `templates/` directory.

### Issue: Missing Dependencies
Run the following command again:
```bash
pip install -r requirements.txt
```

### Issue: Database Connection Errors
Check if your SQL Server is running and update the database connection details in `main.py`.

---

You're all set! 🚀 If you have any issues, feel free to ask for help.

