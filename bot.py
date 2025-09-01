import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
START_MESSAGE = """
Привіт! 👋
Я — офіційний бот сервісу **Автовикуп** 🚗💨

Ми допомагаємо з:
✅ Продажем авто після пожежі або ДТП  
✅ Швидкою оцінкою авто  
✅ Продажем будь-яких автомобілів швидко та вигідно  

Щоб ми могли швидко оцінити ваше авто, залиште інформацію у такому форматі:  
1️⃣ Ваш Telegram або номер телефону  
2️⃣ Пробіг авто (км)  
3️⃣ Короткий опис авто: наприклад, стан кузова, мотор, особливості  
✨ Чим детальніше опишете авто, тим швидше і вигідніше ми допоможемо!  

Наші контакти для зв'язку:
📞 Телефон: {Телефон}
💬 Telegram: {Telegram}

Ми зв’яжемося з вами протягом 24 годин! ⏰
""".format(**CONTACTS)

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
        bot.send_message(call.message.chat.id, "✍️ Будь ласка, напишіть ваше повідомлення у форматі:\n\n"
                                               "1️⃣ Telegram або номер телефону\n"
                                               "2️⃣ Пробіг авто (км)\n"
                                               "3️⃣ Короткий опис авто (стан кузова, мотор, особливості)\n\n"
                                               "✨ Чим детальніше опишете авто, тим швидше і вигідніше ми допоможемо!")
    elif call.data == "contacts":
        bot.send_message(call.message.chat.id, f"📞 Телефон: {CONTACTS['Телефон']}\n💬 Telegram: {CONTACTS['Telegram']}")

# Обробка повідомлень від клієнтів
@bot.message_handler(func=lambda message: True)
def handle_client(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text

    # Відправка адмінові
    for admin in ADMINS:
        bot.send_message(admin, f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{text}\n\n"
                               f"💡 Пам’ятайте перевірити пробіг та опис авто!")

    # Підтвердження клієнту
    bot.reply_to(message, "Дякуємо! ✅ Ваші дані отримані, ми зв’яжемося з вами найближчим часом. "
                          "Підготуйте, будь ласка, фото авто для оцінки 📸")

# Запуск бота
bot.infinity_polling()
