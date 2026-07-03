import asyncio
import json
from datetime import datetime

import pytz
from telethon import TelegramClient, errors
from telethon.tl.functions.account import UpdateProfileRequest


# ---------- Logger (colored simple) ----------
class Log:
    @staticmethod
    def info(msg): print(f"\033[94m[INFO]\033[0m {msg}")
    @staticmethod
    def warn(msg): print(f"\033[93m[WARN]\033[0m {msg}")
    @staticmethod
    def ok(msg): print(f"\033[92m[OK]\033[0m {msg}")
    @staticmethod
    def err(msg): print(f"\033[91m[ERR]\033[0m {msg}")


# ---------- Load config ----------
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

api_id = config["api_id"]
api_hash = config["api_hash"]
timezone = config["timezone"]

update_mode = config["update_mode"]
interval = config["interval"]

bio_template = config["bio_template"]
name_template = config["name_template"]

use_emoji = config["use_emoji"]
safe_mode = config.get("safe_mode", True)


# ---------- Clock emoji ----------
time_texts = {
    0: "🕛", 1: "🕐", 2: "🕑", 3: "🕒", 4: "🕓", 5: "🕔",
    6: "🕕", 7: "🕖", 8: "🕗", 9: "🕘", 10: "🕙", 11: "🕚"
}


def get_time():
    now = datetime.now(pytz.timezone(timezone))
    hour = now.hour % 12
    emoji = time_texts.get(hour, "") if use_emoji else ""
    return now.strftime("%H:%M"), emoji


# ---------- Scheduler (safe interval control) ----------
async def safe_sleep(base):
    jitter = 3 if safe_mode else 0
    await asyncio.sleep(base + jitter)


# ---------- Core updater ----------
async def run():
    client = TelegramClient("session", api_id, api_hash)

    last_bio = None
    last_name = None

    while True:
        try:
            await client.connect()

            if not await client.is_user_authorized():
                Log.err("Session not authorized!")
                return

            Log.ok("Client connected")

            while True:
                time_str, emoji = get_time()

                bio = bio_template.format(time=time_str, emoji=emoji)
                name = name_template.format(time=time_str, emoji=emoji)

                # ---------- Skip duplicate updates ----------
                if bio == last_bio and name == last_name:
                    Log.info("No change detected, skipping update")
                    await safe_sleep(interval)
                    continue

                # ---------- Update bio ----------
                if update_mode in ("bio", "both"):
                    try:
                        await client(UpdateProfileRequest(about=bio))
                        Log.ok(f"Bio updated -> {bio}")
                    except errors.FloodWaitError as e:
                        Log.warn(f"FloodWait bio: sleep {e.seconds}s")
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        Log.err(f"Bio error: {e}")

                # ---------- Update name ----------
                if update_mode in ("name", "both"):
                    try:
                        me = await client.get_me()

                        await client(UpdateProfileRequest(
                            first_name=name,
                            last_name=me.last_name or ""
                        ))

                        Log.ok(f"Name updated -> {name}")

                    except errors.FloodWaitError as e:
                        Log.warn(f"FloodWait name: sleep {e.seconds}s")
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        Log.err(f"Name error: {e}")

                last_bio = bio
                last_name = name

                await safe_sleep(interval)

        except (ConnectionError, OSError) as e:
            Log.err(f"Connection lost: {e}")
            Log.warn("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

        except Exception as e:
            Log.err(f"Fatal error: {e}")
            await asyncio.sleep(10)


# ---------- Entry ----------
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        Log.warn("Stopped manually")
