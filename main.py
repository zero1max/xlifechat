import asyncio
import logging
import sys

from loader import dp, bot
from database.db_handlers import setup_users
import handlers

async def main():
    await setup_users()
    # Webhookni o‘chir
    await bot.delete_webhook(drop_pending_updates=True)
    # Bot pollingni boshlasin (sessiyani polling o‘zi boshqaradi)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
