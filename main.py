# main.py
import os
from dotenv import load_dotenv
import telebot
from telebot import types

# load token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("ERROR: set BOT_TOKEN in .env")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# import phrases
from data.business import BUSINESS_PHRASES
from data.confident import CONFIDENT_PHRASES
from data.authority import AUTHORITY_PHRASES
from data.presentation import PRESENTATION_PHRASES
from data.anticollision import ANTICOLLISION_PHRASES
from data.high_intellect import INTELLECT_PHRASES
from data.emotional_intellect import EMO_PHRASES
from data.block8 import BLOCK8_PHRASES
from data.templates import TEMPLATES

# main menu (reply keyboard)
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("💼 Деловая речь", "💪 Уверенный тон")
    kb.row("🧱 Авторитетный стиль", "🎤 Презентационный стиль")
    kb.row("🤝 Антиконфликт", "🧠 Высокий интеллект")
    kb.row("💓 Эмоциональный интеллект", "⚡ Блок 8")
    kb.row("📚 Шаблоны разговоров", "📞 Контакты")
    return kb

@bot.message_handler(commands=['start', 'help'])
def start_handler(msg):
    bot.send_message(
        msg.chat.id,
        "Привет! Я *TalkingFine_bot* — твой помощник по стилю речи.\n\n"
        "Выбирай раздел на клавиатуре → и получай готовые формулировки (по 20 примеров).",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# helper: send list in pages (to avoid super-long messages)
def send_list(chat_id, title, items):
    # split into chunks of N phrases (we'll send up to 10 per message)
    chunk_size = 10
    total = len(items)
    bot.send_message(chat_id, f"📌 *{title}* — всего {total} примеров.", parse_mode="Markdown")
    for i in range(0, total, chunk_size):
        chunk = items[i:i+chunk_size]
        text = "\n\n".join([f"{i+j+1}. {p}" for j, p in enumerate(chunk)])
        bot.send_message(chat_id, text, parse_mode=None)

@bot.message_handler(func=lambda m: True)
def router(m):
    text = (m.text or "").strip()

    mapping = {
        "💼 Деловая речь": ("Деловая речь", BUSINESS_PHRASES),
        "💪 Уверенный тон": ("Уверенный тон", CONFIDENT_PHRASES),
        "🧱 Авторитетный стиль": ("Авторитетный стиль", AUTHORITY_PHRASES),
        "🎤 Презентационный стиль": ("Презентационный стиль", PRESENTATION_PHRASES),
        "🤝 Антиконфликт": ("Антиконфликт", ANTICOLLISION_PHRASES),
        "🧠 Высокий интеллект": ("Высокий интеллект", INTELLECT_PHRASES),
        "💓 Эмоциональный интеллект": ("Эмоциональный интеллект", EMO_PHRASES),
        "⚡ Блок 8": ("Блок 8", BLOCK8_PHRASES),
        "📚 Шаблоны разговоров": ("Шаблоны разговоров", TEMPLATES),
    }

    if text in mapping:
        title, items = mapping[text]
        send_list(m.chat.id, title, items)
        # return to menu after
        bot.send_message(m.chat.id, "Выберите следующий раздел:", reply_markup=main_menu())
        return

    if text == "📞 Контакты":
        bot.send_message(m.chat.id,
                         "Контакты:\nMSL72Rph\nGitHub: https://github.com/rolloerro",
                         reply_markup=main_menu())
        return

    # fallback
    bot.send_message(m.chat.id, "Выбери раздел на клавиатуре 👇", reply_markup=main_menu())

if __name__ == "__main__":
    print("TalkingFine_bot started")
    bot.infinity_polling(skip_pending=True)
