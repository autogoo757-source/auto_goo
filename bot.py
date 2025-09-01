import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🌟 Токен бота
TOKEN = "8054778077:AAF9wNFN4v5KdDyVdMkmHB86TgJfrhJ7-a8"
bot = telebot.TeleBot(TOKEN)

# 👑 Адмін
ADMINS = [7290935924]

# 📞 Контакти компанії
CONTACTS = {
    "Телефон": "+380731443477",
    "Telegram": "@auto_vukyp_M"
}

# 📝 Стартове повідомлення
START_MESSAGE = f"""
👋 Вітаємо у сервісі швидкого та чесного **автовикупу**!

Ми купуємо **будь-які авто** у будь-якому стані:
⚙️ Биті, проблемні, неробочі  
⏳ Старі авто та авто з великим пробігом  
🛑 Без документів та нерастаможені  

⚡ Купуємо швидко, чесно і вигідно!
"""

# 🔹 Головне меню
def main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🚗 Оцінка авто", callback_data="menu_evaluation"))
    keyboard.add(InlineKeyboardButton("📞 Зв'язатися з нами", callback_data="menu_contacts"))
    keyboard.add(InlineKeyboardButton("ℹ️ Умови викупу", callback_data="menu_terms"))
    return keyboard

# 🔹 Кнопка «Назад»
def back_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu_back"))
    return keyboard

# Старт / головне меню
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=main_keyboard())

# Обробка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "menu_evaluation":
        bot.send_message(
            call.message.chat.id,
            "🚗 **Оцінка авто**\n\n"
            "Щоб ми могли швидко оцінити ваше авто, будь ласка, надішліть:\n"
            "1️⃣ Пробіг авто (км)\n"
            "2️⃣ Короткий опис авто (стан кузова, мотор, особливості)\n"
            "3️⃣ Ваш Telegram або номер телефону\n\n"
            "📸 Можна додавати фото або відео для максимально точної оцінки!",
            reply_markup=back_keyboard()
        )
    elif call.data == "menu_contacts":
        bot.send_message(
            call.message.chat.id,
            f"📞 **Зв'язатися з нами**\n\n"
            f"Телефон: {CONTACTS['Телефон']}\n"
            f"Telegram: {CONTACTS['Telegram']}",
            reply_markup=back_keyboard()
        )
    elif call.data == "menu_terms":
        bot.send_message(
            call.message.chat.id,
            "ℹ️ **Умови викупу**\n\n"
            "• Купуємо будь-які авто, будь-якого стану, навіть без документів та нерастаможені\n"
            "• Швидка оцінка та швидка оплата\n"
            "• Прозорі умови і чесна ціна",
            reply_markup=back_keyboard()
        )
    elif call.data == "menu_back":
        bot.send_message(call.message.chat.id, START_MESSAGE, reply_markup=main_keyboard())

# Обробка всіх повідомлень (текст, фото, відео, документи)
@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def handle_client(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    for admin in ADMINS:
        if message.content_type == 'text':
            bot.send_message(admin, f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.text}")
        elif message.content_type == 'photo':
            photo_id = message.photo[-1].file_id
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Фото авто'}"
            bot.send_photo(admin, photo_id, caption=caption)
        elif message.content_type == 'video':
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Відео авто'}"
            bot.send_video(admin, message.video.file_id, caption=caption)
        elif message.content_type == 'document':
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Документ'}"
            bot.send_document(admin, message.document.file_id, caption=caption)

    bot.reply_to(
        message,
        "Дякуємо! ✅ Ваші дані отримані, ми зв’яжемося з вами найближчим часом. "
        "Підготуйте, будь ласка, фото або відео авто для оцінки 📸"
    )

# Запуск бота
bot.infinity_polling()
