from telegram.ext import Updater, MessageHandler, Filters
import openai
import os

# Assuming keep_alive.py correctly defines the keep_alive function
from keep_alive import keep_alive  

keep_alive()


# Set your OpenAI API Key here
openai.api_key = "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"  # Replace with your actual OpenAI API key

# Function to load the document content from VisabotIQ.txt
def load_document():
    with open("VisabotIQ.txt", "r") as file:
        return file.read()

# Function to query the gpt-3.5-turbo model with the user query and document
def ask_chatgpt(user_query):
    document_content = load_document()

    prompt = f"""You have the following document to refer to for visa information:
    {document_content}

    Based on the document, respond to this query: {user_query}
    """

    # Use the gpt-3.5-turbo model for conversational response with limited tokens
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant helping with visa information."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.5
    )

    return response['choices'][0]['message']['content'].strip()

# Function to handle incoming Telegram messages
def handle_message(update, context):
    if update.message and update.message.text:
        user_query = update.message.text
        print(f"Received message: {user_query}")

        response = ask_chatgpt(user_query)
        update.message.reply_text(response)

    elif update.channel_post and update.channel_post.text:
        user_query = update.channel_post.text
        print(f"Received channel post: {user_query}")

        response = ask_chatgpt(user_query)
        context.bot.send_message(chat_id=update.channel_post.chat_id, text=response)

    else:
        if update.message:
            update.message.reply_text("Please send a text message for assistance.")
        elif update.channel_post:
            context.bot.send_message(chat_id=update.channel_post.chat_id, text="Please send a text message for assistance.")

# Main function to set up and run the bot
def main():
    TOKEN = "7928907301:AAFPzsmGhFHeP8y9HWpvcGVTHB1GruBa7rY"  # Replace with your Telegram Bot token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
