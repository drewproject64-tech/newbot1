from telegram import ReplyKeyboardMarkup

SORT_MENU = ReplyKeyboardMarkup(
    [
        ["Sort A–Z", "Sort Z–A"],
        ["How It Works"],
    ],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Choose an action",
)
