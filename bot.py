import os
import telebot
import anthropic

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

conversation_history = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text
    
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        "role": "user",
        "content": user_text
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=conversation_history[user_id]
    )
    
    assistant_message = response.content[0].text
    
    conversation_history[user_id].append({
        "role": "assistant", 
        "content": assistant_message
    })
    
    bot.reply_to(message, assistant_message)

bot.polling()
