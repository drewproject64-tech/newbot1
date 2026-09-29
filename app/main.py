import logging

from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .config import Settings
from .handlers import start, help_command, handle_message, error_handler

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def configure_bot(application: Application):
    settings = application.bot_data["settings"]

    await application.bot.set_my_name(settings.bot_name)
    await application.bot.set_my_short_description(settings.short_description)
    await application.bot.set_my_description(settings.description)

    await application.bot.set_my_commands([
        BotCommand("start", "Open the main menu"),
        BotCommand("help", "How AlphaSort works"),
    ])

    logger.info(
        "Bot profile configured: %s %s",
        settings.bot_name,
        settings.bot_username,
    )

def build_application(settings: Settings) -> Application:
    application = (
        Application.builder()
        .token(settings.bot_token)
        .post_init(configure_bot)
        .build()
    )

    application.bot_data["settings"] = settings

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_error_handler(error_handler)

    return application

def main():
    settings = Settings.from_env()
    application = build_application(settings)

    logger.info("Starting SB24 AlphaSort Bot...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
