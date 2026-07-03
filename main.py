import pytz
import asyncio
from datetime import datetime
from telethon.sync import TelegramClient
from config import api_id, api_hash, timezone
from telethon.tl.functions.account import UpdateProfileRequest


async def update_profile():
    async with TelegramClient("session", api_id, api_hash) as client:
        while True:
            now = datetime.now(pytz.timezone(timezone))
            about_text = f"You will see this at {now.strftime('%H:%M')} ({timezone})"
            await client(UpdateProfileRequest(about=about_text))
            await asyncio.sleep(60)  # 60 seconds = 1 minute

if __name__ == "__main__":
    asyncio.run(update_profile())
