import asyncio
import importlib
import psutil
import os
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AviaxMusic import LOGGER, app, userbot
from AviaxMusic.core.call import Aviax
from AviaxMusic.misc import sudo
from AviaxMusic.plugins import ALL_MODULES
from AviaxMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AviaxMusic.plugins" + all_module)
    LOGGER("AviaxMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Aviax.start()
    try:
        await Aviax.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AviaxMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Aviax.decorators()
    LOGGER("AviaxMusic").info(
        "\x41\x76\x69\x61\x78\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x41\x76\x69\x61\x78\x4f\x66\x66\x69\x63\x69\x61\x6c"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AviaxMusic").info("Stopping Aviax Music Bot...")


async def check_memory_usage():
    """Check memory usage and stop the process if it exceeds 500 MB."""
    while True:
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        print("RAM used:-",memory_usage)
        if memory_usage > 500:
            os.kill(os.getpid(), 9)  # Terminate the process
        
        await asyncio.sleep(60)  # Sleep for 60 seconds before checking again

async def main():
    asyncio.create_task(check_memory_usage())
    while True:
        await asyncio.sleep(1)# Start monitoring memory usage
    # Add other async tasks or the bot's main loop here if needed

async def run_both():
    await asyncio.gather(main(), init())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_both())
