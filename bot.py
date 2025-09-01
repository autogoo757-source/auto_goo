import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

# 🌟 Ваш бот-токен
TOKEN = "8054778077:AAF9wNFN4v5KdDyVdMkmHB86TgJfrhJ7-a8"
bot = telebot.TeleBot(TOKEN)

# 👑 Адмін бота
ADMINS = [7290935924]

# 📞 Контакти компанії
CONTACTS = {
    "Телефон": "+380731443477",
    "Telegram": "@auto_vukyp_M"
}

# 📝 Стартове повідомлення для клієнтів
START_MESSAGE = f"""
Привіт! 👋
Я — офіційний бот сервісу **Автовикуп** 🚗💨

Ми допомагаємо з:
✅ Продажем авто після пожежі або ДТП  
✅ Швидкою оцінкою авто  
✅ Продажем будь-яких автомобілів швидко та вигідно  

Щоб ми могли швидко оцінити ваше авто, залиште інформацію у такому форматі:  
1️⃣ Пробіг авто (км)  
2️⃣ Короткий опис авто (стан кузова, мотор, особливості)  
3️⃣ Ваш Telegram або номер телефону  
✨ Чим детальніше опишете авто, тим швидше і вигідніше ми допоможемо!  

Наші контакти для зв'язку:
📞 Телефон: {CONTACTS['Телефон']}
💬 Telegram: {CONTACTS['Telegram']}

Ми зв’яжемося з вами протягом 24 годин! ⏰
"""

# 🔹 Кнопки для клієнтів
def main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📄 Залишити заявку", callback_data="apply"))
    keyboard.add(InlineKeyboardButton("📞 Контакти", callback_data="contacts"))
    return keyboard

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=main_keyboard())

# Обробка натискань на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "apply":
        bot.send_message(
            call.message.chat.id,
            "✍️ Будь ласка, напишіть ваше повідомлення у форматі:\n\n"
            "1️⃣ Пробіг авто (км)\n"
            "2️⃣ Короткий опис авто (стан кузова, мотор, особливості)\n"
            "3️⃣ Ваш Telegram або номер телефону\n\n"
            "✨ Чим детальніше опишете авто, тим швидше і вигідніше ми допоможемо!"
        )
    elif call.data == "contacts":
        bot.send_message(call.message.chat.id, f"📞 Телефон: {CONTACTS['Телефон']}\n💬 Telegram: {CONTACTS['Telegram']}")

# Обробка всіх повідомлень (текст + фото)
@bot.message_handler(content_types=['text', 'photo', 'document'])
def handle_client(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Пересилання адміну
    for admin in ADMINS:
        # Если текст
        if message.content_type == 'text':
            bot.send_message(admin, f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.text}")
        # Если фото
        elif message.content_type == 'photo':
            # Берем самое большое фото
            photo_id = message.photo[-1].file_id
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Фото без опису'}"
            bot.send_photo(admin, photo_id, caption=caption)
        # Если документ
        elif message.content_type == 'document':
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Документ'}"
            bot.send_document(admin, message.document.file_id, caption=caption)

    # Подтверждение клиенту
    bot.reply_to(
        message,
        "Дякуємо! ✅ Ваші дані отримані, ми зв’яжемося з вами найближчим часом. "
        "Підготуйте, будь ласка, фото авто для оцінки 📸"
    )

# Запуск бота
bot.infinity_polling()
