import gradio as gr
from chatbot import ask

# Create a Gradio interface
demo = gr.ChatInterface(fn=ask, type="messages", title="SqlBot", examples=[
    "Show me all products with price greater than 100.",
    "Which employees have the most orders associated with them, and how many orders have they processed?",
    "List all orders from the last 7 days with customer names.",
    "What are the top 5 most expensive products and their suppliers?",
    "Which customers have placed the most orders, and what is the total quantity of products they have ordered?",
    "What are the top 5 most popular product categories, based on the number of orders containing products from each category?",
    "Show me the total number of orders per customer in 1997.",
    "List all products in each category with their supplier names.",
])

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch()



