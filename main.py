import random

from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def suggest_random_food(category):
    """Randomly select dinner option based on user input. The user can either choose takeaways, cook or restaurant"""
    options = {
        "takeaways": ["KFC", "McDonalds", "BurgerKing", "Steers", "Chinese", "Nandos", "Debonairs"],
        "cook": [
            "Italian Pasta",
            "Cape Malay Curry",
            "Indian Curry",
            "Southern Fried Chicken",
            "Braai meat",
            "Stew",
            "a chicken wrap",
        ],
        "restaurant": [
            "Korean fried chicken at Gogi",
            "beef steak at the Hussar Grill",
            "a meal at CHEF's Foodhall",
            "sushi at the Blue Marlin Asian Cuisine & Sushi Bar",
        ],
    }
    if category in options:
        return random.choice(options[category])
    else:
        return "Invalid category."


async def dinner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create buttons so that user can select takeaways, cook or restaurant"""
    button_1 = InlineKeyboardButton("Take-aways", callback_data="takeaways")
    button_2 = InlineKeyboardButton("Cook", callback_data="cook")
    button_3 = InlineKeyboardButton("Restaurant", callback_data="restaurant")

    # Create a list of lists for the inline keyboard layout
    keyboard = [[button_1, button_2, button_3]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("What would you like to eat for dinner?", reply_markup=reply_markup)


async def dinner_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery."""
    query = update.callback_query

    if query.data in ["takeaways", "cook", "restaurant"]:
        category = query.data
        suggested_food = suggest_random_food(category)
        await query.message.reply_text(f"You chose {category}. How about having {suggested_food}?")
        await query.answer()
    else:
        await query.message.reply_text("Invalid choice.")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("ADD_TOKEN_HERE").build()

    # Create /start, /help and /dinner command,
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dinner", dinner))
    application.add_handler(CallbackQueryHandler(dinner_button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
