import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🌟 Токен бота
TOKEN = "8054778077:AAF9wNFN4v5KdDyVdMkmHB86TgJfrhJ7-a8"
bot = telebot.TeleBot(TOKEN)

# 👑 Адмін бота
ADMINS = [7290935924]

# 📞 Контакти компанії
CONTACTS = {
    "Телефон": "+380731443477",
    "Telegram": "@auto_vukyp_M"
}

# 📝 Стартове сообщение
START_MESSAGE = f"""
👋 Вітаємо у сервісі швидкого та чесного **автовикупу**!

Ми купуємо будь-які авто:
🔥 Після пожежі та ДТП  
⏳ Старі або з великим пробігом  
⚙️ Неробочі або проблемні  
✨ А також доглянуті та справні машини

Щоб оцінка авто була максимально точною, оберіть категорію: 
"""

# 🔹 Главные кнопки категорий
def category_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔥 Після ДТП", callback_data="category_accident"))
    keyboard.add(InlineKeyboardButton("🔥 Після пожежі", callback_data="category_fire"))
    keyboard.add(InlineKeyboardButton("⏳ Швидка оцінка", callback_data="category_quick"))
    keyboard.add(InlineKeyboardButton("✨ Доглянуте авто", callback_data="category_good"))
    return keyboard

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=category_keyboard())

# Обработка выбора категории
@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
def category_chosen(call):
    categories = {
        "category_accident": "🔥 Після ДТП",
        "category_fire": "🔥 Після пожежі",
        "category_quick": "⏳ Швидка оцінка",
        "category_good": "✨ Доглянуте авто"
    }
    selected_category = categories.get(call.data, "❓ Не відомо")
    bot.send_message(
        call.message.chat.id,
        f"Ви обрали категорію: {selected_category}\n\n"
        "✍️ Будь ласка, надішліть ваше повідомлення у форматі:\n"
        "1️⃣ Пробіг авто (км)\n"
        "2️⃣ Короткий опис авто (стан кузова, мотор, особливості)\n"
        "3️⃣ Ваш Telegram або номер телефону\n\n"
        "📸 Можна додавати фото або відео для точної оцінки!"
    )

# Кнопка контактов
@bot.message_handler(commands=['contacts'])
def send_contacts(message):
    bot.send_message(
        message.chat.id,
        f"Наші контакти:\n📞 Телефон: {CONTACTS['Телефон']}\n📲 Telegram: {CONTACTS['Telegram']}"
    )

# Обработка всех сообщений (текст, фото, видео, документы)
@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def handle_client(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    category = "Категорія не вибрана"
    
    # Если пользователь выбирал категорию ранее
    # (можно расширить с сохранением состояния в dict, пока простая версия)
    
    for admin in ADMINS:
        # Текст
        if message.content_type == 'text':
            bot.send_message(admin, f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.text}")
        # Фото
        elif message.content_type == 'photo':
            photo_id = message.photo[-1].file_id
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Фото авто'}"
            bot.send_photo(admin, photo_id, caption=caption)
        # Видео
        elif message.content_type == 'video':
            caption = f"📩 Нова заявка від {user_name} (ID: {user_id}):\n\n{message.caption or 'Відео авто'}"
            bot.send_video(admin, message.video.file_id, caption=caption)
        # Документ
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
