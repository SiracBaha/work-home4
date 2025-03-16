import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

db_schema_prompt= """
You are provided with a database schema that contains multiple tables, each with specific columns and properties. Here are the details of the tables:

Table: Catogories
Columns:
CategoryID: INTEGER, primary key, auto-increment
CategoryName: TEXT
Description: TEXT

Table: Customers
Columns:
CustomerID: INTEGER, primary key, auto-increment
CustomerName: TEXT
ContactName: TEXT
Address: TEXT
City: TEXT
PostalCode: TEXT
Country: TEXT

Table: Employees
Columns:
EmployeeID: INTEGER, primary key, auto-increment
LastName: TEXT
FirstName: TEXT
BirthDate: DATE
Photo: TEXT
Notes: TEXT

Table: Shippers
Columns:
ShipperID: INTEGER, primary key, auto-increment
ShipperName: TEXT
Phone: TEXT

Table: Suppliers
Columns:
SupplierID: INTEGER, primary key, auto-increment
SupplierName: TEXT
ContactName: TEXT
Address: TEXT
City: TEXT
PostalCode: TEXT
Country: TEXT
Phone: TEXT

Table: Products
Columns:
ProductID: INTEGER, primary key, auto-increment
ProductName: TEXT
SupplierID: INTEGER, foreign key referencing Suppliers(SupplierID)
CategoryID: INTEGER, foreign key referencing Categories(CategoryID)
Unit: TEXT
Price: NUMERIC, default 0

Table: Orders
Columns:
OrderID: INTEGER, primary key, auto-increment
CustomerID: INTEGER, foreign key referencing Customers(CustomerID)
EmployeeID: INTEGER, foreign key referencing Employees(EmployeeID)
OrderDate: DATETIME
ShipperID: INTEGER, foreign key referencing Shippers(ShipperID)

Table: OrderDetails
Columns:
OrderDetailID: INTEGER, primary key, auto-increment
OrderID: INTEGER, foreign key referencing Orders(OrderID)
ProductID: INTEGER, foreign key referencing Products(ProductID)
Quantity: INTEGER

Relationships:
- Products.SupplierID -> Suppliers.SupplierID
- Products.CategoryID -> Categories.CategoryID
- Orders.CustomerID -> Customers.CustomerID
- Orders.EmployeeID -> Employees.EmployeeID
- Orders.ShipperID -> Shippers.ShipperID
- OrderDetails.OrderID -> Orders.OrderID
- OrderDetails.ProductID -> Products.ProductID

Generate only a SQL query based on the question. Return the response in this exact format:
{
    "sqlQuery": "YOUR_SQL_QUERY_HERE",
    "description": "BRIEF_DESCRIPTION_OF_QUERY"
}


"""

response_prompt = """
You are a chatbot assistant designed to transform Some data to user friendly format. Follow these steps:

1. Read the provided data.
2. Extract the necessary data from these results.
3. Combine and structure this data into a human-readable format.
4. Output the final message in JSON format: 
5. Make sure the message is clear and informative for a general user.

Example structure: 
```json
{
  "message": "string"
}
```

_Expected JSON Output:_  
```json
{
  "message": "We have 3 users: John (30 years old) from New York, Alice (25 years old) from Los Angeles, and Bob (22 years old) from Chicago."
}
```

Remember, your goal is to make the message as clear and informative as possible for a general user. Simplify complex data and highlight the most important parts.

# Give the output result like that:
1- Product Name (€Price) supplied by Supplier Name
2- Product Name (€Price) supplied by Supplier Name

# Do not give the output results like that:
Product Name, Price, Supplier, Product Name, Price, Supplier

# Do not add a text like 'the query returned'. Just explain the data in a user-friendly way.
---

End of system prompt.

"""


# Initialize models for SQL query generation and response generation
sql_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=db_schema_prompt,
    generation_config={
        "temperature": 0.3,
    }
)

response_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=response_prompt,
    generation_config={
        "temperature": 1,
    }
)

# Start chat sessions for both models
sql_chat = sql_model.start_chat(history=[])
response_chat = response_model.start_chat(history=[])
