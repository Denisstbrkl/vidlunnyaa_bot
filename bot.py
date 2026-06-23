import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://vidlunnya.site.je")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Перейти до магазину", url=WEBSITE_URL)],
        [InlineKeyboardButton("📦 Наш асортимент", callback_data='products')],
        [InlineKeyboardButton("🚚 Доставка та оплата", callback_data='delivery')],
        [InlineKeyboardButton("📞 Зв'язатися з нами", callback_data='contact')],
    ]
    await update.message.reply_text(
        "👋 Вітаємо у боті магазину *Відлуння*!\n\n"
        "Ми — локальний бренд українського одягу.\n"
        "Оберіть потрібний розділ:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    back_button = [[InlineKeyboardButton("◀️ Назад", callback_data='back')]]

    if query.data == 'products':
        keyboard = [
            [InlineKeyboardButton("🛍 Дивитись каталог", url=f"{WEBSITE_URL}/shop/")],
            [InlineKeyboardButton("◀️ Назад", callback_data='back')]
        ]
        await query.edit_message_text(
            "📦 *Наш асортимент*\n\n"
            "Ми пропонуємо якісний український одяг для жінок та чоловіків.\n\n"
            "Повний каталог з цінами — на сайті:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif query.data == 'delivery':
        await query.edit_message_text(
            "🚚 *Доставка та оплата*\n\n"
            "📫 *Доставка:* Нова Пошта по всій Україні\n"
            "💳 *Оплата:* карткою онлайн або накладений платіж\n"
            "⏱ *Термін:* 1–3 робочих дні\n\n"
            "✅ Безкоштовна доставка від 2 000 грн",
            reply_markup=InlineKeyboardMarkup(back_button),
            parse_mode='Markdown'
        )

    elif query.data == 'contact':
        await query.edit_message_text(
            "📞 *Зв'язатися з нами*\n\n"
            "Напишіть своє запитання прямо тут — менеджер відповість найближчим часом.\n\n"
            "Або завітайте на наш сайт:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Відкрити сайт", url=WEBSITE_URL)],
                [InlineKeyboardButton("◀️ Назад", callback_data='back')]
            ]),
            parse_mode='Markdown'
        )

    elif query.data == 'back':
        keyboard = [
            [InlineKeyboardButton("🛍 Перейти до магазину", url=WEBSITE_URL)],
            [InlineKeyboardButton("📦 Наш асортимент", callback_data='products')],
            [InlineKeyboardButton("🚚 Доставка та оплата", callback_data='delivery')],
            [InlineKeyboardButton("📞 Зв'язатися з нами", callback_data='contact')],
        ]
        await query.edit_message_text(
            "👋 Вітаємо у боті магазину *Відлуння*!\n\n"
            "Ми — локальний бренд українського одягу.\n"
            "Оберіть потрібний розділ:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📋 Головне меню", callback_data='back')]]
    await update.message.reply_text(
        "Дякуємо за повідомлення! 🙏\n"
        "Наш менеджер зв'яжеться з вами найближчим часом.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не встановлено!")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущено...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
