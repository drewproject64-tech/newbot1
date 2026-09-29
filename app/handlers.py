import logging
from telegram import Update
from telegram.ext import ContextTypes

from .keyboards import SORT_MENU
from .sorter import sort_lines

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("sort_mode", None)
    await update.message.reply_text(
        context.bot_data["settings"].welcome_message,
        reply_markup=SORT_MENU,
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How it works:\n\n"
        "1. Choose Sort A–Z or Sort Z–A.\n"
        "2. Send one item per line.\n"
        "3. Receive the sorted result.\n\n"
        "Example:\nbanana\nApple\ncherry",
        reply_markup=SORT_MENU,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    if text == "Sort A–Z":
        context.user_data["sort_mode"] = False
        await update.message.reply_text(
            "A–Z sorting selected. Send the text you want to sort, with one item per line.",
            reply_markup=SORT_MENU,
        )
        return

    if text == "Sort Z–A":
        context.user_data["sort_mode"] = True
        await update.message.reply_text(
            "Z–A sorting selected. Send the text you want to sort, with one item per line.",
            reply_markup=SORT_MENU,
        )
        return

    if text == "How It Works":
        await help_command(update, context)
        return

    mode = context.user_data.get("sort_mode")
    if mode is None:
        await update.message.reply_text(
            "Choose Sort A–Z or Sort Z–A first, then send your text.",
            reply_markup=SORT_MENU,
        )
        return

    try:
        result, count = sort_lines(text, reverse=bool(mode))
        direction = "Z–A" if mode else "A–Z"
        await update.message.reply_text(
            f"Sorted {count} item{'s' if count != 1 else ''} ({direction}):\n\n{result}",
            reply_markup=SORT_MENU,
        )
    except ValueError as exc:
        await update.message.reply_text(str(exc), reply_markup=SORT_MENU)
    except Exception:
        logger.exception("Unexpected sorting error")
        await update.message.reply_text(
            "I couldn't process that text. Please try again with one item per line.",
            reply_markup=SORT_MENU,
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Unhandled Telegram update error", exc_info=context.error)
