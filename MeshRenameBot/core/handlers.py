from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import re
import time
import asyncio
import logging
import signal
from pyrogram.file_id import FileId
from ..utils.progress_for_pyro import progress_for_pyrogram
from ..translations.trans import Trans
from ..maneuvers.ExecutorManager import ExecutorManager
from ..maneuvers.Rename import RenameManeuver

renamelog = logging.getLogger(__name__)


def add_handlers(client: Client) -> None:
    """This function is responsible to manually register all the bot handlers.

    Args:
        client (pyrogram.Client): Initialized pyrogram client.
    """

    client.add_handler(MessageHandler(start_handler, filters.regex("/start", re.IGNORECASE)))
    client.add_handler(MessageHandler(rename_handler, filters.regex("/rename", re.IGNORECASE)))

    print("added")
    signal.signal(signal.SIGINT, term_handler)
    signal.signal(signal.SIGTERM, term_handler)

async def start_handler(client: Client, msg: Message) -> None:
    await msg.reply(Trans.START_MSG, quote=True)


async def rename_handler(client: Client, msg: Message) -> None:
    rep_msg = msg.reply_to_message
    print("in handler",rep_msg.media)
    await ExecutorManager().create_maneuver(RenameManeuver(client, rep_msg, msg))

def term_handler(signum, frame):
    print("yolo")
    ExecutorManager().stop()