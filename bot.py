import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
)
from collections import defaultdict

# Load questions
with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f)

# States for ConversationHandler
ASK_START, ASK_QUESTION = range(2)

CORRECT_ANIMATION = "✅"
WRONG_ANIMATION = "❌"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Please enter the question number you want to start from (1-{}):".format(len(QUESTIONS))
    )
    return ASK_START

async def ask_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        start_num = int(update.message.text)
        if not (1 <= start_num <= len(QUESTIONS)):
            raise ValueError
    except ValueError:
        await update.message.reply_text("Please enter a valid number between 1 and {}.".format(len(QUESTIONS)))
        return ASK_START
    context.user_data["current"] = start_num - 1
    return await ask_question(update, context)

def build_options_keyboard(options):
    # Use radio-style unicode for buttons
    return [
        [InlineKeyboardButton(f"⚪ {opt}", callback_data=str(i))] for i, opt in enumerate(options)
    ]

def build_stats_text(stats, q_idx, options):
    q_stats = stats.get(str(q_idx), {})
    total = sum(q_stats.get(str(i), 0) for i in range(len(options)))
    lines = []
    for i, opt in enumerate(options):
        count = q_stats.get(str(i), 0)
        percent = (count / total * 100) if total > 0 else 0
        lines.append(f"{opt} — {percent:.1f}%")
    lines.append(f"\nTotal attempts: {total}")
    return "\n".join(lines)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data.get("current", 0)
    if idx >= len(QUESTIONS):
        await update.message.reply_text("You've completed all questions! 🎉")
        return ConversationHandler.END

    q = QUESTIONS[idx]
    context.user_data["options"] = q["options"]
    keyboard = build_options_keyboard(q["options"])
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"Q{idx+1}: {q['question']}"
    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )
    return ASK_QUESTION

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idx = context.user_data.get("current", 0)
    q = QUESTIONS[idx]
    options = context.user_data.get("options", [])
    selected_idx = int(query.data)
    selected = options[selected_idx]
    correct = q["correct_answers"][0]
    explanation = q["explanation"]

    # Load and update stats
    stats = load_stats()
    q_stats = stats.get(str(idx), {})
    q_stats[str(selected_idx)] = q_stats.get(str(selected_idx), 0) + 1
    stats[str(idx)] = q_stats
    save_stats(stats)

    # Prepare feedback
    if selected == correct:
        feedback = f"{CORRECT_ANIMATION} Correct!\n\nExplanation: {explanation}\n"
    else:
        feedback = f"{WRONG_ANIMATION} Wrong!\n\nCorrect answer: {correct}\nExplanation: {explanation}\n"

    # Add stats
    stats_text = build_stats_text(stats, idx, options)
    feedback += "\n" + stats_text

    await query.edit_message_text(feedback)
    context.user_data["current"] = idx + 1

    # Ask next question
    if context.user_data["current"] < len(QUESTIONS):
        next_q = QUESTIONS[context.user_data["current"]]
        context.user_data["options"] = next_q["options"]
        keyboard = build_options_keyboard(next_q["options"])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"Q{context.user_data['current']+1}: {next_q['question']}"
        await query.message.reply_text(
            text,
            reply_markup=reply_markup
        )
        return ASK_QUESTION
    else:
        await query.message.reply_text("You've completed all questions! 🎉")
        return ConversationHandler.END

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    # TOKEN = "abcdefghijklmnopqrstuvwxyz"  # Replace with your actual bot token or set as environment variable
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_start)],
            ASK_QUESTION: [CallbackQueryHandler(handle_answer)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()