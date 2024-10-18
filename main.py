from flask import Flask
from telegram.ext import Updater, MessageHandler, Filters
import openai
import os
import threading

app = Flask(__name__)

# Function to keep the server alive
@app.route('/')
def home():
    return "Bot is running!"

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("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")

# Function to load the document content from VisabotIQ.txt
def load_document():
    try:
        with open("VisabotIQ.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Sorry, the document is not available at the moment."

# Function to query the OpenAI model with user query and document
def ask_chatgpt(user_query):
    document_content = load_document()
    prompt = f"You have the following document to refer to for visa information:\n{document_content}\nBased on the document, respond to this query: {user_query}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "I'm having trouble getting a response right now."

# Function to handle incoming Telegram messages
def handle_message(update, context):
    user_query = update.message.text
    response = ask_chatgpt(user_query)
    update.message.reply_text(response)

# Main function to set up and run the bot
def main():
    TOKEN = os.getenv("7928907301:AAFPzsmGhFHeP8y9HWpvcGVTHB1GruBa7rY")  # Set this in your environment
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

# Run the Flask app and the Telegram bot in separate threads
if __name__ == '__main__':
    threading.Thread(target=main).start()
    app.run(host='0.0.0.0', port=8080)
