from google import genai


prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name': str, 'ingredients': list[str]}
Return: list[Recipe]"""

client = genai.Client(api_key="API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
)

# Use the response as a JSON string.
print(response.text)


# Gradio arayüzü oluştur
interface = gr.ChatInterface(
    fn=chat_function,
    chatbot=gr.Chatbot(height=500, type='messages'),
    textbox=gr.Textbox(placeholder="Ask a question or request help..."),
    title="AI Assistant",
    examples=[
        "List orders placed in the last 7 days with customer names",
        "What are the top 3 best-selling products?",
        "Which countries do our customers come from?",
    ],
)

# Arayüzü başlat
if __name__ == "__main__":
    interface.launch()
