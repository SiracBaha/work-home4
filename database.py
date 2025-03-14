import sqlite3
import os
import google.generativeai as genai


   

def natural_to_sql(question, model):
    prompt = f"""
    Convert the following natural language question to a SQL query.
    Return only the raw SQL query without any markdown formatting or backticks.
    
    Database Schema:
    - Categories (CategoryID, CategoryName, Description)
    - Customers (CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country)
    - Employees (EmployeeID, LastName, FirstName, BirthDate, Photo, Notes)
    - Shippers (ShipperID, ShipperName, Phone)
    - Suppliers (SupplierID, SupplierName, ContactName, Address, City, PostalCode, Country, Phone)
    - Products (ProductID, ProductName, SupplierID, CategoryID, Unit, Price)
    - Orders (OrderID, CustomerID, EmployeeID, OrderDate, ShipperID)
    - OrderDetails (OrderDetailID, OrderID, ProductID, Quantity)

    Foreign Key Relationships:
    - Products.CategoryID references Categories.CategoryID
    - Products.SupplierID references Suppliers.SupplierID
    - Orders.EmployeeID references Employees.EmployeeID
    - Orders.CustomerID references Customers.CustomerID
    - Orders.ShipperID references Shippers.ShipperID
    - OrderDetails.OrderID references Orders.OrderID
    - OrderDetails.ProductID references Products.ProductID

    Question: {question}
    
    Rules:
    1. Use the exact column names as shown in the schema
    2. Return only the SQL query without any formatting
    3. For price comparisons, use the Price column from Products table
    4. For dates, use proper SQLite date functions
    5. Make sure to use proper JOIN syntax when querying across tables
    """
    
    response = model.generate_content(prompt)
    sql_query = response.text.strip()
    sql_query = sql_query.replace('```sql', '').replace('```', '')
    sql_query = sql_query.strip()
    return sql_query





def execute_sql_query(conn, sql_query):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return None


def connect_to_database():
    db_path = "/Users/siracbaha/Desktop/work@home4/company.db"
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        print("Successfully connected to database")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def main():
    conn = connect_to_database()
    if conn:
        try:
            # ✅ Define the Gemini model before using it
            genai.configure(api_key="API_KEY")
            model = genai.GenerativeModel("gemini-2.0-flash")  # Define model

            # Example natural language queries
            questions = [
                "Show me all products with price greater than 100",
                "List all orders from the last 7 days with customer names",
                "What are the top 5 most expensive products and their suppliers",
                "Show me the total number of orders per customer in 2024",
                "List all products in each category with their supplier names"
            ]
            
            for question in questions:
                print(f"\nQuestion: {question}")
                sql_query = natural_to_sql(question, model)  # Pass model
                print(f"SQL Query: {sql_query}")
                
                results = execute_sql_query(conn, sql_query)
                if results:
                    print("Results:")
                    for row in results:
                        print(row)
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    main()