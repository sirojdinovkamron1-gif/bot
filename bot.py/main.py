import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8765027680:AAGPAmGeaj2ewrk1DteEKIGj7TTYUYPUNV8'
CHANNEL_USERNAME = '@Kamron_Ai_grop'

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
    except Exception:
        pass
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)

    # Agar a'zo bo'lmagan bo'lsa
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga qo'shilish", url="https://t.me/Kamron_Ai_grop")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data='check_sub')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "Botdan foydalanish uchun kanalimizga qo'shiling:\nhttps://t.me/Kamron_Ai_grop"
        
        if update.message:
            await update.message.reply_text(text, reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
        return

    # Agar a'zo bo'lgan bo'lsa ham, albatta kanal havolasini chiqarib, keyin darslarni beramiz
    keyboard = [
        [InlineKeyboardButton("📢 Kanalga o'tish", url="https://t.me/Kamron_Ai_grop")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "Manashu kanalga qo'shiling va darsni o'rganing:\nhttps://t.me/Kamron_Ai_grop\n\nYo'nalishni tanlang: 👇"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'check_sub':
        await start(update, context)
        return

    if data.startswith('cat_'):
        category = data.split('_')[1]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(f"📚 **{category.upper()}** darslari:", reply_markup=reply_markup, parse_mode='Markdown')

    elif data == 'back_to_main':
        await start(update, context)

    elif data.startswith('pdf_'):
        parts = data.split('_')
        category = parts[1]
        lesson_num = parts[2]
        
        pdf_path = f"pdfs/{category}_{lesson_num}.pdf"

        if os.path.exists(pdf_path):
            await query.message.reply_text(f"⏳ {category.upper()} {lesson_num}-dars yuklanmoqda...")
            with open(pdf_path, 'rb') as doc:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=doc,
                    caption=f"📘 **{category.upper()}** - {lesson_num}-dars"
                )
        else:
            await query.message.reply_text(f"⚠️ Fayl topilmadi (`pdfs/{category}_{lesson_num}.pdf`).", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot ishga tushdi...")
    app.run_polling()