import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_name: str = "SB24 AlphaSort Bot"
    bot_username: str = "@SB24AlphasortBot"

    @classmethod
    def from_env(cls):
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN environment variable is required.")
        return cls(bot_token=token)

    @property
    def short_description(self):
        return "Sort your text lines alphabetically from A–Z or Z–A."

    @property
    def description(self):
        return (
            "SB24 AlphaSort Bot sorts text lines alphabetically. "
            "Choose A–Z or Z–A, send your text, and receive the sorted result."
        )

    @property
    def welcome_message(self):
        return (
            "Welcome to SB24 AlphaSort Bot.\n\n"
            "Sort text lines alphabetically in seconds. "
            "Choose a sorting direction, then send the text you want to sort."
        )
