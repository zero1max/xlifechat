from aiogram import Dispatcher , Router, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from database.db_handlers import Database

TOKEN = '7795441407:AAHv3EyRB-XzcyTYxY598rxJ8lMpfl9VyKQ'

db = Database()
dp = Dispatcher()
router = Router()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.include_router(router=router)